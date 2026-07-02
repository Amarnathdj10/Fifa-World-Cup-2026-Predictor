import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# Setup paths
base_path = r"D:\Coding journey\Fifa World Cup 2026 Predictor"
csv_path = os.path.join(base_path, "world_cup_dataset.csv")
predict_csv_path = os.path.join(base_path, "prediction_dataset.csv")
final_dir = os.path.join(base_path, "finalmodel")
os.makedirs(final_dir, exist_ok=True)

def train_and_evaluate():
    print("=== FIFA World Cup ML Training Pipeline ===")
    
    # 1. DATA LOADING & CLEANING
    df = pd.read_csv(csv_path).dropna(subset=['finish_stage'])
    
    # 2. FEATURE ENGINEERING
    df['attack_efficiency'] = df['win_percentage_since_last_cup'] * df['goals_scored_per_game']
    
    le = LabelEncoder()
    df['confederation_encoded'] = le.fit_transform(df['confederation'])

    features = [
        'elo_rating', 'win_percentage_since_last_cup', 'goals_scored_per_game', 
        'goals_conceded_per_game', 'points_per_game', 'previous_wc_finish',
        'confederation_encoded', 'attack_efficiency'
    ]

    X = df[features]
    y = df['finish_stage']
    y = y.astype(int) - 1
    groups = df['year']

    # 3. DEFINE MODELS
    models = {
    'Logistic Regression': LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    'Random Forest': RandomForestClassifier(
        n_estimators=300,
        max_depth=5,
        random_state=42
    ),

    'XGBoost': XGBClassifier(
        objective='multi:softprob',
        num_class=7,
        n_estimators=200,
        learning_rate=0.05,
        max_depth=3,
        subsample=0.8,
        colsample_bytree=0.7,
        random_state=42,
        eval_metric='mlogloss'
    )
}

    # 4. LEAVE-ONE-GROUP-OUT CROSS-VALIDATION
    logo = LeaveOneGroupOut()
    comparison_results = []
    cv_predictions = {name: [] for name in models}
    actuals_list = []

    print("Evaluating models with Leave-One-Group-Out CV (by Year)...")
    
    for name, model in models.items():
        accs, f1s = [], []
        preds_all = []
        actuals_all = []
        
        for train_idx, test_idx in logo.split(X, y, groups):
            X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
            y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
            
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
            accs.append(
                accuracy_score(
                    y_test,
                    preds
                )
            )

            f1s.append(
                f1_score(
                    y_test,
                    preds,
                    average='weighted'
                )
            )
            
            preds_all.extend(preds)
            if name == list(models.keys())[0]:
                actuals_all.extend(y_test)
                
        cv_predictions[name] = preds_all
        if not actuals_list:
            actuals_list = actuals_all

        avg_acc = np.mean(accs)
        avg_f1 = np.mean(f1s)
        
        print(f"Model: {name:16s} | Accuracy: {avg_acc:.4f} | F1 sccore: {avg_f1:.4f}")
        comparison_results.append({
        'Model': name,
        'Accuracy': avg_acc,
        'F1': avg_f1
    })
    comparison_df = pd.DataFrame(
        comparison_results
    ).sort_values(
        'F1',
        ascending=False
    )
    comparison_df.to_csv(os.path.join(final_dir, "model_comparison.csv"), index=False)

    best_model_name = comparison_df.iloc[0]['Model']
    print(f"Best model selected: {best_model_name}")

    # 5. GENERATE CONFUSION MATRIX FOR BEST MODEL
    best_preds = cv_predictions[best_model_name]
    y_true_round = np.array(actuals_list)
    y_pred_round = np.array(best_preds)

    cm = confusion_matrix(y_true_round, y_pred_round)
    plt.figure(figsize=(10, 8))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=sorted(np.unique(y_true_round)))
    disp.plot(cmap='Blues', values_format='d')
    plt.title(f"Confusion Matrix (Rounded Stages) - {best_model_name}")
    plt.tight_layout()
    plt.savefig(os.path.join(final_dir, "confusion_matrix.png"), dpi=150)
    plt.close()

    # 6. TRAIN BEST MODEL ON FULL DATASET
    best_model = models[best_model_name]
    best_model.fit(X, y)

    # Save feature importances if the best model supports it
    if hasattr(best_model, 'feature_importances_'):
        importances = pd.Series(best_model.feature_importances_, index=features).sort_values(ascending=False)
        importances.to_csv(os.path.join(final_dir, "feature_importance.csv"))
        plt.figure(figsize=(8,6))
        importances.sort_values().plot(
            kind='barh'
        )
        plt.title(
            f'Feature Importance - {best_model_name}'
        )
        plt.tight_layout()
        plt.savefig(
            os.path.join(
                final_dir,
                "feature_importance.png"
            ),
            dpi=150
        )
        plt.close()
        print("\nFeature Importances for Best Model:")
        print(importances.to_string())

    # 7. LOAD 2026 PREDICTION DATASET & GENERATE PREDICTIONS
        print("Loading 2026 qualified teams...")
        predict_df = pd.read_csv(predict_csv_path)

        # Process features
        predict_df['confederation_encoded'] = le.transform(
            predict_df['confederation']
        )

        predict_df['attack_efficiency'] = (
            predict_df['win_percentage_since_last_cup']
            * predict_df['goals_scored_per_game']
        )

        # Predict most likely stage
        predict_df['predicted_finish_stage'] = (
            best_model.predict(
                predict_df[features]
            ) + 1
        )

        # Predict probabilities for all stages
        probs = best_model.predict_proba(
            predict_df[features]
        )

        # Expected stage score (much more stable than winner probability)
        stage_values = np.arange(1, 8)

        predict_df['strength_score'] = (
            probs @ stage_values
        )

        # Winner probability (optional)
        winner_class = 6

        if winner_class in best_model.classes_:
            winner_idx = np.where(
                best_model.classes_ == winner_class
            )[0][0]

            predict_df['winner_probability'] = (
                probs[:, winner_idx]
            )
        else:
            predict_df['winner_probability'] = 0.0

        # Final results
        results = predict_df[
            [
                'team',
                'elo_rating',
                'strength_score',
                'winner_probability',
                'predicted_finish_stage'
            ]
        ].sort_values(
            'strength_score',
            ascending=False
        )

        results.columns = [
            'Team',
            'Elo_Rating',
            'Strength_Score',
            'Winner_Probability',
            'Predicted_Stage'
        ]

        # Save
        output_path = os.path.join(
            final_dir,
            "final_predictions_2026.csv"
        )

        results.to_csv(
            output_path,
            index=False
        )

        print(f"\nPredictions written to:\n{output_path}")

        print("\nTop 10 predicted teams:")
        print(
            results[
                [
                    'Team',
                    'Strength_Score',
                    'Winner_Probability',
                    'Predicted_Stage'
                ]
            ].head(10)
        )