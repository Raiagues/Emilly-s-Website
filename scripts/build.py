#!/usr/bin/env python3
"""Generate a dependency-free multilingual website and a curated Pages artifact."""
from pathlib import Path
import html
import json
import os
import re
import runpy
import shutil
import sys
sys.dont_write_bytecode = True
from artwork import generate
ROOT = Path(__file__).resolve().parents[1]
D = runpy.run_path(str(ROOT/'content/data.py'))
LANGS, UI, PROJECTS, SKILLS = (D[k] for k in ['LANGS','UI','PROJECTS','SKILLS'])
SITE_URL = os.environ.get('SITE_URL','https://raiagues.github.io/Emilly-s-Website').rstrip('/')
EMAIL = D['EMAIL']
E = html.escape
ARROW = '<span aria-hidden="true">↗</span>'
ALL_PATHS = []
def loc(path,lang): return path if lang=='en' else f'{lang}/{path}'
def relative(current,target): return os.path.relpath(target,Path(current).parent).replace(os.sep,'/')
def detail(p): return f'pages/{p["kind"]}/{p["id"]}.html'
def txt(key,lang): return UI[key][lang]
def layout(path,lang,title,description,body,home=False):
    full = loc(path,lang)
    r = lambda p: relative(full,p)
    homepath = r(loc('index.html',lang))
    nav = ''.join(f'<a href="{homepath}#{id}">{txt(key,lang)}</a>' for key,id in [('projects','projects'),('experience','experience'),('about','about-me'),('recognition','recognition')])
    languages = ''.join(f'<a href="{r(loc(path,l))}" lang="{l}" hreflang="{l}" aria-label="{label}" {"aria-current=\"page\"" if l==lang else ""}>{l.upper()}</a>' for l,label in [('en','English'),('pt','Português'),('fr','Français'),('es','Español')])
    alternates = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}/{loc(path,l)}">' for l in LANGS)
    structured = {'@context':'https://schema.org','@type':'ProfilePage','name':title,'mainEntity':{'@type':'Person','name':'Emilly Raiane Rodrigues','url':SITE_URL+'/', 'image':SITE_URL+'/img/me.png','sameAs':[D['LINKEDIN'],D['GITHUB']]}} if home else {'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'inLanguage':lang}
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f4f1e9"><meta name="description" content="{E(description,quote=True)}"><meta name="author" content="Emilly Rodrigues"><meta name="color-scheme" content="light"><title>{E(title)} — Emilly Rodrigues</title><link rel="icon" href="{r('img/favicon.svg')}" type="image/svg+xml"><link rel="canonical" href="{SITE_URL}/{full}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{path}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title,quote=True)} — Emilly Rodrigues"><meta property="og:description" content="{E(description,quote=True)}"><meta property="og:url" content="{SITE_URL}/{full}"><meta property="og:image" content="{SITE_URL}/img/me.png"><meta property="og:image:alt" content="Emilly Rodrigues"><link rel="stylesheet" href="{r('style/style.css')}"><script type="application/ld+json">{json.dumps(structured,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script><script src="{r('src/script.js')}" defer></script>{f'<script src="{r("src/projects.js")}" defer></script>' if home else ''}</head>
<body id="top"><a class="skip-link" href="#main">{txt('skip',lang)}</a><header class="site-header"><div class="header-inner"><a class="wordmark" href="{homepath}" aria-label="Emilly Rodrigues"><img src="{r('img/favicon.svg')}" alt="" width="36" height="36"><span>emilly<span class="wordmark-last"> rodrigues</span><span class="wordmark-dot">.</span></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">{txt('menu',lang)} <span aria-hidden="true">☰</span></button><nav id="main-nav" aria-label="{txt('menu',lang)}">{nav}<a class="nav-contact" href="{homepath}#contact">{txt('contact',lang)} {ARROW}</a></nav><div class="languages" role="group" aria-label="{txt('language',lang)}">{languages}</div></div></header>
{body}
<footer class="site-footer container"><a class="wordmark" href="{homepath}">emilly rodrigues<span class="wordmark-dot">.</span></a><p>{txt('footer',lang)}<br><span>© <span data-year>2026</span> Emilly Rodrigues</span></p><a href="#top">{txt('top',lang)} <span aria-hidden="true">↑</span></a></footer></body></html>'''
def card(p,lang,current,number=1,filterable=False):
    r=lambda x:relative(current,x)
    title=p['title'][lang]
    search=' '.join([title,p['summary'][lang],*p['tech'],p['place'],*[SKILLS[s][lang] for s in p['skills']]])
    return f'''<article class="project-card" {f'data-project data-category="{p["category"]}" data-search="{E(search,quote=True)}"' if filterable else ''}><a class="card-image" href="{r(loc(detail(p),lang))}" tabindex="-1" aria-hidden="true"><img src="{r('img/illustrations/'+p['art']+'.svg')}" alt="" width="800" height="500" loading="lazy"><span class="image-index">{number:02d} / {p['date']}</span><span class="card-arrow" aria-hidden="true">↗</span></a><div class="card-copy"><p class="eyebrow">{txt(p['category'],lang)}</p><h3><a href="{r(loc(detail(p),lang))}">{title}</a></h3><p>{p['summary'][lang]}</p><div class="tags">{''.join(f'<span>{E(t)}</span>' for t in p['tech'][:3])}</div></div></article>'''
def home(lang):
    current=loc('index.html',lang)
    r=lambda x:relative(current,x)
    t=lambda x:txt(x,lang)
    work=[p for p in PROJECTS if p['kind']=='projects']
    jobs=[p for p in PROJECTS if p['kind']=='experience']
    featured=work[0]
    cats=['all','space','hardware','control','software','outreach']
    filters=''.join(f'<button type="button" class="filter-chip" data-filter="{c}" aria-pressed="{str(c=="all").lower()}">{t(c)}</button>' for c in cats)
    cards=''.join(card(p,lang,current,i,True) for i,p in enumerate(work,1))
    company={'cern':'CERN','visiona':'Visiona','cnes':'CNES','experience_1':'TIMA Laboratory','experience_2':'ITA','experience_3':'Dafiti Group'}
    roles={
     'cern':D['L']('Machine Learning & FPGA Research | Pesquisa em Machine Learning e FPGA | Recherche en apprentissage automatique et FPGA | Investigación en aprendizaje automático y FPGA'),
     'visiona':D['L']('Embedded Flight Software | Software de voo embarcado | Logiciel de vol embarqué | Software de vuelo embebido'),
     'cnes':D['L']('Embedded Flight Software | Software de voo embarcado | Logiciel de vol embarqué | Software de vuelo embebido'),
     'experience_1':D['L']('Fault-Tolerant Embedded Software | Software embarcado tolerante a falhas | Logiciel embarqué tolérant aux fautes | Software embebido tolerante a fallos'),
     'experience_2':D['L']('Satellite Control Research | Pesquisa em controle de satélites | Recherche en contrôle de satellites | Investigación en control de satélites'),
     'experience_3':D['L']('Machine Learning | Aprendizado de máquina | Apprentissage automatique | Aprendizaje automático')}
    experience=''.join(f'''<article class="experience-row"><span class="experience-date">{p['date']}</span><div><p class="eyebrow">{E(p['place'])}</p><h3><a href="{r(loc(detail(p),lang))}">{company[p['id']]} <span aria-hidden="true">↗</span></a></h3><p>{roles[p['id']][lang]}</p></div><p class="experience-result">{p['outcome'][lang]}</p></article>''' for p in jobs)
    evidence=''.join(f'''<a class="skill" href="{r(loc(detail(next(p for p in PROJECTS if p['id']==id)),lang))}"><span class="skill-number">0{i}</span><div><h3>{SKILLS[key][lang]} {ARROW}</h3><p>{copy[lang]}</p></div></a>''' for i,(key,id,copy) in enumerate(D['EVIDENCE'],1))
    awards=''.join(f'''<article class="award"><span class="award-year">{date}</span><div><h3>{E(name)}</h3><p>{desc[lang]}</p></div><a class="round-link" href="{url or r('CV_Emilly.pdf')}" aria-label="{E(t('source')+': '+name,quote=True)}" {'target="_blank" rel="noopener noreferrer"' if url else ''}>↗</a></article>''' for date,name,desc,url in D['AWARDS'])
    return layout('index.html',lang,t('discipline'),t('hero_body'),f'''<main id="main">
