# Deploying the safety map

**Host: Vercel.** Daniel's call, 2026-09-14. Cloudflare Pages is kept as a
fallback at the end of this file; both configs are in the repo and must be kept
in step.

The map is a folder of static files. There is no build step and no server.
**Deploying is one command.** That is deliberate: the person who has to do this in
a year may not be a programmer, and a deploy nobody can perform is a map that
quietly stops being updated.

> **One thing first, if you cloned this repository fresh.** The satellite imagery
> lives in `web/tiles/`, 2,152 files and about 20 MB, and it is deliberately NOT
> in git: a public repository is the wrong place for twenty megabytes of
> third-party imagery. Check whether `web/tiles/` exists. If it does, skip this.
> If it does not, run once:
>
> ```
> python tools/build_tiles.py
> ```
>
> It takes a few minutes and needs an internet connection. **Deploying without
> it produces a map with no imagery at all** — every zone line and label in place
> over a blank navy field — and nothing warns you, so check that `web/tiles/`
> is there before you drag anything.

---

## The short version

From a terminal in this repository:

```
npm i -g vercel        # once
vercel login           # once, opens a browser
cd web
vercel                 # first time: answers below
vercel --prod          # publish it
```

**`vercel login` is not optional and is easy to miss.** Without it every other
command fails with `Error: No existing credentials found`, which reads like a
broken install rather than a missing step. It opens a browser, you pick how to
sign in, and the credentials are stored for good. Log in with **the account that
should own this site** — see the open question about account ownership at the
bottom of this file, because switching later means re-adding the domain.

If you want to see it working before deciding who owns it,
`vercel deploy --temporary` produces a live URL with no account at all, which you
can claim into an account afterwards.

`vercel` asks a few questions the first time. The answers:

| Question | Answer |
|---|---|
| Set up and deploy? | **y** |
| Which scope? | your own account |
| Link to existing project? | **n** |
| Project name | `caribbean-guard-map` |
| In which directory is your code? | **`./`** (you are already in `web`) |
| Modify settings? | **n** |

It uploads about 2,165 files and 25 MB, which takes a few minutes the first time
and seconds afterwards, because Vercel only sends files that changed.

You get a `.vercel.app` address and the map works there immediately with no edits
to any file. `vercel` alone makes a preview; **`vercel --prod` is the one that
publishes.**

To publish a change later: `cd web && vercel --prod`. Nothing else to touch.

### Why the CLI rather than the dashboard

Dragging a folder into the Vercel dashboard works, but this folder is 2,165 files
and the browser uploader is slow and easy to interrupt at that size. The CLI
resumes, deduplicates against what is already uploaded, and tells you what it
sent. **Both are comfortably inside Vercel's limits** for a Hobby account, which
are 12,500 files and 100 MB; this deploy is 2,165 files and 25 MB.

### If you prefer connecting the GitHub repo

Do not, without changing something first. `web/tiles/` is gitignored, so a
Git-connected deploy would ship **a map with no imagery at all** and no warning.
Either commit the tiles or add a build step that runs `tools/build_tiles.py`. The
CLI deploy above sends what is on your disk and has no such problem.

---

## What you are dragging

The `web` folder and everything in it. Not the repository root, and not the files
individually, because `web` is what the addresses inside the map are relative to.

```
web/
  index.html          the map itself
  sw.js               makes it work with no signal
  manifest.json       lets people add it to a phone home screen
  vercel.json         tells Vercel how long to cache each thing
  _headers            the same rules for Cloudflare, kept in step
  card.jpg            the picture the Squarespace page links with
  vendor/             Leaflet, the mapping library, kept local on purpose
  tiles/              the satellite imagery, 2,152 files (SEE THE NOTE ABOVE)
  icons/              home screen icons
  data/               Caribbean Guard's hazard annotations
```

Note what is NOT in here. `out/sheets/` holds the printed annotated sheets and is
deliberately outside `web/`: they are unsigned drafts carrying a `SIN FIRMAR`
band, and anything inside `web/` gets published by the act of deploying.

Every path inside the map is relative, so the same folder works at the root of a
domain, at `.vercel.app` and at `.pages.dev` with no edit. That was checked, not
assumed: the service worker registers at `sw.js`, its scope becomes the site
root, and its precache list is relative.

---

## The address

**Preferred:** `mapa.caribbeanguard.org`

