# import tomllib
# from pathlib import Path

# import matplotlib.pyplot as plt
# import pandas as pd

# from wa_analysis.data_loading.config import ConfigLoader
# from wa_analysis.data_loading.processor import DataProcessor
# from wa_analysis.data_loading.reactions import ReactionsAdder
# from wa_analysis.settings.settings import PlotSettings

# settings = PlotSettings("distribution")

# class ReactionPlotter:
#     def __init__(self, plot_settings: PlotSettings, data_processor: ReactionsAdder):
#         """
#         Constructor voor ReactionPlotter
#         """
#         self.plot_settings = plot_settings
#         self.data_processor = data_processor
#         self.df = data_processor.df

#     def create_plot(self):
#         """
#         Maakt de plot
#         """
#         # Labels voor de buckets
#         bucket_labels = [
#             "<1 min",
#             "1-5 min",
#             "5-15 min",
#             "15-30 min",
#             "30-60 min",
#             "1-2 uur",
#             "2-4 uur",
#             ">4 uur",
#         ]
#         bucket_labels = bucket_labels[: len(reactie_counts)]

#         # Opbouw van de figuur
#         fig, ax1 = plt.subplots(figsize=(10, 6))

#         # Kleuren
#         colors = ["#FF9999" if i < 3 else "silver" for i in range(len(bucket_labels))]

#         # Bar plot voor counts
#         ax1.bar(bucket_labels, reactie_counts.values, color=colors, width=0.90)
#         ax1.set_title(
#             "Ruim 73% van alle berichten wordt binnen een kwartier beantwoord",
#             fontsize=12,
#             style="oblique",
#             pad=20,
#         )
#         ax1.set_xlabel("Reactietijd", fontsize=12)
#         ax1.set_ylabel("Aantal reacties", fontsize=12)
#         ax1.tick_params(axis="x", rotation=45)

#         # Voeg waarden toe boven de bars
#         for i, v in enumerate(reactie_counts.values):
#             ax1.text(i, v + 0.1, str(v), ha='center', fontsize=9)

#         ax2 = ax1.twinx()
#         ax2.plot(
#             bucket_labels, cumulative_percentage.values, color="black", linewidth=3
#         )  # marker='o',
#         ax2.set_ylabel("Cumulatief Percentage", fontsize=12)
#         ax2.tick_params(axis="y", colors="black")

#         ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
#         ax2.set_ylim(0, 102.5)
#         ax1.yaxis.grid(True)
#         ax1.set_axisbelow(True)

#         plt.suptitle("Liefde op het eerste bericht", fontsize=16, fontweight="bold")
#         plt.figtext(
#             0.35,
#             0.00,
#             f"Totaal aantal berichten met response: {total_count:,}".replace(",", "."),
#             ha="right",
#             fontsize=10,
#         )
#         ax1.spines["top"].set_visible(False)
#         ax1.spines["right"].set_visible(False)
#         ax1.spines["left"].set_visible(False)
#         ax2.spines["top"].set_visible(False)
#         ax2.spines["right"].set_visible(False)
#         ax2.spines["left"].set_visible(False)
#         ax1.tick_params(axis="both", which="both", length=0)
#         ax2.tick_params(axis="both", which="both", length=0)

#         plt.tight_layout()
#         plt.show()

#         def make_distribution():
#     """
#     Maak de tijdreeks visualisatie
#     """
#     config_loader = ConfigLoader()
#     data_processor = DataProcessor(
#         config=config_loader.config,
#         datafile=config_loader.datafile_wife
#     )

#     data_processor.altered_dataframe = data_processor.add_columns()
#     plotter = ReactionPlotter(settings, reactions_adder)
#     plotter.create_plot()

# if __name__ == "__main__":


# # Initialiseer de ReactionsAdder en verwerk de data
# altered_df, reactie_counts, percentage_counts, cumulative_percentage, total_count = reactions_adder.process_data()
