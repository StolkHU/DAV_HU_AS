import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from loguru import logger

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.merger import Merger
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.settings import PlotSettings

settings = PlotSettings("relationships")


class Replier:
    def __init__(self, plot_settings: PlotSettings, data):
        """
        Initialiseert de Replier klasse met een DataFrame of een tuple met een DataFrame.
        """
        self.plot_settings = plot_settings
        # Controleer of data een tuple is en extraheer het DataFrame indien nodig
        if isinstance(data, tuple):
            # Neem het eerste element van de tuple, wat het DataFrame zou moeten zijn
            self.df = data[0]
        else:
            self.df = data

        self.desired_order = [
            "Keeper",
            "Verdediger",
            "Middenvelder",
            "Aanvaller",
            "Staff",
        ]

        # Voeg de 'prev_position' kolom toe die de positie van de vorige berichtauteur aangeeft
        self.df["prev_position"] = self.df["Position"].shift(1)

    def prepare_data(self):
        """
        Bereid de data voor voor analyse.
        """
        # Aanname: 'Position' en 'prev_position' kolommen bestaan in het DataFrame
        # We filteren berichten waar iemand niet op zichzelf heeft gereageerd
        filtered_df = self.df[self.df["Position"] != self.df["prev_position"]].copy()

        # Maak een pivot table om het aantal berichten van de ene auteur naar de vorige auteur te tellen
        author_matrix = filtered_df.pivot_table(
            index="Position",
            columns="prev_position",
            values="message",
            aggfunc="count",
            fill_value=0,
        )

        # Bewaar de originele matrix met aantallen
        self.author_matrix_counts = author_matrix.copy()

        # Bereken percentages per rij (elke rij telt op tot 100%)
        self.author_matrix_percentages = author_matrix.div(
            author_matrix.sum(axis=1), axis=0
        )
        self.author_matrix_percentages = self.author_matrix_percentages.round(
            3
        )  # Rond af op 3 decimalen

        # Reindex de matrix om de gewenste volgorde te volgen
        self.author_matrix_percentages = self.author_matrix_percentages.reindex(
            index=self.desired_order, columns=self.desired_order
        )

        # Groeperen op 'Position' en tellen van unieke 'author' en het aantal berichten
        self.overzicht_df = pd.DataFrame(
            {
                "Aantal authors": self.df.groupby("Position")["author"].nunique(),
                "Aantal berichten": self.df.groupby("Position")["message"].count(),
            }
        )

        # Reindex het DataFrame op basis van de gewenste volgorde
        self.overzicht_df = self.overzicht_df.reindex(self.desired_order)

        return self

    def create_summary_text(self):
        """
        Creëert een samenvatting in tekst van de data.
        """
        total_messages = self.overzicht_df["Aantal berichten"].sum()
        sentence_parts = [
            f"Gebaseerd op {total_messages:,} berichten, waarbij iemand niet op zichzelf heeft gereageerd.\n"
        ]

        for position, row in self.overzicht_df.iterrows():
            sentence_parts.append(
                f"{position}: {row['Aantal berichten']:,} berichten verzonden door {row['Aantal authors']} auteurs\n"
            )

        self.summary_text = "".join(sentence_parts)
        # Vervang komma's door punten voor Nederlandse numerieke notatie
        self.summary_text = self.summary_text.replace(",", ".")

        return self

    def plot_heatmap(self):
        """
        Plot een heatmap van de percentages.

        Parameters:
        filename (str): Bestandsnaam om de afbeelding op te slaan.
        show (bool): Of de plot ook moet worden weergegeven.
        """
        plt.figure(figsize=(10, 6))
        sns.heatmap(
            self.author_matrix_percentages,
            annot=True,
            fmt=".3f",
            cmap="PuBu",
            linewidths=0.5,
            cbar=False,
        )
        plt.suptitle(
            self.plot_settings.settings.suptitle, fontsize=16, fontweight="bold"
        )
        plt.title(self.plot_settings.settings.title)
        plt.xlabel("Beantwoorder", labelpad=20, fontweight="bold", fontsize=12)
        plt.ylabel("Verzender", labelpad=20, fontweight="bold", fontsize=12)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        plt.gca().xaxis.set_ticks_position("none")
        plt.gca().yaxis.set_ticks_position("none")

        # Voeg figtext toe met het overzicht
        plt.figtext(
            0.0,
            -0.2,
            self.summary_text,
            wrap=True,
            horizontalalignment="left",
            fontsize=10,
        )
        # Voeg witruimte toe aan de rechterkant
        plt.subplots_adjust(right=0.75)

        # Opslaan en eventueel tonen
        plt.savefig("versie1.png", bbox_inches="tight")
        return self


def run_replier():
    """
    Hoofdfunctie om de Replier analyse uit te voeren.
    """
    logger.info("Replier analyse gestart")

    # Laad de configuratie en gegevens
    config_loader = ConfigLoader()
    processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile_hockeyteam
    )
    altered_df = processor.add_columns()

    # Gebruik Merger om de data samen te voegen
    merger = Merger(
        config=config_loader.config,
        altered_df=altered_df,
        role_file=config_loader.role_file,
    )
    merged_df = merger.get_processed_data()

    # Voeg reacties toe
    reactions_adder = ReactionsAdder(config_loader.config, merged_df)
    processed_df = reactions_adder.process_data()

    # Voer de analyse uit en maak de visualisatie
    replier = Replier(settings, processed_df)
    replier.prepare_data().create_summary_text().plot_heatmap()

    logger.info("Replier analyse voltooid")
    return processed_df


if __name__ == "__main__":
    run_replier()
