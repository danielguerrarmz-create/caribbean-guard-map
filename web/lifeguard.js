/* Lifeguard post clock. The post keeps Costa Rica hours, so the reader's phone
 * clock is irrelevant: a visitor whose phone is still on New York or Madrid
 * time must get the same answer as a guard standing at the post.
 * Costa Rica is UTC-6 all year (no daylight saving). Intl is used first so the
 * zone lives in one place; the fixed offset is the fallback for an engine
 * without time zone data.
 */
(function (root) {
  'use strict';
  const ZONE = 'America/Costa_Rica';
  let fmt = null;
  try {
    fmt = new Intl.DateTimeFormat('en-US', {timeZone: ZONE, hour: 'numeric', minute: 'numeric', hourCycle: 'h23'});
  } catch (e) { fmt = null; }
  /* Minutes since midnight, Costa Rica time, for a Date or a ms timestamp. */
  function crMinutes(when = Date.now()) {
    const date = when instanceof Date ? when : new Date(when);
    if (fmt) {
      const parts = fmt.formatToParts(date);
      const get = type => Number(parts.find(p => p.type === type)?.value);
      const h = get('hour') % 24, m = get('minute');
      if (Number.isFinite(h) && Number.isFinite(m)) return h * 60 + m;
    }
    const utc = date.getUTCHours() * 60 + date.getUTCMinutes();
    return (utc - 6 * 60 + 1440) % 1440;
  }
  /* On duty from `from`:00 up to, not including, `to`:00 Costa Rica time. */
  function onDuty(post, when = Date.now()) {
    if (!post) return false;
    const m = crMinutes(when);
    return m >= post.from * 60 && m < post.to * 60;
  }
  /* The one instruction rule: a beach that is only for swimming with
     lifeguards reads "do not go in" while its post is closed. Returns the key
     into the copy table (T[lang]) to render. */
  function instructionKey(beachClass, post, when = Date.now()) {
    if (beachClass === 'high-risk' && post && !onDuty(post, when)) return 'offDuty';
    return beachClass;
  }
  root.CGLifeguard = {ZONE, crMinutes, onDuty, instructionKey};
})(typeof globalThis !== 'undefined' ? globalThis : this);
