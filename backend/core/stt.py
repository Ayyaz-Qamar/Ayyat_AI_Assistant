# Pichle project se aayega - Speech to text
"""
Speech-to-Text Module
=====================
User ki awaz sun ke text mein convert kare.
Bilingual: English (en-US) + Urdu (ur-PK)

Uses: speech_recognition library + Google Web Speech API (free)
"""

from typing import Optional, Tuple
import speech_recognition as sr


# Single recognizer instance - tuned for natural speech
recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8        # silence before phrase ends
recognizer.energy_threshold = 300        # initial baseline


def listen(timeout: Optional[int] = 5,
           phrase_time_limit: int = 8) -> Optional[sr.AudioData]:
    """
    Microphone se awaz capture kare.

    Args:
        timeout: Max seconds to wait for speech to start. None = wait forever.
        phrase_time_limit: Max seconds for one phrase.

    Returns:
        AudioData object on success, None on timeout/error.
    """
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.4)
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )
            return audio
    except sr.WaitTimeoutError:
        return None
    except OSError as e:
        print(f"[Mic Error] {e} - microphone connected hai?")
        return None
    except Exception as e:
        print(f"[Listen Error] {e}")
        return None


def recognize(audio: sr.AudioData, lang: str = "en-US") -> str:
    """AudioData ko text mein convert kare using Google Speech."""
    if audio is None:
        return ""
    try:
        return recognizer.recognize_google(audio, language=lang).strip()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[STT API Error] {e} - internet check karein.")
        return ""


def _has_urdu_script(text: str) -> bool:
    """Text mein Urdu/Arabic characters hain ya nahi."""
    return any("\u0600" <= c <= "\u06FF" for c in text)


def recognize_bilingual(audio: sr.AudioData) -> Tuple[str, str]:
    """
    English aur Urdu DONO mein recognize karo, behtar result le lo.

    Returns:
        (text, language_code)  where language_code is 'en' or 'ur'.
    """
    if audio is None:
        return ("", "en")

    en_text = recognize(audio, "en-US")
    ur_text = recognize(audio, "ur-PK")

    # Urdu prefer karo agar actual Urdu script return hua
    if ur_text and _has_urdu_script(ur_text):
        return (ur_text, "ur")

    # Warna jo zyada lamba/non-empty hai
    if len(en_text) >= len(ur_text) and en_text:
        return (en_text.lower(), "en")
    if ur_text:
        return (ur_text, "ur")
    return ("", "en")


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  STT Test - Bolein, Ayyat sunegi")
    print("=" * 50)
    print("\nKuch bolein (5 second timeout)...")

    while True:
        try:
            print("\n[Listening...]")
            audio = listen(timeout=5, phrase_time_limit=8)
            if audio is None:
                print("Kuch nahi suna. Try again? (Ctrl+C to quit)")
                continue

            text, lang = recognize_bilingual(audio)
            if text:
                print(f"[Detected ({lang})] {text}")
            else:
                print("Samajh nahi paayi. Phir se bolen.")
        except KeyboardInterrupt:
            print("\nBye!")
            break