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
