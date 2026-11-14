import numpy as np
import pytest
from signbridge.classifier import predict_sign

class DummyModel:
    classes_ = np.array(["HELLO", "WATER"])
    def predict(self, X):
        return np.array(["WATER"])
    def predict_proba(self, X):
        return np.array([[0.1, 0.9]])

def test_predict_sign():
    label, confidence = predict_sign(DummyModel(), np.zeros(63))
    assert label == "WATER"
    assert confidence == pytest.approx(0.9)

def test_missing_model():
    with pytest.raises(RuntimeError):
        predict_sign(None, np.zeros(63))
