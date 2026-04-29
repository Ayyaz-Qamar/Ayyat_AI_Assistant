"""
Tool: System Control (v2 - Reliable)
====================================
Volume, brightness, lock, shutdown control.

Uses pyautogui keyboard shortcuts for volume (works on ALL Windows versions).
Pycaw was unreliable across versions - this is much more stable.

Examples:
    "Volume up"           -> Volume +1 step (~2%)
    "Volume up 5"         -> Volume +5 steps (~10%)
    "Mute"                -> Mute toggle
    "Brightness up"
    "Lock screen"
"""

import os
import subprocess
from typing import Tuple, Optional


# ==================== Volume Control (via Keyboard Keys) ====================
def volume_up(steps: int = 5) -> Tuple[bool, str]:
    """
    Volume increase using Windows volume key.
    Each step = ~2% (Windows default).
    """
    try:
        import pyautogui
        for _ in range(steps):
            pyautogui.press("volumeup")
        return True, f"Volume increased by {steps} steps."
    except Exception as e:
        return False, f"Volume up nahi kar saka: {e}"


def volume_down(steps: int = 5) -> Tuple[bool, str]:
    try:
        import pyautogui
        for _ in range(steps):
            pyautogui.press("volumedown")
        return True, f"Volume decreased by {steps} steps."
    except Exception as e:
        return False, f"Volume down nahi kar saka: {e}"


def mute_toggle() -> Tuple[bool, str]:
    try:
        import pyautogui
        pyautogui.press("volumemute")
        return True, "Mute toggled."
    except Exception as e:
        return False, f"Mute nahi kar saka: {e}"


def set_volume(level: int) -> Tuple[bool, str]:
    """
    Volume set kare specific level pe.
    Pehle mute karta hai (max down), phir desired level tak up.
    """
    level = max(0, min(100, int(level)))
    try:
        import pyautogui
        # Volume ko 0 pe le jao - 50 steps zaroor enough hain
        for _ in range(50):
            pyautogui.press("volumedown")
        # Phir desired level tak up karo (each step ~2%)
        steps_needed = level // 2
        for _ in range(steps_needed):
            pyautogui.press("volumeup")
        return True, f"Volume set to ~{level}%."
    except Exception as e:
        return False, f"Volume set nahi kar saka: {e}"


def get_volume() -> Optional[int]:
    """
    Volume read karna pyautogui se possible nahi.
    pycaw try karte hain agar mile.
    """
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        # Try newer API
        for attr in ["Activate", "_dev"]:
            try:
                if attr == "_dev":
                    interface = devices._dev.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                    )
                else:
                    interface = devices.Activate(
                        IAudioEndpointVolume._iid_, CLSCTX_ALL, None
                    )
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                return round(volume.GetMasterVolumeLevelScalar() * 100)
            except (AttributeError, Exception):
                continue
    except Exception:
        pass
    return None


# ==================== Brightness Control ====================
def set_brightness(level: int) -> Tuple[bool, str]:
    level = max(0, min(100, int(level)))
    try:
        import screen_brightness_control as sbc
        sbc.set_brightness(level)
        return True, f"Brightness set to {level}%."
    except Exception as e:
        return False, f"Brightness set nahi kar saka: {e}"


def get_brightness() -> Optional[int]:
    try:
        import screen_brightness_control as sbc
        result = sbc.get_brightness()
        return result[0] if isinstance(result, list) else int(result)
    except Exception:
        return None


def brightness_up(amount: int = 10) -> Tuple[bool, str]:
    current = get_brightness()
    if current is None:
        return False, "Current brightness detect nahi kar saka."
    return set_brightness(min(100, current + amount))


def brightness_down(amount: int = 10) -> Tuple[bool, str]:
    current = get_brightness()
    if current is None:
        return False, "Current brightness detect nahi kar saka."
    return set_brightness(max(0, current - amount))


# ==================== System Actions ====================
def lock_screen() -> Tuple[bool, str]:
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return True, "Screen locked."
    except Exception as e:
        return False, f"Lock nahi kar saka: {e}"


def shutdown(delay_seconds: int = 60) -> Tuple[bool, str]:
    try:
        subprocess.run(["shutdown", "/s", "/t", str(delay_seconds)], check=True)
        return True, f"Shutdown {delay_seconds} seconds mein."
    except Exception as e:
        return False, f"Shutdown nahi kar saka: {e}"


