import pandas as pd


df = pd.read_csv("world_cup_dataset.csv")

stats_data = [
    [29,11,43,41,32],#austria
    [31,16,51,29,58],#belgium
    [29,16,56,30,52],#bosnia
    [34,17,51,33,59],#croatia
    [35,15,47,35,54],#czech rep
    [34,19,69,34,67],#england
    [39,20,58,29,71],#france
    [39,26,103,54,85],#germany
    [36,20,88,33,69],#netherlands
    [34,12,36,41,43],#norway
    [36,20.68,41,66],#portugal
    [28,13,34,34,44],#scotland
    [45,36,119,35,113],#spain
    [43,26,90,56,83],#sweden
    [27,15,41,24,53],#switzerland
    [32,15,48,37,53],#turkey
    [44,24,91,49,85],#argentina
    [48,31,108,39,102],#brazil
    [33,20,51,20,66],#colombia
    [38,16,62,43,60],#ecuador
    [40,16,62,60,58],#paraguay
    [43,21,83,59,74]#uruguay
]

stats_df = pd.DataFrame(
    stats_data,
    columns=[
        "matches_played",
        "wins",
        "goals_scored",
        "goals_conceded",
        "points"
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

stats_df['points_per_game'] = (
    (stats_df['points']/stats_df['matches_played']).round(2)
)

df["win_percentage_since_last_cup"] = stats_df["win_percentage_since_last_cup"]

df["goals_scored_per_game"] = stats_df["goals_scored_per_game"]

df["goals_conceded_per_game"] = stats_df["goals_conceded_per_game"]

df['points_per_game'] = stats_df['points_per_game']

df.to_csv("world_cup_dataset.csv", index=False)
