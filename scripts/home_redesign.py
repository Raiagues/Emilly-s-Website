"""Production home renderer. Content comes unchanged from the existing catalogues.

The prototype supplies presentation, never biographical data. New strings below
are interface labels only, with the same four locales as the existing site.
"""
import html
import re
import runpy

E = html.escape
LABELS = {
    'latest_stop': ('Latest stop', 'Última parada', 'Dernière escale', 'Última parada'),
    'route': ('Flight path', 'Trajetória', 'Itinéraire', 'Trayectoria'),
    'ticket': ('Latest boarding pass', 'Último cartão de embarque', 'Dernière carte d’embarquement', 'Última tarjeta de embarque'),
    'on_air': ('Now on air', 'Agora no ar', 'En ce moment', 'Ahora al aire'),
    'all_stories': ('All stories', 'Todas as histórias', 'Toutes les histoires', 'Todas las historias'),
    'departure': ('Departure', 'Partida', 'Départ', 'Salida'),
    'destination': ('Next destination', 'Próximo destino', 'Prochaine destination', 'Próximo destino'),
    'pass': ('Boarding pass', 'Cartão de embarque', 'Carte d’embarquement', 'Tarjeta de embarque'),
    'media': ('On air & in print', 'No ar e nas páginas', 'À l’antenne et dans la presse', 'Al aire y en la prensa'),
    'newsletter': ('The dispatch', 'Cartas de bordo', 'Le courrier de bord', 'Cartas de a bordo'),
    'newsletter_label': ('Newsletter', 'Newsletter', 'Lettre d’information', 'Boletín'),
    'topics': ('Choose your topics', 'Escolha os assuntos', 'Choisissez vos sujets', 'Elige los temas'),
    'diary_topic': ('Diary stories', 'Histórias do diário', 'Récits du journal', 'Historias del diario'),
    'project_topic': ('Projects and research', 'Projetos e pesquisa', 'Projets et recherche', 'Proyectos e investigación'),
    'media_topic': ('Talks and media', 'Palestras e mídia', 'Conférences et médias', 'Charlas y medios'),
    'frequency': ('Delivery frequency', 'Frequência de envio', 'Fréquence d’envoi', 'Frecuencia de envío'),
    'three': ('Every 3 months', 'A cada 3 meses', 'Tous les 3 mois', 'Cada 3 meses'),
    'six': ('Every 6 months', 'A cada 6 meses', 'Tous les 6 mois', 'Cada 6 meses'),
    'subscribe': ('Subscribe', 'Assinar', 'S’abonner', 'Suscribirse'),
    'unavailable': ('Subscriptions are not open yet. No email addresses are collected.', 'As inscrições ainda não estão abertas. Nenhum e-mail é coletado.', 'Les inscriptions ne sont pas encore ouvertes. Aucune adresse e-mail n’est collectée.', 'Las suscripciones aún no están abiertas. No se recopilan correos electrónicos.'),
}


