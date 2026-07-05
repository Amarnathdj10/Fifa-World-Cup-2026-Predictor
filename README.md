# FIFA World Cup 2026 Predictor

<<<<<<< HEAD
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
=======
Live demo: https://fifa-world-cup-2026-predictor-nu.vercel.app

A data-driven web application that predicts FIFA World Cup 2026 match outcomes and tournament progression using machine learning. This project combines Python data processing and modeling with a modern web frontend to let users explore predictions and match simulations.

## Features

- Predict match outcomes and scores
- Tournament simulation and bracket projection
- Interactive web UI for match-by-match exploration
- Model training and evaluation scripts

## Tech stack

- Python — data processing, modeling, backend logic
- JavaScript — frontend interactivity
- HTML/CSS — UI and layout

## Repository structure (high level)

- /api or /backend: Python scripts for data processing, model training, and API endpoints
- /web or /frontend: HTML/CSS/JavaScript for the client interface
- /data: (optional) datasets, preprocessing scripts
- /notebooks: exploratory analysis and model experiments

(Actual file and folder names may vary — explore the repo to confirm exact paths.)

## Getting started

Prerequisites:
- Python 3.8+
- Node.js 14+ (if running frontend dev server)
- pip or poetry for dependency management

Quick start (local):

1. Clone the repo
   git clone https://github.com/Amarnathdj10/Fifa-World-Cup-2026-Predictor.git
2. Install Python dependencies
   python -m pip install -r requirements.txt
3. Prepare data
   - Place raw datasets in the `data/` directory or follow the data ingestion scripts in `scripts/`
4. Train or load a pre-trained model
   - See `backend/train.py` (or similar) for training instructions
5. Run the backend API
   python backend/app.py
6. Serve the frontend
   - If frontend is static, open `web/index.html` in a browser
   - If there's a dev server: cd web && npm install && npm run dev

## Usage

- Use the web UI to run single-match predictions, view team probabilities, and simulate the tournament.
- For programmatic access, call the backend endpoints (e.g., `/predict`) with JSON payloads (see API docs or example requests).

## Model and data notes

- Models are implemented in Python (scikit-learn / XGBoost / TensorFlow — see requirements). Hyperparameters, evaluation metrics, and training scripts are in the `notebooks/` or `backend/` directories.
- Data sources may include historical World Cup match results, FIFA rankings, Elo ratings, and recent match statistics. Cite sources in `data/README.md` if available.

## Development

- Run tests (if present): python -m pytest
- Linting and formatting: flake8, black or equivalent tools

## Deployment

A deployed demo is available at the project homepage above. To deploy:
- Backend: containerize with Docker and push to your cloud provider
- Frontend: build static assets and host on Vercel/Netlify/GitHub Pages

## Contributing

Contributions are welcome. Please open issues for feature requests or bugs, and submit pull requests for changes.

## License

No license specified. If you want to make this project open source, consider adding an OSI-approved license (e.g., MIT, Apache-2.0).

## Contact

Maintainer: @Amarnathdj10

---

Thank you for checking out the FIFA World Cup 2026 Predictor — good luck and may your predictions be accurate!
>>>>>>> 2b60db6f38b7c04f4dd16d1be4654391f893cd02
