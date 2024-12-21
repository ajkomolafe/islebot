#requirements: python-dotenv (not dotenv), irc, sqlite
#when running, use python and not py b/c py installation doesn't have dotenv
import os
from dotenv import load_dotenv 
import islebot

load_dotenv()
username = str(os.getenv("SERVER_USERNAME")) #aka nickname/realname
server = str(os.getenv("SERVER"))
server_backup = str(os.getenv("SERVER_BACKUP"))
server_port = int(os.getenv("SERVER_PORT"))
server_password = str(os.getenv("SERVER_PASSWORD"))

isle_bot = islebot.IsleBot(username, server, server_backup, server_port, server_password)
isle_bot.start()