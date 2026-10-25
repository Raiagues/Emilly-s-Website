"""Postcard rack adapted from the owner's supplied HTML, with real diary entries."""
import html

E = html.escape
LABELS = {
    'all': ('All', 'Todas as', 'Toutes les', 'Todas las'),
    'stories': ('Stories', 'Histórias', 'Histoires', 'Historias'),
    'postcards': ('postcards', 'cartões-postais', 'cartes postales', 'postales'),
    'intro': ('Places I got to know, people I met and ideas I brought back. A collection of postcards, each with a story to read.', 'Lugares que conheci, pessoas que encontrei e ideias que trouxe comigo. Uma coleção de cartões-postais, cada um com uma história para contar.', 'Des lieux découverts, des rencontres et des idées rapportées. Une collection de cartes postales, chacune avec son histoire.', 'Lugares que conocí, personas que encontré e ideas que traje conmigo. Una colección de postales, cada una con una historia que contar.'),
    'route': ('Every stop in the diary', 'As paradas deste diário', 'Les étapes du journal', 'Las paradas del diario'),
    'newest': ('Newest first', 'Mais recentes', 'Les plus récentes', 'Más recientes'),
    'oldest': ('Oldest first', 'Mais antigas', 'Les plus anciennes', 'Más antiguas'),
    'latest': ('Latest postcard', 'Novo cartão-postal', 'Dernière carte', 'Última postal'),
    'more': ('More postcards', 'Mais cartões-postais', 'Plus de cartes', 'Más postales'),
    'continue': ('Keep exploring', 'Continue pelo diário', 'Poursuivre le voyage', 'Sigue por el diario'),
    'preview': ('Hover or focus on a title to explore', 'Passe pelos títulos para descobrir', 'Survolez un titre pour découvrir', 'Recorre los títulos para descubrir'),
    'previous': ('Previous stories', 'Histórias anteriores', 'Histoires précédentes', 'Historias anteriores'),
    'next': ('Next stories', 'Próximas histórias', 'Histoires suivantes', 'Historias siguientes'),
}
PLACES = {
    'cern': ('Geneva, Switzerland', 'Genebra, Suíça', 'Genève, Suisse', 'Ginebra, Suiza'),
    'estados-unidos': ('United States', 'Estados Unidos', 'États-Unis', 'Estados Unidos'),
    'south-summit': ('Porto Alegre, Brazil', 'Porto Alegre, Brasil', 'Porto Alegre, Brésil', 'Porto Alegre, Brasil'),
    'china': ('Beijing & Shanghai', 'Pequim e Xangai', 'Pékin et Shanghai', 'Pekín y Shanghái'),
    'premio-na-pratica': ('São Paulo, Brazil', 'São Paulo, Brasil', 'São Paulo, Brésil', 'São Paulo, Brasil'),
    'fundacao-estudar': ('Brazil', 'Brasil', 'Brésil', 'Brasil'),
    'visiona': ('Brazil', 'Brasil', 'Brésil', 'Brasil'),
    'cnes': ('Toulouse, France', 'Toulouse, França', 'Toulouse, France', 'Toulouse, Francia'),
    'brafitec': ('Grenoble, France', 'Grenoble, França', 'Grenoble, France', 'Grenoble, Francia'),
}

def label(key, lang):
    return LABELS[key][('en', 'pt', 'fr', 'es').index(lang)]

def place_for(post, lang):
    if post['slug'] in PLACES:
        return PLACES[post['slug']][('en','pt','fr','es').index(lang)]
    location = post.get('location', {})
    return location.get(lang, location.get('en', '')) if isinstance(location, dict) else location

def date_of(post):
    return max((e['date'] for e in post.get('timeline', [])), default=post['date'])

