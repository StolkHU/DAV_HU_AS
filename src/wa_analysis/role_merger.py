import pandas as pd

from wa_analysis.config import ConfigLoader
from wa_analysis.dataprocessor import DataProcessor


class Merger(DataProcessor):
    def __init__(self, config, altered_df, role_file):
        # Je hebt al altered_df, dus we hoeven geen data opnieuw te laden via de BaseDataLoader
        self.altered_dataframe = (
            altered_df  # We gebruiken de altered_df die we al hebben
        )
        self.role_file = role_file
        self.player_roles = self.load_player_roles()  # Laad de spelerrollen
        self.merged_dataframe = self.merge_dataframes()  # Combineer de dataframes

    def load_player_roles(self):
        """
        Laad de rollen van de spelers uit een JSON-bestand.
        """
        return pd.read_json(self.role_file, encoding="latin")

    def merge_dataframes(self):
        """
        Voeg de spelerrollen toe aan de hoofdgegevens op basis van de auteur.
        """
        return pd.merge(
            self.altered_dataframe,
            self.player_roles,
            left_on="author",
            right_on="Author",
        )

    def get_processed_data(self):
        """
        Haal het verwerkte DataFrame op.
        """
        return self.merged_dataframe


if __name__ == "__main__":
    # Laad configuratie en data
    config_loader = ConfigLoader()
    processor = DataProcessor(
        config=config_loader.config, datafile=config_loader.datafile
    )
    altered_df = processor.add_columns()

    merger = Merger(
        config=config_loader.config,
        altered_df=altered_df,
        role_file=config_loader.role_file,
    )
    print(merger.get_processed_data().shape)
