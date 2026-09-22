# Caribbean Guard map: stakeholder review brief (2026-09-17)

You are one reviewer in a five-hat user study of a live coastal swim-safety map.
Live URL: https://caribbean-guard-map.vercel.app/   Local copy: http://127.0.0.1:5173/
Source: C:\Users\danie\caribbean-guard\web\index.html (single file, 2,291 lines; CSS at top, zone
records around line 700-900, design commentary inline). Read it; do not edit anything.
Screenshots (look at every one): the `shots/` folder next to this file.
  01 desktop landing, 02 phone 390px vs desktop side by side, 03 phone beach panel open,
  04 phone in Spanish + desktop panel open with the zone lines zoomed in,
  annotated-base-map-v5.png and dangerous-area-v4.png = Caribbean Guard's OWN hand-made maps,
  the source of their legend vocabulary.
DO NOT use browser automation tools (one shared browser, other agents are using it). Fetching
the URL with curl or WebFetch to read HTML is fine.

Context you must honour (project rulings, not up for debate):
- Mobile first. The primary user scans a QR code standing on the sand, in sun, one-handed.
- Status words are INSTRUCTIONS, never ratings, never permission ("NO ENTRES AL AGUA",
  "SOLO CON GUARDAVIDAS", "REVISA ANTES DE ENTRAR", "TEN CUIDADO IGUAL"). Do not propose "safe".
- The UI may never claim more currency or authority than its data has. Every verdict shows
  who and when; unreviewed must look unreviewed. Colour must never be the only channel.
- Spanish primary (tú register), English always present.
- A lifeguard or flag on the beach outranks the map; every tier says so.
- Offline-first (service worker). Bing tiles, zoom 12 to 17 only.

Known already (do not spend findings on these, but you may build on them):
- On a 390px phone the whole-coast view lands below zoom 12, so the map opens as a navy
  field with a tiny coast strip.
- Zone lines are decimated to 9 points per zone, so they are jagged with sharp corners and
  cut-off ends; a dense traced coastline already exists and will replace them.

Your deliverable: write `hat-<N>-<slug>.md` in this folder, then reply to the orchestrator
with ONLY a 120-word summary (top 3 findings + the one thing to keep). Format of the file:
1. "Who I am" (3 lines: the persona, their situation, what they need in 10 seconds).
2. "Findings", max 12, ranked. Each: Severity (BLOCKER / MAJOR / MINOR), Where (screen +
   element), What happens to me (first person, concrete), Evidence (screenshot or line
   number), Fix (one line, a direction not a spec).
3. "Keep", 3 things that already work for me and must survive the redesign.
4. "Layout vote": in one line each, where should these live on a phone and on desktop:
   status cards / legend / beach panel / emergency 911 / language toggle / locate button.
Acceptance: every finding names a screen or line; no finding repeats the two known issues;
no finding proposes a permission-granting label; file under 900 words.
