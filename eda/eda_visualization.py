import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# Setup paths
base_path = r"d:\Fifa-World-Cup-2026-Predictor"
csv_path = os.path.join(base_path, "world_cup_dataset.csv")
eda_dir = os.path.join(base_path, "eda")
os.makedirs(eda_dir, exist_ok=True)

def df_to_markdown(df):
    """
    Converts a pandas DataFrame to a GitHub markdown table without external dependencies.
    """
    headers = list(df.columns)
    markdown = "| " + " | ".join(headers) + " |\n"
    markdown += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for _, row in df.iterrows():
        # Clean values to avoid markdown formatting breakage
        vals = [str(val).replace("|", "\\|") for val in row]
        markdown += "| " + " | ".join(vals) + " |\n"
    return markdown

def calculate_vif(X):
    """
    Computes Variance Inflation Factor (VIF) manually using LinearRegression
    to avoid statsmodels dependency issues.
    """
    vif_dict = {}
    for col in X.columns:
        X_other = X.drop(columns=[col])
        y_col = X[col]
        # Fit regression of one feature against all others
        lr = LinearRegression()
        lr.fit(X_other, y_col)
        r2 = lr.score(X_other, y_col)
        # Avoid division by zero
        vif = 1.0 / (1.0 - r2) if r2 < 1.0 else float('inf')
        vif_dict[col] = vif
    return pd.Series(vif_dict)

def run_eda():
    print("=== Executing Professional Exploratory Data Analysis (EDA) ===")
    
    # Load dataset
    df = pd.read_csv(csv_path).dropna(subset=['finish_stage'])
    
    # Feature engineering for EDA
    df['elo_host_boost'] = df['elo_rating'] * (df['host'] + 1)
    df['attack_efficiency'] = df['win_percentage_since_last_cup'] * df['goals_scored_per_game']
    
    # Encode confederation
    le = LabelEncoder()
    df['confederation_encoded'] = le.fit_transform(df['confederation'])
    
    features = [
        'elo_rating', 'win_percentage_since_last_cup', 'goals_scored_per_game', 
        'goals_conceded_per_game', 'points_per_game', 'previous_wc_finish', 
        'host', 'confederation_encoded', 'elo_host_boost', 'attack_efficiency'
    ]
    
    X = df[features]
    y = df['finish_stage']
    
    # 1. CORRELATION ANALYSIS
    print("Calculating correlations...")
    plt.figure(figsize=(12, 10))
    corr_df = df[features + ['finish_stage']].corr()
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Feature Correlation Matrix (including Target)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, "correlation_heatmap.png"), dpi=150)
    plt.close()
    
    # 2. MULTICOLLINEARITY (VIF) CHECK
    print("Calculating Variance Inflation Factors (VIF)...")
    vifs = calculate_vif(X)
    vif_df = pd.DataFrame({'Feature': vifs.index, 'VIF': vifs.values}).sort_values('VIF', ascending=False)
    vif_df.to_csv(os.path.join(eda_dir, "vif_metrics.csv"), index=False)
    print(vif_df.to_string(index=False))
    
    # 3. MUTUAL INFORMATION
    print("Computing Mutual Information Regression scores...")
    mi_scores = mutual_info_regression(X, y, random_state=42)
    mi_df = pd.DataFrame({'Feature': features, 'MI_Score': mi_scores}).sort_values('MI_Score', ascending=False)
    mi_df.to_csv(os.path.join(eda_dir, "mutual_information.csv"), index=False)
    
    # 4. RANDOM FOREST FEATURE IMPORTANCE
    print("Running Random Forest for feature importance ranking...")
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    rf_importances = pd.DataFrame({'Feature': features, 'Importance': rf.feature_importances_}).sort_values('Importance', ascending=False)
    rf_importances.to_csv(os.path.join(eda_dir, "rf_importances.csv"), index=False)
    
    # 5. VISUAL RELATIONSHIPS
    print("Generating EDA visualizations...")
    
    # Relationship: Elo Rating Boxplot by Finish Stage
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='finish_stage', y='elo_rating', hue='finish_stage', legend=False, palette='viridis')
    plt.title("Distribution of Elo Rating by World Cup Finish Stage", fontsize=12, fontweight='bold')
    plt.xlabel("Finish Stage (1: Group Exit, 7: Winner)")
    plt.ylabel("Elo Rating")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, "elo_by_stage_boxplot.png"), dpi=150)
    plt.close()
    
    # Relationship: Attack Efficiency vs Goals Conceded colored by Stage
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(
        df['attack_efficiency'], 
        df['goals_conceded_per_game'], 
        c=df['finish_stage'], 
        cmap='viridis', 
        edgecolor='k', 
        s=df['elo_rating']/15,  # size by Elo
        alpha=0.8
    )
    plt.colorbar(scatter, label='Finish Stage')
    plt.title("Attack Efficiency vs. Goals Conceded (Size by Elo Rating)", fontsize=12, fontweight='bold')
    plt.xlabel("Attack Efficiency (Win % * Goals Scored)")
    plt.ylabel("Goals Conceded per Game")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, "efficiency_vs_defense_scatter.png"), dpi=150)
    plt.close()
    
    # Relationship: Confederation Performance
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='confederation', y='finish_stage', estimator=np.mean, errorbar=None, hue='confederation', legend=False, palette='muted')
    plt.title("Average Finish Stage by Confederation", fontsize=12, fontweight='bold')
    plt.xlabel("Confederation")
    plt.ylabel("Average Finish Stage (Higher is Better)")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, "confed_average_finish.png"), dpi=150)
    plt.close()

    # Save summary markdown text using custom markdown generator
    summary_text = f"""# 📊 Advanced EDA Metrics Report

## Multicollinearity (VIF)
Features with VIF > 5.0 (or especially > 10.0) indicate strong multicollinearity.
{df_to_markdown(vif_df)}

## Mutual Information (MI)
MI measures how much information a feature shares with the target variable `finish_stage` (higher means more predictive dependency).
{df_to_markdown(mi_df)}

## Random Forest Feature Importance
Feature importance derived from split criteria in a Random Forest regressor.
{df_to_markdown(rf_importances)}
"""
    with open(os.path.join(eda_dir, "eda_metrics_summary.md"), "w", encoding="utf-8") as f:
        f.write(summary_text)

    print(f"Success! EDA visualizations and data reports saved to {eda_dir}")

if __name__ == "__main__":
    run_eda()
