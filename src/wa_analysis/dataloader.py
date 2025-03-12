### This module loads the data and adds the roles of the players ###

from pathlib import Path

import pandas as pd


class BaseDataLoader:
    def __init__(self, config):
        self.raw = Path("./data/processed").resolve()
        self.config = config
        self.df = self.load_data()

    def load_data(self):
        """
        Laad data op basis van het bestandstype uit de configuratie.
        Ondersteunt bijvoorbeeld JSON of CSV.
        """
        file_path = self.raw / Path(self.config["current"])
        file_extension = file_path.suffix

        if file_extension == ".json":
            df = pd.read_json(file_path, encoding="latin")
        elif file_extension == ".csv":
            df = pd.read_csv(file_path)
        elif file_extension == ".parq":
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(
                "Unsupported file format. Only CSV and JSON are supported."
            )

        print(df.head())
        return df
