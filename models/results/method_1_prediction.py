import pandas as pd
import numpy as np
import os
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import mean_absolute_error

# Setup paths
base_path = r"d:\Fifa-World-Cup-2026-Predictor"
csv_path = os.path.join(base_path, "world_cup_dataset.csv")
elo_path = os.path.join(base_path, "eloratings.csv")
results_dir = os.path.join(base_path, "models", "results")

def method_1_predict():
    df = pd.read_csv(csv_path).dropna(subset=['finish_stage'])
    
    # Feature Engineering
    df['elo_host_boost'] = df['elo_rating'] * (df['host'] + 1)
    df['attack_efficiency'] = df['win_percentage_since_last_cup'] * df['goals_scored_per_game']
    
    le = LabelEncoder()
    df['confederation_encoded'] = le.fit_transform(df['confederation'])
    confed_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

    features = [
        'elo_rating', 'win_percentage_since_last_cup', 'goals_scored_per_game', 
        'goals_conceded_per_game', 'points_per_game', 'previous_wc_finish', 
        'host', 'confederation_encoded', 'elo_host_boost', 'attack_efficiency'
    ]

    # METHOD 1: Train on ALL historical data (2014, 2018, 2022)
    # Using LOGO for MAE estimation
    X = df[features]
    y = df['finish_stage']
    groups = df['year']
    
    xgb = XGBRegressor(objective='reg:absoluteerror', colsample_bytree=0.6, learning_rate=0.05, max_depth=3, n_estimators=100, reg_alpha=1, reg_lambda=2, subsample=0.8, random_state=42)
    
    # Estimate MAE via CV
    logo = LeaveOneGroupOut()
    maes = []
    for train_idx, test_idx in logo.split(X, y, groups):
        xgb.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = xgb.predict(X.iloc[test_idx])
        maes.append(mean_absolute_error(y.iloc[test_idx], preds))
    
    avg_mae = np.mean(maes)
    
    # Train final model on ALL data
    xgb.fit(X, y)

    # Prepare 2026 Prediction Data
    teams_2026 = {
        'AFC': ['Australia', 'Iran', 'Iraq', 'Japan', 'Jordan', 'Korea Republic', 'Qatar', 'Saudi Arabia', 'Uzbekistan'],
        'CAF': ['Algeria', 'Cabo Verde', 'Congo DR', 'Ivory Coast', 'Egypt', 'Ghana', 'Morocco', 'Senegal', 'South Africa', 'Tunisia'],
        'CONCACAF': ['Canada', 'Mexico', 'USA', 'Curacao', 'Haiti', 'Panama'],
        'CONMEBOL': ['Argentina', 'Brazil', 'Colombia', 'Ecuador', 'Paraguay', 'Uruguay'],
        'OFC': ['New Zealand'],
        'UEFA': ['Austria', 'Belgium', 'Bosnia and Herzegovina', 'Croatia', 'Czech Republic', 'England', 'France', 'Germany', 'Netherlands', 'Norway', 'Portugal', 'Scotland', 'Spain', 'Sweden', 'Switzerland', 'Turkey']
    }

    team_list = []
    for conf, teams in teams_2026.items():
        for team in teams:
            team_list.append({'team': team, 'confederation': conf})
    
    predict_df = pd.DataFrame(team_list)
    predict_df['year'] = 2026
    predict_df['host'] = predict_df['team'].apply(lambda x: 1 if x in ['USA', 'Mexico', 'Canada'] else 0)
    predict_df['confederation_encoded'] = predict_df['confederation'].map(confed_mapping)

    elo_df = pd.read_csv(elo_path)
    elo_df["team"] = elo_df["team"].replace({"South Korea": "Korea Republic", "United States": "USA", "Côte d'Ivoire": "Ivory Coast", "Curaçao": "Curacao", "Czechia": "Czech Republic", "Democratic Republic of Congo": "Congo DR", "Cabo Verde": 'Cape Verde'})
    latest_elo = elo_df.sort_values('date').groupby('team')['elo_rating'].last().to_dict()
    predict_df['elo_rating'] = predict_df['team'].map(latest_elo)
    predict_df['elo_rating'] = predict_df['elo_rating'].fillna(df['elo_rating'].mean())

    df_2022 = df[df['year'] == 2022].set_index('team')
    for col in ['win_percentage_since_last_cup', 'goals_scored_per_game', 'goals_conceded_per_game', 'points_per_game', 'finish_stage']:
        predict_df[col] = predict_df['team'].map(df_2022[col].to_dict())
    
    predict_df = predict_df.rename(columns={'finish_stage': 'previous_wc_finish'})
    for col in ['win_percentage_since_last_cup', 'goals_scored_per_game', 'goals_conceded_per_game', 'points_per_game', 'previous_wc_finish']:
        predict_df[col] = predict_df[col].fillna(df[col].mean())

    predict_df['elo_host_boost'] = predict_df['elo_rating'] * (predict_df['host'] + 1)
    predict_df['attack_efficiency'] = predict_df['win_percentage_since_last_cup'] * predict_df['goals_scored_per_game']

    predict_df['predicted_finish_stage'] = xgb.predict(predict_df[features])
    
    # Save Results
    results = predict_df[['team', 'predicted_finish_stage']].sort_values('predicted_finish_stage', ascending=False)
    results.to_csv(os.path.join(results_dir, "method_1_predictions.csv"), index=False)
    
    with open(os.path.join(results_dir, "method_1_mae.txt"), "w") as f:
        f.write(str(avg_mae))
    
    print(f"Method 1 Prediction completed. MAE: {avg_mae:.4f}")

if __name__ == "__main__":
    method_1_predict()
