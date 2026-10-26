"""Builds the Contact Us page from the "Microtec Contact" design, using Elementor's own widgets
(containers, Heading, Text Editor, Icon Box, Icon List, Icon, Image, Google Maps, Button), so every
title, phone number, address and link can be edited in Elementor. The enquiry form is the
Contact Form 7 form FORM_ID (edited under Contact > Contact Forms); its markup is FORM_TEMPLATE
below. The look comes from the theme's assets/css/mt-contact.css, keyed on the mtc-* classes set
here; the hero reuses the guide pages' mtg-hero styles.

    python3 contact.py   ->  sections/contact.json  {elements, form_template}
"""

import json, os
from guides import Ids, con, w, heading, text

U = 'https://microteceng.wsdfy.com/wp-content/uploads/2026/10/'
FORM_ID = 963
TECH_IMG = {'id': 962, 'url': U + 'contact-technician.jpg', 'alt': 'Technician working on machine electronics'}
WORKSHOP_IMG = {'id': 489, 'url': U + 'microtec-building-maxwell-st.jpg',
                'alt': 'Microtec Engineering building, 16-18 Maxwell St, Dandenong South'}

PHONE, PHONE_INTL, TEL = '03 9792 2243', '+61 3 9792 2243', 'tel:+61397922243'
EMAIL = 'enquiries@microteceng.com.au'
STREET = '16-18 Maxwell St, Dandenong South VIC 3175'
PO_BOX = 'PO Box 4413, Dandenong South VIC 3164'
DIRECTIONS = 'https://www.google.com/maps/search/?api=1&query=16+Maxwell+St+Dandenong+South+VIC+3175'

# Line icons already in the media library; Font Awesome where there is no uploaded one.
ICON = {
    'phone': {'value': {'url': U + 'ico-phone.svg', 'id': 91}, 'library': 'svg'},
    'mail': {'value': {'url': U + 'ico-mail.svg', 'id': 92}, 'library': 'svg'},
    'pin': {'value': {'url': U + 'ico-pin.svg', 'id': 93}, 'library': 'svg'},
    'box': {'value': 'fas fa-box', 'library': 'fa-solid'},
    'card': {'value': 'far fa-credit-card', 'library': 'fa-regular'},
}


def link(url, external=False):
    return {'url': url, 'is_external': 'on' if external else '', 'nofollow': ''}


def hero(ids):
    cards = [
        ('Call us', PHONE, TEL, 'phone'),
        ('Email us', EMAIL, 'mailto:' + EMAIL, 'mail'),
        ('Visit us', STREET, '#contact-details', 'pin'),
    ]
    text_col = con(ids, 'mtg-hero-text', [
        text(ids, 'mtg-crumbs', '<p><a href="/">Home</a><span>/</span><strong>Contact Us</strong></p>'),
        heading(ids, 'mtg-title', 'Contact Us', 'h1'),
        text(ids, 'mtg-intro mtc-intro', '<p>Talk to our team about parts, electronic repairs, custom design and '
             'installation for plant and equipment. Call us, email us or send an enquiry below.</p>'),
    ])
    row = con(ids, 'mtc-cards', [
        w(ids, 'icon-box', 'mtc-card', selected_icon=ICON[icon], title_text=label, description_text=value,
          link=link(url), position='left', title_size='div')
        for label, value, url, icon in cards
    ], direction='row')
    inner = con(ids, 'mtg-hero-inner mtc-hero-inner', [text_col, row])
    return con(ids, 'mtg-hero mtp-hero mtc-hero', [inner], _title='Hero')


def enquiry(ids):
    lines = [
        {'_id': ids(), 'text': PHONE, 'link': link(TEL), 'selected_icon': ICON['phone']},
        {'_id': ids(), 'text': EMAIL, 'link': link('mailto:' + EMAIL), 'selected_icon': ICON['mail']},
        {'_id': ids(), 'text': STREET, 'selected_icon': ICON['pin']},
        {'_id': ids(), 'text': PO_BOX, 'selected_icon': ICON['box']},
    ]
    photo = con(ids, 'mtc-photo-card', [
        w(ids, 'image', 'mtc-photo', image=TECH_IMG, image_size='large'),
        con(ids, 'mtc-photo-text', [
            heading(ids, 'mtc-photo-title', 'Need a component, repair or engineering solution?', 'h2'),
            text(ids, 'mtc-photo-sub', '<p>Tell us what you need and our team will get back to you.</p>'),
            w(ids, 'icon-list', 'mtc-lines', icon_list=lines, view='traditional'),
        ]),
    ])
    form = con(ids, 'mtc-form-card', [
        heading(ids, 'mtc-kicker', 'Get in touch', 'div'),
        heading(ids, 'mtc-form-title', 'Send an enquiry', 'h2'),
        w(ids, 'shortcode', 'mtc-form', shortcode=f'[contact-form-7 id="{FORM_ID}" title="Contact page enquiry"]'),
    ])
    wrap = con(ids, 'mtc-enquiry-wrap', [photo, form], direction='row')
    return con(ids, 'mtc-enquiry', [wrap], _title='Enquiry', _element_id='enquiry')


