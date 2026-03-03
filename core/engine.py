from typing import List, Any
from contracts import DataSink, PipelineService
import pandas as pd
from functools import reduce
from utility import *


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def fillNull(self,index,rds): #raw data set
        exclude = ["Indicator_Name", "Indicator_Code","Country_Name", "Country_Code","Continent"]
        fields = [col for col in rds.columns if col not in exclude]
        row = rds.loc[index].copy()
        yearVals = list(row[fields])
        valid = list(filter(lambda w: pd.notna(w) and isinstance(w, (int, float)) and w > 0, yearVals))
        mean = (reduce(lambda e,i: e + i, valid)/len(valid)) if valid else 0
        filledCols = row[fields].fillna(mean)
        return pd.concat([row.drop(fields), filledCols])

    def cleanData(self, rds):
        ds = pd.DataFrame(
            [self.fillNull(index, rds) for index in rds.index],
            index=rds.index
        )
        return ds
                                   
    def filterAttributes(self,index, ds, year):
        row = ds.loc[index].copy()
        cols = ["Country Name", "Country Code", "Continent"]
        attributes = safeExtend(cols,year)
        return pd.Series(row[attributes].values, index=attributes)

    def filterData(self,ds, region, year):
        filteredData = filter(lambda t: getattr(t, "Continent", None) == region, ds.itertuples())
        rows = list(map(lambda t: self.filterAttributes(t.Index, ds, year), filteredData))
        cols = ["Country Name", "Country Code", "Continent"]
        attributes = safeExtend(cols,year)
        return pd.DataFrame(rows, columns=attributes)



    def statistics(self,fds,op,year):
        sum = reduce(lambda e,i: e + i, fds.loc[:, year].dropna().tolist())
        if op == "sum":
            return sum
        else:
            return sum/(len(fds)*1.0)

    def execute(self, raw_data: List[Any]) -> None:

        ds = self.cleanData(raw_data)
        stat = self.statistics(fds,self.config["operation"],self.config["year"])
        results = {
        "top_10": self.top10(ds, self.config["region"], self.config["year"]),
        "bottom_10": self.bottom10(ds, self.config["region"], self.config["year"]),
        "growth_rates": self.growthRates(ds,self.config["region"],self.config["start_year"],self.config["end_year"]),
        "avg_by_continent": self.avgByContinent(ds,self.config["start_year"],self.config["end_year"]),
        "global_trend": self.globalTrend(ds,self.config["start_year"],self.config["end_year"]),
        "fastest_continent": self.fastestContinent(ds,self.config["start_year"],self.config["end_year"]),
        "decline_countries": self.consistentDecline(ds,self.config["region"],self.config["end_year"],self.config["decline_years"]),
        "contribution": self.contribution(ds,self.config["start_year"],self.config["end_year"])
    }
        #self.sink.write(results)