import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import * as cheerio from 'cheerio';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export const REPO_ROOT = path.resolve(__dirname, '..', '..');
export const WXR_PATH = path.join(
  REPO_ROOT,
  'docs',
  'source-material',
  'Squarespace-Wordpress-Export-07-17-2026 (1).xml',
);
export const HOME_HTML_PATH = path.join(REPO_ROOT, 'docs', 'source-material', 'cg-home.html');

// Squarespace slugs (wp:post_name) no longer match the current page titles
// (e.g. nuestro-trabajo -> "Historia", involcrate-1 -> "Vision"), so every
// page must be keyed off wp:post_name / <link>, never <title>.
export function loadPages() {
  const xml = readFileSync(WXR_PATH, 'utf8');
  const $ = cheerio.load(xml, { xmlMode: true });

  return $('item')
    .map((_, el) => {
      const $item = $(el);
      return {
        slug: $item.find('wp\\:post_name').text().trim(),
        title: $item.find('title').first().text().trim(),
        link: $item.find('link').first().text().trim(),
        postId: $item.find('wp\\:post_id').text().trim(),
        status: $item.find('wp\\:status').text().trim(),
        contentHtml: $item.find('content\\:encoded').text(),
      };
    })
    .get();
}

export function loadHomeHtml() {
  return readFileSync(HOME_HTML_PATH, 'utf8');
}
