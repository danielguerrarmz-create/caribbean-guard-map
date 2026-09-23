#!/usr/bin/env node
// Downloads every image referenced by the WXR export (plus the logo and
// favicon, which only live in the separately-saved live-homepage HTML dump)
// into a local media/ staging folder, ready to be manually dragged into
// Drive. media/ is gitignored -- this is a one-time pull from Squarespace's
// CDN before the site leaves Squarespace, not something the app reads from.
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { loadPages, loadHomeHtml, REPO_ROOT } from './lib/wxr.mjs';
import { collectImageUrls, assetIdFromUrl, filenameFromUrl } from './lib/media-urls.mjs';

const MEDIA_DIR = path.join(REPO_ROOT, 'media');
const IMAGES_DIR = path.join(MEDIA_DIR, 'images');
const LOGO_DIR = path.join(MEDIA_DIR, 'logo');
const VIDEO_DIR = path.join(MEDIA_DIR, 'video');
const FAVICON_DEST = path.join(REPO_ROOT, 'src', 'app', 'favicon.ico');
const MANIFEST_PATH = path.join(REPO_ROOT, 'scripts', 'out', 'media-manifest.json');

const VIDEO_SITE_ID = '6658cf433f03af778644f50f';
const VIDEO_SYSTEM_DATA_ID = '7abab123-3a68-44e3-b309-4beff323b12c';
const VIDEO_META = {
  durationSeconds: 412.413417,
  variants: '1920:1080,640:360',
  videoCodec: 'h264',
  audioCodec: 'aac',
};

for (const dir of [IMAGES_DIR, LOGO_DIR, VIDEO_DIR]) mkdirSync(dir, { recursive: true });

function sanitizeFilename(name) {
  return decodeURIComponent(name).replace(/[^A-Za-z0-9._-]/g, '-');
}

// Squarespace serves resized variants via ?format=<width>w; ?format=original
// gets the true source file. Not every asset supports that query (e.g. the
// favicon), so fall back to the bare URL if the "original" request 404s.
async function fetchBestQuality(baseUrl) {
  for (const candidate of [`${baseUrl}?format=original`, baseUrl]) {
    const res = await fetch(candidate);
    if (res.ok) return res;
  }
  throw new Error(`all fetch attempts failed for ${baseUrl}`);
}

async function downloadTo(url, destPath) {
  if (existsSync(destPath)) {
    return { status: 'skipped-existing', bytes: 0 };
  }
  const res = await fetchBestQuality(url);
  const buf = Buffer.from(await res.arrayBuffer());
  writeFileSync(destPath, buf);
  return { status: 'downloaded', bytes: buf.length };
}

function relPath(absPath) {
  return path.relative(REPO_ROOT, absPath).split(path.sep).join('/');
}

const manifest = [];
const summary = { downloaded: 0, skipped: 0, failed: 0 };

// --- content images from every page ---
const pages = loadPages();
const allIncluded = new Set();
const allExcluded = new Set();
for (const page of pages) {
  const { included, excluded } = collectImageUrls(page.contentHtml);
  included.forEach((u) => allIncluded.add(u));
  excluded.forEach((u) => allExcluded.add(u));
}

console.log(`found ${allIncluded.size} unique real-site images (${allExcluded.size} excluded, foreign siteId)`);

for (const url of allIncluded) {
  const assetId = assetIdFromUrl(url);
  const filename = sanitizeFilename(filenameFromUrl(url));
  const localPath = path.join(IMAGES_DIR, `${assetId}--${filename}`);
  try {
    const result = await downloadTo(url, localPath);
    summary[result.status === 'downloaded' ? 'downloaded' : 'skipped'] += 1;
    manifest.push({ squarespaceUrl: url, localPath: relPath(localPath), kind: 'image' });
    console.log(`[${result.status}] ${filename}`);
  } catch (err) {
    summary.failed += 1;
    manifest.push({ squarespaceUrl: url, localPath: null, kind: 'image', status: 'failed-404' });
    console.error(`[failed] ${url}: ${err.message}`);
  }
}

