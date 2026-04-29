"""
Ayyat - Configuration
=====================
Saari settings yahan hain.
"""

import os
from pathlib import Path


# ========== Project Paths ==========
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ========== LLM (Groq) ==========
GROQ_MODEL = "llama-3.3-70b-versatile"


# ========== Voice Settings ==========
# Swara - "Ayyat" sahi pronounce karti hai
TTS_VOICE_EN = "hi-IN-SwaraNeural"
TTS_VOICE_UR = "ur-PK-UzmaNeural"
TTS_VOICE_HI = "hi-IN-SwaraNeural"

# Wake words (multiple variations for accurate detection)
WAKE_WORDS = [
    "ayyat", "ayat", "iyat", "ayet", "ayyet", "hayat",
    "hey ayyat", "hey ayat",
    "عیات", "ایات", "آیت", "آیات",
]

DEFAULT_LANG = "en"
STT_LANG_MAP = {"en": "en-US", "ur": "ur-PK"}


# ========== App Paths (Windows) ==========
APP_PATHS = {
    "chrome":     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome_alt": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "vs code":    r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode":     r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "code":       r"C:\Users\{user}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad":    r"C:\Windows\System32\notepad.exe",
    "calculator": "calc.exe",
    "calc":       "calc.exe",
    "explorer":   "explorer.exe",
    "file explorer": "explorer.exe",
    "cmd":        "cmd.exe",
    "command prompt": "cmd.exe",
    "powershell": "powershell.exe",
    "spotify":    r"C:\Users\{user}\AppData\Roaming\Spotify\Spotify.exe",
    "paint":      "mspaint.exe",
    "task manager": "taskmgr.exe",
    "settings":   "ms-settings:",
}


# ========== Server Settings ==========
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000


# ========== WhatsApp ==========
WHATSAPP_WAIT_TIME = 15
WHATSAPP_TAB_CLOSE_TIME = 3


# ========== Personality ==========
ASSISTANT_NAME = "Ayyat"

SYSTEM_PROMPT = """You are Ayyat, a friendly female AI assistant.

PERSONALITY:
- Friendly, warm, helpful, slightly playful
- Concise - replies should be 1-2 sentences usually
- Confident, like Jarvis from Iron Man

LANGUAGE RULES (STRICT):

1. ALWAYS match the user's exact language:
   - English message -> Reply in English
   - Urdu message (Salam, السلام علیکم, Aap kaise hain) -> Reply in Urdu (Urdu script)
   - Hindi message (Namaste, नमस्ते) -> Reply in Hindi (Devanagari script)

2. NEVER mix or swap languages:
   - User says "Salam" -> NEVER reply with "Namaste"
   - User says "Hello" -> NEVER reply with "Namaste" or "Salam"
   - User says "Namaste" -> Reply in Hindi only

3. Default to English unless user clearly used another language.

4. Keep your identity simple:
   - Just say "I'm Ayyat" - don't say "AI assistant" or "bilingual" in introductions
   - When asked who you are: "I'm Ayyat. How can I help?"

YOU HAVE TOOLS TO:
- Open apps on Windows (Chrome, VS Code, Notepad, etc.)
- Search the web
- Send WhatsApp messages
- Play music/videos on YouTube
- Control system: volume, brightness, lock, shutdown

IMPORTANT:
- When user asks for an action, USE THE TOOLS - don't just say you can't.
- After a tool succeeds, give a short confirmation.
- Never make up information - use web_search if unsure.
"""