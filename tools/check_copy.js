#!/usr/bin/env node
/* check_copy.js -- the copy rules of web/index.html, as a test.
 *
 * Node, no dependencies, no browser. Run it before any commit that touches the
 * map's words:
 *
 *     node tools/check_copy.js
 *
 * Exits 0 when everything passes and non-zero on the first category that fails,
 * printing every failure rather than stopping at one.
 *
 * WHY THIS FILE EXISTS
 * Three of the defects the 2026-09-17 user study found were single words. A
 * Rioplatense verb nobody in Limón says. A peninsular noun for a bulletin. Two
 * different Spanish names for the current that kills people on this coast. None
 * of them is a bug a browser can fail on, none shows up in a screenshot, and
 * every one of them told a local reader that this map was written somewhere
 * else. They were fixed by hand and there is nothing stopping the next edit
 * putting them back.
 *
 * WHY IT STRIPS COMMENTS FIRST
 * index.html carries about twelve hundred lines of design commentary and that
 * commentary has to be able to NAME the words it is banning, or the reason for
 * the rule cannot be written down next to the rule. So the checker reads what
 * ships to a reader: HTML comments, block comments and line comments come out,
 * and what is left is the live copy.
 */

/* ES MODULE, not CommonJS, because the repo's package.json sets
   "type": "module" and a .js file there is parsed as one. Written as an import
   rather than renamed to .cjs so the filename stays the one the release check
   asks for. No dependencies either way. */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FILE = path.join(HERE, "..", "web", "index.html");

/* ------------------------------------------------------------------ helpers */

/* Comments out, live copy left. The line-comment rule deliberately refuses to
   fire on "https://", which is the one place a double slash appears inside a
   live string in this file. */
