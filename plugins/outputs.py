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

    def plotTop10(self):
        data = self.results["top_10"]
        countries = [x[0] for x in data]
        values = [x[1] for x in data]

        plt.bar(countries, values)
        plt.xticks(rotation=45)
        plt.title("Top 10 Countries")

    def plotBottom10(self):
        data = self.results["bottom_10"]
        countries = [x[0] for x in data]
        values = [x[1] for x in data]

        plt.bar(countries, values)
        plt.xticks(rotation=45)
        plt.title("Bottom 10 Countries")

    def plotGlobalTrend(self):
        data = self.results["global_trend"]
        years = [int(x[0]) for x in data]
        totals = [x[1] for x in data]

        plt.plot(years, totals)
        plt.title("Global GDP Trend")
        plt.xlabel("Year")
        plt.ylabel("Total GDP")

    def plotContribution(self):
        data = self.results["contribution"]
        continents = [x[0] for x in data]
        percentages = [x[1] for x in data]

        plt.pie(percentages, labels=continents, autopct="%1.1f%%")
        plt.title("Contribution to Global GDP")

    def plotAvgByContinent(self):
        data = self.results["avg_by_continent"]
        continents = [x[0] for x in data]
        averages = [x[1] for x in data]

        plt.bar(continents, averages)
        plt.xticks(rotation=45)
        plt.title("Average GDP by Continent")

    def plotGrowthRates(self):
        data = self.results["growth_rates"]
        countries = [x[0] for x in data]
        growth = [x[1] for x in data]

        plt.barh(countries, growth)
        plt.title("GDP Growth Rates (%)")
        
    def print_summary(self, results):
        print("\nFastest Growing Continent:")
        print(results["fastest_continent"])

        print("\nCountries with Consistent Decline:")
        for country in results["decline_countries"]:
            print(country)

    def nextSlide(self, event):
        if event.key == "right":
            self.currentSlide = (self.currentSlide + 1) % len(self.slides)
            self.showSlide()

    def showSlide(self):
        plt.clf()
        self.slides[self.currentSlide]()
        plt.tight_layout()
        plt.draw()

    def write(self, records: dict):

        self.results = records

        self.slides = [
            self.plotTop10,
            self.plotBottom10,
            self.plotGlobalTrend,
            self.plotContribution,
            self.plotAvgByContinent,
            self.plotGrowthRates
        ]

        self.currentSlide = 0
        self.print_summary(records)

        self.fig = plt.figure(figsize=(10, 6))
        self.fig.canvas.mpl_connect("key_press_event", self.nextSlide)

        self.showSlide()
        plt.show()