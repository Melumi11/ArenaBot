import os
from os import path
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

def updatestats(name, outcome, twenties, ones, luckies, seventeens, clash):
    data = read(name)
    if data["fnf"]:
        with open("./players/" + str(name) + ".yml", "w") as f:
            yaml.dump(
                {"fnf": False, "name": name, "special": "unknown", "weapon": "unknown", "lucky": 1, "total": 0,
                 "wins": 0, "losses": 0, "draws": 0, "ones": 0, "twenties": 0, "luckies": 0, "seventeens": 0,
                 "clashes": 0}, f)
        data = read(name)
    origtwenties = int(data["twenties"])
    origones = int(data["ones"])
    origluckies = int(data["luckies"])
    origseventeens = int(data["seventeens"])
    origclash = int(data["clashes"])
    origtotal = int(data["total"])
    data["twenties"] = origtwenties + twenties
    data["ones"] = origones + ones
    data["luckies"] = origluckies + luckies
    data["seventeens"] = origseventeens + seventeens
    data["clashes"] = origclash + clash
    data["total"] = origtotal + 1
    if outcome == 0:
        origwins = int(data["wins"])
        data["wins"] = origwins + 1
    elif outcome == 1:
        origwins = int(data["losses"])
        data["losses"] = origwins + 1
    elif outcome == 2:
        origwins = int(data["draws"])
        data["draws"] = origwins + 1
    with open("./players/" + str(name) + ".yml", "r+") as f:
        f.truncate(0)
        yaml.dump(data, f)
