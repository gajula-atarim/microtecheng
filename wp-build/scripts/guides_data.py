"""Technical / Installation Guides: content from the client's old site
(microteceng.com.au/page/external-warning-light-and-light-control-module-mk/~-118,
/page/external-warning-light-and-light-control-module-mk/,
/page/tadano-cranes-technical-information/ and
/page/bronto-lcd-display-keypad-overlay-replacement/).

Each document is (label, file name under the old site's /assets/files/). The PDFs are copied
into the WordPress media library, so the links keep working when the old site goes."""

OLD_FILES = 'https://www.microteceng.com.au/assets/files/'

PRE = [
    ('General', [
        ('Connecting a Light Control Module (LCM) to external warning lights', 'Connections to all light types x7.pdf'),
        ('General installation instructions for the Microtec Light Control Module (LCM)', 'Universal Light Contol Module Instructions.pdf'),
        ('Thiess Light Control Module overview', 'Microtec Light Activation Box overview (Theiss).pdf'),
    ]),
    ('3B6', [
        ('3B6 LCM installation instructions', 'Franna 3B6 Instructions(Thesis)(1).pdf'),
    ]),
    ('Grove/Manitowoc', [
        ('EKS 83 LCM installation instructions', 'Grove EKS83(4).pdf'),
        ('EKS 4 LCM installation instructions', 'Grove EKS4_Normal_.pdf'),
        ('EKS 5 LCM installation instructions', 'Grove EKS5_Normal_(1).pdf'),
    ]),
    ('Kato', [
        ('MS7 LCM installation instructions', 'MS7.pdf'),
        ('MS10 LCM installation instructions', 'Kato ms10.pdf'),
        ('MS15B LCM installation instructions', 'Kato MS15B(1).pdf'),
    ]),
    ('Liebherr', [
        ('Liccon LCM installation instructions', 'Liccon Liebherr(1).pdf'),
    ]),
    ('PAT', [
        ('DS350G LCM installation instructions', 'PAT DS350G.pdf'),
    ]),
    ('Robway', [
        ('1502 LCM installation instructions', 'Robway 1502.pdf'),
    ]),
    ('Tadano', [
        ('AML LC, LA installation instructions', 'AML LC-LA.pdf'),
        ('AML M1, M2 installation instructions for truck cranes', 'Tadano AML M1_M2.pdf'),
        ('AML M1, M2 installation instructions for rough terrain cranes', 'Tadano AML M1_M2(1).pdf'),
    ]),
]

POST_LIGHTS = [
    ('Connecting an LCM MKII/MKIII to Microtec Compact LED external warning lights', 'Mk II Connections to Compact Microtec LED Light.pdf'),
    ('Connecting an LCM MKII/MKIII to Microtec Standard Globe Tower lights', 'MkII Connections to Microtec Standard Globe Tower Light.pdf'),
    ('Connecting an LCM MKII/MKIII to Patlite WME-A common ground light assembly', 'MkII Connections to Common Ground WME-A.pdf'),
    ('Connecting an LCM MKII/MKIII to Patlite WME-A light assembly', 'MkII Connections to WME-A.pdf'),
    ('Connecting an LCM MKII/MKIII to Patlite WME-AFB light assembly', 'MkII Connections to WME-AFB with buzzer.pdf'),
    ('Connecting an LCM MKII/MKIII to Patlite KJSB-302-RAG light assembly', 'MkII Connections to KJSB-302-RAG with buzzer.pdf'),
    ('Connecting an LCM MKII/MKIII to Microtec Large LED light assembly', 'MkII Connections to large Microtec LED Light.pdf'),
    ('Connecting an LCM MKII/MKIII to Robway LED light assembly', 'MkII Connections to Robway LED Light.pdf'),
    ('Connecting an LCM MKII/MKIII to 8 types of light assemblies', 'MkII LCM Connections to 8 Light Types.pdf'),
]

POST_CRANES = [
    ('3B6', [
        ('Franna late model 3B6 LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Franna 3B6 Late Model.pdf'),
        ('Franna early model 3B6 LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Franna 3B6 Older Model.pdf'),
    ]),
    ('Grove/Manitowoc', [
        ('EKS 4 LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Grove EKS4.pdf'),
        ('EKS 5 LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Grove EKS5.pdf'),
    ]),
    ('Kato', [
        ('MS10 LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Kato MS10.pdf'),
        ('MS15B LCM MKII/MKIII installation instructions', 'MkII Connection Instructions Kato MS15.pdf'),
    ]),
    ('Kobelco', [
        ('RK70-2 installation instructions', 'MkII Connection Instructions Kobelco RK70-2.pdf'),
        ('RK160-2 installation instructions', 'MkII Connection Instructions Kobelco RK160-2.pdf'),
    ]),
    ('Liebherr', [
        ('Liccon LCM installation instructions', 'MkII Connection Instructions Liebherr Liccon.pdf'),
    ]),
    ('PAT', [
        ('DS350G LCM installation instructions', 'MkII Connection Instructions PAT DS350.pdf'),
    ]),
    ('Robway', [
        ('1502 LCM installation instructions', 'MkII Connection Instructions Robway 1502.pdf'),
    ]),
    ('Tadano', [
        ('AML LC, LA installation instructions', 'MkII Connection Instructions Tadano AML LA LC.pdf'),
        ('AML M1, M2 installation instructions for truck cranes', 'MkII Connection Instructions Tadano AML M1 M2-TL.pdf'),
        ('AML M1, M2 installation instructions for rough terrain cranes', 'MkII Connection Instructions Tadano AML M1 M2-TR.pdf'),
    ]),
]

