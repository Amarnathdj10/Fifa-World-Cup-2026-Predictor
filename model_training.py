import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

train_df = pd.read_csv("world_cup_dataset.csv")
pred_df = pd.read_csv("prediction_dataset.csv")

X_train = train_df.drop(
    columns=["team", "year", "finish_stage"]
)

y_train = train_df["finish_stage"]

X_pred = pred_df.drop(
    columns=["team", "year"]
)

le_conf = LabelEncoder()
le_host = LabelEncoder()

train_df["confederation"] = le_conf.fit_transform(
    train_df["confederation"]
)
pred_df["confederation"] = le_conf.transform(
    pred_df["confederation"]
)

train_df["host"] = le_host.fit_transform(
    train_df["host"]
)
pred_df["host"] = le_host.transform(
    pred_df["host"]
)

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)

pred_df["predicted_finish"] = model.predict(X_pred)

probs = model.predict_proba(X_pred)

results = pred_df[
    ["team", "predicted_finish"]
]

print(results)