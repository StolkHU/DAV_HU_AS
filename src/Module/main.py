### Code for Categorical Visualizations ###
import tomllib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def categorical_visualization():
    configfile = Path("./config.toml").resolve()
    with configfile.open("rb") as f:
        config = tomllib.load(f)

    root = Path("./").resolve()
    processed = root / Path(config["processed"])
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
        "wacky-hummingbird",
    ]
    base_dataframe["function"] = base_dataframe["author"].apply(
        lambda x: "Staff" if any(name in x for name in namen_staff) else "Player"
    )

    # Toevoegen date kolommen
    base_dataframe["day_of_month"] = base_dataframe["timestamp"].dt.day
    base_dataframe["day"] = base_dataframe["timestamp"].dt.day_name()
    base_dataframe["month_number"] = base_dataframe["timestamp"].dt.month
    base_dataframe["month_name"] = base_dataframe["timestamp"].dt.month_name()
    base_dataframe["year"] = base_dataframe["timestamp"].dt.year
    base_dataframe["has_image"] = (
        base_dataframe["message"].str.contains("<Media weggelaten>").astype(int)
    )

    # Berekenen lengte, lengte van player messages en staff messages voor de string
    base_dataframe["message_length"] = base_dataframe["message"].str.len()
    player_message_count = base_dataframe[
        base_dataframe["function"] == "Player"
    ].count()["message"]
    staff_message_count = base_dataframe[base_dataframe["function"] == "Staff"].count()[
        "message"
    ]

    # Dataframe voor de visual
    p1 = (
        base_dataframe[["function", "message_length"]]
        .groupby("function")
        .mean()
        .sort_values("message_length", ascending=False)
    )

    # Barplot creëren
    sns.barplot(x=p1.index, y=p1["message_length"], palette=["red", "lightgrey"])
    for i, v in enumerate(p1["message_length"]):
        plt.text(i, v * 0.98, f"{v:.1f}", ha="center", va="top", fontsize=12)
    plt.xlabel("Function within team")
    plt.ylabel("Average Message length")
    plt.title("Staff members sending longer messages")
    plt.figtext(
        0.05,
        0.05,
        f"Gebaseerd op {player_message_count:,}".replace(",", ".")
        + f" berichten van de players en {staff_message_count:,}".replace(",", ".")
        + f" berichten van de staff.",
        ha="left",
        va="center",
        fontsize=8,
        fontstyle="italic",
    )
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    # Opslaan van de plot
    output_dir = Path("img/automatic")
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_dir / "Average Message Length.png")


if __name__ == "__main__":
    categorical_visualization()
