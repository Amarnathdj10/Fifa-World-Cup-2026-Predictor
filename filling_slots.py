import pandas as pd

df = pd.read_csv("world_cup_dataset.csv")
pred_df = pd.read_csv("prediction_dataset.csv")

# Create lookup from 2022 finish_stage
finish_2022 = (
    df[df["year"] == 2022]
    .set_index("team")["finish_stage"]
)

# Fill previous_wc_finish for 2026 teams
pred_df["previous_wc_finish"] = (
    pred_df["team"]
    .map(finish_2022)
)

pred_df.to_csv("prediction_dataset.csv", index=False)

print("Done.")