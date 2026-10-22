const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const S = process.env.S, dir = S + '/zip/microtec-site', out = S + '/render';
const V = S + '/vendor';
const map = {
  'react.production.min.js': V + '/react-18.3.1/umd/react.production.min.js',
  'react-dom.production.min.js': V + '/react-dom-18.3.1/umd/react-dom.production.min.js',
  'babel.min.js': V + '/babel-standalone-7.29.0/babel.min.js',
};
const only = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.dc.html') && !/index|brand-kit|sitemap/.test(f)).filter(f => !only || f.includes(only));
  for (const f of files) {
    for (const w of [1440, 390]) {
      const p = await b.newPage({ viewport: { width: w, height: 900 } });
      await p.route('**/*', r => {
        const u = r.request().url();
        if (u.includes('unpkg.com')) { const k = Object.keys(map).find(k => u.endsWith(k)); return r.fulfill({ path: map[k], contentType: 'application/javascript' }); }
        if (u.startsWith('http://localhost') || u.includes('fonts.g')) return r.continue();
        return r.abort();
      });
      p.on('pageerror', e => console.log('pageerror', f, e.message.slice(0, 200)));
      await p.goto('http://localhost:8765/' + encodeURIComponent(f), { waitUntil: 'load' });
      await p.waitForTimeout(3500);
      const slug = f.replace('.dc.html', '').replace(/[^A-Za-z0-9]+/g, '-') + (w < 500 ? '-m' : '');
      if (w > 500) fs.writeFileSync(path.join(out, slug + '.html'), await p.content());
      await p.screenshot({ path: path.join(out, slug + '.png'), fullPage: true });
      console.log('done', slug, await p.evaluate(() => document.documentElement.scrollHeight));
      await p.close();
    }
  }
  await b.close();
})();
