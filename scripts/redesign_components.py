"""Shared, production components ported from the five design prototypes."""
import html
import re

E = html.escape
ARROW = '<span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-5-5 5 5-5 5"/></svg></span>'
BACK_ARROW = '<span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5m5-5-5 5 5 5"/></svg></span>'
STAR = '<span class="spark" aria-hidden="true"><svg viewBox="0 0 40 40"><path d="M20 0C21 14 26 19 40 20C26 21 21 26 20 40C19 26 14 21 0 20C14 19 19 14 20 0Z" fill="currentColor"/></svg></span>'
LABELS = {
 'departure': ('Departure','Partida','Départ','Salida'),
 'next': ('Next destination','Próximo destino','Prochaine destination','Próximo destino'),
 'pass': ('Boarding pass','Cartão de embarque','Carte d’embarquement','Tarjeta de embarque'),
 'passenger': ('Passenger','Passageira','Passagère','Pasajera'),
 'base': ('Base','Base','Base','Base'),
 'period': ('Period','Período','Période','Período'),
 'route': ('Flight path','Trajetória','Itinéraire','Trayectoria'),
 'route_projects': ('Every project, in order','Cada projeto, em ordem','Chaque projet, dans l’ordre','Cada proyecto, en orden'),
 'route_experience': ('Every boarding pass so far','Cada experiência até aqui','Toutes les expériences jusqu’ici','Cada experiencia hasta aquí'),
 'route_stories': ('Every story, in order','Cada história, em ordem','Chaque récit, dans l’ordre','Cada historia, en orden'),
 'preview': ('Pick a stop to preview it','Escolha uma parada para conhecer','Choisissez une étape à découvrir','Elige una parada para conocerla'),
 'here': ('You are here','Você está aqui','Vous êtes ici','Estás aquí'),
 'open': ('Open','Abrir','Ouvrir','Abrir'),
 'story': ('Story','História','Récit','Historia'),
 'learned': ('What I learned','O que aprendi','Ce que j’ai appris','Lo que aprendí'),
 'home': ('Back home','Voltar ao início','Retour à l’accueil','Volver al inicio'),
 'logbook': ('Mission logbook','Diário de missões','Carnet de missions','Bitácora de misiones'),
 'about_nav': ('About','Sobre','À propos','Sobre mí'),
 'home_nav': ('Home','Início','Accueil','Inicio'),
 'portfolio': ('Portfolio','Portfólio','Portfolio','Portafolio'),
 'all_projects_prefix': ('All','Todos os','Tous les','Todos los'),
 'all_experience_prefix': ('All','Todas as','Toutes les','Todas las'),
 'experiences': ('Experience','Experiências','Expériences','Experiencias'),
 'continue': ('Keep exploring','Continue explorando','Continuez à explorer','Sigue explorando'),
 'hover_preview': ('Hover or focus to preview','Passe o mouse ou use o teclado','Survolez ou utilisez le clavier','Pasa el cursor o usa el teclado'),
 'previous_experience': ('Previous experience','Experiência anterior','Expérience précédente','Experiencia anterior'),
 'next_experience': ('Next experience','Próxima experiência','Expérience suivante','Experiencia siguiente'),
 'older': ('Earlier entries','Itens anteriores','Éléments précédents','Elementos anteriores'),
 'newer': ('Later entries','Próximos itens','Éléments suivants','Elementos siguientes'),
 'footer_line': ('Engineering, projects and stories along the way.','Engenharia, projetos e histórias pelo caminho.','Ingénierie, projets et récits au fil du chemin.','Ingeniería, proyectos e historias por el camino.'),
 'elsewhere': ('Find me elsewhere','Vamos nos conectar','Retrouvez-moi aussi','Conectemos'),
 'search_experience': ('Search experiences or technologies','Buscar experiências ou tecnologias','Rechercher expériences ou technologies','Buscar experiencias o tecnologías'),
 'experience_results': ('experiences found','experiências encontradas','expériences trouvées','experiencias encontradas'),
 'no_experience': ('No matching experience. Try another term.','Nenhuma experiência encontrada. Tente outro termo.','Aucune expérience trouvée. Essayez un autre terme.','No se encontró ninguna experiencia. Prueba otro término.'),
}


def chronological(items):
    return sorted(items, key=lambda p: tuple(map(int, re.findall(r'\d{4}', p['date']))))


