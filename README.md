# PyTwitch
A collection of tools and utilities for easier interaction with Twitch.

# Examples

### Chat
```python
from pytwitchinteract.chat import TwitchChat

def memes(message):
    message.reply("Thank you for the memes @{}!".format(message.sender))

chat = TwitchChat("oauth:YOUR_TOKEN", "YOUR_CHANNEL")
chat.register_command("memes", memes)
chat.listen()
```

# OAuth Token
You can get your Twitch OAuth token from here: https://twitchapps.com/tmi/