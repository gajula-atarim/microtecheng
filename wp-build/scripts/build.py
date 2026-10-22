"""Turn the extracted design trees into WordPress-ready HTML sections + one stylesheet.

Inline styles from each breakpoint render become a class per element; differences between
breakpoints become max-width media queries (desktop first, matching the design's JS breakpoints).
"""
import sys, json, re, html, hashlib, os
sys.path.insert(0, sys.argv[1] + '/scripts')
from common import load
S, OUT = sys.argv[1], sys.argv[2]

WIDTHS = ['1440', '1200', '1050', '900', '700', '620', '390']
MQ = [None, 1239, 1099, 999, 759, 639, 599]
PAGES = 'about design repairs ewp load loader forklift telehandler crane'.split()

LINKS = {
    'Microtec Home v4.dc.html': '/',
    'Microtec Home v4.dc.html#enquiry': '/#enquiry',
    'Microtec Home v4.dc.html#services': '/#services',
    'Microtec Load Systems.dc.html': '/services/load-systems/',
    'Microtec Load Systems - Loader Weighing.dc.html': '/services/load-systems/loader-excavator-weighing/',
    'Microtec Load Systems - Forklift Weighing.dc.html': '/services/load-systems/forklift-weighing/',
    'Microtec Load Systems - Telescopic Handler.dc.html': '/services/load-systems/telescopic-handler/',
    'Microtec Load Systems - Crane Safety.dc.html': '/services/load-systems/crane-safety-systems/',
}
P = '.mtp.mtp.mtp'  # (0,3,0): stays above Elementor kit / theme selectors
VOID = {'img', 'br', 'input', 'hr'}

def split_style(s):
    out, buf, depth, q = [], '', 0, None
    for ch in s:
        if q:
            buf += ch
            if ch == q: q = None
            continue
        if ch in '"\'': q = ch
        elif ch == '(': depth += 1
        elif ch == ')': depth -= 1
        if ch == ';' and depth == 0:
            out.append(buf); buf = ''
        else:
            buf += ch
    out.append(buf)
    d = {}
    for decl in out:
        if ':' not in decl: continue
        k, v = decl.split(':', 1)
        k, v = k.strip(), v.strip()
        if k: d[k] = v
    return d

def decls(d):
    return '; '.join(f'{k}: {v}' for k, v in d.items())

classes = {}      # signature -> class name
css_blocks = []   # (classname, [dict per level])
hover_cls = {}    # rule body -> class
hover_css = []
missing_fs = []
slot_classes = set()  # classes on images that replace the design's <image-slot>

def cls_for(levels):
    sig = json.dumps(levels, sort_keys=True)
    if sig not in classes:
        name = 'm' + hashlib.md5(sig.encode()).hexdigest()[:6]
        classes[sig] = name
        css_blocks.append((name, levels))
    return classes[sig]

def level_css(name, levels, scope='.mtp .'):
    """Return {mq: decl-string} for one class."""
    res = {None: decls(levels[0])} if levels[0] else {}
    for i in range(1, len(levels)):
        prev, cur = levels[i - 1], levels[i]
        diff = {k: v for k, v in cur.items() if prev.get(k) != v}
        for k in prev:
            if k not in cur: diff[k] = 'revert'
        if diff: res[MQ[i]] = decls(diff)
    return res

