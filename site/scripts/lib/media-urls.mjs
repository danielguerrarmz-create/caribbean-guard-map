// Most images live under siteId 6658cf433f03af778644f50f (the real site).
// A couple of images resolve under a different siteId (631899055f241153091de64b)
// -- leftover/foreign stock assets baked into the export -- and are excluded.
const REAL_SITE_ID = '6658cf433f03af778644f50f';
const URL_PATTERN = /https:\/\/images\.squarespace-cdn\.com\/content\/v1\/([a-zA-Z0-9]+)\/[^\s"'<>&]+/g;

// content:encoded CDATA carries embedded JSON (data-current-context, etc)
// pre-encoded with HTML entities (&quot;, &amp;, ...) even before any HTML
// parser touches it. Decode defensively so URL matches never end up with a
// dangling "&quot;" tail, regardless of whether the caller already ran the
// string through an HTML parser.
function decodeEntities(str) {
  return str
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}

// Scans a blob of HTML/CDATA text for every CDN image URL, whether it
// appears in a plain <img src>/srcset or inside an embedded JSON attribute
// (data-current-context, data-props, etc). Query params (?format=...) are
// stripped and results deduped, so repeated srcset variants of the same
// asset collapse to one entry.
export function collectImageUrls(rawHtml) {
  const html = decodeEntities(rawHtml);
  const included = new Set();
  const excluded = new Set();

  for (const match of html.matchAll(URL_PATTERN)) {
    const [full, siteId] = match;
    const base = full.split('?')[0];
    if (siteId === REAL_SITE_ID) {
      included.add(base);
    } else {
      excluded.add(base);
    }
  }

  return { included: [...included], excluded: [...excluded] };
}

export function assetIdFromUrl(url) {
  // .../content/v1/<siteId>/<assetId>/<filename>
  const parts = url.split('/');
  return parts[parts.length - 2];
}

export function filenameFromUrl(url) {
  const parts = url.split('/');
  return decodeURIComponent(parts[parts.length - 1]);
}
