from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.dataloader import BaseDataLoader


class DataProcessor(BaseDataLoader):
    def __init__(self, config, datafile=None):
        # Roep de init van de superklasse aan om de data in te laden
        super().__init__(config, datafile)
        if self.df is not None:
            self.altered_dataframe = self.df.copy()
        else:
            self.altered_dataframe = None
        self.altered_dataframe = self.df.copy()

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
            .fillna("")
            .str.contains("<Media weggelaten>")
            .astype(int)
        )
        self.altered_dataframe["has_tikkie"] = (
            self.altered_dataframe["message"]
            .fillna("")
            .str.contains("<https://tikkie.me")
            .astype(int)
        )
        self.altered_dataframe["message_length"] = self.altered_dataframe[
            "message"
        ].str.len()
        self.altered_dataframe["prev_author"] = self.altered_dataframe["author"].shift(
            1
        )
        self.altered_dataframe["prev_timestamp"] = self.altered_dataframe[
            "timestamp"
        ].shift(1)
        self.altered_dataframe["time_since_prev"] = (
            self.altered_dataframe["timestamp"]
            - self.altered_dataframe["prev_timestamp"]
        ).dt.total_seconds() / 60
        return self.altered_dataframe


if __name__ == "__main__":
    config_loader = ConfigLoader()
    processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile_wife
    )
    altered = processor.add_columns()
    print(altered.shape)
