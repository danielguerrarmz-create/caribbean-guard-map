import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const MODULE = fileURLToPath(new URL('../../web/lifeguard.js', import.meta.url));
const HTML = readFileSync(new URL('../../web/index.html', import.meta.url), 'utf8');
const WORKER = readFileSync(new URL('../../web/sw.js', import.meta.url), 'utf8');
const POST = {from: 9, to: 17};
// Costa Rica is UTC-6 all year, so CR hh:mm on 2026-10-29 is (hh+6):mm UTC.
const cr = (h, m) => Date.UTC(2026, 9, 29, h + 6, m);
const CASES = [
  ['08:59', cr(8, 59), false],
  ['09:00', cr(9, 0), true],
  ['16:49', cr(16, 49), true],
  ['16:59', cr(16, 59), true],
  ['17:00', cr(17, 0), false],
  ['17:05', cr(17, 5), false],
];
const PHONE_ZONES = ['America/New_York', 'Europe/Madrid', 'America/Costa_Rica'];

/* Each phone time zone runs in its own process with TZ set, the way a phone
   with that zone would run the page. The answer must not move. */
function runIn(tz) {
  const script = `
    require(${JSON.stringify(MODULE)});
    const {crMinutes, onDuty, instructionKey} = globalThis.CGLifeguard;
    const post = ${JSON.stringify(POST)};
    const out = ${JSON.stringify(CASES.map(c => c[1]))}.map(t => ({
      local: new Date(t).getHours(), minutes: crMinutes(t), onDuty: onDuty(post, t),
      highRisk: instructionKey('high-risk', post, t), noSwim: instructionKey('no-swim', post, t)}));
    process.stdout.write(JSON.stringify(out));`;
  return JSON.parse(execFileSync(process.execPath, ['-e', script], {env: {...process.env, TZ: tz}}).toString());
}

for (const tz of PHONE_ZONES) {
  test(`post hours follow Costa Rica time on a phone set to ${tz}`, () => {
    const results = runIn(tz);
    CASES.forEach(([label, , expected], i) => {
      const [h, m] = label.split(':').map(Number);
      assert.equal(results[i].minutes, h * 60 + m, `${tz} ${label} CR minutes`);
      assert.equal(results[i].onDuty, expected, `${tz} ${label} on duty`);
      assert.equal(results[i].highRisk, expected ? 'high-risk' : 'offDuty', `${tz} ${label} instruction`);
      assert.equal(results[i].noSwim, 'no-swim', `${tz} ${label} other classes untouched`);
    });
  });
}

test('the phone zones really differ from Costa Rica, so the test can catch the old bug', () => {
  const at = CASES.findIndex(c => c[0] === '16:49');
  const local = Object.fromEntries(PHONE_ZONES.map(tz => [tz, runIn(tz)[at].local]));
  assert.equal(local['America/Costa_Rica'], 16);
  assert.equal(local['America/New_York'], 18);
  assert.equal(local['Europe/Madrid'], 23);
});

test('boundaries: 8:59 and 17:00 are off duty, 9:00 and 16:59 are on duty', async () => {
  await import('../../web/lifeguard.js');
  const {onDuty, instructionKey} = globalThis.CGLifeguard;
  assert.equal(onDuty(POST, cr(8, 59)), false);
  assert.equal(onDuty(POST, cr(9, 0)), true);
  assert.equal(onDuty(POST, cr(16, 59)), true);
  assert.equal(onDuty(POST, cr(17, 0)), false);
  assert.equal(onDuty(null, cr(12, 0)), false);
  assert.equal(instructionKey('high-risk', undefined, cr(20, 0)), 'high-risk', 'no post, no clock claim');
  for (const cls of ['no-swim', 'conditional', 'lower-risk'])
    assert.equal(instructionKey(cls, POST, cr(20, 0)), cls);
});

test('the off duty instruction exists in ES and EN and tells the reader not to go in', () => {
  const strings = [...HTML.matchAll(/offDuty:"([^"]+)"/g)].map(m => m[1]);
  assert.equal(strings.length, 2, 'one ES and one EN offDuty string');
  const [es, en] = strings;
  assert.match(es, /^NO ENTRES\b/);
  assert.match(es, /GUARDAVIDAS/);
  assert.match(en, /^DON'T GO IN\b/);
  assert.match(en, /LIFEGUARDS/);
  for (const s of strings) assert.doesNotMatch(s, /\b(seguro|safe|ok|puede)\b/i);
  const zones = [...HTML.matchAll(/postZone:"([^"]+)"/g)].map(m => m[1]);
  assert.deepEqual(zones, ['(hora local de Costa Rica)', '(Costa Rica local time)']);
});

test('the page renders through the Costa Rica clock and refreshes it', () => {
  assert.match(HTML, /<script src="lifeguard\.js"><\/script>/);
  const hours = HTML.slice(HTML.indexOf('function hoursLine('), HTML.indexOf('function statusCardInner('));
  assert.doesNotMatch(hours, /getHours\(\)/, 'hoursLine must not read the phone clock');
  assert.match(HTML, /setInterval\(\(\)=>\{\s*refreshPostClock\(\)/);
  assert.match(HTML, /visibilitychange',\(\)=>\{\s*if\(!document\.hidden\)\{refreshPostClock\(\)/);
  assert.match(HTML, /<span class="instr">\$\{t\[instructionKey\(z, when\)\]\}<\/span>/);
  assert.match(HTML, /<span class="beach-status">\$\{t\[instructionKey\(z\)\]\}<\/span>/);
  assert.match(WORKER, /"lifeguard\.js",/);
  assert.doesNotMatch(WORKER, /cg-map-v50-aj-rescue-pins/, 'offline cache version bumped');
});

test('the access point sheet shows the same clock-aware instruction as the beach', () => {
  assert.doesNotMatch(HTML, /T\[lang\]\[[\w?.]*character\??\.class\]/, 'no instruction keyed on class alone');
  const access = HTML.slice(HTML.indexOf('function openAccess('), HTML.indexOf('function updateAccessMarkers('));
  assert.match(access, /T\[lang\]\[instructionKey\(beach\)\]/);
  const refresh = HTML.slice(HTML.indexOf('function refreshPostClock('), HTML.indexOf('/* ---------- map ---------- */'));
  assert.match(refresh, /\.access-risk\[data-zone=/, 'an open access sheet is patched when the post flips');
  assert.doesNotMatch(WORKER, /cg-map-v51-lifeguard-cr-time/, 'offline cache version bumped');
});
