"""Pages that are not in the design handoff. The service pages are written from the client's old site
(microteceng.com.au/page/radio-control-systems/ and /page/system-intergration/) and the
copy already on the new site. They reuse the class combinations of the built service pages,
so they share the same CSS, fonts and layout. The Contact page is assembled from the
homepage enquiry block and the About page contact details."""

import json

U = 'https://microteceng.wsdfy.com/wp-content/uploads/2026/10/'

def hero(title, intro, img, alt, crumbs='<a class="m892be7" href="/#services">Our Services</a><span>/</span>'):
    return f'''<section class="m75245e mtp-hero">
  <div class="mbefb19"><span class="m0069f5"></span><span class="m0069f5"></span><span class="m0069f5"></span></div>
  <div class="md6a7de">
    <div class="m350759">
      <div class="m40d029">
        <div class="m58aedf"><a class="m892be7" href="/">Home</a><span>/</span>{crumbs}<span class="m8f2809">{title}</span></div>
        <h1 class="m6f8485">{title}</h1>
        <p class="m54d788">{intro}</p>
      </div>
      <div class="m1e56ad"><img class="m0e7591" src="{U}{img}" alt="{alt}" loading="lazy"></div>
    </div>

  </div></section>'''

ICONS = {
    'radio': 'M5 12.5a10 10 0 0 1 14 0M8 15.5a5.5 5.5 0 0 1 8 0M12 19h.01',
    'sliders': 'M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M14 4v4M8 10v4M16 16v4',
    'link': 'M4 12h16M4 6h4v12H4zM16 6h4v12h-4zM10 9h4v6h-4z',
    'swap': 'M4 7h13l-3-3M20 17H7l3 3',
    'shield': 'M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6zM8.5 12l2.5 2.5 4.5-5',
    'tools': 'M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z',
    'chip': 'M7 7h10v10H7zM10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4',
    'crane': 'M12 3v3M5 21h14M7 21l5-12 5 12M4 9h16',
    'scale': 'M4 20V10M10 20V4M16 20v-7M22 20H2',
    'truck': 'M3 7h11v9H3zM14 10h4l3 3v3h-7M7 19a2 2 0 1 0 0-.01M17 19a2 2 0 1 0 0-.01',
    'belt': 'M4 15h16M6 15a3 3 0 1 0 0 .01M18 15a3 3 0 1 0 0 .01M7 11h10l2 4H5z',
    'tree': 'M12 3l6 8h-4l4 6H6l4-6H6zM12 17v4',
    'tower': 'M8 21l4-18 4 18M6 9h12M7 15h10',
    'winch': 'M4 12a4 4 0 1 0 8 0 4 4 0 1 0-8 0M12 12h8M20 12v6M18 18h4',
}

def svg(name, cls, stroke):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="{stroke}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="{ICONS[name]}"></path></svg>')

def cards(kicker, heading, side, items):
    out = []
    for n, (icon, title, text) in enumerate(items, 1):
        if n == 1:
            out.append(f'''      <div class="m16698d mh8">
        <div class="ma60859">
          <span class="mf2879b">{svg(icon, 'mc4771a', '#3B479C')}</span>
          <span class="m483246">{n:02d}</span>
        </div>
        <span class="m2d6cbd">{title}</span>
        <span class="m286bc1">{text}</span>
      </div>''')
        else:
            out.append(f'''      <div class="mf9aa13 mh8">
        <div class="ma60859">
          <span class="md3f8d6">{svg(icon, 'mc4771a', '#fff')}</span>
          <span class="m483246">{n:02d}</span>
        </div>
        <span class="m2d6cbd">{title}</span>
        <span class="mc3fc4d">{text}</span>
      </div>''')
    return f'''<section class="mbdbf5b">
  <div class="md5e4d6">
    <div class="m3a688e">
      <div class="m5e01f3">
        <div class="md8d053">{kicker}</div>
        <h2 class="m71bc66">{heading}</h2>
      </div>
      <p class="m21c823">{side}</p>
    </div>
    <div class="mc1ef13">
{chr(10).join(out)}
    </div>
  </div></section>'''

