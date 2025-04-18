from pathlib import Path
from typing import Any, Dict

import pandas as pd

from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.logger import Logger

# Setup logger
logger = Logger().get_logger()


class Merger(DataProcessor):
    def __init__(
        self, config: Dict[str, Any], altered_df: pd.DataFrame, role_file: Path
    ) -> None:
        logger.info("Initialiseren van Merger")
        # Je hebt al altered_df, dus we hoeven geen data opnieuw te laden via de BaseDataLoader
        self.altered_dataframe = altered_df
        logger.debug(f"Altered dataframe met vorm: {altered_df.shape}")

        self.role_file = role_file
        logger.debug(f"Role file: {role_file}")

        self.player_roles = self.load_player_roles()
        logger.info(f"Spelerrollen geladen met {len(self.player_roles)} entries")

        self.merged_dataframe = self.merge_dataframes()
        logger.info(
            f"Dataframes samengevoegd, resultaat heeft vorm: {self.merged_dataframe.shape}"
        )

    def load_player_roles(self) -> pd.DataFrame:
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

    def merge_dataframes(self) -> pd.DataFrame:
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

    def get_processed_data(self) -> pd.DataFrame:
        """
        Haal het verwerkte DataFrame op.
        """
        logger.info("Ophalen van verwerkt dataframe")
        return self.merged_dataframe
