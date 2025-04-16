### This module is to load the dataframe using the configfile

import tomllib
from pathlib import Path

from wa_analysis.settings.logger import Logger

# Setup logger
logger = Logger().get_logger()


class ConfigLoader:
    def __init__(self):
        logger.info("Initialiseren van ConfigLoader")
        self.config_path = Path("./config.toml").resolve()
        logger.debug(f"Config pad: {self.config_path}")

        self.config = self.load_config()

        self.root = Path("./").resolve()
        logger.debug(f"Root pad: {self.root}")

        self.processed = self.root / Path(
            self.config["processed"]
        )  # pad naar de processed-folder
        logger.debug(f"Processed pad: {self.processed}")

        self.raw = self.root / Path(self.config["raw"])  # pad naar de raw-folder
        logger.debug(f"Raw pad: {self.raw}")

        self.datafile_hockeyteam = self.processed / (
            self.config["current"]
        )  # gebruik het hockeyteam bestand
        logger.debug(f"Hockey team datafile: {self.datafile_hockeyteam}")

        self.datafile_wife = self.processed / (
            self.config["wife_file"]
        )  # gebruik het wife bestand
        logger.debug(f"Wife datafile: {self.datafile_wife}")

        self.role_file = self.raw / Path(self.config["role_file"])
        logger.debug(f"Role file: {self.role_file}")

        self.output_folder = self.root / Path(self.config["output_folder"])
        logger.debug(f"Output folder: {self.output_folder}")

        logger.info("ConfigLoader succesvol geïnitialiseerd")

    def load_config(self):
        """Laad de configuratie uit het TOML-bestand."""
        logger.info(f"Laden van configuratie uit: {self.config_path}")
        try:
            with self.config_path.open("rb") as f:
                config = tomllib.load(f)
                logger.debug(f"Configuratie geladen met {len(config)} items")
                return config
        except Exception as e:
            logger.error(f"Fout bij het laden van configuratie: {str(e)}")
            raise


if __name__ == "__main__":
    logger.info("Start uitvoering config.py")
    try:
        config_loader = ConfigLoader()
        logger.info("Configuratie succesvol geladen")
        logger.debug(f"Config inhoud: {config_loader.config}")
    except Exception as e:
        logger.error(f"Fout bij uitvoeren van config.py: {str(e)}")
