#!/usr/bin/env python3
import sys
import os
import time
import subprocess
import threading
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentinel.config import load_config, log

PROXY_SCRIPT = os.path.join(os.path.dirname(__file__), "proxy.py")
VENV_MITMDUMP = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "venv/bin/mitmdump"
)

def show_dialog(dialog_type, message, title="Sentinel"):
    subprocess.run([
        "zenity", f"--{dialog_type}",
        f"--text={message}",
        f"--title={title}"
    ], capture_output=True)

def ask_minutes():
    result = subprocess.run([
        "zenity", "--entry",
        "--title=Sentinel",
        "--text=How many minutes do you want to browse?",
        "--entry-text=10"
    ], capture_output=True, text=True)
    if result.returncode != 0:
        return None
    try:
        minutes = int(result.stdout.strip())
        return minutes if minutes > 0 else None
    except ValueError:
        return None

def start_proxy(port=8080):
    proc = subprocess.Popen([
        VENV_MITMDUMP,
        "-s", PROXY_SCRIPT,
        "--listen-port", str(port),
        "-q"
    ])
    time.sleep(2)
    return proc

def main():
    config = load_config()

    # Check cooldown
    remaining = get_remaining_cooldown()
    if remaining > 0:
        try:
            with open(os.path.join(os.path.expanduser("~/.config/sentinel"), "cooldown_duration")) as f:
                duration = int(f.read().strip())
        except Exception:
            duration = 300
        if duration == config["session"]["flagged_cooldown"]:
            show_dialog("error",
                f"A flagged search triggered a cooldown. {remaining} seconds remaining.")
        else:
            show_dialog("error",
                f"Cooldown active. Please wait {remaining} more seconds.")
        sys.exit(1)

    # Ask session length
    minutes = ask_minutes()
    if minutes is None:
        sys.exit(0)

    # Confirm
    result = subprocess.run([
        "zenity", "--question",
        f"--text=Browse for {minutes} minute(s)?",
        "--title=Sentinel",
        "--ok-label=Yes", "--cancel-label=Cancel"
    ], capture_output=True)
    if result.returncode != 0:
        sys.exit(0)

    # Start proxy
    proxy_proc = start_proxy()
    log(f"SESSION STARTED | {minutes} minutes")

    # Session timer
    def on_session_end():
        show_dialog("warning",
            f"Your {minutes} minute session has ended.")
        proxy_proc.terminate()
        kill_browsers()
        trigger_normal_end()

    start_timer(minutes, on_session_end)

    # Wait for proxy to exit
    try:
        proxy_proc.wait()
    except KeyboardInterrupt:
        proxy_proc.terminate()
        kill_browsers()
        trigger_normal_end()

if __name__ == "__main__":
    main()
