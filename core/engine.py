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

    def top10(self, ds, region, year):
        filtered = ds[ds["Continent"] == region]
        sortedDf = filtered.sort_values(by=year, ascending=False)
        result = sortedDf[["Country Name", year]].head(10)
        return list(result.itertuples(index=False, name=None))
    
    def bottom10(self, ds, region, year):
        filtered = ds[ds["Continent"] == region]
        sortedDf = filtered.sort_values(by=year, ascending=True)
        result = sortedDf[["Country Name", year]].head(10)
        return list(result.itertuples(index=False, name=None))
    
    def growthRates(self, ds, region, start_year, end_year):
        filtered = ds[ds["Continent"] == region]
        def computeGrowth(row):
            start = row[start_year]
            end = row[end_year]
            if start > 0:
                return ((end - start) / start) * 100
            return 0

        growthList = list(
            map(lambda row: (row["Country Name"],computeGrowth(row)),
            filtered.to_dict("records"))
        )

        return growthList
    
    
    def avgByContinent(self, ds, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        continents = ds["Continent"].unique()
        def computeAvg(continent):
            subset = ds[ds["Continent"] == continent]
            avg = subset[years].mean().mean()
            return (continent, avg)

        return list(map(computeAvg, continents))

    def globalTrend(self, ds, start_year, end_year):
        years = list(range(start_year, end_year + 1))
        return list(
            map(lambda year: (year,ds[year].sum()),
            years)
        )

    def fastestContinent(self, ds, start_year, end_year):
        continents = ds["Continent"].unique()

        def growth(continent):
            subset = ds[ds["Continent"] == continent]
            startTotal = subset[start_year].sum()
            endTotal = subset[end_year].sum()

            if startTotal > 0:
                return ((endTotal - startTotal) / startTotal)
            return 0

        growthValues = list(map(lambda c: (c, growth(c)), continents))

        return max(growthValues, key=lambda x: x[1])[0]

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