def build(key):
    d = load(S, key)
    hov_rules = {}
    for r in d['1440']['hov']:
        m = re.match(r'\.(scp\d+):hover \{ (.*) \}', r)
        body = m.group(2)
        if body not in hover_cls:
            hover_cls[body] = f'mh{len(hover_cls)}'
            hover_css.append(f'{P} .{hover_cls[body]}:hover {{ {body} }}')
        hov_rules[m.group(1)] = hover_cls[body]
    trees = [d[w]['sections'] for w in WIDTHS]
    out = []

    def emit(nodes, ewp_item=None):
        # nodes: same element at each width
        n0 = nodes[0]
        if 't' in n0:
            return html.escape(n0['t'], quote=False)
        tag = n0['tag']
        levels = [split_style(n['style']) for n in nodes]
        extra = []
        if n0.get('slot'):
            levels = [{'display': 'block', 'width': '100%', 'height': '100%', 'object-fit': 'cover', **l} for l in levels]
        if tag in ('h1', 'h2', 'h3', 'h4', 'p') and 'font-size' not in levels[0]:
            missing_fs.append((key, tag, n0['tpl']))
        if ewp_item is not None and n0['tpl'] in EWP_TPLS:
            # cycle list: base = inactive item, .is-active = active item
            inactive = [split_style(x['style']) for x in ewp_item['inactive'][n0['tpl']]]
            active = [split_style(x['style']) for x in ewp_item['active'][n0['tpl']]]
            name = 'mtp-ewp-' + n0['tpl']
            ewp_css.append((name, inactive, active))
            extra.append(name)
        elif any(levels):
            extra.append(cls_for(levels))
            if n0.get('slot'):
                slot_classes.add(extra[-1])
        for h in n0['hov']:
            extra.append(hov_rules[h])
        attrs = dict(n0['attrs'])
        if 'href' in attrs:
            attrs['href'] = LINKS.get(attrs['href'], attrs['href'])
        if tag == 'img':
            attrs['src'] = '{{IMG:' + attrs['src'] + '}}'
            attrs.setdefault('alt', '')
            attrs['loading'] = 'lazy'
        if n0.get('label', '').startswith('01'):
            extra.append('mtp-hero')
        if ewp_item is not None and n0['tpl'] == EWP_ITEM_TPL:
            extra.append('mtp-ewp-item')
        if ewp_item is not None and n0['tpl'] == EWP_LIST_TPL:
            extra.append('mtp-ewp-list')
        a = ''.join(f' {k}="{html.escape(v)}"' for k, v in attrs.items())
        c = f' class="{" ".join(extra)}"' if extra else ''
        if tag in VOID:
            return f'<{tag}{c}{a}>'
        inner = ''.join(emit([n['kids'][i] for n in nodes], ewp_item) for i in range(len(n0['kids'])))
        return f'<{tag}{c}{a}>{inner}</{tag}>'

    for si in range(len(trees[0])):
        nodes = [t[si] for t in trees]
        ewp_item = None
        if key == 'ewp' and nodes[0].get('label') == '02 EWP':
            ewp_item = ewp_states(nodes)
        out.append({'label': nodes[0].get('label'), 'html': emit(nodes, ewp_item)})
    return out

# --- EWP feature list (tpl 213 list, 215 item) -------------------------------------------
EWP_LIST_TPL, EWP_ITEM_TPL = '213', '215'
EWP_TPLS = {'215', '216', '217', '224'}
ewp_css = []
def find(n, tpl):
    if 't' in n: return None
    if n['tpl'] == tpl: return n
    for k in n['kids']:
        r = find(k, tpl)
        if r: return r
def ewp_states(nodes):
    act, inact = {}, {}
    for t in EWP_TPLS: act[t] = []; inact[t] = []
    for n in nodes:
        lst = find(n, EWP_LIST_TPL)
        items = [k for k in lst['kids'] if 't' not in k]
        ai = next(i for i, it in enumerate(items) if 'width: 100%' in find(it, '216')['style'])
        ii = next(i for i in range(len(items)) if i != ai)
        def grab(item, store):
            stack = [item]
            while stack:
                x = stack.pop()
                if 't' in x: continue
                if x['tpl'] in EWP_TPLS: store[x['tpl']].append(x)
                stack.extend(x['kids'])
        grab(items[ai], act); grab(items[ii], inact)
    return {'active': act, 'inactive': inact}

pages = {k: build(k) for k in PAGES}

# --- CSS -----------------------------------------------------------------------------------
by_mq = {m: [] for m in MQ}
for name, levels in css_blocks:
    for mq, body in level_css(name, levels).items():
        by_mq[mq].append(f'{P} .{name} {{ {body} }}')
for name, inactive, active in ewp_css:
    for mq, body in level_css(name, inactive).items():
        by_mq[mq].append(f'{P} .{name} {{ {body} }}')
    for mq, body in level_css(name, active).items():
        by_mq[mq].append(f'{P} .mtp-ewp-item.is-active .{name}, {P} .mtp-ewp-item.is-active.{name} {{ {body} }}')

css = [open(S + '/scripts/base.css').read()]
for mq in MQ:
    rules = list(dict.fromkeys(by_mq[mq]))
    if not rules: continue
    if mq is None: css += rules
    else: css.append(f'@media (max-width: {mq}px) {{\n  ' + '\n  '.join(rules) + '\n}')
# image-slot frames are absolutely positioned, so the image never sizes its box
css.append(f"{P} :is({', '.join('.' + c for c in sorted(slot_classes))}) {{ contain: size; }}")
css.append('/* Hover states from the design */')
css += hover_css
os.makedirs(OUT, exist_ok=True)
open(OUT + '/mt-pages.css', 'w').write('\n'.join(css) + '\n')
json.dump(pages, open(OUT + '/pages.json', 'w'), indent=1)
print('classes', len(css_blocks), 'hover', len(hover_css), 'css bytes', sum(map(len, css)))
print('headings/p without font-size:', missing_fs[:20], len(missing_fs))
