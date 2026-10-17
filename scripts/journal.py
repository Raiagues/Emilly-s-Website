"""Small, data-driven journal renderer. Posts are plain JSON, never executable HTML."""
import html
import json
import os
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

E = html.escape
LANGS = ('en', 'pt', 'fr', 'es')


def text(value, lang):
    return (value.get(lang) or value['en']) if isinstance(value, dict) else value


def load_posts(root):
    posts = []
    for file in sorted((root / 'content/journal').glob('*.json')):
        if file.name in ('ui.json', 'entities.json'):
            continue
        post = json.loads(file.read_text())
        if not post.get('published', False):
            continue
        assert post['slug'] != 'connections' and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', post['slug']), file
        date.fromisoformat(post['date'])
        for event in post.get('timeline', []):
            value = event['date']
            assert re.fullmatch(r'\d{4}-\d{2}(?:-\d{2})?', value), (file, value)
            date.fromisoformat(value + '-01' if len(value) == 7 else value)
            assert event['title'].get('en') and event['label'].get('en')
        ids = [s['id'] for s in post['sections']]
        assert len(ids) == len(set(ids)) and all(re.fullmatch(r'[a-z][a-z0-9-]*', i) for i in ids)
        for key in ('title', 'subtitle', 'intro', 'period', 'closing'):
            assert post[key].get('en'), (file, key)
        for photo in post['photos'].values():
            asset = (root / photo['file']).resolve()
            assert asset.is_relative_to((root / 'portifolio').resolve()) and asset.is_file(), asset
            assert photo['caption'].get('en') and photo['width'] > 0 and photo['height'] > 0
        for event in post.get('timeline', []):
            assert not event.get('section') or event['section'] in ids, (file, event)
        for key in post['cover'] + [key for section in post['sections'] for key in section.get('photos', []) + section.get('documents', [])]:
            assert key in post['photos'], key
        for section in post['sections']:
            assert section['title'].get('en') and all(p.get('en') for p in section['paragraphs'])
            for source in section.get('links', []):
                url = urlsplit(source['url'])
                assert url.scheme in ('https', 'http') and url.netloc and source['label'].get('en'), (file, source)
        if post.get('resource'):
            asset = (root / post['resource']['file']).resolve()
            assert asset.is_relative_to((root / 'portifolio').resolve()) and asset.is_file(), asset
        posts.append(post)
    assert len({p['slug'] for p in posts}) == len(posts), 'Duplicate journal slug'
    return sorted(posts, key=lambda p: min((e['date'] for e in p.get('timeline', [])), default=p['date']))


def load_entities(root, posts):
    entities = json.loads((root / 'content/journal/entities.json').read_text())
    for key, entity in entities.items():
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key)
        assert entity['name'].get('en') and entity['kind'] in ('person', 'institution')
    for post in posts:
        assert all(key in entities for key in post.get('entities', [])), post['slug']
    return {key: entity for key, entity in entities.items() if any(key in p.get('entities', []) for p in posts)}


def relative(current, target):
    return os.path.relpath(target, Path(current).parent).replace(os.sep, '/')


def path(post):
    return f'journal/{post["slug"]}.html'


def photo_html(photo, lang, current, eager=False):
    caption = E(text(photo['caption'], lang), quote=True)
    return f'<img src="{relative(current, photo["file"])}" alt="{caption}" width="{photo["width"]}" height="{photo["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async">'


def cover(post, lang, current):
    return '<div class="journal-mosaic" aria-hidden="true">' + ''.join(photo_html(post['photos'][key], lang, current, True).replace('alt="'+E(text(post['photos'][key]['caption'], lang), quote=True)+'"', 'alt=""') for key in post['cover']) + '</div>'


