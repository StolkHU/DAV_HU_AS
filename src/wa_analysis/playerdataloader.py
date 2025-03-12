### This module loads the data and adds the roles of the players ###

from pathlib import Path

import pandas as pd
from config import ConfigLoader


# Class to add the roles of players and staff to the dataframe
class DataLoader:
    def __init__(self, config, df):
        self.raw = Path("./data/raw").resolve()
        self.role_file = self.raw / Path(config["role_file"])
        self.df = df
        self.player_roles = self.load_player_roles()
        self.merged_dataframe = self.merge_dataframes()

    # Get the player information from the json
    def load_player_roles(self):
        return pd.read_json(self.role_file, encoding="latin")

    # Merge the dataframes based on autheur name
    def merge_dataframes(self):
        return pd.merge(self.df, self.player_roles, left_on="author", right_on="Author")

    def add_columns(self):
        self.merged_dataframe["day_of_month"] = self.merged_dataframe[
            "timestamp"
        ].dt.day
        self.merged_dataframe["day"] = self.merged_dataframe["timestamp"].dt.day_name()
        self.merged_dataframe["month_number"] = self.merged_dataframe[
            "timestamp"
        ].dt.month
        self.merged_dataframe["month_name"] = self.merged_dataframe[
            "timestamp"
        ].dt.month_name()
        self.merged_dataframe["year"] = self.merged_dataframe["timestamp"].dt.year
        self.merged_dataframe["has_image"] = (
            self.merged_dataframe["message"]
            .str.contains("<Media weggelaten>")
            .astype(int)
        )
        self.merged_dataframe["has_tikkie"] = (
            self.merged_dataframe["message"]
            .str.contains("<https://tikkie.me")
            .astype(int)
        )
        self.merged_dataframe["message_length"] = self.merged_dataframe[
            "message"
        ].str.len()

    @staticmethod
    def load_data():
        config_loader = ConfigLoader("./config.toml")
        config = config_loader.config
        df = config_loader.df

        data_loader = DataLoader(config, df)
        data_loader.add_columns()
        return data_loader.merged_dataframe


if __name__ == "__main__":
    processed_data = DataLoader.load_data()
    print(processed_data.head())
