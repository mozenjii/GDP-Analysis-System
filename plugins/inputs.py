import pandas as pd
from core.contracts import PipelineService


class ExcelReader:

    def __init__(self, service: PipelineService):
        self.service = service

    def loadData():
        try:
            loadedData = pd.read_excel("data/gdp_with_continent_filled.xlsx")
        except FileNotFoundError:
            raise FileNotFoundError("Error: ""GDP with continent data"" file not found!")
        return loadedData

    def restructureData(loadedData):
        exclude = ["Indicator_Name", "Indicator_Code"]
        rds = loadedData[[col for col in loadedData.columns if col not in exclude]].copy()
        if rds.empty:
            raise CustomError("Restructuring Failed!")
        return rds


    def run(self):
        loadedData = self.loadData()
        data = self.restructureData(loadedData)
        self.service.execute(data)


class CsvReader:
    def __init__(self, service: PipelineService):
        self.service = service

    def loadData(self):
        try:
            loadedData = pd.read_csv("data/gdp_with_continent_filled.csv")
        except FileNotFoundError:
            raise FileNotFoundError("Error: 'GDP with continent data' CSV file not found!")
        return loadedData

    def restructureData(self, loadedData):
        exclude = ["Indicator_Name", "Indicator_Code"]
        rds = loadedData[[col for col in loadedData.columns if col not in exclude]].copy()
        if rds.empty:
            raise CustomError("Restructuring Failed!")
        return rds

    def run(self):
        loadedData = self.loadData()
        data = self.restructureData(loadedData)
        self.service.execute(data)
