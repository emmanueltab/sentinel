import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mitmproxy import http
from urllib.parse import urlparse, parse_qs
from sentinel.filter import run_pipeline
from sentinel.config import log
import subprocess
import re

def extract_query(flow: http.HTTPFlow):
    """Extract search query from URL if it's a search request."""
    url = flow.request.pretty_url
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Google search
    if "google.com/search" in url and "q" in params:
        return params["q"][0], url

    # Bing
    if "bing.com/search" in url and "q" in params:
        return params["q"][0], url

    # DuckDuckGo
    if "duckduckgo.com" in url and "q" in params:
        return params["q"][0], url

    # YouTube search
    if "youtube.com/results" in url and "search_query" in params:
        return params["search_query"][0], url

    return None, url

def kill_browsers():
    """Kill all known browser processes."""
    browsers = [
        "firefox", "chrome", "chromium", "brave", "opera",
        "vivaldi", "microsoft-edge", "epiphany", "falkon"
    ]
    for browser in browsers:
        subprocess.run(["pkill", "-x", browser], capture_output=True)

def request(flow: http.HTTPFlow):
    query, url = extract_query(flow)

    if not query:
        return

    log(f"QUERY: {query} | URL: {url}")

    flagged, reason, layer = run_pipeline(query, url)

    if flagged:
        # Block the request
        flow.response = http.Response.make(
            403,
            f"Blocked by Sentinel: {reason}",
            {"Content-Type": "text/plain"}
        )
        # Kill all browsers
        kill_browsers()
        log(f"SESSION TERMINATED | Layer: {layer} | Reason: {reason}")
