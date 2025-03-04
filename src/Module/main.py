### Code for Categorical Visualizations ###
from pathlib import Path
from loguru import logger
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tomllib

def categorical_visualization() :
    configfile = Path("../DAV_HU_AS/config.toml").resolve()
    with configfile.open("rb") as f:
        config = tomllib.load(f)
    print(config)

    root = Path("../DAV_HU_AS").resolve()
    processed = root / Path(config["processed"])
    raw = root / Path(config["raw"])
    datafile = processed / config["current"]

    base_dataframe = pd.read_parquet(datafile)

    # Toevoegen namen van staf
    namen_staff = [
    "bellowing-tarsier",
    "carefree-kouprey",
    "frolicsome-whistling duck",
    "glittering-eland",
    "groovy-ostrich",
    "loony-penguin",
    "mirthful-louse",
    "motley-fox",
    "patchwork-gerbil",
    "rib-tickling-hamster",
    "roaring-cassowary",
    "sparkling-sand dollar",
    "vivacious-dogfish",
    "wacky-hummingbird"
    ]
    base_dataframe["function"] = base_dataframe["author"].apply(
        lambda
          x: "Staff" if any(name in x for name in namen_staff) else "Player"
    )

    # Toevoegen date kolommen
    base_dataframe["day_of_month"] = base_dataframe["timestamp"].dt.day
    base_dataframe["day"] = base_dataframe["timestamp"].dt.day_name()
    base_dataframe["month_number"] = base_dataframe["timestamp"].dt.month
    base_dataframe["month_name"] = base_dataframe["timestamp"].dt.month_name()
    base_dataframe["year"] = base_dataframe["timestamp"].dt.year
    base_dataframe["has_image"] = base_dataframe["message"].str.contains("<Media weggelaten>").astype(int)

    base_dataframe["message_length"] = base_dataframe["message"].str.len()

    p1 = (
        base_dataframe[["function", "message_length"]]
        .groupby("function")
        .mean()
        .sort_values("message_length", ascending=False)
    )

    sns.barplot(x=p1.index, y=p1["message_length"], palette = ["darkolivegreen", "lightgrey"]  )
    plt.xlabel("Function within team")
    plt.ylabel("Average Message length")
    plt.title("Staff members sending longer messages")
    plt.show()

    # Opslaan van de plot
    output_dir = Path("img/automatic")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "average_message_length.png")
    

if __name__ == "__main__":
    categorical_visualization()