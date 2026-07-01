# 🏆 2026 FIFA World Cup: Predictive Modelling and Monte Carlo Simulation Report

This report presents the complete end-to-end methodology and results for predicting the 2026 FIFA World Cup. It covers the **Exploratory Data Analysis (EDA)**, the **Machine Learning Training and Refinement** process, and the final **Monte Carlo Simulations** using both random group setups and the official 2026 scheduled brackets.

---

## 📅 1. Project Overview & Objective
The objective of this project is to model and forecast the performance of all 48 qualified teams in the 2026 FIFA World Cup using historical tournament records (2014, 2018, and 2022). 

Our forecasting engine uses:
1. A **Machine Learning Model** to estimate the base capability (`Predicted_Stage`) of each team based on recent form, Elo rating, defensive metrics, and historical finishes.
2. A **Monte Carlo Simulation Engine** (10,000 iterations) that uses a hybrid strength index to simulate matches, calculate tie-breakers, resolve groups, and play out the knockout brackets to obtain robust tournament outcomes.

---

## 📊 2. Exploratory Data Analysis (EDA) Stage
We conducted a professional EDA on the historical dataset to understand feature dependencies and prevent model instability.

### A. Key Insights & Feature Correlations
- **Elo is King**: `elo_rating` exhibits the strongest direct correlation (**0.68**) with tournament success, followed by the team's finish in the previous World Cup cycle (**0.51**).
- **Defense Over Attack**: A team's defensive metric (`goals_conceded_per_game`) is more than **3x** as critical in predicting progress compared to their offensive metric (`goals_scored_per_game`) in tree splits (13.8% vs. 4.1%).
- **Confederation Strength**: Teams from **UEFA** and **CONMEBOL** show a statistically higher average finish stage than other confederations, reflecting their historical dominance.

### B. Multicollinearity (VIF) and Mutual Information
- **High Multicollinearity**: Calculating the Variance Inflation Factor (VIF) revealed extreme multicollinearity among engineered variables:
  - `elo_host_boost`: **123.99** VIF
  - `attack_efficiency`: **63.82** VIF
  - `elo_rating`: **51.91** VIF
- **Implication**: Simple linear models (like Ordinary Least Squares) will suffer from highly unstable coefficients. Regularized linear models (Ridge) or tree-based algorithms (Random Forest, XGBoost) must be used.
- **Mutual Information (MI)**: The features sharing the most raw information with the target variable `finish_stage` are `elo_host_boost` (**0.375**) and `elo_rating` (**0.375**).

