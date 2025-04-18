from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.merger import Merger
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import (MessageCalculations, PlotSettings,
                                           Settings)

logger = Logger().get_logger()
settings = PlotSettings("comparing_categories")


class HockeyBarChart:
    """Analyseert de berichten van gegroepeerde accounts."""

    def __init__(self, settings: Settings, df: pd.DataFrame) -> None:
        logger.info("Initialiseren van HockeyBarChart")
        self.plot_settings: Settings = settings
        self.hockeybar_settings: MessageCalculations = MessageCalculations()
        self.df: pd.DataFrame = df
        logger.debug(f"DataFrame geladen met vorm: {df.shape}")

    def calculate_message_count(self) -> pd.DataFrame:
        """
        Calculate the average message length for each function.

        Returns:
            pd.DataFrame: DataFrame with average message length per function
        """
        logger.info("Berekenen van gemiddelde berichtlengte per functie")
        average_message_length: pd.DataFrame = (
            self.df.groupby(self.hockeybar_settings.function_column)[
                self.hockeybar_settings.message_length_column
            ]
            .mean()
            .reset_index()
            .sort_values(
                by=self.hockeybar_settings.message_length_column, ascending=False
            )
        )
        logger.debug(f"Resultaat berekening: {average_message_length}")
        return average_message_length

    def plot_average_message_length(
        self, average_message_length: pd.DataFrame
    ) -> plt.Figure:
        """
        Create a bar plot of average message length with specific colors per category.

        Args:
            average_message_length: DataFrame with average message length per function

        Returns:
            plt.Figure: The generated matplotlib figure
        """
        logger.info("Maken van barplot voor gemiddelde berichtlengte")

        try:
            fig: plt.Figure
            ax: plt.Axes
            fig, ax = plt.subplots(figsize=(10, 8))
            logger.debug("Figuur en axes aangemaakt")

            # Definieer kleuren per categorie
            category_colors: Dict[str, str] = {}
            for category in average_message_length[
                self.hockeybar_settings.function_column
            ]:
                if category.lower() == "staff":
                    category_colors[category] = "#FF9999"  # Rood voor staff
                else:
                    category_colors[category] = (
                        "silver"  # Zilver voor andere categorieën
                    )

            # Maak een lijst van kleuren in dezelfde volgorde als de data
            color_list: List[str] = [
                category_colors[cat]
                for cat in average_message_length[
                    self.hockeybar_settings.function_column
                ]
            ]

            # Plot met matplotlib voor betere controle over kleuren per bar
            bars = ax.bar(
                average_message_length[self.hockeybar_settings.function_column],
                average_message_length[self.hockeybar_settings.message_length_column],
                color=color_list,
            )
            logger.debug("Barplot gecreëerd")

            # Datalabels toevoegen aan de bars
            for bar in bars:
                height: float = bar.get_height()
                ax.annotate(
                    f"{height:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    ha="center",
                    va="center",
                    xytext=(0, -10),
                    textcoords="offset points",
                )
            logger.debug("Datalabels toegevoegd")

            # Instellingen toepassen
            self.plot_settings.apply_settings(ax)
            fig.suptitle(
                self.plot_settings.settings.suptitle,
                fontweight=self.plot_settings.settings.suptitle_fontweight,
                fontsize=self.plot_settings.settings.suptitle_fontsize,
            )
            logger.debug("Plot instellingen toegepast")

            plt.tight_layout()
            plt.figtext(
                self.plot_settings.settings.figtext_x,
                self.plot_settings.settings.figtext_y,
                self.plot_settings.settings.figtext,
                ha=self.plot_settings.settings.figtext_ha,
                va=self.plot_settings.settings.figtext_va,
            )

            # Wat ruimte maken voor de figtext
            plt.subplots_adjust(
                bottom=self.plot_settings.settings.subplot_adjust_bottom
            )
            logger.debug("Layout aangepast")

            # Sla de plot op met de geconfigureerde instellingen
            self.plot_settings.save_plot(fig)
            logger.info("Plot succesvol opgeslagen")

            return fig

        except Exception as e:
            logger.error(f"Fout bij het maken van de plot: {str(e)}")
            raise


def make_comparing_categories() -> plt.Figure:
    """
    Create a bar chart comparing message lengths by category.

    Returns:
        plt.Figure: The generated figure
    """
    logger.info("Start maken van vergelijkende categorieëngrafiek")

    try:
        # Laad de configuratie en gegevens voor de merge
        config_loader: ConfigLoader = ConfigLoader()
        logger.info("Configuratie geladen")

        processor: DataProcessor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )
        altered_df: pd.DataFrame = processor.add_columns()
        logger.info("Data verwerkt")

        # Gebruik Merger om de data samen te voegen
        merger: Merger = Merger(
            config=config_loader.config,
            altered_df=altered_df,
            role_file=config_loader.role_file,
        )
        merged_df: pd.DataFrame = merger.get_processed_data()
        logger.info("Data samengevoegd")

        # Maak de grafiek met de samengevoegde data
        chart: HockeyBarChart = HockeyBarChart(settings, merged_df)

        # Bereken de gemiddelde berichtlengte per functie
        avg_message_length: pd.DataFrame = chart.calculate_message_count()

        # Maak de grafiek van de gemiddelde berichtlengte
        fig: plt.Figure = chart.plot_average_message_length(avg_message_length)
        logger.info("Vergelijkende categorieëngrafiek succesvol gemaakt")

        return fig

    except Exception as e:
        logger.error(
            f"Fout bij het maken van vergelijkende categorieëngrafiek: {str(e)}"
        )
        raise


if __name__ == "__main__":
    logger.info("Start uitvoering comparing_categories.py")
    try:
        result: plt.Figure = make_comparing_categories()
        logger.info("Einde uitvoering comparing_categories.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering comparing_categories.py - Fout: {str(e)}")
