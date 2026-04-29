# Step 3 mein bharenge - YouTube/Music
"""
Tool: Media (YouTube / Music)
=============================
Voice command se YouTube pe gaana ya video play kare.

Examples:
    "Play Atif Aslam songs"
    "Play tum hi ho song"
    "YouTube pe Imran Khan speech laga do"
    "اتف اسلم گانے چلاؤ"

How it works:
    pywhatkit YouTube pe pehla matching video kholta hai aur play karta hai.
    Default browser mein khulta hai.
"""

import urllib.parse
import webbrowser
from typing import Tuple


# ========== Play on YouTube ==========
def play_youtube(query: str) -> Tuple[bool, str]:
    """
    YouTube pe pehla video search karke play kare.

    Args:
        query: Gaana ya video ka naam (e.g., "tum hi ho", "atif aslam songs")

    Returns:
        (success, status_message)
    """
    if not query or not query.strip():
        return False, "Kya play karna hai, batayein."

    query = query.strip()

    # Try pywhatkit first
    try:
        import pywhatkit as pwk
        pwk.playonyt(query)
        return True, f"YouTube pe '{query}' play kar di."
    except Exception:
        pass

    # Fallback: open YouTube search URL directly
    try:
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return True, f"YouTube search khol di '{query}' ke liye."
    except Exception as e:
        return False, f"YouTube nahi khol saka: {e}"


# ========== Open YouTube Home ==========
def open_youtube() -> Tuple[bool, str]:
    """Sirf YouTube homepage khole."""
    try:
        webbrowser.open("https://www.youtube.com")
        return True, "YouTube khol di."
    except Exception as e:
        return False, f"YouTube nahi khol saka: {e}"


# ========== Test Mode ==========
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Media (YouTube) - Test Mode")
    print("=" * 50)

    while True:
        try:
            q = input("\nKya play karna hai? (ya 'quit'): ").strip()
            if q.lower() in ("quit", "exit", "q", ""):
                break

            success, msg = play_youtube(q)
            print(f"\n{'[OK]' if success else '[FAIL]'} {msg}")
        except KeyboardInterrupt:
            break