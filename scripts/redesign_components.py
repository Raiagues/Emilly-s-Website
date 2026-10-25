"""Shared, production components ported from the five design prototypes."""
import html
import re

E = html.escape
ARROW = '<span class="arr" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14m-5-5 5 5-5 5"/></svg></span>'
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
        if name == 'platform' and item_id != 'flight-platform':
            return self.b['art'](name)
        if hero and name == 'satellite': return self.drawing('project-pass')
        if hero and name == 'detector': return self.drawing('experience-pass')
        choices={'platform':'flight-console','satellite':'project-satellite','chip':'project-chip','outreach':'project-outreach','rover':'project-rover','aircraft':'project-aircraft','code':'project-code','detector':'experience-detector'}
        return self.drawing(choices[name]) if name in choices else self.b['art'](name)

    def button(self, label, url, solid=False, attrs=''):
        return f'<a class="btn {"btn-solid" if solid else ""}" href="{E(url,quote=True)}" {attrs}>{label}{ARROW}</a>'

    def keywords(self, values):
        return '<div class="keywords">' + STAR.join(f'<span>{E(v)}</span>' for v in values) + '</div>'

    def header(self, active):
        sections=self.b['SECTIONS']
        nav=''.join(f'<a href="{self.link(path)}" {"aria-current=\"page\"" if key == active or (active == "stories" and key == "home") else ""}>{self.t(key)}</a>' for key,path in sections)
        languages=''.join(f'<a href="{self.r(self.b["loc"](self.path,code))}" lang="{code}" hreflang="{code}" aria-label="{name}" {"aria-current=\"page\"" if code == self.lang else ""}>{code.upper()}</a>' for code,name in [('en','English'),('pt','Português'),('fr','Français'),('es','Español')])
        return f'<header class="home-header"><div class="airmail-line" aria-hidden="true"></div><div class="wrap navigation"><a class="brand" href="{self.link("index.html")}"><span class="brand-icon">{self.drawing("guide-projects")}</span><span>Emilly Rodrigues</span></a><nav id="main-nav" aria-label="{self.t("menu")}">{nav}</nav><div class="languages" role="group" aria-label="{self.t("language")}">{languages}</div></div></header>'

    def footer(self):
        return f'<footer class="wrap footer"><span>© 2026 Emilly Rodrigues · {self.t("footer_note")}</span><a href="#top">{self.t("top")}{ARROW}</a></footer>'

    def boarding(self, p, compact=False):
        peers=chronological([q for q in self.b['PROJECTS'] if q['kind']==p['kind']])
        i=peers.index(p)
        successor=peers[i+1] if i+1<len(peers) else None
        year=re.search(r'\d{4}',p['date']).group()
        destination=f'<div><span class="mono">{self.u("next")}</span><a class="next-destination" href="{self.link(self.b["detail"](successor))}">{E(successor["title"][self.lang])}</a></div>' if successor else ''
        meta=f'<dl class="boarding-meta"><div><dt>{self.u("passenger")}</dt><dd>Emilly Rodrigues</dd></div><div><dt>{self.u("base")}</dt><dd>{E(p["place"])}</dd></div><div><dt>{self.u("period")}</dt><dd>{E(p["date"])}</dd></div></dl>'
        return f'<header class="case-boarding {"experience-boarding" if p["kind"]=="experience" else "project-boarding"}" data-case-id="{p["id"]}"><div class="boarding-art" aria-hidden="true">{self.art(p["art"],True,p["id"])}<span class="mono">{self.u("pass")}</span></div><div class="boarding-copy"><p class="eyebrow">{self.t(p["category"])} · {E(p["date"])}</p><h1>{p["title"][self.lang]}</h1><p class="boarding-summary">{p["summary"][self.lang]}</p>{self.keywords(p["tech"])}{meta}</div><div class="boarding-stub"><div><span class="mono">{self.u("departure")}</span><strong>{year}</strong></div>{destination}<span class="barcode" aria-hidden="true"></span></div></header>'

    def flight_path(self, items, current_id, kind):
        """All real stops, ordered by event date; native links work without JS."""
        columns=min(7,len(items))
        rows=(len(items)+columns-1)//columns
        stops=[]; panels=[]; curves=[]
        for row in range(rows):
            curves.append(f'<path d="M4 {row*135+83} Q{100/columns/2} {row*135+15} {100/columns+4} {row*135+83} T{100/columns*2+4} {row*135+83} T{100/columns*3+4} {row*135+83} T{100/columns*4+4} {row*135+83} T{100/columns*5+4} {row*135+83} T{100/columns*6+4} {row*135+83}"/>')
        for i,item in enumerate(items):
            here=item['id']==current_id
            row,col=divmod(i,columns)
            x=(col+.5)*100/columns
            y=row*135+(46 if col%2 else 88)
            panel=f'flight-preview-{i}'
            stops.append(f'<a class="flight-stop" data-flight-stop data-preview="{panel}" data-date="{E(item["date"])}" href="{E(item["url"],quote=True)}" aria-label="{E(item["title"],quote=True)}" {"aria-current=\"page\"" if here else ""} style="--stop-x:{x:.3f}%;--stop-y:{y}px"><span class="flight-dot" aria-hidden="true">{STAR if here else ""}</span><span class="flight-code">{i+1:02} · {E(item["year"])}</span></a>')
            state=f'<span class="flight-here">{STAR}{self.u("here")}</span>' if here else self.button(self.u('open'),item['url'],True)
            panels.append(f'<article class="flight-preview" id="{panel}" {"" if here else "hidden"}><div><p class="eyebrow">{E(item["meta"])}</p><h3>{E(item["title"])}</h3><p>{E(item["summary"])}</p>{state}</div><div class="flight-preview-stub"><span class="mono">{self.u("period")}</span><strong>{E(item["year"])}</strong><span class="barcode" aria-hidden="true"></span></div></article>')
        return f'<section class="flight-path flight-{kind}" aria-labelledby="flight-title"><div class="flight-heading"><div><p class="eyebrow">{self.u("route")}</p><h2 id="flight-title">{self.u("route_"+kind)}</h2></div><p class="mono">{self.u("preview")}</p></div><nav class="flight-map" aria-label="{self.u("route")}" style="--route-height:{rows*135}px"><svg viewBox="0 0 100 {rows*135}" preserveAspectRatio="none" aria-hidden="true">{"".join(curves)}</svg>{"".join(stops)}</nav><div class="flight-previews" aria-live="polite">{"".join(panels)}</div></section>'
