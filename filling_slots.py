import pandas as pd

df = pd.read_csv("world_cup_dataset.csv")

finish_2018 = (
    df[df["year"] == 2018]
    .set_index("team")["finish_stage"]
)

mask = df["year"] == 2022

df.loc[mask, "previous_wc_finish"] = (
    df.loc[mask, "team"]
    .map(finish_2018)
)

df.to_csv("world_cup_dataset.csv", index=False)

print("Done.")