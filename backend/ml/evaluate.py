

import os
import sys
import joblib
import yaml
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CONFIG_PATH = os.path.join(PROJECT_ROOT, "backend", "config.yaml")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def resolve_path(path):
    """Convert a project-relative path from config.yaml to an absolute path."""
    return os.path.join(PROJECT_ROOT, path)



def evaluate_classifier(config):
    print("\n" + "=" * 60)
    print("CLASSIFICATION MODEL — TEST SET EVALUATION")
    print("=" * 60)

    data_path = resolve_path(config["data"]["processed"]["ticket"])
    model_path = resolve_path(config["models"]["classifier"]["path"])

    df = pd.read_csv(data_path)
    model = joblib.load(model_path)

    target = config["features"]["ticket"]["target"]
    use_cols = config["features"]["ticket"]["use"]

    X = df[use_cols]
    y = df[target]

    # EXACTLY the same split used in ml_engine.py
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Prediction only — NO TRAINING
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    auc = roc_auc_score(y_test, y_prob)

    print(f"Test samples : {len(y_test)}")
    print(f"Accuracy     : {accuracy:.4f} ({accuracy * 100:.2f}%)")
    print(f"Precision    : {precision:.4f}")
    print(f"Recall       : {recall:.4f}")
    print(f"F1 Score     : {f1:.4f}")
    print(f"ROC-AUC      : {auc:.4f}")

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "roc_auc": auc,
    }



def evaluate_regressor(config):
    print("\n" + "=" * 60)
    print("REGRESSION MODEL — TEST SET EVALUATION")
    print("=" * 60)

    data_path = resolve_path(config["data"]["processed"]["delay"])
    model_path = resolve_path(config["models"]["regressor"]["path"])

    df = pd.read_csv(data_path)
    model = joblib.load(model_path)

    target = config["features"]["delay"]["target"]

    X = df.drop(columns=[target])
    y = df[target]

    # EXACTLY the same split used in ml_engine.py
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    # Prediction only — NO TRAINING
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print(f"Test samples : {len(y_test)}")
    print(f"MAE          : {mae:.4f}")
    print(f"MSE          : {mse:.4f}")
    print(f"RMSE         : {rmse:.4f}")
    print(f"R²           : {r2:.4f}")

    return {
        "mae": mae,
        "mse": mse,
        "rmse": rmse,
        "r2": r2,
    }


if __name__ == "__main__":
    print("\nTransReliant — Existing Model Evaluation")
    print("NO MODEL TRAINING WILL BE PERFORMED.")
    print("Loading .pkl files and evaluating on the test split...\n")

    config = load_config()

    classifier_metrics = evaluate_classifier(config)
    regressor_metrics = evaluate_regressor(config)

    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE")
    print("=" * 60)
    print("Existing models were evaluated without retraining.")
