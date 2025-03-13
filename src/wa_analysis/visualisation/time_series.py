### Python program to create a time series visualisation ###

import tomllib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# Class to load in the data
# This class needs to go and filled with the class from staging.dataloader
class ConfigLoader:
    def __init__(self, config_path, datafile=None):
        self.config_path = Path(config_path).resolve()
        self.config = self.load_config()
        self.root = Path("./").resolve()
        self.processed = self.root / Path(self.config["processed"])
        self.datafile = self.processed / (
            datafile if datafile else self.config["current"]
        )
        self.df = self.load_dataframe()

    def load_config(self):
        with self.config_path.open("rb") as f:
            return tomllib.load(f)

    def load_dataframe(self):
        return pd.read_parquet(self.datafile)


# Class to process the data and give a 1 for the messages with images
class DataProcessor:
    def __init__(self, df):
        self.df = df
        self.df["has_image"] = (
            self.df["message"].fillna("").str.contains("<Media weggela").astype(int)
        )

    def photo_percentage_per_month(self):
        return (
            self.df.groupby(self.df["timestamp"].dt.to_period("Q"))["has_image"].mean()
            * 100
        )

    def date_range(self):
        dates = self.df["timestamp"].dt.date
        min_date = dates.min()
        max_date = dates.max()
        number_of_days = (max_date - min_date).days
        average = len(self.df) / number_of_days
        return min_date, max_date, number_of_days, average


# Class for plotting the barchart of the timeseries
class Plotter:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def plot_photos_percentage_per_month(self):
        photos_percentage_per_month = self.data_processor.photo_percentage_per_month()
        min_date, max_date, number_of_days, average = self.data_processor.date_range()

        # Plot code, using Func Formatter for de percentages op de Y-as
        plt.figure(figsize=(20, 10))
        ax = plt.gca()
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

        # Aanpassen kleur naar hotpink vanaf Q3-2022
        colors = [
            "hotpink" if period >= pd.Period("2022-Q3", freq="Q") else "silver"
            for period in photos_percentage_per_month.index
        ]
        photos_percentage_per_month.plot(kind="bar", ax=ax, color=colors)

        # Datalabels toevoegen aan de bars
        for p in ax.patches:
            ax.annotate(
                f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2.0, p.get_height()),
                ha="center",
                va="center",
                xytext=(0, 10),
                textcoords="offset points",
            )

        # Tweaken van de visual
        plt.suptitle('"Photoboom"', size=30, fontweight="bold")
        plt.title(
            "Het percentage foto's stijgt aanzienlijk na de geboorte van onze dochter in November '22",
            fontstyle="italic",
            pad=25,
            size=16,
        )
        plt.xlabel("")
        plt.xticks(rotation=0)
        plt.figtext(
            0.01,
            0.01,
            f"Gebaseerd op {self.data_processor.df.shape[0]:,}".replace(",", ".")
            + f' berichten tussen {min_date.strftime("%d-%m-%Y")} en {max_date.strftime("%d-%m-%Y")}.',
            ha="left",
            fontsize=16,
        )
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08)

        # Output folder en opslaan van de visual
        output_dir = Path("img")
        output_dir.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_dir / "Photoboom.png")


# Voor het draaien van main.py
def make_timeseries():
    wife_file = ConfigLoader("./config.toml", datafile="wife.parq")
    data_processor = DataProcessor(wife_file.df)
    plotter = Plotter(data_processor)

    plotter.plot_photos_percentage_per_month()


if __name__ == "__main__":
    time_series = make_timeseries()
