import re
from sentinel.config import (
    load_wordlist, load_patterns, load_whitelist,
    load_prompt, load_config, log
)
from sentinel.ai.backend import evaluate

def check_wordlist(query):
    query_lower = query.lower()
    for word in load_wordlist():
        if word in query_lower:
            return word
    return None

def check_patterns(url):
    url_lower = url.lower()
    for pattern in load_patterns():
        if pattern in url_lower:
            return pattern
    return None

def check_whitelist(query):
    query_lower = query.lower()
    for entry in load_whitelist():
        if query_lower == entry.lower():
            return True
    return False

def run_pipeline(query, url):
    """
    Runs the full filter pipeline against a query and URL.
    Returns a tuple: (flagged: bool, reason: str, layer: str)
    """

    # Layer 0 — Wordlist
    word = check_wordlist(query)
    if word:
        log(f"FLAGGED WORD: {word} | QUERY: {query}")
        return True, word, "wordlist"

    # Layer 1 — URL patterns
    pattern = check_patterns(url)
    if pattern:
        log(f"FLAGGED PATTERN: {pattern} | URL: {url}")
        return True, pattern, "pattern"

    # Whitelist — skip AI for known safe queries
    if check_whitelist(query):
        log(f"WHITELISTED: {query}")
        return False, None, "whitelist"

    # Layer 2 — AI
    config = load_config()
    if config["ai"]["backend"] != "none":
        prompt = load_prompt()
        response = evaluate(query, prompt, config)

        if response is None:
            log(f"AI UNAVAILABLE: {query}")
            return True, "AI unavailable", "ai_unavailable"

        log(f"AI RESPONSE: {response}")

        if response.strip().upper().startswith("YES"):
            log(f"AI FLAGGED: {query}")
            return True, response, "ai"

    return False, None, None
