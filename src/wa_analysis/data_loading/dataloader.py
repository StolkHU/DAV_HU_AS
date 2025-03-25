### This module loads the data and adds the roles of the players ###

from pathlib import Path

import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader


# Basis dataloader class. Aan de hand van de folder pakt hij de data
class BaseDataLoader:
    def __init__(self, config, datafile=None):
        self.processed = Path(config["processed"]).resolve()
        self.config = config
        self.datafile = datafile
        if self.datafile is not None:
            self.df = self.load_data()
        else:
            self.df = None  # Als geen bestand is opgegeven, stel df in op None
        # self.df = self.load_data()

    def load_data(self):
        """
        Laad data op basis van het bestandstype uit de configuratie.
        Ondersteunt bijvoorbeeld JSON, Parquet of CSV.
        """
        file_path = self.processed / Path(self.datafile)
        file_extension = file_path.suffix

        if file_extension == ".json":
            df = pd.read_json(file_path, encoding="latin")
        elif file_extension == ".csv":
            df = pd.read_csv(file_path)
        elif file_extension == ".parq":
            df = pd.read_parquet(file_path)
        else:
            raise ValueError(
                "Unsupported file format. Only CSV, Parquet and JSON are supported."
            )

        print(df.head())
        return df


if __name__ == "__main__":
    config_loader = ConfigLoader()
    data_loader_hockey = BaseDataLoader(
        config=config_loader.config, datafile=config_loader.datafile_hockeyteam
    )
    data_loader_wife = BaseDataLoader(
        config=config_loader.config, datafile=config_loader.datafile_wife
    )
