import pandas as pd


df = pd.read_csv("world_cup_dataset.csv")

stats_data = [
    [37,14,52,49]
]

stats_df = pd.DataFrame(
    stats_data,
    columns=[
        "matches_played",
        "wins",
        "goals_scored",
        "goals_conceded"
    ]
)

# Create derived features
stats_df["win_percentage_since_last_cup"] = (
    (stats_df["wins"] / stats_df["matches_played"]).round(2)
)

stats_df["goals_scored_per_game"] = (
    (stats_df["goals_scored"] / stats_df["matches_played"]).round(2)
)

stats_df["goals_conceded_per_game"] = (
    (stats_df["goals_conceded"] / stats_df["matches_played"]).round(2)
)

df["win_percentage_since_last_cup"] = stats_df["win_percentage_since_last_cup"]

df["goals_scored_per_game"] = stats_df["goals_scored_per_game"]

df["goals_conceded_per_game"] = stats_df["goals_conceded_per_game"]

df.to_csv("world_cup_dataset.csv", index=False)

print(df.head())
