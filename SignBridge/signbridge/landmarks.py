"""MediaPipe hand landmark extraction utilities."""
from __future__ import annotations
import numpy as np

def extract_hand_features(image_rgb: np.ndarray) -> np.ndarray | None:
    """Return normalized 63-value feature vector for the first detected hand.

    Coordinates are normalized relative to the wrist and scaled by the maximum
    wrist-relative distance. Returns None when no hand is detected.
    """
    try:
        import mediapipe as mp
    except ImportError as exc:
        raise RuntimeError("MediaPipe is not installed. Run: pip install -r requirements.txt") from exc

    hands_api = mp.solutions.hands
    with hands_api.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        result = hands.process(image_rgb)
    if not result.multi_hand_landmarks:
        return None

    points = np.array(
        [[p.x, p.y, p.z] for p in result.multi_hand_landmarks[0].landmark],
        dtype=np.float32,
    )
    points -= points[0]  # wrist-relative translation invariance
    scale = float(np.max(np.linalg.norm(points, axis=1)))
    if scale > 1e-6:
        points /= scale
    return points.flatten()
