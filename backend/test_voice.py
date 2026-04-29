"""
Quick Edge TTS Voice Test
=========================
Indian female voice ka sample bana ke save kare.

Run:
    python test_voice.py
"""

import asyncio
import edge_tts


async def main():
    # Test 1: Indian English Female
    print("[1/3] Generating English voice (Neerja)...")
    voice = "en-IN-NeerjaNeural"
    text = "Hello! I am Ayyat, your bilingual AI assistant. How can I help you today?"
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("test_english.mp3")
    print("      Saved: test_english.mp3")

    # Test 2: Pakistani Urdu Female
    print("\n[2/3] Generating Urdu voice (Uzma)...")
    voice = "ur-PK-UzmaNeural"
    text = "السلام علیکم! میں عیات ہوں، آپ کی ذاتی معاون۔ میں آپ کی کیا مدد کر سکتی ہوں؟"
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("test_urdu.mp3")
    print("      Saved: test_urdu.mp3")

    # Test 3: Alternative Indian voice
    print("\n[3/3] Generating alternative voice (Aashi)...")
    voice = "en-IN-AashiNeural"
    text = "Hi there! This is another Indian voice option for you."
    communicate = edge_tts.Communicate(text=text, voice=voice)
    await communicate.save("test_aashi.mp3")
    print("      Saved: test_aashi.mp3")

    print("\nDone! Ab files play karo:")
    print("  start test_english.mp3")
    print("  start test_urdu.mp3")
    print("  start test_aashi.mp3")


if __name__ == "__main__":
    asyncio.run(main())