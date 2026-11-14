"""Collect labelled hand landmark samples using a local webcam."""
from __future__ import annotations
import argparse, csv
from pathlib import Path
import cv2
import mediapipe as mp

OUT = Path("data/landmarks.csv")
FEATURE_COLUMNS = [f"f{i}" for i in range(63)]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", nargs="+", required=True, help="Labels in key order (max 9 per run)")
    args = parser.parse_args()
    if len(args.labels) > 9:
        raise SystemExit("Use at most 9 labels per run (keys 1-9). Run another batch for remaining labels.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    new_file = not OUT.exists()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Could not open webcam. Check camera permissions.")
    hands_api = mp.solutions.hands
    with hands_api.Hands(max_num_hands=1, min_detection_confidence=0.55) as hands, \
         OUT.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label"] + FEATURE_COLUMNS)
        if new_file:
            writer.writeheader()
        selected = 0
        print("Label keys:")
        for i, label in enumerate(args.labels, 1):
            print(f"  {i}: {label}")
        print("Press 1-9 to select label, S to save current hand sample, Q to quit.")
        current_features = None
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Camera frame unavailable.")
                break
            frame = cv2.flip(frame, 1)
            result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            current_features = None
            if result.multi_hand_landmarks:
                points = [[p.x, p.y, p.z] for p in result.multi_hand_landmarks[0].landmark]
                import numpy as np
                points = np.array(points, dtype=np.float32)
                points -= points[0]
                scale = float(np.max(np.linalg.norm(points, axis=1)))
                if scale > 1e-6: points /= scale
                current_features = points.flatten().tolist()
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, result.multi_hand_landmarks[0], hands_api.HAND_CONNECTIONS
                )
            label = args.labels[selected]
            cv2.putText(frame, f"Label: {label} | S=save | Q=quit",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,255,0), 2)
            cv2.imshow("SignBridge Dataset Collector", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in [ord(str(i)) for i in range(1, len(args.labels)+1)]:
                selected = int(chr(key)) - 1
            elif key in (ord("s"), ord("S")):
                if current_features is None:
                    print("No hand detected; sample not saved.")
                else:
                    writer.writerow({"label": args.labels[selected], **{
                        col: val for col, val in zip(FEATURE_COLUMNS, current_features)
                    }})
                    f.flush()
                    print(f"Saved sample for {args.labels[selected]}")
            elif key in (ord("q"), ord("Q")):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
