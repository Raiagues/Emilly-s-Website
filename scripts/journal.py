"""Small, data-driven journal renderer. Posts are plain JSON, never executable HTML."""
import html
import json
import os
import re
import runpy
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

E = html.escape
LANGS = ('en', 'pt', 'fr', 'es')
icon = runpy.run_path(str(Path(__file__).parent / 'icons.py'))['icon']


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
            assert re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?', value), (file, value)
            date.fromisoformat(value + {4: '-01-01', 7: '-01', 10: ''}[len(value)])
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
    by_slug = {post['slug']: post for post in posts}
    for post in posts:
        for section in post['sections']:
            for destination in section.get('stories', []):
                assert destination['slug'] in by_slug, destination
                assert destination['title'].get('en') and destination['description'].get('en')
                assert not destination.get('section') or destination['section'] in {s['id'] for s in by_slug[destination['slug']]['sections']}
    return sorted(posts, key=lambda p: max((e['date'] for e in p.get('timeline', [])), default=p['date']), reverse=True)


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


def cover(post, lang, current, thumbnail=False):
    frames = []
    for key in (post['cover'][-1:] if thumbnail else post['cover']):
        photo = post['photos'][key]
        orientation = 'photo-portrait' if photo['height'] > photo['width'] else 'landscape'
        frames.append(f'<div class="cover-photo {orientation}">{photo_html(photo, lang, current, not thumbnail)}</div>')
    return '<div class="journal-mosaic" aria-hidden="true">' + ''.join(frames) + '</div>'


def gallery(items):
    """Balance rows using the photos' real proportions, preserving reading order."""
    rows, row = [], []
    for markup, ratio in items:
        row.append((markup, ratio))
        if sum(r for _, r in row) >= 2.1 or len(row) == 3:
            rows.append(row)
            row = []
    if row:
        if len(row) == 1 and row[0][1] < 1 and rows and len(rows[-1]) < 3:
            rows[-1].extend(row)
        else:
            rows.append(row)
    return '<div class="journal-gallery">' + ''.join(
        f'<div class="photo-row" style="--row-max:{sum(r for _,r in row)*340 + len(row)*24 + (len(row)-1)*20:.0f}px">' + ''.join(markup for markup, _ in row) + '</div>' for row in rows
    ) + '</div>' if rows else ''


def feed(posts, lang, current, link, ui):
    t = lambda key: E(text(ui[key], lang))
    cards = []
    for number, post in enumerate(posts, 1):
        photo = post['photos'][post['cover'][-1]]
        extra = post['photos'][post['cover'][0]]
        orientation = 'portrait-cover' if photo['height'] > photo['width'] else 'landscape-cover'
        album = f'<div class="notebook-photos {orientation}" aria-hidden="true"><figure class="notebook-photo main-photo">{photo_html(photo, lang, current)}<figcaption>{E(text(photo["caption"], lang))}</figcaption></figure><figure class="notebook-photo small-photo">{photo_html(extra, lang, current)}</figure></div>'
        cards.append(f'''<article class="journal-entry"><a href="{link(path(post))}" class="journal-entry-link">
{album}<div class="journal-entry-copy"><p class="journal-meta">{E(text(post['period'], lang))}</p><h3>{E(text(post['title'], lang))}</h3><p>{E(text(post['intro'], lang))}</p><span class="notebook-read">{t('read')} </span><span class="notebook-page" aria-hidden="true">{number:02d} / {len(posts):02d}</span></div></a></article>''')
    events = sorted(((event, post) for post in posts for event in post.get('timeline', [])), key=lambda item: item[0]['date'], reverse=True)
    timeline = ''.join(f'<li><time datetime="{event["date"]}">{E(text(event["label"], lang))}</time><a href="{link(path(post))}{"#" + event["section"] if event.get("section") else ""}">{E(text(event["title"], lang))} </a></li>' for event, post in events)
    return f'<section class="journal-feed notebook" id="journal"><div class="notebook-heading"><div><p class="eyebrow">{t("notebook_label")}</p><h2>{t("latest")}</h2></div><p class="archive-order">{t("newest_first")}</p></div><details class="journal-timeline"><summary>{t("timeline")} <span aria-hidden="true">+</span></summary><nav aria-label="{t("timeline")}"><ol>{timeline}</ol></nav></details><div class="journal-cards">{"".join(cards)}</div></section>'


def chronology(post, posts, lang, current, link, ui):
    entries = []
    for item in posts:
        event = max(item.get('timeline', []), key=lambda e: e['date'], default=None)
        date_label = text(event['label'] if event else item['period'], lang)
        photo = item['photos'][item['cover'][-1]]
        active = 'aria-current="page"' if item['slug'] == post['slug'] else ''
        entries.append(f'<li data-date="{event["date"] if event else item["date"]}"><a href="{link(path(item))}" {active}><img src="{relative(current, photo["file"])}" alt="" width="56" height="56" loading="lazy"><span><time datetime="{event["date"] if event else item["date"]}">{E(date_label)}</time><span>{E(text(item["title"], lang))}</span></span></a></li>')
    return f'<details class="story-menu"><summary>{E(text(ui["archive"], lang))}</summary><p class="archive-order">{E(text(ui["newest_first"], lang))}</p><nav class="journal-chronology" aria-label="{E(text(ui["archive"], lang))}"><ol>{"".join(entries)}</ol></nav></details>'


