### This module is to load the dataframe using the configfile

import tomllib
from pathlib import Path

import pandas as pd


# Class to load configurations
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
