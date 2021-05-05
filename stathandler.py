import os

# writes data to csv table
def write(name, special, weapon, lucky, total, wins, losses, draws, ones, twenties, luckies, seventeens, clashes):
    info = str(name) + "," + str(special) + "," + str(weapon) + "," + str(lucky) + "," + str(total) + "," + str(wins) + "," + str(losses) + "," + str(draws) + "," + str(ones) + "," + str(twenties) + "," + str(luckies) + "," + str(seventeens) + "," + str(clashes)
    with open("./players/" + str(name) + ".csv", "w") as f:
        f.write(info)

# reads data from csv table, returning [True, [data]] if it exists and [False] if not
def read(name):
    try:
        with open("./players/" + str(name) + ".csv") as f:
            return [True, f.read().split(",")]
    except:
        return [False]

# reads data from csv table, retuning an integer with the value of the fourth cell of the table
def readluckies():
    luckies = {}
    for filename in os.listdir("./players/"):
        with open("./players/" + filename) as f:
            luckies[int(filename.replace(".csv", ""))] = int(f.read().split(",")[3])
    return luckies

# reads data from csv table, if no table exists creates default table, then rereads table and updates statistics accordingly
# for outcomes: 0 = win, 1 = loss, 2 = draw
def updatestats(name, outcome, twenties, ones, luckies, seventeens, clash):
    data = read(name)
    if not data[0]:
        write(name, "Unknown", "Unknown", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0")
    data = read(name)[1]
    if outcome == 0:
        data[6] = int(data[6]) + 1
    elif outcome == 1:
        data[5] = int(data[5]) + 1
    else:
        data[7] = int(data[7]) + 1
    data[4] = int(data[4]) + 1
    data[8] = int(data[8]) + int(ones)
    data[9] = int(data[9]) + int(twenties)
    data[10] = int(data[10]) + int(luckies)
    data[11] = int(data[11]) + int(seventeens)
    data[12] = int(data[12]) + int(clash)
    datastring = ""
    for val in data:
        datastring += str(val) + ","
    datastring.removesuffix(",")
    with open("./players/" + str(name) + ".csv", "w") as f:
        f.write(datastring)
