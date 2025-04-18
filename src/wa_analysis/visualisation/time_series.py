from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import PlotSettings

logger = Logger().get_logger()
settings: PlotSettings = PlotSettings("time_series")


class PhotoPlotter:
    def __init__(
        self, plot_settings: PlotSettings, data_processor: DataProcessor
    ) -> None:
        """
        Constructor voor PhotoPlotter

        Args:
            plot_settings: Plot configuratie
            data_processor: Data processor met DataFrame
        """
        logger.info("Initialiseren PhotoPlotter")
        self.plot_settings: PlotSettings = plot_settings
        self.data_processor: DataProcessor = data_processor
        self.df: pd.DataFrame = data_processor.altered_dataframe
        logger.debug(f"DataFrame geladen met vorm: {self.df.shape}")

    def photo_percentage_per_quarter(self) -> pd.Series:
        """
        Bereken percentage foto's per kwartaal

        Returns:
            pd.Series: Een serie met percentages foto's per kwartaal
        """
        logger.info("Berekenen percentage foto's per kwartaal")
        photos_per_quarter: pd.Series = (
            self.df.groupby(pd.Grouper(key="timestamp", freq="QE"))["has_image"].mean()
            * 100
        )
        logger.debug(f"Berekend over {len(photos_per_quarter)} kwartalen")
        return photos_per_quarter

    def plot_photos_percentage_per_quarter(self) -> None:
        """
        Maak de plot van foto percentages per quarter met zwarte rolling average lijn
        """
        logger.info("Maken van foto percentages plot per kwartaal")
        try:
            # Bereken foto percentages
            photos_percentage_per_quarter: pd.Series = (
                self.photo_percentage_per_quarter()
            )
            rolling_avg: pd.Series = photos_percentage_per_quarter.rolling(
                window=4
            ).mean()
            logger.debug("Percentages en rolling average berekend")

            # Maak de figuur
            fig: plt.Figure
            ax: plt.Axes
            fig, ax = plt.subplots(figsize=(20, 10))
            logger.debug("Figuur en assen aangemaakt")

            # Formatter voor Y-as percentages
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0f}%"))
            ax.tick_params(
                axis="y", labelsize=self.plot_settings.settings.ylabel_fontsize
            )
            logger.debug("Y-as formattering toegepast")

            # Kleur selectie
            colors: List[str] = [
                (
                    "#FF9999"
                    if pd.Period(period, freq="Q") >= pd.Period("2022-Q3", freq="Q")
                    else "silver"
                )
                for period in photos_percentage_per_quarter.index
            ]
            logger.debug(f"Kleuren bepaald voor {len(colors)} waarden")

            # Plot de data
            photos_percentage_per_quarter.plot(
                kind="bar", ax=ax, color=colors, zorder=1, label="_nolegend_"
            )
            logger.debug("Barplot gemaakt")

            # Bereid x-posities voor voor de rolling average lijn
            x_positions: range = range(len(photos_percentage_per_quarter.index))

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
            logger.debug("Rolling average lijn toegevoegd")

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
            logger.debug("Datalabels toegevoegd")

            # Pas plot-instellingen toe
            self.plot_settings.apply_settings(ax)
            logger.debug("Plot instellingen toegepast")

            ax.set_xticks(range(len(photos_percentage_per_quarter.index)))
            ax.set_xticklabels(
                [
                    f"{period.year} Q{period.quarter}"
                    for period in photos_percentage_per_quarter.index
                ],
                rotation=self.plot_settings.settings.xlabel_rotation,
                fontsize=self.plot_settings.settings.xlabel_fontsize,
            )
            logger.debug("X-as labels ingesteld")

            # Zoek index van 2022 Q4 voor annotatie
            target_quarter: pd.Period = pd.Period("2022-Q4", freq="Q")
            logger.debug(f"Zoeken naar {target_quarter} voor annotatie")

            # Vind de index van 2022 Q4 in de data
            q4_2022_idx: Optional[int] = None
            q4_2022_value: Optional[float] = None
            for i, period in enumerate(photos_percentage_per_quarter.index):
                if pd.Period(period, freq="Q") == target_quarter:
                    q4_2022_idx = i
                    q4_2022_value = photos_percentage_per_quarter.iloc[i]
                    break

            if q4_2022_idx is not None:
                logger.debug(
                    f"Kwartaal {target_quarter} gevonden op index {q4_2022_idx}"
                )
                # Bepaal de maximale hoogte voor de plot
                y_max: float = ax.get_ylim()[1]

                # Annotatie
                ax.annotate(
                    "Geboorte dochter\n(Nov 2022)",
                    xy=(q4_2022_idx, q4_2022_value * 1.08),  # Positie van de textbox
                    xytext=(
                        q4_2022_idx - 1.5,
                        y_max * 0.9,
                    ),  # Tekst links van de textbox
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
                logger.debug("Annotatie toegevoegd voor Q4 2022")
            else:
                logger.warning(f"Kwartaal {target_quarter} niet gevonden in de data")

            plt.figtext(
                self.plot_settings.settings.figtext_x,
                self.plot_settings.settings.figtext_y,
                self.plot_settings.settings.figtext,
                ha=self.plot_settings.settings.figtext_ha,
                fontsize=self.plot_settings.settings.figtext_fontsize,
            )
            logger.debug("Figtext toegevoegd")

            # Sla de plot op met de geconfigureerde instellingen
            self.plot_settings.save_plot(fig)
            logger.info("Plot succesvol opgeslagen")

        except Exception as e:
            logger.error(f"Fout bij het maken van de foto percentages plot: {str(e)}")
            raise


def make_timeseries() -> None:
    """
    Maak de tijdreeks visualisatie
    """
    logger.info("Start tijdreeks visualisatie")
    try:
        # Laad configuratie
        config_loader: ConfigLoader = ConfigLoader()
        logger.debug("Configuratie geladen")

        # Maak data processor aan
        data_processor: DataProcessor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_wife
        )
        logger.debug("DataProcessor geïnitialiseerd")

        # Voeg kolommen toe
        data_processor.altered_dataframe = data_processor.add_columns()
        logger.debug("Kolommen toegevoegd aan dataframe")

        # Maak plot settings aan
        plot_settings: PlotSettings = PlotSettings("time_series")
        logger.debug("PlotSettings geïnitialiseerd")

        # Maak de chart aan met data processor
        chart: PhotoPlotter = PhotoPlotter(plot_settings, data_processor)
        logger.debug("PhotoPlotter geïnitialiseerd")

        # Plot de foto percentage per maand
        chart.plot_photos_percentage_per_quarter()
        logger.info("Tijdreeks visualisatie succesvol gemaakt")

    except Exception as e:
        logger.error(f"Fout bij het maken van tijdreeks visualisatie: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Start uitvoering time_series.py")
    try:
        make_timeseries()
        logger.info("Einde uitvoering time_series.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering time_series.py - Fout: {str(e)}")
