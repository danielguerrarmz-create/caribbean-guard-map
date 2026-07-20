import * as cheerio from 'cheerio';

// Maps Squarespace's data-section-theme value to the theme classes defined
// in src/app/globals.css during step 1 (theme-white/theme-light/theme-black/theme-bright).
// Squarespace leaves the attribute blank for its default/light theme.
function normalizeTheme(theme) {
  const t = (theme || '').trim();
  if (t === '') return 'light';
  return t;
}

function textOf($, el) {
  return $(el).text().trim();
}

function parseJsonAttr($, el, attr) {
  const raw = $(el).attr(attr);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function extractRichText($, $section) {
  return $section
    .find('.sqs-html-content')
    .map((_, el) => ($(el).html() || '').trim())
    .get()
    .filter(Boolean);
}

function extractStandaloneImages($, $section) {
  // Images that belong to a gallery-grid or user-items-list are handled by
  // those extractors separately; skip them here to avoid double-counting.
  return $section
    .find('.image-block img')
    .filter((_, el) => $(el).closest('.gallery-grid, .user-items-list').length === 0)
    .map((_, el) => ({ url: $(el).attr('src') || $(el).attr('data-image') || '', alt: $(el).attr('alt') || '' }))
    .get()
    .filter((img) => img.url);
}

function extractButtons($, $section) {
  return $section
    .find('.button-block')
    .map((_, el) => {
      const $a = $(el).find('a').first();
      const text = textOf($, $a);
      const link = $a.attr('href') || '';
      return { text, link, needsManualContent: !text && !link };
    })
    .get();
}

function normalizeUserItem(item) {
  const button = item.button || {};
  return {
    title: item.title || '',
    descriptionHtml: item.description || '',
    button: {
      text: button.buttonText || '',
      link: button.buttonLink || '',
    },
    image: item.image
      ? {
          url: item.image.assetUrl || '',
          filename: item.image.filename || '',
          originalSize: item.image.originalSize || '',
        }
      : null,
  };
}

function extractUserItemsList($, $section) {
  const $container = $section.find('.user-items-list-item-container').first();
  if ($container.length === 0) return null;

  const context = parseJsonAttr($, $container.get(0), 'data-current-context');
  if (!context) return null;

  return {
    layout: context.layout || '',
    sectionTitle: context.sectionTitle || '',
    sectionButton: context.isSectionButtonEnabled
      ? { text: context.sectionButton?.buttonText || '', link: context.sectionButton?.buttonLink || '' }
      : null,
    items: (context.userItems || []).map(normalizeUserItem),
  };
}

function extractGalleryGrid($, $section) {
  const items = $section
    .find('figure.gallery-grid-item img')
    .map((_, el) => ({ url: $(el).attr('src') || $(el).attr('data-image') || '', alt: $(el).attr('alt') || '' }))
    .get()
    .filter((img) => img.url);
  return items.length > 0 ? items : null;
}

function extractMarquee($, $section) {
  const $marquee = $section.find('.marquee-block, .sqs-block-marquee').first();
  if ($marquee.length === 0) return null;
  const text = ($marquee.find('.sqs-block-content').html() || '').trim();
  return { text, needsManualContent: !text };
}

function extractAccordion($, $section) {
  const $items = $section.find('.accordion-block li');
  if ($items.length === 0) return null;
  return $items
    .map((_, li) => {
      const name = textOf($, $(li).find('[data-sqsp-accordion-block-item-title] span').first());
      const bioHtml = ($(li).find('[data-sqsp-accordion-block-item-description]').first().html() || '').trim();
      return { name, bioHtml };
    })
    .get()
    .filter((entry) => entry.name);
}

// Squarespace uses two competing section-layout systems: the classic
// "page-section" (nested .content div, no data-fluid-engine) and the newer
// "fluid-engine" free-form grid (data-fluid-engine="true", CSS Grid
// .fe-block-<id> cells). Both are walked the same way here since every
// block type we care about is found via class-based selectors that work
// regardless of which grid system wraps them.
export function extractSections(contentHtml) {
  const $ = cheerio.load(contentHtml);

  return $('section[data-test="page-section"]')
    .map((_, el) => {
      const $section = $(el);
      const isFluidEngine = $section.find('[data-fluid-engine="true"]').length > 0;

      return {
        sectionId: $section.attr('data-section-id') || '',
        theme: normalizeTheme($section.attr('data-section-theme')),
        layoutKind: isFluidEngine ? 'fluid-engine' : 'page-section',
        richText: extractRichText($, $section),
        images: extractStandaloneImages($, $section),
        buttons: extractButtons($, $section),
        userItemsList: extractUserItemsList($, $section),
        galleryGrid: extractGalleryGrid($, $section),
        marquee: extractMarquee($, $section),
        accordion: extractAccordion($, $section),
      };
    })
    .get();
}

// The client typed a handful of names slightly differently between the two
// widgets (missing accent, trailing period), e.g. "Melissa Gonzalez" vs
// "Melissa González", "Hershell Lewis" vs "Hershell Lewis." -- normalize
// aggressively for MATCHING only so those don't come out as duplicate people.
function normalizeNameKey(name) {
  return name
    .trim()
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/["'.,“”‘’]/g, '')
    .replace(/\s+/g, ' ');
}

// Team page merges two structures for the same person: the user-items-list
// carousel gives {name, role, photo}; a separate accordion block gives the
// full bio. Join by normalized-name match since that's the only shared key
// between the two structures.
export function mergeTeamMembers(sections) {
  const roster = new Map();

  for (const section of sections) {
    for (const item of section.userItemsList?.items || []) {
      const key = normalizeNameKey(item.title);
      if (!key) continue;
      roster.set(key, {
        name: item.title.trim(),
        role: item.descriptionHtml,
        photoUrl: item.image?.url || '',
        bioHtml: '',
      });
    }
    for (const entry of section.accordion || []) {
      const key = normalizeNameKey(entry.name);
      if (!key) continue;
      const existing = roster.get(key) || { name: entry.name.trim(), role: '', photoUrl: '', bioHtml: '' };
      existing.bioHtml = entry.bioHtml;
      roster.set(key, existing);
    }
  }

  return [...roster.values()];
}