def feed(posts, lang, current, link, ui):
    t = lambda key: E(text(ui[key], lang))
    cards = []
    for post in posts:
        cards.append(f'''<article class="journal-entry"><a href="{link(path(post))}" class="journal-entry-link">
{cover(post, lang, current)}<div class="journal-entry-copy"><p class="journal-meta">{E(text(post.get('series', ''), lang))} · {E(text(post['period'], lang))}</p><h3>{E(text(post['title'], lang))}</h3><p>{E(text(post['subtitle'], lang))}</p><span class="text-link">{t('read')} <span aria-hidden="true">↗</span></span></div></a></article>''')
    events = sorted(((event, post) for post in posts for event in post.get('timeline', [])), key=lambda item: item[0]['date'])
    timeline = ''.join(f'<li><time datetime="{event["date"]}">{E(text(event["label"], lang))}</time><a href="{link(path(post))}{"#" + event["section"] if event.get("section") else ""}">{E(text(event["title"], lang))} <span aria-hidden="true">↗</span></a></li>' for event, post in events)
    return f'<section class="journal-feed" id="journal"><div class="section-title"><h2>{t("latest")}</h2></div><nav class="journal-timeline" aria-label="{t("timeline")}"><h3>{t("timeline")}</h3><ol>{timeline}</ol></nav><p class="journal-browse"><a class="text-link" href="{link("journal/connections.html")}">{t("all_connections")} →</a></p><div class="journal-cards">{"".join(cards)}</div></section>'


def connections(posts, entities, lang, link, ui):
    t = lambda key: E(text(ui[key], lang))
    index = ''.join(f'<a class="button button-soft" href="#{key}">{E(text(entity["name"], lang))}</a>' for key, entity in entities.items())
    groups = []
    for key, entity in entities.items():
        entries = ''.join(f'<li><span>{E(text(post["period"], lang))}</span><a href="{link(path(post))}">{E(text(post["title"], lang))} →</a></li>' for post in posts if key in post.get('entities', []))
        groups.append(f'<section class="connection-group" id="{key}"><h2>{E(text(entity["name"], lang))}</h2><ul>{entries}</ul></section>')
    return f'<main id="main" class="container content-page connections-page"><a class="text-link" href="{link("index.html")}#journal">← {t("back")}</a><h1>{t("connections")}</h1><p>{t("connections_intro")}</p><nav class="connection-tags" aria-label="{t("connections")}">{index}</nav>{"".join(groups)}</main>'


def related_stories(post, posts, entities, lang, link, ui):
    keys = post.get('entities', [])
    if not keys:
        return ''
    t = lambda key: E(text(ui[key], lang))
    tags = ''.join(f'<a class="button button-soft" href="{link("journal/connections.html")}#{key}">{E(text(entities[key]["name"], lang))}</a>' for key in keys)
    related = [p for p in posts if p['slug'] != post['slug'] and set(keys).intersection(p.get('entities', []))]
    links = ''.join(f'<li><a class="text-link" href="{link(path(p))}">{E(text(p["title"], lang))} →</a></li>' for p in related)
    more = f'<h3>{t("related")}</h3><ul>{links}</ul>' if related else ''
    return f'<section class="journal-connections"><h2>{t("connections_in_story")}</h2><div class="connection-tags">{tags}</div>{more}</section>'


