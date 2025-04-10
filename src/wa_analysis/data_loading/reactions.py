import pandas as pd

from wa_analysis.data_loading.processor import DataProcessor


class ReactionsAdder(DataProcessor):
    def __init__(self, config, df: pd.DataFrame):
        self.df = df

    def create_reaction_dataframe(self):
        """
        Haalt berichten eruit die geen beantwoorder hebben
        """
        self.df = self.df[self.df["prev_author"].notna()]
        self.df = self.df[self.df["author"] != self.df["prev_author"]].copy()
        return self.df

    def add_buckets(self):
        """
        Voegt reactietijd buckets toe aan de dataframe
        """
        buckets = [0, 1, 5, 15, 30, 60, 120, 240, self.df["time_since_prev"].max()]
        self.df["reactietijd_bucket"] = pd.cut(self.df["time_since_prev"], buckets)
        return self.df

    def calculate_percentages(self):
        """
        Bereken percentage van totaal en cumulatief percentage
        """
        reactie_counts = self.df["reactietijd_bucket"].value_counts().sort_index()
        total_count = reactie_counts.sum()
        percentage_counts = reactie_counts / total_count
        # Bereken de werkelijke cumulatieve som
        cumulative_percentage = percentage_counts.cumsum()
        return reactie_counts, percentage_counts, cumulative_percentage, total_count

    def process_data(self):
        """
        Voert alle bewerkingen uit en geeft de dataframe terug
        """
        self.create_reaction_dataframe()
        self.add_buckets()
        reactie_counts, percentage_counts, cumulative_percentage, total_count = (
            self.calculate_percentages()
        )
        return (
            self.df,
            reactie_counts,
            percentage_counts,
            cumulative_percentage,
            total_count,
        )
