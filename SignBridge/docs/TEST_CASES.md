# SignBridge Test Cases

| ID | Type | Preconditions / Input | Steps | Expected Result |
|---|---|---|---|---|
| TC-01 | UI | App running | Open app | SignBridge title and capture/upload controls appear |
| TC-02 | Input | Valid JPG/PNG | Upload image | Image preview appears |
| TC-03 | Detection | Image with visible hand | Upload image | 21 hand landmarks are extracted |
| TC-04 | Detection negative | Image with no hand | Upload image | Clear no-hand message; app remains usable |
| TC-05 | Model missing | No model artifact | Upload hand image | App asks user to collect data and train model |
| TC-06 | Classification | Trained model and known sign sample | Upload sample | One supported label is predicted |
| TC-07 | Sequence | At least one model class exists | Add label(s) | Gloss sequence updates |
| TC-08 | Clear sequence | Non-empty sequence | Click Clear sequence | Sequence becomes empty |
| TC-09 | Text generation | Non-empty sequence | Generate English output | Non-empty text appears |
| TC-10 | Transformer fallback | Transformer unavailable | Enable Transformer and generate | App returns deterministic fallback text |
| TC-11 | Speech | TTS available | Generate speech | Audio file is playable |
| TC-12 | Speech negative | TTS unavailable | Generate speech | Warning appears; text remains visible |
| TC-13 | Training | CSV with >=2 classes and >=2 rows/class | Run training script | Model artifact is saved |
| TC-14 | Training negative | Dataset missing | Run training script | Actionable error is printed |
| TC-15 | Evaluation | CSV has reference/prediction columns | Run evaluation script | BLEU and chrF are reported |
| TC-16 | Invalid evaluation | Missing required CSV column | Run evaluation script | Validation error is printed |

## Evaluation protocol
1. Use a held-out set that is not used during model fitting.
2. Prefer signer-independent or session-independent splitting.
3. Report class-wise precision, recall and F1, not accuracy alone.
4. For sentence generation, prepare human-verified reference sentences.
5. Report BLEU/chrF and qualitative examples; automatic metrics alone do not establish semantic correctness.