function stripComments(src) {
  let out = src.replace(/<!--[\s\S]*?-->/g, " ");
  out = out.replace(/\/\*[\s\S]*?\*\//g, " ");
  out = out.replace(/(^|[^:"'`\\])\/\/[^\n]*/g, "$1");
  return out;
}

/* Reports the 1-based line a character offset falls on, so a failure names a
   place to go rather than a string to search for. */
function lineOf(src, index) {
  return src.slice(0, index).split("\n").length;
}

const failures = [];
function fail(category, message) {
  failures.push({ category, message });
}

const src = fs.readFileSync(FILE, "utf8");
const live = stripComments(src);

/* ------------------------------------------------- 1. banned in live copy */

/* Every one of these is a real finding from the study, not a style preference.
   - retorno / salvamento: the association's own legend says resaca and Estación
     de Rescate. Two names for one thing reads as two things.
   - relevar / relevamiento: Rioplatense, and to a guard on duty it means being
     relieved at the end of a shift.
   - "parte hoy": peninsular. On this coast a bulletin is a reporte.
   - "600 m": the rescue post that was not there, which pointed a family walking
     for help at a live coral reef.
   - bañado: a marsh. The word for swimming here is baño.
   - en dash and em dash: house style, and they do not exist in the latin subset
     this page self-hosts, so they render as tofu on a phone with no fallback. */
const BANNED = [
  { needle: "retorno",      why: "use 'corriente de resaca'" },
  { needle: "salvamento",   why: "use 'Estación de Rescate'" },
  { needle: "relevar",      why: "use 'recorrer'" },
  { needle: "relevamiento", why: "use 'tramo recorrido'" },
  { needle: "parte hoy",    why: "use 'reporte'" },
  { needle: "600 m",        why: "the rescue post 600 m east does not exist" },
  { needle: "bañado",       why: "a marsh; the word is 'baño'" },
  { needle: "\u2013", why: "en dash: not in the font subset, and house style" },
  { needle: "\u2014", why: "em dash: not in the font subset, and house style" }
];

for (const rule of BANNED) {
  let at = live.indexOf(rule.needle);
  while (at !== -1) {
    const label = rule.needle === "\u2013" ? "U+2013"
                : rule.needle === "\u2014" ? "U+2014"
                : `"${rule.needle}"`;
    fail("banned word",
      `${label} in live copy at line ${lineOf(live, at)} -- ${rule.why}`);
    at = live.indexOf(rule.needle, at + 1);
  }
}

/* ------------------------------------------- 2. the eight tier labels */

/* THE RULE THIS ENFORCES IS THE PRODUCT.
   Every level name is an INSTRUCTION, never a rating and never permission. The
   lowest tier used to read SE PUEDE NADAR / SWIMMING OK, which is a stronger
   claim than the United States' national rip current forecast is willing to
   make, on imagery uncertain to 75 m, about beaches no guard has reviewed.
   Nobody may quietly soften these back into a scale or into a yes. */
const CLASSES = ["no-swim", "high-risk", "conditional", "lower-risk"];
const PERMISSION = ["seguro", "safe", "ok", "puede"];

const labels = [];
for (const cls of CLASSES) {
  const re = new RegExp('"' + cls + '"\\s*:\\s*"([^"]+)"', "g");
  let m;
  while ((m = re.exec(live)) !== null) labels.push({ cls, text: m[1] });
}

if (labels.length !== 8) {
  fail("tier labels",
    `expected 8 tier labels (4 classes x 2 languages), found ${labels.length}. ` +
    "A renamed class or a changed quoting style will do this, and a label this " +
    "checker cannot see is a label it cannot check.");
}

for (const label of labels) {
  const hay = label.text.toLowerCase();
  for (const word of PERMISSION) {
    /* Word boundaries, so "OK" does not fire on a word that contains those two
       letters and "puede" does not fire on "pueden" being part of a longer
       instruction that still grants nothing. */
    if (new RegExp("\\b" + word + "\\b").test(hay)) {
      fail("tier labels",
        `${label.cls} reads "${label.text}" and contains "${word}". ` +
        "A level name is an instruction, never permission.");
    }
  }
}

/* ------------------------------------------------- 3. the deferral sentence */

/* "If there is a lifeguard or a flag on the beach, that beats this map."
   It renders under EVERY level and in every sheet, not only the calm ones. It
   is the sentence that still works when this map is wrong, which is the whole
   reason it is allowed to be published at all, and it is the one hat 5 said he
   would want read aloud in an inquiry. A sheet that omits it is a sheet that
   claims to be the last word. */
const SHEETS = ["openZone", "openVoid", "openPost", "openAnnot", "openLegend"];

/* A renderer may satisfy this DIRECTLY, by interpolating t.defer itself, or
   INDIRECTLY, by calling trustLine(), which is the one line the beach sheet was
   cut down to on 2026-09-17 and which carries the sentence word for word.

   The indirect route is only allowed because trustLine() is checked separately,
   immediately below, and by the same regex. Without that second check this
   would be a hole exactly the size of the rule: "openZone calls a function
   named trustLine" is not evidence that anything renders the sentence. Any
   future helper takes the same deal -- add it here AND check its body. */
function rendersDefer(body) {
  return /\bt\.defer\b|\bT\[lang\]\.defer\b/.test(body);
}

/* ANCHORED ON THE WHOLE NAME, not on a prefix. `live.indexOf("function " +
   name)` was the version this had, and it matched "function trustLineX" when
   asked for trustLine: a mutation that renamed the definition and left the call
   site pointing at nothing still passed, because the checker found the renamed
   function and read the sentence out of it. A check that cannot go red on the
   fault it exists for is not a check. The boundary is `(`, optionally spaced. */
function bodyOf(name) {
  const at = new RegExp("function\\s+" + name + "\\s*\\(").exec(live);
  if (!at) return null;
  const start = at.index;
  /* To the next top-level function, which is where this file's sheet renderers
     end. Good enough to scope one function without parsing JavaScript. */
  const next = live.indexOf("\nfunction ", start + 1);
  return live.slice(start, next === -1 ? live.length : next);
}

const trust = bodyOf("trustLine");
if (trust === null) {
  fail("deferral",
    "trustLine() not found. The beach sheet delegates the deferral sentence to " +
    "it; if it was renamed this checker has to be told.");
} else if (!rendersDefer(trust)) {
  fail("deferral", "trustLine() does not render the deferral sentence.");
}

for (const name of SHEETS) {
  const body = bodyOf(name);
  if (body === null) {
    fail("deferral",
      `${name}() not found. It was renamed or removed; this checker has to be ` +
      "told, because a sheet it cannot find is a sheet it cannot check.");
    continue;
  }
  if (!rendersDefer(body) && !(trust !== null && /\btrustLine\s*\(/.test(body))) {
    fail("deferral", `${name}() does not render the deferral sentence.`);
  }
}

/* ------------------------------------------------------------------ report */

const CATEGORIES = ["banned word", "tier labels", "deferral"];

if (failures.length === 0) {
  console.log("check_copy: PASS");
  console.log("  banned words   0 in live copy (9 rules)");
  console.log(`  tier labels    ${labels.length} checked, none grants permission`);
  console.log(`  deferral       present in all ${SHEETS.length} sheet renderers`);
  process.exit(0);
}

console.error("check_copy: FAIL");
for (const category of CATEGORIES) {
  const hits = failures.filter(f => f.category === category);
  if (!hits.length) continue;
  console.error(`\n  ${category} (${hits.length}):`);
  for (const hit of hits) console.error(`    ${hit.message}`);
}
console.error(`\n${failures.length} failure(s). Nothing was changed.`);
process.exit(1);
