# Step 3 mein bharenge - Web search
"""
Tool: Web Search
================
Voice command se web pe search kare aur summary de.

Examples:
    "Search Python tutorials"
    "What is quantum computing"
    "Imran Khan kaun hai"
    "موسم کیسا ہے" (with location)

Strategy:
    1. DuckDuckGo Instant Answer API (free, no API key) - quick facts
    2. Wikipedia API (free) - encyclopedia summaries
    3. Google search URL fallback - opens browser if no instant answer
"""

import requests
import urllib.parse
from typing import Tuple


# ========== DuckDuckGo Instant Answer ==========
def _search_duckduckgo(query: str) -> str:
    """
    DuckDuckGo Instant Answer API - free, no API key needed.
    Returns short instant answer if available, else empty string.
    """
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_html": "1",
            "skip_disambig": "1",
        }
        resp = requests.get(url, params=params, timeout=5)
        data = resp.json()

        # Try different response fields
        if data.get("AbstractText"):
            return data["AbstractText"][:500]
        if data.get("Answer"):
            return str(data["Answer"])[:500]
        if data.get("Definition"):
            return data["Definition"][:500]

        # Related topics fallback
        if data.get("RelatedTopics"):
            for topic in data["RelatedTopics"]:
                if isinstance(topic, dict) and topic.get("Text"):
                    return topic["Text"][:500]
    except Exception:
        pass
    return ""


# ========== Wikipedia Summary ==========
def _search_wikipedia(query: str) -> str:
    """Wikipedia REST API - free, no key, returns article summary."""
    try:
        # Pehle search karo to get correct article title
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        }
        resp = requests.get(search_url, params=search_params, timeout=5)
        results = resp.json().get("query", {}).get("search", [])

        if not results:
            return ""

        title = results[0]["title"]

        # Phir summary fetch karo
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
        resp = requests.get(summary_url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            extract = data.get("extract", "")
            if extract:
                return extract[:600]
    except Exception:
        pass
    return ""


# ========== Open in Browser (last resort) ==========
def _open_search_in_browser(query: str) -> bool:
    """Google search browser mein khol de."""
    try:
        import webbrowser
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        webbrowser.open(url)
        return True
    except Exception:
        return False


# ========== Main Function ==========
def web_search(query: str, open_browser: bool = False) -> Tuple[bool, str]:
    """
    Web pe search kare aur summary return kare.

    Args:
        query: Search query
        open_browser: Agar True ho, browser mein bhi khole

    Returns:
        (success, result_text)
    """
    if not query or not query.strip():
        return False, "Search ke liye query nahi mili."

    query = query.strip()

    # Strategy 1: DuckDuckGo
    ddg_result = _search_duckduckgo(query)
    if ddg_result:
        if open_browser:
            _open_search_in_browser(query)
        return True, ddg_result

    # Strategy 2: Wikipedia
    wiki_result = _search_wikipedia(query)
    if wiki_result:
        if open_browser:
            _open_search_in_browser(query)
        return True, wiki_result

    # Strategy 3: No instant answer - open in browser
    if _open_search_in_browser(query):
        return True, f"'{query}' ke liye browser mein search khol di hai."

    return False, "Search nahi kar saka, internet check karein."


# ========== Test Mode ==========
if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Web Search - Test Mode")
    print("=" * 50)

    while True:
        try:
            q = input("\nKya search karna hai? (ya 'quit'): ").strip()
            if q.lower() in ("quit", "exit", "q", ""):
                break

            print("\nSearching...")
            success, result = web_search(q)
            print(f"\n{'[OK]' if success else '[FAIL]'}")
            print(f"\n{result}\n")
            print("-" * 50)
        except KeyboardInterrupt:
            break