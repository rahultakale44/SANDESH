"""Optional local text-to-speech helper."""
import tempfile
from pathlib import Path

def synthesize_speech(text: str) -> Path | None:
    if not text.strip():
        return None
    try:
        import pyttsx3
        path = Path(tempfile.gettempdir()) / "signbridge_output.wav"
        engine = pyttsx3.init()
        engine.save_to_file(text, str(path))
        engine.runAndWait()
        return path if path.exists() else None
    except Exception:
        return None
