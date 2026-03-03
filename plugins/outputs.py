from typing import List
import matplotlib.pyplot as plt

class ConsoleWriter:

    def write(self, records: List[dict]) -> None:
        print("=== OUTPUT ===")
        for record in records:
            print(record)


