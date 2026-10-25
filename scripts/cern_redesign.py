"""CERN's supplied deep-dive design, rendered as ordinary multilingual HTML.

The prototype's dimensions and illustrations live in page.html.tmpl/cern.css. This
module supplies content, static detector geometry and progressive controls;
it does not ship the prototype's React/export runtime.
"""
import html
import json
import math
import re

E = html.escape
REPORT = 'https://zenodo.org/records/23164381'
SLIDES = 'https://indico.cern.ch/event/1707614/contributions/7181959/attachments/3327941/5960411/Emilly_PowerPoint.pptx%20(3).pdf'


def atlas_geometry():
    shapes = []

    def add(layer, w, h, ml, mt, tf, bg='transparent', bd='none', br='0', sh='none', op=1, origin='50% 50%'):
        style = f'width:{w:.1f}px;height:{h:.1f}px;margin-left:{ml:.1f}px;margin-top:{mt:.1f}px;transform:{tf};background:{bg};border:{bd};border-radius:{br};box-shadow:{sh};opacity:{op};transform-origin:{origin}'
        shapes.append(f'<span data-atlas-layer="{layer}" data-opacity="{op}" style="{E(style, quote=True)}"></span>')

    def tube(layer, r, length, n, bg, op=1, bd='none'):
        chord = 2 * r * math.sin(math.pi / n) + .8
        for i in range(n):
            add(layer, length, chord, -length / 2, -chord / 2,
                f'rotateX({i * 360 / n:.2f}deg) translateZ({r:.1f}px)', bg, bd, op=op)

    def disc(layer, r, x, bg, bd):
        add(layer, 2*r, 2*r, -r, -r, f'translateX({x}px) rotateY(90deg)', bg, bd, '50%')

    tube('muon', 150, 330, 16, 'rgba(216,204,224,0.10)', bd='1px solid rgba(216,204,224,0.35)')
    for f in range(8):
        add('muon', 300, 56, -150, -28, f'rotateX({f * 45 + 22.5}deg) translateY(112px)', 'rgba(110,90,134,0.55)', '1.5px solid #D8CCE0', '28px')
    for x in [-185, 185]:
        disc('muon', 150, x, 'transparent', '3px solid rgba(216,204,224,0.7)')
    for x in [-205, 205]:
        disc('muon', 118, x, 'transparent', '2px dashed rgba(216,204,224,0.5)')
    tube('had', 80, 230, 24, 'rgba(169,203,197,0.42)', bd='1px solid rgba(169,203,197,0.8)')
    for x in [-115, 115]:
        disc('had', 80, x, 'radial-gradient(circle, transparent 0 46%, rgba(169,203,197,0.5) 47%)', '1.5px solid #A9CBC5')
    tube('em', 56, 200, 20, 'rgba(229,140,112,0.42)', bd='1px solid rgba(242,203,174,0.8)')
    for x in [-100, 100]:
        disc('em', 56, x, 'radial-gradient(circle, transparent 0 55%, rgba(229,140,112,0.45) 56%)', '1.5px solid #F2CBAE')
    tube('inner', 34, 170, 16, 'rgba(241,226,178,0.30)', bd='1px solid rgba(241,226,178,0.75)')
    tube('beam', 3.5, 460, 8, '#F4EEE2', .9)
    tracks = [(18,30,120,'#F2CBAE'),(26,42,116,'#F2CBAE'),(10,52,112,'#F2CBAE'),(-160,200,120,'#F2CBAE'),(-150,212,114,'#F2CBAE'),(-170,222,108,'#F2CBAE'),(70,120,96,'#F1E2B2'),(80,110,92,'#F1E2B2'),(-40,300,100,'#F1E2B2'),(140,160,240,'#FFFDF8'),(-110,330,240,'#FFFDF8')]
    for z, x, length, color in tracks:
        add('tracks', length, 2, 0, -1, f'rotateX({x}deg) rotateZ({z}deg)', color, br='2px', sh=f'0 0 6px {color}', origin='0 50%')
    for angle in [0,60,120]:
        add('tracks', 14, 14, -7, -7, f'rotateY({angle}deg)', '#FFFDF8', br='50%', sh='0 0 18px 6px rgba(242,203,174,0.9)')
    return ''.join(shapes)


