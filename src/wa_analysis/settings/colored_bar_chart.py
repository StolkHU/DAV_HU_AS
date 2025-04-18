from typing import Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

from wa_analysis.settings.baseplot import BasePlot
from wa_analysis.settings.logger import Logger
from wa_analysis.settings.settings import ColoredPlotSettings

# Setup logger
logger = Logger().get_logger()


class ColoredBarPlot(BasePlot):
    """Bar plot that extends BasePlot with color options."""

    def __init__(self, settings: ColoredPlotSettings):
        logger.info("Initialiseren ColoredBarPlot")
        super().__init__(settings)
        self.rotation: int = 0
        logger.debug("ColoredBarPlot geïnitialiseerd")

    def set_rotation(self, rotation: int) -> "ColoredBarPlot":
        """Set the rotation for x-axis labels."""
        logger.info(f"Instellen rotatie x-labels op {rotation} graden")
        self.rotation = rotation
        return self  # voor method chaining

    def plot(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        hue_column: Optional[str] = None,
    ) -> Figure:
        """Create a bar plot using the provided data and settings."""
        logger.info(f"Maken barplot met x={x_column}, y={y_column}, hue={hue_column}")

        try:
            logger.debug(f"Data vorm: {data.shape}")

            # Maak figuur aan als die nog niet bestaat
            if self.fig is None or self.ax is None:
                logger.debug("Figuur aanmaken")
                self.create_figure()

            # Bepaal de te gebruiken kleurenpalet
            palette: Optional[Union[str, list]] = getattr(
                self.settings, "color_palette", None
            )
            logger.debug(f"Kleurenpalet: {palette}")

            # Maak barplot
            sns.barplot(
                data=data,
                x=x_column,
                y=y_column,
                hue=hue_column,
                palette=palette,
                ax=self.ax,
            )
            logger.debug("Barplot aangemaakt")

            # Pas rotatie toe op x-labels
            plt.xticks(rotation=self.rotation)
            logger.debug(f"X-as labels geroteerd met {self.rotation} graden")

            logger.info("Barplot succesvol gemaakt")
            return self.fig

        except Exception as e:
            logger.error(f"Fout bij het maken van barplot: {str(e)}")
            raise
