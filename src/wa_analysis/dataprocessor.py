from wa_analysis.dataloader import BaseDataLoader


class DataProcessor(BaseDataLoader):
    def __init__(self, config, role_file):
        # Roep de init van de superklasse aan om de data in te laden
        super().__init__(config)
        self.role_file = role_file

    def add_columns(self):
        """
        Voeg extra kolommen toe aan de samengevoegde DataFrame.
        """
        self.altered_dataframe["day_of_month"] = self.altered_dataframe[
            "timestamp"
        ].dt.day
        self.altered_dataframe["day"] = self.altered_dataframe[
            "timestamp"
        ].dt.day_name()
        self.altered_dataframe["month_number"] = self.altered_dataframe[
            "timestamp"
        ].dt.month
        self.altered_dataframe["month_name"] = self.altered_dataframe[
            "timestamp"
        ].dt.month_name()
        self.altered_dataframe["year"] = self.altered_dataframe["timestamp"].dt.year
        self.altered_dataframe["has_image"] = (
            self.altered_dataframe["message"]
            .str.contains("<Media weggelaten>")
            .astype(int)
        )
        self.altered_dataframe["has_tikkie"] = (
            self.altered_dataframe["message"]
            .str.contains("<https://tikkie.me")
            .astype(int)
        )
        self.altered_dataframe["message_length"] = self.altered_dataframe[
            "message"
        ].str.len()

    def get_processed_data(self):
        """
        Haal de verwerkte DataFrame op.
        """
        return self.altered_dataframe
