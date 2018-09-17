from multiprocessing import Process, Value
import socket
import re


MESSAGE_PATTERN = re.compile("^:([^\n\s]+?)\s([^\n\s]+?)\s([^\n\s]+?)\s:([^\n]+?)$")
SENDER_PATTERN = re.compile("^(.+?)!")


class TwitchChat:

    def __init__(self, token, channel, host='irc.twitch.tv', port=6667, verbose=False, debug=False):
        self.token = token
        self.channel = channel
        self.host = host
        self.port = port
        self.verbose = verbose
        self.debug = debug
        self.running = Value('i', 0)
        self.commands = []

        if not token.startswith("oauth:"):
            self.token = "oauth:" + self.token

        if not channel.startswith("#"):
            self.channel = "#" + self.channel

    def __reconnect(self):
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()

        self.connection = socket.socket()
        self.connection.settimeout(1)
        self.connection.connect((self.host, self.port))

        if self.verbose:
            print("Connection established with:", (self.host, self.port))

        self.__send_message("PASS {}".format(self.token))

        # Nickname doesn't actually matter, only requires to be sent
        self.__send_message("NICK PyTwitch")

        authentication = Message(self, self.connection.recv(1024).decode('UTF-8').split('\n')[0])

        if 'failed' in authentication.content:
            raise Exception(authentication.content)

        if self.verbose:
            print("Authenticated successfully:", authentication.content)

        self.__send_message("JOIN {}".format(self.channel))

        if self.verbose:
            print("Joined channel:", self.channel)

    def __send_message(self, message):
        if self.verbose:
            print("Sending:", message.replace(self.token, '***'))

        self.connection.send(bytes('{}\r\n'.format(message), 'UTF-8'))

    def send_chat_message(self, message):
        self.__send_message("PRIVMSG {} :{}".format(self.channel, message))

    def register_command(self, command, callback, prefix='!', beginning=True):
        self.commands.append(Command(prefix, command, beginning, callback))

    def listen(self, async=False):
        if async:
            p = Process(target=self._listen_internal, args=(self.running,))
            p.start()
        else:
            self._listen_internal(self.running)

    def _listen_internal(self, running):
        running.value = 1

        self.__reconnect()

        if self.verbose:
            print("Listening to chat")

        line = ""
        while running.value == 1:
            try:
                line += self.connection.recv(1).decode('UTF-8', 'replace')
                if line[-2:] == '\r\n':
                    print("Received:", line.encode('utf-8').rstrip())
                    try:
                        if line.startswith("PING :tmi.twitch.tv"):
                            self.__send_message("PONG tmi.twitch.tv")

                        else:
                            msg = Message(self, line[:-2])
                            for command in self.commands:
                                matches = command.matches(msg)
                                if len(matches) > 0:
                                    command.callback(msg, matches)
                    except MessageProcessException as e:
                        if self.debug:
                            print(e)

                    line = ""
            except socket.timeout:
                pass

    def stop_listening(self):
        self.running.value = 0


class Message:

    def __init__(self, chat, message):
        self.chat = chat

        if not isinstance(message, str):
            raise Exception("Message not a string")

        data = MESSAGE_PATTERN.search(message)

        if data is None:
            raise MessageProcessException(message)

        self.sender = data.group(1)
        self.type = data.group(2)
        self.target = data.group(3)
        self.content = data.group(4)

        if self.content[-1] == '\r':
            self.content = self.content[:-1]

        user = SENDER_PATTERN.search(self.sender)

        if user is not None:
            self.sender = user.group(1)

    def reply(self, message):
        self.chat.send_chat_message(message)


class MessageProcessException(Exception):

    def __init__(self, message):
        Exception.__init__(self, "Failed to process message: '{}'".format(message))


class Command:

    def __init__(self, prefix, command, beginning, callback):
        if not isinstance(command, list):
            command = [command]

        self.prefix = prefix
        self.command = command
        self.beginning = beginning
        self.callback = callback

        regex = "(?:(?:(?<=\s)|(?<=^))({})(?:(?=\s)|(?=$)))+".format("|".join(list(map(lambda z: re.escape(prefix) + re.escape(z), command))))

        if beginning:
            self.matcher = re.compile("^" + regex)
        else:
            self.matcher = re.compile(regex)

    def matches(self, message):
        return self.matcher.findall(message.content)
