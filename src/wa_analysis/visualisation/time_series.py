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
        Maak de plot van foto percentages per quarter met zwarte rolling average lijn
        """
        # Bereken foto percentages
        photos_percentage_per_quarter = self.photo_percentage_per_quarter()
        rolling_avg = photos_percentage_per_quarter.rolling(window=4).mean()

        # Maak de figuur
        fig, ax = plt.subplots(figsize=(20, 10))

        # Formatter voor Y-as percentages
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))

        ax.tick_params(axis="y", labelsize=self.plot_settings.settings.ylabel_fontsize)

        # Kleur selectie
        colors = [
            (
                "#FF9999"
                if pd.Period(period, freq="Q") >= pd.Period("2022-Q3", freq="Q")
                else "silver"
            )
            for period in photos_percentage_per_quarter.index
        ]

        # Plot de data
        photos_percentage_per_quarter.plot(
            kind="bar", ax=ax, color=colors, zorder=1, label="_nolegend_"
        )

        # Bereid x-posities voor voor de rolling average lijn
        x_positions = range(len(photos_percentage_per_quarter.index))

        # Plot rolling Average
        ax.plot(
            x_positions,
            rolling_avg.values,
            color="black",
            linewidth=3,
            marker="o",
            markersize=7,
            label="4 Kwartalen Rolling Average",
            zorder=2,
        )

        ax.legend(fontsize=12)

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

        ax.set_xticks(range(len(photos_percentage_per_quarter.index)))
        ax.set_xticklabels(
            [
                f"{period.year} Q{period.quarter}"
                for period in photos_percentage_per_quarter.index
            ],
            rotation=self.plot_settings.settings.xlabel_rotation,
            fontsize=self.plot_settings.settings.xlabel_fontsize,
        )

        # plt.subplots_adjust(bottom=0.2)  # Extra ruimte onderaan voor figtext

        plt.figtext(
            self.plot_settings.settings.figtext_x,
            self.plot_settings.settings.figtext_y,
            self.plot_settings.settings.figtext,
            ha=self.plot_settings.settings.figtext_ha,
            fontsize=self.plot_settings.settings.figtext_fontsize,
        )

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
