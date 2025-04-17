import matplotlib.pyplot as plt
import numpy as np

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import PlotSettings

# Setup logger
logger = Logger().get_logger()
settings = PlotSettings("distribution")


class ReactionPlotter:
    def __init__(self, plot_settings: PlotSettings, data_processor: ReactionsAdder):
        """
        Constructor voor ReactionPlotter
        """
        logger.info("Initialiseren van ReactionPlotter")
        self.plot_settings = plot_settings
        self.data_processor = data_processor
        self.df = data_processor.df
        logger.debug(f"DataFrame geladen met vorm: {self.df.shape}")

    def create_plot(self, percentage_counts, cumulative_percentage):
        """
        Maakt de plot met individuele percentages en subtiele cumulatieve lijn
        """
        logger.info("Maken van distributieplot")

        try:
            # Labels voor de buckets
            bucket_labels = [
                "<1 min",
                "1-5 min",
                "5-15 min",
                "15-30 min",
                "30-60 min",
                "1-2 uur",
                "2-4 uur",
                ">4 uur",
            ]
            bucket_labels = bucket_labels[: len(percentage_counts)]
            logger.debug(f"Bucket labels: {bucket_labels}")

            # Opbouw van de figuur
            fig, ax1 = plt.subplots(figsize=(10, 7))
            logger.debug("Figuur en primaire as aangemaakt")

            # Bar plot voor waarschijnlijkheid
            ax1.bar(bucket_labels, percentage_counts, color="silver", width=0.90)
            logger.debug("Barplot voor percentages aangemaakt")

            ax1.set_title(
                self.plot_settings.settings.title,
                fontsize=self.plot_settings.settings.title_fontsize,
                style=self.plot_settings.settings.title_fontstyle,
                pad=20,
            )
            ax1.set_xlabel(
                self.plot_settings.settings.xlabel,
                fontsize=self.plot_settings.settings.xlabel_fontsize,
                fontweight=self.plot_settings.settings.xlabel_fontweight,
            )
            ax1.set_ylabel(
                self.plot_settings.settings.ylabel,
                fontsize=self.plot_settings.settings.ylabel_fontsize,
                fontweight=self.plot_settings.settings.ylabel_fontweight,
            )
            ax1.tick_params(axis="x", rotation=45)
            logger.debug("Titel en labels ingesteld")

            ax2 = ax1.twinx()
            logger.debug("Secundaire as aangemaakt voor cumulatieve lijn")

            # Plot de lijn met markers op elk punt en voeg een label toe voor de legenda
            (line,) = ax2.plot(
                bucket_labels,
                cumulative_percentage,
                "o-",
                color="black",
                linewidth=2,
                markersize=3,
                label="Cumulatief",  # Label toevoegen voor de legenda
            )

            ax2.set_ylim(0, 1.05)  # Op 1.05 omdat het anders niet past
            ax2.set_yticklabels([])
            ax2.tick_params(axis="y", labelcolor="black", length=0)
            logger.debug("Cumulatieve lijn geplot")

            # Voeg een legenda toe voor de lijn
            ax2.legend(handles=[line], loc="upper left", bbox_to_anchor=(0, 1.03))
            logger.debug("Legenda toegevoegd voor cumulatieve lijn")

            # Annotaties toevoegen
            for i, val in enumerate(cumulative_percentage):
                # Maak de tekst voor de derde marker dikgedrukt
                if i == 2:
                    ax2.annotate(
                        f"{val:.2f}",
                        (i, val),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha="center",
                        color="black",
                        fontweight="bold",
                    )
                else:
                    ax2.annotate(
                        f"{val:.2f}",
                        (i, val),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha="center",
                        color="black",
                    )
            logger.debug("Annotaties toegevoegd aan cumulatieve lijn")

            # Verdere opmaak
            ax1.yaxis.grid(True)
            ax1.set_axisbelow(True)

            plt.suptitle(
                self.plot_settings.settings.suptitle,
                fontsize=self.plot_settings.settings.suptitle_fontsize,
                fontweight=self.plot_settings.settings.suptitle_fontweight,
            )

            plt.tight_layout()
            plt.figtext(
                self.plot_settings.settings.figtext_x,
                self.plot_settings.settings.figtext_y,
                self.plot_settings.settings.figtext,
                ha=self.plot_settings.settings.figtext_ha,
                fontsize=self.plot_settings.settings.figtext_fontsize,
            )
            logger.debug("Suptitle en figtext toegevoegd")

            # Spines configureren
            ax1.spines["top"].set_visible(False)
            ax1.spines["right"].set_visible(False)
            ax1.spines["left"].set_visible(False)
            ax1.tick_params(axis="both", which="both", length=0)

            # Verberg alle randen van de tweede as
            ax2.spines["top"].set_visible(False)
            ax2.spines["right"].set_visible(False)
            ax2.spines["left"].set_visible(False)
            ax2.spines["bottom"].set_visible(False)
            logger.debug("Spines en ticks geconfigureerd")

            # Sla de plot op met de geconfigureerde instellingen
            self.plot_settings.save_plot(fig)
            logger.info("Distributieplot succesvol opgeslagen")

            return fig

        except Exception as e:
            logger.error(f"Fout bij het maken van de distributieplot: {str(e)}")
            raise


def make_distribution():
    """
    Maak de distributie visualisatie
    """
    logger.info("Start maken van distributievisualisatie")

    try:
        # Laad configuratie
        config_loader = ConfigLoader()
        logger.info("Configuratie geladen")

        # Maak data processor aan
        data_processor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_wife
        )
        logger.info("DataProcessor geïnitialiseerd")

        # Voeg kolommen toe
        altered_dataframe = data_processor.add_columns()
        logger.info("Kolommen toegevoegd aan dataframe")

        # Initialiseer de ReactionsAdder en verwerk de data
        reactions_adder = ReactionsAdder(config_loader.config, altered_dataframe)
        logger.info("ReactionsAdder geïnitialiseerd")

        (
            altered_df,
            reactie_counts,
            percentage_counts,
            cumulative_percentage,
            total_count,
        ) = reactions_adder.process_data()
        logger.info(f"Data verwerkt, {total_count} reacties geanalyseerd")
        logger.debug(f"Percentage counts: {percentage_counts}")
        logger.debug(f"Cumulatieve percentages: {cumulative_percentage}")

        # Maak de chart aan met data processor
        chart = ReactionPlotter(settings, reactions_adder)
        fig = chart.create_plot(percentage_counts, cumulative_percentage)
        logger.info("Distributievisualisatie succesvol gemaakt")

        return fig

    except Exception as e:
        logger.error(f"Fout bij het maken van distributievisualisatie: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Start uitvoering distribution.py")
    try:
        make_distribution()
        logger.info("Einde uitvoering distribution.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering distribution.py - Fout: {str(e)}")
