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
    'repairs-board-hd': U + 'repairs-board-hd.jpg',
    'ewp-schematic': U + 'ewp-schematic.jpg',
    'forklift-weighing-diagram': U + 'forklift-weighing-diagram.jpg',
    'telehandler-diagram': U + 'telehandler-diagram.jpg',
    'loader-weighing-diagram': U + 'loader-weighing-diagram.jpg',
}

def img_url(src):
    m = re.search(r'pexels-photo-(\d+)', src) or re.search(r'assets/([a-z-]+)\.png', src)
    return IMAGES[m.group(1)]

def eid(*parts):
    return hashlib.md5('/'.join(parts).encode()).hexdigest()[:7]

def page_tree(key, sections):
    out = []
    for i, s in enumerate(sections):
        html = re.sub(r'\{\{IMG:([^}]*)\}\}', lambda m: img_url(m.group(1)), s['html'])
        if i == 0:
            html = html.replace(' loading="lazy"', '', 1)  # hero image loads eagerly
        out.append({
            'id': eid(key, str(i), 'con'), 'elType': 'container', 'isInner': False,
            'settings': {
                '_title': s['label'], 'content_width': 'full', 'css_classes': 'mtp-con',
                'flex_gap': {'column': '0', 'row': '0', 'isLinked': True, 'unit': 'px', 'size': 0},
                'padding': {'unit': 'px', 'top': '0', 'right': '0', 'bottom': '0', 'left': '0', 'isLinked': True},
            },
            'elements': [{
                'id': eid(key, str(i), 'html'), 'elType': 'widget', 'widgetType': 'html',
                'settings': {'html': '<div class="mtp">' + html + '</div>'}, 'elements': [],
            }],
        })
    return out

pages = json.load(open('sections/pages.json'))
for key, secs in pages.items():
    tree = page_tree(key, secs)
    json.dump(tree, open(f'sections/{key}.elementor.json', 'w'), separators=(',', ':'))
    print(key, len(json.dumps(tree, separators=(',', ':'))))