def explorer(b, d, current):
    posts = sorted(b['POSTS'], key=date_of)
    stops, panels = [], []
    for i, post in enumerate(posts):
        selected = post['slug'] == current
        photo = post['photos'][post['cover'][-1]]
        target = d.link(b['J']['path'](post))
        panel = 'story-preview-' + post['slug']
        stops.append(f'<a class="flight-stop story-stop" data-flight-stop data-date="{date_of(post)}" data-preview="{panel}" href="{target}" {"aria-current=\"page\"" if selected else ""}><span class="mono">{date_of(post)[:4]} · {i + 1:02}</span><strong>{d.local(post["title"])}</strong></a>')
        action = f'<span class="flight-here">{d.u("here")}</span>' if selected else d.button(d.local(b['JUI']['read']), target, True)
        panels.append(f'<article class="flight-preview story-explorer-preview" id="{panel}" {"" if selected else "hidden"}><div class="explorer-photo">{b["J"]["photo_html"](photo,d.lang,d.current)}</div><div class="explorer-copy"><p class="eyebrow">{d.local(post["period"])}</p><h3>{d.local(post["title"])}</h3><p>{d.local(post["subtitle"])}</p>{action}</div></article>')
    return f'''<section class="flight-path story-explorer" aria-labelledby="flight-title"><div class="explorer-heading"><div><p class="eyebrow">{d.local(b['JUI']['home'])}</p><h2 id="flight-title">{label('continue',d.lang)}</h2></div>{d.button(label('all',d.lang)+' '+label('stories',d.lang).lower()+f' · {len(posts)}',d.link('journal.html'))}</div><div class="explorer-layout"><div class="explorer-stops"><p class="mono explorer-hint">{label('preview',d.lang)}</p><nav class="flight-map" aria-label="{d.u('route')}">{''.join(stops)}</nav><div class="explorer-controls" hidden><button type="button" data-story-prev aria-label="{label('previous',d.lang)}">↑</button><button type="button" data-story-next aria-label="{label('next',d.lang)}">↓</button></div></div><div class="flight-previews">{''.join(panels)}</div></div></section>'''

def render(b, lang):
    d = b['DESIGN']['Design'](b, lang, 'journal.html')
    posts, journal, ui = b['POSTS'], b['J'], b['JUI']
    u = lambda key: label(key,lang)
    title = u('all') + ' ' + u('stories').lower()
    cards, stops = [], []
    for i, post in enumerate(posts):
        photo = min((post['photos'][key] for key in post['cover']), key=lambda image: image['width']/image['height'])
        place = place_for(post, lang)
        date = date_of(post)
        stops.append(f'<li data-date="{date}"><a href="#archive-{post["slug"]}" class="rack-stop" {"aria-current=\"location\"" if i == 0 else ""}><span class="rack-dot">{i+1:02}</span><time datetime="{date}">{date[:4]}</time><span class="rack-tooltip">{d.local(post["title"])}</span></a></li>')
        cards.append(f'''<li id="archive-{post['slug']}" data-date="{date}"><a class="postcard-card postcard-colour-{i%4}" href="{d.link(journal['path'](post))}" aria-label="{d.local(post['title'])}">{f'<span class="postcard-latest">{u("latest")}</span>' if i==0 else ''}<span class="postcard-tape" aria-hidden="true"></span><div class="postcard-photo">{journal['photo_html'](photo,lang,d.current)}{f"<span>{E(place)}</span>" if place else ""}</div><div class="postcard-copy"><div class="postcard-meta"><p class="eyebrow">{d.local(post['period'])}</p><span class="postcard-stamp" aria-hidden="true"><span>Par avion</span><strong>{i+1:02}</strong></span></div><h2>{d.local(post['title'])}</h2><p>{d.local(post['intro'])}</p><div class="postcard-read"><span class="more">{d.local(ui['read'])}{b['DESIGN']['ARROW']}</span><span class="mono">{i+1:02} / {len(posts):02}</span></div></div></a></li>''')
    return f'''<main id="main" class="wrap inner-content journal-archive-page"><div class="inner-breadcrumb">{d.button(d.u('home'),d.link('index.html#journal'),back=True)}<span class="mono">{d.local(ui['home'])} · Par avion</span></div><header class="rack-heading"><div><p class="eyebrow">{d.local(ui['home'])} · {len(posts)} {u('postcards')}</p><h1><span>{u('all')}</span><strong>{u('stories')}</strong></h1><p>{u('intro')}</p></div><div class="rack-illustration" aria-hidden="true">{d.drawing('postcard-rack')}</div></header><section class="rack-route" aria-labelledby="rack-route-title"><div class="rack-route-heading"><h2 id="rack-route-title">{u('route')}</h2><div class="rack-sort" role="group" aria-label="{u('route')}" hidden><button type="button" class="chip" data-story-order="newest" aria-pressed="true">{u('newest')}</button><button type="button" class="chip" data-story-order="oldest" aria-pressed="false">{u('oldest')}</button></div></div><nav aria-label="{u('route')}"><ol class="rack-route-stops">{''.join(stops)}</ol></nav></section><section class="story-archive postcard-rack" aria-label="{title}"><ol>{''.join(cards)}</ol><button type="button" class="btn rack-more" hidden>{u('more')}{b['DESIGN']['ARROW']}</button></section></main>'''
