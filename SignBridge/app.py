from pathlib import Path
import os
import streamlit as st
import numpy as np
from PIL import Image

from signbridge.landmarks import extract_hand_features
from signbridge.classifier import load_classifier, predict_sign
from signbridge.translator import format_glosses, transformer_gloss_to_text
from signbridge.speech import synthesize_speech

st.set_page_config(page_title="SignBridge", page_icon="🤟", layout="wide")
st.title("🤟 SignBridge")
st.caption("Indian Sign Language gesture recognition and text / speech prototype")

with st.sidebar:
    st.header("Settings")
    use_transformer = st.checkbox(
        "Use pre-trained FLAN-T5 Transformer for gloss-to-English",
        value=os.getenv("ENABLE_TRANSFORMER", "0") == "1",
        help="First run downloads google/flan-t5-small. Disable if your system has limited memory.",
    )
    st.info("Baseline scope: isolated/static signs. This is not a certified interpreter.")

model = load_classifier()
if model is None:
    st.warning("No trained sign model found. Follow README steps to collect samples and train it.")
else:
    st.success("Trained gesture classifier loaded.")

left, right = st.columns([1, 1])
with left:
    st.subheader("1. Capture or upload a sign")
    image_file = st.camera_input("Take a gesture photo")
    if image_file is None:
        image_file = st.file_uploader("Or upload a JPG / PNG image", type=["jpg", "jpeg", "png"])

with right:
    st.subheader("2. Recognized sign")
    if image_file is not None:
        image = Image.open(image_file).convert("RGB")
        st.image(image, caption="Input image", use_container_width=True)
        try:
            features = extract_hand_features(np.array(image))
            if features is None:
                st.error("No hand detected. Try a clear, well-lit image with the full hand visible.")
            elif model is None:
                st.info("Hand detected. Train a classifier before requesting a sign prediction.")
            else:
                label, confidence = predict_sign(model, features)
                st.session_state["latest_sign"] = label
                st.success(f"Prediction: **{label}**")
                if confidence is not None:
                    st.metric("Model confidence (not calibrated)", f"{confidence:.1%}")
                if st.button("Add prediction to sentence"):
                    st.session_state.setdefault("glosses", []).append(label)
        except Exception as exc:
            st.error(str(exc))

st.divider()
st.subheader("3. Build a gloss sequence")
st.caption("Add signs one at a time. Gloss order is only a prototype approximation of ISL grammar.")
if "glosses" not in st.session_state:
    st.session_state["glosses"] = []

available_labels = list(getattr(model, "classes_", [])) if model is not None else []
manual = st.selectbox("Add a known sign manually (useful for testing)", ["— select —"] + available_labels)
c1, c2 = st.columns(2)
with c1:
    if st.button("Add selected sign", disabled=manual == "— select —"):
        st.session_state["glosses"].append(manual)
with c2:
    if st.button("Clear sequence"):
        st.session_state["glosses"] = []

st.write("Current sequence:", " → ".join(st.session_state["glosses"]) or "No signs added")
if st.button("Generate English output", type="primary", disabled=not st.session_state["glosses"]):
    if use_transformer:
        st.session_state["sentence"] = transformer_gloss_to_text(st.session_state["glosses"])
    else:
        st.session_state["sentence"] = format_glosses(st.session_state["glosses"])

if st.session_state.get("sentence"):
    st.subheader("4. English output")
    st.success(st.session_state["sentence"])
    if st.button("Generate speech"):
        audio_path = synthesize_speech(st.session_state["sentence"])
        if audio_path:
            st.audio(str(audio_path))
        else:
            st.warning("Speech synthesis is unavailable on this system. Install/configure pyttsx3 or use browser TTS.")
