# FIFA World Cup 2026 Predictor

A FIFA World Cup 2026 prediction project combining machine learning and Monte Carlo simulation to estimate tournament outcomes for the 48-team tournament.

## Project Summary

This repository uses historical World Cup team data, feature engineering, and regression modeling to predict team strength. It then simulates tournament progress through group and knockout stages to produce championship probability estimates.

## Key Components

- `world_cup_dataset.csv` — historical World Cup dataset used for training.
- `prediction_dataset.csv` — feature dataset for 2026 qualified teams.
- `models/train.py` — machine learning pipeline that trains models, evaluates them using Leave-One-Group-Out CV, and produces 2026 team predictions.
- `finalmodel/` — generated model outputs including metrics, feature importances, confusion matrix, and final 2026 predictions.
- `monte_carlo/scheduled_bracket_simulation.py` — Monte Carlo simulation engine for the official 2026 bracket.
- `monte_carlo/scheduled_results_2026.csv` — sample simulation results for scheduled bracket runs.
- `webapp/backend/` — Flask API backend for serving team, group, results, bracket, and simulation endpoints.
- `webapp/frontend/` — Vite frontend for displaying predictions and bracket visualization.
- `eda/` — exploratory data analysis, reports, visualizations, and feature summaries.

## Features

- Historical World Cup team modeling
- Feature engineering with Elo, goals, win percentage, and confederation
- Model comparison across Ridge, Random Forest, and XGBoost
- Monte Carlo simulation of World Cup bracket outcomes
- REST API backend for simulation and results
- Frontend UI for visualizing predictions and knockouts

## Installation

### Prerequisites

- Python 3.11+ or equivalent environment
- Node.js 18+ (for frontend)

### Python backend

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\webapp\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Frontend

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\webapp\frontend"
npm install
```

## Usage

### Run model training and prediction

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\models"
python train.py
```

This will:

- evaluate models with Leave-One-Group-Out CV
- save comparison metrics to `finalmodel/model_comparison.csv`
- generate `finalmodel/final_predictions_2026.csv`
- save a confusion matrix and feature importances if available

### Run scheduled Monte Carlo simulation

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\monte_carlo"
python scheduled_bracket_simulation.py
```

This writes results to `monte_carlo/scheduled_results_2026.csv`.

### Run the Flask API

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\webapp\backend"
python app.py
```

API endpoints include:

- `GET /api/status`
- `GET /api/teams`
- `GET /api/groups`
- `GET /api/results/random`
- `GET /api/results/scheduled`
- `GET /api/bracket/<mode>`
- `POST /api/simulate`
- `GET /api/simulate/status/<job_id>`

### Run the frontend

```powershell
cd "d:\Coding journey\Fifa World Cup 2026 Predictor\webapp\frontend"
npm run dev
```

Then open the local Vite URL shown in the terminal.

## Data Notes

- `world_cup_dataset.csv` contains historical team features and finish stages.
- `prediction_dataset.csv` contains the 2026 qualified team features used for prediction.
- `finalmodel/final_predictions_2026.csv` contains predicted finish stages for teams in 2026.

## Project Structure

```text
.
├── capstone_summary.md
├── eda/
├── finalmodel/
├── models/
├── monte_carlo/
├── webapp/
│   ├── backend/
│   └── frontend/
├── world_cup_dataset.csv
├── prediction_dataset.csv
└── README.md
```

## Notes

- Squad form data is not currently used in the published pipeline.
- The project uses Elo rating as a strong predictive feature.
- Knockout stage ties are resolved by probabilistic penalty-style decisions in the simulation engine.

## License

This repository is provided as a project demo and currently has no formal open-source license applied.
