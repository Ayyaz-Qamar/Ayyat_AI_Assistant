"""
Tool: App Opener
================
Voice command se Windows apps kholne ke liye.

Examples:
    "Open Chrome"           -> Chrome khole
    "Launch VS Code"        -> VS Code khole
    "Notepad kholo"         -> Notepad khole
    "کرومر کھولو"           -> Chrome khole

Smart fallback:
    1. config.py ke APP_PATHS mein check
    2. Windows PATH mein dhoondo (where command)
    3. Start Menu shortcuts mein dhoondo
    4. Last resort: 'start' command (Windows default handler)
"""

import os
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple

# Config import - relative path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import APP_PATHS


# ========== Helper: Username substitution ==========
def _resolve_path(path: str) -> str:
    """{user} placeholder ko actual username se replace karta hai."""
    username = os.getenv("USERNAME") or os.getenv("USER") or "Default"
    return path.replace("{user}", username)


# ========== Helper: Search in Windows PATH ==========
def _find_in_path(app_name: str) -> Optional[str]:
    """Windows PATH mein executable dhoondta hai (jaise 'where' command)."""
    # shutil.which works cross-platform - Python ka built-in 'where'
    for variant in [app_name, f"{app_name}.exe"]:
        result = shutil.which(variant)
        if result:
            return result
    return None


# ========== Helper: Search Start Menu ==========
def _find_in_start_menu(app_name: str) -> Optional[str]:
    """Start Menu shortcuts mein .lnk files dhoondta hai."""
    start_menu_paths = [
        Path(os.getenv("APPDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
        Path(os.getenv("PROGRAMDATA", "")) / "Microsoft/Windows/Start Menu/Programs",
    ]

    app_lower = app_name.lower()
    for base in start_menu_paths:
        if not base.exists():
            continue
        # Recursive search through all subfolders
        for lnk_file in base.rglob("*.lnk"):
            if app_lower in lnk_file.stem.lower():
                return str(lnk_file)
    return None


# ========== Main Function: Open App ==========
def open_app(app_name: str) -> Tuple[bool, str]:
    """
    Voice command se app open kare.

    Args:
        app_name: App ka naam (e.g., "chrome", "notepad", "vs code")

    Returns:
        (success: bool, message: str)
    """
    if not app_name:
        return False, "App ka naam nahi mila."

    name_clean = app_name.lower().strip()

    # ----- Strategy 1: Config se path le -----
    if name_clean in APP_PATHS:
        path = _resolve_path(APP_PATHS[name_clean])

        # Agar full path hai aur exists kare, directly run karo
        if Path(path).is_file() or path.endswith(":"):
            try:
                if path.endswith(":"):  # ms-settings: jaisa URI
                    os.startfile(path)
                else:
                    subprocess.Popen([path])
                return True, f"Opened {app_name} successfully."
            except Exception as e:
                return False, f"Path mila lekin open nahi hua: {e}"

        # Agar simple command hai (calc.exe, cmd.exe), Popen with shell
        if not Path(path).is_absolute():
            try:
                subprocess.Popen(path, shell=True)
                return True, f"Opened {app_name} successfully."
            except Exception as e:
                return False, f"Couldn't open {app_name}: {e}"

    # ----- Strategy 2: Windows PATH search -----
    found = _find_in_path(name_clean)
    if found:
        try:
            subprocess.Popen([found])
            return True, f"Opened {app_name} from system PATH."
        except Exception as e:
            return False, f"Found but couldn't open: {e}"

    # ----- Strategy 3: Start Menu search -----
    shortcut = _find_in_start_menu(name_clean)
    if shortcut:
        try:
            os.startfile(shortcut)
            return True, f"Opened {app_name} from Start Menu."
        except Exception as e:
            return False, f"Shortcut mila lekin open nahi hua: {e}"

    # ----- Strategy 4: Last resort - Windows 'start' command -----
    try:
        subprocess.Popen(f"start {name_clean}", shell=True)
        return True, f"Tried opening {app_name} via system."
    except Exception:
        pass

    return False, f"App '{app_name}' nahi mila. Config mein add karein ya naam check karein."


# ========== List All Available Apps ==========
def list_apps() -> list:
    """Saare configured apps ki list return kare."""
    return sorted(set(APP_PATHS.keys()))


# ========== Test Mode ==========
if __name__ == "__main__":
    """
    Direct test:
        python tools/apps.py
    """
    print("\n" + "=" * 50)
    print("  App Opener - Test Mode")
    print("=" * 50)

    print(f"\nAvailable apps in config:\n  {', '.join(list_apps())}\n")

    while True:
        try:
            user_input = input("\nApp ka naam likhein (ya 'quit' to exit): ").strip()
            if user_input.lower() in ("quit", "exit", "q", ""):
                print("Bye!")
                break

            success, message = open_app(user_input)
            status = "[OK]" if success else "[FAIL]"
            print(f"{status} {message}")
        except KeyboardInterrupt:
            print("\nBye!")
            break# Step 2 mein bharenge - App opener
