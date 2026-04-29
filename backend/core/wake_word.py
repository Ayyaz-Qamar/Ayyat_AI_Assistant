# Pichle project se aayega - Wake word
"""
Wake-Word Detection
===================
Continuous listen kare, "Ayyat" / "عیات" sunte hi True return.

Approach:
    Short audio listen → STT → keyword match check
    Simple aur reliable, internet pe depend hai.

Production use ke liye Picovoice Porcupine better hai (offline,
trained custom keyword), lekin abhi free + simple yeh sahi hai.
"""

from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.stt import listen, recognize_bilingual
from config import WAKE_WORDS


def is_wake_word(text: str) -> bool:
    """Text mein wake word hai ya nahi."""
    if not text:
        return False
    text = text.lower().strip()
    return any(w in text for w in WAKE_WORDS)


def wait_for_wake(verbose: bool = True) -> bool:
    """
    Ek short phrase sune, wake word ho toh True.
    Loop ke andar call karo main.py se.
    """
    audio = listen(timeout=None, phrase_time_limit=3)
    if audio is None:
        return False

    text, _ = recognize_bilingual(audio)
    if text and verbose:
        print(f"[heard] {text}")
    return is_wake_word(text)


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Wake Word Test")
    print("=" * 50)
    print(f"\nListening for: {', '.join(WAKE_WORDS[:6])}, ...")
    print("Bolein 'Ayyat' kabhi bhi (Ctrl+C to stop)\n")

    while True:
        try:
            print("[Listening...]")
            if wait_for_wake():
                print("\n>>> WAKE WORD DETECTED! <<<\n")
            else:
                pass  # silently continue
        except KeyboardInterrupt:
            print("\nBye!")
            break