<section class="hero container" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow"><span class="tiny-star" aria-hidden="true">✳</span> {t('intro')}</p><h1 id="hero-title">{t('hero')}</h1><p class="discipline">{t('discipline')}</p><p class="hero-description">{t('hero_body')}</p><div class="hero-actions"><a class="button button-dark" href="#projects">{t('explore')} <span aria-hidden="true">↓</span></a><a class="text-link" href="{r('CV_Emilly.pdf')}" download>{t('cv')} <span aria-hidden="true">↗</span></a></div></div><div class="hero-visual"><div class="orbit-art" aria-hidden="true"><div class="planet"></div><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><span class="orbital-point point-one"></span><span class="orbital-point point-two"></span><span class="hero-star">✳</span><span class="coordinates">BR → FR → CH</span></div><img class="portrait" src="{r('img/me.png')}" alt="{t('portrait')}" width="484" height="718" fetchpriority="high"><div class="portrait-note"><span aria-hidden="true">↗</span><p>{t('orbit_note')}</p></div><span class="visual-caption">AEROSPACE / EMBEDDED / HUMAN</span></div></section>
<div class="journey-strip container"><p class="eyebrow">{t('journey')}</p><div class="organizations"><span>CERN<span class="org-dot">·</span></span><span>CNES<span class="org-dot">·</span></span><span>Visiona<span class="org-dot">·</span></span><span>Grenoble INP<span class="org-dot">·</span></span><span>UFSM</span></div></div>
<section id="projects" class="section container"><div class="section-heading"><div><p class="eyebrow">{t('work_eyebrow')}</p><h2>{t('work_title')}</h2></div><p>{t('work_body')}</p></div><article class="featured-project"><div class="featured-copy"><p class="eyebrow">{t('featured')} / 2025–2026</p><h3>{featured['title'][lang]}</h3><p>{featured['summary'][lang]}</p><span class="feature-note">AIAA SciTech 2027</span><a class="button button-light" href="{r(loc(detail(featured),lang))}">{t('case')} {ARROW}</a></div><a class="featured-art" href="{r(loc(detail(featured),lang))}" tabindex="-1" aria-hidden="true"><img src="{r('img/illustrations/platform.svg')}" alt="" width="800" height="500" loading="lazy"></a></article>
<div class="project-tools" hidden data-project-tools><label class="search-label"><span class="sr-only">{t('search')}</span><span aria-hidden="true">⌕</span><input id="project-search" type="search" placeholder="{t('search')}" maxlength="120" autocomplete="off"></label><div class="filters" role="group" aria-label="{t('projects')}">{filters}</div><p class="results-count" id="results-count" aria-live="polite" data-label="{t('results')}"></p></div><div id="project-grid" class="project-grid">{cards}</div><div id="empty-state" class="empty-state" hidden><p>{t('empty')}</p><button class="button button-dark" id="reset-filters" type="button">{t('reset')}</button></div><div class="more-wrap"><button class="button button-soft" id="show-more" type="button" data-more="{t('more')}" data-less="{t('less')}" aria-expanded="false" aria-controls="project-grid" hidden>{t('more')} <span aria-hidden="true">↓</span></button></div></section>
<section id="experience" class="experience-section"><div class="container section"><div class="section-heading"><div><p class="eyebrow">{t('exp_eyebrow')}</p><h2>{t('exp_title')}</h2></div><p>{t('exp_body')}</p></div><div class="experience-list">{experience}</div></div></section>
<section id="about-me" class="section container"><p class="eyebrow">{t('about_eyebrow')}</p><div class="about-grid"><div class="about-heading"><h2>{t('about_title')}</h2><div class="story-illustration"><img src="{r('img/illustrations/rocket.svg')}" alt="" width="800" height="500" loading="lazy"><span class="handwritten">per aspera ad astra</span></div></div><div class="about-copy"><p>{t('about_p1')}</p><p>{t('about_p2')}</p><div class="education"><h3>{t('education')}</h3><p><strong>{t('degree1')}</strong><span>{t('degree1_date')}</span></p><p><strong>{t('degree2')}</strong><span>{t('degree2_date')}</span></p></div><p class="language-levels">{t('languages')}</p></div></div><div class="skills-heading"><h2>{t('skills_title')}</h2><p>{t('skills_body')}</p></div><div class="skills-grid">{evidence}</div></section>
<section id="recognition" class="recognition-section"><div class="container section recognition-grid"><div class="recognition-intro"><p class="eyebrow">{t('awards_eyebrow')}</p><h2>{t('awards_title')}</h2><span class="award-star" aria-hidden="true">✳</span><article class="press-card"><p class="eyebrow">{t('press')} / EXAME</p><h3>{t('press_title')}</h3><p>{t('press_body')}</p><a class="text-link" href="{D['EXAME']}" target="_blank" rel="noopener noreferrer">{t('article')} {ARROW}</a></article></div><div class="awards-list">{awards}</div></div></section>
<section id="contact" class="section container contact-grid"><div><p class="eyebrow">{t('contact_eyebrow')}</p><h2>{t('contact_title')}</h2><p class="contact-description">{t('contact_body')}</p><div class="contact-links"><a href="{D['LINKEDIN']}" target="_blank" rel="noopener noreferrer">LinkedIn {ARROW}</a><a href="{D['GITHUB']}" target="_blank" rel="noopener noreferrer">GitHub {ARROW}</a><a href="{r('CV_Emilly.pdf')}" download>{t('cv')} {ARROW}</a></div><div class="direct-email"><p>{t('direct')}</p><a href="mailto:{EMAIL}">{EMAIL}</a><button type="button" id="copy-email" data-email="{EMAIL}" data-success="{t('copied')}" data-error="{t('copy_error')}" hidden>{t('copy')} <span aria-hidden="true">⧉</span></button><p id="copy-status" role="status"></p></div></div><form class="contact-form" action="https://formsubmit.co/{EMAIL}" method="POST"><div class="form-row"><label>{t('name')}<input type="text" name="name" autocomplete="name" required maxlength="100"></label><label>{t('email')}<input type="email" name="email" autocomplete="email" required maxlength="254"></label></div><label>{t('subject')}<input type="text" name="subject" required maxlength="160"></label><label>{t('message')}<textarea name="message" rows="5" required maxlength="5000"></textarea></label><input type="hidden" name="_subject" value="Portfolio · Emilly Rodrigues"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" tabindex="-1" autocomplete="off" class="honeypot" aria-hidden="true"><button class="button button-dark" type="submit">{t('send')} {ARROW}</button><p class="form-note">{t('form_note')} <a href="https://formsubmit.co/privacy.pdf" target="_blank" rel="noopener noreferrer">FormSubmit ↗</a></p></form></section></main>''',True)
def project(p,lang):
    path=detail(p); current=loc(path,lang)
    r=lambda x:relative(current,x)
    t=lambda x:txt(x,lang)
    related=sorted([q for q in PROJECTS if q['id']!=p['id']],key=lambda q:(q['category']!=p['category'], q['kind']!=p['kind']))[:3]
    links=''.join(f'<a class="button button-soft" href="{url}" target="_blank" rel="noopener noreferrer">{t(label)} {ARROW}</a>' for label,url in p['links'])
    main=f'''<main id="main" class="detail-main"><div class="container"><nav class="breadcrumb" aria-label="{t('projects')}"><a href="{r(loc('index.html',lang))}#{p['kind']}"><span aria-hidden="true">←</span> {t('experience') if p['kind']=='experience' else t('back')}</a><span>/</span><span>{t(p['category'])}</span></nav><section class="detail-heading"><p class="eyebrow">{E(p['place'])} / {p['date']}</p><h1>{p['title'][lang]}</h1><p class="detail-intro">{p['summary'][lang]}</p></section><figure class="detail-image"><img src="{r('img/illustrations/'+p['art']+'.svg')}" alt="{E(p['title'][lang],quote=True)}" width="800" height="500" fetchpriority="high"><figcaption>{t('illustration')}</figcaption></figure><div class="detail-layout"><aside class="project-facts"><dl><dt>{t('context')}</dt><dd>{E(p['place'])}</dd><dt>{t('period')}</dt><dd>{p['date']}</dd><dt>{t('toolkit')}</dt><dd class="tags">{''.join(f'<span>{E(x)}</span>' for x in p['tech'])}</dd></dl><a class="text-link" href="{r(loc('index.html',lang))}#contact">{t('contact')} {ARROW}</a></aside><div class="detail-story"><section><p class="eyebrow">01 / {t('overview')}</p><h2>{t('contributions')}</h2><ul class="contributions">{''.join(f'<li>{item[lang]}</li>' for item in p['contributions'])}</ul></section><section class="result-panel"><p class="eyebrow">02 / {t('outcome')}</p><p>{p['outcome'][lang]}</p></section><section><p class="eyebrow">03 / {t('practice')}</p><div class="skill-tags">{''.join(f'<span>{SKILLS[s][lang]}</span>' for s in p['skills'])}</div></section>{f'<section><h2>{t("links")}</h2><div class="detail-links">{links}</div></section>' if links else ''}</div></div><section class="related section"><div class="section-heading"><h2>{t('related')}</h2><a class="text-link" href="{r(loc('index.html',lang))}#projects">{t('back')} {ARROW}</a></div><div class="project-grid">{''.join(card(q,lang,current,i) for i,q in enumerate(related,1))}</div></section></div></main>'''
    return layout(path,lang,p['title'][lang],p['summary'][lang],main)