def render(b, lang):
    d, posts, j, jui = (b[k] for k in ('D', 'POSTS', 'J', 'JUI'))
    current = b['loc']('index.html', lang)
    r = lambda x: b['relative'](current, x)
    link = lambda x: b['href'](current, x, lang)
    t = lambda k: b['txt'](k, lang)
    u = lambda k: LABELS[k][('en', 'pt', 'fr', 'es').index(lang)]
    jt = lambda k: E(j['text'](jui[k], lang))
    localized = lambda value: E(j['text'](value, lang))
    illustration_count = 0

    def drawing(name):
        """Port the prototype's vector artwork, with unique SVG IDs per instance."""
        nonlocal illustration_count
        illustration_count += 1
        svg = (b['ROOT'] / f'img/redesign/{name}.svg').read_text()
        for identifier in re.findall(r'\bid="([^"]+)"', svg):
            unique = f'home-{illustration_count}-{identifier}'
            svg = svg.replace(f'id="{identifier}"', f'id="{unique}"')
            svg = svg.replace(f'url(#{identifier})', f'url(#{unique})')
            svg = svg.replace(f'href="#{identifier}"', f'href="#{unique}"')
        opening = re.match(r'<svg\b[^>]*>', svg).group()
        # Positioning belongs to the production component, not the template slot.
        clean = re.sub(r'\s(?:style|class|aria-hidden)="[^"]*"', '', opening)
        clean = clean.replace('<svg ', '<svg class="illustration" aria-hidden="true" ', 1)
        return clean + svg[len(opening):]

    def art(name):
        original = {'platform': 'flight-console', 'satellite': 'project-satellite',
                    'chip': 'project-chip', 'outreach': 'project-outreach',
                    'rover': 'project-rover', 'aircraft': 'project-aircraft',
                    'code': 'project-code', 'detector': 'experience-detector'}
        return drawing(original[name]) if name in original else b['art'](name)
    icon = b['icon']
    projects = [p for p in b['PROJECTS'] if p['kind'] == 'projects']
    featured = next(p for p in projects if p['id'] == 'flight-platform')
    selected = [p for p in projects if p != featured][:3]
    experiences = sorted((p for p in b['PROJECTS'] if p['kind'] == 'experience'),
                         key=lambda p: tuple(int(x) for x in re.findall(r'\d{4}', p['date'])))
    latest = experiences[-1]
    arrow = '<span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-5-5 5 5-5 5"/></svg></span>'
    rocket = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 2c3 3 4 7 4 11l-4 3-4-3c0-4 1-8 4-11z" fill="#FBF8F1"/><circle cx="12" cy="9" r="1.5" fill="#1F4A4F"/><path d="m8 13-3 3 3 1m8-4 3 3-3 1" fill="#D9694E"/><path d="m10 18 2 4 2-4" stroke="#B04A32"/></svg>'

    def button(label, target, solid=False, extra=''):
        return f'<a class="btn {"btn-solid" if solid else ""}" href="{E(target, quote=True)}" {extra}>{label}{arrow}</a>'

    def keywords(values):
        return '<div class="keywords">' + ''.join(f'<span>{E(v)}</span>' for v in values) + '</div>'

    def section_heading(number, title, extra=''):
        return f'<div class="section-heading"><span class="section-number">{number:02}</span><h2>{title}</h2>{extra}</div>'

    def polaroid(photo, cls='', eager=False):
        return f'<figure class="polaroid {cls}">{j["photo_html"](photo, lang, current, eager)}<figcaption>{localized(photo["caption"])}</figcaption></figure>'

    def item_image(p, cls=''):
        # These are illustrated slots in the prototype, including experiences.
        return f'<div class="art {cls}" aria-hidden="true">{art(p["art"])}</div>'

    design = b['DESIGN']['Design'](b, lang, 'index.html')
    nav_sections = [('current-work', t('projects')), ('experience', t('experience')), ('my-story', design.u('about_nav')), ('journal', jt('home')), ('say-hello', t('contact'))]
    nav = ''.join(f'<a href="#{key}">{label}</a>' for key, label in nav_sections)
    top = f'''<header class="home-header"><div class="airmail-line" aria-hidden="true"></div>
<div class="wrap navigation"><a class="brand" href="{link('index.html')}" aria-label="{design.u('home')}"><span class="brand-icon">{rocket}</span></a><nav id="main-nav" aria-label="{t('menu')}">{nav}</nav>{design.language_selector()}</div></header>'''

    hero = f'''<section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><h1 id="hero-title">Emilly Rodrigues</h1><p class="hero-description">{t('hero_body')}</p></div>
<figure class="polaroid portrait"><div class="portrait-paper"><img src="{r('img/me.png')}" alt="{t('portrait')}" width="484" height="718" fetchpriority="high"></div></figure></section>'''

    route_stops = [('UFSM', link('about.html')), ('Grenoble INP', link('journal/brafitec.html')), ('CNES', link('pages/experience/cnes.html')), ('CERN', link('pages/experience/cern.html'))]
    route = f'''<div class="journey-strip"><div class="route-card"><span class="eyebrow">{u('route')}</span><div class="route-map"><svg viewBox="0 0 400 220" preserveAspectRatio="none" aria-hidden="true"><path d="M35 155C65 75 95 55 130 65S190 150 220 145S270 40 295 50" fill="none" stroke="#1F4A4F" stroke-width="2" stroke-dasharray="6 6"/></svg>{''.join(f'<a href="{url}" class="route-stop stop-{i}"><span aria-hidden="true"></span>{label}</a>' for i, (label, url) in enumerate(route_stops))}</div></div>
<a class="mini-ticket" href="{link(b['detail'](latest))}"><div class="mini-ticket-copy"><span class="eyebrow">{u('latest_stop')}</span><strong>{E(latest['place'])}</strong><span class="mono">{latest['date']}</span></div><div class="mini-ticket-stub">{arrow}</div></a>
<a class="on-air" href="{link(b['detail'](featured))}"><div class="on-air-copy"><span class="eyebrow">{t('current_work')}</span><p>{t('current_title')}</p><span class="more">{t('case')}{arrow}</span></div></a></div>'''

    stories = []
    for i, post in enumerate(posts[:2]):
        images = [post['photos'][post['cover'][-1]], post['photos'][post['cover'][0]]]
        stories.append(f'''<article class="story-preview" id="journal-{post['slug']}"><div class="story-preview-copy"><p class="eyebrow">{localized(post['period'])} <span class="story-count">{i+1:02} / {len(posts):02}</span></p><h3><a href="{link(j['path'](post))}">{localized(post['title'])}</a></h3><p>{localized(post['intro'])}</p>{button(jt('read'), link(j['path'](post)))}</div><div class="story-photos">{polaroid(images[0], 'photo-main')}{polaroid(images[1], 'photo-small')}</div></article>''')
    archive = ''.join(f'<li id="archive-{post["slug"]}"><a href="{link(j["path"](post))}"><span class="mono">{localized(post["period"])}</span><span>{localized(post["title"])}</span>{arrow}</a></li>' for post in posts)
    events = sorted(((event, post) for post in posts for event in post.get('timeline', [])), key=lambda pair: pair[0]['date'], reverse=True)
    timeline = ''.join(f'<li><time datetime="{event["date"]}">{localized(event["label"])}</time><a href="{link(j["path"](post))}{"#" + event["section"] if event.get("section") else ""}">{localized(event["title"])}</a></li>' for event, post in events)
    diary = f'<section id="journal">{section_heading(1, jt("home"), f'<a class="section-related" href="#media">{u("media")}{arrow}</a>')}{"".join(stories)}<details class="story-archive"><summary class="btn">{u("all_stories")} <span class="archive-count">{len(posts):02}</span>{arrow}</summary><ol>{archive}</ol><details class="journal-timeline"><summary>{jt("timeline")}</summary><nav aria-label="{jt("timeline")}"><ol>{timeline}</ol></nav></details></details></section>'

    cards = ''.join(f'''<a class="project-card" href="{link(b['detail'](p))}" data-featured-project="{p['id']}">{item_image(p)}<p class="eyebrow">{t(p['category'])} · {p['date']}</p><h3>{p['title'][lang]}</h3><p>{p['summary'][lang]}</p>{keywords(p['tech'])}<span class="more">{t('case')}{arrow}</span></a>''' for p in selected)
    current_work = f'''<section id="current-work">{section_heading(2, t('projects'))}<article class="current-panel"><div class="current-copy"><p class="eyebrow">{u('on_air')}  {featured['date']}</p><h3>{t('current_title')}</h3><p>{featured['summary'][lang]}</p><p class="current-outcome">{featured['outcome'][lang]}</p>{keywords(featured['tech'])}{button(t('case'), link(b['detail'](featured)))}</div>{item_image(featured, 'current-art')}</article><div class="project-grid">{cards}<a class="project-deck" href="{link('projects.html')}"><div class="deck-stack"><span aria-hidden="true"></span><span aria-hidden="true"></span><span>{drawing('deck-satellite')}<strong>+{len(projects)-len(selected)-1}</strong><span class="mono">{t('more_projects')}</span></span></div><span class="more">{t('all_projects')}{arrow}</span></a></div></section>'''

    passes = []
    for i, p in reversed(list(enumerate(experiences))):
        successor = experiences[i+1] if i+1 < len(experiences) else None
        departure_year = re.search(r'\d{4}', p['date']).group()
        # Use the next real experience. The newest pass has no invented future stop.
        destination = f'<div><span class="mono">{u("destination")}</span><strong class="next-destination">{E(successor["place"])}</strong></div>' if successor else ''
        passes.append(f'''<a class="boarding-pass" data-experience="{p['category']}" href="{link(b['detail'](p))}">{item_image(p)}<div class="pass-copy"><p class="eyebrow">{E(p['place'])} · {p['date']}</p><h3>{p['title'][lang]}</h3><p>{p['summary'][lang]}</p>{keywords(p['tech'])}</div><div class="pass-stub"><div><span class="mono">{u('departure')}</span><strong>{departure_year}</strong></div>{destination}<span class="more">{t('read')}{arrow}</span></div></a>''')
    categories = list(dict.fromkeys(p['category'] for p in reversed(experiences)))
    filters = ''.join(f'<button type="button" class="chip" data-experience-filter="{key}" aria-pressed="{str(key == "all").lower()}">{t(key)}</button>' for key in ['all', *categories])
    experience = f'<section id="experience">{section_heading(3, t("experience"))}<div class="experience-filters" role="group" aria-label="{t("filter_label")}" hidden>{filters}</div><div class="boarding-passes">{"".join(passes)}</div><div class="section-end">{button(t("all_experience"), link("experience.html"))}</div></section>'

    about = f'''<section id="my-story" aria-labelledby="about-title"><div class="envelope"><div class="envelope-sheet"><div class="envelope-copy"><p class="eyebrow">Par avion · 04 / {t('about')}</p><h2 id="about-title">{t('personal_title').replace('<br>', ' ')}</h2><p>{t('about_p1')}</p><div class="letter-lines"><p>{t('degree1')}</p><p>{t('degree2')}</p><p>{t('languages')}</p></div><div class="about-links">{button(t('more_about'), link('about.html'))}<a class="section-related" href="#recognition">{t('recognition')}{arrow}</a></div></div><div class="about-aside"><figure class="portrait-stamp"><div class="portrait-stamp-inner"><span class="portrait-number" aria-hidden="true">No. 04</span><div class="portrait-paper"><img src="{r('img/me.png')}" alt="{t('portrait')}" width="484" height="718" loading="lazy"></div></div></figure></div></div></div></section>'''

    award_cards = []
    stamp_art = ['rocket', 'satellite', 'planet', 'satellite']
    for i, (date, name, description, url) in enumerate(d['AWARDS']):
        related = next((post for post in posts if post.get('related_award') == name), None)
        target = url or (link(j['path'](related)) if related else link('recognition.html'))
        external = 'target="_blank" rel="noopener noreferrer"' if url else ''
        award_cards.append(f'''<a class="award-card" href="{target}" {external}><div class="stamp-holder"><div class="stamp stamp-{i % 4}"><div class="stamp-inner"><span class="stamp-year">{E(date)}</span>{drawing("stamp-" + stamp_art[i % 4])}<span class="stamp-name">{E(name)}</span></div></div></div><h3>{E(name)}</h3><p>{description[lang]}</p><span class="more">{t('source')}{arrow}</span></a>''')
    awards = f'<section id="recognition">{section_heading(5, t("recognition"))}<div class="award-grid">{"".join(award_cards)}</div></section>'

    media_body = runpy.run_path(str(b['ROOT'] / 'scripts/media_redesign.py'))['render'](b['ROOT'], lang, r, drawing, arrow)
    media = f'<section id="media">{section_heading(6, u("media"))}{media_body}</section>'

    topics = ''.join(f'<label class="topic"><input type="checkbox" name="topic" value="{key}" checked><span>{u(key)}</span></label>' for key in ['diary_topic', 'project_topic', 'media_topic'])
    frequencies = ''.join(f'<label class="frequency-stamp"><input type="radio" name="frequency" value="{n}" {"checked" if n == 3 else ""}><span class="frequency-paper"><span class="frequency-inner">{drawing("guide-about" if n == 3 else "guide-projects")}<strong>{n}</strong><span>{u(key)}</span></span></span><svg class="frequency-mark" viewBox="0 0 120 70" aria-hidden="true"><circle cx="38" cy="35" r="26"/><circle cx="38" cy="35" r="20"/><path d="m27 35 7 7 15-17M63 23q12-7 24 0t24 0M63 33q12-7 24 0t24 0M63 43q12-7 24 0t24 0"/></svg></label>' for n, key in [(3, 'three'), (6, 'six')])
    # Deliberately not a submitting form. Existing FormSubmit is contact-only.
    newsletter = f'''<section id="newsletter" class="newsletter"><div class="newsletter-intro"><div class="postcard-art" aria-hidden="true">{drawing('postcard')}</div><div class="postcard-title"><p class="eyebrow">{u('newsletter_label')}</p><h2>{u('newsletter')}</h2></div></div><div class="postcard"><p class="eyebrow">{u('newsletter_label')} </p><p id="newsletter-status">{u('unavailable')}</p><div class="postcard-options"><fieldset><legend>{u('topics')}</legend><div class="topics">{topics}</div></fieldset><fieldset class="frequency-field"><legend>{u('frequency')}</legend><div class="frequencies">{frequencies}</div></fieldset></div><div class="address-lines" aria-hidden="true"><span></span><span></span></div><label for="newsletter-email" class="mono">{t('email')}</label><div class="newsletter-send"><input id="newsletter-email" type="email" disabled aria-describedby="newsletter-status"><button type="button" class="btn btn-solid" disabled aria-describedby="newsletter-status">{u('subscribe')}{arrow}</button></div></div></section>'''

    contact = f'''<section id="say-hello" class="contact-section"><div><p class="eyebrow">{t('contact')}</p><h2>{t('contact_title')}</h2><p>{t('contact_body')}</p><div class="actions">{button(t('send'), link('contact.html'), True)}{button(t('cv'), r('CV_Emilly.pdf'), extra='download')}</div></div><div class="tag-holder"><svg class="tag-string" viewBox="0 0 160 80" aria-hidden="true"><path d="M154 61C105 13 77 78 23 47S37 6 69 22S94 76 154 61" fill="none" stroke="#B04A32" stroke-width="2"/></svg><div class="luggage-tag"><span class="tag-hole" aria-hidden="true"></span><div class="tag-heading"><span class="mono">{t('direct')}</span></div><a class="contact-email" href="mailto:{d['EMAIL']}">{d['EMAIL']}</a><nav class="social-links" aria-label="{t('contact')}"><a href="{d['LINKEDIN']}" target="_blank" rel="noopener noreferrer">LinkedIn {arrow}</a><a href="{d['GITHUB']}" target="_blank" rel="noopener noreferrer">GitHub {arrow}</a></nav><div class="barcode" aria-hidden="true"></div></div></div></section>'''

    footer = f'<footer class="wrap footer"><span>© 2026 Emilly Rodrigues · {t("footer_note")}</span><a href="#top">{t("top")}{arrow}</a></footer>'
    return top + '<main id="main" class="wrap home-content">' + hero + route + diary + current_work + experience + about + awards + media + newsletter + contact + '</main>' + footer
