"""Collect a small, commit-pinned SVG study. Never download executable packages."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs/design/symbol-study/assets'
SOURCES = {
    'tabler': ('tabler/tabler-icons', 'ed177a085b652fe04ec4f37ced867c94621e7840', 'LICENSE', 'icons/outline/',
        ['current-location', 'compass', 'lifebuoy', 'alert-triangle', 'swimming', 'ripple', 'map-pin', 'info-circle']),
    'phosphor': ('phosphor-icons/core', '2b75f3ad12b420c9504ef05df8d2564a28f8500e', 'LICENSE', 'assets/regular/',
        ['crosshair', 'compass', 'lifebuoy', 'warning', 'person-simple-swim', 'waves', 'map-pin', 'info']),
    'phosphor-duotone': ('phosphor-icons/core', '2b75f3ad12b420c9504ef05df8d2564a28f8500e', 'LICENSE', 'assets/duotone/',
        ['person-simple-swim-duotone', 'prohibit-duotone', 'lifebuoy-duotone', 'warning-duotone', 'waves-duotone', 'question-duotone', 'first-aid-kit-duotone', 'arrow-up-duotone', 'image-duotone', 'map-pin-duotone', 'bed-duotone', 'fork-knife-duotone', 'shopping-bag-duotone', 'flag-duotone', 'road-horizon-duotone', 'path-duotone', 'person-simple-walk-duotone', 'crosshair-duotone', 'timer-duotone', 'thermometer-duotone', 'compass-duotone', 'arrow-clockwise-duotone', 'x-duotone', 'arrow-up-right-duotone', 'caret-right-duotone', 'caret-down-duotone', 'caret-up-duotone', 'user-circle-duotone']),
    'lucide': ('lucide-icons/lucide', '1980e3d59b0fa1a2aeb566d5902b25ee98204001', 'LICENSE', 'icons/',
        ['locate-fixed', 'compass', 'life-buoy', 'triangle-exclamation-point', 'navigation', 'waves-horizontal', 'map-pin', 'info']),
    'maki': ('mapbox/maki', '28e2a3602e4bde033a1dd388e86e9c117b425e34', 'LICENSE.txt', 'icons/',
        ['beach', 'swimming', 'information', 'hospital']),
}

def collect(job):
    family, repo, commit, source, name = job
    url = f'https://raw.githubusercontent.com/{repo}/{commit}/{source}'
    try:
        data = urlopen(Request(url, headers={'User-Agent': 'CaribbeanGuard-design-study'}), timeout=30).read()
    except Exception as error:
        raise RuntimeError(f'Cannot collect {url}: {error}') from error
    if name.endswith('.svg'):
        svg = ET.fromstring(data)
        if svg.tag.split('}')[-1] != 'svg':
            raise ValueError(f'Not SVG: {url}')
        for element in svg.iter():
            if element.tag.split('}')[-1] in ('script', 'foreignObject', 'image', 'use'):
                raise ValueError(f'Unexpected active/external SVG content: {url}')
            if any(k.lower().startswith('on') or k.split('}')[-1] == 'href' for k in element.attrib):
                raise ValueError(f'Unexpected SVG attribute: {url}')
    target = DEST / family / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return {'family': family, 'file': f'{family}/{name}', 'source': url, 'sha256': sha256(data).hexdigest()}

if __name__ == '__main__':
    jobs = []
    for family, (repo, commit, licence, prefix, names) in SOURCES.items():
        jobs.append((family, repo, commit, licence, 'LICENSE.txt'))
        jobs.extend((family, repo, commit, prefix + name + '.svg', name + '.svg') for name in names)
    with ThreadPoolExecutor(max_workers=6) as pool:
        manifest = list(pool.map(collect, jobs))
    (DEST / 'manifest.json').write_text(json.dumps({'date': '2026-11-03', 'status': 'research candidates, unmodified source SVGs', 'assets': manifest}, indent=2) + '\n', encoding='utf-8')
    print(f'Collected {len(manifest)} files with source URLs and SHA-256 hashes.')