class Design:
    def __init__(self, b, lang, path):
        self.b, self.lang, self.path = b, lang, path
        self.current = b['loc'](path, lang)
        self.count = 0

    def t(self, key): return self.b['txt'](key, self.lang)
    def u(self, key): return LABELS[key][('en','pt','fr','es').index(self.lang)]
    def local(self, value): return E(self.b['J']['text'](value, self.lang))
    def r(self, target): return self.b['relative'](self.current, target)
    def link(self, target): return self.b['href'](self.current, target, self.lang)

    def drawing(self, name):
        self.count += 1
        svg = (self.b['ROOT'] / f'img/redesign/{name}.svg').read_text()
        for identifier in re.findall(r'\bid="([^"]+)"', svg):
            unique = f'design-{self.count}-{identifier}'
            svg = svg.replace(f'id="{identifier}"', f'id="{unique}"').replace(f'url(#{identifier})', f'url(#{unique})').replace(f'href="#{identifier}"', f'href="#{unique}"')
        opening = re.match(r'<svg\b[^>]*>', svg).group()
        clean = re.sub(r'\s(?:style|class|aria-hidden)="[^"]*"','',opening)
        return clean.replace('<svg ', '<svg class="illustration" aria-hidden="true" ',1) + svg[len(opening):]

    def art(self, name, hero=False, item_id=None):
        if item_id == 'damas-espaciais':
            return f'<svg class="illustration damas-illustration" aria-hidden="true" viewBox="0 0 400 260"><rect width="400" height="260" fill="#E6DDEA"/><g transform="translate(78 8) rotate(-8 120 120)"><rect x="-8" y="-8" width="256" height="256" rx="12" fill="#1E3A3D"/><image href="{self.r("img/damas-espaciais/board.jpg")}" width="240" height="240"/><image href="{self.r("img/damas-espaciais/blue.png")}" x="30" y="0" width="30" height="30"/><image href="{self.r("img/damas-espaciais/blue.png")}" x="90" y="60" width="30" height="30"/><image href="{self.r("img/damas-espaciais/pink.png")}" x="150" y="180" width="30" height="30"/><image href="{self.r("img/damas-espaciais/pink-king.png")}" x="60" y="150" width="30" height="30"/><circle cx="135" cy="105" r="6" fill="#F1E2B2"/></g></svg>'
        if name == 'platform' and item_id != 'flight-platform':
            return self.b['art'](name)
        if hero and name == 'satellite': return self.drawing('project-pass')
        if hero and name == 'detector': return self.drawing('experience-pass')
        choices={'platform':'flight-console','satellite':'project-satellite','chip':'project-chip','outreach':'project-outreach','rover':'project-rover','aircraft':'project-aircraft','code':'project-code','detector':'experience-detector'}
        return self.drawing(choices[name]) if name in choices else self.b['art'](name)

    def button(self, label, url, solid=False, attrs='', back=False):
        return f'<a class="btn {"btn-solid" if solid else ""} {"btn-back" if back else ""}" href="{E(url,quote=True)}" {attrs}>{BACK_ARROW if back else ""}{label}{"" if back else ARROW}</a>'

    def keywords(self, values):
        return '<div class="keywords tags">' + ''.join(f'<span>{E(v)}</span>' for v in values) + '</div>'

    def language_selector(self):
        locales = [('en','English'),('pt','Português'),('fr','Français'),('es','Español')]
        links = ''.join(f'<a href="{self.r(self.b["loc"](self.path,code))}" lang="{code}" hreflang="{code}" aria-label="{label}" {"aria-current=\"page\"" if code == self.lang else ""}>{code.upper()}</a>' for code,label in locales)
        return f'<nav class="languages" aria-label="{self.t("language")}">{links}</nav>'

    def header(self, active):
        current = 'diary' if active == 'stories' or self.path.startswith('journal/') else active
        sections = [('home','index.html#top'),('experience','experience.html'),('projects','projects.html'),('about','about.html'),('recognition','recognition.html'),('diary','journal.html'),('contact','contact.html')]
        labels = {'home': self.u('home_nav'), 'about': self.u('about_nav'), 'diary': self.t('home')}
        nav=''.join(f'<a href="{self.link(path)}" {"aria-current=\"page\"" if key == current else ""}>{labels[key] if key in labels else self.t(key)}</a>' for key,path in sections)
        return f'<header class="home-header"><div class="airmail-line" aria-hidden="true"></div><div class="wrap navigation"><a class="brand" href="{self.link("index.html#top")}"><span class="brand-icon">{self.drawing("guide-projects")}</span><span>Emilly Rodrigues<small>{self.u("portfolio")}</small></span></a><nav id="main-nav" aria-label="{self.t("menu")}">{nav}</nav>{self.language_selector()}</div></header>'

    def footer(self):
        links = ''.join(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{name}<span aria-hidden="true">↗</span></a>' for name,url in [('GitHub',self.b['D']['GITHUB']),('LinkedIn',self.b['D']['LINKEDIN'])])
        return f'<footer class="wrap footer portfolio-footer"><div class="footer-person"><a href="{self.link("index.html#top")}">Emilly Rodrigues</a><p>{self.u("footer_line")}</p><small>© 2026 · {self.u("portfolio")}</small></div><div class="footer-connect"><p>{self.u("elsewhere")}</p><nav aria-label="{self.t("contact")}">{links}<a href="mailto:{self.b["EMAIL"]}">{self.t("contact")}<span aria-hidden="true">↗</span></a></nav><a class="footer-email" href="mailto:{self.b["EMAIL"]}">{self.b["EMAIL"]}</a></div></footer>'

    def boarding(self, p, compact=False):
        peers=chronological([q for q in self.b['PROJECTS'] if q['kind']==p['kind']])
        i=peers.index(p)
        successor=peers[i+1] if i+1<len(peers) else None
        year=re.search(r'\d{4}',p['date']).group()
        destination=f'<div><span class="mono">{self.u("next")}</span><a class="next-destination" href="{self.link(self.b["detail"](successor))}">{E(successor["title"][self.lang])}</a></div>' if successor else ''
        meta=f'<dl class="boarding-meta"><div><dt>{self.u("passenger")}</dt><dd>Emilly Rodrigues</dd></div><div><dt>{self.u("base")}</dt><dd>{E(p["place"])}</dd></div><div><dt>{self.u("period")}</dt><dd>{E(p["date"])}</dd></div></dl>'
        return f'<header class="case-boarding {"experience-boarding" if p["kind"]=="experience" else "project-boarding"}" data-case-id="{p["id"]}"><div class="boarding-art" aria-hidden="true">{self.art(p["art"],True,p["id"])}<span class="mono">{self.u("pass")}</span></div><div class="boarding-copy"><p class="eyebrow">{self.t(p["category"])} · {E(p["date"])}</p><h1>{p["title"][self.lang]}</h1><p class="boarding-summary">{p["summary"][self.lang]}</p>{self.keywords(p["tech"])}{meta}</div><div class="boarding-stub"><div><span class="mono">{self.u("departure")}</span><strong>{year}</strong></div>{destination}<span class="barcode" aria-hidden="true"></span></div></header>'

    def flight_path(self, items, current_id, kind):
        """Bounded title rail with native links and previews on hover or focus."""
        stops, panels = [], []
        for i, item in enumerate(items):
            here = item['id'] == current_id
            panel = 'flight-preview-' + item['id']
            current = 'aria-current="page"' if here else ''
            stops.append(f'<a class="flight-stop story-stop" data-flight-stop data-preview="{panel}" data-date="{E(item["date"])}" href="{E(item["url"],quote=True)}" {current}><span class="mono">{E(item["date"])}</span><strong>{E(item["title"])}</strong></a>')
            action = f'<span class="flight-here">{self.u("here")}</span>' if here else f'<a class="explorer-open" href="{E(item["url"],quote=True)}">{self.u("open")}{ARROW}</a>'
            hidden = '' if here else 'hidden'
            panels.append(f'<article class="flight-preview story-explorer-preview" id="{panel}" {hidden}><div class="explorer-photo explorer-art" aria-hidden="true">{item["art"]}</div><div class="explorer-copy"><p class="eyebrow">{E(item["meta"])}</p><h3>{E(item["title"])}</h3><p>{E(item["summary"])}</p>{action}</div></article>')
        all_label = self.t('all_projects' if kind == 'projects' else 'all_experience')
        return f'<section class="flight-path story-explorer case-explorer flight-{kind}" aria-labelledby="flight-title"><div class="explorer-heading"><div><p class="eyebrow">{self.t(kind)}</p><h2 id="flight-title">{self.u("continue")}</h2></div>{self.button(all_label+f" · {len(items)}",self.link(kind+".html"))}</div><div class="explorer-layout"><div class="explorer-stops"><p class="mono explorer-hint">{self.u("hover_preview")}</p><nav class="flight-map" aria-label="{self.u("route")}">{"".join(stops)}</nav><div class="explorer-controls" hidden><button type="button" data-story-prev aria-label="{self.u("older")}">↑</button><button type="button" data-story-next aria-label="{self.u("newer")}">↓</button></div></div><div class="flight-previews">{"".join(panels)}</div></div></section>'
