# ⚽ FIFA World Cup 2026 Prediction Engine

> End-to-end ML + simulation pipeline to forecast the FIFA World Cup 2026 — featuring XGBoost team capability modelling, Poisson match simulation, and 10,000-run Monte Carlo tournament prediction.

🔴 **[Live Demo](https://fifa-world-cup-2026-predictor-nu.vercel.app)**

---

## 📌 Overview

The 2026 FIFA World Cup introduced an expanded 48-team format, making traditional prediction methods less reliable. This project builds a two-stage prediction engine:

1. **ML Stage** — XGBoost regressor trained on historical World Cup data (2014–2022) predicts how far each of the 48 teams will progress.
2. **Simulation Stage** — A Poisson-based match simulator runs 10,000 Monte Carlo iterations of the official bracket to estimate win probabilities for every team.

The result: data-driven tournament winner probabilities grounded in historical performance, Elo ratings, and squad statistics.

---

## 🏆 Predictions — Official 2026 Bracket

| Rank | Team | Win Probability | Notes |
|------|------|----------------|-------|
| 🥇 1 | 🇪🇸 Spain | **32.6%** | Favorable bracket path + peak Elo 2172 |
| 🥈 2 | 🇫🇷 France | 11.8% | Highest ML-predicted capability (3.59) |
| 🥉 3 | 🇦🇷 Argentina | 11.8% | Defending champions |
| 4 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 England | 9.6% | |
| 5 | 🇨🇴 Colombia | 5.9% | Top South American dark horse |

> Simulated across 10,000 iterations using the official group draw and knockout bracket.

---

## 🧠 Methodology

```
Historical WC Data (2014, 2018, 2022)
            ↓
   Feature Engineering + EDA
            ↓
  XGBoost Stage Predictor (ML)
            ↓
  Hybrid Strength Score
  (Elo + Predicted_Stage × 50)
            ↓
  Poisson Match Simulator
            ↓
  Monte Carlo (10,000 runs)
            ↓
  Win Probability per Team
```

### Stage 1 — EDA & Key Findings

- **Elo rating** is the strongest predictor of tournament progression, with a correlation of **0.68**
- **Defence > Attack**: `goals_conceded_per_game` accounts for **13.8%** of split importance vs only **4.1%** for `goals_scored_per_game` — keeping clean sheets matters 3× more than scoring
- High multicollinearity (VIF > 50) in interaction terms necessitated comparing linear vs tree-based models

### Stage 2 — Machine Learning

Three models evaluated using **Leave-One-Group-Out Cross Validation** (held out by tournament year — 2014, 2018, 2022 in rotation):

| Model | MAE | RMSE | R² |
|-------|-----|------|-----|
| Ridge Regression | — | — | — |
| Random Forest | — | — | — |
| **XGBoost** ✅ | **0.676** | **1.075** | **0.450** |

**XGBoost selected** — average error of less than one round in predicting exit stage.

Top ML-ranked teams by predicted capability:
- 🇨🇴 Colombia: 3.60
- 🇫🇷 France: 3.59
- 🇺🇾 Uruguay: 3.47

### Stage 3 — Monte Carlo Simulation

Each match is simulated using a **Poisson goal model**:
- Expected goals drawn from Poisson distribution parameterised by team strength
- Team strength = hybrid score combining Elo rating and ML-predicted stage
- 10,000 full tournament simulations run for both a randomised draw and the official 2026 bracket
- Win probability = fraction of simulations where a team lifts the trophy

---

## 🗂️ Repository Structure

```
Fifa-World-Cup-2026-Predictor/
│
├── eda/                            # EDA notebooks and feature importance analysis
├── models/                         # Model training scripts (Ridge, RF, XGBoost)
├── finalmodel/                     # Final model outputs, metrics, stage predictions
├── monte_carlo/                    # Poisson simulator + Monte Carlo engine
├── webapp/                         # Frontend web application (deployed on Vercel)
│
├── world_cup_dataset.csv           # Historical WC data (2014–2022)
├── prediction_dataset.csv          # Feature-engineered 2026 team dataset
├── eloratings.csv                  # Elo ratings for all 48 qualified teams
├── teams.csv                       # Team metadata
├── capstone_summary.md             # Full methodology and findings report
└── render.yaml                     # Deployment config
```

---

## ⚙️ Setup & Usage

### 1. Clone the repo

```bash
git clone https://github.com/Amarnathdj10/Fifa-World-Cup-2026-Predictor.git
cd Fifa-World-Cup-2026-Predictor
```

### 2. Install dependencies

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn scipy
```

### 3. Run the ML model

```bash
cd models
python train.py
```

### 4. Run the Monte Carlo simulation

```bash
cd monte_carlo
python scheduled_bracket_simulation.py
```

---

## 📊 Features Used

| Feature | Description |
|---------|-------------|
| `elo_rating` | Team's Elo score at tournament start |
| `goals_scored_per_game` | Historical average goals scored per WC game |
| `goals_conceded_per_game` | Historical average goals conceded per WC game |
| `win_rate` | Historical WC win percentage |
| `squad_value` | Transfer market valuation of squad (in €M) |
| `attack_efficiency` | Goals scored per shot on target |
| `elo_host_boost` | Elo adjustment for host nations (USA, Canada, Mexico) |

---

## 🔭 Future Work

- [ ] Incorporate real-time squad injury/availability data
- [ ] Add player-level ratings (FIFA/Sofascore) as additional features
- [ ] Bayesian updating of probabilities as group stage results come in
- [ ] Live dashboard updating predictions round-by-round

---

## 👤 Author

**Mekha S.R.**
B.Tech CSE (AI & ML), SCTCE Thiruvananthapuram  
[LinkedIn](https://linkedin.com/in/mekha-s-r-1930783b1)
[GitHub](https://github.com/mekha06)

**Amarnath D.J.**  
B.Tech CSE (AI & ML), SCTCE Thiruvananthapuram  
[Portfolio](https://amarnath-dj.me) · [LinkedIn](https://linkedin.com/in/amarnath-dj-b710abc) · [GitHub](https://github.com/Amarnathdj10)