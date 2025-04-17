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

        ax.legend(fontsize=14)

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

        # Zoek index van 2022 Q4 voor annotatie
        target_quarter = pd.Period("2022-Q4", freq="Q")

        # Vind de index van 2022 Q4 in de data
        q4_2022_idx = None
        q4_2022_value = None
        for i, period in enumerate(photos_percentage_per_quarter.index):
            if pd.Period(period, freq="Q") == target_quarter:
                q4_2022_idx = i
                q4_2022_value = photos_percentage_per_quarter.iloc[i]
                break

        # Als 2022 Q4 is gevonden, voeg annotatie toe
        if q4_2022_idx is not None:
            # Bepaal de maximale hoogte voor de plot
            y_max = ax.get_ylim()[1]

            # Voeg annotatie toe voor de gebeurtenis, pijl wijst naar de balk
            ax.annotate(
                "Geboorte dochter\n(Nov 2022)",
                xy=(q4_2022_idx, q4_2022_value * 1.08),  # Positie van de balk
                xytext=(q4_2022_idx - 1.5, y_max * 0.9),  # Tekst links van de balk
                ha="center",
                va="center",
                fontsize=12,
                fontweight="bold",
                color="#AA3333",
                bbox=dict(
                    boxstyle="round,pad=0.5", fc="white", ec="#AA3333", alpha=0.7
                ),
                arrowprops=dict(
                    arrowstyle="->",
                    connectionstyle="arc3,rad=-0.4",
                    color="#AA3333",
                    lw=2,
                ),
            )

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
