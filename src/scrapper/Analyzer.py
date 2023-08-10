import matplotlib.pyplot as plt
import pandas as pd

from config.Logger import logger
from domain.CategorizedComment import CategorizedComment


class Analyzer:
    def __init__(self, path: str):
        self._path = path

    def analyze(self, categorized_comments: list[CategorizedComment]):
        self._plot_category_bar_chart(categorized_comments)
        self._plot_time_spent_bar_chart(categorized_comments)
        pass

    def _plot_category_bar_chart(self, categorized_comments):
        logger.info('Plotting category bar chart')
        data = [c.to_dict() for c in categorized_comments]
        df = pd.DataFrame(data)
        category_counts = df['category'].value_counts()
        category_counts.plot(kind='bar')
        plt.subplots_adjust(bottom=0.4)
        plt.xticks(rotation=45)
        plt.title("Frequency of Categories")
        plt.ylabel("Number of Comments")
        plt.xlabel("Category")
        plt.savefig(f'{self._path}/category-bar-chart.png')
        plt.clf()

    def _plot_time_spent_bar_chart(self, categorized_comments):
        logger.info('Plotting time spent bar chart')
        data = [c.to_dict() for c in categorized_comments]

        # Aggregate time spent in each category
        category_times = {}
        for item in data:
            category_times[item['category']] = category_times.get(item['category'], 0) + item['time_spent']

        categories = list(category_times.keys())
        times = list(category_times.values())

        # Bar plot
        plt.bar(categories, times)
        plt.subplots_adjust(bottom=0.4)
        plt.xticks(rotation=45)
        plt.title('Time Spent in Each Category')
        plt.xlabel('Category')
        plt.ylabel('Time Spent(H)')
        plt.savefig(f'{self._path}/time-spent-bar-chart.png')
        plt.clf()
