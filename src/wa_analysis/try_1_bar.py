import matplotlib.pyplot as plt
import pandas as pd

from wa_analysis.colored_bar_chart import ColoredBarPlot
from wa_analysis.config import ConfigLoader
from wa_analysis.dataprocessor import DataProcessor
from wa_analysis.role_merger import Merger
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
    fig = chart.plot_average_message_length(avg_message_length)

    # Toon de grafiek
    plt.savefig("test.png")
