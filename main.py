import json
from core import TransformationEngine
from plugins.inputs import ExcelReader, CSVReader
from plugins.outputs import ConsoleWriter, GraphicsChartWriter

INPUT_DRIVERS = {
    "excel": ExcelReader,
    "csv" : CSVReader
}

OUTPUT_DRIVERS = {
    "console": ConsoleWriter,
    "dashboard": GraphicsChartWriter
}

def readConfig():
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("COnfiguration File not found!")
    return config

def validateConfig(config):
    print("Validating the configuration file...")
    #checking the required fields
    requiredKeys = ["region", "year", "operation", "output","input", "start_year","end_year","decline_years"]
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
    if not isinstance(config["end_year"], int):
        raise TypeError("End Year must be an integer")
    if not isinstance(config["start_year"], int):
        raise TypeError("Start Year must be an integer")
    if not isinstance(config["decline_years"], int):
        raise TypeError("Decline Years must be integers")
    
    if config["operation"] not in ["average", "sum"]:
        raise ValueError("Undefined Operation detected!")
    print("Successful")

    

def bootstrap():

    config = readConfig()
    validateConfig(config)

    sink_class = OUTPUT_DRIVERS[config["output"]]
    sink = sink_class()

    engine = TransformationEngine(sink, config)

    input_class = INPUT_DRIVERS[config["input"]]
    reader = input_class(engine)

    reader.run()


if __name__ == "__main__":
    bootstrap()