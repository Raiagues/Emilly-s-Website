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
        if file.name == 'ui.json':
            continue
        post = json.loads(file.read_text())
        if not post.get('published', False):
            continue
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', post['slug']), file
        date.fromisoformat(post['date'])
        ids = [s['id'] for s in post['sections']]
        assert len(ids) == len(set(ids)) and all(re.fullmatch(r'[a-z][a-z0-9-]*', i) for i in ids)
        for key in ('title', 'subtitle', 'intro', 'period', 'closing'):
            assert post[key].get('en'), (file, key)
        for photo in post['photos'].values():
            asset = (root / photo['file']).resolve()
            assert asset.is_relative_to((root / 'portifolio').resolve()) and asset.is_file(), asset
            assert photo['caption'].get('en') and photo['width'] > 0 and photo['height'] > 0
        for key in post['cover'] + [key for section in post['sections'] for key in section.get('photos', [])]:
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
    return sorted(posts, key=lambda p: p['date'], reverse=True)


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
    return f'<section class="journal-feed" id="journal"><div class="section-title"><h2>{t("latest")}</h2></div>{"".join(cards)}</section>'


def story(post, lang, current, link, ui):
    t = lambda key: E(text(ui[key], lang))
    paragraphs = lambda items: ''.join(f'<p>{E(text(p, lang))}</p>' for p in items)
    contents = ''.join(f'<a href="#{s["id"]}">{E(text(s["title"], lang))}</a>' for s in post['sections'])
    technical = ''
    if post.get('technical_path') and not post.get('resource'):
        technical = f'<p><a class="text-link" href="{link(post["technical_path"])}">{E(text(post.get("technical_label", ui["technical"]), lang))} →</a></p>'
    sections = []
    for section in post['sections']:
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
        sources = ''.join(f'<p><a class="text-link" href="{E(source["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{E(text(source["label"], lang))} ↗</a></p>' for source in section.get('links', []))
        sections.append(f'''<section id="{section['id']}" class="journal-chapter"><div class="journal-prose"><h2>{E(text(section['title'], lang))}</h2>{paragraphs(section['paragraphs'])}{sources}{resource}{letter}</div><div class="journal-gallery {'single-photo' if len(photos) == 1 else ''}">{''.join(photos)}</div></section>''')
    return f'''<main id="main" class="container journal-page"><a class="text-link journal-back" href="{link('index.html')}#journal">← {t('back')}</a>
<article><header class="journal-heading"><p class="journal-meta">{E(text(post.get('series', ''), lang))} · {E(text(post['period'], lang))}</p><h1>{E(text(post['title'], lang))}</h1><p class="journal-deck">{E(text(post['subtitle'], lang))}</p><p class="journal-byline">Emilly Rodrigues <span aria-hidden="true">/</span> {t('photos_credit')}</p></header>
{cover(post, lang, current)}
<div class="journal-reading"><aside class="journal-index"><h2>{t('chapters')}</h2><nav aria-label="{t('chapters')}">{contents}</nav><p>{t('photos_hint')}</p></aside>
<div class="journal-body"><div class="journal-prose journal-intro"><p>{E(text(post['intro'], lang))}</p>{technical}</div>{''.join(sections)}<div class="journal-closing journal-prose"><p>{E(text(post['closing'], lang))}</p><span class="journal-signature">Emilly</span><a class="text-link" href="{link('index.html')}#journal">← {t('back')}</a></div></div></div>
</article>
<dialog class="photo-dialog" aria-label="{t('photo')}" data-photo-label="{t('photo')}" data-of-label="{t('of')}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{t('close')} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{t('previous_photo')}">←</button><button type="button" data-photo-next aria-label="{t('next_photo')}">→</button></div></dialog></main>'''
