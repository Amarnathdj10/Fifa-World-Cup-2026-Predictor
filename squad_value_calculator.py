import pandas as pd

wc_df = pd.read_csv("world_cup_dataset.csv")

squad_values = [
    # gk, defense, midfield, attack

    [3.70,44.80,16.70,30.33],   # Austria 2014
    [24.50,101.20,108.75,98.90],  # Belgium 2014
    [4.1,14.15,44.2,40.45],#bosnia 2014
    [6.05,54.50,82.55,56.60],#croatia 2014
    [31,40.35,35.6,17],#czech 2014
    [37.25,193,138,160.5],#england 2014
    [45.5,174,142,160],#france 2014
    [59,133.5,235.5,150.5],#germany 2014
    [33.5,55.95,118.55,135],#netherlands 2014
    [],#norway 2014
    [],#portugal 2014
    [],#scotland 2014
    [],#spain 2014
    [],#sweden 2014
    [],#switzerland 2014
    [],#turkey 2014
    [3.98,91.35,46.45,22.10],#austria 2018
    [56.5,106.75,186,255.5],#belgium
    [11.5,22.55,65.95,34.65],#bosnia 2018
    [10.25,67.75,195.05,83.80],#croatia 2018
    [7,26.8,31.73,11.3],#czech 2018
    [43.25,232,152.8,176.5],#england 2018
    [51.5,216.5,270,255],#france 2018
    [44,209.5,275.75,193.5],#germany 2018
    [30.5,108.85,100,126.5],#netherlands 2018
    [],#norway 2018
    [],#portugal 2018
    [],#scotland 2018
    [],#spain 2018
    [],#sweden 2018
    [],#switzerland 2018
    [],#turkey 2018
    [7,167.6,123.1,61.4],#austria 2022
    [1.98,25.48,81.38,19.1],#bosnia 2022
    [24.9,99.7,207,97.5],#croatia 2022
    [14.6,43.85,99.4,86.8],#czech 2022
    [80.5,483,289.7,630],#england 2022
    [51,545,338.5,551],#france 2022
    [],#germany 2022
    [31.05,325.7,237,197.5],#netherlands 2022
    [],#norway 2022
    [],#portugal 2022
    [],#scotland 2022
    [],#spain 2022
    [],#sweden 2022
    [],#switzerland 2022
    [],#turkey 2022
]

stats_df = pd.DataFrame(
    squad_values,
    columns=[
        "goalkeeper_value",
        "defense_value",
        "midfield_value",
        "attack_value"
    ]
)

stats_df["squad_value"] = (
    stats_df["goalkeeper_value"]
    + stats_df["defense_value"]
    + stats_df["midfield_value"]
    + stats_df["attack_value"]
)

wc_df["goalkeeper_value"] = stats_df["goalkeeper_value"]
wc_df["defense_value"] = stats_df["defense_value"]
wc_df["midfield_value"] = stats_df["midfield_value"]
wc_df["attack_value"] = stats_df["attack_value"]
wc_df["squad_value"] = stats_df["squad_value"]

wc_df.to_csv("world_cup_dataset.csv", index=False)