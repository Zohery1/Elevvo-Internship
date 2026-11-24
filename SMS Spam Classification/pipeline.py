#!/usr/bin/env python3
import os
from pathlib import Path
import urllib.request

import joblib
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

DATA_URL = "https://huggingface.co/datasets/codesignal/sms-spam-collection/raw/main/sms-spam-collection.csv"
DATA_PATH = Path(__file__).parent / "sms-spam-collection.csv"
MODEL_PATH = Path(__file__).parent / "spam_classifier.joblib"


def ensure_dataset(file_path: Path) -> Path:
    if not file_path.exists():
        print(f"Downloading dataset to {file_path}...")
        req = urllib.request.Request(DATA_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(file_path, "wb") as f:
            f.write(response.read())
        print("Download complete.")
    return file_path


def load_and_inspect_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    print("\nDataset Overview:")
    print(f"Total messages: {len(df)}")
    print(f"Missing values:\n{df.isnull().sum()}")

    counts = df["label"].value_counts()
    percentages = df["label"].value_counts(normalize=True) * 100
    print("\nClass Distribution:")
    for label in counts.index:
        print(f"  {label}: {counts[label]} ({percentages[label]:.2f}%)")

    print("\nSample Ham Message:")
    ham_sample = df[df["label"] == "ham"]["message"].iloc[0]
    print(f"  {ham_sample}")

    print("\nSample Spam Message:")
    spam_sample = df[df["label"] == "spam"]["message"].iloc[0]
    print(f"  {spam_sample}")

    return df


def build_pipeline(classifier_type: str = "logistic_regression") -> Pipeline:
    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=2,
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    if classifier_type == "logistic_regression":
        classifier = LogisticRegression(random_state=42, class_weight="balanced")
    elif classifier_type == "multinomial_nb":
        classifier = MultinomialNB()
    else:
        raise ValueError(f"Unknown classifier type: {classifier_type}")

    return Pipeline([("tfidf", vectorizer), ("clf", classifier)])


def evaluate_model(name: str, y_true, y_pred) -> dict:
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, pos_label="spam", zero_division=0)
    rec = recall_score(y_true, y_pred, pos_label="spam", zero_division=0)
    f1 = f1_score(y_true, y_pred, pos_label="spam", zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=["ham", "spam"])

    print(f"\n--- {name} ---")
    print(f"Accuracy:        {acc:.4f}")
    print(f"Spam Precision:  {prec:.4f}")
    print(f"Spam Recall:     {rec:.4f}")
    print(f"Spam F1-Score:   {f1:.4f}")
    print(f"Confusion Matrix (labels: [ham, spam]):\n{cm}")
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, zero_division=0))

    return {
        "name": name,
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "confusion_matrix": cm,
    }


def analyze_errors(X_test: pd.Series, y_true: pd.Series, y_pred) -> None:
    results = pd.DataFrame({"message": X_test, "actual": y_true, "predicted": y_pred})

    false_positives = results[(results["actual"] == "ham") & (results["predicted"] == "spam")]
    false_negatives = results[(results["actual"] == "spam") & (results["predicted"] == "ham")]

    print("\nError Analysis:")
    print(f"False Positives (ham flagged as spam): {len(false_positives)}")
    for _, row in false_positives.head(3).iterrows():
        print(f"  - {row['message'][:90]}")

    print(f"\nFalse Negatives (spam missed by model): {len(false_negatives)}")
    for _, row in false_negatives.head(3).iterrows():
        print(f"  - {row['message'][:90]}")


def run_pipeline() -> None:
    dataset_file = ensure_dataset(DATA_PATH)
    df = load_and_inspect_data(dataset_file)

    X_train, X_test, y_train, y_test = train_test_split(
        df["message"],
        df["label"],
        test_size=0.20,
        random_state=42,
        stratify=df["label"],
    )

    print(f"\nTrain set size: {len(X_train)} messages")
    print(f"Test set size:  {len(X_test)} messages")

    # 1. Majority-class Baseline
    dummy = DummyClassifier(strategy="most_frequent")
    dummy.fit(X_train, y_train)
    evaluate_model("Majority-Class Baseline", y_test, dummy.predict(X_test))

    # 2. Logistic Regression (Primary model)
    lr_pipeline = build_pipeline("logistic_regression")
    lr_pipeline.fit(X_train, y_train)
    evaluate_model("TF-IDF + Logistic Regression (Balanced)", y_test, lr_pipeline.predict(X_test))

    # 3. Multinomial Naive Bayes (Bonus comparison)
    nb_pipeline = build_pipeline("multinomial_nb")
    nb_pipeline.fit(X_train, y_train)
    evaluate_model("TF-IDF + Multinomial Naive Bayes", y_test, nb_pipeline.predict(X_test))

    # Error analysis on Logistic Regression
    analyze_errors(X_test, y_test, lr_pipeline.predict(X_test))

    # Save primary model
    joblib.dump(lr_pipeline, MODEL_PATH)
    print(f"\nSaved trained pipeline to: {MODEL_PATH}")


if __name__ == "__main__":
    run_pipeline()