def feature_list(img, alt, badge, kicker, heading, items):
    rows = []
    for n, (icon, title, text) in enumerate(items, 1):
        sub = f'<span class="me7083a">{text}</span>' if text else ''
        rows.append(f'''          <div class="mtp-ewp-215 mtp-ewp-item">
            <span class="mtp-ewp-216"></span>
            <span class="mtp-ewp-217">{svg(icon, 'm38124c', '#fff')}</span>
            <div class="m615852">
              <span class="m43070f">{title}</span>
              {sub}
            </div>
            <span class="mtp-ewp-224">{n:02d}</span>
          </div>''')
    return f'''<section class="md56f20">
  <div class="md83142"></div>
  <div class="m880959">
    <div class="m1915b4">
      <div class="m728776"></div>
      <div class="mac8912"><img class="m0e7591" src="{U}{img}" alt="{alt}" loading="lazy"></div>
      <div class="m85dd56">
        <span class="m916ed1">{svg('shield', 'm667ff9', '#fff')}</span>
        <span class="m7943ff">{badge}</span>
      </div>
    </div>
    <div class="me75a9f">
      <div class="m88bfaf">
        <div class="m80de70">{kicker}</div>
        <h2 class="mf56df2">{heading}</h2>
      </div>
      <div class="m88bfaf mtp-ewp-list">
{chr(10).join(rows)}
      </div>
    </div>
  </div></section>'''

def band(title, text):
    return f'''<section class="ma2e621">
  <div class="ma1032d">
    <div class="m5cba87">
      <div class="m83ad2c"><span class="m2b2537"></span><span class="m2b2537"></span><span class="m2b2537"></span></div>
      <span class="m0659dc">{title}</span>
      <p class="m0973e4">{text}</p>
    </div>
  </div></section>'''

def process(kicker, heading, intro, note, steps):
    rows = ''.join(f'''
          <div class="mb0ca0d">
            <span class="mcb78bb">{n:02d}</span>
            <div class="m7299c9"><span class="md63603">{t}</span><span class="md04055">{d}</span></div>
          </div>''' for n, (t, d) in enumerate(steps, 1))
    return f'''<section class="ma2e621">
  <div class="m0787aa">
    <div class="m51de31">
      <div class="md8d053">{kicker}</div>
      <h2 class="m71bc66">{heading}</h2>
      <p class="m1ca2d3">{intro}</p>
      <div class="m119a29">
        {svg('shield', 'md59f61', '#3B479C')}
        <p class="m12fd6b">{note}</p>
      </div>
    </div>
    <div class="m61d522">{rows}
    </div>
  </div></section>'''

def cta(title):
    return f'''<section class="ma2e621">
  <div class="medb174">
    <div class="mc602d2">
      <div class="m31ca0a"><span class="mcbbb19"></span><span class="mcbbb19"></span><span class="mcbbb19"></span></div>
      <div class="m4a6cf4">
        <span class="m4d81a6">{title}</span>
        <span class="m7d9b41">Call us to arrange an appointment to discuss your requirements.</span>
      </div>
      <div class="m4f30b6">
        <a class="me9eab3 mh7" href="/#enquiry">Contact Us →</a>
        <span class="m9b34cf">or call</span>
        <a class="m0f60a8" href="tel:0397922243">03 9792 2243</a>
      </div>
    </div>
  </div></section>'''

# Contact page: the homepage enquiry block (with its own Contact Form 7 form) and the About
# page contact details and map, as they are built for those pages.
_built = json.load(open('sections/pages.json'))
CONTACT_FORM = '<div class="mtp-form">[contact-form-7 id="419" title="Contact page enquiry"]</div>'
_enquiry = _built['home'][8]['html'].replace(
    '<div class="mtp-form">[contact-form-7 id="88" title="Homepage enquiry"]</div>', CONTACT_FORM)
assert CONTACT_FORM in _enquiry
_details = _built['about'][3]['html'].replace(
    '<a class="mef7ec2 mh2" href="/#enquiry">Contact Us →</a>',
    '<a class="mef7ec2 mh2" href="#enquiry">Send an Enquiry →</a>')
_details = _details.replace('Please fill in the form on the <a class="mbfe739" href="/#enquiry">contact us page</a>',
                            'Please fill in the <a class="mbfe739" href="#enquiry">enquiry form above</a>')
assert 'Send an Enquiry' in _details and 'enquiry form above' in _details

