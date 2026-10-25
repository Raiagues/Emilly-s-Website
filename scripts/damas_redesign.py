"""Render the supplied Damas design with shared navigation and the original C engine."""
import html
import json
import re

E = html.escape


def render(b, p, lang):
    root = b['ROOT']
    d = b['DESIGN']['Design'](b, lang, b['detail'](p))
    catalog = json.loads((root / 'content/damas-espaciais/strings.json').read_text())
    assert all(set(value) == set(b['LANGS']) for value in catalog.values())
    t = lambda key: catalog[key][lang]
    config = json.loads((root / 'content/damas-espaciais/controls.json').read_text())

    def localize(value):
        if isinstance(value, dict):
            return {key: localize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [localize(item) for item in value]
        return t(value) if isinstance(value, str) and value in catalog else value

    # Step keys are identifiers, not translatable words.
    step_keys = [step['key'] for step in config['steps']]
    config = localize(config)
    for step, key in zip(config['steps'], step_keys):
        step['key'] = key
    config['engine'] = b['asset_url'](d.current, 'src/damas-engine/game.wasm')
    config['pieces'] = ['', *[d.r('img/damas-espaciais/' + name + '.png') for name in ['blue', 'pink', 'blue-king', 'pink-king']]]
    for screen in config['screens'].values():
        screen['image'] = d.r('img/damas-espaciais/' + screen['image'])
    names = [config['text'][key] for key in ['empty', 'blue', 'pink', 'blueKing', 'pinkKing']]
    rows = []
    for row in range(8):
        cells = []
        for col in range(8):
            piece = (1 if row < 3 else 2 if row > 4 else 0) if (row + col) % 2 else 0
            image = f'<img src="{config["pieces"][piece]}" alt="" width="80" height="80" draggable="false">' if piece else ''
            label = f'{chr(65+col)}{row+1}, {names[piece]}'
            cells.append(f'<button type="button" class="cell" role="gridcell" data-cell="{row*8+col}" data-piece="{piece}" aria-selected="false" aria-label="{E(label,quote=True)}" tabindex="-1" disabled>{image}<span class="cell-number" aria-hidden="true" hidden>{piece}</span></button>')
        rows.append('<div role="row">' + ''.join(cells) + '</div>')
    steps = ''.join(f'<li data-check="{step["key"]}" data-state="idle"><span class="check-icon" aria-hidden="true">·</span><span><span class="check-label">{E(step["label"])}</span><span class="visually-hidden check-status"></span><code>{E(step["code"])}</code></span></li>' for step in config['steps'])
    nodes = ''.join(f'<button type="button" class="node" disabled data-screen="{key}" aria-pressed="{str(key=="PLAY").lower()}" style="grid-column:{screen["col"]};grid-row:{screen["row"]}"><strong>{key}</strong><small>{E(screen["sub"])}</small>{"<span class=screen-arrow aria-hidden=true>→</span>" if key in ["MENU","COUNTDOWN","PLAY"] else ""}{"<span class=screen-return aria-hidden=true>↕</span>" if key=="RULES" else ""}</button>' for key, screen in config['screens'].items())
    versions = ''.join(f'<button type="button" class="tog" data-version="{year}" aria-pressed="{str(year=="2021").lower()}">{E(t("version"+year))}</button>' for year in ['2021','2026'])
    peers = [q for q in b['PROJECTS'] if q['kind'] == 'projects']
    components = {'board': ''.join(rows), 'steps': steps, 'nodes': nodes, 'versions': versions,
                  'route': d.flight_path(b['INNER']['route_items'](d, peers), p['id'], 'projects'),
                  'pagination': b['INNER']['case_pagination'](d, p, peers),
                  'config': '<script type="application/json" id="damas-data">' + json.dumps(config, ensure_ascii=False).replace('<', '\\u003c') + '</script>'}

    def token(match):
        key = match.group(1)
        if key.startswith('text.'):
            return E(t(key[5:]), quote=True)
        if key.startswith('asset.'):
            return E(d.r('img/damas-espaciais/' + key[6:]), quote=True)
        if key.startswith('component.'):
            return components[key[10:]]
        if key == 'url.projects':
            return E(d.link('projects.html'), quote=True)
        raise ValueError('Unknown Damas template token: ' + key)

    template = (root / 'content/damas-espaciais/page.html.tmpl').read_text()
    return re.sub(r'\{\{([^{}]+)\}\}', token, template)