def story(post, lang, current, link, ui, posts, entities):
    t = lambda key: E(text(ui[key], lang))
    paragraphs = lambda items: ''.join(f'<p>{E(text(p, lang))}</p>' for p in items)
    contents = ''.join(f'<a href="#{s["id"]}">{E(text(s["title"], lang))}</a>' for s in post['sections'])
    technical = ''
    if post.get('technical_path') and not post.get('resource'):
        technical = f'<p><a class="text-link" href="{link(post["technical_path"])}">{E(text(post.get("technical_label", ui["technical"]), lang))} →</a></p>'
    sections = []
    for number, section in enumerate(post['sections'], 1):
        photos = []
        for key in section.get('photos', []):
            photo = post['photos'][key]
            photos.append(f'''<figure class="journal-photo {'landscape' if photo['width'] > photo['height'] else ''}"><a href="{relative(current, photo['file'])}" data-gallery data-caption="{E(text(photo['caption'], lang), quote=True)}">{photo_html(photo, lang, current)}<span class="photo-expand" aria-hidden="true">↗</span></a><figcaption>{E(text(photo['caption'], lang))}</figcaption></figure>''')
        resource = ''
        if section.get('resource') and post.get('resource'):
            resource = f'<div class="journal-resource"><a class="button button-primary" href="{relative(current, post["resource"]["file"])}" target="_blank" rel="noopener noreferrer">{E(text(post["resource"]["label"], lang))} ↗</a><a class="text-link" href="{link(post.get("technical_path", "projects.html"))}">{t("technical")} →</a></div>'
        letter = ''
        if section.get('letter'):
            item = section['letter']
            letter = f'<aside class="journal-letter"><p class="journal-meta">{E(text(item["label"], lang))}</p><p class="letter-subject" lang="en">{E(item["subject"])}</p><blockquote lang="en">{E(item["excerpt"])}</blockquote></aside>'
            if section.get('documents'):
                letter = f'<details class="journal-transcript"><summary>{t("transcript")}</summary>{letter}</details>'
        documents = ''
        for key in section.get('documents', []):
            document = post['photos'][key]
            documents += f'<figure class="journal-document"><a href="{relative(current, document["file"])}" target="_blank" rel="noopener noreferrer">{photo_html(document, lang, current)}</a><figcaption>{E(text(document["caption"], lang))}</figcaption></figure>'
        sources = ''.join(f'<p><a class="text-link" href="{E(source["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{E(text(source["label"], lang))} ↗</a></p>' for source in section.get('links', []))
        paired = bool(photos) and not documents
        lead = photos[0] if paired else ''
        remaining = photos[1:] if paired else photos
        gallery = f'<div class="journal-gallery">{"".join(remaining)}</div>' if remaining else ''
        sections.append(f'''<section id="{section['id']}" class="journal-chapter {'chapter-paired' if paired else 'chapter-text'}"><div class="chapter-layout"><div class="journal-prose"><span class="chapter-number" aria-hidden="true">{number:02d}</span><h2>{E(text(section['title'], lang))}</h2>{paragraphs(section['paragraphs'])}{sources}{resource}{documents}{letter}</div>{f'<div class="chapter-image">{lead}</div>' if lead else ''}</div>{gallery}</section>''')
    return f'''<main id="main" class="container journal-page"><a class="text-link journal-back" href="{link('index.html')}#journal">← {t('back')}</a>
<article><div class="journal-opening"><header class="journal-heading"><p class="journal-meta">{E(text(post.get('series', ''), lang))} · {E(text(post['period'], lang))}</p><h1>{E(text(post['title'], lang))}</h1><p class="journal-deck">{E(text(post['subtitle'], lang))}</p><p class="journal-byline">Emilly Rodrigues <span aria-hidden="true">/</span> {t('photos_credit')}</p></header>
{cover(post, lang, current)}</div>
<div class="journal-reading"><aside class="journal-index"><h2>{t('chapters')}</h2><nav aria-label="{t('chapters')}">{contents}</nav><p>{t('photos_hint')}</p></aside>
<div class="journal-body"><div class="journal-prose journal-intro"><p>{E(text(post['intro'], lang))}</p>{technical}</div>{''.join(sections)}<div class="journal-closing journal-prose"><p class="eyebrow">{t("reflection")}</p><p>{E(text(post['closing'], lang))}</p><span class="journal-signature">Emilly</span><a class="text-link" href="{link('index.html')}#journal">← {t('back')}</a></div></div></div>
{related_stories(post, posts, entities, lang, link, ui)}</article>
<dialog class="photo-dialog" aria-label="{t('photo')}" data-photo-label="{t('photo')}" data-of-label="{t('of')}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{t('close')} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{t('previous_photo')}">←</button><button type="button" data-photo-next aria-label="{t('next_photo')}">→</button></div></dialog></main>'''
