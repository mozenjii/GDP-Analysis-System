from typing import List, Any
from contracts import DataSink, PipelineService
import pandas as pd
from functools import reduce
from utility import *


class TransformationEngine(PipelineService):

    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    def fillNull(index,rds): #raw data set
        exclude = ["Indicator_Name", "Indicator_Code","Country_Name", "Country_Code","Continent"]
        fields = [col for col in rds.columns if col not in exclude]
        row = rds.loc[index].copy()
        yearVals = list(row[fields])
        valid = list(filter(lambda w: pd.notna(w) and isinstance(w, (int, float)) and w > 0, yearVals))
        mean = (reduce(lambda e,i: e + i, valid)/len(valid)) if valid else 0
        filledCols = row[fields].fillna(mean)
        return pd.concat([row.drop(fields), filledCols])

    def cleanData(rds):
        ds = pd.DataFrame(list(map(lambda index: self.fillNull(index, rds), rds.index)), index=rds.index, columns=rds.columns) #dataset
        return ds

                                   
    def filterAttributes(index, ds, year):
        row = ds.loc[index].copy()
        cols = ["Country Name", "Country Code", "Continent"]
        attributes = safeExtend(cols,year)
        return pd.Series(row[attributes].values, index=attributes)

    def filterData(ds, region, year):
        filteredData = filter(lambda t: getattr(t, "Continent", None) == region, ds.itertuples())
        rows = list(map(lambda t: self.filterAttributes(t.Index, ds, year), filteredData))
        cols = ["Country Name", "Country Code", "Continent"]
        attributes = safeExtend(cols,year)
        return pd.DataFrame(rows, columns=attributes)

    def statistics(fds,op,year):
        sum = reduce(lambda e,i: e + i, fds.loc[:, year].dropna().tolist())
        if op == "sum":
            return sum
        else:
            return sum/(len(fds)*1.0)

    def execute(self, raw_data: List[Any]) -> None:

        ds = self.cleanData(raw_data)
        fds = self.filterData(ds,self.config["region"],self.config["year"])
        stat = self.statistics(fds,self.config["operation"],self.config["year"])
        #self.sink.write(results)