import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

    def __init__(self, settings: Settings, df: pd.DataFrame):
        logger.info("Initialiseren van HockeyBarChart")
        self.plot_settings = settings
        self.hockeybar_settings = MessageCalculations()
        self.df = df
        logger.debug(f"DataFrame geladen met vorm: {df.shape}")

    def calculate_message_count(self):
        """Calculate the average message length for each function."""
        logger.info("Berekenen van gemiddelde berichtlengte per functie")
        average_message_length = (
            self.df.groupby(self.hockeybar_settings.function_column)[
                self.hockeybar_settings.message_length_column
            ]
            .mean()
            .reset_index()
            .sort_values(
                by=self.hockeybar_settings.message_length_column, ascending=False
            )  # Sort by message length
        )
        logger.debug(f"Resultaat berekening: {average_message_length}")
        return average_message_length

    def plot_average_message_length(self, average_message_length):
        """Create a bar plot of average message length."""
        logger.info("Maken van barplot voor gemiddelde berichtlengte")

        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            logger.debug("Figuur en axes aangemaakt")

            # Plot met seaborn
            sns.barplot(
                x=average_message_length[self.hockeybar_settings.function_column],
                y=average_message_length[self.hockeybar_settings.message_length_column],
                palette=["#FF9999", "silver"],
                ax=ax,
            )
            logger.debug("Barplot gecreëerd")

            # Datalabels toevoegen aan de bars
            for p in ax.patches:
                ax.annotate(
                    f"{p.get_height():.1f}",
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
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


def make_comparing_categories():
    logger.info("Start maken van vergelijkende categorieëngrafiek")

    try:
        # Laad de configuratie en gegevens voor de merge
        config_loader = ConfigLoader()
        logger.info("Configuratie geladen")

        processor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )
        altered_df = processor.add_columns()
        logger.info("Data verwerkt")

        # Gebruik Merger om de data samen te voegen
        merger = Merger(
            config=config_loader.config,
            altered_df=altered_df,
            role_file=config_loader.role_file,
        )
        merged_df = merger.get_processed_data()  # Haal het samengevoegde dataframe op
        logger.info("Data samengevoegd")

        # Maak de grafiek met de samengevoegde data
        chart = HockeyBarChart(settings, merged_df)

        # Bereken de gemiddelde berichtlengte per functie
        avg_message_length = chart.calculate_message_count()

        # Maak de grafiek van de gemiddelde berichtlengte
        fig = chart.plot_average_message_length(avg_message_length)
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
        make_comparing_categories()
        logger.info("Einde uitvoering comparing_categories.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering comparing_categories.py - Fout: {str(e)}")
