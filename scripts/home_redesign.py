"""Home layout using the supplied illustrations and multilingual catalogue.

Personal copy follows the owner's brief; reference placeholders are never facts.
"""
import html
import re
import runpy

E = html.escape
LABELS = {
    'details': ('Details', 'Detalhes', 'Détails', 'Detalles'),
    'guide': ('Flight guide', 'Guia de voo', 'Guide de vol', 'Guía de vuelo'),
    'pause': ('Pause animation', 'Pausar animação', 'Mettre en pause', 'Pausar animación'),
    'play': ('Play animation', 'Reproduzir animação', 'Lire l’animation', 'Reproducir animación'),
    'portrait_caption': ('A visit to the lab.', 'Uma visita ao laboratório.', 'Une visite au laboratoire.', 'Una visita al laboratorio.'),
    'all_awards': ('All awards', 'Todas as conquistas', 'Toutes les distinctions', 'Todos los reconocimientos'),
    'personal_title': ('Beyond the projects.', 'Além dos projetos.', 'Au-delà des projets.', 'Más allá de los proyectos.'),
    'personal_body': ('I was born in Jaru, Rondônia, Brazil. I enjoy discovering places, hiking in the mountains and meeting people with different perspectives. This is where I keep some of those encounters alongside the things I build.', 'Nasci em Jaru, Rondônia. Gosto de conhecer lugares, caminhar nas montanhas e aprender com pessoas de contextos diferentes. Por aqui, reúno um pouco desses encontros e do que construo pelo caminho.', 'Je suis née à Jaru, dans le Rondônia, au Brésil. J’aime découvrir des lieux, marcher en montagne et rencontrer des personnes aux parcours différents. Je rassemble ici quelques-unes de ces rencontres et les projets que je construis.', 'Nací en Jaru, Rondônia, Brasil. Me gusta descubrir lugares, caminar por las montañas y conocer personas con distintas perspectivas. Aquí reúno algunos de esos encuentros y los proyectos que voy construyendo.'),
    'from': ('From', 'De', 'De', 'De'),
    'to': ('To', 'Para', 'Vers', 'Hacia'),
    'personal_destination': ('New ideas, projects and places', 'Novas ideias, projetos e lugares', 'De nouvelles idées, projets et lieux', 'Nuevas ideas, proyectos y lugares'),
    'dear_reader': ('Dear reader,', 'Olá,', 'Chère lectrice, cher lecteur,', 'Hola,'),
    'letter_body': ('A short letter every few months, with new diary stories, projects in progress and discoveries along the way.', 'Uma carta de tempos em tempos, com novas histórias do diário, projetos em andamento e descobertas pelo caminho.', 'Une courte lettre de temps en temps, avec de nouveaux récits, des projets en cours et des découvertes en chemin.', 'Una carta de vez en cuando, con nuevas historias, proyectos en marcha y descubrimientos por el camino.'),
    'letter_by': ('by Emilly Rodrigues', 'por Emilly Rodrigues', 'par Emilly Rodrigues', 'por Emilly Rodrigues'),
    'dispatch_first': ('The', 'Cartas', 'Le', 'Cartas'),
    'dispatch_last': ('Dispatch', 'de bordo', 'courrier', 'de a bordo'),
    'pick_stamp': ('Pick your stamp', 'Escolha seu selo', 'Choisissez votre timbre', 'Elige tu sello'),
    'every': ('Every', 'A cada', 'Tous les', 'Cada'),
    'months': ('months', 'meses', 'mois', 'meses'),
    'contact_destination': ('Destination', 'Destino', 'Destination', 'Destino'),
    'contact_inbox': ('Your inbox', 'Seu e-mail', 'Votre boîte mail', 'Tu correo'),
    'contact_line': ('Let’s talk about space, software and projects that make room for learning.', 'Vamos conversar sobre espaço, software e projetos que abrem espaço para aprender.', 'Parlons d’espace, de logiciel et de projets qui donnent envie d’apprendre.', 'Hablemos de espacio, software y proyectos que invitan a aprender.'),
    'luggage': ('Luggage tag', 'Etiqueta de bagagem', 'Étiquette de bagage', 'Etiqueta de equipaje'),
    'currently': ('Currently', 'Atualmente', 'En ce moment', 'Actualmente'),
    'currently_body': ('Flight software and research', 'Software de voo e pesquisa', 'Logiciel de vol et recherche', 'Software de vuelo e investigación'),
    'looking_for': ('Looking for', 'Próximas conexões', 'Prochains échanges', 'Próximas conexiones'),
    'looking_body': ('Projects in space and education', 'Projetos em espaço e educação', 'Projets dans le spatial et l’éducation', 'Proyectos en espacio y educación'),
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
    projects = [p for p in b['PROJECTS'] if p['kind'] == 'projects']
    featured = next(p for p in projects if p['id'] == 'flight-platform')
    selected = [p for p in projects if p != featured][:3]
    experiences = sorted((p for p in b['PROJECTS'] if p['kind'] == 'experience'),
                         key=lambda p: tuple(int(x) for x in re.findall(r'\d{4}', p['date'])))
    arrow = '<span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-5-5 5 5-5 5"/></svg></span>'
    rocket = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M12 2c3 3 4 7 4 11l-4 3-4-3c0-4 1-8 4-11z" fill="#FBF8F1"/><circle cx="12" cy="9" r="1.5" fill="#1F4A4F"/><path d="m8 13-3 3 3 1m8-4 3 3-3 1" fill="#D9694E"/><path d="m10 18 2 4 2-4" stroke="#B04A32"/></svg>'

    def button(label, target, solid=False, extra=''):
        return f'<a class="btn {"btn-solid" if solid else ""}" href="{E(target, quote=True)}" {extra}>{label}{arrow}</a>'

    def keywords(values):
        return '<div class="keywords">' + ''.join(f'<span>{E(v)}</span>' for v in values) + '</div>'

    def section_heading(title, extra=''):
        return f'<div class="section-heading"><h2>{title}</h2>{extra}</div>'

    def postmark(label, center):
        nonlocal illustration_count
        illustration_count += 1
        path_id = f'postmark-{illustration_count}'
        return f'<svg class="postmark" viewBox="0 0 240 130" aria-hidden="true"><g transform="translate(85 65) rotate(-15)"><defs><path id="{path_id}" d="M-42 0a42 42 0 1 1 84 0a42 42 0 1 1-84 0"/></defs><circle r="54"/><circle r="34"/><text class="postmark-ring"><textPath href="#{path_id}">{E(label)} · </textPath></text><text class="postmark-center" y="6" text-anchor="middle">{E(center)}</text></g><path d="M125 40q15-9 30 0t30 0t30 0M125 53q15-9 30 0t30 0t30 0M125 66q15-9 30 0t30 0t30 0M125 79q15-9 30 0t30 0t30 0"/></svg>'

    def polaroid(photo, cls='', eager=False):
        return f'<figure class="polaroid {cls}">{j["photo_html"](photo, lang, current, eager)}<figcaption>{localized(photo["caption"])}</figcaption></figure>'

    def item_image(p, cls=''):
        drawings = {'cnes': 'experience-clock', 'visiona': 'experience-satellite', 'experience_2': 'experience-satellite'}
        illustration = drawing(drawings[p['id']]) if p['id'] in drawings else art(p['art'])
        return f'<div class="art {cls}" aria-hidden="true">{illustration}</div>'

    design = b['DESIGN']['Design'](b, lang, 'index.html')
    nav_sections = [('experience', t('experience')), ('current-work', t('projects')), ('my-story', design.u('about_nav')), ('journal', jt('home')), ('say-hello', t('contact'))]
    nav = ''.join(f'<a href="#{key}">{label}</a>' for key, label in nav_sections)
    top = f'''<header class="home-header"><div class="airmail-line" aria-hidden="true"></div>
<div class="wrap navigation"><a class="brand" href="{link('index.html')}" aria-label="{design.u('home')}"><span class="brand-icon">{rocket}</span></a><nav id="main-nav" aria-label="{t('menu')}">{nav}</nav>{design.language_selector()}</div></header>'''

    guide_art = ['experience', 'projects', 'about', 'diary', 'contact']
    launch = (b['ROOT'] / 'img/redesign/launch.svg').read_text()
    hero = f'''<section class="hero" aria-labelledby="hero-title"><div class="hero-scrapbook"><figure class="polaroid portrait"><div class="portrait-paper"><img src="{r('img/portrait-lab.jpeg')}" alt="{t('portrait')}" width="1150" height="1280" fetchpriority="high"></div><figcaption>{u('portrait_caption')}</figcaption></figure><aside class="guide"><span class="mono">{u('guide')}</span><nav aria-label="{u('guide')}">{''.join(f'<a href="#{key}">{drawing("guide-" + name)}{label}</a>' for (key, label), name in zip(nav_sections, guide_art))}</nav></aside></div>
<div class="hero-copy"><h1 id="hero-title"><span>Emilly</span> <strong>Rodrigues</strong></h1><p class="hero-description">{t('hero_body')}</p><div class="actions">{button(t('explore'), '#current-work', True)}{button(jt('home'), '#journal')}</div></div>
<div class="hero-launch"><div class="launch-window" aria-hidden="true">{launch}</div><button class="motion-toggle" type="button" data-pause="{u('pause')}" data-play="{u('play')}" aria-pressed="false" hidden>{u('pause')}</button></div></section>'''

    stories = []
    for i, post in enumerate(posts[:2]):
        images = [post['photos'][post['cover'][-1]], post['photos'][post['cover'][0]]]
        stories.append(f'''<article class="story-preview" id="journal-{post['slug']}"><div class="story-preview-copy"><p class="eyebrow">{localized(post['period'])}</p><h3><a href="{link(j['path'](post))}">{localized(post['title'])}</a></h3><p>{localized(post['intro'])}</p><div class="story-preview-actions">{button(jt('read'), link(j['path'](post)), True)}<span class="story-count mono">{i+1:02} / {len(posts):02}</span></div></div><div class="story-photos">{polaroid(images[0], 'photo-main')}{polaroid(images[1], 'photo-small')}</div></article>''')
    diary = f'<section id="journal">{section_heading(jt("home"), button(u("all_stories") + f" · {len(posts)}", link("journal.html")))}{"".join(stories)}</section>'

    cards = ''.join(f'''<a class="project-card" href="{link(b['detail'](p))}" data-featured-project="{p['id']}">{item_image(p)}<p class="eyebrow">{t(p['category'])} · {p['date']}</p><h3>{p['title'][lang]}</h3><p>{p['summary'][lang]}</p>{keywords(p['tech'])}<span class="more">{t('case')}{arrow}</span></a>''' for p in selected)
    current_work = f'''<section id="current-work">{section_heading(t('projects'))}<article class="current-panel"><div class="current-copy"><p class="eyebrow">{u('on_air')}  {featured['date']}</p><h3>{t('current_title')}</h3><p>{featured['summary'][lang]}</p><p class="current-outcome">{featured['outcome'][lang]}</p>{keywords(featured['tech'])}{button(t('case'), link(b['detail'](featured)))}</div>{item_image(featured, 'current-art')}</article><div class="project-grid">{cards}<a class="project-deck" href="{link('projects.html')}"><div class="deck-stack"><span aria-hidden="true"></span><span aria-hidden="true"></span><span>{drawing('deck-satellite')}<strong>+{len(projects)-len(selected)-1}</strong><span class="mono">{t('more_projects')}</span></span></div><span class="more">{t('all_projects')}{arrow}</span></a></div></section>'''

    passes = []
    stops = {'cern': 'CERN · GVA', 'visiona': 'VISIONA · BR', 'cnes': 'CNES · TLS', 'experience_1': 'TIMA · GRENOBLE', 'experience_2': 'ITA · BR', 'experience_3': 'DAFITI · BR'}
    for i, p in reversed(list(enumerate(experiences))):
        successor = experiences[i+1] if i+1 < len(experiences) else None
        departure_year = re.sub(r'(\d{4})–\d{2}(\d{2})', r'\1–\2', E(p['date']))
        # Use the next real experience. The newest pass has no invented future stop.
        destination = f'<div><span class="mono">{u("destination")}</span><strong class="next-destination">{E(stops.get(successor["id"], successor["place"]))}</strong></div>' if successor else ''
        passes.append(f'''<a class="boarding-pass" data-experience-id="{p['id']}" data-experience="{p['category']}" href="{link(b['detail'](p))}">{item_image(p)}<div class="pass-copy"><p class="eyebrow">{E(p['place'])}</p><h3>{p['title'][lang].split(' · ', 1)[-1]}</h3><p>{p['summary'][lang]}</p>{keywords(p['tech'][:3])}</div><div class="pass-stub"><div><span class="mono">{u('departure')}</span><strong>{departure_year}</strong></div>{destination}<span class="more">{u('details')}{arrow}</span></div></a>''')
    categories = list(dict.fromkeys(p['category'] for p in reversed(experiences)))
    filters = ''.join(f'<button type="button" class="chip" data-experience-filter="{key}" aria-pressed="{str(key == "all").lower()}">{t(key)}</button>' for key in ['all', *categories])
    experience = f'<section id="experience">{section_heading(t("experience"))}<div class="experience-filters" role="group" aria-label="{t("filter_label")}" hidden>{filters}</div><div class="boarding-passes">{"".join(passes)}</div><div class="section-end">{button(t("all_experience"), link("experience.html"))}</div></section>'

    about = f'''<section id="my-story" aria-labelledby="about-title"><div class="envelope"><div class="envelope-sheet"><div class="envelope-copy"><p class="eyebrow">Par avion · {t('about')}</p><h2 id="about-title">{u('personal_title')}</h2><p>{u('personal_body')}</p><div class="letter-lines"><p>{u('from')} · Jaru, Rondônia</p><p>{u('to')} · {u('personal_destination')}</p></div>{button(t('more_about'), link('about.html'))}</div><div class="about-aside"><figure class="portrait-stamp"><div class="portrait-stamp-inner"><div class="portrait-paper"><img src="{r('img/portrait-lab.jpeg')}" alt="{t('portrait')}" width="1150" height="1280" loading="lazy"></div></div></figure>{postmark('JARU · RONDÔNIA · BRASIL', 'PAR AVION')}</div></div></div></section>'''

    award_cards = []
    stamp_art = ['rocket', 'satellite', 'star', 'planet']
    for i, (date, name, description, url) in enumerate(d['AWARDS'][:4]):
        related = next((post for post in posts if post.get('related_award') == name), None)
        target = url or (link(j['path'](related)) if related else link('recognition.html'))
        external = 'target="_blank" rel="noopener noreferrer"' if url else ''
        award_cards.append(f'''<a class="award-card" href="{target}" {external}><div class="stamp-holder"><div class="stamp stamp-{i}"><div class="stamp-inner"><span class="stamp-year">{E(date)}</span>{drawing("stamp-" + stamp_art[i])}<span class="stamp-name">{E(name)}</span></div></div>{postmark('EMILLY RODRIGUES', date) if i in (0, 2) else ""}</div><h3>{E(name)}</h3><p>{description[lang]}</p><span class="more">{t('source')}{arrow}</span></a>''')
    awards = f'<section id="recognition">{section_heading(t("recognition"), button(u("all_awards"), link("recognition.html")))}<div class="award-grid">{"".join(award_cards)}</div></section>'

    media_body = runpy.run_path(str(b['ROOT'] / 'scripts/media_redesign.py'))['render'](b['ROOT'], lang, r, drawing, arrow)
    media = f'<section id="media">{section_heading(u("media"))}{media_body}</section>'

    topics = ''.join(f'<label class="topic"><input type="checkbox" name="topic" value="{key}" checked><span>{u(key)}</span></label>' for key in ['diary_topic', 'project_topic', 'media_topic'])
    frequencies = ''.join(f'<label class="frequency-stamp"><input type="radio" name="frequency" value="{n}" aria-label="{u(key)}" {"checked" if n == 3 else ""}><span class="frequency-paper"><span class="frequency-inner"><span>{u("every")}</span><strong>{n}</strong><span>{u("months")}</span></span></span><svg class="frequency-mark" viewBox="0 0 120 70" aria-hidden="true"><circle cx="38" cy="35" r="26"/><path d="m27 35 7 7 15-17M63 23q12-7 24 0t24 0M63 33q12-7 24 0t24 0M63 43q12-7 24 0t24 0"/></svg></label>' for n, key in [(3, 'three'), (6, 'six')])
    # Deliberately not a submitting form. Existing FormSubmit is contact-only.
    newsletter = f'''<section id="newsletter">{section_heading(u('newsletter'))}<div class="dispatch-card"><div class="dispatch-art"><div class="postcard-art" aria-hidden="true">{drawing('postcard')}</div><div class="dispatch-title"><span class="mono">Par avion</span><span class="dispatch-kicker">{u('dispatch_first')}</span><strong>{u('dispatch_last')}</strong><span class="dispatch-by">{u('letter_by')}</span></div></div><div class="dispatch-letter"><p class="letter-salutation">{u('dear_reader')}</p><p>{u('letter_body')}</p><fieldset><legend>{u('topics')}</legend><div class="topics">{topics}</div></fieldset><p class="letter-signature">Emilly</p></div><div class="dispatch-address"><fieldset><legend>{u('pick_stamp')}</legend><div class="frequencies">{frequencies}</div></fieldset><label class="dispatch-to" for="newsletter-email"><span class="mono">{u('to')}</span><input id="newsletter-email" type="email" placeholder="{'email@exemplo.com' if lang == 'pt' else 'your@email.com'}" disabled aria-describedby="newsletter-status"></label><div class="dispatch-from"><span class="mono">{u('from')}</span><span>Emilly Rodrigues</span></div><button type="button" class="btn btn-solid" disabled aria-describedby="newsletter-status">{u('subscribe')}{arrow}</button><p id="newsletter-status">{u('unavailable')}</p></div></div></section>'''

    contact = f'''<section id="say-hello" class="contact-section"><div><h2><span>{u('contact_destination')}</span><strong>{u('contact_inbox')}</strong></h2><p>{u('contact_line')}</p><div class="actions">{button(t('send'), 'mailto:' + d['EMAIL'], True)}<a class="btn btn-plain" href="{d['LINKEDIN']}" target="_blank" rel="noopener noreferrer">LinkedIn</a><a class="btn btn-plain" href="{d['GITHUB']}" target="_blank" rel="noopener noreferrer">GitHub</a><a class="btn btn-plain" href="{r('CV_Emilly.pdf')}" download>CV · PDF</a></div></div><div class="tag-holder"><svg class="tag-string" viewBox="0 0 160 80" aria-hidden="true"><path d="M4 70C40 10 90 80 150 44" fill="none" stroke="#B04A32" stroke-width="2"/></svg><div class="luggage-tag"><span class="tag-hole" aria-hidden="true"></span><div class="tag-heading">{u('luggage')}</div><dl><div><dt>{u('currently')}</dt><dd>{u('currently_body')}</dd></div><div><dt>{u('looking_for')}</dt><dd>{u('looking_body')}</dd></div></dl></div></div></section>'''

    footer = f'<footer class="wrap footer"><span>© 2026 Emilly Rodrigues · {t("footer_note")}</span><a href="#top">{t("top")}{arrow}</a></footer>'
    return top + '<main id="main" class="wrap home-content">' + hero + experience + current_work + about + awards + media + diary + newsletter + contact + '</main>' + footer
