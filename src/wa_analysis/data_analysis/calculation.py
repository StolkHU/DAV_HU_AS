# def calculate_message_count(self):
#     """Calculate the average message length for each function."""
#     average_message_length = (
#         self.df.groupby(self.hockeybar_settings.function_column)[
#             self.hockeybar_settings.message_length_column
#         ]
#         .mean()
#         .reset_index()
#         .sort_values(
#             by=self.hockeybar_settings.message_length_column, ascending=False
#         )  # Sort by message length
#     )
