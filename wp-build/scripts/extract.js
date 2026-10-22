// Render each design page at the design's JS breakpoints and dump a serialised tree of the
// content sections (everything with data-screen-label except the header; footer excluded).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs');
const S = process.env.S, V = S + '/vendor';
const map = {
  'react.production.min.js': V + '/react-18.3.1/umd/react.production.min.js',
  'react-dom.production.min.js': V + '/react-dom-18.3.1/umd/react-dom.production.min.js',
  'babel.min.js': V + '/babel-standalone-7.29.0/babel.min.js',
};
const WIDTHS = [1440, 1200, 1050, 900, 700, 620, 390];
const PAGES = {
  about: 'Microtec About.dc.html',
  design: 'Microtec Design Services.dc.html',
  repairs: 'Microtec Electronic Repairs.dc.html',
  ewp: 'Microtec EWP Control Systems.dc.html',
  load: 'Microtec Load Systems.dc.html',
  loader: 'Microtec Load Systems - Loader Weighing.dc.html',
  forklift: 'Microtec Load Systems - Forklift Weighing.dc.html',
  telehandler: 'Microtec Load Systems - Telescopic Handler.dc.html',
  crane: 'Microtec Load Systems - Crane Safety.dc.html',
};
function inPage() {
  const SKIP_ATTR = /^(style|class|data-dc-tpl|style-hover|data-screen-label|on.*)$/;
  function ser(n) {
    if (n.nodeType === 3) return { t: n.nodeValue };
    if (n.nodeType !== 1) return null;
    const tag = n.tagName.toLowerCase();
    if (tag === 'script' || tag === 'style') return null;
    if (n.classList.contains('sc-interp') || tag === 'sc-if' || tag === 'sc-for') {
      return { frag: [...n.childNodes].map(ser).filter(Boolean) };
    }
    const o = { tag, tpl: n.getAttribute('data-dc-tpl'), style: n.getAttribute('style') || '', attrs: {}, hov: [...n.classList].filter(c => /^scp\d+$/.test(c)) };
    if (tag === 'image-slot') {
      o.tag = 'img'; o.slot = true;
      o.attrs = { src: n.getAttribute('src'), alt: n.getAttribute('placeholder') || '' };
      o.kids = [];
      return o;
    }
    for (const a of n.attributes) if (!SKIP_ATTR.test(a.name)) o.attrs[a.name] = a.value;
    if (n.getAttribute('data-screen-label')) o.label = n.getAttribute('data-screen-label');
    o.kids = [...n.childNodes].map(ser).filter(Boolean);
    return o;
  }
  const secs = [...document.querySelectorAll('[data-screen-label]')].filter(e => e.getAttribute('data-screen-label') !== 'Header');
  // hover rules
  const hov = [];
  for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) if (/\.scp\d+/.test(r.cssText)) hov.push(r.cssText); } catch (e) {} }
  return { sections: secs.map(ser), hov };
}
(async () => {
  const b = await chromium.launch();
  const only = process.argv[2];
  for (const [key, f] of Object.entries(PAGES)) {
    if (only && key !== only) continue;
    const out = {};
    for (const w of WIDTHS) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      await p.route('**/*', r => {
        const u = r.request().url();
        if (u.includes('unpkg.com')) { const k = Object.keys(map).find(k => u.endsWith(k)); return r.fulfill({ path: map[k], contentType: 'application/javascript' }); }
        if (u.startsWith('http://localhost') || u.includes('fonts.g')) return r.continue();
        return r.abort();
      });
      await p.goto('http://localhost:8765/' + encodeURIComponent(f), { waitUntil: 'load' });
      await p.waitForTimeout(2500);
      out[w] = await p.evaluate(inPage);
      await p.close();
    }
    fs.writeFileSync(`${S}/extract/${key}.json`, JSON.stringify(out));
    console.log('extracted', key, out[1440].sections.map(s => s.label).join(' | '));
  }
  await b.close();
})();
