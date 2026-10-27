"""Verify the deployed static site against the files in this GitHub commit."""
import hashlib
import http.cookiejar
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request
import urllib.error

site = Path(__file__).resolve().parents[1] / "public"
client = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
# HostGator rejects Python's default client identifier on static requests.
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"


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
        "User-Agent": USER_AGENT,
    })
    if path.name == '.htaccess':
        try:
            with client.open(request, timeout=45):
                raise RuntimeError('Apache configuration must not be publicly readable')
        except urllib.error.HTTPError as error:
            if error.code not in (403, 404):
                raise
        print('Apache configuration is not publicly readable:', relative)
        continue
    with client.open(request, timeout=45) as response:
        if response.status != 200:
            raise RuntimeError("Unexpected HTTP status for " + relative)
        content = response.read()
        if path.suffix == '.html' and relative.startswith('nueva/'):
            cache = response.headers.get('Cache-Control', '').lower()
            if not all(value in cache for value in ('no-cache', 'max-age=0', 'must-revalidate')):
                raise RuntimeError('Preview HTML must revalidate its cached version: ' + relative)
        if relative == "nueva/api/siniestros.php":
            data = json.loads(content)
            if not (data.get("ok") is True and data.get("ready") is True
                    and data.get("version") == "claims-20261009"
                    and data.get("recipient") == "siniestros@efyseguros.com"
                    and len(data.get("csrf", "")) == 64
                    and data.get("limits", {}).get("max_files") == 3):
                raise RuntimeError("Claim intake is not ready on the deployed server")
            cookies = response.headers.get("Set-Cookie", "").lower()
            if "secure" not in cookies or "httponly" not in cookies:
                raise RuntimeError("Claim form session cookie is not protected")
        elif relative == "nueva/api/coberturas.php":
            data = json.loads(content)
            if not (data.get("ok") is True and data.get("ready") is True
                    and data.get("version") == "coverage-20261026"
                    and len(data.get("csrf", "")) == 64):
                reason = data.get("unavailable_reason")
                allowed_reasons = {"CONFIG_FILE_UNAVAILABLE", "CONFIG_INVALID", "API_KEY_FORMAT_INVALID",
                                   "API_URL_INVALID", "PRIVATE_STORAGE_UNAVAILABLE", "CURL_UNAVAILABLE"}
                safe_reason = reason if isinstance(reason, str) and reason in allowed_reasons else "UNKNOWN"
                raise RuntimeError("Cooperative coverage lookup is not ready: " + safe_reason)
            if "no-store" not in response.headers.get("Cache-Control", "").lower():
                raise RuntimeError("Coverage responses must not be cached")
            cookies = response.headers.get("Set-Cookie", "").lower()
            if "secure" not in cookies or "httponly" not in cookies:
                raise RuntimeError("Coverage lookup session cookie is not protected")
            if set(data) != {"ok", "ready", "version", "csrf"}:
                raise RuntimeError("Coverage configuration exposes unexpected fields")
        elif path.suffix == ".php":
            raise RuntimeError("A new PHP endpoint needs an explicit runtime check: " + relative)
        elif hashlib.sha256(content).digest() != hashlib.sha256(path.read_bytes()).digest():
            raise RuntimeError("Published file differs from this version: " + relative)
    print("HTTPS verified:", relative)
print("Página y recursos verificados por HTTPS; coinciden con la versión publicada.")
