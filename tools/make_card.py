"""Generate web/card.jpg, the link card image the Squarespace page points at.

It is a REAL SCREENSHOT of the deployed files, not a mockup. That matters: a
hand-made card drifts into showing an interface that no longer exists, and this
one is the only picture of the map most people on the website will ever see.
Re-run it whenever the map's appearance changes.

    python tools/make_card.py

Serves web/ on a local port, drives headless Chrome over the DevTools protocol,
sets Spanish, hides the two pieces of live-only chrome that would freeze into a
still (the saved-copy bar with its timestamp, and the closed bottom sheet whose
edge peeks in at desktop widths), captures at 2x and downsamples to 1200x630.

1200x630 is the standard social preview ratio, so the same file also works as an
og:image later without a second export.

Needs: Pillow, websockets, and Chrome. All present on this machine.
"""
import asyncio, base64, http.server, json, os, shutil, socket
import subprocess, sys, tempfile, threading, time

from PIL import Image
import websockets

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "web")
OUT = os.path.join(WEB, "card.jpg")

WIDTH, HEIGHT, SCALE, QUALITY = 1200, 630, 2, 82

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

# Live-only chrome. Everything else in the interface is real and stays.
PREPARE = """(() => {
  setLang("es");
  document.getElementById("saved").style.display = "none";
  document.getElementById("sheet").style.display = "none";
  document.getElementById("update").classList.remove("show");
  document.getElementById("toast").classList.remove("show");
  return "ok";
})()"""


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(directory, port):
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=directory, **kw)
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("No Chrome or Edge found. Edit CHROME_CANDIDATES.")


async def capture(url, debug_port):
    import urllib.request
    # the browser's own page target
    for _ in range(40):
        try:
            targets = json.load(urllib.request.urlopen(
                f"http://127.0.0.1:{debug_port}/json/list"))
            page = next(t for t in targets if t["type"] == "page")
            break
        except Exception:
            time.sleep(0.25)
    else:
        sys.exit("Chrome did not expose a debugging target.")

    async with websockets.connect(page["webSocketDebuggerUrl"],
                                  max_size=64 * 1024 * 1024) as ws:
        n = 0

        async def cmd(method, params=None):
            nonlocal n
            n += 1
            await ws.send(json.dumps({"id": n, "method": method,
                                      "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == n:
                    if "error" in msg:
                        sys.exit(f"{method}: {msg['error']}")
                    return msg.get("result", {})

        async def js(expr):
            r = await cmd("Runtime.evaluate",
                          {"expression": expr, "awaitPromise": True,
                           "returnByValue": True})
            return r.get("result", {}).get("value")

        await cmd("Page.enable")
        await cmd("Runtime.enable")
        await cmd("Emulation.setDeviceMetricsOverride",
                  {"width": WIDTH, "height": HEIGHT,
                   "deviceScaleFactor": SCALE, "mobile": False})
        await cmd("Page.navigate", {"url": url})
        await asyncio.sleep(7)          # imagery, geojson and the opening fit
        await js(PREPARE)
        await asyncio.sleep(2)          # the relayout after setLang

        state = await js("""JSON.stringify({
            z: map.getZoom(), cards: document.querySelectorAll(".picker .card").length,
            w: Math.round([...document.querySelectorAll(".leaflet-image-layer")]
                 .find(e => !e.classList.contains("backdrop")).getBoundingClientRect().width)
        })""")
        print("  map state:", state)
        s = json.loads(state)
        if s["cards"] < 6 or s["w"] < WIDTH * 0.5:
            sys.exit(f"Refusing to write a card from a map that did not render: {state}")

        shot = await cmd("Page.captureScreenshot", {"format": "png"})
        return base64.b64decode(shot["data"])


def main():
    port = free_port()
    httpd = serve(WEB, port)
    debug_port = free_port()
    profile = tempfile.mkdtemp(prefix="cg-card-")
    chrome = find_chrome()
    proc = subprocess.Popen(
        [chrome, "--headless=new", f"--remote-debugging-port={debug_port}",
         f"--user-data-dir={profile}", "--no-first-run", "--disable-gpu",
         "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        png = asyncio.run(capture(f"http://127.0.0.1:{port}/", debug_port))
        raw = os.path.join(profile, "raw.png")
        open(raw, "wb").write(png)
        im = Image.open(raw).convert("RGB")
        print(f"  captured {im.size[0]}x{im.size[1]}")
        im.resize((WIDTH, HEIGHT), Image.LANCZOS).save(
            OUT, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print(f"wrote {OUT}  {os.path.getsize(OUT):,} B  {WIDTH}x{HEIGHT}")
    finally:
        proc.terminate()
        httpd.shutdown()
        shutil.rmtree(profile, ignore_errors=True)


if __name__ == "__main__":
    main()
