import requests
import os
from dotenv import load_dotenv
import ossapi
import rosu_pp_py as rosu

load_dotenv()

client_id = int(os.getenv("CLIENT_ID"))
client_secret = str(os.getenv("CLIENT_SECRET"))
api = ossapi.Ossapi(client_id, client_secret)

class Beatmap():
    def __init__(self, beatmap_id):
        difficulty = api.beatmap(beatmap_id)

        self.version = difficulty.version
        self.data = api.beatmapset(difficulty.beatmapset_id)

        if not (difficulty.mode == ossapi.enums.GameMode.MANIA):
            raise Exception("Not a mania difficulty")
        if not (difficulty.status == ossapi.enums.RankStatus.RANKED or difficulty.status == ossapi.enums.RankStatus.APPROVED):
            raise Exception("Difficulty is not ranked")
        
        difficulty_url = "https://osu.ppy.sh/osu/" + str(difficulty.id)

        try:
            filename = "./difficulties/" + str(difficulty.id) + ".osu"

            if not os.path.exists(filename): #dont overwrite if file has been downloaded, as they don't change
                response = requests.get(difficulty_url)
                with open(filename, "w", encoding=response.encoding) as file:
                    lines = response.text.split("\n")
                    for line in lines:
                        file.write(line)
                    # file.flush()

            rosu_difficulty = None
            with open(filename, encoding='utf-8') as file:
                rosu_difficulty = rosu.Beatmap(content = file.read()) #doesn't have to be converted as mode is already in the file

            #cache these using mongodb, as well as w mods etc
            #values can be improved but its fine for now
            max_geki = difficulty.count_circles + difficulty.count_sliders
            diff_calc = rosu.Performance(accuracy = 100,
                                         n_geki=max_geki,
                                         lazer=False).calculate(rosu_difficulty)

            rosu_perf = rosu.Performance(accuracy = 100, n_geki=max_geki, lazer=False)
            self.acc_max = rosu_perf.calculate(rosu_difficulty).pp

            rosu_perf.set_n_geki((max_geki * 3) // 4) # 3:1 ratio for max to 300
            
            rosu_perf.set_accuracy(99)
            self.acc_99 = rosu_perf.calculate(rosu_difficulty).pp

            rosu_perf.set_accuracy(98)
            self.acc_98 = rosu_perf.calculate(rosu_difficulty).pp

            rosu_perf.set_accuracy(95)
            self.acc_95 = rosu_perf.calculate(rosu_difficulty).pp
            
            self.sr = diff_calc.difficulty.stars
            self.od = rosu_difficulty.od
            self.hp = rosu_difficulty.hp
            self.hit_length = difficulty.hit_length

            # print(diff_calc.difficulty)
            # print(diff_calc)

        except Exception as e:
            raise e
        

def beatmapset_to_beatmap(beatmapset_id):
    difficulties = api.beatmapset(beatmapset_id).beatmaps

    highest_sr = max(difficulties, key=lambda x: x.difficulty_rating).difficulty_rating

    for difficulty in difficulties:
        if difficulty.difficulty_rating == highest_sr:
            return Beatmap(difficulty.id)