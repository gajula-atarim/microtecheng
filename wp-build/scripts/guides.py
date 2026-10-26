"""Builds the Technical / Installation Guides pages from the "Microtec Technical Guides" design,
using Elementor's own widgets (containers, Heading, Text Editor, Image, Icon List, Button), so
every title, list item and PDF link can be edited in Elementor. The look comes from the
theme's assets/css/mt-guides.css, keyed on the CSS classes set here.

    python3 guides.py   ->  sections/guides.json  {page key: {title, slug, elements}}
"""

import hashlib, json, os, re
from guides_data import (PRE, POST_LIGHTS, POST_CRANES, POST_MISC, TADANO, BRONTO_INTRO,
                         BRONTO_BEFORE, BRONTO_PHASES)

U = 'https://microteceng.wsdfy.com/wp-content/uploads/2026/10/'
# PDFs that the old site links to but no longer serves: listed without a download link.
MISSING = {'Microtec Light Activation Box overview (Theiss).pdf',
           'MkII Connections to Microtec Standard Globe Tower Light.pdf'}

HERO_IMG = {'id': 755, 'url': U + 'led-warning-light-hero.jpg'}
POST_IMG = {'id': 967, 'url': U + 'led-tower-light-post-hero.jpg'}
TADANO_IMG = {'id': 641, 'url': U + 'tadano-exchange-load-cell-a.jpg'}
BRONTO_IMG = {'id': 668, 'url': U + 'bronto-skylift-screen-overlay-3.jpg'}

GUIDES = '/guides/'
PAGES = {
    'pre': ('Pre 01/09/11 Ext Lights & LCM', 'pre-01-09-11-ext-lights-lcm'),
    'post': ('Post 01/09/11 Ext Lights & LCM', 'post-01-09-11-ext-lights-lcm'),
    'tadano': ('Tadano Cranes Tech Information', 'tadano-cranes-tech-information'),
    'bronto': ('Bronto LCD Display Keypad Overlay Replacement', 'bronto-lcd-display-keypad-overlay-replacement'),
}


def pdf_url(f):
    return U + 'guide-' + re.sub(r'[^a-z0-9]+', '-', f[:-4].lower()).strip('-') + '.pdf'


class Ids:
    """Stable element ids, so rebuilding a page keeps the same ids."""
    def __init__(self, key):
        self.key, self.n = key, 0

    def __call__(self):
        self.n += 1
        return hashlib.md5(f'{self.key}/{self.n}'.encode()).hexdigest()[:7]


def con(ids, cls, children, direction='column', width='full', **extra):
    # Spacing (padding, gap) comes from mt-guides.css, keyed on the class.
    s = {'content_width': width, 'flex_direction': direction, 'css_classes': cls}
    s.update(extra)
    return {'id': ids(), 'elType': 'container', 'isInner': False, 'settings': s, 'elements': children}


def w(ids, kind, cls, **settings):
    settings['_css_classes'] = cls
    return {'id': ids(), 'elType': 'widget', 'widgetType': kind, 'settings': settings, 'elements': []}


def heading(ids, cls, text, tag='h2', link=None):
    s = {'title': text, 'header_size': tag}
    if link:
        s['link'] = {'url': link, 'is_external': '', 'nofollow': ''}
    return w(ids, 'heading', cls, **s)


def text(ids, cls, html):
    return w(ids, 'text-editor', cls, editor=html)


def doc_list(ids, docs):
    items = []
    for label, f in docs:
        item = {'_id': ids(), 'text': label,
                'selected_icon': {'value': 'far fa-file-alt', 'library': 'fa-regular'}}
        if f in MISSING:
            item['text'] = label + ' (contact us for a copy)'
        else:
            item['link'] = {'url': pdf_url(f), 'is_external': 'on', 'nofollow': ''}
        items.append(item)
    return w(ids, 'icon-list', 'mtg-docs', icon_list=items, view='traditional')


def hero(ids, title, intro, img, caption, crumbs):
    trail = ''.join(f'<a href="{u}">{t}</a><span>/</span>' for t, u in crumbs)
    left = con(ids, 'mtg-hero-text', [
        text(ids, 'mtg-crumbs', f'<p>{trail}<strong>{title}</strong></p>'),
        heading(ids, 'mtg-title', title, 'h1'),
        text(ids, 'mtg-intro', f'<p>{intro}</p>'),
    ])
    right = con(ids, 'mtg-hero-media', [
        w(ids, 'image', 'mtg-hero-img', image=img, image_size='full', caption_source='custom', caption=caption),
    ])
    inner = con(ids, 'mtg-hero-inner', [left, right], direction='row')
    return con(ids, 'mtg-hero mtp-hero', [inner], _title='Hero')


