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


def bootstrap():

    with open("config.json") as f:
        config = json.load(f)

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