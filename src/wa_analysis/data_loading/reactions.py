import pandas as pd

from wa_analysis.data_loading.processor import DataProcessor
from wa_analysis.settings.logger import Logger

# Setup logger
logger = Logger().get_logger()


class ReactionsAdder(DataProcessor):
    def __init__(self, config, df: pd.DataFrame):
        logger.info("Initialiseren ReactionsAdder")
        self.df = df
        logger.debug(f"DataFrame geladen met vorm: {df.shape}")

    def create_reaction_dataframe(self):
        """
        Haalt berichten eruit die geen beantwoorder hebben
        """
        logger.info("Filteren van berichten die geen antwoord zijn")
        try:
            original_shape = self.df.shape

            # Filter berichten zonder voorgaande auteur
            self.df = self.df[self.df["prev_author"].notna()]
            na_filtered_shape = self.df.shape
            logger.debug(
                f"Na filteren op notna: {na_filtered_shape[0]} rijen (verwijderd: {original_shape[0] - na_filtered_shape[0]})"
            )

            # Filter berichten waar dezelfde persoon reageert op zichzelf
            self.df = self.df[self.df["author"] != self.df["prev_author"]].copy()
            self_filtered_shape = self.df.shape
            logger.debug(
                f"Na filteren op zelf-reacties: {self_filtered_shape[0]} rijen (verwijderd: {na_filtered_shape[0] - self_filtered_shape[0]})"
            )

            # Log percentage behouden berichten
            pct_behouden = (self_filtered_shape[0] / original_shape[0]) * 100
            logger.info(
                f"Reactiefiltering voltooid, {pct_behouden:.1f}% van de berichten behouden"
            )

            return self.df

        except Exception as e:
            logger.error(f"Fout bij het maken van reactie-dataframe: {str(e)}")
            raise

    def add_buckets(self):
        """
        Voegt reactietijd buckets toe aan de dataframe
        """
        logger.info("Toevoegen van reactietijd buckets")
        try:
            max_time = self.df["time_since_prev"].max()
            buckets = [0, 1, 5, 15, 30, 60, 120, 240, max_time]
            logger.debug(f"Buckets: {buckets}")

            self.df["reactietijd_bucket"] = pd.cut(self.df["time_since_prev"], buckets)

            # Log aantal berichten per bucket
            bucket_counts = self.df["reactietijd_bucket"].value_counts().sort_index()
            logger.debug(f"Berichten per bucket: {bucket_counts}")

            logger.info(
                f"Reactietijd buckets toegevoegd (max tijd: {max_time:.1f} min)"
            )
            return self.df

        except Exception as e:
            logger.error(f"Fout bij het toevoegen van buckets: {str(e)}")
            raise

    def calculate_percentages(self):
        """
        Bereken percentage van totaal en cumulatief percentage
        """
        logger.info("Berekenen van percentages en cumulatieve percentages")
        try:
            reactie_counts = self.df["reactietijd_bucket"].value_counts().sort_index()
            total_count = reactie_counts.sum()
            logger.debug(f"Totaal aantal reacties: {total_count}")

            percentage_counts = reactie_counts / total_count
            logger.debug(f"Percentage per bucket: {percentage_counts}")

            # Bereken de werkelijke cumulatieve som
            cumulative_percentage = percentage_counts.cumsum()
            logger.debug(f"Cumulatief percentage: {cumulative_percentage}")

            logger.info(f"Percentages berekend voor {total_count} reacties")
            return reactie_counts, percentage_counts, cumulative_percentage, total_count

        except Exception as e:
            logger.error(f"Fout bij het berekenen van percentages: {str(e)}")
            raise

    def process_data(self):
        """
        Voert alle bewerkingen uit en geeft de dataframe terug
        """
        logger.info("Start verwerking reactiedata")
        try:
            self.create_reaction_dataframe()
            self.add_buckets()
            reactie_counts, percentage_counts, cumulative_percentage, total_count = (
                self.calculate_percentages()
            )

            logger.info(f"Reactiedata verwerking voltooid voor {total_count} berichten")
            return (
                self.df,
                reactie_counts,
                percentage_counts,
                cumulative_percentage,
                total_count,
            )

        except Exception as e:
            logger.error(f"Fout bij het verwerken van reactiedata: {str(e)}")
            raise
