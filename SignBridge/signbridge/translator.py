"""Gloss sequence to English sentence generation."""
from __future__ import annotations
import os
import re

DEFAULT_MODEL = os.getenv("TRANSFORMER_MODEL", "google/flan-t5-small")

def format_glosses(glosses: list[str]) -> str:
    """Safe deterministic baseline; replace with fluent ISL-reviewed rules as needed."""
    cleaned = [re.sub(r"[^A-Za-z0-9_' -]", "", g).strip().upper() for g in glosses]
    cleaned = [g for g in cleaned if g]
    if not cleaned:
        return ""
    # A gloss sequence is not necessarily grammatical English.
    return " ".join(cleaned).capitalize() + "."

def transformer_gloss_to_text(glosses: list[str], model_name: str = DEFAULT_MODEL) -> str:
    """Optional pre-trained Transformer generation. Requires torch/transformers and internet on first run."""
    if not glosses:
        return ""
    try:
        from transformers import pipeline
        generator = pipeline("text2text-generation", model=model_name)
        prompt = (
            "Convert this sequence of Indian Sign Language gloss labels into one "
            "short, clear English sentence. Preserve the intended meaning. "
            "If the sequence is ambiguous, do not invent details. Glosses: "
            + " ".join(glosses)
        )
        output = generator(prompt, max_new_tokens=64, do_sample=False)
        text = output[0]["generated_text"].strip()
        return text if text else format_glosses(glosses)
    except Exception:
        # Do not crash the app if optional model download/runtime fails.
        return format_glosses(glosses)
