import json


def readConfig():
    with open("config.jason", "r") as f:
        config = json.load(f)
    return config

config = readConfig()

def validateConfig():
    



print(config["region"])