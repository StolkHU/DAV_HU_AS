import pandas as pd

from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.logger import Logger

# Setup logger
logger = Logger().get_logger()


class Merger(DataProcessor):
    def __init__(self, config, altered_df, role_file):
        logger.info("Initialiseren van Merger")
        # Je hebt al altered_df, dus we hoeven geen data opnieuw te laden via de BaseDataLoader
        self.altered_dataframe = (
            altered_df  # We gebruiken de altered_df die we al hebben
        )
        logger.debug(f"Altered dataframe met vorm: {altered_df.shape}")

        self.role_file = role_file
        logger.debug(f"Role file: {role_file}")

        self.player_roles = self.load_player_roles()  # Laad de spelerrollen
        logger.info(f"Spelerrollen geladen met {len(self.player_roles)} entries")

        self.merged_dataframe = self.merge_dataframes()  # Combineer de dataframes
        logger.info(
            f"Dataframes samengevoegd, resultaat heeft vorm: {self.merged_dataframe.shape}"
        )

    def load_player_roles(self):
        """
        Laad de rollen van de spelers uit een JSON-bestand.
        """
        logger.info(f"Laden van spelerrollen uit: {self.role_file}")
        try:
            roles_df = pd.read_json(self.role_file, encoding="latin")
            logger.debug(f"Spelerrollen geladen met vorm: {roles_df.shape}")
            return roles_df
        except Exception as e:
            logger.error(f"Fout bij het laden van spelerrollen: {str(e)}")
            raise

    def merge_dataframes(self):
        """
        Voeg de spelerrollen toe aan de hoofdgegevens op basis van de auteur.
        """
        logger.info("Samenvoegen van dataframes op basis van auteur")
        try:
            merged_df = pd.merge(
                self.altered_dataframe,
                self.player_roles,
                left_on="author",
                right_on="Author",
            )
            logger.debug(f"Samengevoegd resultaat heeft vorm: {merged_df.shape}")

            # Rapporteer hoeveel rijen behouden zijn
            pct_behouden = (merged_df.shape[0] / self.altered_dataframe.shape[0]) * 100
            logger.info(
                f"Samenvoeging behield {pct_behouden:.1f}% van de oorspronkelijke rijen"
            )

            return merged_df
        except Exception as e:
            logger.error(f"Fout bij het samenvoegen van dataframes: {str(e)}")
            raise

    def get_processed_data(self):
        """
        Haal het verwerkte DataFrame op.
        """
        logger.info("Ophalen van verwerkt dataframe")
        return self.merged_dataframe


if __name__ == "__main__":
    logger.info("Start uitvoering merger.py")

    try:
        # Laad configuratie en data
        config_loader = ConfigLoader()
        logger.info("Configuratie geladen")

        processor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_hockeyteam
        )
        logger.info("DataProcessor geïnitialiseerd")

        altered_df = processor.add_columns()
        logger.info("Kolommen toegevoegd aan dataframe")

        merger = Merger(
            config=config_loader.config,
            altered_df=altered_df,
            role_file=config_loader.role_file,
        )
        logger.info("Merger geïnitialiseerd")

        merged_df = merger.get_processed_data()
        logger.info(f"Samengevoegd dataframe heeft vorm: {merged_df.shape}")
        logger.info("Einde uitvoering merger.py - Succesvol")

    except Exception as e:
        logger.error(f"Fout bij uitvoeren van merger.py: {str(e)}")
