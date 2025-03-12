import matplotlib.pyplot as plt
import pandas as pd

from wa_analysis.colored_bar_chart import ColoredBarPlot
from wa_analysis.playerdataloader import DataLoader
from wa_analysis.settings import ColoredPlotSettings, MessageCalculations

settings = ColoredPlotSettings(
    title="Staff sending longer messages",
    xlabel="Function within Team",
    ylabel="Average Message Length",
    legend_title="Average Message Length",
)


class HockeyBarChart:
    """Analyseert de berichten van gegroepeerde accounts."""

    def __init__(self, settings: ColoredPlotSettings, df: pd.DataFrame):
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
        )
        return average_message_length

    def plot_average_message_length(self, average_message_length):
        """Create a bar plot of average message length."""
        plotter = ColoredBarPlot(self.plot_settings)
        fig = plotter.plot(
            data=average_message_length,
            x_column=self.hockeybar_settings.function_column,
            y_column=self.hockeybar_settings.message_length_column,
        )

        return fig


if __name__ == "__main__":
    process_data = DataLoader.load_data()
    chart = HockeyBarChart(settings, process_data)

    avg_message_length = chart.calculate_message_count()

    fig = chart.plot_average_message_length(avg_message_length)

    # Show the plot
    plt.savefig("test")
