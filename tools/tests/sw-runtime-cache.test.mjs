import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const sw = readFileSync(new URL('../../web/sw.js', import.meta.url), 'utf8');
const cacheName = sw.match(/const CACHE = "([^"]+)"/)[1];
const coastalCss = sw.match(/const CRITICAL = \[[\s\S]*?"(coastal\.css[^"\n]*)"/)[1];

class Response {
  constructor(body, {status = 200} = {}) {
    this.body = body;
    this.status = status;
    this.ok = status >= 200 && status < 300;
    this.bodyUsed = false;
  }
  clone() {
    if (this.bodyUsed) throw new TypeError('Body has already been consumed');
    return new Response(this.body, {status: this.status});
  }
  async text() {
    this.bodyUsed = true;
    return this.body;
  }
}

function worker(status, {delayOpen = false, savedAt = '100'} = {}) {
  const listeners = {};
  const saved = new Map(savedAt === null ? [] : [['cg-map-saved-at', savedAt]]);
  const cache = {async put(key, response) { saved.set(key, await response.text()); }};
  runInNewContext(sw, {
    self: {addEventListener(type, handler) { listeners[type] = handler; }},
    location: {origin: 'https://map.test'},
    caches: {
      async match() {},
      async open() {
        if (delayOpen) await new Promise(resolve => setImmediate(resolve));
        return cache;
      }
    },
    fetch: async () => new Response('network body', {status}),
    Response, URL, setTimeout, clearTimeout,
    Date: {now: () => 200}
  });
  return {
    saved,
    async request(path, mode) {
      const request = {
        url: 'https://map.test/' + path,
        method: 'GET', mode, headers: {get: () => ''}
      };
      let result;
      listeners.fetch({request, respondWith(promise) {
        result = promise.then(async response => ({
          status: response.status, body: await response.text()
        }));
      }});
      const response = await result;
      await new Promise(resolve => setImmediate(resolve));
      return {request, response};
    }
  };
}

test('a cache-miss asset is cached even when respondWith consumes its body immediately', async () => {
  const {saved, request} = worker(200, {delayOpen: true});
  const result = await request('tiles/16/1/1.jpg', 'cors');
  assert.equal(result.response.body, 'network body');
  assert.equal(saved.get(result.request), 'network body');
});

test('document fetches never advance the core download timestamp', async () => {
  for (const status of [500, 200]) for (const savedAt of [null, '100']) {
    const {saved, request} = worker(status, {savedAt});
    const result = await request('index.html', 'navigate');
    assert.equal(result.response.status, status);
    assert.equal(saved.get('cg-map-saved-at'), savedAt ?? undefined);
  }
});

function installer(failedPath, oldName = 'cg-map-v71-versioned-bootstrap') {
  const listeners = {}, stores = new Map(), fetched = [];
  const old = new Map([['cg-map-saved-at', '100'], ['index.html', 'old document']]);
  if (oldName !== null) stores.set(oldName, old);
  const keyOf = key => typeof key === 'string' ? key : key.url;
  runInNewContext(sw, {
    self: {
      location: {href: 'https://map.test/sw.js'},
      addEventListener(type, handler) { listeners[type] = handler; },
      clients: {async claim() {}, async matchAll() { return []; }}
    },
    location: {origin: 'https://map.test'},
    caches: {
      async open(name) {
        if (!stores.has(name)) stores.set(name, new Map());
        const saved = stores.get(name);
        return {
          async put(key, response) { saved.set(keyOf(key), await response.text()); },
          async match(key) { const body = saved.get(keyOf(key)); return body === undefined ? undefined : new Response(body); }
        };
      },
      async keys() { return [...stores.keys()]; },
      async delete(name) { return stores.delete(name); }
    },
    Request: class { constructor(url) { this.url = url; } },
    fetch: async req => {
      fetched.push(req.url);
      return new Response('network body', {status: req.url === failedPath ? 404 : 200});
    },
    Response, URL, setTimeout, clearTimeout,
    console: {warn() {}, error() {}},
    Date: {now: () => 200}
  });
  return {
    stores, fetched, old,
    async lifecycle(type) {
      let result;
      listeners[type]({waitUntil(promise) { result = promise; }});
      await result;
    }
  };
}

test('a failed core download refuses install, removes the partial cache and preserves the old saved copy', async () => {
  for (const path of ['data/zones-geometry.json', coastalCss]) {
    const worker = installer(path);
    await assert.rejects(worker.lifecycle('install'));
    assert.deepEqual([...worker.stores.keys()], ['cg-map-v71-versioned-bootstrap']);
    assert.equal(worker.old.get('cg-map-saved-at'), '100');
    assert.equal(worker.old.get('index.html'), 'old document');
  }
});

test('a failed core download with the same cache name preserves the active cache and stamp', async () => {
  const worker = installer('data/zones-geometry.json', cacheName);
  await assert.rejects(worker.lifecycle('install'));
  assert.deepEqual([...worker.stores.keys()], [cacheName]);
  assert.equal(worker.stores.get(cacheName).get('cg-map-saved-at'), '100');
});

test('a failed core download on first install leaves no cache or stamp', async () => {
  const worker = installer('data/zones-geometry.json', null);
  await assert.rejects(worker.lifecycle('install'));
  assert.equal(worker.stores.size, 0);
});

test('a full core download installs and stamps even if an optional download fails', async () => {
  const worker = installer('icons/icon-180.png');
  await worker.lifecycle('install');
  assert.ok(worker.fetched.includes('icons/icon-180.png'));
  const current = [...worker.stores.entries()].find(([name]) => name !== 'cg-map-v71-versioned-bootstrap')[1];
  assert.equal(current.get('cg-map-saved-at'), '200');
  assert.equal(current.get('data/zones-geometry.json'), 'network body');
  await worker.lifecycle('activate');
  assert.equal(worker.stores.has('cg-map-v71-versioned-bootstrap'), false);
});
