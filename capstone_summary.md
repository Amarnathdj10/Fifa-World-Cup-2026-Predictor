# 🏆 Capstone Project Summary: FIFA World Cup 2026 Prediction Engine

An end-to-end machine learning and simulation pipeline built to forecast the outcome of the FIFA World Cup 2026 (48-team format) using historical tournament data (2014, 2018, 2022).

---

## 🎯 1. Core Objective
To predict the progress and ultimate champion of the 2026 FIFA World Cup by modeling team capability through regression learning and tournament volatility through Monte Carlo simulations.

---

## 🔬 2. Methodology & Key Findings

### Stage 1: Exploratory Data Analysis (EDA)
- **Primary Insight**: Elo rating remains the strongest predictor of team progression (correlation **0.68**).
- **Defense Over Attack**: Split-criteria importance indicates that keeping clean sheets (`goals_conceded_per_game` at **13.8%**) is **3x** as critical as scoring goals (`goals_scored_per_game` at **4.1%**).
- **Multicollinearity**: High VIF values (>50) for interaction terms (`elo_host_boost`, `attack_efficiency`) necessitated comparing linear and tree-based regression models.

### Stage 2: Machine Learning Modeling
We evaluated Ridge Regression, Random Forest, and XGBoost using **Leave-One-Group-Out Cross Validation** (by tournament year).
- **Selected Model**: **XGBoost Regressor**
- **Performance**: MAE of **0.6760**, RMSE of **1.0751**, and $R^2$ of **0.4504**. Average prediction of a team's exit stage is off by less than one round.
- **2026 Top Seed Capability**: XGBoost ranked **Colombia** (3.60), **France** (3.59), and **Uruguay** (3.47) as the highest-capability teams.

### Stage 3: Monte Carlo Simulation (10,000 Iterations)
A hybrid rating ($\text{Strength} = \text{Elo} + \text{Predicted\_Stage} \times 50$) was used in a Poisson match simulator. We ran simulations for both a randomized draw and the **Official 2026 Schedule & Bracket**:

#### Top 5 Favorites (Official Scheduled Bracket)
1. 🇪🇸 **Spain** — **32.6%** Win Probability (Favorable bracket path + peak Elo 2172)
2. 🇫🇷 **France** — **11.8%** Win Probability
3. 🇦🇷 **Argentina** — **11.8%** Win Probability
4. 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **England** — **9.6%** Win Probability
5. 🇨🇴 **Colombia** — **5.9%** Win Probability (Top South American dark horse)

---

## 📁 3. Directory File Map
- 📊 **[eda_report.md](file:///d:/Fifa-World-Cup-2026-Predictor/eda/eda_report.md)**: Feature importance analysis & visualization figures.
- 🤖 **[train.py](file:///d:/Fifa-World-Cup-2026-Predictor/models/train.py)**: Machine learning pipeline (Ridge vs. RF vs. XGBoost).
- 📁 **[finalmodel/](file:///d:/Fifa-World-Cup-2026-Predictor/finalmodel/)**: Model output metrics, confusion matrix plot, and 2026 stage predictions.
- 🎲 **[scheduled_bracket_simulation.py](file:///d:/Fifa-World-Cup-2026-Predictor/monte_carlo/scheduled_bracket_simulation.py)**: Official 2026 bracket Monte Carlo engine.
- 📝 **[report.md](file:///d:/Fifa-World-Cup-2026-Predictor/monte_carlo/report.md)**: In-depth final project documentation.
