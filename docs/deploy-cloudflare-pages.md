# Deploying the safety map

The map is a folder of static files. There is no build step, no server, and
nothing to install. **Deploying is dragging one folder into a web page.** That is
deliberate: the person who has to do this in a year may not be a programmer, and
a deploy nobody can perform is a map that quietly stops being updated.

---

## The short version

1. Go to <https://dash.cloudflare.com> and sign in.
2. **Workers & Pages** in the left menu, then **Create**, then the **Pages** tab,
   then **Upload assets**.
3. Name the project `caribbean-guard-map`.
4. Drag the **`web` folder** from this repository into the upload box.
5. Press **Deploy site**.

That is the whole deploy. It takes about a minute. Cloudflare gives you an
address ending in `.pages.dev`, and the map works there immediately with no
changes to any file.

To publish a change later, repeat steps 1, 2 and 4 on the same project and
Cloudflare replaces the old version. Nothing else has to be touched.

---

## What you are dragging

The `web` folder and everything in it. Do not drag the repository root and do not
drag the files individually, because `web` is what the addresses inside the map
are relative to.

```
web/
  index.html          the map itself
  sw.js               makes it work with no signal
  manifest.json       lets people add it to a phone home screen
  _headers            tells Cloudflare how long to cache each thing
  card.jpg            the picture the Squarespace page links with
  vendor/             Leaflet, the mapping library, kept local on purpose
  img/                the coastline imagery
  icons/              home screen icons
  data/               Caribbean Guard's hazard annotations
```

Every path inside the map is relative, so the same folder works at the root of a
domain and at `.pages.dev` with no edit. That was checked, not assumed: the
service worker registers at `sw.js`, its scope becomes the site root, and its
precache list is relative.

---

## The address

**Preferred:** `mapa.caribbeanguard.org`

**Unconfirmed, and this is a real blocker to check early.** The DNS for
`caribbeanguard.org` is managed at **WordPress.com**, not at Squarespace and not
at Cloudflare. Nobody on this project has said they have that login. Adding the
subdomain requires signing in there and adding one CNAME record that Cloudflare
will tell you the value of.

If that login cannot be found, **do nothing and use the `.pages.dev` address.**
The map is complete and correct at that address. The only cost is a less
memorable URL, and since the map is reached by scanning a QR code, almost nobody
types it.

**Whichever address is chosen has to be final before the QR codes are printed.**
The codes go on aluminium bolted to posts. That is the least revisable thing this
project will produce, and a redirect is not available if the domain is the part
that changes. Print the human readable URL under every code as well, so a code
that stops scanning is still followable.

### If the WordPress.com login is found

In Cloudflare, open the project, **Custom domains**, **Set up a custom domain**,
enter `mapa.caribbeanguard.org`. Cloudflare shows a CNAME target. Add that CNAME
at WordPress.com. It usually resolves within an hour.

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
5. **Turn on aeroplane mode and reload.** The map should still draw, and the bar
   above the beach cards should say when it was saved. If it says "No guardado en
   este teléfono", wait a few seconds with signal on and reload once, then try
   again.

---

## Caching, and the one trap in it

`web/_headers` tells Cloudflare how long browsers may keep each file. It is
already correct and does not need editing.

The one thing to know: **the imagery is cached for a year and marked immutable.**
If the coastline imagery is ever re-exported, deploying is not enough, because
browsers that already hold a copy will not ask again. Rename the file, for
example `base-lo-2.webp`, and update the two places that name it, `index.html`
and the `CRITICAL` list in `sw.js`. The comment in `_headers` says this too.

The map's text and the hazard data are not affected: `index.html` is never
cached, and the annotations revalidate every five minutes.

---

## Why Cloudflare Pages and not GitHub Pages

Both are free and both serve static files. Cloudflare Pages was chosen because it
has a **drag-and-drop upload in a browser**, and GitHub Pages requires a git push.
A handover where the update procedure is "commit and push to a repository" is a
handover to somebody who already has a GitHub account and knows what a branch is.
This one is "drag the folder", which is the difference between a map that gets
updated after we leave and one that does not.

---

## Open questions

- **The WordPress.com DNS login.** For AJ. Until it is answered, treat
  `mapa.caribbeanguard.org` as unavailable and plan on `.pages.dev`.
- **Who owns the Cloudflare account?** It should be Caribbean Guard's own email,
  not a personal one belonging to anybody on this project. Small organisations
  lose sites this way: `docs/precedents/01-mapping-tools.md` records a
  conservation nonprofit whose subdomain lapsed and now redirects to gambling
  spam. Create the account under `caribbeanguard.pv@gmail.com`.
