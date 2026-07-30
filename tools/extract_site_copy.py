"""Pull the real Spanish copy out of the saved Squarespace pages.

The rebuild must carry Caribbean Guard's own words. Anything invented here would
be putting words in a safety organization's mouth, so this reads the text nodes
out of the saved HTML and writes them to JSON for review before any of it is
retyped into the new site.

Squarespace stores body copy inside `.sqs-html-content` blocks, so those are what
we want; the rest of the document is framework chrome.
"""
import html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "docs", "site-revamp")

PAGES = ["home", "vision", "team", "nuestro-trabajo", "proyectos",
         "programa-playa-organizada", "lifesaving-club", "swim-club",
         "freediving-club", "involcrate", "donar"]

TAG = re.compile(r"<[^>]+>")
BLOCK = re.compile(r'<div class="sqs-html-content"[^>]*>(.*?)</div>', re.S)
HEAD = re.compile(r"<(h[1-4])[^>]*>(.*?)</\1>", re.S)
ACC = re.compile(r'<span class="accordion-item__title">(.*?)</span>', re.S)
# The section copy on the programme, projects and club pages is NOT in the HTML
# body at all. It lives as escaped JSON in the carousel block's data-current-context
# attribute, under userItems, which is why a plain text scrape returns headings
# with nothing under them.
CTX = re.compile(r'data-current-context="(.*?)"', re.S)


def text(s):
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"</p>", "\n\n", s)
    s = TAG.sub("", s)
    s = html.unescape(html.unescape(s))          # Squarespace double-escapes
    s = s.replace(" ", " ")
    return re.sub(r"[ \t]+", " ", s).strip()


out = {}
for p in PAGES:
    f = os.path.join(SRC, f"_{p}.html")
    if not os.path.exists(f):
        continue
    raw = open(f, encoding="utf-8", errors="replace").read()
    title = re.search(r"<title\s*>(.*?)</title>", raw, re.S)
    blocks = [text(b) for b in BLOCK.findall(raw)]
    sections = []
    for ctx in CTX.findall(raw):
        try:
            data = json.loads(html.unescape(ctx))
        except Exception:
            continue
        for it in data.get("userItems", []) or []:
            t, d = text(it.get("title") or ""), text(it.get("description") or "")
            if t or d:
                sections.append({"title": t, "body": d})

    out[p] = {
        "current_title": html.unescape(title.group(1)).strip() if title else None,
        "headings": [[h[0], text(h[1])] for h in HEAD.findall(raw) if text(h[1])],
        "accordion_titles": [text(a) for a in ACC.findall(raw)],
        "sections": sections,
        "body_blocks": [b for b in blocks if len(b) > 20],
    }

dst = os.path.join(HERE, "site_copy.json")
json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for p, d in out.items():
    print(f"{p:28} {len(d['body_blocks']):2d} blocks, "
          f"{len(d['headings']):2d} headings, {len(d['sections']):2d} sections")
print("\nwrote", dst)
