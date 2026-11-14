# Software Requirements Specification (SRS)
## SignBridge — ISL Gesture Recognition and Translation Prototype
**Version:** 1.0 | **Status:** Academic project baseline

## 1. Introduction
### 1.1 Purpose
This document specifies requirements for SignBridge, a prototype that recognizes selected isolated Indian Sign Language (ISL) hand gestures from camera images and presents predicted gloss labels as English text, with optional speech output.

### 1.2 Scope
The first release supports a team-defined vocabulary of isolated/static signs. It extracts hand landmarks using MediaPipe, classifies them using a supervised machine-learning model trained on labelled samples, and optionally uses a pre-trained text-to-text Transformer (`google/flan-t5-small`) to turn a sequence of gloss labels into a short English sentence. Speech is generated using local text-to-speech.

**Out of scope for v1:** certified interpretation, unrestricted continuous ISL translation, full ISL grammar, regional dialect coverage, robust two-hand/body/face modelling, medical/legal emergency use.

### 1.3 Intended users
- ISL signers participating in consented data collection and usability testing.
- Hearing users who need to understand a supported set of signs.
- Student developers, evaluators and instructors.

### 1.4 Definitions
- **ISL:** Indian Sign Language.
- **Landmark:** a detected keypoint such as a finger joint.
- **Gloss:** a written label representing a sign, not a complete natural-language translation.
- **WER:** Word Error Rate.
- **BLEU / chrF:** corpus-level machine-translation evaluation metrics.

## 2. Overall Description
### 2.1 Product perspective
A local web application with image capture/upload, landmark extraction, gesture classification, gloss-sequence composition, optional Transformer sentence generation and optional speech output.

### 2.2 User characteristics
Users need basic ability to operate a browser and camera. The application must clearly communicate that only supported signs are recognized.

### 2.3 Operating environment
Python 3.10/3.11, Windows/Linux/macOS, webcam, modern browser. Model inference runs locally. First-time package/model installation may require internet.

### 2.4 Constraints
- Model quality depends on dataset size, signer diversity and capture conditions.
- The baseline uses one-hand static landmarks.
- The optional FLAN-T5 model may require substantial memory and network access on first use.
- Transformer output may be fluent but semantically incorrect; it must be evaluated against human references.
- ISL is a natural language; gloss order is not necessarily English word order.

### 2.5 Assumptions and dependencies
A consenting signer or licensed dataset is available. Python dependencies install successfully. Webcam permissions are granted. ISL labels are validated by a fluent signer or qualified reviewer.

## 3. System Features and Functional Requirements
### FR-01 Image Input
The system shall allow the user to capture an image through the browser camera or upload a JPG/PNG image.

### FR-02 Hand Detection
The system shall attempt to detect one hand and extract 21 3D landmarks.

### FR-03 Feature Normalization
The system shall normalize landmark coordinates relative to the wrist and hand scale before classification.

### FR-04 Sign Classification
The system shall classify a feature vector into one of the labels represented in the trained model.

### FR-05 Unknown / Failure Handling
The system shall display a clear message if no hand is detected or no trained model is available. The baseline shall not imply that every gesture is supported.

### FR-06 Gloss Sequence
The user shall be able to add recognized or manually selected labels to a sequence and clear the sequence.

### FR-07 English Text Generation
The system shall generate a baseline gloss rendering and optionally invoke a pre-trained text-to-text Transformer to produce an English sentence.

### FR-08 Speech Output
The system shall provide optional speech playback for generated English text when local TTS is available.

### FR-09 Dataset Collection
The developer shall be able to collect labelled landmark samples using a local webcam utility.

### FR-10 Model Training
The developer shall be able to train and save a classifier from the labelled CSV dataset.

### FR-11 Evaluation
The system shall support reporting classification accuracy, precision, recall and F1, and sentence-level BLEU/chrF when reference translations are supplied.

## 4. Non-Functional Requirements
### NFR-01 Usability
The interface shall label each step and show actionable error messages.

### NFR-02 Performance
On the project team's test laptop, a single-image prediction should complete within a target of 2 seconds after model load; actual measured latency shall be reported, not assumed.

### NFR-03 Reliability
Missing model files, invalid images and absent hand detections shall be handled without an unhandled application crash.

### NFR-04 Privacy
The application shall process images locally by default. The team shall obtain informed consent before recording or sharing signer data.

### NFR-05 Maintainability
Data collection, landmark extraction, classification, text generation and speech shall be separated into modules.

### NFR-06 Portability
The application shall run on supported desktop operating systems with a compatible Python environment.

### NFR-07 Accessibility
Text output shall remain available even if speech synthesis is unavailable.

### NFR-08 Transparency
The application shall disclose that it is a limited prototype and not a replacement for a qualified interpreter.

## 5. External Interface Requirements
### 5.1 User interface
Streamlit browser interface with camera/upload input, prediction result, gloss-sequence controls, text result and optional audio.

### 5.2 Software interfaces
- MediaPipe Hands for landmark extraction.
- scikit-learn model for sign classification.
- Hugging Face Transformers / FLAN-T5 for optional gloss-to-text generation.
- pyttsx3 for local speech synthesis.

### 5.3 Hardware interfaces
Webcam and a general-purpose laptop/desktop. GPU is not mandatory for the baseline classifier.

## 6. Data Requirements
Training CSV schema: `label,f0,...,f62`. Each row contains a class label and 63 normalized landmark values. Keep train/test data separated by signer or recording session for a credible generalization estimate. Do not publish identifiable video without consent.

## 7. System Architecture
Camera/upload image → MediaPipe hand landmarks → normalized feature vector → trained classifier → gloss sequence → optional FLAN-T5 text generation → English text → optional TTS.

The visual classifier in v1 is trained from collected examples; FLAN-T5 is a pre-trained Transformer used only in the gloss-to-English stage. This distinction must be stated in the project report.

## 8. UML Diagrams
PlantUML source files are supplied in `docs/uml/`:
- `use_case.puml`
- `activity.puml`
- `sequence.puml`
- `class.puml`
- `architecture.puml`

Render them using a PlantUML extension or PlantUML server before inserting into the final report.

## 9. Acceptance Criteria
- User can capture/upload an image.
- Hand landmarks are extracted when a hand is visible.
- After training, classifier predicts one of the collected labels.
- No-hand and missing-model conditions show clear messages.
- User can build a gloss sequence and generate text.
- Optional speech is playable where supported.
- Team reports measured classifier metrics and BLEU/chrF on a held-out test set.
- Limitations, dataset provenance and consent practices are documented.

## 10. Risks and Mitigations
| Risk | Mitigation |
|---|---|
| Small / biased dataset | Collect multiple samples from multiple consenting signers; report limitations |
| Similar hand shapes | Add more examples; review labels with ISL expert |
| Static model misses motion | Scope v1 to isolated signs; plan temporal model for future work |
| Transformer changes meaning | Compare with human references; provide deterministic fallback |
| TTS unavailable | Keep text output as primary output |
| Privacy concerns | Local processing, consent and data minimization |
