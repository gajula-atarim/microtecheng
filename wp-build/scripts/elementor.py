"""Build the Elementor element tree for each page from sections/pages.json."""
import json, re, hashlib, sys

U = 'https://microteceng.wsdfy.com/wp-content/uploads/2026/10/'
IMAGES = {
    '38190066': U + 'pexels-photo-38190066.jpeg',
    '14319099': U + 'pexels-photo-14319099.jpeg',
    '9242885': U + 'pexels-photo-9242885.jpeg',
    '2136243': U + 'pexels-photo-2136243.jpeg',
    '33488902': U + 'pexels-photo-33488902.jpeg',
    '33694019': U + 'pexels-photo-33694019-scaled.jpeg',
    '28442180': U + 'pexels-photo-28442180.jpeg',
    '16100275': U + 'pexels-photo-16100275.jpeg',
    '4705088': U + 'pexels-photo-4705088.jpeg',
    '37492292': U + 'pexels-photo-37492292-scaled.jpeg',
    '34054470': U + 'pexels-photo-34054470-scaled.jpeg',
    '33694016': U + 'pexels-photo-33694016-scaled.jpeg',
    '29502218': U + 'pexels-photo-29502218.jpeg',
    '38146898': U + 'pexels-photo-38146898.jpeg',
    '5328573': U + 'pexels-photo-5328573.jpeg',
    '36861987': U + 'pexels-photo-36861987.jpeg',
    '37492293': U + 'pexels-photo-37492293.jpeg',
    '39105511': U + 'pexels-photo-39105511.jpeg',
    '33531830': U + 'pexels-photo-33531830.jpeg',
    '29502219': U + 'pexels-photo-29502219.jpeg',
    '11454241': U + 'pexels-photo-11454241.jpeg',
    '31580848': U + 'pexels-photo-31580848-scaled.jpeg',
    '29827405': U + 'pexels-photo-29827405.jpeg',
    '4993793': U + 'pexels-photo-4993793.jpeg',
    '35072810': U + 'pexels-photo-35072810-scaled.jpeg',
    '32588540': U + 'pexels-photo-32588540-scaled.jpeg',
    '35693092': U + 'pexels-photo-35693092.jpeg',
    '35290678': U + 'pexels-photo-35290678-scaled.jpeg',
    '7286002': U + 'pexels-photo-7286002.jpeg',
    '7286016': U + 'pexels-photo-7286016.jpeg',
    'repairs-board-hd': U + 'repairs-board-hd.jpg',
    'ewp-schematic': U + 'ewp-schematic.jpg',
    'forklift-weighing-diagram': U + 'forklift-weighing-diagram.jpg',
    'telehandler-diagram': U + 'telehandler-diagram.jpg',
    'loader-weighing-diagram': U + 'loader-weighing-diagram.jpg',
}

def img_url(src):
    m = re.search(r'pexels-photo-(\d+)', src) or re.search(r'assets/([a-z-]+)\.png', src)
    return IMAGES[m.group(1)]

