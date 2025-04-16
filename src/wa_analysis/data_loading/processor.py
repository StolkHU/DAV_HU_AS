from wa_analysis.data_loading.config import ConfigLoader
from wa_analysis.data_loading.dataloader import BaseDataLoader
from wa_analysis.settings.logger import Logger

# Setup logger als deze niet al is geïmporteerd via BaseDataLoader
logger = Logger().get_logger()


class DataProcessor(BaseDataLoader):
    def __init__(self, config, datafile=None):
        logger.info(f"Initialiseren DataProcessor voor bestand: {datafile}")
        # Roep de init van de superklasse aan om de data in te laden
        super().__init__(config, datafile)

        if self.df is not None:
            logger.info(f"Kopie maken van DataFrame met vorm: {self.df.shape}")
            self.altered_dataframe = self.df.copy()
        else:
            logger.warning("Geen DataFrame beschikbaar om te verwerken")
            self.altered_dataframe = None

    def add_columns(self):
        """
        Voeg extra kolommen toe aan de samengevoegde DataFrame.
        """
        logger.info("Toevoegen van extra kolommen aan DataFrame")

        try:
            if self.altered_dataframe is None:
                raise ValueError(
                    "Geen DataFrame beschikbaar om kolommen aan toe te voegen"
                )

            # Datum/tijd kolommen
            logger.debug("Toevoegen datum/tijd kolommen")
            self.altered_dataframe["day_of_month"] = self.altered_dataframe[
                "timestamp"
            ].dt.day
            self.altered_dataframe["day"] = self.altered_dataframe[
                "timestamp"
            ].dt.day_name()
            self.altered_dataframe["month_number"] = self.altered_dataframe[
                "timestamp"
            ].dt.month
            self.altered_dataframe["month_name"] = self.altered_dataframe[
                "timestamp"
            ].dt.month_name()
            self.altered_dataframe["year"] = self.altered_dataframe["timestamp"].dt.year

            # Media en bericht kolommen
            logger.debug("Toevoegen van media en berichtkolommen")
            self.altered_dataframe["has_image"] = (
                self.altered_dataframe["message"]
                .fillna("")
                .str.contains("<Media weggelaten>")
                .astype(int)
            )
            self.altered_dataframe["has_tikkie"] = (
                self.altered_dataframe["message"]
                .fillna("")
                .str.contains("<https://tikkie.me")
                .astype(int)
            )
            self.altered_dataframe["message_length"] = self.altered_dataframe[
                "message"
            ].str.len()

            # Kolommen voor interactie-analyse
            logger.debug("Toevoegen van interactie-analysekolommen")
            self.altered_dataframe["prev_author"] = self.altered_dataframe[
                "author"
            ].shift(1)
            self.altered_dataframe["prev_timestamp"] = self.altered_dataframe[
                "timestamp"
            ].shift(1)
            self.altered_dataframe["time_since_prev"] = (
                self.altered_dataframe["timestamp"]
                - self.altered_dataframe["prev_timestamp"]
            ).dt.total_seconds() / 60

            # Samenvattende statistieken loggen
            img_count = self.altered_dataframe["has_image"].sum()
            tikkie_count = self.altered_dataframe["has_tikkie"].sum()
            avg_msg_len = self.altered_dataframe["message_length"].mean()

            logger.info(
                f"Kolommen toegevoegd: {len(self.altered_dataframe.columns)} kolommen totaal"
            )
            logger.info(
                f"Statistieken: {img_count} afbeeldingen, {tikkie_count} tikkies, gemiddelde berichtlengte: {avg_msg_len:.1f}"
            )

            return self.altered_dataframe

        except Exception as e:
            logger.error(f"Fout bij het toevoegen van kolommen: {str(e)}")
            raise


if __name__ == "__main__":
    logger.info("Start uitvoering processor.py")

    try:
        config_loader = ConfigLoader()
        logger.info("Configuratie geladen")

        processor = DataProcessor(
            config=config_loader.config, datafile=config_loader.datafile_wife
        )
        logger.info("DataProcessor geïnitialiseerd")

        altered = processor.add_columns()
        logger.info(f"DataFrame verwerkt met vorm: {altered.shape}")
        logger.info("Einde uitvoering processor.py - Succesvol")

    except Exception as e:
        logger.error(f"Fout bij uitvoeren van processor.py: {str(e)}")
