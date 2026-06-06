import pandas as pd

teams = [
    "Austria",
    "Belgium",
    "Bosnia and Herzegovina",
    "Croatia",
    "Czech Republic",
    "England",
    "France",
    "Germany",
    "Netherlands",
    "Norway",
    "Portugal",
    "Scotland",
    "Spain",
    "Sweden",
    "Switzerland",
    "Turkey",
    "Argentina",
    "Brazil",
    "Colombia",
    "Ecuador",
    "Paraguay",
    "Uruguay",
    "Algeria",
    "Cabo Verde",
    "Congo DR",
    "Ivory Coast",
    "Egypt",
    "Ghana",
    "Morocco",
    "Senegal",
    "South Africa",
    "Tunisia",
    "Canada",
    "Mexico",
    "USA",
    "Curacao",
    "Haiti",
    "Panama",
    "Australia",
    "Iran",
    "Iraq",
    "Japan",
    "Jordan",
    "Korea Republic",
    "Qatar",
    "Saudi Arabia",
    "Uzbekistan",
    "New Zealand"
]

rows = []

years = [2014, 2018, 2022]

for year in years:
    for team in teams:
       rows.append([team,year])

df = pd.DataFrame(rows,columns=['team','year'])

df.to_csv('teams.csv',index=False)