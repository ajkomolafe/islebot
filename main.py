#requirements: python-dotenv (not dotenv), irc, sqlite
#when running, use python and not py b/c py installation doesn't have dotenv
import os
import irc.bot
from dotenv import load_dotenv
import re
import islebeatmap

class IsleBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, server, server_backup, port, password):
        BanchoIRC = irc.bot.ServerSpec(server, port, password)
        BanchoCHO = irc.bot.ServerSpec(server_backup, port, password)
        irc.bot.SingleServerIRCBot.__init__(self, [BanchoIRC, BanchoCHO], username, username)
        print("Connected to bancho.")
        #todo: check on if the thing rejoins on disconnect

    # def on_welcome(self, c, e):
    #     c.join("#osu")

    # def _on_mode(self, c, e):
    #     print(e)

    def on_ctcp(self, c, e):
        self.handle_beatmap_link(c, e, e.arguments[1])

    # def on_pubmsg(self, c, e):
    #     print(f"{e.source.nick}: {e.arguments[0].lower()}")
    
    def handle_beatmap_link(self, c, e, message):
        osu_url_regex = r"https?://osu\.ppy\.sh/beatmapsets/[\da-zA-Z#/]*\b"
        beatmapset_urls = re.findall(osu_url_regex, message)
        if len(beatmapset_urls) >= 1:
            beatmapset_url = beatmapset_urls[0]
            if '#' in beatmapset_url: 
                #Specific difficulty given
                beatmap = None
                try:
                    hashtag_index = beatmapset_url.index('#')
                    beatmap_id = int(beatmapset_url[hashtag_index+2:])
                    beatmap = islebeatmap.Beatmap(beatmap_id)
                    output_message = f"[{beatmapset_url} {beatmap.data.artist_unicode} - {beatmap.data.title_unicode} [{beatmap.version}]] | All MAX: {beatmap.acc_100:.2f}pp | 99%: {beatmap.acc_99:.2f}pp | 97%: {beatmap.acc_97:.2f}pp | 95%: {beatmap.acc_95:.2f}pp ♥"
                    c.privmsg(e.source.nick, output_message)
                    print(f"Message to {e.source.nick}: {output_message}")

                except Exception as e:
                    print("Error: " + repr(e))
                    return
                
            else: 
                #Beatmapset only
                beatmapset_url = beatmapset_url.replace("https://", '').replace("http://", '')
                beatmapset_url = beatmapset_url.replace("osu.ppy.sh/", '')
                beatmapset_url = beatmapset_url.replace("beatmapsets/", '')
                try:
                    hashtag_index = beatmapset_url.index('#')
                    beatmapset_url = beatmapset_url[:hashtag_index]
                except Exception:
                    print("Error: " + repr(e))
                    return

    def on_privmsg(self, c, e):
        # if e.target == self.connection.get_nickname(): #if i am target of message
            sender = e.source.nick
            input_message = e.arguments[0].lower()
        
            if '♥' in input_message: #from me
                return

            self.handle_beatmap_link(c, e, e.arguments[0])

            if (not input_message.startswith("!")) and sender != self.connection.get_nickname():
                output_message = "Hi, I'm isle."
                c.privmsg(sender, "Hi, I'm isle.")
                print(f"Message to {e.source.nick}: {output_message}")

            elif input_message.startswith("!h"): #!help
                output_message = "Hi, I'm isle. You can /np mania beatmaps or type !recommend for a recommend beatmap."
                c.privmsg(sender, output_message)
                print(f"Message to {e.source.nick}: {output_message}")

            elif input_message.startswith("!r"): #!recommend
                output_message = "Hi, I'm isle. This command is WIP."
                c.privmsg(sender, output_message)
                print(f"Message to {e.source.nick}: {output_message}")

load_dotenv()
username = str(os.getenv("SERVER_USERNAME")) #aka nickname/realname
server = str(os.getenv("SERVER"))
server_backup = str(os.getenv("SERVER_BACKUP"))
server_port = int(os.getenv("SERVER_PORT"))
server_password = str(os.getenv("SERVER_PASSWORD"))
l = [username, server, server_backup, server_port, server_password]

isleBot = IsleBot(username, server, server_backup, server_port, server_password)
isleBot.start()