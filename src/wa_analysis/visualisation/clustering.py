import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from loguru import logger

from wa_analysis.data_analysis.model import TextClustering
from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.merger import Merger
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.settings import PlotSettings

settings = PlotSettings("clustering")


class Clustering:
    def __init__(self, plot_settings, data):
        self.plot_settings = plot_settings
        self.df = data
        self.corpus = self._create_corpus()
        self.text = [part for text in self.corpus.values() for part in text]
        self.wa_labels = [k for k, v in self.corpus.items() for _ in range(len(v))]
        self.custom_palette = self._create_custom_palette()

    def _create_corpus(self):
        self.df = self.df.groupby("author").filter(lambda x: len(x) > 350)
        logger.info(f"Cleaning authors with less than 351 messages")
        authors = list(np.unique(self.df.author))
        corpus = {}
        for author in authors:
            subset = self.df[self.df.author == author].reset_index()
            longseq = " ".join(subset.message)
            parts = [longseq[i : i + 500] for i in range(0, len(longseq), 500)]
            if len(parts) > 2:
                corpus[author] = parts
        return corpus

    def _create_custom_palette(self):
        logger.info(f"Creating a custom palette")
        unique_labels = list(set(self.wa_labels))
        return {
            label: "red" if label == "motley-fox" else "silver"
            for label in unique_labels
        }

    def plot_clustering(self):
        logger.info(f"Create the clustering plot")
        plt.figure(figsize=(12, 8), tight_layout=False)

        clustering = TextClustering()
        # Geef de palette expliciet mee aan de TextClustering class
        clustering.custom_palette = self.custom_palette
        clustering.plot = self._plot.__get__(clustering, TextClustering)
        clustering(
            text=self.text, k=200, labels=self.wa_labels, batch=False, method="tSNE"
        )
        self._customize_plot()

    def _plot(self, xx: np.ndarray, labels: list) -> None:
        logger.info(f"Plotting the data in a scatterplot")
        sns.scatterplot(
            x=xx[:, 0],
            y=xx[:, 1],
            hue=labels,
            palette=self.custom_palette,
            edgecolor="white",
            linewidth=0.8,
        )

    def _customize_plot(self):
        logger.info(f"Customizing the plot")
        scatter = plt.gca().collections[0]
        scatter.set_edgecolor("white")
        scatter.set_linewidth(0.5)
        plt.xticks([])  # Verwijdert de x-as labels als dit in config is ingesteld.
        plt.yticks([])  # Verwijdert de y-as labels als dit in config is ingesteld.
        rect = patches.Rectangle(
            (-45, -4),
            20,
            12,
            linewidth=2,
            edgecolor="silver",
            facecolor="none",
            linestyle="--",
        )
        plt.gca().add_patch(rect)
        plt.annotate(
            "Voornamelijk inhoud over het verzamelen",
            xy=(-40, -3),
            xytext=(-45, 8.5),
            fontsize=9,
            color="silver",
        )
        plt.legend(
            title="Auteur",
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            title_fontproperties={"weight": "bold"},
        )
        plt.suptitle(
            "De coach communiceert duidelijk anders dan de rest",
            fontsize=16,
            fontweight="bold",
        )
        plt.title("en bemoeit zich al helemaal niet met het verzamelen...")
        plt.figtext(
            0.0,
            -0.05,
            "Gebaseerd op de top 10 bijdragers aan de WhatsApp groepchat (op basis van aantal berichten).\n Bij het verzamelen wordt meestal één bericht gemaakt, waar de spelers hun eigen naam in zetten en versturen...",
            wrap=True,
            horizontalalignment="left",
            fontsize=10,
        )
        plt.savefig("clustering.png")


def run_visualizer():
    logger.info(f"Running the visualizer")
    config_loader = ConfigLoader()
    processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile_hockeyteam
    )
    altered_df = processor.add_columns()
    reactions_adder = ReactionsAdder(config_loader.config, altered_df)
    processed_df = reactions_adder.process_data()

    if isinstance(processed_df, tuple):
        processed_df = processed_df[0]

    visualizer = Clustering(settings, processed_df)
    visualizer.plot_clustering()
    logger.info(f"Done creating the clustering plot")


if __name__ == "__main__":
    run_visualizer()
