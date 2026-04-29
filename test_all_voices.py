"""
Voice Tester - Sab voices ek-ek karke directly play karta hai.
"""

import asyncio
import edge_tts
import tempfile
import os
import time

# pygame for direct playback
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame


# Sab female voices testing
VOICES = [
    # ===== ENGLISH (Indian / South Asian) =====
    ("en-IN-NeerjaNeural",   "Neerja - Indian female (warm)"),

    # ===== ENGLISH (American) =====
    ("en-US-JennyNeural",    "Jenny - American female (assistant)"),
    ("en-US-AriaNeural",     "Aria - American female (newscaster)"),
    ("en-US-MichelleNeural", "Michelle - American female (calm)"),
    ("en-US-SaraNeural",     "Sara - American female (cheerful)"),

    # ===== ENGLISH (British) =====
    ("en-GB-SoniaNeural",    "Sonia - British female"),
    ("en-GB-LibbyNeural",    "Libby - British female (young)"),

    # ===== ENGLISH (Australian) =====
    ("en-AU-NatashaNeural",  "Natasha - Australian female"),

    # ===== URDU =====
    ("ur-PK-UzmaNeural",     "Uzma - Pakistani Urdu"),
    ("ur-IN-GulNeural",      "Gul - Indian Urdu"),

    # ===== HINDI (saath try karte hain - sometimes work for Urdu too) =====
    ("hi-IN-SwaraNeural",    "Swara - Hindi female"),
    ("hi-IN-AnanyaNeural",   "Ananya - Hindi female (young)"),
]


# Test text
TEXT_EN = "Hello, I am Ayyat. I am your bilingual AI assistant. How can I help you today?"
TEXT_UR = "السلام علیکم، میں عیات ہوں۔ میں آپ کی بات سن رہی ہوں۔"
TEXT_HI = "नमस्ते, मैं आयत हूँ। मैं आपकी कैसे मदद कर सकती हूँ?"


def get_text_for_voice(voice_id):
    """Voice ke language ke hisab se text choose kare."""
    if voice_id.startswith("ur-"):
        return TEXT_UR
    if voice_id.startswith("hi-"):
        return TEXT_HI
    return TEXT_EN


async def play_voice(voice_id, description):
    """Voice ko generate karke directly play kare (no save)."""
    text = get_text_for_voice(voice_id)
    print(f"\n  Voice: {voice_id}")
    print(f"  Type:  {description}")
    print(f"  Text:  {text[:60]}...")
    print("  Generating...")

    # Temp file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp.close()

    try:
        c = edge_tts.Communicate(text=text, voice=voice_id)
        await c.save(tmp.name)

        # Check if file has content
        if os.path.getsize(tmp.name) == 0:
            print("  FAILED - empty audio file")
            return False

        # Play it
        pygame.mixer.music.load(tmp.name)
        pygame.mixer.music.play()
        print("  PLAYING NOW... (sun rahe ho?)")

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        pygame.mixer.music.unload()
        return True

    except Exception as e:
        print(f"  FAILED - {e}")
        return False
    finally:
        # Cleanup
        try:
            os.remove(tmp.name)
        except OSError:
            pass


async def main():
    print("\n" + "=" * 60)
    print("  Ayyat - Voice Tester")
    print("  Sab voices ek-ek karke play hongi")
    print("=" * 60)

    # Init audio
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"\nAudio init failed: {e}")
        return

    print(f"\nTotal voices to test: {len(VOICES)}")
    print("Press Enter to start, then press Enter to play next voice.")
    input("\nReady? Press Enter > ")

    favorites = []

    for i, (voice_id, description) in enumerate(VOICES, 1):
        print(f"\n[{i}/{len(VOICES)}] " + "-" * 50)

        played = await play_voice(voice_id, description)

        if played:
            print("\n  Pasand aayi ye voice?")
            choice = input("    'y' = haan add to favorites, 'n' = nahi, 'q' = quit > ").strip().lower()
            if choice == "y":
                favorites.append((voice_id, description))
                print(f"    ✓ Added to favorites!")
            elif choice == "q":
                print("\nStopping...")
                break
        else:
            input("  Press Enter to continue > ")

    # Summary
    print("\n" + "=" * 60)
    print("  TEST COMPLETE")
    print("=" * 60)
    if favorites:
        print(f"\n  Aapki {len(favorites)} favorite voices:\n")
        for voice_id, desc in favorites:
            print(f"    {voice_id}")
            print(f"      ({desc})\n")
        print("  In se English + Urdu ke liye ek-ek choose karein!")
    else:
        print("\n  No favorites marked.")
    print()


if __name__ == "__main__":
    asyncio.run(main())