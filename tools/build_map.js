// Copy the offline map intact: Vite's site build targets the separate NGO site.
import { cpSync, existsSync, mkdirSync, readFileSync } from 'node:fs';
import { runInNewContext } from 'node:vm';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';
const root = fileURLToPath(new URL('../', import.meta.url));
const source = resolve(root, 'web');
const target = resolve(root, 'dist-map');
if (!existsSync(resolve(source, 'tiles/11'))) {
  throw new Error('Map tiles are missing. Run tools/build_tiles.py before packaging.');
}
const worker = readFileSync(resolve(source, 'sw.js'), 'utf8');
const boundary = worker.indexOf('async function put(');
if (boundary < 0) throw new Error('Cannot locate service-worker asset declarations.');
const assets = runInNewContext(worker.slice(0, boundary) + '\n[...CRITICAL, ...OPTIONAL]', {}, { timeout: 1000 });
const missing = assets.filter(asset => !existsSync(resolve(source, asset)));
if (missing.length) throw new Error(`Missing offline assets:\n${missing.join('\n')}`);
console.log(`Validated ${assets.length} offline asset references.`);
mkdirSync(target, { recursive: true });
cpSync(source, target, { recursive: true });
console.log(`Map packaged with offline assets: ${target}`);
