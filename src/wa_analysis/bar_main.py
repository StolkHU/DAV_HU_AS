import matplotlib.pyplot as plt

from wa_analysis.config import ConfigLoader
from wa_analysis.dataprocessor import DataProcessor
from wa_analysis.role_merger import Merger
from wa_analysis.settings import ColoredPlotSettings
from wa_analysis.try_1_bar import HockeyBarChart

if __name__ == "__main__":
    settings = ColoredPlotSettings(
        title="Staff sending longer messages",
        xlabel="Function within Team",
        ylabel="Average Message Length",
        legend_title="Average Message Length",
    )

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
