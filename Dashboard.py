import json


def readConfig():
    with open("config.jason", "r") as f:
        config = json.load(f)
    return config

config = readConfig()

def validateConfig():
    print("Validating the configuration file...")
    #checking the required fields
    requiredKeys = ["region", "year", "operation", "output"]
    for key in requiredKeys:
        if key not in config:
            raise ValueError(f"Missing Value: {key}")

    #checking the appropriate data types
    if not isinstance(config["region"], str):
        raise TypeError("Region must be a string")
    if not isinstance(config["year"], int):
        raise TypeError("Year must be an integer")
    if not isinstance(config["operation"], str):
        raise TypeError("Operation must be a string")
    if not isinstance(config["output"], str):
        raise TypeError("Output must be a string")

    #checking appropriate Values
    if config["operation"] == "average" or "sum":
        raise ValueError("Undefined Operation detected!")
    print("Successful")



print(config["region"])