def card(ids, num, title, meta, body, link=None):
    head = [heading(ids, 'mtg-num', num, 'div'), con(ids, 'mtg-card-heading', [
        heading(ids, 'mtg-card-title', title, 'h2', link),
        text(ids, 'mtg-card-meta', f'<p>{meta}</p>'),
    ])]
    children = [con(ids, 'mtg-card-head', head, direction='row')]
    if body:
        children.append(con(ids, 'mtg-card-body', body))
    return con(ids, 'mtg-card' + (' mtg-card-link' if link else ''), children)


def group(ids, label, docs):
    parts = [heading(ids, 'mtg-group-label', label, 'h3')] if label else []
    return con(ids, 'mtg-group' + ('' if label else ' mtg-group-plain'), parts + [doc_list(ids, docs)], direction='row')


def body(ids, cards):
    return con(ids, 'mtg-body', [con(ids, 'mtg-wrap', cards)], _title='Guides')


def cta(ids, title='Can’t find the guide you need?'):
    left = con(ids, 'mtg-cta-text', [
        heading(ids, 'mtg-cta-title', title, 'h2'),
        text(ids, 'mtg-cta-sub', '<p>Feel free to contact our office for further information.</p>'),
    ])
    right = con(ids, 'mtg-cta-actions', [
        w(ids, 'button', 'mtg-cta-btn', text='Contact Us →', link={'url': '/contact/', 'is_external': '', 'nofollow': ''}),
        text(ids, 'mtg-cta-or', '<p>or call</p>'),
        heading(ids, 'mtg-cta-phone', '03 9792 2243', 'div', 'tel:0397922243'),
    ], direction='row')
    return con(ids, 'mtg-cta-wrap', [con(ids, 'mtg-cta', [left, right], direction='row')], _title='Call to action')


def count(groups):
    docs = sum(len(d) for _, d in groups)
    return f'{docs} documents · {len(groups)} categories'


def guide_hero(ids, key, intro, img=HERO_IMG, caption='Microtec external LED warning light'):
    return hero(ids, PAGES[key][0], intro, img, caption,
                [('Home', '/'), ('Technical / Installation Guides', GUIDES)])


def bronto_guide(ids):
    """The Bronto guide from the "Microtec Bronto Keypad Overlay Guide" design: a hero with
    "Start the guide" and "Download PDF", then a progress card and "Before you start" beside
    the steps in four phases. Steps are tap-to-tick (assets/js/mt-guide.js)."""
    total = sum(1 for _, items in BRONTO_PHASES for i in items if isinstance(i, str))
    title = PAGES['bronto'][0]
    crumbs = ('<p><a href="/">Home</a><span>/</span><a href="/guides/">Technical / Installation Guides</a>'
              '<span>/</span><strong>Bronto Keypad Overlay</strong></p>')
    link = lambda url: {'url': url, 'is_external': '', 'nofollow': ''}
    left = con(ids, 'mtg-hero-text', [
        text(ids, 'mtg-crumbs', crumbs),
        heading(ids, 'mtb-kicker', f'Installation guide · {total} steps', 'div'),
        heading(ids, 'mtg-title', title, 'h1'),
        con(ids, 'mtb-hero-actions', [
            w(ids, 'button', 'mtb-btn mtb-btn-start', text='Start the guide', link=link('#steps'),
              selected_icon={'value': 'fas fa-arrow-down', 'library': 'fa-solid'}, icon_align='row-reverse'),
            w(ids, 'button', 'mtb-btn mtb-btn-pdf', text='Download PDF', link=link('#print'),
              selected_icon={'value': 'fas fa-download', 'library': 'fa-solid'}, icon_align='row-reverse'),
        ], direction='row'),
    ])
    right = con(ids, 'mtg-hero-media mtb-hero-media', [
        w(ids, 'image', 'mtg-hero-img', image=BRONTO_IMG, image_size='full'),
    ])
    hero_sec = con(ids, 'mtg-hero mtp-hero', [con(ids, 'mtg-hero-inner', [left, right], direction='row')], _title='Hero')

    # Sidebar: progress and the safety note.
    phase_links = [{'_id': ids(), 'text': f'0{i + 1} {t}', 'link': link(f'#phase-{i + 1}'),
                    'selected_icon': {'value': '', 'library': ''}}
                   for i, (t, _) in enumerate(BRONTO_PHASES)]
    progress = con(ids, 'mtb-card mtb-progress', [
        con(ids, 'mtb-progress-head', [
            heading(ids, 'mtb-label', 'Your progress', 'div'),
            heading(ids, 'mtb-count', f'0 / {total}', 'div'),
        ], direction='row'),
        con(ids, 'mtb-bar', [con(ids, 'mtb-bar-fill', [])]),
        text(ids, 'mtb-hint', '<p>Tap a step to mark it done.</p>'),
        w(ids, 'icon-list', 'mtb-phases', icon_list=phase_links, view='traditional'),
    ])
    before = con(ids, 'mtb-card mtb-before', [
        heading(ids, 'mtb-label', 'Before you start', 'div'),
        text(ids, 'mtb-before-text', f'<p><strong>{BRONTO_BEFORE}</strong></p><p>{BRONTO_INTRO}</p>'),
    ])
    side = con(ids, 'mtb-side', [progress, before])

    # Steps, phase by phase.
    phases, n = [], 0
    for i, (t, items) in enumerate(BRONTO_PHASES):
        kids = [con(ids, 'mtb-phase-head', [
            heading(ids, 'mtb-pnum', f'0{i + 1}', 'div'),
            heading(ids, 'mtb-ptitle', t, 'h2'),
        ], direction='row')]
        for item in items:
            if isinstance(item, str):
                n += 1
                kids.append(con(ids, 'mtb-step', [
                    heading(ids, 'mtb-snum', str(n), 'div'),
                    text(ids, 'mtb-stext', f'<p>{item}</p>'),
                ], direction='row'))
            elif 'warn' in item:
                kids.append(con(ids, 'mtb-warn', [
                    heading(ids, 'mtb-warn-title', 'WARNING!', 'div'),
                    text(ids, 'mtb-warn-text', f'<p>{item["warn"]}</p>'),
                ]))
            else:
                kids.append(text(ids, 'mtb-tip', f'<p>{item["tip"]}</p>'))
        phases.append(con(ids, 'mtb-phase', kids, _element_id=f'phase-{i + 1}'))
    phases.append(text(ids, 'mtb-alldone', f'<p>All {total} steps complete.</p>'))
    steps = con(ids, 'mtb-steps', phases)

    body_sec = con(ids, 'mtg-body mtb-body', [con(ids, 'mtb-wrap', [side, steps], direction='row')],
                   _title='Steps', _element_id='steps')
    cta_sec = cta(ids, 'Need help with your Bronto display?')
    return [hero_sec, body_sec, cta_sec]