# Client feedback (Atarim) applied on top of the design's copy: page -> [(old, new)].
COPY_CHANGES = {
    'home': [
        ('Since 2000 · Construction &amp; mining equipment', 'Established 2000 · Specialist Electronics Engineering'),
        ('Specialist Crane Electronics <span class="m4bffa3">&amp; Engineering Solutions</span>',
         'Electronic Engineering, Repairs <span class="m4bffa3">&amp; Custom Solutions for Plant and Equipment</span>'),
        ('custom-designed systems for construction and mining equipment.</p>',
         'custom-designed systems for plant and equipment.</p>'),
        # Hydraulic and mechanical components is no longer a range: the 4th card shows the
        # next category in the carousel data instead.
        ('<a class="mb099a5 mh11 mtp-cat-card" href="#">\n'
         '          <div class="mf2a67f"><img class="m0e7591 mtp-cat-img" src="https://microteceng.wsdfy.com/wp-content/uploads/2026/10/pexels-photo-29502218.jpeg" alt="Hydraulic and mechanical components" loading="lazy"></div>\n'
         '          <div class="m1ee890">\n'
         '            <span class="mf63644 mtp-cat-name">Hydraulic and mechanical components</span>\n'
         '            <span class="mb0299f mtp-cat-desc">Hydraulic parts, level bubbles and mechanical spares for cranes and plant.</span>',
         '<a class="mb099a5 mh11 mtp-cat-card" href="/product-category/hetronic/">\n'
         '          <div class="mf2a67f"><img class="m0e7591 mtp-cat-img" src="https://microteceng.wsdfy.com/wp-content/uploads/2026/10/pexels-photo-38146898.jpeg" alt="Radio remote controls" loading="lazy"></div>\n'
         '          <div class="m1ee890">\n'
         '            <span class="mf63644 mtp-cat-name">Radio remote controls</span>\n'
         '            <span class="mb0299f mtp-cat-desc">Hetronic radio remote controls, supplied and repaired in-house.</span>'),
        # The EWP service stays on its own page but is no longer featured in the services slider.
        ('          <a class="mc8fec3 mh5" href="/services/ewp-control-systems/">\n'
         '            <div class="m363e2e"><img class="m0e7591" src="https://microteceng.wsdfy.com/wp-content/uploads/2026/10/pexels-photo-16100275.jpeg" alt="Elevated Work Platform Control Systems" loading="lazy"></div>\n'
         '            <div class="m8ef944">\n'
         '              <span class="m4cfc65">Elevated Work Platform Control Systems</span>\n'
         '              <span class="mbad608">Control systems for elevated work platforms.</span>\n'
         '              <span class="m934ec2">View more →</span>\n'
         '            </div>\n'
         '          </a>\n'
         '        \n', ''),
        ('<span class="m88aee1">A full range of services for construction and mining equipment.</span>',
         '<span class="m88aee1">A full range of services for plant and equipment.</span>'),
        # Street address alongside the PO Box in the enquiry block.
        ('<span class="mc2e688">PO Box 4413, Dandenong South VIC 3164</span>',
         '<span class="mc2e688">16-18 Maxwell St, Dandenong South VIC 3175</span>\n'
         '        <span class="mc2e688">PO Box 4413, Dandenong South VIC 3164</span>'),
    ],
    # The street address is in Dandenong South.
    'about': [
        ('16-18 Maxwell St<br>Dandenong, Victoria, 3175', '16-18 Maxwell St<br>Dandenong South, Victoria, 3175'),
    ],
    'repairs': [
        ('16 -18 Maxwell St, Dandenong, 3175', '16-18 Maxwell St, Dandenong South VIC 3175'),
    ],
}
# Site-wide wording from the client's review: Microtec serves plant and equipment, not just
# construction and mining. Industry names (the Construction and Mining tiles, project case
# studies) stay as they are.
SITE_COPY = [
    ('assisting customers with construction and mining equipment', 'assisting customers with plant and equipment'),
    ('a full range of services to construction and mining equipment.', 'a full range of services for plant and equipment.'),
    ('<span class="mc16a85">Construction &amp; mining equipment</span>', '<span class="mc16a85">Plant &amp; equipment</span>'),
    ('electronics used in construction and mining equipment', 'electronics used in plant and equipment'),
    ('repair services to the construction and mining industry since 2000.', 'repair services for plant and equipment since 2000.'),
    ('services and repairs for construction and mining equipment', 'services and repairs for plant and equipment'),
    ('Electronics experience built on construction and mining sites.', 'Electronics experience built for plant and equipment.'),
    ('harsh Australian conditions on construction and mining sites.', 'harsh Australian site conditions.'),
    ('years supporting<br>construction &amp; mining', 'years supporting<br>plant &amp; equipment'),
]

def eid(*parts):
    return hashlib.md5('/'.join(parts).encode()).hexdigest()[:7]

def widget(key, i, html):
    # Sections holding a shortcode (the enquiry form) use Elementor's Shortcode widget so
    # WordPress renders it; everything else is an HTML widget.
    if '[contact-form-7' in html:
        return {'id': eid(key, str(i), 'html'), 'elType': 'widget', 'widgetType': 'shortcode',
                'settings': {'shortcode': html}, 'elements': []}
    return {'id': eid(key, str(i), 'html'), 'elType': 'widget', 'widgetType': 'html',
            'settings': {'html': html}, 'elements': []}

def page_tree(key, sections):
    out = []
    for i, s in enumerate(sections):
        html = re.sub(r'\{\{IMG:([^}]*)\}\}', lambda m: img_url(m.group(1)), s['html'])
        for before, after in COPY_CHANGES.get(key, []) + SITE_COPY:
            html = html.replace(before, after)
        if i == 0:
            html = html.replace(' loading="lazy"', '', 1)  # hero image loads eagerly
        out.append({
            'id': eid(key, str(i), 'con'), 'elType': 'container', 'isInner': False,
            'settings': {
                '_title': s['label'], 'content_width': 'full', 'css_classes': 'mtp-con',
                'flex_gap': {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0},
                'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
            },
            'elements': [widget(key, i, '<div class="mtp">' + html + '</div>')],
        })
    return out

pages = json.load(open('sections/pages.json'))
sys.path.insert(0, 'scripts')
from extra_pages import EXTRA_PAGES
pages.update(EXTRA_PAGES)
for key, secs in pages.items():
    tree = page_tree(key, secs)
    json.dump(tree, open(f'sections/{key}.elementor.json', 'w'), separators=(',', ':'))
    print(key, len(json.dumps(tree, separators=(',', ':'))))
