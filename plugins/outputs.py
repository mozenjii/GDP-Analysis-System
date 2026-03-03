from typing import List
import matplotlib.pyplot as plt

class ConsoleWriter:

    def write(self, records: dict) -> None:
        print("=== OUTPUT ===")
        for record in records:
            print(record)


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