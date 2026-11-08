"""Render the supplied ITA formation design with readable static initial states."""
import html
import json
import re

TOKEN = re.compile(r'\{\{([\w.-]+)\}\}')
LOOP = re.compile(r'<sc-for\s+as="(\w+)"\s+list="\{\{([\w.]+)\}\}">')


def render(b, project, lang):
    root = b['ROOT'] / 'content/ita-formation'
    d = b['DESIGN']['Design'](b, lang, b['detail'](project))
    catalog = json.loads((root / 'strings.json').read_text())
    assert all(set(row) == set(b['LANGS']) and all(row.values()) for row in catalog.values())
    text = {k: row[lang] for k, row in catalog.items()}
    translations = {row['en']: row[lang] for row in catalog.values()}
    values = json.loads((root / 'default.json').read_text())
    names = ['models', 'matrix', 'filter', 'lab', 'control']
    templates = {name: (root / (name + '.html.tmpl')).read_text() for name in names}
    components = {}
    context = {**values, 'text': text, 'component': components, 'url': {
        'experience': d.link('experience.html'), 'wingbox': d.link('pages/projects/wing-box-analysis.html')}}

    def lookup(key, ctx):
        obj = ctx
        for part in key.split('.'):
            obj = obj[part]
        return obj

    def raw(value, ctx):
        value = translations.get(str(value), str(value))
        return TOKEN.sub(lambda m: raw(lookup(m[1], ctx), ctx), value)

    def fill(template, ctx):
        while (match := LOOP.search(template)):
            depth = 1
            for tag in re.finditer(r'<sc-for\b[^>]*>|</sc-for>', template[match.end():]):
                depth += -1 if tag[0].startswith('</') else 1
                if depth == 0:
                    start, end = match.end() + tag.start(), match.end() + tag.end()
                    break
            if depth:
                raise ValueError('Unclosed formation template loop')
            body = template[match.end():start]
            result = ''.join(fill(body, {**ctx, match[1]: item}) for item in lookup(match[2], ctx))
            template = template[:match.start()] + result + template[end:]
        return TOKEN.sub(lambda m: str(lookup(m[1], ctx)) if m[1].startswith('component.') else html.escape(raw(lookup(m[1], ctx), ctx), quote=True), template)

    for name in names:
        components[name] = fill(templates[name], context).replace('<button ', '<button disabled ')
    peers = [p for p in b['PROJECTS'] if p['kind'] == 'experience']
    components['route'] = d.flight_path(b['INNER']['route_items'](d, peers), project['id'], 'experience')
    components['pagination'] = b['INNER']['case_pagination'](d, project, peers)
    config = {'text': text, 'translations': translations, 'templates': templates, 'worker': d.r('src/formation-worker.js')}
    components['config'] = '<p class="formation-status" role="status" data-formation-status></p><script type="application/json" id="formation-data">' + json.dumps(config, ensure_ascii=False).replace('<', '\\u003c') + '</script>'
    return fill((root / 'page.html.tmpl').read_text(), context)
