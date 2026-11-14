"""Train and evaluate a baseline Random Forest on collected landmark CSV."""
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

DATA = Path("data/landmarks.csv")
OUT = Path("models/sign_classifier.joblib")

def main():
    if not DATA.exists():
        raise SystemExit("Dataset not found. Run scripts/collect_dataset.py first.")
    df = pd.read_csv(DATA)
    if "label" not in df or df["label"].nunique() < 2:
        raise SystemExit("Collect samples for at least two different labels.")
    feature_cols = [c for c in df.columns if c.startswith("f")]
    if len(feature_cols) != 63:
        raise SystemExit("Expected 63 landmark feature columns.")
    X, y = df[feature_cols].fillna(0), df["label"].astype(str)
    counts = y.value_counts()
    if counts.min() < 2:
        raise SystemExit("Each class needs at least 2 samples for a stratified split.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    model = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    print(f"Test accuracy: {accuracy_score(y_test, pred):.4f}")
    print(classification_report(y_test, pred, zero_division=0))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUT)
    print(f"Saved model: {OUT}")

if __name__ == "__main__":
    main()
