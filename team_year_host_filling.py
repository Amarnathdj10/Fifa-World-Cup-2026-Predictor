import pandas as pd

uefa_teams = [
    "Austria", "Belgium", "Bosnia and Herzegovina", "Croatia",
    "Czech Republic", "England", "France", "Germany",
    "Netherlands", "Norway", "Portugal", "Scotland", "Spain",
    "Sweden", "Switzerland", "Turkey"
]

conmebol_teams = [
    "Argentina", "Brazil", "Colombia",
    "Ecuador", "Paraguay", "Uruguay"
]

caf_teams = [
    "Algeria", "Cabo Verde", "Congo DR",
    "Ivory Coast", "Egypt", "Ghana",
    "Morocco", "Senegal", "South Africa",
    "Tunisia"
]

concacaf_teams = [
    "Canada", "Mexico", "USA",
    "Curacao", "Haiti", "Panama"
]

afc_teams = [
    "Australia", "Iran", "Iraq",
    "Japan", "Jordan", "Korea Republic",
    "Qatar", "Saudi Arabia", "Uzbekistan"
]

ofc_teams = [
    "New Zealand"
]

confederation_map = {}

for team in uefa_teams:
    confederation_map[team] = "UEFA"

for team in conmebol_teams:
    confederation_map[team] = "CONMEBOL"

for team in caf_teams:
    confederation_map[team] = "CAF"

for team in concacaf_teams:
    confederation_map[team] = "CONCACAF"

for team in afc_teams:
    confederation_map[team] = "AFC"

for team in ofc_teams:
    confederation_map[team] = "OFC"

all_teams = list(confederation_map.keys())

years = [2014, 2018, 2022]

rows = []

for year in years:
    for team in all_teams:

        host = 0

        if year == 2014 and team == "Brazil":
            host = 1

        elif year == 2018 and team == "Russia":
            host = 1

        elif year == 2022 and team == "Qatar":
            host = 1

        rows.append({
            "team": team,
            "year": year,
            "host": host,
            "confederation": confederation_map[team],
            "elo_rating": None,
            "squad_form": None,
            "win_percentage_since_last_cup": None,
            "goals_scored_per_game": None,
            "goals_conceded_per_game": None,
            "wc_appearances": None,
            "previous_cup_finish": None,
            "previous_wc_finish": None,
            "finish_stage": None
        })

df = pd.DataFrame(rows)

df.to_csv("world_cup_dataset.csv", index=False)