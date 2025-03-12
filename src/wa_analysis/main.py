### Code for running the project ###

# Import packages
import logging
import tomllib
from pathlib import Path

# Import modules
from staging import dataloader
from visualising import bar_chart, time_series

# Configure logging
configfile = Path("./config.toml").resolve()
with configfile.open("rb") as f:
    config = tomllib.load(f)
root = Path("./").resolve()
logfolder = root / Path(config["logging"])
datafile = logfolder / config["log_file"]

logging.basicConfig(level=logging.INFO, filename=datafile, filemode="w")


def run_project():
    """
    This function runs the program in the correct sequence
    """

    # Step 1: Load the data
    try:
        print("Started data load...")
        logging.info("Started data load...")
        loaded_dataframe = dataloader.load_data()
        logging.info("Finished data load succesfully!")
    except Exception:
        logging.error("Error occured during data load... Please fix!")
        print("Error in data load step, see logging files for more information...")

    # Step 2: Visualize the bars
    try:
        print("Started visualising bar chart...")
        logging.info("Started visualising bar chart...")
        bar_chart.make_barchart(loaded_dataframe)
        logging.info("Bar chart created!")
        print("Bar chart created!")
    except Exception:
        logging.error("Error occured during visualising bar chart.. Please fix!")
        print(
            "Error in bar chart visualising step, see logging files for more information..."
        )

    # Step 3: Visualize the time series chart
    try:
        print("Started visualising time series chart...")
        logging.info("Started visualising time series chart...")
        time_series.make_timeseries()
        logging.info("Time series chart created!")
        print("Time series chart created!")
    except Exception:
        logging.error(
            "Error occured during visualising time series chart.. Please fix!"
        )
        print(
            "Error in time series chart visualising step, see logging files for more information..."
        )


if __name__ == "__main__":
    run_project()