*All visualizations (heatmaps, boxplots, and scatter charts) are saved in the [eda/](file:///d:/Fifa-World-Cup-2026-Predictor/eda/) directory.*

---

## 🤖 3. Machine Learning Training & Refinement Stage
We built a model evaluation pipeline using **Leave-One-Group-Out (LOGO) Cross-Validation** (grouping by `year`). This simulates training on past tournaments (e.g., 2014, 2018) and testing on an unseen tournament (e.g., 2022) to prevent overfitting.

### A. Model Performance Comparison
We compared three regressors: Ridge Regression (L2 regularized linear model), Random Forest, and XGBoost.

| Model | Cross-Validation MAE ↓ | Cross-Validation RMSE | Cross-Validation $R^2$ | Status |
| :--- | :---: | :---: | :---: | :--- |
| **XGBoost Regressor** | **0.6760** | **1.0751** | **0.4504** | 🥇 **Best Model (Selected)** |
| **Random Forest** | 0.6856 | 1.0936 | 0.4275 | 🥈 Strong Competitor |
| **Ridge Regression** | 0.7864 | 1.0836 | 0.4393 | 🥉 Decent Baseline |

### B. Final Model Architecture (XGBoost)
We trained the final XGBoost model on all historical data. The top features driving the splits are:
1. `attack_efficiency`: **19.3%**
2. `elo_host_boost`: **17.4%**
3. `points_per_game`: **15.4%**
4. `elo_rating`: **10.6%**

### C. 2026 Finish Stage Predictions (Top 10 Teams)
Using the fully populated `prediction_dataset.csv`, the model predicted the base "Finish Stage" value (on a scale of 1 to 7) for all 48 teams:

| Team | Elo Rating | Predicted Finish Stage (Out of 7) |
| :--- | :---: | :---: |
| **Colombia** | 1998 | **3.60** (Quarter-Final capability) |
| **France** | 2062 | **3.59** (Quarter-Final capability) |
| **Uruguay** | 1890 | **3.47** (R16-QF capability) |
| **England** | 2042 | **3.46** (R16-QF capability) |
| **Belgium** | 1850 | **3.29** |
| **Ecuador** | 1933 | **3.24** |
| **Netherlands** | 1959 | **3.16** |
| **Austria** | 1818 | **3.04** |
| **Croatia** | 1933 | **3.00** |
| **Senegal** | 1807 | **2.97** |

---

## 🎲 4. Monte Carlo Simulation Stage (10,000 Iterations)
To translate the static ML predictions into tournament probabilities, we ran two simulation setups.

### A. Hybrid Strength Index
Instead of relying solely on Elo ratings or static ML predictions, we created a **Hybrid Strength Metric** for each team:
$$\text{Strength} = \text{Elo\_Rating} + \text{Predicted\_Stage} \times 50$$
This integrates historical Elo capability with recent form, goal stats, and tournament pedigree. Matches are simulated using a Poisson Process with expected goals adjusted by this strength difference.

### B. Method 1: Random-Seeded Groups
In this baseline simulation, groups are randomized using standard snake seeding based on Strength pots:

| Rank | Team | Win Probability % | Reach Final % | Reach Semi-Final % |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Spain** | **25.1%** | 36.3% | 49.4% |
| 2 | **Argentina** | **14.4%** | 24.3% | 38.3% |
| 3 | **France** | **13.8%** | 23.8% | 38.0% |
| 4 | **England** | **11.1%** | 20.2% | 33.7% |
| 5 | **Colombia** | **8.0%** | 15.5% | 27.6% |
| 6 | **Portugal** | **4.2%** | 9.3% | 19.2% |
| 7 | **Netherlands** | **3.9%** | 8.9% | 18.9% |
| 8 | **Ecuador** | **2.7%** | 7.3% | 16.7% |
| 9 | **Brazil** | **2.6%** | 7.2% | 16.7% |
| 10 | **Croatia** | **2.6%** | 6.7% | 15.4% |

### C. Method 2: Scheduled Official Bracket
This simulation uses the actual, official group stage drawings and bracket mechanics for the 2026 World Cup:

| Rank | Team | Win Probability % (Scheduled) | Reach Final % | Reach Semi-Final % |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Spain** | **32.6%** | 48.2% | 61.4% |
| 2 | **France** | **11.8%** | 20.9% | 34.7% |
| 3 | **Argentina** | **11.8%** | 20.3% | 32.8% |
| 4 | **England** | **9.6%** | 16.9% | 28.3% |
| 5 | **Colombia** | **5.9%** | 12.0% | 23.0% |
| 6 | **Netherlands** | **4.2%** | 9.8% | 18.0% |
| 7 | **Ecuador** | **3.3%** | 8.2% | 16.3% |
| 8 | **Portugal** | **3.2%** | 6.8% | 15.8% |
| 9 | **Brazil** | **3.0%** | 8.6% | 21.5% |
| 10 | **Uruguay** | **2.7%** | 7.9% | 17.6% |

---

## 🏆 5. Key Takeaways
1. **Spain emerges as the heavy favorite**: Spain possesses the highest Elo rating in the qualified dataset (**2172**) and is predicted with an exceptionally strong hybrid index, granting them a dominant win probability of **32.6%** in the official bracket.
2. **Official Brackets Shift the Odds**: In the scheduled bracket, Spain's win probability increases significantly (from 25.1% to 32.6%) due to favorable group dynamics and path matching, whereas Argentina's odds decrease slightly (from 14.4% to 11.8%) because of their specific scheduled opponents and knockout paths.
3. **South American Dark Horses**: Colombia and Ecuador show solid win probabilities (5.9% and 3.3% respectively) due to excellent points-per-game and win rates since 2022, placing them ahead of traditionally favored teams like Brazil or Portugal.

---

## 📁 6. Directory File Structure
- `world_cup_dataset.csv`: Cleaned historical dataset.
- `prediction_dataset.csv`: Cleaned dataset for 2026 teams.
- `eda/`:
  - `eda_visualization.py`: Main EDA execution script.
  - `eda_report.md`: Detailed analysis, multicollinearity, and plots.
- `models/`:
  - `train.py`: Model cross-validation and 2026 prediction generator.
- `finalmodel/`:
  - `final_predictions_2026.csv`: Predicted finish stages.
  - `confusion_matrix.png`, `feature_importance.csv`, `metrics.txt`: Validation outputs.
- `monte_carlo/`:
  - `monte_carlo_simulation.py`: Randomized-group simulation script.
  - `scheduled_bracket_simulation.py`: Official-group scheduled simulation script.
  - `monte_carlo_results_2026.csv`, `scheduled_results_2026.csv`: Simulation outputs.
  - `report.md`: This comprehensive report.
