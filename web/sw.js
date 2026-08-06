/* Caribbean Guard safety map, service worker.
   ============================================================================

   WHY THIS EXISTS
   The map's whole reason to be is working at the water's edge, where there is no
   signal. Across eight verified national public safety map viewers in Latin
   America, not one registers a service worker or ships a manifest. Offline is not
   a standard this project is behind on; it is the gap the whole regional field
   leaves open, on a continent where the people most likely to need a hazard map
   are the ones least likely to have a bar of signal.

   THE PRECACHE LIST IS NOT HAND MAINTAINED AS AN addAll
   MDN, on install: "If the promise is rejected, the installation fails, and the
   worker won't do anything." cache.addAll() is all or nothing and the
   specification makes it reject on any response outside the ok range. So ONE 404
   in a hand-written list silently disables offline support entirely, with nothing
   visible to the user and nothing visible to whoever deployed it. On a map whose
   offline capability is the reason it exists, that failure mode is unacceptable
   as a silent one.

   So: Promise.allSettled over individual cache.put() calls. A missing asset
   degrades one file instead of the whole feature, and what failed is logged and
   reported back to the page.

   THE LIST IS ALSO TIERED
   base.webp is 2.52 MB and it is the deferred detail image. It failing must not
   take down a precache that would otherwise have delivered a working
   overview-resolution map. CRITICAL is what makes the map usable; OPTIONAL is
   what makes it detailed. Install waits only for CRITICAL.

   HTML IS NETWORK FIRST, EVERYTHING ELSE IS CACHE FIRST
   The document carries the safety verdicts. Somebody with signal must get today's
   copy, not a cached one, so index.html races the network with a short timeout and
   falls back to the cache. The imagery, Leaflet and the geojson are content
   addressed by deploy and change rarely, so they are served from cache and
   revalidated in the background.
   ============================================================================ */

const CACHE = "cg-map-v1";
const STAMP = "cg-map-saved-at";     // written into the cache as a fake response

/* Relative, not absolute. The map is served from / in production and from
   /mapa/app/ inside the local site build, and a leading slash would break one of
   the two. The worker's scope already anchors these. */
const CRITICAL = [
  "./",
  "index.html",
  "manifest.json",
  "vendor/leaflet.js",
  "vendor/leaflet.css",
  "img/base-lo.webp",
  "data/cg-hazards.geojson"
];
const OPTIONAL = [
  "img/base.webp",
  "icons/icon-180.png",
  "icons/icon-192.png",
  "icons/icon-512.png"
];

/* One asset, fetched fresh from the network and written on its own, so a failure
   is one missing file rather than a dead feature. cache:"reload" bypasses the
   HTTP cache: a precache built from stale bytes is a stale safety map that
   believes it is current. */
async function put(cache, url){
  const res = await fetch(new Request(url, {cache:"reload"}));
  if(!res.ok) throw new Error(url + " -> " + res.status);
  await cache.put(url, res);
  return url;
}

async function precache(urls){
  const cache = await caches.open(CACHE);
  const results = await Promise.allSettled(urls.map(u => put(cache, u)));
  const failed = results
    .map((r, i) => r.status === "rejected" ? urls[i] : null)
    .filter(Boolean);
  if(failed.length) console.warn("[cg-sw] not cached:", failed);
  return {ok: urls.length - failed.length, failed};
}

/* The timestamp is only written when the WHOLE critical set landed.
   Stamping after a partial precache would put a fresh date on a cache that is
   missing pieces, and the date is the one thing the interface uses to tell
   somebody how old the advice in front of them is. Better for the bar to read
   "not saved" while most of it is there than for it to read "saved just now"
   while the geojson is missing. */
async function stamp(){
  const cache = await caches.open(CACHE);
  await cache.put(STAMP, new Response(String(Date.now())));
}
async function broadcast(msg){
  const clients = await self.clients.matchAll();
  clients.forEach(c => c.postMessage(msg));
}
async function readStamp(){
  const cache = await caches.open(CACHE);
  const r = await cache.match(STAMP);
  return r ? Number(await r.text()) : null;
}

self.addEventListener("install", e=>{
  e.waitUntil((async ()=>{
    const res = await precache(CRITICAL);
    if(res.failed.length === 0) await stamp();
    else console.error("[cg-sw] incomplete precache, not stamping:", res.failed);
    // the detail image is allowed to arrive late and is allowed to fail
    precache(OPTIONAL).catch(()=>{});
  })());
});

self.addEventListener("activate", e=>{
  e.waitUntil((async ()=>{
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
    await broadcast({savedAt: await readStamp()});
  })());
});

const isDoc = req => req.mode === "navigate" ||
                     (req.headers.get("accept") || "").includes("text/html");

/* Race the network, but not forever. On a beach the connection is not down, it is
   slow, and a fetch that hangs for thirty seconds is worse than a cached copy
   served instantly with its date on it. */
function timed(promise, ms){
  return new Promise((resolve, reject)=>{
    const t = setTimeout(()=>reject(new Error("timeout")), ms);
    promise.then(v=>{ clearTimeout(t); resolve(v); },
                 e=>{ clearTimeout(t); reject(e); });
  });
}

self.addEventListener("fetch", e=>{
  const req = e.request;
  if(req.method !== "GET") return;
  const url = new URL(req.url);
  if(url.origin !== location.origin) return;   // tel: and Google Maps links, untouched

  if(isDoc(req)){
    // network first: the document carries the verdicts
    e.respondWith((async ()=>{
      try{
        const res = await timed(fetch(req), 4000);
        const cache = await caches.open(CACHE);
        cache.put("index.html", res.clone());
        stamp();
        return res;
      }catch(err){
        const hit = await caches.match("index.html") || await caches.match("./");
        return hit || Response.error();
      }
    })());
    return;
  }

  // everything else: cache first, revalidate quietly behind it
  e.respondWith((async ()=>{
    const hit = await caches.match(req, {ignoreSearch:false});
    const net = fetch(req).then(res=>{
      if(res.ok) caches.open(CACHE).then(c => c.put(req, res.clone()));
      return res;
    }).catch(()=>null);
    return hit || (await net) || Response.error();
  })());
});

self.addEventListener("message", e=>{
  const d = e.data || {};

  if(d.action === "SKIP_WAITING"){
    self.skipWaiting();
    return;
  }

  if(d.action === "SAVED_AT"){
    readStamp().then(at=>{
      if(e.source) e.source.postMessage({savedAt: at});
    });
    return;
  }

  /* Manual refresh from the saved-copy bar. Re-fetches everything from the
     network and answers on the port the page opened, so the bar can say whether
     it worked instead of silently pretending it did.

     A failed refresh must leave BOTH the cache and the displayed date exactly as
     they were. The first version of this stamped unconditionally and then
     broadcast the new date to every client, so tapping refresh with no signal
     moved the timestamp forward without a single byte having been fetched. That
     is the interface claiming more currency than the data has, which is the one
     rule this whole file exists to keep. */
  if(d.action === "REFRESH"){
    const port = e.ports && e.ports[0];
    (async ()=>{
      const res = await precache(CRITICAL);
      const ok = res.failed.length === 0;
      if(ok){
        await stamp();
        precache(OPTIONAL).catch(()=>{});
      }
      const at = await readStamp();
      if(port) port.postMessage({ok, failed: res.failed, savedAt: at});
      if(ok) await broadcast({savedAt: at});
    })().catch(err=>{
      if(port) port.postMessage({ok:false, error:String(err)});
    });
  }
});
