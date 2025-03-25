import matplotlib.pyplot as plt
import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.settings import PlotSettings

settings = PlotSettings("time_series")


class PhotoPlotter:
    def __init__(self, plot_settings: PlotSettings, data_processor: DataProcessor):
        """
        Constructor voor PhotoPlotter
        """
        self.plot_settings = plot_settings
        self.data_processor = data_processor
        self.df = data_processor.altered_dataframe

    def photo_percentage_per_quarter(self):
        """
        Bereken percentage foto's per maand
        """
        photos_per_quarter = (
            self.df.groupby(pd.Grouper(key="timestamp", freq="QE"))["has_image"].mean()
            * 100
        )

        return photos_per_quarter

    def plot_photos_percentage_per_quarter(self):
        """
        Maak de plot van foto percentages per quarter
        """
        # Bereken foto percentages
        photos_percentage_per_quarter = self.photo_percentage_per_quarter()

        # Bepaal datum range
        min_date = self.df["timestamp"].min()
        max_date = self.df["timestamp"].max()

        # Maak de figuur
        fig, ax = plt.subplots(figsize=(20, 10))

        # Formatter voor Y-as percentages
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

        # Kleur selectie
        colors = [
            (
                "hotpink"
                if pd.Period(period, freq="Q") >= pd.Period("2022-Q3", freq="Q")
                else "silver"
            )
            for period in photos_percentage_per_quarter.index
        ]

        # Plot de data
        photos_percentage_per_quarter.plot(kind="bar", ax=ax, color=colors)

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

        # Pas plot-instellingen toe
        self.plot_settings.apply_settings(ax)

        # Extra tekstuele annotaties
        plt.figtext(
            0.01,
            0.01,
            f"Gebaseerd op {self.df.shape[0]:,}".replace(",", ".")
            + f' berichten tussen {min_date.strftime("%d-%m-%Y")} en {max_date.strftime("%d-%m-%Y")}.',
            ha="left",
            fontsize=16,
        )

        ax.set_xticks(range(len(photos_percentage_per_quarter.index)))
        ax.set_xticklabels(
            [
                f"{period.year} Q{period.quarter}"
                for period in photos_percentage_per_quarter.index
            ],
            rotation=0,
        )

        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08)

        # Sla de plot op met de geconfigureerde instellingen
        self.plot_settings.save_plot(fig)


def make_timeseries():
    """
    Maak de tijdreeks visualisatie
    """
    # Laad configuratie
    config_loader = ConfigLoader()

    # Maak data processor aan
    data_processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile_wife
    )

    # Voeg kolommen toe
    # Let op: add_columns() retourneert de DataFrame
    data_processor.altered_dataframe = data_processor.add_columns()

    # Maak plot settings aan
    plot_settings = PlotSettings("time_series")

    # Maak de chart aan met data processor
    chart = PhotoPlotter(plot_settings, data_processor)

    # Plot de foto percentage per maand
    chart.plot_photos_percentage_per_quarter()


if __name__ == "__main__":
    make_timeseries()
