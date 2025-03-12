import pandas as pd

from wa_analysis.playerdataloader import DataProcessor


class Merger(DataProcessor):
    def __init__(self, config, role_file):
        # Roep de init van de superklasse aan om de data in te laden
        super().__init__(config)
        self.role_file = role_file
        self.player_roles = self.load_player_roles()
        self.merged_dataframe = self.merge_dataframes()

    def load_player_roles(self):
        """
        Laad de rollen van de spelers uit een JSON-bestand.
        """
        return pd.read_json(self.role_file, encoding="latin")

    def merge_dataframes(self):
        """
        Voeg de spelerrollen toe aan de hoofdgegevens op basis van de auteur.
        """
        return pd.merge(self.df, self.player_roles, left_on="author", right_on="Author")

    def get_processed_data(self):
        """
        Haal de verwerkte DataFrame op.
        """
        return self.merged_dataframe
