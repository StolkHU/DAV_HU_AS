## A python program for a Base Plot


import matplotlib.pyplot as plt

from wa_analysis.settings import PlotSettings


# Base Plot class
class BasePlot:
    """Base class for creating plots."""

    def __init__(self, settings: PlotSettings):
        self.settings = settings
        self.fig = None
        self.ax = None

    def create_figure(self):
        """Create a figure and configure it based on settings."""
        self.fig, self.ax = plt.subplots(figsize=self.settings.figsize)
        self.ax.set_xlabel(self.settings.xlabel)
        self.ax.set_ylabel(self.settings.ylabel)
        self.ax.set_title(self.settings.title)
        if self.settings.legend_title is not None:
            self.ax.legend(title=self.settings.legend_title)

        plt.tight_layout()
        return self.fig, self.ax

    def get_figure(self):
        """Return the figure, creating it if needed."""
        if self.fig is None:
            self.create_figure()
        return self.fig
