"""The prototype's media objects, filled with supplied links and verified titles."""
import html
import json

E = html.escape
UI = {
    'watch': ('Watch', 'Assistir', 'Regarder', 'Ver'),
    'cover': ('Cover', 'Capa', 'Couverture', 'Portada'),
    'read': ('Read the article', 'Ler a matéria', 'Lire l’article', 'Leer el artículo'),
    'previous': ('Previous', 'Anterior', 'Précédent', 'Anterior'),
    'next': ('Next', 'Próximo', 'Suivant', 'Siguiente'),
    'social': ('Posts', 'Publicações', 'Publications', 'Publicaciones'),
}


def render(root, lang, relative, drawing, arrow):
    u = lambda key: UI[key][('en', 'pt', 'fr', 'es').index(lang)]
    data = json.loads((root / 'content/media.json').read_text())
    external = 'target="_blank" rel="noopener noreferrer"'

    def controls():
        return f'<div class="media-controls" hidden><button type="button" data-carousel-prev aria-label="{u("previous")}">{arrow}</button><span class="mono" data-carousel-count aria-live="polite"></span><button type="button" data-carousel-next aria-label="{u("next")}">{arrow}</button></div>'

    cover = data['cover']
    magazine = f'<a class="media-magazine" href="{cover["url"]}" {external}><img src="{relative(cover["file"])}" alt="{E(cover["outlet"] + ' · ' + cover["title"], quote=True)}" width="730" height="964" loading="lazy"><span class="eyebrow">{u("cover")} · Exame</span><span class="more">{u("read")}{arrow}</span></a>'
    tapes = []
    for item in data['videos']:
        tapes.append(f'<a class="media-tape" data-carousel-item href="{E(item["url"], quote=True)}" {external}><span class="eyebrow"><i class="live-dot" aria-hidden="true"></i>{"Podcast" if item["kind"] == "podcast" else "Video"} · {E(item["outlet"])}</span><div class="cassette-art">{drawing("media-cassette")}<span class="cassette-label">{E(item["outlet"])}</span></div><h3 lang="pt">{E(item["title"])}</h3><span class="more">{u("watch")}{arrow}</span></a>')
    papers = []
    for start in range(0, len(data['press']), 2):
        clips = []
        for i, item in enumerate(data['press'][start:start+2]):
            lines = '<div class="newspaper-lines" aria-hidden="true">' + '<div><i></i><i></i><i></i></div>' * 2 + '</div>'
            clips.append(f'<a class="newspaper-clip {"clip-small" if i else ""}" href="{item["url"]}" {external}><div class="torn-paper"><div class="newspaper-meta"><span>{E(item["outlet"])}</span><time datetime="{item["date"]}">{item["date"]}</time></div><h3 lang="pt">{E(item["title"])}</h3>{lines if not i else ""}<span class="more">{u("read")}{arrow}</span></div></a>')
        papers.append(f'<div class="clipping-pair" data-carousel-item>{"".join(clips)}</div>')
    phones = []
    for i, item in enumerate(data['social'], 1):
        phones.append(f'<a class="media-phone" href="{item["url"]}" {external} aria-label="{u("social")} · {item["platform"]} · {i}"><span class="phone-screen"><span class="phone-platform">{item["platform"]}</span><span class="phone-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m7 4 13 8-13 8z" fill="currentColor"/></svg></span></span></a>')
    return f'<div class="media-shelf">{magazine}<div class="tape-player" data-carousel>{"".join(tapes)}{controls()}</div><div class="press-clippings" data-carousel>{"".join(papers)}{controls()}</div></div><div class="media-social"><p class="eyebrow">{u("social")} · Instagram · LinkedIn</p><div class="phone-row">{"".join(phones)}</div></div>'
