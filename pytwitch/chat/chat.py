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
        self.running = True
        self.commands = []

        if not token.startswith("oauth:"):
            self.token = "oauth:" + self.token

        if not channel.startswith("#"):
            self.channel = "#" + self.channel

    def __reconnect(self):
        if hasattr(self, 'connection') and self.connection is not None:
            self.connection.close()

        self.connection = socket.socket()
        self.connection.connect((self.host, self.port))

        self.__send_message("PASS {}".format(self.token))

        # Nickname doesn't actually matter, only requires to be sent
        self.__send_message("NICK PyTwitch")

        authentication = Message(self, self.connection.recv(1024).decode('UTF-8').split('\n')[0])

        if 'failed' in authentication.content:
            raise Exception(authentication.content)

        self.__send_message("JOIN {}".format(self.channel))

    def __send_message(self, message):
        if self.verbose:
            print("Sending:", message.replace(self.token, '***'))

        self.connection.send(bytes('{}\r\n'.format(message), 'UTF-8'))

    def send_chat_message(self, message):
        self.__send_message("PRIVMSG {} :{}".format(self.channel, message))

    def register_command(self, command, callback, prefix='!'):
        self.commands.append(Command(prefix, command, callback))

    def listen(self):
        self.running = True

        self.__reconnect()

        line = ""
        while self.running:
            line += self.connection.recv(1).decode('UTF-8')
            if line[-2:] == '\r\n':
                try:
                    msg = Message(self, line[:-2])
                    for command in self.commands:
                        if command.matches(msg):
                            command.callback(msg)
                except MessageProcessException as e:
                    if self.debug:
                        print(e)

                line = ""

    def stop(self):
        self.running = False


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

    def __init__(self, prefix, command, callback):
        self.prefix = prefix
        self.command = command
        self.callback = callback
        self.matcher = re.compile("{}{}.*".format(prefix, command))

    def matches(self, message):
        return self.matcher.search(message.content) is not None