// --- logo + favicon, from the saved live-homepage HTML (not the XML) ---
const homeHtml = loadHomeHtml();
const logoMatch = homeHtml.match(/(?:https:)?\/\/static1\.squarespace\.com\/static\/[^\s"']*Logo\.png/);
const faviconMatch = homeHtml.match(/https:\/\/images\.squarespace-cdn\.com\/content\/v1\/[^\s"']*favicon\.ico/);

if (logoMatch) {
  const logoUrl = logoMatch[0].startsWith('//') ? `https:${logoMatch[0]}` : logoMatch[0];
  const localPath = path.join(LOGO_DIR, 'logo.png');
  try {
    const result = await downloadTo(logoUrl.split('?')[0], localPath);
    summary[result.status === 'downloaded' ? 'downloaded' : 'skipped'] += 1;
    manifest.push({ squarespaceUrl: logoUrl.split('?')[0], localPath: relPath(localPath), kind: 'logo' });
    console.log(`[${result.status}] logo.png`);
  } catch (err) {
    summary.failed += 1;
    console.error(`[failed] logo: ${err.message}`);
  }
} else {
  console.error('[failed] could not find Logo.png reference in docs/source-material/cg-home.html');
  summary.failed += 1;
}

if (faviconMatch) {
  const faviconUrl = faviconMatch[0];
  try {
    const result = await downloadTo(faviconUrl, FAVICON_DEST);
    summary[result.status === 'downloaded' ? 'downloaded' : 'skipped'] += 1;
    console.log(`[${result.status}] src/app/favicon.ico (committed, not staged in media/)`);
  } catch (err) {
    summary.failed += 1;
    console.error(`[failed] favicon: ${err.message}`);
  }
} else {
  console.error('[failed] could not find favicon.ico reference in docs/source-material/cg-home.html');
  summary.failed += 1;
}

// --- homepage hero video ---
// Not present anywhere in the static export (Squarespace's native video
// player resolves the segment URLs client-side). It IS reachable as an
// AES-128-encrypted HLS stream at a predictable /playlist.m3u8 path,
// discovered by capturing the real request from a browser Network tab.
// ffmpeg's HLS demuxer handles the decryption + byte-range segments + the
// separate video/audio "programs" transparently -- it just needs
// extension_picky disabled, since the segment URLs have no file extension
// (ffmpeg's default segment-extension allowlist rejects those otherwise).
const videoBase = `https://video.squarespace-cdn.com/content/v1/${VIDEO_SITE_ID}/${VIDEO_SYSTEM_DATA_ID}`;
const videoPlaylistUrl = `${videoBase}/playlist.m3u8`;
const videoLocalPath = path.join(VIDEO_DIR, 'homepage-hero-1920x1080.mp4');
let videoDownloaded = false;

if (existsSync(videoLocalPath)) {
  videoDownloaded = true;
  summary.skipped += 1;
  manifest.push({ squarespaceUrl: videoPlaylistUrl, localPath: relPath(videoLocalPath), kind: 'video' });
  console.log('[skipped-existing] homepage-hero-1920x1080.mp4');
} else {
  try {
    const playlistRes = await fetch(videoPlaylistUrl);
    if (playlistRes.ok) {
      const { execFileSync } = await import('node:child_process');
      execFileSync(
        'ffmpeg',
        ['-y', '-extension_picky', '0', '-i', videoPlaylistUrl, '-map', 'p:1', '-c', 'copy', videoLocalPath],
        { stdio: 'inherit' },
      );
      videoDownloaded = true;
      summary.downloaded += 1;
      manifest.push({ squarespaceUrl: videoPlaylistUrl, localPath: relPath(videoLocalPath), kind: 'video' });
      console.log('[downloaded] homepage-hero-1920x1080.mp4');
    }
  } catch (err) {
    console.error(`[failed] video download via ffmpeg: ${err.message}`);
  }
}

if (!videoDownloaded) {
  manifest.push({
    squarespaceUrl: videoPlaylistUrl,
    localPath: null,
    kind: 'video',
    status: 'manual-download-required',
    meta: VIDEO_META,
  });
  console.log('');
  console.log('[action required] Could not auto-download the homepage hero video --');
  console.log('  Either ffmpeg is not on PATH (winget installs need a fresh shell), or the');
  console.log(`  signed playlist URL has expired: ${videoPlaylistUrl}`);
  console.log('  Re-discover it via browser devtools Network tab (filter "m3u8") while the');
  console.log('  video plays on caribbeanguard.org, then run:');
  console.log('    ffmpeg -extension_picky 0 -i "<playlist-url>" -map p:1 -c copy \\');
  console.log(`      ${relPath(videoLocalPath)}`);
  console.log('');
}

writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2) + '\n', 'utf8');

console.log('---');
console.log(`downloaded: ${summary.downloaded}, skipped (already present): ${summary.skipped}, failed: ${summary.failed}`);
console.log(`wrote ${relPath(MANIFEST_PATH)}`);
