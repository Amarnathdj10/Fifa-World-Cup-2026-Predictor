# 📊 Advanced EDA Metrics Report

## Multicollinearity (VIF)
Features with VIF > 5.0 (or especially > 10.0) indicate strong multicollinearity.
| Feature | VIF |
| --- | --- |
| elo_host_boost | 123.9936071240124 |
| host | 64.6015915297705 |
| attack_efficiency | 63.82526484794819 |
| elo_rating | 51.91144020711605 |
| goals_scored_per_game | 29.559545564466585 |
| win_percentage_since_last_cup | 23.415885590381617 |
| points_per_game | 9.770399429617033 |
| goals_conceded_per_game | 2.434231926362318 |
| previous_wc_finish | 1.9436558831250608 |
| confederation_encoded | 1.772329512328487 |


## Mutual Information (MI)
MI measures how much information a feature shares with the target variable `finish_stage` (higher means more predictive dependency).
| Feature | MI_Score |
| --- | --- |
| elo_host_boost | 0.37534147239943616 |
| elo_rating | 0.37523017498766054 |
| attack_efficiency | 0.3407162966410544 |
| points_per_game | 0.24100286357010026 |
| win_percentage_since_last_cup | 0.20881686405789335 |
| previous_wc_finish | 0.1991474934256141 |
| goals_scored_per_game | 0.19168312748689198 |
| goals_conceded_per_game | 0.14632218184573365 |
| confederation_encoded | 0.0825467524101704 |
| host | 0.0010088490093904667 |


## Random Forest Feature Importance
Feature importance derived from split criteria in a Random Forest regressor.
| Feature | Importance |
| --- | --- |
| elo_rating | 0.4320870501484071 |
| elo_host_boost | 0.15756474698852585 |
| goals_conceded_per_game | 0.13805752515017386 |
| points_per_game | 0.07972082913510162 |
| attack_efficiency | 0.06754818652148478 |
| goals_scored_per_game | 0.04091537717401658 |
| win_percentage_since_last_cup | 0.03666440105308199 |
| previous_wc_finish | 0.0319065563822671 |
| confederation_encoded | 0.014787168363040133 |
| host | 0.0007481590839008305 |

