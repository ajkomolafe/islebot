#requirements: python-dotenv (not dotenv), irc, sqlite
#when running, use python and not py b/c py installation doesn't have dotenv
import os
import irc.bot
from dotenv import load_dotenv

class IsleBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, server, server_backup, port, password):
        BanchoIRC = irc.bot.ServerSpec(server, port, password)
        BanchoCHO = irc.bot.ServerSpec(server_backup, port, password)
        irc.bot.SingleServerIRCBot.__init__(self, [BanchoIRC, BanchoCHO], username, username)
        print("Connected to bancho.")
        #todo: check on if the thing rejoins on disconnect

    def on_privmsg(self, c, e):
        if e.target == self.connection.get_nickname(): #if i am target of message
            sender = e.source.nick
            message = e.arguments[0].lower()

            # Process the message (example: respond to "!hello")
            if not message.startswith("!"):
                c.privmsg(sender, "Hi, I'm isle.")

            elif message.startswith("!h"): #!help
                c.privmsg(sender, f"Hi, I'm isle. The only command I have currently is !r.")

            elif message.startswith("!r"): #!recommend
                 c.privmsg(sender, f"Hi, I'm isle. The only command I have currently is !r.")

load_dotenv()
username = str(os.getenv("SERVER_USERNAME")) #aka nickname/realname
server = str(os.getenv("SERVER"))
server_backup = str(os.getenv("SERVER_BACKUP"))
server_port = int(os.getenv("SERVER_PORT"))
server_password = str(os.getenv("SERVER_PASSWORD"))
l = [username, server, server_backup, server_port, server_password]
print(l)

isleBot = IsleBot(username, server, server_backup, server_port, server_password)
isleBot.start()