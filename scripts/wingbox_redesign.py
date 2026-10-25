"""Render the supplied wing-box design, with precomputed, accessible result panels.

The vectors and historical values in values.json come from the supplied prototype.
They are deliberately separate from the revised solver linked in the page header.
No exported React runtime, template interpreter or third-party script ships to users.
"""
import html
import json
import re

E = html.escape
TOKEN = re.compile(r'\{\{([\w.-]+)\}\}')
LOOP = re.compile(r'<sc-for\s+as="(\w+)"\s+list="\{\{([\w.]+)\}\}">')


def render(b, project, lang):
    root = b['ROOT'] / 'content/wing-box'
    d = b['DESIGN']['Design'](b, lang, b['detail'](project))
    catalog = json.loads((root / 'strings.json').read_text())
    assert all(set(item) == set(b['LANGS']) and all(item.values()) for item in catalog.values())
    text = {key: item[lang] for key, item in catalog.items()}
    values = json.loads((root / 'values.json').read_text())
    templates = {name: (root / (name + '.html.tmpl')).read_text() for name in ['page', 'envelope', 'charts', 'summary', 'torsion', 'part']}
    peers = [p for p in b['PROJECTS'] if p['kind'] == 'projects']
    components = {}
    base = {**values['controls'], 'text': text, 'asset': {'wing-cad.jpg': d.r('img/wing-box/wing-cad.jpg')},
            'url': {'projects': d.link('projects.html')}, 'component': components}

    def lookup(key, context):
        # The asset name includes a period; all remaining paths are object keys.
        if key.startswith('asset.'):
            return base['asset'][key[6:]]
        obj = context
        for part in key.split('.'):
            obj = obj[part]
        return obj

    def raw(value, context):
        if isinstance(value, bool):
            return str(value).lower()
        return TOKEN.sub(lambda m: raw(lookup(m[1], context), context), str(value))

    def fill(template, context):
        # Expand nested loops during the static build, not in the browser.
        while (match := LOOP.search(template)):
            depth, end = 1, match.end()
            for tag in re.finditer(r'<sc-for\b[^>]*>|</sc-for>', template[match.end():]):
                depth += -1 if tag[0].startswith('</') else 1
                if depth == 0:
                    start = match.end() + tag.start()
                    end = match.end() + tag.end()
                    break
            if depth:
                raise ValueError('Unclosed wing-box template loop')
            body = template[match.end():start]
            result = ''.join(fill(body, {**context, match[1]: item}) for item in lookup(match[2], context))
            template = template[:match.start()] + result + template[end:]

        def token(match):
            key = match[1]
            value = lookup(key, context)
            return str(value) if key.startswith('component.') else E(raw(value, context), quote=True)
        return TOKEN.sub(token, template)

    def panel(name, context, visible, prefix):
        result = fill(templates[name], {**base, **context})
        for ident in re.findall(r'\bid="([^"]+)"', result):
            result = result.replace('id="' + ident + '"', 'id="' + prefix + '-' + ident + '"')
            result = result.replace('url(#' + ident + ')', 'url(#' + prefix + '-' + ident + ')')
        if not visible:
            result = result.replace('<div ', '<div hidden ', 1)
        return result

    components['envelope'] = ''.join(panel('envelope', {**modes['loads'], 'condition': cond}, cond == '1', 'envelope-' + cond) for cond, modes in values['flights'].items())
    for name in ['charts', 'summary']:
        components[name] = ''.join(panel(name, {**v, 'condition': cond, 'mode': mode}, cond == '1' and mode == 'loads', name + '-' + cond + '-' + mode) for cond, modes in values['flights'].items() for mode, v in modes.items())
    components['torsion'] = ''
    for case, tor in values['torsion'].items():
        label = next(o['label'] for o in values['controls']['torCases'] if o['key'] == case)
        tor['aria'] = label + ': q1 ' + tor['q1'] + ', q2 ' + tor['q2'] + ', q3 ' + tor['q3'] + '. {{text.t019}}: ' + tor['tmax']
        components['torsion'] += panel('torsion', {'tor': tor, 'case': case}, case == 'f', 'torsion-' + case)
    components['parts'] = ''.join(panel('part', {'p': p, 'choice': choice}, choice == 'ideal', 'part-' + name + '-' + choice) for name, choices in values['parts'].items() for choice, p in choices.items())

    headers = ['t007', 'velocity', 'load_factor', 't008', 't009', 't010', 't011', 't012']
    rows = ''.join('<tr>' + ''.join(f'<{tag}>{E(str(value))}</{tag}>' for tag, value in zip(['th', *['td']*7], [c['name'], c['v'], c['n'], str(c['sig'])+' MPa', str(c['ang'])+'°', c['ribs'], c['top'], c['side']])) + '</tr>' for c in values['conditions'])
    components['fallback'] = f'<div class="wingbox-fallback"><p>{E(text["nojs"])}</p><div class="wingbox-table-scroll" tabindex="0" role="region" aria-label="{E(text["fallback"], quote=True)}"><table><caption>{E(text["fallback"])}</caption><thead><tr>{"".join("<th scope=col>"+E(text[h])+"</th>" for h in headers)}</tr></thead><tbody>{rows}</tbody></table></div></div>'
    components['route'] = d.flight_path(b['INNER']['route_items'](d, peers), project['id'], 'projects')
    components['pagination'] = b['INNER']['case_pagination'](d, project, peers)
    # Connect the supplied ticket to the real OS project instead of a mock link.
    next_project = next(p for p in peers if p['id'] == 'project_1')
    components['next'] = f'<a class="wingbox-next" href="{E(d.link(b["detail"](next_project)), quote=True)}">{E(next_project["title"][lang])} <span>{E(next_project["date"])}</span></a>'
    config = {'conditions': values['conditions'], 'selection': text['selection'], 'pause': text['pause'], 'resume': text['resume'],
              'modes': {o['key']: raw(o['label'], base) for o in values['controls']['modes']}}
    components['config'] = '<p class="visually-hidden" role="status" data-wing-status></p><script type="application/json" id="wingbox-data">' + json.dumps(config, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
    return fill(templates['page'], base)
