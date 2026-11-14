# SignBridge — Indian Sign Language Recognition (Starter Project)

A student project starter for an **Indian Sign Language (ISL) gesture recognition and translation prototype**.

## What is included

- Streamlit web interface for capturing/uploading a gesture image.
- MediaPipe hand-landmark extraction (21 landmarks per detected hand).
- A scikit-learn Random Forest classifier trained on examples collected by your team.
- A small gloss-to-English sentence formatter.
- Optional pre-trained Transformer integration (`google/flan-t5-small`) for gloss-to-sentence generation.
- Optional text-to-speech output.
- Dataset collection and model-training scripts.
- SRS, UML source diagrams, test cases and evaluation script.

> **Important scope/academic honesty:** This ZIP is a runnable project scaffold, not a pre-trained ISL model. It does not contain a licensed, validated ISL dataset or trained weights. You must record examples from consenting signers or use a properly licensed dataset, then run the collection/training steps. The starter recognizes isolated/static signs; it is not yet a full continuous sign-language translator. Facial expression, body movement, grammar, regional variation and signer-independent performance are not fully modelled.

## 1. Requirements

- Python 3.10 or 3.11 recommended.
- Webcam for dataset collection / camera capture.
- Windows, Linux or macOS.
- Internet is needed once to download Python packages and (optionally) the Transformer model.

## 2. Setup (Windows PowerShell)

```powershell
cd SignBridge
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

## 3. Collect your own ISL samples

Get informed consent before recording anyone. Use the same sign definition consistently and record multiple repetitions from multiple signers.

```powershell
python scripts/collect_dataset.py --labels HELLO THANK_YOU WATER HELP YES NO
```

The collector saves one CSV row per detected hand. Press:
- `1` through `9` to choose the corresponding label shown in the terminal.
- `s` to save the current detected landmark sample.
- `q` to quit.

For more than 9 labels, run collection in batches. Dataset rows are saved to `data/landmarks.csv`.

**Dataset quality matters:** aim for at least 50–100 varied samples per sign, from more than one consenting signer, with different lighting/backgrounds. This is only a starting target, not a guarantee of accuracy.

## 4. Train the gesture classifier

```powershell
python scripts/train_model.py
```

The script creates `models/sign_classifier.joblib` and prints a held-out test accuracy. For a valid evaluation, collect enough samples and keep signers or recording sessions separated between train and test where possible. A random split can overestimate real-world generalization.

## 5. Run the application

```powershell
streamlit run app.py
```

Use the camera widget or upload a clear image showing one hand. Select the predicted sign, build a sequence of glosses, and generate English text. Speech playback is optional.

## 6. Transformer sentence generation

The app has an optional Hugging Face `google/flan-t5-small` integration. On first use it downloads model files and may take time / memory. Disable it in the sidebar if your laptop cannot run it. The deterministic gloss formatter is the fallback.

This Transformer is used for **gloss-to-English text generation**, not visual sign recognition. The visual classifier is trained on your collected landmark data.

## 7. Evaluation

```powershell
python scripts/evaluate.py --references data/evaluation.csv
```

Expected CSV columns:
- `reference`: human-written reference English sentence
- `prediction`: system-generated English sentence

The script reports BLEU and chrF if `sacrebleu` is installed. For gesture classification, also report the held-out accuracy, precision, recall and F1 printed during training. Keep the test set separate from training.

## 8. Repository layout

```text
SignBridge/
├── app.py
├── requirements.txt
├── signbridge/
│   ├── landmarks.py
│   ├── classifier.py
│   ├── translator.py
│   └── speech.py
├── scripts/
│   ├── collect_dataset.py
│   ├── train_model.py
│   └── evaluate.py
├── data/
├── models/
├── docs/
│   ├── SRS.md
│   ├── TEST_CASES.md
│   └── uml/
└── tests/
```

## 9. Known limitations and future work

1. Static isolated-sign recognition only in this baseline.
2. One-hand landmark features; two-hand signs need extension.
3. No facial-expression or upper-body features yet.
4. Gloss order is not equivalent to natural-language grammar.
5. The Transformer may hallucinate or change meaning; review outputs and compare against references.
6. A small team-collected dataset may not generalize to unseen signers.
7. Future work: temporal landmark sequences (LSTM/Transformer), two-hand/body/face features, signer-independent evaluation, continuous ISL translation and human evaluation by fluent ISL users.

## 10. Ethical and accessibility notes

- Do not claim the prototype replaces a qualified interpreter.
- Do not record or publish signers' videos without informed consent.
- Clearly label uncertain predictions.
- Involve ISL users / fluent signers in dataset validation and usability testing.
