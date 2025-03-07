### Program to create barchart based on the data ###

from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns


class BarChart:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.add_message_length()
        self.player_message_count = self.calculate_message_count("Player")
        self.staff_message_count = self.calculate_message_count("Staff")
        self.plot_average_message_length()

    def add_message_length(self):
        self.dataframe["message_length"] = self.dataframe["message"].str.len()

    def calculate_message_count(self, function):
        return self.dataframe[self.dataframe["Function"] == function].count()["message"]

    def plot_average_message_length(self):
        p1 = (
            self.dataframe[["Function", "message_length"]]
            .groupby("Function")
            .mean()
            .sort_values("message_length", ascending=False)
        )

        sns.barplot(x=p1.index, y=p1["message_length"], palette=["red", "lightgrey"])
        for i, v in enumerate(p1["message_length"]):
            plt.text(i, v * 0.98, f"{v:.1f}", ha="center", va="top", fontsize=12)
        plt.xlabel("Function within team")
        plt.ylabel("Average Message length")
        plt.title("Staff members sending longer messages")

        plt.figtext(
            0.05,
            0.05,
            f"Gebaseerd op {self.player_message_count:,}".replace(",", ".")
            + f" berichten van de players en {self.staff_message_count:,}".replace(
                ",", "."
            )
            + " berichten van de staff.",
            ha="left",
            va="center",
            fontsize=8,
            fontstyle="italic",
        )
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        plt.subplots_adjust(bottom=0.2)
        output_dir = Path("img/automatic")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / "Average Message Length.png")


def make_barchart(loaded_dataframe):
    """
    This is the function to be called for running all the steps to create the bar chart visual
    """
    BarChart(loaded_dataframe)


if __name__ == "__main__":
    bar_chart = make_barchart()