def restart(delay_seconds: int = 60) -> Tuple[bool, str]:
    try:
        subprocess.run(["shutdown", "/r", "/t", str(delay_seconds)], check=True)
        return True, f"Restart {delay_seconds} seconds mein."
    except Exception as e:
        return False, f"Restart nahi kar saka: {e}"


def cancel_shutdown() -> Tuple[bool, str]:
    try:
        subprocess.run(["shutdown", "/a"], check=True)
        return True, "Shutdown cancel kar di."
    except Exception as e:
        return False, f"Cancel nahi kar saka: {e}"


# ==================== Friendly Command Parser ====================
def _parse_command(cmd: str):
    cmd = cmd.strip().lower()

    # Number aliases
    aliases = {
        "1": ("vol_up", None),
        "2": ("vol_down", None),
        "3": ("vol_set", None),
        "4": ("mute", None),
        "5": ("bright_up", None),
        "6": ("bright_down", None),
        "7": ("lock", None),
        "8": ("cancel", None),
    }
    if cmd in aliases:
        return aliases[cmd]

    # Text commands - volume up/down (with optional number)
    if any(w in cmd for w in ["volume up", "vol up", "louder"]):
        # Extract number if present
        for tok in cmd.split():
            if tok.isdigit():
                return ("vol_up_n", int(tok))
        return ("vol_up", None)

    if any(w in cmd for w in ["volume down", "vol down", "quieter"]):
        for tok in cmd.split():
            if tok.isdigit():
                return ("vol_down_n", int(tok))
        return ("vol_down", None)

    if "mute" in cmd or "unmute" in cmd:
        return ("mute", None)

    if any(w in cmd for w in ["brightness up", "bright up", "brighter"]):
        return ("bright_up", None)
    if any(w in cmd for w in ["brightness down", "bright down", "dimmer", "darker"]):
        return ("bright_down", None)

    if "lock" in cmd:
        return ("lock", None)
    if "cancel" in cmd:
        return ("cancel", None)

    # "volume 50" or "set volume 50"
    parts = cmd.replace("set", "").split()
    if "volume" in parts or "vol" in parts:
        for p in parts:
            if p.isdigit():
                return ("vol_set", int(p))
    if "brightness" in parts or "bright" in parts:
        for p in parts:
            if p.isdigit():
                return ("bright_set", int(p))

    return (None, None)


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  System Control v2 - Test Mode")
    print("=" * 50)

    vol = get_volume()
    bright = get_brightness()
    print(f"\nCurrent Volume:     {str(vol) + '%' if vol is not None else 'N/A (detection limited)'}")
    print(f"Current Brightness: {str(bright) + '%' if bright is not None else 'N/A'}")
    print("\nNote: Volume control kaam karega even agar reading 'N/A' aaye.")

    menu = """
    Commands (number ya text):
      1 / volume up         2 / volume down
      3 / volume 50         4 / mute
      5 / brightness up     6 / brightness down
      7 / lock              8 / cancel shutdown
      q / quit

    Bhi try karein: 'volume up 10', 'brightness 70'
    """
    print(menu)

    while True:
        try:
            raw = input("Choice: ").strip()
            if raw.lower() in ("q", "quit", "exit", ""):
                print("Bye!")
                break

            action, value = _parse_command(raw)

            if action == "vol_up":
                print(volume_up()[1])
            elif action == "vol_up_n":
                print(volume_up(steps=value)[1])
            elif action == "vol_down":
                print(volume_down()[1])
            elif action == "vol_down_n":
                print(volume_down(steps=value)[1])
            elif action == "vol_set":
                if value is None:
                    value = int(input("Volume level (0-100): "))
                print(set_volume(value)[1])
            elif action == "mute":
                print(mute_toggle()[1])
            elif action == "bright_up":
                print(brightness_up()[1])
            elif action == "bright_down":
                print(brightness_down()[1])
            elif action == "bright_set":
                print(set_brightness(value)[1])
            elif action == "lock":
                print("Locking in 2 seconds... (Ctrl+C to cancel)")
                import time; time.sleep(2)
                print(lock_screen()[1])
            elif action == "cancel":
                print(cancel_shutdown()[1])
            else:
                print(f"  Samajh nahi aaya: '{raw}' - menu se try karein.")
        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"Error: {e}")