def build():
    out = {}

    ids = Ids('pre')
    out['pre'] = [
        guide_hero(ids, 'pre', 'Installation instructions for the external warning light and Light Control '
                   'Module (LCM) MKI, for units purchased before 1 September 2011. Select a guide below to '
                   'view and download the PDF.'),
        body(ids, [card(ids, '01', 'External Warning Light & Light Control Module (LCM) MKI Installation '
                        'Instructions (PRE 1/9/2011 Purchase)', count(PRE),
                        [group(ids, label, docs) for label, docs in PRE])]),
        cta(ids),
    ]

    ids = Ids('post')
    out['post'] = [
        guide_hero(ids, 'post', 'Installation instructions for the external warning light and Light Control '
                   'Module (LCM) MKII/MKIII, for units purchased from 1 September 2011. Select a guide below '
                   'to view and download the PDF.', POST_IMG),
        body(ids, [
            card(ids, '01', 'Light Control Module (LCM) MKII/MKIII to external warning light connections',
                 f'{len(POST_LIGHTS)} documents', [group(ids, None, POST_LIGHTS)]),
            card(ids, '02', 'Light Control Module (LCM) MKII/MKIII connections to crane computers',
                 count(POST_CRANES), [group(ids, label, docs) for label, docs in POST_CRANES]),
            card(ids, '03', 'LCM MKII/MKIII miscellaneous instructions',
                 f'{len(POST_MISC)} documents', [group(ids, None, POST_MISC)]),
        ]),
        cta(ids),
    ]

    ids = Ids('tadano')
    out['tadano'] = [
        guide_hero(ids, 'tadano', 'Technical information for Tadano cranes from the Microtec team. Download '
                   'the guide below, or contact us on +61 3 9792 2243.', TADANO_IMG, 'Tadano load cell'),
        body(ids, [card(ids, '01', 'Tadano Cranes Technical Information', f'{len(TADANO)} document',
                        [group(ids, None, TADANO),
                         text(ids, 'mtg-note', '<p>Contact us on <a href="tel:+61397922243">+61 3 9792 2243</a></p>')])]),
        cta(ids),
    ]

    out['bronto'] = bronto_guide(Ids('bronto'))

    # The Guides page: one card per guide, linking to its page.
    ids = Ids('guides')
    meta = {
        'pre': count(PRE),
        'post': f'{len(POST_LIGHTS) + sum(len(d) for _, d in POST_CRANES) + len(POST_MISC)} documents · 3 sections',
        'tadano': f'{len(TADANO)} document',
        'bronto': 'Step-by-step instructions',
    }
    out['guides'] = [
        hero(ids, 'Technical / Installation Guides', 'Installation instructions and technical information for '
             'Microtec products. Select a guide below to view and download the PDFs.', HERO_IMG,
             'Microtec external LED warning light', [('Home', '/')]),
        body(ids, [card(ids, f'0{i + 1}', PAGES[k][0], meta[k], None, f'{GUIDES}{PAGES[k][1]}/')
                   for i, k in enumerate(['pre', 'post', 'tadano', 'bronto'])]),
        cta(ids),
    ]
    return out


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    data = build()
    path = os.path.join(here, '..', 'sections', 'guides.json')
    json.dump(data, open(path, 'w'), ensure_ascii=False, indent=1)
    for k, v in data.items():
        print(k, len(json.dumps(v)))
