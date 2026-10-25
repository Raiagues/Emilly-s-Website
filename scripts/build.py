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
icon = runpy.run_path(str(ROOT / 'scripts/icons.py'))['icon']
ART = runpy.run_path(str(ROOT / 'scripts/illustrations.py'))
art = lambda name: ART['illustration'](ROOT, name)
J = runpy.run_path(str(ROOT / 'scripts/journal.py'))
POSTS = J['load_posts'](ROOT)
ENTITIES = J['load_entities'](ROOT, POSTS)
INNER = runpy.run_path(str(ROOT / 'scripts/inner_redesign.py'))
CERN = runpy.run_path(str(ROOT / 'scripts/cern_redesign.py'))
DAMAS = runpy.run_path(str(ROOT / 'scripts/damas_redesign.py'))
WINGBOX = runpy.run_path(str(ROOT / 'scripts/wingbox_redesign.py'))
DESIGN = runpy.run_path(str(ROOT / 'scripts/redesign_components.py'))
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
    nav = ''.join(f'<a href="{href(current, target, lang)}" {"aria-current=\"page\"" if key == active else ""}>{icon(key)}<span>{t(key)}</span></a>' for key, target in SECTIONS)
    languages = ''.join(f'<a href="{r(loc(path, code))}" lang="{code}" hreflang="{code}" aria-label="{name}" {"aria-current=\"page\"" if code == lang else ""}>{code.upper()}</a>' for code, name in [('en','English'),('pt','Português'),('fr','Français'),('es','Español')])
    alternates = ''.join(f'<link rel="alternate" hreflang="{code}" href="{SITE_URL}/{loc(path, code)}">' for code in LANGS)
    structured = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'inLanguage': lang}
    if path == 'index.html':
        structured.update({'@type': 'ProfilePage', 'mainEntity': {'@type': 'Person', 'name': 'Emilly Raiane Rodrigues', 'sameAs': [D['LINKEDIN'], D['GITHUB']]}})
    post = next((post for post in POSTS if J['path'](post) == path), None)
    if post:
        structured.update({'@type': 'BlogPosting', 'headline': title, 'datePublished': post['date'], 'author': {'@type': 'Person', 'name': 'Emilly Rodrigues'}, 'image': [SITE_URL + '/' + post['photos'][key]['file'] for key in post['cover']]})
    redesigned_home = path == 'index.html'
    cern_report = path == 'pages/experience/cern.html'
    damas_project = path == 'pages/projects/damas-espaciais.html'
    wingbox_project = path == 'pages/projects/wing-box-analysis.html'
    design = DESIGN['Design'](globals(), lang, path)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#F4EEE2"><meta name="color-scheme" content="light">
  <title>{E(title)} — Emilly Rodrigues</title><meta name="description" content="{E(description, quote=True)}">
  <link rel="icon" href="{asset('img/favicon.svg')}" type="image/svg+xml">
  <link rel="canonical" href="{SITE_URL}/{current}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{path}">
  <meta property="og:title" content="{E(title, quote=True)} — Emilly Rodrigues"><meta property="og:description" content="{E(description, quote=True)}">
  <meta property="og:type" content="website"><meta property="og:url" content="{SITE_URL}/{current}"><meta property="og:image" content="{SITE_URL}/img/me.png">
{f'<link rel="stylesheet" href="{asset("style/style.css")}">' if path == 'about.html' else ''}
  <link rel="stylesheet" href="{asset('style/fonts.css')}">
  <link rel="stylesheet" href="{asset('style/home.css')}">
{f'<link rel="stylesheet" href="{asset("style/launch.css")}">' if redesigned_home else ''}
{f'<link rel="stylesheet" href="{asset("style/media.css")}">' if redesigned_home else f'<link rel="stylesheet" href="{asset("style/inner.css")}">'}
{f'<link rel="stylesheet" href="{asset("style/journal-design.css")}">' if not cern_report and (post or path == 'journal.html' or path.startswith('pages/')) else ''}
  <link rel="stylesheet" href="{asset('style/components.css')}">
{f'<link rel="stylesheet" href="{asset("style/work.css")}">' if not cern_report and (path in ('projects.html','experience.html','recognition.html','contact.html') or path.startswith('pages/')) else ''}{chr(10) + f'<link rel="stylesheet" href="{asset("style/cern.css")}">' if cern_report else ''}
  <script type="application/ld+json">{json.dumps(structured, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script>{chr(10) + f'<link rel="stylesheet" href="{asset("style/damas.css")}"><script src="{asset("src/damas.js")}" defer></script>' if damas_project else ''}{chr(10) + f'<link rel="stylesheet" href="{asset("style/wingbox.css")}"><script src="{asset("src/wingbox.js")}" defer></script>' if wingbox_project else ''}
  <script src="{asset('src/home.js') if redesigned_home else asset('src/script.js')}" defer></script>
  <script src="{asset('src/redesign.js')}" defer></script>
{f'<script src="{asset("src/projects.js")}" defer></script>' if path in ('projects.html','experience.html') else ''}
{f'<script src="{asset("src/journal.js")}" defer></script>' if post or cern_report else ''}{chr(10) + f'<script src="{asset("src/cern.js")}" defer></script>' if cern_report else ''}
{f'<script src="{asset("src/stories.js")}" defer></script>' if not cern_report and (post or path == 'journal.html' or path.startswith('pages/')) else ''}
</head>
<body id="top" data-page="{active}"{' class="redesign-home"' if redesigned_home else ' class="redesign-inner"'}>
<a class="skip-link" href="#main">{t('skip')}</a>
{'' if redesigned_home else design.header(active)}
{body}
{'' if redesigned_home else design.footer()}
</body></html>'''

def social_links():
    return ''.join(f'<a class="icon-link" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="{name}" title="{name}">{icon(key)}</a>' for key, name, url in [('linkedin', 'LinkedIn', D['LINKEDIN']), ('github', 'GitHub', D['GITHUB'])])

def heading(lang, title, description='', extra=''):
    return f'<div class="page-heading"><h1>{title}</h1>{f"<p>{description}</p>" if description else ""}{extra}</div>'

def project_row(p, lang, current, filterable=False, featured=False):
    title = p['title'][lang]
    search = ' '.join([title, p['summary'][lang], p['place'], *p['tech'], *[SKILLS[k][lang] for k in p['skills']]])
    attrs = f'data-project data-category="{p["category"]}" data-search="{E(search, quote=True)}"' if filterable else ''
    return f'''<article class="project-row {'featured-row' if featured else ''}" {attrs} id="{p['id']}">
<a class="project-link art-link" href="{href(current, detail(p), lang)}" {'data-result-link' if filterable else ''}>
<div class="project-thumb">{art(p['art'])}<span class="art-date">{p['date']}</span></div>
<div class="project-row-copy"><div class="row-meta"><span>{txt(p['category'], lang)}</span></div><h3>{title}</h3><p>{p['summary'][lang]}</p>{tags(p)}</div></a></article>'''

def experience_row(p, lang, current, compact=False):
    return f'''<article class="experience-row"><a class="art-link" href="{href(current, detail(p), lang)}"><div class="experience-art project-thumb">{art(p['art'])}<span class="art-date">{p['date']}</span></div><div class="experience-copy"><p class="row-meta">{E(p['place'])}</p><h3>{p['title'][lang]}</h3><p class="experience-result">{p['summary'][lang] if compact else p['outcome'][lang]}</p>{tags(p, 3)}</div></a></article>'''

def featured_project(lang, current):
    p = next(p for p in PROJECTS if p['id'] == 'flight-platform')
    return f'''<article class="current-project"><a class="art-link current-project-link" href="{href(current, detail(p), lang)}"><div class="current-project-copy"><p class="eyebrow">{txt('current_work', lang)} / {p['date']}</p><h2>{txt('current_title', lang)}</h2><p>{p['summary'][lang]}</p><p class="current-status">{p['outcome'][lang]}</p></div><div class="current-project-art">{art('platform')}</div></a></article>'''

def home(lang):
    body = runpy.run_path(str(ROOT / 'scripts/home_redesign.py'))['render'](globals(), lang)
    return layout('index.html', lang, J['text'](JUI['home'], lang), J['text'](JUI['bio'], lang), body)

def journal(post, lang):
    path = J['path'](post)
    current = loc(path, lang)
    body = INNER['story'](globals(), post, lang)
    return layout(path, lang, J['text'](post['title'], lang), J['text'](post['subtitle'], lang), body)

def journal_archive(lang):
    body = runpy.run_path(str(ROOT / 'scripts/journal_archive.py'))['render'](globals(), lang)
    return layout('journal.html', lang, J['text'](JUI['home'], lang), J['text'](JUI['bio'], lang), body, 'stories')

def projects(lang):
    return layout('projects.html', lang, txt('projects', lang), txt('work_body', lang), INNER['projects'](globals(), lang), 'projects')


def experience(lang):
    return layout('experience.html', lang, txt('experience', lang), txt('exp_body', lang), INNER['experience'](globals(), lang), 'experience')


def about(lang):
    current = loc('about.html', lang)
    t = lambda x: txt(x, lang)
    evidence = ''.join(f'<article class="skill"><h3>{SKILLS[key][lang]}</h3><p>{copy[lang]}</p><a class="text-link" href="{href(current, detail(next(p for p in PROJECTS if p["id"] == id)), lang)}">{txt("case", lang)} </a></article>' for key, id, copy in D['EVIDENCE'])
    body = f'''<main id="main" class="container content-page">{heading(lang, t('about'))}
<div class="about-layout"><div class="prose"><p>{t('about_p1')}</p><p>{t('about_p2')}</p><a class="text-link" href="{href(current, 'pages/projects/project_17.html', lang)}">EP Aero </a></div><aside class="education"><h2>{t('education')}</h2><p><strong>{t('degree1')}</strong><span>{t('degree1_date')}</span></p><p><strong>{t('degree2')}</strong><span>{t('degree2_date')}</span></p><p class="language-levels">{t('languages')}</p></aside></div>
<section class="skills-section"><h2>{t('awards_title')}</h2><p>{t('awards_body')}</p><a class="button button-soft" href="{href(current, 'recognition.html', lang)}">{t('recognition')}</a></section><section class="skills-section"><h2>{t('skills_title')}</h2><p>{t('skills_body')}</p><div class="skills-grid">{evidence}</div></section></main>'''
    return layout('about.html', lang, t('about'), t('short_bio'), body, 'about')

def recognition(lang):
    d = DESIGN['Design'](globals(),lang,'recognition.html')
    cards=[]
    for i,(date,name,description,url) in enumerate(D['AWARDS']):
        publisher = D['AWARD_SOURCES'][name][0]
        stamp = d.drawing('stamp-'+['rocket','satellite','star','planet','satellite'][i])
        cards.append(f'<a class="recognition-card" href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer"><div class="stamp stamp-{i%4}"><div class="stamp-inner"><span class="stamp-year">{E(date)}</span>{stamp}<span class="stamp-name">{E(name)}</span></div></div><div class="recognition-copy"><p class="eyebrow">{E(date)}</p><h2>{E(name)}</h2><p>{description[lang]}</p><span class="publication-link">{E(publisher)}<span aria-hidden="true">↗</span></span></div></a>')
    body=f'<main id="main" class="wrap inner-content recognition-page"><div class="inner-breadcrumb">{d.button(d.u("home"),d.link("index.html#recognition"),back=True)}</div><header class="recognition-heading"><p class="eyebrow">{d.t("awards_title")}</p><h1>{d.t("recognition")}</h1><p>{d.t("awards_body")}</p></header><div class="recognition-grid">{"".join(cards)}</div></main>'
    return layout('recognition.html', lang, d.t('awards_title'), d.t('awards_body'), body, 'recognition')


def contact_panel(lang, current):
    t = lambda x: txt(x, lang)
    return f'''<div class="contact-layout"><div class="contact-info"><div class="contact-postcard" aria-hidden="true">{DESIGN["Design"](globals(),lang,"contact.html").drawing("postcard-rack")}</div><h2>{t('direct')}</h2><a class="email-address" href="mailto:{EMAIL}">{EMAIL}</a><button class="button button-soft" type="button" id="copy-email" data-email="{EMAIL}" data-success="{t('copied')}" data-error="{t('copy_error')}" hidden>{t('copy')}</button><p id="copy-status" role="status"></p><div class="social-links">{social_links()}</div></div>
<form class="contact-form" action="https://formsubmit.co/{EMAIL}" method="POST"><div class="form-row"><label>{t('name')}<input type="text" name="name" autocomplete="name" required maxlength="100"></label><label>{t('email')}<input type="email" name="email" autocomplete="email" required maxlength="254"></label></div><label>{t('subject')}<input type="text" name="subject" required maxlength="160"></label><label>{t('message')}<textarea name="message" rows="6" required maxlength="5000"></textarea></label><input type="hidden" name="_subject" value="Portfolio · Emilly Rodrigues"><input type="hidden" name="_template" value="table"><input class="honeypot" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="button button-primary" type="submit">{t('send')} </button><p class="form-note">{t('form_note')} <a href="https://formsubmit.co/privacy.pdf" target="_blank" rel="noopener noreferrer">FormSubmit </a></p></form></div>'''

def contact(lang):
    t = lambda x: txt(x, lang)
    d = DESIGN['Design'](globals(),lang,'contact.html')
    body = f'<main id="main" class="wrap inner-content contact-page"><div class="inner-breadcrumb">{d.button(d.u("home"),d.link("index.html#say-hello"),back=True)}</div><header class="contact-heading"><p class="eyebrow">Par avion</p><h1>{t("contact_title")}</h1><p>{t("contact_body")}</p></header>{contact_panel(lang, loc("contact.html", lang))}</main>'
    return layout('contact.html', lang, t('contact'), t('contact_body'), body, 'contact')

def project(p, lang):
    if p['id'] == 'wing-box-analysis':
        return layout(detail(p), lang, p['title'][lang], p['summary'][lang], WINGBOX['render'](globals(), p, lang), 'projects')
    if p['id'] == 'damas-espaciais':
        return layout(detail(p), lang, p['title'][lang], p['summary'][lang], DAMAS['render'](globals(), p, lang), 'projects')
    if p['id'] == 'cern':
        body, title, description = CERN['render'](globals(), lang)
        return layout(detail(p), lang, title, description, body, 'experience')
    body = INNER['case'](globals(), p, lang)
    return layout(detail(p), lang, p['title'][lang], p['summary'][lang], body, p['kind'])


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
        for path, render in [('index.html', home), ('projects.html', projects), ('experience.html', experience), ('about.html', about), ('recognition.html', recognition), ('journal.html', journal_archive), ('contact.html', contact)]:
            write(loc(path, lang), render(lang))
        for post in POSTS:
            write(loc(J['path'](post), lang), journal(post, lang))
        for p in PROJECTS:
            write(loc(detail(p), lang), project(p, lang))
    for old in ['pages/projects/projects_exemple.html', 'pages/experience/experience_exemple.html']:
        write(old, '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=../../projects.html"><title>Projects — Emilly Rodrigues</title><a href="../../projects.html">Projects</a></html>')
    base = SITE_URL + '/'
    write('404.html', f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found — Emilly Rodrigues</title><link rel="stylesheet" href="{base}style/style.css?v={asset_version("style/style.css")}"><main class="container content-page"><h1>Page not found.</h1><p><a class="button button-primary" href="{base}">Home </a></p></main></html>')
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
    for folder in ['style', 'src', 'img']:
        shutil.copytree(ROOT / folder, dist / folder, dirs_exist_ok=True)
    assets = {photo['file'] for post in POSTS for photo in post['photos'].values()}
    assets.update(post['resource']['file'] for post in POSTS if post.get('resource'))
    for asset in assets:
        destination = dist / asset
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / asset, destination)
    print(f'Built {len(PROJECTS)} case studies and {len(POSTS)} journal posts, plus 7 main pages × {len(LANGS)} languages.')

if __name__ == '__main__':
    main()
