"""
Ayyat — Project Structure Setup
================================
Ye script saari folders aur empty files bana deti hai.

USAGE:
    python setup.py

Run karne ke baad:
    - Saari folders ban jayengi (backend/, frontend/, etc.)
    - Saari empty files ban jayengi (placeholders)
    - Phir hum step-by-step files bharte jayenge

Ek baar chalao, phir delete kar dena (ya rehne dena, koi farak nahi).
"""

import os
from pathlib import Path

# Sab folders jo banane hain
FOLDERS = [
    "backend",
    "backend/core",
    "backend/tools",
    "frontend",
    "frontend/css",
    "frontend/js",
    "frontend/assets",
]

# Sab files jo banane hain (path: starter content)
FILES = {
    # Backend root
    "backend/main.py":          "# Step 6 mein bharenge - FastAPI server\n",
    "backend/assistant.py":     "# Step 5 mein bharenge - Main brain\n",
    "backend/config.py":        "# Step 1 ka pehla file - Settings\n",
    "backend/responses.py":     "# Pichle project se aayega - Bilingual replies\n",

    # Backend/core
    "backend/core/__init__.py": '"""Core voice + LLM modules."""\n',
    "backend/core/stt.py":      "# Pichle project se aayega - Speech to text\n",
    "backend/core/tts.py":      "# Pichle project se aayega - Text to speech\n",
    "backend/core/wake_word.py":"# Pichle project se aayega - Wake word\n",
    "backend/core/llm.py":      "# Step 4 mein bharenge - Ollama LLM\n",

    # Backend/tools
    "backend/tools/__init__.py":   '"""Tool implementations."""\n',
    "backend/tools/registry.py":   "# Step 4 mein bharenge - Tool registry\n",
    "backend/tools/apps.py":       "# Step 2 mein bharenge - App opener\n",
    "backend/tools/web_search.py": "# Step 3 mein bharenge - Web search\n",
    "backend/tools/whatsapp.py":   "# Step 3 mein bharenge - WhatsApp\n",
    "backend/tools/media.py":      "# Step 3 mein bharenge - YouTube/Music\n",
    "backend/tools/system.py":     "# Step 3 mein bharenge - System control\n",

    # Frontend
    "frontend/index.html":      "<!-- Step 7 mein bharenge - Jarvis HUD -->\n",
    "frontend/css/style.css":   "/* Step 7 mein bharenge - Jarvis theme */\n",
    "frontend/js/app.js":       "// Step 8 mein bharenge - Main controller\n",
    "frontend/js/websocket.js": "// Step 8 mein bharenge - WebSocket\n",
    "frontend/js/orb.js":       "// Step 8 mein bharenge - Animated orb\n",

    # Root
    ".gitignore": (
        "# Python\n"
        "__pycache__/\n"
        "*.pyc\n"
        "venv/\n"
        ".env\n\n"
        "# IDE\n"
        ".vscode/\n"
        ".idea/\n\n"
        "# OS\n"
        "Thumbs.db\n"
        ".DS_Store\n\n"
        "# Audio temp\n"
        "*.mp3\n"
        "*.wav\n"
    ),
}


def main():
    base = Path(__file__).resolve().parent
    print("\n" + "=" * 50)
    print("  Ayyat - Project Structure Setup")
    print("=" * 50 + "\n")

    # Folders banao
    print("[1/2] Creating folders...")
    for folder in FOLDERS:
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  Created folder: {folder}/")

    # Files banao
    print("\n[2/2] Creating files...")
    for file_path, content in FILES.items():
        path = base / file_path
        # Sirf tab banao agar pehle se nahi hai (overwrite na ho)
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"  Created file:   {file_path}")
        else:
            print(f"  Skipped (exists): {file_path}")

    print("\n" + "=" * 50)
    print("  Done! Project structure ready.")
    print("=" * 50)
    print(f"\n  Total: {len(FOLDERS)} folders, {len(FILES)} files")
    print("\n  Next steps:")
    print("    1. VS Code mein left panel mein structure dekho")
    print("    2. Ye batao 'structure ban gaya'")
    print("    3. Phir Step 1 ke baki files (config.py + requirements.txt) bharenge\n")


if __name__ == "__main__":
    main()