**Unconfirmed, and this is a real blocker to check early.** The DNS for
`caribbeanguard.org` is managed at **WordPress.com**, not at Squarespace and not
at Cloudflare. Nobody on this project has said they have that login. Adding the
subdomain requires signing in there and adding one CNAME record that Vercel will
tell you the value of.

If that login cannot be found, **do nothing and use the `.vercel.app` address.**
The map is complete and correct at that address. The only cost is a less
memorable URL, and since the map is reached by scanning a QR code, almost nobody
types it.

**Whichever address is chosen has to be final before the QR codes are printed.**
The codes go on aluminium bolted to posts. That is the least revisable thing this
project will produce, and a redirect is not available if the domain is the part
that changes. Print the human readable URL under every code as well, so a code
that stops scanning is still followable.

### If the WordPress.com login is found

In Vercel, open the project, **Settings**, **Domains**, add
`mapa.caribbeanguard.org`. Vercel shows a CNAME target, usually
`cname.vercel-dns.com`. Add that CNAME at WordPress.com. It usually resolves
within an hour, and the certificate is issued automatically once it does.

---

## After deploying, check these five things

On a phone, not a laptop. Two minutes.

1. **The map draws** and you can see the whole coast on arrival.
2. **Tap a beach.** A panel opens with an instruction, a "Hoy" block, and the
   "Autor / Revisado" lines.
3. **Turn the phone sideways.** The coast should get wider, not disappear.
4. **Open the address with `?z=cocles` on the end.** It should open on Playa
   Cocles. This is the QR code path and it is the one that is expensive to get
   wrong.
5. **Turn on aeroplane mode and reload.** The map should still draw (the coast, not the close zooms), and the bar
   above the beach cards should say when it was saved. If it says "No guardado en
   este teléfono", wait a few seconds with signal on and reload once, then try
   again.

---

## Caching, and the one trap in it

`web/vercel.json` tells Vercel how long browsers may keep each file, and
`web/_headers` says the same for Cloudflare. Both are already correct and need no
editing. **Change them together or not at all.**

The one thing to know: **the tiles are cached for a year and marked immutable,
and a tile's name is its coordinate.** `tiles/15/8850/15500.jpg` keeps that name
forever, whatever imagery is inside it, so rebuilding `web/tiles/` over the same
coordinates is invisible to anyone who has already loaded the map. If the imagery
is ever re-fetched from a different source or a different date, serve it from a
new prefix (`tiles2/`) and change the URL template in `index.html` and the
generated lists in `sw.js`. Deploying alone is not enough.

The map's text and the hazard data are not affected: `index.html` is never
cached, and the annotations revalidate every five minutes.

---

## Why a static host, and why not GitHub Pages

Vercel, Cloudflare Pages and GitHub Pages are all free and all serve static
files. GitHub Pages is the one ruled out: its update procedure is "commit and
push to a repository", which is a handover to somebody who already has a GitHub
account and knows what a branch is.

Vercel is the choice (Daniel, 2026-09-14). Cloudflare Pages remains a fallback
and needs no code change, only the other config file. **The property that matters
in both is that updating is one action, not a workflow**, which is the difference
between a map that gets updated after we leave and one that does not.

---

## Open questions

- **The WordPress.com DNS login.** For AJ. Until it is answered, treat
  `mapa.caribbeanguard.org` as unavailable and plan on `.vercel.app`.
- **Who owns the hosting account?** It should be Caribbean Guard's own email,
  not a personal one belonging to anybody on this project. Small organisations
  lose sites this way: `docs/precedents/01-mapping-tools.md` records a
  conservation nonprofit whose subdomain lapsed and now redirects to gambling
  spam. Create the account under `caribbeanguard.pv@gmail.com`.

---

## Appendix: Cloudflare Pages

Kept as a fallback. The map is host-agnostic, so this still works with no edits:

1. <https://dash.cloudflare.com> → **Workers & Pages** → **Create** → **Pages**
   → **Upload assets**.
2. Name the project `caribbean-guard-map`.
3. Drag the **`web` folder** in.
4. **Deploy site**.

Cloudflare reads `web/_headers`; Vercel reads `web/vercel.json` and ignores
`_headers` entirely. **They carry the same rules and must be edited together.** A
caching rule that exists on one host and not the other is a bug that surfaces
only after a migration, which is the worst moment to discover it.
