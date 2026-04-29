"""
Text-to-Speech Module (Edge TTS - Female Desi Voices)
======================================================
Ayyat ki awaz - female, South Asian accent.

Voices:
    English: en-IN-NeerjaNeural   (Indian female - warm, friendly)
    Urdu:    ur-PK-UzmaNeural     (Pakistani female - natural)

Edge TTS = Microsoft's free neural TTS, bilkul ChatGPT-quality!

Fallback: gTTS with Indian accent if edge_tts not available.
"""

import os
import tempfile
import time
import asyncio

# pygame banner silence
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame  # noqa: E402


# ==================== Voice Configuration ====================
# Pakistani/Indian female voices - Ayyat ki personality
VOICES = {
    "en": "en-IN-NeerjaNeural",   # Indian English female - warm, expressive
    "ur": "ur-PK-UzmaNeural",     # Pakistani Urdu female - natural
}

# Alternative voices (agar primary kaam na kare):
ALT_VOICES = {
    "en": "en-IN-PrabhatNeural",  # Indian English (different tone)
    "ur": "ur-IN-GulNeural",      # Indian Urdu female
}

# Voice settings
VOICE_RATE = "+0%"      # Speed: -50% to +100% (e.g., "+10%" for faster)
VOICE_PITCH = "+0Hz"    # Pitch: -50Hz to +50Hz


# ==================== pygame mixer setup ====================
_mixer_ready = False


def _ensure_mixer() -> bool:
    global _mixer_ready
    if _mixer_ready:
        return True
    try:
        pygame.mixer.init()
        _mixer_ready = True
        return True
    except Exception as e:
        print(f"[Audio Init Error] {e}")
        return False


# ==================== Edge TTS (Primary - Best Quality) ====================
async def _edge_tts_save(text: str, voice: str, output_path: str) -> bool:
    """Edge TTS se MP3 generate kare."""
    try:
        import edge_tts
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate=VOICE_RATE,
            pitch=VOICE_PITCH,
        )
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"[Edge TTS Error] {e}")
        return False


def _generate_edge(text: str, lang: str, output_path: str) -> bool:
    """Edge TTS wrapper (sync)."""
    voice = VOICES.get(lang, VOICES["en"])
    try:
        # Run async function in sync context
        return asyncio.run(_edge_tts_save(text, voice, output_path))
    except Exception as e:
        print(f"[Edge TTS Wrapper Error] {e}")
        return False


# ==================== gTTS (Fallback) ====================
def _generate_gtts(text: str, lang: str, output_path: str) -> bool:
    """gTTS fallback - Indian accent."""
    try:
        from gtts import gTTS
        # Indian English accent for English (tld='co.in')
        if lang == "en":
            tts = gTTS(text=text, lang="en", tld="co.in", slow=False)
        else:
            tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        return True
    except Exception as e:
        print(f"[gTTS Error] {e}")
        return False


# ==================== Main speak() function ====================
def speak(text: str, lang: str = "en") -> None:
    """
    Text ko speech mein convert kare aur play kare.

    Tries Edge TTS first (best quality), falls back to gTTS.

    Args:
        text: Kya bolna hai
        lang: 'en' or 'ur'
    """
    text = (text or "").strip()
    if not text:
        return

    if not _ensure_mixer():
        print(f"[Ayyat says] {text}")
        return

    temp_path = None
    try:
        # Temp file path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        # Try Edge TTS first (best quality)
        success = _generate_edge(text, lang, temp_path)

        # Fallback to gTTS if Edge fails
        if not success or not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            print("[TTS] Edge failed, trying gTTS fallback...")
            success = _generate_gtts(text, lang, temp_path)

        if not success:
            print(f"[Ayyat says (text-only)] {text}")
            return

        # Play the audio
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        pygame.mixer.music.unload()

    except Exception as e:
        print(f"[TTS Error] {e}")
        print(f"[Ayyat says] {text}")
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


def detect_language(text: str) -> str:
    """Text Urdu hai ya English."""
    if any("\u0600" <= c <= "\u06FF" for c in text):
        return "ur"
    return "en"


# ==================== List Available Voices ====================
async def _list_voices_async():
    """Edge TTS ke saare available voices list kare (testing utility)."""
    try:
        import edge_tts
        voices = await edge_tts.list_voices()
        # Filter for South Asian voices
        for v in voices:
            locale = v.get("Locale", "")
            if any(loc in locale for loc in ["en-IN", "en-PK", "ur-PK", "ur-IN", "hi-IN"]):
                gender = v.get("Gender", "")
                short_name = v.get("ShortName", "")
                print(f"  {short_name:30} - {gender:6} - {locale}")
    except Exception as e:
        print(f"Error listing voices: {e}")


def list_desi_voices():
    """Show available Indian/Pakistani voices."""
    print("\nSouth Asian Voices Available:\n")
    asyncio.run(_list_voices_async())


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  TTS Test - Ayyat ki Desi Awaz")
    print("=" * 50)

    print(f"\nVoices being used:")
    print(f"  English: {VOICES['en']}")
    print(f"  Urdu:    {VOICES['ur']}")

    print("\n[1] English test (Indian accent female)...")
    speak("Hello! I am Ayyat, your bilingual voice assistant. "
          "I can help you with anything!", lang="en")

    print("\n[2] Urdu test (Pakistani female)...")
    speak("السلام علیکم! میں عیات ہوں، آپ کی ذاتی معاون۔ "
          "میں آپ کی کیا مدد کر سکتی ہوں؟", lang="ur")

    print("\n[3] Mixed conversation test...")
    speak("Sure thing! Let me open notepad for you.", lang="en")
    speak("جی ہاں، نوٹ پیڈ کھول دیا ہے۔", lang="ur")

    print("\nDone! Awaz pasand aayi?")
    print("\nTip: Aur voices dekhna chahein toh:")
    print("  python -c 'from core.tts import list_desi_voices; list_desi_voices()'")