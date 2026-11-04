import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const sw = readFileSync(new URL('../../web/sw.js', import.meta.url), 'utf8');

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

function worker(status, {delayOpen = false} = {}) {
  const listeners = {};
  const saved = new Map([['cg-map-saved-at', '100']]);
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

test('only a successful document fetch advances the saved timestamp', async () => {
  for (const status of [500, 200]) {
    const {saved, request} = worker(status);
    const result = await request('index.html', 'navigate');
    assert.equal(result.response.status, status);
    assert.equal(saved.get('cg-map-saved-at'), status === 200 ? '200' : '100');
  }
});
