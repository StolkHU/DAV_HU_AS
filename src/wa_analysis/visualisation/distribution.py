import tomllib
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

configfile = Path("../config.toml").resolve()
with configfile.open("rb") as f:
    config = tomllib.load(f)
config

root = Path("..").resolve()
processed = root / Path(config["processed"])
raw = root / Path(config["raw"])
datafile = processed / config["wife_file"]

merged_df = pd.read_parquet(datafile)
merged_df.dtypes
merged_df["message_length"] = merged_df["message"].str.len()
merged_df["prev_author"] = merged_df["author"].shift(1)
merged_df["prev_timestamp"] = merged_df["timestamp"].shift(1)
merged_df["time_since_prev"] = (
    merged_df["timestamp"] - merged_df["prev_timestamp"]
).dt.total_seconds() / 60
merged_df.head()

# alleen responses meenemen die volgen op een andere vorige auteur
responses = merged_df[merged_df["author"] != merged_df["prev_author"]].copy()

# aanmaken van de buckets
buckets = [0, 1, 5, 15, 30, 60, 120, 240, responses["time_since_prev"].max()]
responses["reactietijd_bucket"] = pd.cut(responses["time_since_prev"], buckets)

# percentage van totaal berekenen
reactie_counts = responses["reactietijd_bucket"].value_counts().sort_index()
total_count = reactie_counts.sum()
percentage_counts = (reactie_counts / total_count) * 100
cumulative_percentage = percentage_counts.cumsum()

# Labels voor de buckets
bucket_labels = [
    "<1 min",
    "1-5 min",
    "5-15 min",
    "15-30 min",
    "30-60 min",
    "1-2 uur",
    "2-4 uur",
    ">4 uur",
]
bucket_labels = bucket_labels[: len(reactie_counts)]

# opbouw van de figuur
fig, ax1 = plt.subplots(figsize=(10, 6))


# kleuren
colors = ["#FF9999" if i < 3 else "silver" for i in range(len(bucket_labels))]

# Bar plot for counts
ax1.bar(bucket_labels, reactie_counts.values, color=colors, width=0.90)
ax1.set_title(
    "Ruim 73% van alle berichten wordt binnen een kwartier beantwoord",
    fontsize=12,
    style="oblique",
    pad=20,
)
ax1.set_xlabel("Reactietijd", fontsize=12)
ax1.set_ylabel("Aantal reacties", fontsize=12)
ax1.tick_params(axis="x", rotation=45)

# Voeg waarden toe boven de bars
# for i, v in enumerate(reactie_counts.values):
#     ax1.text(i, v + 0.1, str(v), ha='center', fontsize=9)

ax2 = ax1.twinx()
ax2.plot(
    bucket_labels, cumulative_percentage.values, color="black", linewidth=3
)  # marker='o',
ax2.set_ylabel("Cumulatief Percentage", fontsize=12)
ax2.tick_params(axis="y", colors="black")

ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x)}%"))
ax2.set_ylim(0, 102.5)
# ax1.set_ylim(0,12000)
ax1.yaxis.grid(True)
ax1.set_axisbelow(True)

plt.suptitle("Liefde op het eerste bericht", fontsize=16, fontweight="bold")
plt.figtext(
    0.35,
    0.00,
    f"Totaal aantal berichten met response: {total_count:,}".replace(",", "."),
    ha="right",
    fontsize=10,
)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax1.tick_params(axis="both", which="both", length=0)
ax2.tick_params(axis="both", which="both", length=0)

plt.tight_layout()
plt.show()

# total_count = reactie_counts.sum()
# first_three_buckets_percentage = (reactie_counts.iloc[:3].sum() / total_count) * 100
# print(f"Het percentage van de eerste drie buckets is {first_three_buckets_percentage:.2f}%")
