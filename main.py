import json
from core.engine import TransformationEngine
from plugins.inputs import ExcelReader
from plugins.outputs import ConsoleWriter

INPUT_DRIVERS = {
    "excel": ExcelReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter
}

def readConfig():
    try:
        with open("config.jason", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("COnfiguration File not found!")
    return config

def validateConfig(config):
    print("Validating the configuration file...")
    #checking the required fields
    requiredKeys = ["region", "year", "operation", "output","input"]
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
    if not isinstance(config["input"], str):
        raise TypeError("Input must be a string")
    
    if config["operation"] == "average" or "sum":
        raise ValueError("Undefined Operation detected!")
    print("Successful")

    

def bootstrap():


    config = readConfig()
    validateConfig(config)



    # Create output
    sink_class = OUTPUT_DRIVERS[config["output"]]
    sink = sink_class()

    # Create engine (inject sink)
    engine = TransformationEngine(sink, config)

    # Create input (inject engine)
    input_class = INPUT_DRIVERS["excel"]
    reader = input_class(engine)

    # Run
    reader.run()


if __name__ == "__main__":
    bootstrap()