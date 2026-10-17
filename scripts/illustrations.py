"""Inline our original drawings, with isolated IDs and independently moving parts."""
import itertools
import xml.etree.ElementTree as ET

_instances = itertools.count()
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

# Child indices refer to the original illustration's foreground group.
PARTS = {
    'satellite': {'float': [2], 'pulse': [4, 5]},
    'platform': {'draw': [9], 'pulse': [2, 3, 4], 'slide': [6]},
    'chip': {'tilt': [0], 'draw': [1]},
    'outreach': {'draw': [3, 6], 'pulse': [2]},
    'rover': {'drive': [2]},
    'aircraft': {'float': [1]},
    'code': {'draw': [6], 'slide': [5]},
    'fault': {'draw': [1], 'pulse': [2]},
    'image': {'slide': [2], 'pulse': [5, 6]},
    'signal': {'draw': [1, 2]},
    'suspension': {'float': [3], 'pulse': [4]},
    'radio': {'pulse': [2]},
    'rocket': {'launch': [1]},
    'observatory': {'tilt': [2], 'pulse': [3, 4, 5, 6]},
    'detector': {'draw': [29, 30, 31, 32, 33], 'pulse': [34]},
}


def illustration(root, name):
    svg = ET.parse(root / 'img/illustrations' / f'{name}.svg').getroot()
    prefix = f'art-{next(_instances)}-'
    ids = {node.get('id'): prefix + node.get('id') for node in svg.iter() if node.get('id')}
    for node in svg.iter():
        for key, value in list(node.attrib.items()):
            for old, new in ids.items():
                value = value.replace(f'url(#{old})', f'url(#{new})')
            node.set(key, ids[value] if key == 'id' else value)
    svg.attrib.update({'class': f'illustration art-{name}', 'aria-hidden': 'true', 'focusable': 'false', 'width': '800', 'height': '500'})
    subject = list(svg)[3]
    children = list(subject)
    for motion, indices in PARTS[name].items():
        for index in indices:
            node = children[index]
            if motion == 'draw':
                node.set('class', 'art-draw')
                node.set('pathLength', '1')
            else:
                # Animate a wrapper so the original SVG transform is preserved.
                position = list(subject).index(node)
                subject.remove(node)
                wrapper = ET.Element(f'{{{NS}}}g', {'class': f'art-{motion}'})
                wrapper.append(node)
                subject.insert(position, wrapper)
    return ET.tostring(svg, encoding='unicode')
