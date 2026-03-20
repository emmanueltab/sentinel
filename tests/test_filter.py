import sys
sys.path.insert(0, '.')

from sentinel.filter import run_pipeline

tests = [
    ("cats", "https://google.com/search?q=cats"),
    ("gmail", "https://google.com/search?q=gmail"),
    ("to love ru", "https://google.com/search?q=to+love+ru"),
    ("beach girls", "https://google.com/search?q=beach+girls"),
]

for query, url in tests:
    flagged, reason, layer = run_pipeline(query, url)
    status = "FLAGGED" if flagged else "ALLOWED"
    print(f"{status} | Layer: {layer} | Query: {query} | Reason: {reason}")
