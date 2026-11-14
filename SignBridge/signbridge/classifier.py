"""Load and run the trained isolated-sign classifier."""
from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path("models/sign_classifier.joblib")

def load_classifier(path: str | Path = MODEL_PATH):
    path = Path(path)
    if not path.exists():
        return None
    return joblib.load(path)

def predict_sign(model, features: np.ndarray):
    if model is None:
        raise RuntimeError("No trained model found. Collect data and run scripts/train_model.py.")
    if features is None:
        raise ValueError("No hand landmarks detected.")
    prediction = model.predict([features])[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        confidence = float(np.max(model.predict_proba([features])[0]))
    return str(prediction), confidence
