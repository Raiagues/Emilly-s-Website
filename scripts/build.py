#!/usr/bin/env python3
"""Build the multilingual portfolio: short homepage, directories, and case studies."""
from pathlib import Path
import html
import hashlib
import json
import os
import runpy
import shutil
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
D = runpy.run_path(str(ROOT / 'content/data.py'))
LANGS, UI, PROJECTS, SKILLS = (D[k] for k in ['LANGS', 'UI', 'PROJECTS', 'SKILLS'])
SITE_URL = os.environ.get('SITE_URL', 'https://raiagues.github.io/Emilly-s-Website').rstrip('/')
E = html.escape
EMAIL = D['EMAIL']
ALL_PATHS = []
J = runpy.run_path(str(ROOT / 'scripts/journal.py'))
POSTS = J['load_posts'](ROOT)
JUI = json.loads((ROOT / 'content/journal/ui.json').read_text())
UI['home'] = JUI['home']
SECTIONS = [('home', 'index.html'), ('projects', 'projects.html'), ('experience', 'experience.html'),
            ('about', 'about.html'), ('recognition', 'recognition.html'), ('contact', 'contact.html')]
MEDIA = {id: f'img/projects/{name}.jpg' for id, name in [('project_9', 'cubesat'), ('project_7', 'vehicle')]
         if (ROOT / f'img/projects/{name}.jpg').exists()}

def loc(path, lang):
    return path if lang == 'en' else f'{lang}/{path}'

def relative(current, target):
    return os.path.relpath(target, Path(current).parent).replace(os.sep, '/')

def asset_version(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]

def asset_url(current, path):
    return relative(current, path) + '?v=' + asset_version(path)

def detail(p):
    return f'pages/{p["kind"]}/{p["id"]}.html'

def txt(key, lang):
    return UI[key][lang]

def href(current, target, lang):
    return relative(current, loc(target, lang))

def tags(p, limit=4):
    return '<div class="tags">' + ''.join(f'<span>{E(x)}</span>' for x in p['tech'][:limit]) + '</div>'

