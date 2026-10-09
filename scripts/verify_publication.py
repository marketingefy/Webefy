"""Verify the deployed static site against the files in this GitHub commit."""
import hashlib
from pathlib import Path
import time
import urllib.parse
import urllib.request

site = Path(__file__).resolve().parents[1] / "public"
for path in sorted(site.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(site).as_posix()
    route = "" if relative == "index.html" else urllib.parse.quote(relative)
    url = "https://www.efyseguros.com/" + route + "?efy_publish=" + str(time.time_ns())
    # HostGator rejects Python's default client identifier with HTTP 406.
    # Use browser-compatible request headers; retain HTTPS/TLS and exact-content checks.
    request = urllib.request.Request(url, headers={
        "Cache-Control": "no-cache",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    })
    with urllib.request.urlopen(request, timeout=45) as response:
        if response.status != 200:
            raise RuntimeError("Unexpected HTTP status for " + relative)
        if hashlib.sha256(response.read()).digest() != hashlib.sha256(path.read_bytes()).digest():
            raise RuntimeError("Published file differs from this version: " + relative)
    print("HTTPS verified:", relative)
print("Página y recursos verificados por HTTPS; coinciden con la versión publicada.")
