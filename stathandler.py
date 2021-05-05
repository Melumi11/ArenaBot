import os
from os import path

# change to csv

def write(name, special, weapon, lucky, total, wins, losses, draws, ones, twenties, luckies, seventeens, clashes):
    info = str(name) + "," + str(special) + "," + str(weapon) + "," + str(lucky) + "," + str(total) + "," + str(wins) + "," + str(losses) + "," + str(draws) + "," + str(ones) + "," + str(twenties) + "," + str(luckies) + "," + str(seventeens) + "," + str(clashes)
    with open("./players/" + str(name) + ".csv", "w") as f:
        f.write(info)

def read(name):
    try:
        with open("./players/" + str(name) + ".csv") as f:
            return [True, f.read().split(",")]
    except:
        return [False]

def readluckies():
    luckies = {}
    for filename in os.listdir("./players/"):
        with open("./players/" + filename) as f:
            luckies.pop(filename.replace(".csv", ""), int(f.read().split(",")[3]))
    return luckies

def updatestats(name, outcome, twenties, ones, luckies, seventeens, clash):
    data = read(name)
    # if data
# read and update
