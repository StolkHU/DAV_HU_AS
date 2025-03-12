from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from wa_analysis.baseplot import BasePlot
from wa_analysis.settings import ColoredPlotSettings


class ColoredBarPlot(BasePlot):
    """Bar plot that extends BasePlot with color options."""

    def __init__(self, settings: ColoredPlotSettings):
        super().__init__(settings)
        self.rotation = 0

    def set_rotation(self, rotation: int):
        """Set the rotation for x-axis labels."""
        self.rotation = rotation

    def plot(
        self,
        data: pd.DataFrame,
        x_column: str,
        y_column: str,
        hue_column: Optional[str] = None,
    ):
        """Create a bar plot using the provided data and settings."""

        self.create_figure()
        sns.barplot(
            data=data,
            x=x_column,
            y=y_column,
            hue=hue_column,
            palette=self.settings.color_palette,
            ax=self.ax,
        )
        plt.xticks(rotation=self.rotation)

        return self.fig
