from typing import Any, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import Settings

# Setup logger
logger = Logger().get_logger()


# Base Plot class
class BasePlot:
    """Base class for creating plots."""

    def __init__(self, settings: Settings) -> None:
        logger.info("Initialiseren BasePlot")
        self.settings: Settings = settings
        self.fig: Optional[Figure] = None
        self.ax: Optional[Axes] = None
        logger.debug("BasePlot geïnitialiseerd")

    def create_figure(self) -> Tuple[Figure, Axes]:
        """
        Create a figure and configure it based on settings.

        Returns:
            Tuple[Figure, Axes]: Matplotlib figure and axes objects
        """
        logger.info("Aanmaken figuur en assen")

        try:
            # Controleer of figsize aanwezig is
            if not hasattr(self.settings, "figsize"):
                logger.warning(
                    "Figsize niet gevonden in settings, gebruik standaard (10, 6)"
                )
                figsize: Tuple[int, int] = (10, 6)
            else:
                figsize = self.settings.figsize
                logger.debug(f"Figsize uit settings: {figsize}")

            self.fig, self.ax = plt.subplots(figsize=figsize)
            logger.debug("Figuur en assen aangemaakt")

            # X-as label instellen
            if hasattr(self.settings, "xlabel"):
                self.ax.set_xlabel(
                    self.settings.xlabel,
                    fontsize=getattr(self.settings, "xlabel_fontsize", 12),
                    fontweight=getattr(self.settings, "xlabel_fontweight", "normal"),
                )
                logger.debug(f"X-label ingesteld: {self.settings.xlabel}")

            # Y-as label instellen
            if hasattr(self.settings, "ylabel"):
                self.ax.set_ylabel(
                    self.settings.ylabel,
                    fontsize=getattr(self.settings, "ylabel_fontsize", 12),
                    fontweight=getattr(self.settings, "ylabel_fontweight", "normal"),
                )
                logger.debug(f"Y-label ingesteld: {self.settings.ylabel}")

            # Titel instellen
            if hasattr(self.settings, "title"):
                self.ax.set_title(self.settings.title)
                logger.debug(f"Titel ingesteld: {self.settings.title}")

            # Suptitle instellen
            if hasattr(self.settings, "suptitle") and self.settings.suptitle:
                self.fig.suptitle(self.settings.suptitle)
                logger.debug(f"Suptitle ingesteld: {self.settings.suptitle}")

            # Legenda instellen
            if (
                hasattr(self.settings, "legend_title")
                and self.settings.legend_title is not None
            ):
                self.ax.legend(title=self.settings.legend_title)
                logger.debug(f"Legenda titel ingesteld: {self.settings.legend_title}")

            # Grid uitschakelen
            self.ax.grid(False)
            logger.debug("Grid uitgeschakeld")

            # Verberg spines
            self.ax.spines["top"].set_visible(False)
            self.ax.spines["right"].set_visible(False)
            self.ax.spines["left"].set_visible(False)
            logger.debug("Spines aangepast (top, right, left verborgen)")

            plt.tight_layout()
            logger.debug("Tight layout toegepast")

            logger.info("Figuur succesvol aangemaakt")
            return self.fig, self.ax

        except Exception as e:
            logger.error(f"Fout bij het aanmaken van figuur: {str(e)}")
            raise

    def get_figure(self) -> Figure:
        """
        Return the figure, creating it if needed.

        Returns:
            Figure: The matplotlib figure object
        """
        logger.info("Ophalen figuur")
        if self.fig is None:
            logger.debug("Figuur bestaat nog niet, wordt nu aangemaakt")
            self.create_figure()
        return self.fig
