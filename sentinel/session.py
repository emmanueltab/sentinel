import os
import time
import subprocess
import threading
from datetime import datetime
from sentinel.config import load_config, log

BASE_DIR = os.path.expanduser("~/.config/sentinel")
COOLDOWN_FILE = os.path.join(BASE_DIR, "cooldown")
COOLDOWN_DURATION_FILE = os.path.join(BASE_DIR, "cooldown_duration")

def get_remaining_cooldown():
    """Returns remaining cooldown in seconds, or 0 if none."""
    if not os.path.exists(COOLDOWN_FILE):
        return 0
    try:
        with open(COOLDOWN_FILE) as f:
            last = int(f.read().strip())
        with open(COOLDOWN_DURATION_FILE) as f:
            duration = int(f.read().strip())
        elapsed = int(time.time()) - last
        remaining = duration - elapsed
        return max(0, remaining)
    except Exception:
        return 0

def set_cooldown(duration):
    """Sets a cooldown of the given duration in seconds."""
    with open(COOLDOWN_FILE, "w") as f:
        f.write(str(int(time.time())))
    with open(COOLDOWN_DURATION_FILE, "w") as f:
        f.write(str(duration))
    log(f"COOLDOWN SET: {duration} seconds")

def kill_browsers():
    """Kill all known browser processes."""
    browsers = [
        "firefox", "chrome", "chromium", "brave", "opera",
        "vivaldi", "microsoft-edge", "epiphany", "falkon",
        "qutebrowser", "luakit", "surf", "palemoon",
        "basilisk", "waterfox", "librewolf", "icecat", "seamonkey"
    ]
    for browser in browsers:
        subprocess.run(["pkill", "-x", browser], capture_output=True)

    # Kill Flatpak browsers
    flatpak_browsers = [
        "com.brave.Browser",
        "com.google.Chrome",
        "com.microsoft.Edge",
        "org.mozilla.firefox"
    ]
    for app in flatpak_browsers:
        subprocess.run(["pkill", "-f", app], capture_output=True)

    log("ALL BROWSERS KILLED")

def trigger_flag(layer, reason):
    """Flag a session — kill browsers and set 20 min cooldown."""
    config = load_config()
    cooldown = config["session"]["flagged_cooldown"]
    kill_browsers()
    set_cooldown(cooldown)
    log(f"FLAGGED | Layer: {layer} | Reason: {reason}")

def trigger_unavailable():
    """AI unavailable — kill browsers and set 5 min cooldown."""
    config = load_config()
    cooldown = config["session"]["unavailable_cooldown"]
    kill_browsers()
    set_cooldown(cooldown)
    log("SESSION CLOSED: AI unavailable")

def trigger_normal_end():
    """Normal session end — set 5 min cooldown."""
    config = load_config()
    cooldown = config["session"]["normal_cooldown"]
    set_cooldown(cooldown)
    log("SESSION ENDED normally")

def start_timer(minutes, on_end):
    """
    Starts a session timer.
    Calls on_end() when the session expires.
    """
    seconds = minutes * 60
    log(f"SESSION STARTED | {minutes} minutes")

    def timer():
        # 1 minute warning
        if minutes > 2:
            time.sleep(seconds - 60)
            log("1 MINUTE REMAINING")
            subprocess.run(["zenity", "--warning",
                "--text=1 minute remaining in your session.",
                "--title=Sentinel"], capture_output=True)
            time.sleep(60)
        else:
            time.sleep(seconds)

        log("SESSION TIMER EXPIRED")
        on_end()

    t = threading.Thread(target=timer, daemon=True)
    t.start()
    return t
