from typing import Any, Callable, Dict, List, Optional, Tuple

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from wa_analysis.data_analysis.model import TextClustering
from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.data_loading.reactions import ReactionsAdder
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import PlotSettings

# Setup logger
logger = Logger().get_logger()
settings = PlotSettings("clustering")


class Clustering:
    def __init__(self, plot_settings: PlotSettings, data: pd.DataFrame) -> None:
        """
        Initialiseert de Clustering klasse.

        Args:
            plot_settings: Plot configuratie
            data: DataFrame met berichten
        """
        logger.info("Initialiseren Clustering")
        self.plot_settings: PlotSettings = plot_settings
        self.df: pd.DataFrame = data
        logger.debug(f"DataFrame geladen met vorm: {self.df.shape}")

        self.corpus: Dict[str, List[str]] = self._create_corpus()
        logger.debug(f"Corpus gemaakt met {len(self.corpus)} auteurs")

        self.text: List[str] = [part for text in self.corpus.values() for part in text]
        logger.debug(f"Tekstlengtes: {len(self.text)}")

        self.wa_labels: List[str] = [
            k for k, v in self.corpus.items() for _ in range(len(v))
        ]
        logger.debug(f"Labels maken voor {len(self.wa_labels)} items")

        self.custom_palette: Dict[str, str] = self._create_custom_palette()
        logger.debug(f"Custom palette gemaakt voor {len(self.custom_palette)} auteurs")

    def _create_corpus(self) -> Dict[str, List[str]]:
        """
        Maak een corpus van berichten per auteur voor tekstanalyse.

        Returns:
            Dict[str, List[str]]: Dictionary met auteurs als keys en lijsten van tekstfragmenten als values
        """
        logger.info("Maken van corpus voor tekstanalyse")

        # Filter auteurs met minimaal 351 berichten
        self.df = self.df.groupby("author").filter(lambda x: len(x) > 350)
        logger.info("Gefilterd op auteurs met meer dan 350 berichten")

        authors: List[str] = list(np.unique(self.df.author))
        logger.debug(f"Aantal auteurs na filtering: {len(authors)}")

        corpus: Dict[str, List[str]] = {}
        for author in authors:
            subset = self.df[self.df.author == author].reset_index()
            longseq = " ".join(subset.message)
            parts = [longseq[i : i + 500] for i in range(0, len(longseq), 500)]
            if len(parts) > 2:
                corpus[author] = parts
                logger.debug(f"Auteur {author}: {len(parts)} tekstfragmenten")

        logger.debug(f"Corpus gemaakt met {len(corpus)} auteurs")
        return corpus

    def _create_custom_palette(self) -> Dict[str, str]:
        """
        Maak een aangepaste kleurenpalet voor de visualisatie.

        Returns:
            Dict[str, str]: Dictionary met auteurs als keys en kleuren als values
        """
        logger.info("Maken van aangepast kleurenpalet")
        unique_labels: List[str] = list(set(self.wa_labels))
        palette: Dict[str, str] = {
            label: "red" if label == "motley-fox" else "silver"
            for label in unique_labels
        }
        logger.debug(f"Kleurenpalet gemaakt voor {len(unique_labels)} unieke labels")
        return palette

    def plot_clustering(self) -> None:
        """
        Visualiseer de clustering van tekstfragmenten.
        """
        logger.info("Maken van clustering visualisatie")
        try:
            plt.figure(figsize=(12, 8), tight_layout=False)
            logger.debug("Figuur aangemaakt")

            clustering = TextClustering()
            clustering.custom_palette = self.custom_palette
            clustering.plot = self._plot.__get__(clustering, TextClustering)
            logger.debug("TextClustering object geconfigureerd")

            clustering(
                text=self.text, k=200, labels=self.wa_labels, batch=False, method="tSNE"
            )
            logger.debug("Clustering algoritme uitgevoerd")

            self._customize_plot()
            logger.info("Clustering visualisatie succesvol gemaakt")

        except Exception as e:
            logger.error(f"Fout bij het maken van de clustering visualisatie: {str(e)}")
            raise

    def _plot(self, xx: np.ndarray, labels: List[str]) -> None:
        """
        Interne methode voor het plotten van de clustering data.

        Args:
            xx: Array met coördinaten
            labels: Labels voor de datapunten
        """
        logger.info("Plotten van de data in een scatterplot")
        sns.scatterplot(
            x=xx[:, 0],
            y=xx[:, 1],
            hue=labels,
            palette=self.custom_palette,
            edgecolor="white",
            linewidth=1,
        )
        logger.debug("Scatterplot gemaakt")

    def _customize_plot(self) -> None:
        """
        Pas de plot aan met extra opmaak en annotaties.
        """
        logger.info("Aanpassen van de plot met extra opmaak")
        try:
            # Configureer punten
            scatter = plt.gca().collections[0]
            scatter.set_edgecolor("white")
            scatter.set_linewidth(0.5)
            logger.debug("Scatter punten geconfigureerd")

            # Verberg assen
            plt.xticks([])
            plt.yticks([])
            logger.debug("Assen verborgen")

            # Voeg rechthoek toe
            rect = patches.Rectangle(
                (-33, -40),
                27,
                20,
                linewidth=2,
                edgecolor="silver",
                facecolor="none",
                linestyle="--",
            )
            plt.gca().add_patch(rect)
            logger.debug("Rechthoek toegevoegd")

            # Voeg annotatie toe
            plt.annotate(
                "Voornamelijk inhoud over het verzamelen",
                xy=(0, -35),
                xytext=(-33, -19),
                fontsize=9,
                color="black",
            )
            logger.debug("Annotatie toegevoegd")

            # Configureer legenda
            plt.legend(
                title=self.plot_settings.legend_title,
                bbox_to_anchor=(1.05, 1),
                loc="upper left",
                title_fontproperties={"weight": "bold"},
                edgecolor="black",
            )
            logger.debug("Legenda geconfigureerd")

            # Voeg suptitle toe
            plt.suptitle(
                self.plot_settings.settings.suptitle,
                fontsize=self.plot_settings.settings.suptitle_fontsize,
                fontweight=self.plot_settings.settings.suptitle_fontweight,
                horizontalalignment="center",
            )
            logger.debug("Suptitle toegevoegd")

            # Voeg title toe
            plt.title(
                self.plot_settings.settings.title,
                fontsize=self.plot_settings.settings.title_fontsize,
                style=self.plot_settings.settings.title_fontstyle,
                horizontalalignment="center",
                x=0.65,
            )
            logger.debug("Title toegevoegd")

            # Voeg figtext toe
            plt.figtext(
                0.0,
                -0.05,
                self.plot_settings.settings.figtext,
                wrap=True,
                horizontalalignment="left",
                fontsize=self.plot_settings.settings.figtext_fontsize,
            )
            logger.debug("Figtext toegevoegd")

            # Sla plot op
            self.plot_settings.save_plot(plt.gcf())
            logger.info("Plot opgeslagen")

        except Exception as e:
            logger.error(f"Fout bij het aanpassen van de plot: {str(e)}")
            raise


def make_clustering() -> None:
    """
    Hoofdfunctie om de clustering visualisatie te maken.
    """
    logger.info("Start maken van clustering visualisatie")

    try:
        # Laad configuratie en data
        config_loader: ConfigLoader = ConfigLoader()
        logger.debug("Configuratie geladen")

        processor: DataProcessor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )
        altered_df: pd.DataFrame = processor.add_columns()
        logger.debug("Data verwerkt")

        # Extracteer DataFrame uit tuple indien nodig
        if isinstance(altered_df, tuple):
            altered_df = altered_df[0]
            logger.debug("DataFrame geëxtraheerd uit tuple")

        # Maak visualisatie
        visualizer: Clustering = Clustering(settings, altered_df)
        visualizer.plot_clustering()
        logger.info("Clustering visualisatie succesvol gemaakt")

    except Exception as e:
        logger.error(f"Fout bij het maken van clustering visualisatie: {str(e)}")
        raise


if __name__ == "__main__":
    logger.info("Start uitvoering clustering.py")
    try:
        make_clustering()
        logger.info("Einde uitvoering clustering.py - Succesvol")
    except Exception as e:
        logger.error(f"Einde uitvoering clustering.py - Fout: {str(e)}")