POST_MISC = [
    ('LCM MKII/MKIII fault finding table', 'Light Control Module Fault Finding Table.pdf'),
    ('LCM MKII/MKIII operational overview', 'Microtec MkII Light Control Module Overview.pdf'),
    ('LCM MKII/MKIII Thiess spec/latching module operational overview', 'Microtec MkII Latching Light Control Module Overview.pdf'),
    ('Replacing an old LCM with a new LCM MKII/MKIII', 'MkII LCM Conversion.pdf'),
]

TADANO = [
    ('Troubleshooting Tadano load cell faults', 'Troubleshooting Tadano load cell faults.pdf'),
]

BRONTO_INTRO = ('Reasonable care is exercised in the preparation of these instructions, but variations in '
                'machine build may impact the accuracy from time to time and are beyond our control. These '
                'instructions should be used by suitably competent personnel for guidance only.')

# The old page's paragraphs, in order. The warning paragraph and the silicone note are kept
# as their own blocks on the new page.
BRONTO_STEPS = [
    'Before undertaking any electrical work on a vehicle ensure that the power supply is isolated.',
    'Unscrew the front panel of the display unit. Disconnect the internal connectors to allow separation of the panel from the housing. Ensure that the connectors can be returned to their original locations during re assembly.',
    'Remove the display to a clean work area.',
    'Remove the outer cover and mounting screws that secure the main PCB behind the display module.',
    'Taking great care not to tug on or damage the interconnecting wires, remove the fixings that secure the display module behind the front panel.',
    'Carefully unplug the 14 way ribbon cable connecting the front panel to the main PCB. Separate the 2 assemblies and put the electronics safely aside ready for re assembly.',
    'Cut through the silicone around the rear of the ribbon cable to free the cable from the panel.',
    'Without damaging the paint finish or the acrylic window on the panel, lift an outer corner of the keypad label and peel it from the panel.',
    'Thoroughly clean remnants of the old label and any adhesive / sealant from the panel and cable slot. A solvent such as IPA alcohol is ideal for this because of its degreasing properties. Stronger solvents may damage the acrylic window or paint finish.',
    'Dry fit the replacement label to ensure a good fit. Do not kink or tightly bend the connecting ribbon as this will cause irreparable damage to the new overlay.',
    'When a satisfactory fit is confirmed the label should be removed and approximately 1/3 of the protective backing peeled back from the area nearest to the ribbon cable. Also remove the backing from the small in-fill piece behind the ribbon cable ensuring that the ribbon is not allowed to contact the adhesive.',
]
BRONTO_WARNING = 'Once adhered to the panel, removal of the new label will not be possible without damage.'
BRONTO_STEPS_2 = [
    'Feed the ribbon cable through the slot and carefully place the section of the label <strong>WITH</strong> backing in place on the panel while keeping the section with exposed adhesive clear of the panel.',
    'Use the section of the label <strong>WITH</strong> backing to slide the label precisely into position.',
    'Only when absolutely sure of a perfect placement should the section with exposed adhesive be allowed to come down gently on the panel. The margins of the adhesive that bound the backing material should not be allowed to bond firmly with the panel as this makes removal of the remaining backing difficult.',
    'The remaining backing must now be removed from beneath the label so that the entire surface may be fully applied to the panel. Firmly rub down the label to ensure complete adhesion and sealing.',
    'Invert the panel and pour a small quantity of flowable silicone into the slot around the ribbon cable. It is beneficial for the silicone to seep into any voids around the ribbon in-fill area. <em>The quality of the seal provided by this step will determine the level of protection afforded to the electronics within the enclosure.</em>',
    'Allow the silicone to fully cure before plugging the ribbon connector into the main PCB and re assembling the display.',
]
BRONTO_NOTE = '“Permatex Flowable Silicone” is available in 42g tubes from Repco for under $10.'


def all_files():
    files = [f for _, docs in PRE for _, f in docs]
    files += [f for _, f in POST_LIGHTS]
    files += [f for _, docs in POST_CRANES for _, f in docs]
    files += [f for _, f in POST_MISC + TADANO]
    return files
