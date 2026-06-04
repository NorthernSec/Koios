# healthcheck.py
import json
import sys
import urllib.request

try:
    response = urllib.request.urlopen(
        "http://localhost:8000/_health",
        timeout=3,
    )
    data = json.load(response)
    sys.exit(0 if data.get("status") == "ok" else 1)
except Exception:
    sys.exit(1)
