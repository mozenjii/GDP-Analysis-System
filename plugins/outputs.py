from typing import List
import matplotlib.pyplot as plt

class ConsoleWriter:
    def __init__(self):
        pass

    def printTop10(self, data):
        print("\nTop 10 Countries")
        print("-" * 60)

        for index, (country, value) in enumerate(data, 1):
            print(f"{index:2}. {country:<25} {value:>15,.2f}")
    def printBottom10(self, data):
        print("\nBottom 10 Countries")
        print("-" * 60)

        for index, (country, value) in enumerate(data, 1):
            print(f"{index:2}. {country:<25} {value:>15,.2f}")

    def printGrowthRates(self, data):
        print("\nGDP Growth Rates (%)")
        print("-" * 60)

        for country, growth in data:
            print(f"{country:<25} {growth:>10.2f}%")

    def printAvgByContinent(self, data):
        print("\nAverage GDP by Continent")
        print("-" * 60)

        for continent, average in data:
            print(f"{continent:<20} {average:>15,.2f}")

    def printGlobalTrend(self, data):
        print("\nGlobal GDP Trend")
        print("-" * 60)

        for year, total in data:
            print(f"{year:<10} {total:>20,.2f}")

    def printFastestContinent(self, continent):
        print("\nFastest Growing Continent")
        print("-" * 60)
        print(continent)

    def printDeclineCountries(self, countries):
        print("\nCountries with Consistent GDP Decline")
        print("-" * 60)

        if not countries:
            print("None")
        else:
            for country in countries:
                print(country)

    def printContribution(self, data):
        print("\nContribution to Global GDP (%)")
        print("-" * 60)

        for continent, percentage in data:
            print(f"{continent:<20} {percentage:>10.2f}%")    

    def write(self, results: dict):
        title = "GDP ANALYTICS DASHBOARD"
        print("\n" + "=" * 60)
        print(title.center(60))
        print("=" * 60)
        self.printTop10(results["top_10"])
        self.printBottom10(results["bottom_10"])
        self.printGrowthRates(results["growth_rates"])
        self.printAvgByContinent(results["avg_by_continent"])
        self.printGlobalTrend(results["global_trend"])
        self.printFastestContinent(results["fastest_continent"])
        self.printDeclineCountries(results["decline_countries"])
        self.printContribution(results["contribution"])

class GraphicsChartWriter:

    def __init__(self):
        pass

    def plot_top_10(self, data):
        countries = [x[0] for x in data]
        values = [x[1] for x in data]

        plt.figure()
        plt.bar(countries, values)
        plt.xticks(rotation=45)
        plt.title("Top 10 Countries")
        plt.tight_layout()
        plt.show()

    def plot_bottom_10(self, data):
        countries = [x[0] for x in data]
        values = [x[1] for x in data]

        plt.figure()
        plt.bar(countries, values)
        plt.xticks(rotation=45)
        plt.title("Bottom 10 Countries")
        plt.tight_layout()
        plt.show()

    def plot_global_trend(self, data):
        years = [int(x[0]) for x in data]
        totals = [x[1] for x in data]

        plt.figure()
        plt.plot(years, totals)
        plt.title("Global GDP Trend")
        plt.xlabel("Year")
        plt.ylabel("Total GDP")
        plt.tight_layout()
        plt.show()

    def plot_contribution(self, data):
        continents = [x[0] for x in data]
        percentages = [x[1] for x in data]

        plt.figure()
        plt.pie(percentages, labels=continents, autopct='%1.1f%%')
        plt.title("Continent Contribution")
        plt.show()


    def plot_avg_by_continent(self, data):
        continents = [x[0] for x in data]
        averages = [x[1] for x in data]

        plt.figure()
        plt.bar(continents, averages)
        plt.title("Average GDP by Continent")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_growth_rates(self, data):
        countries = [x[0] for x in data]
        growth = [x[1] for x in data]

        plt.figure()
        plt.barh(countries, growth)
        plt.title("GDP Growth Rates")
        plt.tight_layout()
        plt.show()
        
    def print_summary(self, results):
        print("\nFastest Growing Continent:")
        print(results["fastest_continent"])

        print("\nCountries with Consistent Decline:")
        for country in results["decline_countries"]:
            print(country)

    def write(self, records: dict):

        self.plot_top_10(records["top_10"])
        self.plot_bottom_10(records["bottom_10"])
        self.plot_global_trend(records["global_trend"])
        self.plot_contribution(records["contribution"])
        self.plot_avg_by_continent(records["avg_by_continent"])
        self.plot_growth_rates(records["growth_rates"])
        self.print_summary(records)