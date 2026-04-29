# Step 5 mein bharenge - Main brain
"""
Ayyat - Main Assistant Orchestrator
====================================
Sab modules ko integrate karta hai:
    Wake Word -> STT -> LLM Brain -> Tools -> TTS -> Loop

Run:
    python assistant.py
"""

import sys
from pathlib import Path

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from core.stt import listen, recognize_bilingual
from core.tts import speak, detect_language
from core.wake_word import wait_for_wake
from core.llm import chat, reset_memory


# ==================== Banner ====================
BANNER = r"""
   _____                  _
  /  _  \  _   _ _   _  __ _| |_
 |  /_\  || | | | | | |/ _` | __|
 |  _____|| |_| | |_| | (_| | |_
 |_|       \__, |\__, |\__,_|\__|
           |___/ |___/
   Bilingual AI Voice Assistant
   Powered by Llama 3.3 70B (Groq)
   Wake word: "Ayyat"  /  "عیات"
"""


# Hard exit phrases - poori app band kare
HARD_EXIT_PHRASES = [
    "shutdown ayyat", "shut down ayyat", "exit ayyat",
    "ayyat band karo", "بند کرو سب", "ایات بند",
    "goodbye ayyat", "stop everything",
]


# ==================== Single Session Handler ====================
def handle_session() -> bool:
    """
    Wake word ke baad ek interaction handle kare.
    Returns False to exit completely, True to continue.
    """
    # Acknowledge wake
    speak("Yes?", lang="en")

    # User ka command sune
    audio = listen(timeout=6, phrase_time_limit=10)
    if audio is None:
        speak("Kuch suna nahi. Wapas so rahi hun.", lang="en")
        return True

    user_text, lang = recognize_bilingual(audio)
    if not user_text:
        speak("Sorry, samajh nahi paayi.", lang="en")
        return True

    print(f"\n[You ({lang})] {user_text}")

    # Hard exit check
    if any(phrase in user_text.lower() for phrase in HARD_EXIT_PHRASES):
        speak("Goodbye! Shutting down.", lang="en")
        return False

    # LLM brain ko bhejo
    print("[Ayyat thinking...]")
    try:
        reply = chat(user_text, verbose=False)
    except Exception as e:
        print(f"[Brain Error] {e}")
        reply = "Sorry, kuch masla hua. Phir se kahein."

    # Reply ko bolo (apni language detect karke)
    print(f"[Ayyat] {reply}\n")
    reply_lang = detect_language(reply)
    speak(reply, lang=reply_lang)

    return True


# ==================== Main Loop ====================
def main() -> None:
    print(BANNER)
    print("Initializing...\n")

    # Welcome message
    try:
        speak("Ayyat is ready. Say my name to wake me up.", lang="en")
    except Exception as e:
        print(f"[Init Warning] {e}")

    print("Ready! Say 'Ayyat' to begin.\n")

    try:
        while True:
            print("[Listening for wake word: 'Ayyat']")
            if wait_for_wake(verbose=True):
                print("\n>>> Wake word detected <<<\n")
                if not handle_session():
                    break
                print()  # spacing between sessions

    except KeyboardInterrupt:
        print("\n[Interrupted by user]")
        try:
            speak("Goodbye!", lang="en")
        except Exception:
            pass

    except Exception as e:
        print(f"\n[Fatal Error] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()