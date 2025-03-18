import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.merger import Merger
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.settings import (MessageCalculations, PlotSettings,
                                           Settings)

settings = PlotSettings("comparing_categories")


class HockeyBarChart:
    """Analyseert de berichten van gegroepeerde accounts."""

    def __init__(self, settings: Settings, df: pd.DataFrame):
        self.plot_settings = settings
        self.hockeybar_settings = MessageCalculations()
        self.df = df

    def calculate_message_count(self):
        """Calculate the average message length for each function."""
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
        return average_message_length

    def plot_average_message_length(self, average_message_length):
        """Create a bar plot of average message length."""
        fig, ax = plt.subplots()
        plt.figure(figsize=(10, 6))

        for i, v in enumerate(
            average_message_length[self.hockeybar_settings.message_length_column]
        ):
            plt.text(i, v * 0.98, f"{v:.1f}", ha="center", va="top", fontsize=12)

        self.plot_settings.apply_settings(ax)
        fig.suptitle(
            self.plot_settings.settings.suptitle,
            fontweight=self.plot_settings.settings.suptitle_fontweight,
            fontsize=self.plot_settings.settings.suptitle_fontsize,
        )
        plt.figtext(
            0.05,
            0.05,
            f"Gebaseerd op {self.df.shape[0]:,}".replace(",", ".")
            + " berichten verstuurd in de groepschat van een hockeyteam."
            + "\n"
            + "Staf is iedereen rondom een team die geen speler is: trainer, coach, fysio, etc.",
            ha="left",
            va="center",
            fontsize=10,
            fontstyle="italic",
        )
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.2)
        sns.barplot(
            x=average_message_length[self.hockeybar_settings.function_column],
            y=average_message_length[self.hockeybar_settings.message_length_column],
            palette=["red", "lightgrey"],
            ax=ax,
        )
        fig.savefig("Average Message Length_wip.png")


if __name__ == "__main__":
    # Laad de configuratie en gegevens voor de merge
    config_loader = ConfigLoader()
    processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile
    )
    altered_df = processor.add_columns()

    # Gebruik Merger om de data samen te voegen
    merger = Merger(
        config=config_loader.config,
        altered_df=altered_df,
        role_file=config_loader.role_file,
    )
    merged_df = merger.get_processed_data()  # Haal het samengevoegde dataframe op

    # Maak de grafiek met de samengevoegde data
    chart = HockeyBarChart(settings, merged_df)

    # Bereken de gemiddelde berichtlengte per functie
    avg_message_length = chart.calculate_message_count()

    # Maak de grafiek van de gemiddelde berichtlengte
    chart.plot_average_message_length(avg_message_length)

    # # Toon de grafiek
    # output_dir = Path(config_loader.output_folder)
    # output_dir.mkdir(parents=True, exist_ok=True)
    # plt.savefig(output_dir / "Average Message Length_wip.png")
