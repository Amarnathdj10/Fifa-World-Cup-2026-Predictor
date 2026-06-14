import pandas as pd

df = pd.read_csv("world_cup_dataset.csv")

# Keep only 2022 rows
prediction_df = df[df["year"] == 2022].copy()

# Change year to 2026
prediction_df["year"] = 2026

# Empty the feature columns
prediction_df["elo_rating"] = None
prediction_df["win_percentage_since_last_cup"] = None
prediction_df["goals_scored_per_game"] = None
prediction_df["goals_conceded_per_game"] = None
prediction_df["points_per_game"] = None
prediction_df["previous_wc_finish"] = None

# Remove target column
prediction_df = prediction_df.drop(columns=["finish_stage"])

prediction_df.to_csv(
    "prediction_dataset.csv",
    index=False
)

print(prediction_df.head())