def write(path,content):
    target=ROOT/path; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content,encoding='utf-8'); ALL_PATHS.append(path)
def main():
    generate(ROOT)
    for lang in LANGS:
        write(loc('index.html',lang),home(lang))
        for p in PROJECTS: write(loc(detail(p),lang),project(p,lang))
    for old in ['pages/projects/projects_exemple.html','pages/experience/experience_exemple.html']:
        write(old,'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=../../index.html#projects"><title>Projects — Emilly Rodrigues</title><a href="../../index.html#projects">Explore projects</a></html>')
    base=SITE_URL+'/'
    write('404.html',f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found — Emilly Rodrigues</title><link rel="stylesheet" href="{base}style/style.css"><main class="container section"><p class="eyebrow">404 / EMILLY RODRIGUES</p><h1>{txt("notfound","en")}</h1><p><a class="button button-dark" href="{base}">{txt("home","en")} ↗</a></p></main></html>')
    write('.nojekyll','')
    write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{SITE_URL}/{p}</loc></url>' for p in ALL_PATHS if p.endswith('.html') and 'exemple' not in p and p!='404.html')+'</urlset>')
    # Only publish web assets, not tooling, source archives, caches or Git metadata.
    dist=ROOT/'dist'; dist.mkdir(exist_ok=True)
    for path in ALL_PATHS:
        dest=dist/path; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(ROOT/path,dest)
    for folder in ['style','src','img','doc']:
        shutil.copytree(ROOT/folder,dist/folder,dirs_exist_ok=True)
    for name in ['CV_Emilly.pdf','Emilly_Rodrigues_Resume.pdf']: shutil.copyfile(ROOT/name,dist/name)
    print(f'Built {len(PROJECTS)} case studies × {len(LANGS)} languages, homepages, sitemap and GitHub Pages artifact in dist/.')
if __name__=='__main__': main()
