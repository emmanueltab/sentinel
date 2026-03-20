import yaml
import os

BASE_DIR = os.path.expanduser("~/.config/sentinel")

CONFIG_FILE = os.path.join(BASE_DIR, "config.yml")
WORDLIST_FILE = os.path.join(BASE_DIR, "wordlist.txt")
PATTERNS_FILE = os.path.join(BASE_DIR, "patterns.txt")
PROMPT_FILE = os.path.join(BASE_DIR, "prompt.txt")
LOG_FILE = os.path.join(BASE_DIR, "activity.log")
COOLDOWN_FILE = os.path.join(BASE_DIR, "cooldown")
COOLDOWN_DURATION_FILE = os.path.join(BASE_DIR, "cooldown_duration")
WHITELIST_FILE = os.path.join(BASE_DIR, "whitelist.txt")



def load_config():
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def load_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return []
    with open(WHITELIST_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_wordlist():
    if not os.path.exists(WORDLIST_FILE):
        return []
    with open(WORDLIST_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_patterns():
    if not os.path.exists(PATTERNS_FILE):
        return []
    with open(PATTERNS_FILE, "r") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_prompt():
    if not os.path.exists(PROMPT_FILE):
        return ""
    with open(PROMPT_FILE, "r") as f:
        return f.read()

def log(message):
    from datetime import datetime
    entry = f"{datetime.now()} | {message}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
