import requests
import ossapi as osu
import os
from dotenv import load_dotenv

load_dotenv()

client_id = int(os.getenv("CLIENT_ID"))
client_secret = str(os.getenv("CLIENT_SECRET"))
    
api = osu.Ossapi(client_id, client_secret)

set = api.beatmapset(1)
if set.status == osu.enums.RankStatus.RANKED:
    print("ranked")