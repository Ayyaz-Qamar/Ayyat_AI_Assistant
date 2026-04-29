# Step 4 mein bharenge - Ollama LLM
"""
LLM Module - Groq + Llama 3.3 70B
==================================
Yeh Ayyat ka "brain" hai. Kya karta hai:

  1. User ka message Llama ko bheje
  2. Llama decide kare: "Tool use karna hai ya seedha jawab dena hai?"
  3. Agar tool: argument extract kar ke execute kare
  4. Final reply generate kare user ke liye

Llama 3.3 70B free hai Groq pe, super fast hai (<1 sec).
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from dotenv import load_dotenv
from groq import Groq

# Path setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from tools.registry import TOOL_SCHEMAS, execute_tool
from config import SYSTEM_PROMPT


# ==================== Initialize Groq Client ====================
load_dotenv()  # .env file se API key load karega

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError(
        "GROQ_API_KEY nahi mili .env file mein. "
        "Root folder mein .env banayein with GROQ_API_KEY=your_key"
    )

# Free, fast model
MODEL = "llama-3.3-70b-versatile"

# Groq client
client = Groq(api_key=API_KEY)


# ==================== Conversation Memory ====================
# Pichli baatein yaad rakhe (last 10 exchanges)
class ConversationMemory:
    def __init__(self, max_turns: int = 10):
        self.history: List[Dict] = []
        self.max_turns = max_turns

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        # Old messages trim karo (system prompt protect karte hue)
        if len(self.history) > self.max_turns * 2:
            self.history = self.history[-self.max_turns * 2:]

    def get_messages(self) -> List[Dict]:
        return [{"role": "system", "content": SYSTEM_PROMPT}] + self.history

    def clear(self):
        self.history = []


# Global memory instance
memory = ConversationMemory(max_turns=10)


# ==================== Main Chat Function ====================
def chat(user_message: str, verbose: bool = False) -> str:
    """
    User ka message process kare aur reply de.
    Tool use bhi automatically handle karta hai.

    Args:
        user_message: User ne kya kaha
        verbose: True ho toh internal steps print kare (debugging)

    Returns:
        Final reply text (user ko show karne ke liye)
    """
    if not user_message or not user_message.strip():
        return "Aap ne kuch kaha nahi."

    # User message memory mein add karo
    memory.add("user", user_message)

    if verbose:
        print(f"\n[User] {user_message}")

    try:
        # ----- Step 1: Llama ko message bhejo with tool list -----
        response = client.chat.completions.create(
            model=MODEL,
            messages=memory.get_messages(),
            tools=TOOL_SCHEMAS,           # Available tools batao
            tool_choice="auto",            # Llama khud decide karega
            temperature=0.7,               # Creative but focused
            max_tokens=500,
        )

        msg = response.choices[0].message

        # ----- Step 2: Check kar ke Llama ne tools call kiye ya nahi -----
        if msg.tool_calls:
            if verbose:
                print(f"[LLM] Calling {len(msg.tool_calls)} tool(s)...")

            # Llama ka decision memory mein save (saath assistant message)
            memory.history.append({
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        }
                    } for tc in msg.tool_calls
                ]
            })

            # ----- Step 3: Har tool execute karo -----
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                try:
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}

                if verbose:
                    print(f"   - {tool_name}({arguments})")

                # Tool execute karo
                success, result = execute_tool(tool_name, arguments)
                status = "✓" if success else "✗"

                if verbose:
                    print(f"     {status} {result}")

                # Tool result memory mein add karo
                memory.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": f"{status} {result}",
                })

            # ----- Step 4: Llama se final reply lo (tool results ke baad) -----
            final_response = client.chat.completions.create(
                model=MODEL,
                messages=memory.get_messages(),
                temperature=0.7,
                max_tokens=300,
            )

            final_reply = final_response.choices[0].message.content
            memory.add("assistant", final_reply)

            if verbose:
                print(f"[Ayyat] {final_reply}")

            return final_reply

        else:
            # Tools nahi chahiye - seedha jawab
            reply = msg.content
            memory.add("assistant", reply)

            if verbose:
                print(f"[Ayyat] {reply}")

            return reply

    except Exception as e:
        error_msg = f"Sorry, kuch masla hua: {e}"
        if verbose:
            print(f"[Error] {e}")
        return error_msg


# ==================== Reset Conversation ====================
def reset_memory():
    """Naye conversation start karne ke liye."""
    memory.clear()


# ==================== Test Mode ====================
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Ayyat LLM - Test Mode")
    print("  Powered by Llama 3.3 70B via Groq")
    print("=" * 50)
    print("\nAap kuch bhi pooch sakte hain ya commands de sakte hain:")
    print("  - 'Hello' / 'السلام علیکم'")
    print("  - 'Open Notepad'")
    print("  - 'Search what is python'")
    print("  - 'Volume up'")
    print("  - 'Play tum hi ho'")
    print("  - 'reset' to clear conversation")
    print("  - 'quit' to exit\n")

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Bye!")
                break
            if user_input.lower() == "reset":
                reset_memory()
                print("[Memory cleared]")
                continue

            reply = chat(user_input, verbose=True)
            print(f"\nAyyat > {reply}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nBye!")
            break
        except Exception as e:
            print(f"[Error] {e}\n")