def layout(path, lang, title, description, body, active='home'):
    current = loc(path, lang)
    r = lambda x: relative(current, x)
    asset = lambda x: asset_url(current, x)
    t = lambda x: txt(x, lang)
    nav = ''.join(f'<a href="{href(current, target, lang)}" {"aria-current=\"page\"" if key == active else ""}>{t(key)}</a>' for key, target in SECTIONS)
    languages = ''.join(f'<a href="{r(loc(path, code))}" lang="{code}" hreflang="{code}" aria-label="{name}" {"aria-current=\"page\"" if code == lang else ""}>{code.upper()}</a>' for code, name in [('en','English'),('pt','Português'),('fr','Français'),('es','Español')])
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{SITE_URL}/{loc(path, code)}">' for code in LANGS)
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'inLanguage': lang}
    if path == 'index.html':
        structured.update({'@type': 'ProfilePage', 'mainEntity': {'@type': 'Person', 'name': 'Emilly Raiane Rodrigues', 'sameAs': [D['LINKEDIN'], D['GITHUB']]}})
    if path.startswith('journal/'):
        post = next(post for post in POSTS if J['path'](post) == path)
        structured.update({'@type': 'BlogPosting', 'headline': title, 'datePublished': post['date'], 'author': {'@type': 'Person', 'name': 'Emilly Rodrigues'}, 'image': [SITE_URL + '/' + post['photos'][key]['file'] for key in post['cover']]})
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#f4f1e9"><meta name="color-scheme" content="light">
  <title>{E(title)} — Emilly Rodrigues</title><meta name="description" content="{E(description, quote=True)}">
  <link rel="icon" href="{asset('img/favicon.svg')}" type="image/svg+xml">
  <link rel="canonical" href="{SITE_URL}/{current}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{path}">
  <meta property="og:title" content="{E(title, quote=True)} — Emilly Rodrigues"><meta property="og:description" content="{E(description, quote=True)}">
  <meta property="og:type" content="website"><meta property="og:url" content="{SITE_URL}/{current}"><meta property="og:image" content="{SITE_URL}/img/me.png">
  <link rel="stylesheet" href="{asset('style/style.css')}">
  <script type="application/ld+json">{json.dumps(structured, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>
  <script src="{asset('src/script.js')}" defer></script>
{f'<script src="{asset("src/projects.js")}" defer></script>' if path == 'projects.html' else ''}
{f'<script src="{asset("src/journal.js")}" defer></script>' if path.startswith('journal/') else ''}
</head>
<body id="top" data-page="{active}">
<a class="skip-link" href="#main">{t('skip')}</a>
<header class="site-header"><div class="header-inner">
  <a class="wordmark" href="{href(current, 'index.html', lang)}"><img src="{asset('img/favicon.svg')}" width="34" height="34" alt="">emilly rodrigues<span class="wordmark-dot" aria-hidden="true">.</span></a>
  <nav id="main-nav" aria-label="{t('menu')}">{nav}</nav>
  <div class="languages" role="group" aria-label="{t('language')}">{languages}</div>
</div></header>
{body}
<footer class="site-footer container"><div><a class="wordmark" href="{href(current, 'index.html', lang)}">Emilly Rodrigues</a><p>© <span data-year>2026</span></p></div><div class="footer-links"><a href="{D['LINKEDIN']}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="{D['GITHUB']}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="{href(current, 'contact.html', lang)}">{t('contact')}</a><a href="#top">{t('top')} ↑</a></div></footer>
</body></html>'''

def heading(lang, title, description='', extra=''):
    return f'<div class="page-heading"><h1>{title}</h1>{f"<p>{description}</p>" if description else ""}{extra}</div>'

def project_row(p, lang, current, filterable=False, featured=False):
    title = p['title'][lang]
    search = ' '.join([title, p['summary'][lang], p['place'], *p['tech'], *[SKILLS[k][lang] for k in p['skills']]])
    attrs = f'data-project data-category="{p["category"]}" data-search="{E(search, quote=True)}"' if filterable else ''
    preview = MEDIA.get(p["id"], f'img/illustrations/{p["art"]}.svg')
    media = f'<img src="{relative(current, preview)}" alt="" width="800" height="500" loading="lazy">'
    return f'''<article class="project-row {'featured-row' if featured else ''}" {attrs} id="{p['id']}">
<a class="project-link" href="{href(current, detail(p), lang)}" {'data-result-link' if filterable else ''}>
{f'<div class="project-thumb">{media}</div>' if media else ''}
<div class="project-row-copy"><div class="row-meta"><span>{txt(p['category'], lang)}</span><span>{p['date']}</span></div><h3>{title}</h3><p>{p['summary'][lang]}</p>{tags(p)}</div>
<span class="row-open">{txt('case', lang)} <span aria-hidden="true">→</span></span></a></article>'''

def experience_row(p, lang, current, compact=False):
    return f'''<article class="experience-row"><a href="{href(current, detail(p), lang)}"><span class="experience-date">{p['date']}</span><div><h3>{p['title'][lang]}</h3><p class="place">{E(p['place'])}</p>{'' if compact else f'<p class="experience-result">{p["outcome"][lang]}</p>'}</div><span aria-hidden="true">→</span></a></article>'''

def home(lang):
    current = loc('index.html', lang)
    r = lambda x: relative(current, x)
    t = lambda x: txt(x, lang)
    jt = lambda x: E(J['text'](JUI[x], lang))
    link = lambda x: href(current, x, lang)
    body = f'''<main id="main" class="container journal-home">
<section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span class="tiny-star" aria-hidden="true">✳</span> {t('intro')}</p><h1 id="hero-title">{t('hero')}</h1><p class="discipline">{t('discipline')}</p><p class="hero-description">{jt('bio')}</p><div class="hero-actions"><a class="button button-primary" href="#journal">{jt('home')} <span aria-hidden="true">↓</span></a><a class="text-link" href="{link('projects.html')}">{t('explore')} →</a><a class="text-link" href="{r('CV_Emilly.pdf')}" download>{t('cv')} ↗</a></div></div><div class="hero-visual"><div class="orbit-art" aria-hidden="true"><div class="planet"></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><span class="orbital-point point-one"></span><span class="orbital-point point-two"></span><span class="hero-star">✳</span><span class="coordinates">BR → FR → CH</span></div><img class="portrait" src="{r('img/me.png')}" alt="{t('portrait')}" width="484" height="718" fetchpriority="high"><div class="portrait-note"><span aria-hidden="true">↗</span><p>{t('orbit_note')}</p></div><span class="visual-caption">AEROSPACE / EMBEDDED / HUMAN</span></div></section>
{J['feed'](POSTS, lang, current, link, JUI)}
<section class="journal-work" id="projects"><div><h2>{jt('work')}</h2><p>{jt('work_body')}</p></div><div class="journal-work-links"><a class="button button-primary" href="{link('projects.html')}">{t('all_projects')} →</a><a class="button button-soft" href="{link('experience.html')}" id="experience">{t('experience')} →</a><a class="text-link" href="{r('CV_Emilly.pdf')}" download>{t('cv')} ↓</a></div></section>
<div class="journal-footlinks"><a class="text-link" id="about-me" href="{link('about.html')}">{t('about')} →</a><a class="text-link" id="recognition" href="{link('recognition.html')}">{t('awards_title')} →</a><a class="text-link" id="contact" href="{link('contact.html')}">{t('contact')} →</a></div></main>'''
    return layout('index.html', lang, jt('home'), J['text'](JUI['bio'], lang), body)

def journal(post, lang):
    path = J['path'](post)
    current = loc(path, lang)
    body = J['story'](post, lang, current, lambda x: href(current, x, lang), JUI)
    return layout(path, lang, J['text'](post['title'], lang), J['text'](post['subtitle'], lang), body)

def projects(lang):
    current = loc('projects.html', lang)
    t = lambda x: txt(x, lang)
    work = [p for p in PROJECTS if p['kind'] == 'projects']
    categories = ['all', 'space', 'hardware', 'control', 'software', 'outreach']
    filters = ''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(key == "all").lower()}">{t(key)}</button>' for key in categories)
    body = f'''<main id="main" class="container directory-page">
{heading(lang, t('projects'), t('work_body'))}
<div class="project-tools" data-project-tools hidden><label class="search-label" for="project-search">{t('search')}<input id="project-search" type="search" placeholder="{t('search_short')}" autocomplete="off" maxlength="120"></label><div class="filters" role="group" aria-label="{t('filter_label')}">{filters}</div><div class="filter-status"><p id="results-count" aria-live="polite" data-label="{t('results')}"></p><button id="reset-filters" type="button">{t('reset')}</button></div></div>
<div id="project-grid" class="project-list">{''.join(project_row(p, lang, current, True) for p in work)}</div><div id="empty-state" class="empty-state" hidden><h2>{t('empty')}</h2></div>
</main>'''
    return layout('projects.html', lang, t('projects'), t('work_body'), body, 'projects')

def experience(lang):
    current = loc('experience.html', lang)
    t = lambda x: txt(x, lang)
    body = '<main id="main" class="container directory-page">' + heading(lang, t('experience'), t('exp_body'))
    body += '<div class="experience-list">' + ''.join(experience_row(p, lang, current) for p in PROJECTS if p['kind'] == 'experience') + '</div></main>'
    return layout('experience.html', lang, t('experience'), t('exp_body'), body, 'experience')

def about(lang):
    current = loc('about.html', lang)
    t = lambda x: txt(x, lang)
    evidence = ''.join(f'<article class="skill"><h3>{SKILLS[key][lang]}</h3><p>{copy[lang]}</p><a class="text-link" href="{href(current, detail(next(p for p in PROJECTS if p["id"] == id)), lang)}">{txt("case", lang)} →</a></article>' for key, id, copy in D['EVIDENCE'])
    body = f'''<main id="main" class="container content-page">{heading(lang, t('about'))}
<div class="about-layout"><div class="prose"><p>{t('about_p1')}</p><p>{t('about_p2')}</p><a class="text-link" href="{href(current, 'pages/projects/project_17.html', lang)}">EP Aero →</a></div><aside class="education"><h2>{t('education')}</h2><p><strong>{t('degree1')}</strong><span>{t('degree1_date')}</span></p><p><strong>{t('degree2')}</strong><span>{t('degree2_date')}</span></p><p class="language-levels">{t('languages')}</p><a class="button button-soft" href="{relative(current, 'CV_Emilly.pdf')}" download>{t('cv')} ↓</a></aside></div>
<section class="skills-section"><h2>{t('skills_title')}</h2><p>{t('skills_body')}</p><div class="skills-grid">{evidence}</div></section></main>'''
    return layout('about.html', lang, t('about'), t('short_bio'), body, 'about')

def recognition(lang):
    current = loc('recognition.html', lang)
    t = lambda x: txt(x, lang)
    related = {}
    for post in POSTS:
        if post.get('related_award'):
            related[post['related_award']] = f'<p><a class="text-link" href="{href(current, J["path"](post), lang)}">{E(J["text"](post.get("award_link_label", post["title"]), lang))} →</a></p>'
    awards = ''.join(f'<article class="award"><span class="award-year">{date}</span><div><h2>{E(name)}</h2><p>{desc[lang]}</p>{related.get(name, "")}</div><a class="text-link" href="{url or relative(current, "CV_Emilly.pdf")}" aria-label="{E(t("source") + ": " + name, quote=True)}" {"target=\"_blank\" rel=\"noopener noreferrer\"" if url else ""}>{t("source")} ↗</a></article>' for date, name, desc, url in D['AWARDS'])
    body = f'''<main id="main" class="container content-page">{heading(lang, t('awards_title'), t('awards_body'))}<div class="awards-list">{awards}</div>
<article class="press-panel"><div><p class="role-label">Exame</p><h2>{t('press_title')}</h2><p>{t('press_body')}</p></div><a class="button button-primary" href="{D['EXAME']}" target="_blank" rel="noopener noreferrer">{t('article')} ↗</a></article></main>'''
    return layout('recognition.html', lang, t('awards_title'), t('awards_body'), body, 'recognition')

def contact(lang):
    current = loc('contact.html', lang)
    t = lambda x: txt(x, lang)
    body = f'''<main id="main" class="container content-page">{heading(lang, t('contact_title'), t('contact_body'))}<div class="contact-layout"><div class="contact-info"><h2>{t('direct')}</h2><a class="email-address" href="mailto:{EMAIL}">{EMAIL}</a><button class="button button-soft" type="button" id="copy-email" data-email="{EMAIL}" data-success="{t('copied')}" data-error="{t('copy_error')}" hidden>{t('copy')}</button><p id="copy-status" role="status"></p><a href="{D['LINKEDIN']}" target="_blank" rel="noopener noreferrer">LinkedIn ↗</a><a href="{D['GITHUB']}" target="_blank" rel="noopener noreferrer">GitHub ↗</a><a href="{relative(current, 'CV_Emilly.pdf')}" download>{t('cv')} ↓</a></div>
<form class="contact-form" action="https://formsubmit.co/{EMAIL}" method="POST"><div class="form-row"><label>{t('name')}<input type="text" name="name" autocomplete="name" required maxlength="100"></label><label>{t('email')}<input type="email" name="email" autocomplete="email" required maxlength="254"></label></div><label>{t('subject')}<input type="text" name="subject" required maxlength="160"></label><label>{t('message')}<textarea name="message" rows="6" required maxlength="5000"></textarea></label><input type="hidden" name="_subject" value="Portfolio · Emilly Rodrigues"><input type="hidden" name="_template" value="table"><input class="honeypot" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="button button-primary" type="submit">{t('send')} →</button><p class="form-note">{t('form_note')} <a href="https://formsubmit.co/privacy.pdf" target="_blank" rel="noopener noreferrer">FormSubmit ↗</a></p></form></div></main>'''
    return layout('contact.html', lang, t('contact'), t('contact_body'), body, 'contact')

def project(p, lang):
    path = detail(p)
    current = loc(path, lang)
    t = lambda x: txt(x, lang)
    parent = p['kind'] + '.html'
    peers = [q for q in PROJECTS if q['kind'] == p['kind']]
    idx = peers.index(p)
    prev = peers[idx - 1] if idx > 0 else None
    nxt = peers[idx + 1] if idx + 1 < len(peers) else None
    links = ''.join(f'<a class="button button-soft" href="{url}" target="_blank" rel="noopener noreferrer">{t(label)} ↗</a>' for label, url in p['links'])
    media = ''
    related_post = next((post for post in POSTS if post.get('technical_path') == path), None)
    if related_post:
        label = related_post.get('journal_link_label', JUI['cern_link'] if p['id'] == 'cern' else related_post['title'])
        media = f'<aside class="journal-callout"><a class="text-link" href="{href(current, J["path"](related_post), lang)}">{E(J["text"](label, lang))} →</a></aside>'
    if p['id'] in MEDIA:
        media = f'<figure class="project-media"><img src="{relative(current, MEDIA[p["id"]])}" alt="{E(p["title"][lang], quote=True)}" width="640" height="400"><figcaption>{t("video_caption")}</figcaption></figure>'
    pager = ''.join(f'<a href="{href(current, detail(q), lang)}"><span>{t(key)}</span><strong>{q["title"][lang]} {arrow}</strong></a>' for q, key, arrow in [(prev, 'previous', '←'), (nxt, 'next', '→')] if q)
    body = f'''<main id="main" class="container detail-page"><nav class="breadcrumb" aria-label="{t('projects')}"><a href="{href(current, parent, lang)}" {f'data-back-results="{p["id"]}"' if p['kind'] == 'projects' else ''}>← {t('back_results') if p['kind'] == 'projects' else t('experience')}</a><span>/ {t(p['category'])}</span></nav>
<div class="detail-heading"><p class="role-label">{E(p['place'])} · {p['date']}</p><h1>{p['title'][lang]}</h1><p>{p['summary'][lang]}</p></div>
<div class="detail-layout"><aside class="project-facts"><h2>{t('toolkit')}</h2>{tags(p, None)}<h2>{t('contents')}</h2><nav class="contents-nav" aria-label="{t('contents')}"><a href="#contribution">{t('contributions')}</a><a href="#results">{t('outcome')}</a><a href="#skills">{t('practice')}</a>{f'<a href="#resources">{t("links")}</a>' if links else ''}</nav></aside>
<div class="detail-story"><section id="contribution"><h2>{t('contributions')}</h2><ul>{''.join(f'<li>{item[lang]}</li>' for item in p['contributions'])}</ul></section><section id="results" class="result-panel"><h2>{t('outcome')}</h2><p>{p['outcome'][lang]}</p></section>{media}<section id="skills"><h2>{t('practice')}</h2><div class="skill-tags">{''.join(f'<span>{SKILLS[s][lang]}</span>' for s in p['skills'])}</div></section>{f'<section id="resources"><h2>{t("links")}</h2><div class="detail-links">{links}</div></section>' if links else ''}</div></div>
<nav class="project-pagination" aria-label="{t('projects')}">{pager}</nav><div class="detail-bottom"><a class="button button-soft" href="{href(current, parent, lang)}" {f'data-back-results="{p["id"]}"' if p['kind'] == 'projects' else ''}>← {t('back_results') if p['kind'] == 'projects' else t('experience')}</a><a class="text-link" href="{href(current, 'contact.html', lang)}">{t('contact')} →</a></div></main>'''
    return layout(path, lang, p['title'][lang], p['summary'][lang], body, p['kind'])

def write(path, content):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    ALL_PATHS.append(path)

def main():
    # Only generated journal pages are removed; unpublished entries stay out of the site.
    for lang in LANGS:
        folder = ROOT / loc('journal', lang)
        if folder.exists():
            for old in folder.glob('*.html'):
                old.unlink()
    for lang in LANGS:
        for path, render in [('index.html', home), ('projects.html', projects), ('experience.html', experience), ('about.html', about), ('recognition.html', recognition), ('contact.html', contact)]:
            write(loc(path, lang), render(lang))
        for post in POSTS:
            write(loc(J['path'](post), lang), journal(post, lang))
        for p in PROJECTS:
            write(loc(detail(p), lang), project(p, lang))
    for old in ['pages/projects/projects_exemple.html', 'pages/experience/experience_exemple.html']:
        write(old, '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=../../projects.html"><title>Projects — Emilly Rodrigues</title><a href="../../projects.html">Projects</a></html>')
    base = SITE_URL + '/'
    write('404.html', f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found — Emilly Rodrigues</title><link rel="stylesheet" href="{base}style/style.css?v={asset_version("style/style.css")}"><main class="container content-page"><h1>Page not found.</h1><p><a class="button button-primary" href="{base}">Home →</a></p></main></html>')
    write('.nojekyll', '')
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE_URL}/{p}</loc></url>' for p in ALL_PATHS if p.endswith('.html') and 'exemple' not in p and p != '404.html') + '</urlset>')
    dist = ROOT / 'dist'
    if dist.exists():
        shutil.rmtree(dist)
    dist.mkdir()
    for path in ALL_PATHS:
        dest = dist / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, dest)
    for folder in ['style', 'src', 'img', 'doc']:
        shutil.copytree(ROOT / folder, dist / folder, dirs_exist_ok=True)
    assets = {photo['file'] for post in POSTS for photo in post['photos'].values()}
    assets.update(post['resource']['file'] for post in POSTS if post.get('resource'))
    for asset in assets:
        destination = dist / asset
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / asset, destination)
    for name in ['CV_Emilly.pdf', 'Emilly_Rodrigues_Resume.pdf']:
        shutil.copyfile(ROOT / name, dist / name)
    print(f'Built {len(PROJECTS)} case studies and {len(POSTS)} journal posts, plus 6 main pages × {len(LANGS)} languages.')

if __name__ == '__main__':
    main()
