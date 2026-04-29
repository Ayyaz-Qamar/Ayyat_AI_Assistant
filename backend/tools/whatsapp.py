# Step 3 mein bharenge - WhatsApp
"""
Tool: WhatsApp Messaging
========================
Voice command se WhatsApp pe message bhejna.

Examples:
    "WhatsApp Ali — meeting at 5"
    "Send WhatsApp to +923001234567 — kaisa hai"

Requirements:
    - WhatsApp Web pehle login hona chahiye Chrome mein
    - Pehli baar QR code scan karna padega

How it works:
    pywhatkit web.whatsapp.com kholta hai aur message type karta hai.
    Ye automation hai - Chrome mein Whatsapp Web khulega.

NOTE:
    Phone numbers ko 'contacts dictionary' mein save karna hota hai
    voice se naam ke saath bhejne ke liye. Phone numbers configurable.
"""

import time
import urllib.parse
import webbrowser
from datetime import datetime, timedelta
from typing import Tuple

# Import config for wait times
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import WHATSAPP_WAIT_TIME, WHATSAPP_TAB_CLOSE_TIME


# ========== Contacts (yahan add karein apne contacts) ==========
# Voice se "WhatsApp Ali" bolen toh ye dictionary se number lega
# Format: "name (lowercase)" -> "+countrycodenumber"
CONTACTS = {
    # Examples - apne contacts add karein:
    # "ali":     "+923001234567",
    # "ammi":    "+923334567890",
    # "papa":    "+923009876543",
    # "ahmad":   "+923451234567",
}


# ========== Resolve Recipient ==========
def _resolve_recipient(recipient: str) -> str:
    """
    Recipient ko phone number mein convert karta hai.
    Agar pehle se number hai (+ se start), waisa hi return.
    Agar naam hai, CONTACTS dictionary mein dhoondega.
    """
    recipient = recipient.strip().lower()

    # Already a phone number
    if recipient.startswith("+") or recipient.startswith("00"):
        # Clean up - remove spaces and dashes
        return recipient.replace(" ", "").replace("-", "")

    # Look up in contacts
    return CONTACTS.get(recipient, "")


# ========== Send WhatsApp via pywhatkit ==========
def send_whatsapp(recipient: str, message: str) -> Tuple[bool, str]:
    """
    WhatsApp pe message bheje.

    Args:
        recipient: Phone number (+923001234567) ya CONTACTS ka naam ("ali")
        message: Bhejne wala message

    Returns:
        (success, status_message)
    """
    if not recipient or not message:
        return False, "Recipient ya message khaali hai."

    phone = _resolve_recipient(recipient)
    if not phone:
        return False, (
            f"'{recipient}' contacts mein nahi mila. "
            f"whatsapp.py mein CONTACTS dictionary mein add karein, "
            f"ya seedha number bolenein (+923001234567)."
        )

    # Try pywhatkit first (preferred - automated send)
    try:
        import pywhatkit as pwk
        # Calculate send time (current time + small offset)
        now = datetime.now()
        send_time = now + timedelta(seconds=WHATSAPP_WAIT_TIME)

        pwk.sendwhatmsg(
            phone_no=phone,
            message=message,
            time_hour=send_time.hour,
            time_minute=send_time.minute,
            wait_time=WHATSAPP_WAIT_TIME,
            tab_close=True,
            close_time=WHATSAPP_TAB_CLOSE_TIME,
        )
        return True, f"WhatsApp message bhej diya {recipient} ko."
    except Exception as e:
        # Fallback: open WhatsApp Web with pre-filled message manually
        try:
            encoded_msg = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={phone}&text={encoded_msg}"
            webbrowser.open(url)
            return True, (
                f"WhatsApp Web khol di. Send button manually press karein."
            )
        except Exception:
            return False, f"WhatsApp bhejne mein masla: {e}"


# ========== List Contacts ==========
def list_contacts() -> list:
    """Saved contacts ki list."""
    return sorted(CONTACTS.keys())


# ========== Test Mode ==========
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  WhatsApp - Test Mode")
    print("=" * 50)
    print(f"\nSaved contacts: {list_contacts() or 'None - whatsapp.py mein add karein'}")
    print("\nNote: Test ke liye pehle apna number CONTACTS mein add karein,")
    print("ya direct number type karein (+923001234567)\n")

    try:
        recipient = input("Recipient (naam ya +number): ").strip()
        message = input("Message: ").strip()

        if recipient and message:
            confirm = input(f"\nSend '{message}' to {recipient}? (y/n): ")
            if confirm.lower() == "y":
                success, msg = send_whatsapp(recipient, message)
                print(f"\n{'[OK]' if success else '[FAIL]'} {msg}")
            else:
                print("Cancelled.")
    except KeyboardInterrupt:
        print("\nBye!")