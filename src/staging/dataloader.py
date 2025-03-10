### This module loads the data and adds the roles of the players ###

import tomllib
from pathlib import Path

import pandas as pd


# Class to load in the data
class ConfigLoader:
    def __init__(self, config_path, datafile=None):
        self.config_path = Path(config_path).resolve()
        self.config = self.load_config()
        self.root = Path("./").resolve()
        self.processed = self.root / Path(self.config["processed"])
        self.datafile = self.processed / (
            datafile if datafile else self.config["current"]
        )
        self.df = self.load_dataframe()

    def load_config(self):
        with self.config_path.open("rb") as f:
            return tomllib.load(f)

    def load_dataframe(self):
        return pd.read_parquet(self.datafile)


# Class to add the roles of players and staff to the dataframe
class RoleFileAdder:
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


# Class to add columns based on date and images #
class ColumnAdder:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.add_columns()

    def add_columns(self):
        self.dataframe["day_of_month"] = self.dataframe["timestamp"].dt.day
        self.dataframe["day"] = self.dataframe["timestamp"].dt.day_name()
        self.dataframe["month_number"] = self.dataframe["timestamp"].dt.month
        self.dataframe["month_name"] = self.dataframe["timestamp"].dt.month_name()
        self.dataframe["year"] = self.dataframe["timestamp"].dt.year
        self.dataframe["has_image"] = (
            self.dataframe["message"].str.contains("<Media weggelaten>").astype(int)
        )


def load_data():
    config_loader = ConfigLoader("./config.toml")
    df = config_loader.df
    print(df.head())

    role_file_adder = RoleFileAdder(config_loader.config, df)
    merged_df = role_file_adder.merged_dataframe
    print(merged_df.head())

    column_adder = ColumnAdder(merged_df)
    updated_df = column_adder.dataframe
    print(updated_df.head())

    return updated_df


if __name__ == "__main__":
    load_data()
