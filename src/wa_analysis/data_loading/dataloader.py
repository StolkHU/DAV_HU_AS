### This module loads the data and adds the roles of the players ###

from pathlib import Path

import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.settings.logger import Logger


# Basis dataloader class. Aan de hand van de folder pakt hij de data
class BaseDataLoader:
    def __init__(self, config, datafile=None):
        # Initialiseer de logger
        self.logger = Logger().get_logger()
        self.logger.info(f"Initializing BaseDataLoader with datafile: {datafile}")

        self.processed = Path(config["processed"]).resolve()
        self.config = config
        self.datafile = datafile

        self.logger.debug(f"Processed directory: {self.processed}")

        if self.datafile is not None:
            self.logger.info(f"Loading data from file: {self.datafile}")
            self.df = self.load_data()
        else:
            self.logger.warning("No datafile specified, df set to None")
            self.df = None  # Als geen bestand is opgegeven, stel df in op None

    def load_data(self):
        """
        Laad data op basis van het bestandstype uit de configuratie.
        Ondersteunt bijvoorbeeld JSON, Parquet of CSV.
        """
        file_path = self.processed / Path(self.datafile)
        file_extension = file_path.suffix

        self.logger.info(
            f"Loading data from {file_path} with extension {file_extension}"
        )

        try:
            if file_extension == ".json":
                self.logger.debug("Loading JSON file")
                df = pd.read_json(file_path, encoding="latin")
            elif file_extension == ".csv":
                self.logger.debug("Loading CSV file")
                df = pd.read_csv(file_path)
            elif file_extension == ".parq":
                self.logger.debug("Loading Parquet file")
                df = pd.read_parquet(file_path)
            else:
                error_msg = f"Unsupported file format: {file_extension}. Only CSV, Parquet and JSON are supported."
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            self.logger.info(f"Successfully loaded dataframe with shape: {df.shape}")
            return df

        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            raise


if __name__ == "__main__":
    logger = Logger().get_logger()
    logger.info("Starting data loading process")

    try:
        config_loader = ConfigLoader()
        logger.info("Config loaded successfully")

        logger.info("Loading hockey team data")
        data_loader_hockey = BaseDataLoader(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )

        logger.info("Loading wife data")
        data_loader_wife = BaseDataLoader(
            config=config_loader.config, datafile=config_loader.datafile_wife
        )

        logger.info(f"Hockey data shape: {data_loader_hockey.df.shape}")
        logger.info(f"Wife data shape: {data_loader_wife.df.shape}")

        logger.info("Data loading completed successfully")

    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        raise
