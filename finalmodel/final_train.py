import pandas as pd
import numpy as np
import os
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error

# Setup paths
base_path = r"d:\Fifa-World-Cup-2026-Predictor"
csv_path = os.path.join(base_path, "world_cup_dataset.csv")
elo_path = os.path.join(base_path, "eloratings.csv")
final_dir = os.path.join(base_path, "finalmodel")

def final_training_and_prediction():
    print("🚀 Initializing Final World Cup 2026 Prediction Engine (Method 1)...")
    
    # 1. DATA LOADING & CLEANING
    df = pd.read_csv(csv_path).dropna(subset=['finish_stage'])
    
    # 2. FEATURE ENGINEERING
    # Adding best-performing interaction terms from research
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

    X = df[features]
    y = df['finish_stage']
    groups = df['year']

    # 3. MODEL CONFIGURATION (Optimized XGBoost)
    xgb = XGBRegressor(
        objective='reg:absoluteerror', 
        colsample_bytree=0.6, 
        learning_rate=0.05, 
        max_depth=3, 
        n_estimators=100, 
        reg_alpha=1, 
        reg_lambda=2, 
        subsample=0.8, 
        random_state=42,
        tree_method='hist'
    )

    # 4. CROSS-VALIDATION & PERFORMANCE METRICS
    print("Evaluating model performance across all tournaments...")
    logo = LeaveOneGroupOut()
    maes, r2s, rmses = [], [], []
    all_actuals, all_preds = [], []
    
    for train_idx, test_idx in logo.split(X, y, groups):
        xgb.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = xgb.predict(X.iloc[test_idx])
        
        maes.append(mean_absolute_error(y.iloc[test_idx], preds))
        r2s.append(r2_score(y.iloc[test_idx], preds))
        rmses.append(np.sqrt(mean_squared_error(y.iloc[test_idx], preds)))
        
        all_actuals.extend(y.iloc[test_idx].tolist())
        all_preds.extend(preds.tolist())
    
    # 4.1 Confusion Matrix Generation (Round predictions to nearest stage)
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
    import matplotlib.pyplot as plt

    # Round to nearest integer class (1-7)
    y_true_round = np.round(all_actuals).astype(int)
    y_pred_round = np.clip(np.round(all_preds), 1, 7).astype(int)

    cm = confusion_matrix(y_true_round, y_pred_round)
    plt.figure(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(np.unique(y_true_round)))
    disp.plot(cmap='Blues', values_format='d')
    plt.title("Confusion Matrix (Rounded Stages)")
    plt.savefig(os.path.join(final_dir, "confusion_matrix.png"))
    plt.close()

    # Metrics Summary
    metrics_summary = f"""--- FINAL MODEL METRICS (Method 1) ---
Mean Absolute Error (MAE): {np.mean(maes):.4f}
R-Squared (R2): {np.mean(r2s):.4f}
Root Mean Squared Error (RMSE): {np.mean(rmses):.4f}
Note: Confusion Matrix saved as confusion_matrix.png
"""
    print(metrics_summary)
    with open(os.path.join(final_dir, "metrics.txt"), "w") as f:
        f.write(metrics_summary)

    # 5. FINAL TRAINING
    print("Training final model on full historical dataset...")
    xgb.fit(X, y)

    # 6. 2026 PREDICTION DATA PREPARATION
    print("Generating 2026 World Cup predictions...")
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

    # Fetch Latest Elo
    elo_df = pd.read_csv(elo_path)
    elo_df["team"] = elo_df["team"].replace({"South Korea": "Korea Republic", "United States": "USA", "Côte d'Ivoire": "Ivory Coast", "Curaçao": "Curacao", "Czechia": "Czech Republic", "Democratic Republic of Congo": "Congo DR", "Cabo Verde": 'Cape Verde'})
    latest_elo = elo_df.sort_values('date').groupby('team')['elo_rating'].last().to_dict()
    predict_df['elo_rating'] = predict_df['team'].map(latest_elo).fillna(df['elo_rating'].mean())

    # Form Stats (Historical Proxy)
    df_2022 = df[df['year'] == 2022].set_index('team')
    for col in ['win_percentage_since_last_cup', 'goals_scored_per_game', 'goals_conceded_per_game', 'points_per_game', 'finish_stage']:
        predict_df[col] = predict_df['team'].map(df_2022[col].to_dict())
    
    predict_df = predict_df.rename(columns={'finish_stage': 'previous_wc_finish'})
    for col in ['win_percentage_since_last_cup', 'goals_scored_per_game', 'goals_conceded_per_game', 'points_per_game', 'previous_wc_finish']:
        predict_df[col] = predict_df[col].fillna(df[col].mean())

    predict_df['elo_host_boost'] = predict_df['elo_rating'] * (predict_df['host'] + 1)
    predict_df['attack_efficiency'] = predict_df['win_percentage_since_last_cup'] * predict_df['goals_scored_per_game']

    # 7. INFERENCE
    predict_df['predicted_finish_stage'] = xgb.predict(predict_df[features])
    
    # Save Final Results
    results = predict_df[['team', 'elo_rating', 'predicted_finish_stage']].sort_values('predicted_finish_stage', ascending=False)
    results.columns = ['Team', 'Elo_Rating', 'Predicted_Stage']
    results.to_csv(os.path.join(final_dir, "final_predictions_2026.csv"), index=False)
    
    # Feature Importance for analysis
    importances = pd.Series(xgb.feature_importances_, index=features).sort_values(ascending=False)
    importances.to_csv(os.path.join(final_dir, "feature_importance.csv"))

    print(f"✅ Success! Predictions and metrics saved to {final_dir}")

if __name__ == "__main__":
    final_training_and_prediction()
