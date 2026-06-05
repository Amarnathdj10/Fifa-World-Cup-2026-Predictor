import pandas as pd

wc_df = pd.read_csv('D:\Coding journey\Fifa World Cup 2026 Predictor\world_cup_dataset.csv')
elo_df = pd.read_csv('D:\Coding journey\Fifa World Cup 2026 Predictor\eloratings.csv')

wc_df = wc_df.drop(columns=['elo_rating'])

elo_df["team"] = elo_df["team"].replace({
    "South Korea": "Korea Republic",
    "United States": "USA",
    "Côte d'Ivoire": "Ivory Coast",
    "Curaçao": "Curacao",
    "Czechia": "Czech Republic",
    "Democratic Republic of Congo": "Congo DR",
    "Cabo Verde": 'Cape Verde'
})

elo_df = elo_df.drop(columns=['change'])

#print(wc_df.head())
#print(elo_df.head())

elo_df['date'] = pd.to_datetime(elo_df['date'],format="mixed")

world_cups = {
    2014: "2014-06-11",
    2018: "2018-06-14",
    2022: "2022-11-20"
}

elo_snapshots = []

for wc_year, cutoff in world_cups.items():

    cutoff = pd.Timestamp(cutoff)

    temp = elo_df[elo_df["date"] <= cutoff]

    latest = (
        temp.sort_values("date")
            .groupby("team")
            .tail(1)
            .copy()
    )

    latest["year"] = wc_year

    elo_snapshots.append(
        latest[["team", "year", "elo_rating"]]
    )

elo_wc = pd.concat(
    elo_snapshots,
    ignore_index=True
)

wc_df = wc_df.merge(
    elo_wc,
    on=["team", "year"],
    how="left"
)

print(
    wc_df[wc_df["elo_rating"].isna()]
    [["team", "year"]]
)

wc_df.to_csv(
   r"D:\Coding journey\Fifa World Cup 2026 Predictor\world_cup_dataset.csv",
   index=False
)