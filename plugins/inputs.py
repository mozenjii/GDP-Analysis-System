import pandas as pd
from core.contracts import PipelineService


class ExcelReader:

    def __init__(self, service: PipelineService):
        self.service = service

    def run(self):
        data = pd.read_excel("data/gdp_with_continent_filled.xlsx")
        self.service.execute(data)