def details(ids):
    rows = [
        ('pin', 'Physical Address', '<p>16-18 Maxwell St<br>Dandenong South, Victoria, 3175</p>'),
        ('phone', 'Phone', f'<p><a href="{TEL}">{PHONE_INTL}</a></p>'),
        ('box', 'Mailing Address', '<p>PO Box 4413<br>Dandenong Sth B.C., Victoria, Australia, 3164</p>'),
        ('mail', 'Email', f'<p>Please fill in the <a href="#enquiry">enquiry form above</a><br>or<br>'
                          f'<a href="mailto:{EMAIL}">enquiries@<wbr>microteceng.com.au</a></p>'),
        ('card', 'Accounts', f'<p><a href="{TEL}">{PHONE_INTL}</a></p>'),
    ]
    info = con(ids, 'mtc-info', [
        heading(ids, 'mtc-kicker mtc-kicker-light', 'Get in touch', 'div'),
        heading(ids, 'mtc-details-title', 'Company contact details', 'h2'),
        con(ids, 'mtc-rows', [
            con(ids, 'mtc-row', [
                w(ids, 'icon', 'mtc-row-icon', selected_icon=ICON[icon]),
                heading(ids, 'mtc-row-label', label, 'h3'),
                text(ids, 'mtc-row-value', value),
            ], direction='row')
            for icon, label, value in rows
        ]),
        con(ids, 'mtc-pills', [
            heading(ids, 'mtc-pill', 'ACN: 103 309 253', 'div'),
            heading(ids, 'mtc-pill', 'ABN: 26 103 309 253', 'div'),
        ], direction='row'),
    ])
    workshop = con(ids, 'mtc-workshop', [
        w(ids, 'image', 'mtc-workshop-img', image=WORKSHOP_IMG, image_size='full'),
        con(ids, 'mtc-workshop-text', [
            heading(ids, 'mtc-workshop-title', 'Our workshop', 'div'),
            text(ids, 'mtc-workshop-sub', '<p>16-18 Maxwell St, Dandenong South</p>'),
        ]),
        w(ids, 'button', 'mtc-directions', text='Get directions →', link=link(DIRECTIONS, True)),
    ], direction='row')
    mapcol = con(ids, 'mtc-map', [
        w(ids, 'google_maps', 'mtc-map-embed', address='16 Maxwell St, Dandenong South VIC 3175, Australia',
          zoom={'unit': 'px', 'size': 15, 'sizes': []}, height={'unit': 'px', 'size': 520, 'sizes': []}),
        workshop,
    ])
    card = con(ids, 'mtc-details-card', [info, mapcol], direction='row')
    return con(ids, 'mtc-details', [con(ids, 'mtc-details-wrap', [card])],
               _title='Contact details', _element_id='contact-details')


# The enquiry form (Contact Form 7). Field names match the form's mail template.
FORM_TEMPLATE = '''<div class="mtc-cf">
<div class="mtc-field mtc-full"><span class="mtc-label">Product or service needed</span>
[radio product-service use_label_element default:1 "Part or component" "Electronic repair" "Design & installation" "Technical support" "Other"]</div>
<label class="mtc-field">Name [text* your-name autocomplete:name]</label>
<label class="mtc-field">Company [text your-company autocomplete:organization]</label>
<label class="mtc-field">Email [email* your-email autocomplete:email]</label>
<label class="mtc-field">Phone [tel* your-phone autocomplete:tel]</label>
<label class="mtc-field mtc-full">Part number (optional) [text part-number placeholder "e.g. 363-xxxx"]</label>
<label class="mtc-field mtc-full">Message [textarea* your-message x4 placeholder "Machine make and model, fault description, quantity…"]</label>
<label class="mtc-file mtc-full"><span class="mtc-file-icon" aria-hidden="true"></span><span class="mtc-file-text"><span class="mtc-file-title">Photo (optional)</span><span class="mtc-file-name">No file chosen · JPG or PNG</span></span><span class="mtc-file-browse" aria-hidden="true">Browse</span>[file photo limit:8mb filetypes:jpg|jpeg|png|gif|webp|heic]</label>
<div class="mtc-submit mtc-full">[submit "Send an Enquiry →"]</div>
</div>'''


def build():
    ids = Ids('contact')
    return {'elements': [hero(ids), enquiry(ids), details(ids)], 'form_template': FORM_TEMPLATE}


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    data = build()
    path = os.path.join(here, '..', 'sections', 'contact.json')
    json.dump(data, open(path, 'w'), ensure_ascii=False, indent=1)

    def count(els, c):
        for e in els:
            k = e.get('widgetType', e['elType'])
            c[k] = c.get(k, 0) + 1
            count(e['elements'], c)
        return c
    print(count(data['elements'], {}), len(json.dumps(data['elements'])))
