# Microtec Engineering – inner pages build

Source for the Home, About, Services and Load Systems pages on https://microteceng.wsdfy.com,
built from the design handoff (`Microtec_Engineering_website_rebuild.zip`).
`backup/home-48-elementor-before.json` is the homepage's Elementor data before the rebuild.

## How it works

1. `scripts/extract.js` renders every design page (`*.dc.html`) in Chromium at the design's
   JavaScript breakpoints (1440 / 1200 / 1050 / 900 / 700 / 620 / 390 px) and serialises the
   content sections (header and footer are left to the site's global UAE templates).
2. `scripts/build.py` turns each element's inline styles into a class, and the differences
   between breakpoints into `max-width` media queries (1239 / 1099 / 999 / 759 / 639 / 599).
   Output: `theme/assets/css/mt-pages.css` and `sections/pages.json` (one HTML block per
   section, with `{{IMG:…}}` placeholders replaced by media-library URLs on upload).
3. Each WordPress page is an Elementor page: one full-width container per design section, each
   holding an HTML widget wrapped in `<div class="mtp">`.

## Theme files (microtec-child)

- `assets/css/mt-pages.css` – all rules scoped to `.mtp`, the wrapper on each built section.
- `assets/js/mt-pages.js` – EWP feature list rotation and the homepage hero slides, category
  arrows, services slider, "Why choose" highlight and industry tiles.
- `functions.php` – enqueues the two files plus Barlow Semi Condensed / Inter on pages.

`images/` holds web-sized copies of the design's local diagrams; Pexels photos are placeholders
(see the handoff README) and are uploaded to the media library straight from Pexels.