def render(b, lang):
    root = b['ROOT']
    design = b['DESIGN']['Design'](b, lang, 'pages/experience/cern.html')
    catalog = json.loads((root / 'content/cern-openlab/strings.json').read_text())
    t = lambda key: catalog[key][lang]
    config = json.loads((root / 'content/cern-openlab/controls.json').read_text())

    def localize(value):
        if isinstance(value, dict):
            return {key: localize(item) for key, item in value.items()}
        if isinstance(value, list):
            return [localize(item) for item in value]
        return t(value) if isinstance(value, str) and value in catalog else value

    config = localize(config)
    for value in config['visibility'].values():
        value['img'] = design.r('img/cern-openlab/' + value['img'])
    model = config['models']['v0']
    values = {'atlasNote': t('t011')}
    for key, value in config['visibility']['0'].items():
        values['vis' + key[0].upper() + key[1:]] = value
    values.update({'cm.' + key: f'{value:.1f}%' if key in ['eff','pur','acc','sel'] else value for key, value in model.items()})

    def buttons(items, kind, selected, css):
        return ''.join(f'<button type="button" class="{css}" data-{kind}="{key}" aria-pressed="{str(key == selected).lower()}">{E(item["label"])}</button>' for key, item in items.items())

    legend = ''.join(f'<button type="button" class="lg cern-layer" data-layer="{item["key"]}" aria-pressed="false"><span aria-hidden="true" style="background:{item["color"]}"></span>{E(item["label"])}</button>' for item in config['layers'])
    pause = f'<button type="button" class="cern-pause" data-atlas-pause data-cern-controls hidden aria-label="{E(config["pause"], quote=True)}" aria-pressed="false"><span aria-hidden="true">Ⅱ</span></button>'
    components = {'atlas': atlas_geometry(), 'atlasLegend': legend, 'pause': pause,
                  'visOpts': buttons(config['visibility'], 'visibility', '0', 'chip cern-choice'),
                  'models': buttons(config['models'], 'model', 'v0', 'chip cern-choice')}

    def token(match):
        key = match.group(1)
        if key.startswith('text.'):
            return E(t(key[5:]), quote=True)
        if key.startswith('asset.'):
            return E(design.r('img/cern-openlab/' + key[6:]), quote=True)
        if key.startswith('component.'):
            return components[key[10:]]
        if key == 'url.experience':
            return E(design.link('experience.html'), quote=True)
        if key in ['url.report', 'url.slides']:
            return E(REPORT if key == 'url.report' else SLIDES, quote=True)
        return E(str(values[key]), quote=True)

    body = re.sub(r'\{\{([^{}]+)\}\}', token, (root / 'content/cern-openlab/page.html.tmpl').read_text())
    # A usable first state is present even without JavaScript. The fallback table
    # retains every model, and both threshold images remain accessible.
    heads = [t(key) for key in ['t228','t133','t095','t097','t131','t132','t099','t134','t135']]
    rows = ''.join('<tr>' + ''.join(f'<{tag}>{E(str(value))}</{tag}>' for tag, value in [('th', m['name']), ('td',m['params']), *[('td',f'{m[key]:.1f}%') for key in ['eff','pur','acc','sel']], ('td',m['auc']),('td',m['dr']),('td',m['mae'])]) + '</tr>' for m in config['models'].values())
    fallback = '<noscript><div class="cern-fallback"><h3>' + E(config['comparison']) + '</h3><div class="cern-table-scroll" tabindex="0"><table><thead><tr>' + ''.join('<th scope="col">'+E(h)+'</th>' for h in heads) + '</tr></thead><tbody>' + rows + '</tbody></table></div>'
    fallback += ''.join(f'<figure><a href="{v["img"]}"><img src="{v["img"]}" alt="{E(v["alt"], quote=True)}" loading="lazy" width="869" height="721"></a><figcaption>{E(v["label"])} · {E(v["note"])}</figcaption></figure>' for v in config['visibility'].values()) + '</div></noscript>'
    dialog = f'''<dialog class="photo-dialog" aria-label="{E(config['figure'])}" data-photo-label="{E(config['figure'])}" data-of-label="{E(config['of'])}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{E(config['close'])} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{E(config['previous'])}">{b['icon']('previous')}</button><button type="button" data-photo-next aria-label="{E(config['next'])}">{b['icon']('next')}</button></div></dialog>'''
    data = json.dumps(config, ensure_ascii=False).replace('<', '\\u003c')
    body = body.replace('</main>', fallback + f'<script type="application/json" id="cern-data">{data}</script></main>' + dialog)
    return body, t('t004'), t('t005')
