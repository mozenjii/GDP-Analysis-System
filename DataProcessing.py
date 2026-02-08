from DataLoader import loadModule, pd
import numpy as np
from functools import reduce
from utility import *
ds = loadModule()


fields = [1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970, 1971, 
          1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 
          1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 
        1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 
        2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]


def fillNull(index,rds): #raw data set
    row = rds.loc[index].copy()
    yearVals = list(row[fields])
    valid = list(filter(lambda w: pd.notna(w) and isinstance(w, (int, float)) and w > 0, yearVals))
    mean = (reduce(lambda e,i: e + i, valid)/len(valid)) if valid else 0
    filledCols = row[fields].fillna(mean)
    return pd.concat([row.drop(fields), filledCols])

def cleanData(rds):
    ds = pd.DataFrame(list(map(lambda index: fillNull(index, rds), rds.index)), index=rds.index, columns=rds.columns) #dataset
    return ds

def filterAttributes(index, ds, year):
    row = ds.loc[index].copy()
    cols = ["Country Name", "Country Code", "Continent"]
    attributes = safeExtend(cols,year)
    return pd.Series(row[attributes].values, index=attributes)


def filterData(ds, region, year):
    filteredData = filter(lambda t: getattr(t, "Continent", None) == region, ds.itertuples())
    rows = list(map(lambda t: filterAttributes(t.Index, ds, year), filteredData))
    cols = ["Country Name", "Country Code", "Continent"]
    attributes = safeExtend(cols,year)
    return pd.DataFrame(rows, columns=attributes)

def statistics(ds,op,year):
  sum = reduce(lambda e,i: e + i, ds.loc[:, year].dropna().tolist())
  if op == "sum":
    return sum
  else:
    return sum/(len(ds)*1.0)


list = filterData(cleanData(ds), "Asia", 2000)
print(list)
print(statistics(list,"average"))