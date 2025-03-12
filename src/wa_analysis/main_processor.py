from pathlib import Path

from wa_analysis.config import ConfigLoader
from wa_analysis.playerdataloader import DataProcessor


class MainProcessor:
    @staticmethod
    def load_data():
        # Laad configuratie en data
        config_loader = ConfigLoader("./config.toml")
        config = config_loader.config

        # Verwerk de data via de DataProcessor klasse (nu met de superklasse functionaliteit)
        data_processor = DataProcessor(
            config, config_loader.raw / Path(config["role_file"])
        )
        data_processor.add_columns()

        return data_processor.get_processed_data()


if __name__ == "__main__":
    processed_data = MainProcessor.load_data()
    print(processed_data.head())
