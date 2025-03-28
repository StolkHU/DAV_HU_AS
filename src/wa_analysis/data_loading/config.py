### This module is to load the dataframe using the configfile

import tomllib
from pathlib import Path


class ConfigLoader:
    def __init__(self):
        self.config_path = Path("./config.toml").resolve()
        self.config = self.load_config()

        self.root = Path("./").resolve()
        self.processed = self.root / Path(
            self.config["processed"]
        )  # pad naar de processed-folder
        self.raw = self.root / Path(self.config["raw"])  # pad naar de raw-folder
        self.datafile_hockeyteam = self.processed / (
            self.config["current"]
        )  # gebruik het hockeyteam bestand
        self.datafile_wife = self.processed / (
            self.config["wife_file"]
        )  # gebruik het wife bestand
        self.role_file = self.raw / Path(self.config["role_file"])
        self.output_folder = self.root / Path(self.config["output_folder"])

    def load_config(self):
        with self.config_path.open("rb") as f:
            return tomllib.load(f)


if __name__ == "__main__":
    config_loader = ConfigLoader()
    print(config_loader.config)