def story(post, lang, current, link, ui, posts, entities, parts_only=False):
    t = lambda key: E(text(ui[key], lang))
    paragraphs = lambda items: ''.join(f'<p>{E(text(p, lang))}</p>' for p in items)
    contents = ''.join(f'<a href="#{s["id"]}">{E(text(s["title"], lang))}</a>' for s in post['sections'])
    technical = ''
    if post.get('technical_path') and not post.get('resource'):
        technical = f'<p><a class="text-link" href="{link(post["technical_path"])}">{E(text(post.get("technical_label", ui["technical"]), lang))} </a></p>'
    sections = []
    for number, section in enumerate(post['sections'], 1):
        photos = []
        for key in section.get('photos', []):
            photo = post['photos'][key]
            ratio = photo['width'] / photo['height']
            markup = f'''<figure class="journal-photo {'landscape' if ratio > 1 else 'photo-portrait'}" style="--photo-ratio: {ratio:.6f}"><a href="{relative(current, photo['file'])}" data-gallery data-caption="{E(text(photo['caption'], lang), quote=True)}">{photo_html(photo, lang, current)}<span class="photo-expand" aria-hidden="true">{icon("zoom")}</span></a><figcaption>{E(text(photo['caption'], lang))}</figcaption></figure>'''
            photos.append((markup, ratio))
        resource = ''
        if section.get('resource') and post.get('resource'):
            resource = f'<div class="journal-resource"><a class="button button-primary" href="{relative(current, post["resource"]["file"])}" target="_blank" rel="noopener noreferrer">{E(text(post["resource"]["label"], lang))} </a><a class="text-link" href="{link(post.get("technical_path", "projects.html"))}">{t("technical")} </a></div>'
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
        sources = ''.join(f'<p><a class="text-link" href="{E(source["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{E(text(source["label"], lang))} </a></p>' for source in section.get('links', []))
        paired = bool(photos) and photos[0][1] < 1 and not documents and len(' '.join(text(p, lang) for p in section['paragraphs'])) < 1150
        lead = photos[0][0] if paired else ''
        remaining = photos[1:] if paired else photos
        sections.append(f'''<section id="{section['id']}" class="journal-chapter {'chapter-paired' if paired else 'chapter-text'}"><div class="chapter-layout"><div class="journal-prose"><span class="chapter-number" aria-hidden="true">{number:02d}</span><h2>{E(text(section['title'], lang))}</h2>{paragraphs(section['paragraphs'])}{sources}{resource}{documents}{letter}</div>{f'<div class="chapter-image">{lead}</div>' if lead else ''}</div>{gallery(remaining)}</section>''')
    if parts_only:
        return {'chapters': ''.join(sections), 'technical': technical, 'contents': contents}
    return f'''<main id="main" class="container journal-page"><a class="text-link journal-back" href="{link('index.html')}#journal"> {t('back')}</a>
<article><div class="journal-opening"><header class="journal-heading"><p class="journal-meta">{E(text(post.get('series', ''), lang))} · {E(text(post['period'], lang))}</p><h1>{E(text(post['title'], lang))}</h1><p class="journal-deck">{E(text(post['subtitle'], lang))}</p><p class="journal-byline">{t('photos_credit')}</p></header>
{cover(post, lang, current)}</div>
<div class="journal-reading"><aside class="journal-sidebar"><details class="journal-navigation" open><summary><span class="navigation-hide">{t('hide_navigation')}</span><span class="navigation-show">{t('show_navigation')}</span></summary><div class="journal-sidebar-content"><details class="journal-index" open><summary>{t('chapters')}</summary><nav aria-label="{t('chapters')}">{contents}</nav></details>{chronology(post, posts, lang, current, link, ui)}<p class="gallery-hint">{t('photos_hint')}</p></div></details></aside>
<div class="journal-body"><div class="journal-prose journal-intro"><p>{E(text(post['intro'], lang))}</p>{technical}</div>{''.join(sections)}<div class="journal-closing journal-prose"><p>{E(text(post['closing'], lang))}</p></div></div></div>
</article>
<dialog class="photo-dialog" aria-label="{t('photo')}" data-photo-label="{t('photo')}" data-of-label="{t('of')}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{t('close')} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{t('previous_photo')}">{icon("previous")}</button><button type="button" data-photo-next aria-label="{t('next_photo')}">{icon("next")}</button></div></dialog></main>'''
