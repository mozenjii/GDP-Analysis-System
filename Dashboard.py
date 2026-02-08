import json
from DataLoader import loadModule
import matplotlib.pyplot as plt
from DataProcesser import processModule, statistics, cleanData, fields


def readConfig():
    try:
        with open("config.jason", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("COnfiguration File not found!")
    return config

config = readConfig()

def validateConfig():
    print("Validating the configuration file...")
    #checking the required fields
    requiredKeys = ["region", "year", "operation", "output"]
    for key in requiredKeys:
        if key not in config:
            raise ValueError(f"Missing Value: {key}")

    #checking the appropriate data types
    if not isinstance(config["region"], str):
        raise TypeError("Region must be a string")
    if not isinstance(config["year"], int):
        raise TypeError("Year must be an integer")
    if not isinstance(config["operation"], str):
        raise TypeError("Operation must be a string")
    if not isinstance(config["output"], str):
        raise TypeError("Output must be a string")

    #checking appropriate Values
    if config["operation"] == "average" or "sum":
        raise ValueError("Undefined Operation detected!")
    print("Successful")

rds = loadModule() # Raw Data Set
fds = processModule(rds, config["region"], config["year"]) # Cleaned & Filtered Data Set
cds = cleanData(rds) # Cleaned Data Set

stat = statistics(fds,config["operation"],config["year"])

def runDashboard(config, fds, cds, stat):
    try:
        if fds.empty:
            raise ValueError("No data available for selected configuration")

        region = config["region"]
        year = config["year"]
        operation  = config["operation"]

        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        header_ax = fig.add_axes([0, 0.9, 1, 0.1])  # [left, bottom, width, height]
        header_ax.axis('off')

        header_ax.add_patch(
            plt.Rectangle(
                (0, 0), 1, 1,
                transform=header_ax.transAxes,
                color="#1f4e79"  # Example color, you can change it
            )
        )

        header_text = (
            "GDP ANALYTICS DASHBOARD\n\n"
            f"Region: {region}    |    Year: {year}    |    Operation: {operation.upper()}\n"
            f"Result: {operation.upper()} GDP = {stat:,.2f}"
        )

        header_ax.text(
            0.5, 0.5,  # Centered in the header axis
            header_text,
            ha='center',
            va='center',
            fontsize=14,
            color='white',
            weight='bold'
        )

        # Regionwise Bar chart
        barChart = axes[0, 0]
        barChart.bar(fds["Country Code"], fds[year])
        barChart.set_title(f"Region-wise GDP — Bar chart ({region}, {year})")
        barChart.set_xlabel("Country")
        barChart.set_ylabel("GDP")
        barChart.tick_params(axis="x", rotation=90)

        values = fds[year]
        labels = fds["Country Code"]
        total = values.sum()
        angles = (values / total) * 360

        # Show labels only if angle > 10 degrees
        filteredLabels = [label if angle >= 10 else "" for label, angle in zip(labels, angles)]

        # Regionwise Pie chart
        pieChart = axes[0, 1]
        pieChart.pie(values,labels=filteredLabels,autopct=lambda pct: f"{pct:.1f}%" if pct * 3.6 >= 10 else "",)
        pieChart.set_title(f"Region-wise GDP — Pie chart ({region}, {year})")

        # Year pecific Line graph (regional total GDP per year)
        lineGraph = axes[1, 0]
        region_rows = cds[cds["Continent"] == region]
        if not region_rows.empty and len(fields) > 0:
            yearly_total = region_rows[fields].sum(axis=0)
            lineGraph.plot(fields, yearly_total.values)
        lineGraph.set_title(f"Year-specific GDP — Line ({region})")
        lineGraph.set_xlabel("Year")
        lineGraph.set_ylabel("Total GDP (region)")
        lineGraph.tick_params(axis="x", rotation=45)

        # Year-specific Scatter Plot(year vs regional total GDP)
        scatterPlot = axes[1, 1]
        if not region_rows.empty and len(fields) > 0:
            yearly_total = region_rows[fields].sum(axis=0)
            scatterPlot.scatter(fields, yearly_total.values)
        scatterPlot.set_title(f"Year-specific GDP — Scatter ({region})")
        scatterPlot.set_xlabel("Year")
        scatterPlot.set_ylabel("Total GDP (region)")
        scatterPlot.tick_params(axis="x", rotation=45)

        fig.suptitle(
            f"Region: {region}  |  Year: {year}  |  {operation.upper()} = {stat:,.2f}",
            fontsize=12, y=1.02
        )
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("DASHBOARD ERROR")
        print(e)


runDashboard(config, fds, cds, stat)
