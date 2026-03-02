from typing import List


class ConsoleWriter:

    def write(self, records: List[dict]) -> None:
        print("=== OUTPUT ===")
        for record in records:
            print(record)