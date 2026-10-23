"""Builds the Technical / Installation Guides pages from the "Microtec Technical Guides" design,
using Elementor's own widgets (containers, Heading, Text Editor, Image, Icon List, Button), so
every title, list item and PDF link can be edited in Elementor. The look comes from the
theme's assets/css/mt-guides.css, keyed on the CSS classes set here.

    python3 guides.py   ->  sections/guides.json  {page key: {title, slug, elements}}
"""

import hashlib, json, os, re
from guides_data import (PRE, POST_LIGHTS, POST_CRANES, POST_MISC, TADANO, BRONTO_INTRO,
                         BRONTO_STEPS, BRONTO_WARNING, BRONTO_STEPS_2, BRONTO_NOTE)

U = 'https://microteceng.wsdfy.com/wp-content/uploads/2026/10/'
# PDFs that the old site links to but no longer serves: listed without a download link.
MISSING = {'Microtec Light Activation Box overview (Theiss).pdf',
           'MkII Connections to Microtec Standard Globe Tower Light.pdf'}

HERO_IMG = {'id': 755, 'url': U + 'led-warning-light-hero.jpg'}
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


def cta(ids):
    left = con(ids, 'mtg-cta-text', [
        heading(ids, 'mtg-cta-title', 'Can’t find the guide you need?', 'h2'),
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
                   'to view and download the PDF.'),
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

    ids = Ids('bronto')
    steps = ''.join(f'<li>{s}</li>' for s in BRONTO_STEPS)
    steps2 = ''.join(f'<li>{s}</li>' for s in BRONTO_STEPS_2)
    out['bronto'] = [
        guide_hero(ids, 'bronto', 'Step-by-step instructions for replacing the keypad overlay on a Bronto '
                   'LCD display.', BRONTO_IMG, 'Bronto Skylift display'),
        body(ids, [card(ids, '01', 'Bronto LCD Display Keypad Overlay Replacement',
                        f'{len(BRONTO_STEPS) + len(BRONTO_STEPS_2)} steps', [
                            text(ids, 'mtg-disclaimer', f'<p>{BRONTO_INTRO}</p>'),
                            text(ids, 'mtg-steps', f'<ol>{steps}</ol>'),
                            text(ids, 'mtg-warning', f'<p><strong>WARNING!</strong> {BRONTO_WARNING}</p>'),
                            text(ids, "mtg-steps", f"<ol>{steps2}</ol>"),
                            text(ids, 'mtg-note', f'<p>{BRONTO_NOTE}</p>'),
                        ])]),
        cta(ids),
    ]

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
