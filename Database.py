#Database format
#IsleBot
#   data
#       user_metrics
#       beatmapsets
#       beatmaps

import os
from dotenv import load_dotenv
import ossapi
import pymongo as mongo

load_dotenv()

client_id = int(os.getenv("CLIENT_ID"))
client_secret = str(os.getenv("CLIENT_SECRET"))
api = ossapi.Ossapi(client_id, client_secret)

database_uri = str(os.getenv("DATABASE_URI"))
client = mongo.MongoClient(database_uri)

#databases are created when you read/write on them
db = client["data"]
# user_metrics = db["user_metrics"]
beatmapsets = db["beatmapsets"]
beatmaps = db["beatmaps"]

def database_setup():
    beatmapsets.create_index([("beatmapset_id", mongo.ASCENDING)], unique=True)
    beatmaps.create_index([("beatmap_id", mongo.ASCENDING)], unique=True)

def is_beatmap_cached(beatmap_id):
    if beatmaps.find_one({'beatmap_id': int(beatmap_id)}) == None:
        return False
    return True

def cache_beatmap(beatmap_id, beatmap, version, acc_max, acc_99, acc_98, acc_95, sr, od, hp, hit_length):
    if is_beatmap_cached(beatmap_id):
        return
    
    beatmap_data = {
        'beatmap_id': int(beatmap_id),
        'beatmapset_id': int(beatmap.beatmapset_id),
        'version': str(version),
        'acc_max': int(acc_max),
        'acc_99': int(acc_99),
        'acc_98': int(acc_98),
        'acc_95': int(acc_95),
        'sr': int(sr),
        'od': int(od),
        'hp': int(hp),
        'hit_length': int(hit_length),
    }
    beatmaps.insert_one(beatmap_data)


def cache_beatmapset(beatmapset_id, artist, title, beatmap_ids):
    beatmapset_data = {
        'beatmapset_id': int(beatmapset_id),
        'artist': str(artist),
        'title': str(title),
        'beatmap_ids': list(beatmap_ids),
    }

print(is_beatmap_cached(1))