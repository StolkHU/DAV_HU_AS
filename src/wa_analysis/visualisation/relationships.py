from typing import Any, Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.merger import Merger
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import PlotSettings

# Setup logger
logger = Logger().get_logger()
settings = PlotSettings("relationships")


class Replier:
    def __init__(
        self, plot_settings: PlotSettings, data: Union[pd.DataFrame, Tuple]
    ) -> None:
        """
        Initialiseert de Replier klasse met een DataFrame of een tuple met een DataFrame.

        Args:
            plot_settings: Plot configuratie
            data: DataFrame of tuple met DataFrame op eerste positie
        """
        logger.info("Initialiseren van Replier")
        self.plot_settings: PlotSettings = plot_settings

        # Controleer of data een tuple is en extraheer het DataFrame indien nodig
        if isinstance(data, tuple):
            # Neem het eerste element van de tuple, wat het DataFrame zou moeten zijn
            self.df: pd.DataFrame = data[0]
            logger.debug("DataFrame geëxtraheerd uit tuple")
        else:
            self.df = data
            logger.debug("DataFrame direct gebruikt")

        logger.debug(f"DataFrame geladen met vorm: {self.df.shape}")

        self.desired_order: List[str] = [
            "Keeper",
            "Verdediger",
            "Middenvelder",
            "Aanvaller",
            "Staff",
        ]
        logger.debug(f"Gewenste volgorde voor visualisatie: {self.desired_order}")

        # Voeg de 'prev_position' kolom toe die de positie van de vorige berichtauteur aangeeft
        self.df["prev_position"] = self.df["Position"].shift(1)
        logger.debug("Kolom 'prev_position' toegevoegd")

    def prepare_data(self) -> "Replier":
        """
        Bereid de data voor voor analyse.

        Returns:
            Replier: Self voor method chaining
        """
        logger.info("Voorbereiden data voor analyse")
        filtered_df: pd.DataFrame = self.df[
            self.df["author"] != self.df["prev_author"]
        ].copy()
        logger.debug(
            f"Gefilterd op verschillende auteurs: {filtered_df.shape[0]} rijen"
        )

        # Maak een pivot table om het aantal berichten van de ene auteur naar de vorige auteur te tellen
        author_matrix: pd.DataFrame = filtered_df.pivot_table(
            index="Position",
            columns="prev_position",
            values="message",
            aggfunc="count",
            fill_value=0,
        )
        logger.debug(f"Pivot table gemaakt met vorm: {author_matrix.shape}")

        # Bewaar de originele matrix met aantallen
        self.author_matrix_counts: pd.DataFrame = author_matrix.copy()

        # Bereken percentages per rij (elke rij telt op tot 100%)
        self.author_matrix_percentages: pd.DataFrame = author_matrix.div(
            author_matrix.sum(axis=1), axis=0
        )
        self.author_matrix_percentages = self.author_matrix_percentages.round(3)
        logger.debug("Percentages berekend en afgerond op 3 decimalen")

        # Reindex de matrix om de gewenste volgorde te volgen
        self.author_matrix_percentages = self.author_matrix_percentages.reindex(
            index=self.desired_order, columns=self.desired_order
        )
        logger.debug("Matrix geherindexeerd volgens gewenste volgorde")

        # Groeperen op 'Position' en tellen van unieke 'author' en het aantal berichten
        self.overzicht_df: pd.DataFrame = pd.DataFrame(
            {
                "Aantal authors": self.df.groupby("Position")["author"].nunique(),
                "Aantal berichten": self.df.groupby("Position")["message"].count(),
            }
        )
        logger.debug(f"Overzicht DataFrame gemaakt met vorm: {self.overzicht_df.shape}")

        # Reindex het DataFrame op basis van de gewenste volgorde
        self.overzicht_df = self.overzicht_df.reindex(self.desired_order)
        logger.debug("Overzicht DataFrame geherindexeerd volgens gewenste volgorde")

        return self

    def plot_heatmap(self) -> "Replier":
        """
        Plot een heatmap van de percentages.

        Returns:
            Replier: Self voor method chaining
        """
        logger.info("Maken van heatmap voor relaties tussen posities")
        try:
            plt.figure(figsize=(10, 6))
            logger.debug("Figuur aangemaakt")

            sns.heatmap(
                self.author_matrix_percentages,
                annot=True,
                fmt=".3f",
                cmap=sns.light_palette("#FF9999", as_cmap=True),
                linewidths=0.5,
                cbar=False,
            )
            logger.debug("Heatmap gemaakt")

            plt.suptitle(
                self.plot_settings.settings.suptitle,
                fontsize=self.plot_settings.settings.suptitle_fontsize,
                fontweight=self.plot_settings.settings.suptitle_fontweight,
                horizontalalignment="center",
                x=0.35,
            )
            plt.title(
                self.plot_settings.settings.title,
                fontsize=self.plot_settings.settings.title_fontsize,
                fontstyle=self.plot_settings.settings.title_fontstyle,
                horizontalalignment="center",
                x=0.35,
            )
            logger.debug("Titels toegevoegd")

            plt.xlabel(
                self.plot_settings.settings.xlabel,
                labelpad=20,
                fontsize=self.plot_settings.settings.xlabel_fontsize,
                fontweight=self.plot_settings.settings.xlabel_fontweight,
            )
            plt.ylabel(
                self.plot_settings.settings.ylabel,
                labelpad=20,
                fontsize=self.plot_settings.settings.ylabel_fontsize,
                fontweight=self.plot_settings.settings.ylabel_fontweight,
            )
            logger.debug("Labels toegevoegd")

            plt.xticks(rotation=0)
            plt.yticks(rotation=0)
            plt.gca().xaxis.set_ticks_position("none")
            plt.gca().yaxis.set_ticks_position("none")
            logger.debug("Ticks aangepast")

            # Voeg figtext toe met het overzicht
            plt.figtext(
                0.0,
                -0.05,
                self.plot_settings.settings.figtext,
                wrap=True,
                horizontalalignment="left",
                fontsize=10,
            )
            logger.debug("Figtext toegevoegd")

            # Voeg witruimte toe aan de rechterkant
            plt.subplots_adjust(right=0.75)
            logger.debug("Layout aangepast")

            # Opslaan en eventueel tonen
            self.plot_settings.save_plot(plt.gcf())
            logger.info("Heatmap opgeslagen")

            return self

        except Exception as e:
            logger.error(f"Fout bij het maken van de heatmap: {str(e)}")
            raise


