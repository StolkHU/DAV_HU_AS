import matplotlib.pyplot as plt

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.settings import PlotSettings

settings = PlotSettings("distribution")


class ReactionPlotter:
    def __init__(self, plot_settings: PlotSettings, data_processor: ReactionsAdder):
        """
        Constructor voor ReactionPlotter
        """
        self.plot_settings = plot_settings
        self.data_processor = data_processor
        self.df = data_processor.df

    def create_plot(self, percentage_counts, cumulative_percentage):
        """
        Maakt de plot met individuele percentages en subtiele cumulatieve lijn
        """
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

        # Opbouw van de figuur
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Kleuren
        colors = ["#FF9999" if i < 3 else "silver" for i in range(len(bucket_labels))]

        # Bar plot voor percentages
        ax1.bar(bucket_labels, percentage_counts, color=colors, width=0.90)
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

        # Plot een subtiele cumulatieve lijn op dezelfde y-as
        # Maak een twinx maar verberg de tweede y-as volledig
        ax2 = ax1.twinx()

        # Plot de lijn met markers op elk punt
        ax2.plot(
            bucket_labels,
            cumulative_percentage,
            "o-",
            color="gray",
            linewidth=1,
            markersize=3,
        )
        ax2.set_ylim(0, 1.05)  # Op 1.05 omdat het anders niet past
        ax2.set_ylabel(
            "Cummulatief",
            color="gray",
            fontsize=self.plot_settings.settings.ylabel_fontsize,
            fontweight=self.plot_settings.settings.ylabel_fontweight,
        )
        ax2.tick_params(axis="y", labelcolor="gray", length=0)

        for i, val in enumerate(cumulative_percentage):
            color = "black" if i == 2 else "gray"
            ax2.annotate(
                f"{val:.2f}",
                (i, val),
                textcoords="offset points",
                xytext=(0, 10),
                ha="center",
                color=color,
            )

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
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        ax1.tick_params(axis="both", which="both", length=0)

        # Verberg alle randen van de tweede as
        ax2.spines["top"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["left"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)

        # Sla de plot op met de geconfigureerde instellingen
        self.plot_settings.save_plot(fig)


def make_distribution():
    """
    Maak de distributie visualisatie
    """
    # Laad configuratie
    config_loader = ConfigLoader()

    # Maak data processor aan
    data_processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile_wife
    )

    # Voeg kolommen toe
    # Let op: add_columns() retourneert de DataFrame
    altered_dataframe = data_processor.add_columns()

    # Initialiseer de ReactionsAdder en verwerk de data
    reactions_adder = ReactionsAdder(config_loader.config, altered_dataframe)
    (
        altered_df,
        reactie_counts,
        percentage_counts,
        cumulative_percentage,
        total_count,
    ) = reactions_adder.process_data()

    # Maak de chart aan met data processor
    chart = ReactionPlotter(settings, reactions_adder)
    chart.create_plot(percentage_counts, cumulative_percentage)


if __name__ == "__main__":
    make_distribution()
