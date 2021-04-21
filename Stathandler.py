import os

import yaml


def write(name, special, weapon, lucky, total, wins, losses, draws, ones, twenties, luckies, seventeens, clashes):
    info = {"fnf": False, "name": name, "special": special, "weapon": weapon, "lucky": lucky, "total": total, "wins": wins,
            "losses": losses, "draws": draws, "ones": ones, "twenties": twenties, "luckies": luckies,
            "seventeens": seventeens, "clashes": clashes}
    with open("./players/" + str(name) + ".yml", 'w') as f:
        yaml.dump(info, f)


def read(name):
    try:
        with open("./players/" + str(name) + ".yml") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data
    except:
        return {"fnf": True}


def readluckies():
    luckies = {}
    for filename in os.listdir("./players/"):
        with open("./players/" + filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            luckies[data["name"]] = data["lucky"]
    return luckies

# Outcomes:
# 0 - Win
# 1 - Loss
# 2 - Draw
def updatestats(name, outcome, twenties, ones, luckies, seventeens, clash):
    data = {}
    with open("./players/" + str(name) + ".yml") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    with open("./players/" + str(name) + ".yml", "w") as f:
        data["twenties"] += twenties
        data["ones"] += ones
        data["luckies"] += luckies
        data["seventeens"] += seventeens
        data["clash"] += clash
        data["total"] += 1
        if outcome is 0:
            data["wins"] += 1
            data["losses"] += 1
            data["draws"] += 1