def make_relationships() -> (
    Union[pd.DataFrame, Tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series, int]]
):
    """
    Hoofdfunctie om de Replier analyse uit te voeren.

    Returns:
        Union[pd.DataFrame, Tuple]: De verwerkte data
    """
    logger.info("Start maken van relatievisualisatie")

    try:
        # Laad de configuratie en gegevens
        config_loader: ConfigLoader = ConfigLoader()
        logger.info("Configuratie geladen")

        processor: DataProcessor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )
        altered_df: pd.DataFrame = processor.add_columns()
        logger.info("Data verwerkt en kolommen toegevoegd")

        # Gebruik Merger om de data samen te voegen
        merger: Merger = Merger(
            config=config_loader.config,
            altered_df=altered_df,
            role_file=config_loader.role_file,
        )
        merged_df: pd.DataFrame = merger.get_processed_data()
        logger.info("Data samengevoegd met rollen")

        # Voeg reacties toe
        reactions_adder: ReactionsAdder = ReactionsAdder(
            config_loader.config, merged_df
        )
        processed_df = reactions_adder.process_data()
        logger.info("Reacties verwerkt")

        # Voer de analyse uit en maak de visualisatie
        replier: Replier = Replier(settings, processed_df)
        replier.prepare_data().plot_heatmap()
        logger.info("Relatievisualisatie succesvol gemaakt")

        return processed_df

    except Exception as e:
        logger.error(f"Fout bij het maken van relatievisualisatie: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Start uitvoering relationships.py")
    try:
        make_relationships()
        logger.info("Einde uitvoering relationships.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering relationships.py - Fout: {str(e)}")
