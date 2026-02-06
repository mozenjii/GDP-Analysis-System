import pandas as pd

try:
    ds = pd.read_excel("gdp_with_continent_filled.xlsx")
except:
    print("Error: ""GDP with continent data"" file not found!")

if(ds.shape == (266,70)):
    a = "000";
else:
    raise custom_error("Data structured in an unknown way!")

