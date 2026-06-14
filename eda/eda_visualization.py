import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Setup paths
base_path = r"d:\Fifa-World-Cup-2026-Predictor"
csv_path = os.path.join(base_path, "world_cup_dataset.csv")
eda_dir = os.path.join(base_path, "eda")

def run_eda():
    df = pd.read_csv(csv_path).dropna(subset=['finish_stage'])
    
    # 1. Correlation Matrix
    plt.figure(figsize=(10, 8))
    numeric_df = df.select_dtypes(include=['float64', 'int64']).drop(columns=['year'], errors='ignore')
    corr = numeric_df.corr()
    sns.heatmap(corr, annot=True, cmap='RdYlGn', fmt=".2f")
    plt.title("Feature Correlation with Finish Stage")
    plt.tight_layout()
    plt.savefig(os.path.join(eda_dir, "correlation_heatmap.png"))
    plt.close()
    
    # 2. Key Relationship: Elo vs Progress
    plt.figure(figsize=(8, 6))
    sns.regplot(data=df, x='elo_rating', y='finish_stage')
    plt.title("Elo Rating Impact")
    plt.savefig(os.path.join(eda_dir, "elo_relationship.png"))
    plt.close()
    
    print(f"EDA Visualizations generated in {eda_dir}")

if __name__ == "__main__":
    run_eda()
