# Step 4 mein bharenge - Tool registry
"""
Tool Registry
=============
Yeh file LLM (Llama 3.3) ko batati hai:
  1. Konse tools available hain (apps, web search, whatsapp, etc.)
  2. Har tool kya karta hai
  3. Kya parameters chahiye

Format: OpenAI-style "function calling" schema
(Groq isi format ko support karta hai)

Jab user kuch bole, Llama is registry ko padh ke decide karega:
"User Chrome kholna chahta hai - open_app tool use karunga"
"""

from typing import Tuple
import sys
from pathlib import Path

# Tools import karo
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.apps import open_app, list_apps
from tools.web_search import web_search
from tools.whatsapp import send_whatsapp
from tools.media import play_youtube
from tools.system import (
    volume_up, volume_down, set_volume, mute_toggle,
    brightness_up, brightness_down, set_brightness,
    lock_screen, shutdown, cancel_shutdown,
)


# ==================== Tool Schemas (LLM ke liye) ====================
# Ye list Llama ko bhejenge - taake usko pata ho kya kar sakta hai
TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application on the user's Windows PC. "
                           "Use for: chrome, vs code, notepad, calculator, "
                           "spotify, explorer, cmd, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Name of the app to open (e.g., 'chrome', 'notepad', 'vs code')",
                    }
                },
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information and return a summary. "
                           "Use for factual questions, news, definitions, current events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query - what to look up",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_youtube",
            "description": "Play a song or video on YouTube. "
                           "Use for: 'play X song', 'YouTube pe X laga do', music requests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Song or video name to search and play on YouTube",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_whatsapp",
            "description": "Send a WhatsApp message to a contact. "
                           "Use when user wants to message someone.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "Contact name (e.g., 'ali') or phone number with country code (e.g., '+923001234567')",
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content to send",
                    },
                },
                "required": ["recipient", "message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "volume_up",
            "description": "Increase system volume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "integer",
                        "description": "Number of steps to increase (default 5, each step ~2%)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "volume_down",
            "description": "Decrease system volume.",
            "parameters": {
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "integer",
                        "description": "Number of steps to decrease (default 5)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_volume",
            "description": "Set volume to specific percentage (0-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Volume level 0-100",
                    }
                },
                "required": ["level"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mute_toggle",
            "description": "Toggle mute on/off.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "brightness_up",
            "description": "Increase screen brightness.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "Percentage to increase (default 10)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "brightness_down",
            "description": "Decrease screen brightness.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "Percentage to decrease (default 10)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_brightness",
            "description": "Set brightness to specific percentage (0-100).",
            "parameters": {
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Brightness level 0-100",
                    }
                },
                "required": ["level"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lock_screen",
            "description": "Lock the Windows screen.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "shutdown",
            "description": "Schedule system shutdown.",
            "parameters": {
                "type": "object",
                "properties": {
                    "delay_seconds": {
                        "type": "integer",
                        "description": "Seconds before shutdown (default 60)",
                    }
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_shutdown",
            "description": "Cancel a scheduled shutdown.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


# ==================== Tool Executor ====================
# Mapping: tool_name -> actual function
TOOL_FUNCTIONS = {
    "open_app":         open_app,
    "web_search":       web_search,
    "play_youtube":     play_youtube,
    "send_whatsapp":    send_whatsapp,
    "volume_up":        volume_up,
    "volume_down":      volume_down,
    "set_volume":       set_volume,
    "mute_toggle":      mute_toggle,
    "brightness_up":    brightness_up,
    "brightness_down":  brightness_down,
    "set_brightness":   set_brightness,
    "lock_screen":      lock_screen,
    "shutdown":         shutdown,
    "cancel_shutdown":  cancel_shutdown,
}


def execute_tool(tool_name: str, arguments: dict) -> Tuple[bool, str]:
    """
    LLM ke kahe pe tool execute kare.

    Args:
        tool_name: e.g., 'open_app'
        arguments: e.g., {'app_name': 'chrome'}

    Returns:
        (success, result_message)
    """
    if tool_name not in TOOL_FUNCTIONS:
        return False, f"Tool '{tool_name}' available nahi hai."

    func = TOOL_FUNCTIONS[tool_name]
    try:
        # Call function with the arguments dict expanded
        result = func(**arguments)
        # Sab tools (success, message) tuple return karte hain
        if isinstance(result, tuple) and len(result) == 2:
            return result
        return True, str(result)
    except TypeError as e:
        return False, f"Tool '{tool_name}' ke arguments galat: {e}"
    except Exception as e:
        return False, f"Tool '{tool_name}' execute nahi hua: {e}"


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Tool Registry - Available Tools")
    print("=" * 50)
    print(f"\nTotal tools registered: {len(TOOL_SCHEMAS)}\n")
    for i, schema in enumerate(TOOL_SCHEMAS, 1):
        fn = schema["function"]
        print(f"  {i:2}. {fn['name']:20} - {fn['description'][:60]}")
    print(f"\nTotal functions mapped:  {len(TOOL_FUNCTIONS)}")
    print("\nReady to be used by LLM!\n")