EXTRA_PAGES = {
    'radio': [
        {'label': '01 Services Hero', 'html': hero(
            'Radio Control Systems',
            'We supply and fit radio control systems to all types of machinery. From simple on/off '
            'functions to full proportional and digital control of machines, radio remote systems can '
            'save time and money by increasing your efficiency.',
            'radio-remote-systems.jpg', 'Radio remote control systems and the industries they are used in')},
        {'label': '02 Radio control', 'html': cards(
            'What we supply and fit', 'Radio control for all types of machinery',
            'Every system is customised to suit your machine and your needs.', [
                ('radio', 'Supply and fit', 'Radio control systems supplied and fitted to all types of machinery.'),
                ('sliders', 'On/off to full proportional control', 'From simple on/off functions to full proportional and digital control of machines.'),
                ('link', 'Go wireless', 'Have an existing wired control system? We can design systems to complement your existing safety systems and controls.'),
                ('swap', 'Replacement systems', 'Radio control systems designed to replace your existing control systems.'),
                ('shield', 'Safety upgrades', 'Systems designed to upgrade your machine to meet current safety standards.'),
                ('tools', 'Complete installation', 'The full scope of work, including electronics, hydraulics, pneumatics and mechanical installation.'),
            ])},
        {'label': '03 Installations', 'html': feature_list(
            'pexels-photo-35693092.jpeg', 'Mobile crane fitted with radio remote control', 'Radio remote systems',
            'Our installations', 'Our installations have included radio remote systems for:', [
                ('winch', 'Winches on tow trucks', ''),
                ('belt', 'Conveyor belts', ''),
                ('tree', 'Chippers', ''),
                ('crane', 'Mobile rough terrain cranes', ''),
                ('truck', 'Crane trucks', ''),
                ('tower', '40 metre travel towers', ''),
            ])},
        {'label': '04 Customised', 'html': band(
            'Customised to suit your needs.',
            'Call us to arrange an appointment to discuss your requirements so that we can assist you to '
            'customise a system to suit your needs. We can handle the complete supply and installation of '
            'systems covering the full scope of work including electronics, hydraulics, pneumatics and '
            'mechanical installation.')},
        {'label': 'CTA', 'html': cta('Talk to us about a radio control system')},
    ],
    'integration': [
        {'label': '01 Services Hero', 'html': hero(
            'System Integration',
            'Design and fitting of machine control systems. We integrate electronics and safety systems '
            'across your machine, from custom control electronics to radio remotes, load systems and '
            'crane safety systems.',
            'pexels-photo-31580848-scaled.jpeg', 'Machine control system integration')},
        {'label': '02 Integration', 'html': cards(
            'What we design and fit', 'Machine control systems, designed and fitted',
            'We can assist you to customise a system to suit your needs.', [
                ('chip', 'Customised machine control electronics', 'Custom electronic products and systems designed and manufactured for your machinery since 2007.'),
                ('shield', 'Safety systems', 'Load monitoring, light control modules, warning lights, height limiting and alarm latching systems.'),
                ('radio', 'Radio remote control', 'Radio control to complement your existing safety systems and controls, or to replace them.'),
                ('scale', 'Load systems', 'Weighing systems for front end loaders, excavators, forklifts and telescopic handlers.'),
                ('link', 'CanBus control systems', 'CanBus technology minimises wiring, increases reliability and makes troubleshooting simpler.'),
                ('tools', 'Complete installation', 'The full scope of work, including electronics, hydraulics, pneumatics and mechanical installation.'),
            ])},
        {'label': '03 How we work', 'html': process(
            'How we work', 'From your requirements to a fitted, working system',
            'Every system is specified, fitted and calibrated by our engineers to suit your machine and your site.',
            'Robust, reliable and made to withstand harsh conditions. Our experience with electronics used in '
            'plant and equipment goes into every design.', [
                ('Discuss your requirements', 'Call us to arrange an appointment so we can understand your machine, your site and what the system needs to do.'),
                ('Design', 'Custom electronics and control systems designed and manufactured for your machinery.'),
                ('Supply and fit', 'The complete supply and installation, covering electronics, hydraulics, pneumatics and mechanical installation.'),
                ('Calibrate', 'Systems are calibrated by our engineers to suit your machine and your site.'),
            ])},
        {'label': 'CTA', 'html': cta('Need a machine control system designed and fitted?')},
    ],
    'contact': [
        {'label': '01 Contact Hero', 'html': hero(
            'Contact Us',
            'Talk to our team about parts, electronic repairs, custom design and installation for '
            'plant and equipment. Call us, email us or send an enquiry below.',
            'pexels-photo-14319099.jpeg', 'Technician working on machine electronics', crumbs='')},
        {'label': '02 Enquiry', 'html': _enquiry},
        {'label': '03 Contact details', 'html': _details},
    ],
}
