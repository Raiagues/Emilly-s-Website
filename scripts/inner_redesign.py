"""Real case studies and stories in the supplied project/experience/story layouts."""
import html
import re
import runpy
from pathlib import Path

C=runpy.run_path(str(Path(__file__).with_name('redesign_components.py')))
Design, chronological, E, ARROW, STAR=(C[k] for k in ('Design','chronological','E','ARROW','STAR'))


def route_items(d, peers):
    return [dict(id=q['id'],date=q['date'],year=q['date'],meta=q['place']+' · '+q['date'],title=q['title'][d.lang],summary=q['summary'][d.lang],url=d.link(d.b['detail'](q))) for q in chronological(peers)]


def photo_frame(d, photo, eager=False):
    ratio=photo['width']/photo['height']
    return f'<figure class="polaroid" style="--photo-ratio:{ratio:.6f}">{d.b["J"]["photo_html"](photo,d.lang,d.current,eager)}<figcaption>{d.local(photo["caption"])}</figcaption></figure>'


def case(b, p, lang):
    d=Design(b,lang,b['detail'](p))
    peers=[q for q in b['PROJECTS'] if q['kind']==p['kind']]
    back=d.button(d.t('back_results') if p['kind']=='projects' else d.t('experience'), d.link(p['kind']+'.html'), attrs=f'data-back-results="{p["id"]}"' if p['kind']=='projects' else '')
    links=''.join(d.button(d.t(label),url,i==0,attrs='target="_blank" rel="noopener noreferrer"') for i,(label,url) in enumerate(p['links']))
    related=next((post for post in b['POSTS'] if post.get('technical_path')==b['detail'](p)),None)
    journal_link=''
    photos=''
    if related:
        label=related.get('journal_link_label',b['JUI']['cern_link'] if p['id']=='cern' else related['title'])
        journal_link=f'<aside class="journal-callout">{d.button(d.local(label),d.link(b["J"]["path"](related)))}</aside>'
        for key in dict.fromkeys(related['cover']):
            photo=related['photos'][key]
            photos+=photo_frame(d,photo)
    if p['id'] in b['MEDIA']:
        photos+=f'<figure class="polaroid"><img src="{d.r(b["MEDIA"][p["id"]])}" alt="{E(p["title"][lang],quote=True)}" loading="lazy"><figcaption>{d.t("video_caption")}</figcaption></figure>'
    if p['kind']=='experience':
        contributions='<ol class="mission-tasks">'+''.join(f'<li><span aria-hidden="true">{chr(65+i)}</span><p>{item[lang]}</p></li>' for i,item in enumerate(p['contributions']))+'</ol>'
    else:
        contributions='<div class="mission-sequence"><svg class="sequence-route" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M0 70Q25 0 50 50T100 50"/></svg>'+''.join(f'<div class="mission-stage"><span class="stage-icon" aria-hidden="true">{d.drawing(["guide-projects","guide-about","guide-experience"][i%3])}</span><span class="mono">{i+1:02}</span><p>{item[lang]}</p></div>' for i,item in enumerate(p['contributions']))+'</div>'
    postcard=f'<aside class="city-postcard"><div>{d.drawing("experience-city")}<span class="mono">{E(p["place"])}</span></div></aside>' if p['id']=='cern' else ''
    section_title=f'<div class="case-section-heading"><span class="eyebrow">01 /</span><h2>{d.t("contributions")}</h2></div>'
    skills=d.keywords([b['SKILLS'][key][lang] for key in p['skills']])
    body=f'''<main id="main" class="wrap inner-content case-page" data-case-kind="{p['kind']}"><div class="inner-breadcrumb">{back}<span class="mono">{d.t(p['kind'])} · {d.t(p['category'])} · {p['date']}</span></div>{d.boarding(p)}
<div class="case-content {"has-city" if postcard else ""}"><div><section id="contribution">{section_title}{contributions}</section><section id="skills" class="case-skills"><h2>{d.t('practice')}</h2>{skills}</section></div>{postcard}</div>
{f'<section class="case-photo-slots" aria-label="{d.local(b["JUI"]["photo"])}">{photos}</section>' if photos else ''}
<section id="results" class="lesson-envelope"><div><div><p class="eyebrow">02 · {d.t('outcome')}</p><h2 class="visually-hidden">{d.t('outcome')}</h2><p>{p['outcome'][lang]}</p></div></div></section>{journal_link}
{f'<section id="resources" class="case-resources"><h2>{d.t("links")}</h2><div class="actions">{links}</div></section>' if links else ''}
{d.flight_path(route_items(d,peers),p['id'],p['kind'])}<div class="detail-bottom">{back}{d.button(d.t('contact'),d.link('contact.html'))}</div></main>'''
    return body


def projects(b,lang):
    d=Design(b,lang,'projects.html')
    work=list(reversed(chronological([p for p in b['PROJECTS'] if p['kind']=='projects'])))
    categories=['all','space','hardware','control','software','outreach']
    filters=''.join(f'<button type="button" class="chip" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{d.t(key)} <span>{sum(key=="all" or p["category"]==key for p in work)}</span></button>' for key in categories)
    cards=[]
    for p in work:
        search=' '.join([p['title'][lang],p['summary'][lang],p['place'],*p['tech'],*[b['SKILLS'][key][lang] for key in p['skills']]])
        cards.append(f'<article class="catalogue-item" id="{p["id"]}" data-project data-category="{p["category"]}" data-search="{E(search,quote=True)}"><a class="project-card" href="{d.link(b["detail"](p))}" data-result-link><div class="art">{d.art(p["art"],item_id=p["id"])}<span class="art-date">{p["date"]}</span></div><p class="eyebrow">{d.t(p["category"])}</p><h2>{p["title"][lang]}</h2><p>{p["summary"][lang]}</p>{d.keywords(p["tech"])}<span class="more">{d.t("case")}{ARROW}</span></a></article>')
    return f'''<main id="main" class="wrap inner-content project-directory"><div class="inner-breadcrumb">{d.button(d.u('home'),d.link('index.html'))}<span class="mono">{d.u('logbook')}</span></div><header class="catalogue-heading"><div><p class="eyebrow">{d.u('logbook')}</p><h1>{d.t('all_projects')}</h1><p>{d.t('work_body')}</p></div><div class="catalogue-drawing" aria-hidden="true">{d.drawing('project-pass')}</div></header><div class="project-tools" data-project-tools hidden><div class="filters" role="group" aria-label="{d.t('filter_label')}">{filters}</div><label class="search-label" for="project-search">{d.t('search')}<input id="project-search" type="search" placeholder="{d.t('search_short')}" autocomplete="off" maxlength="120"></label><div class="filter-status"><p id="results-count" aria-live="polite" data-label="{d.t('results')}"></p><button class="chip" id="reset-filters" type="button">{d.t('reset')}</button></div></div><div id="project-grid" class="catalogue-grid">{''.join(cards)}</div><div id="empty-state" hidden><h2>{d.t('empty')}</h2></div></main>'''


def experience(b,lang):
    d=Design(b,lang,'experience.html')
    items=list(reversed(chronological([p for p in b['PROJECTS'] if p['kind']=='experience'])))
    passes=[]
    for p in items:
        passes.append(f'<a class="boarding-pass" href="{d.link(b["detail"](p))}"><div class="art" aria-hidden="true">{d.art(p["art"],item_id=p["id"])}</div><div class="pass-copy"><p class="eyebrow">{E(p["place"])}</p><h2>{p["title"][lang]}</h2><p>{p["outcome"][lang]}</p>{d.keywords(p["tech"])}</div><div class="pass-stub"><div><span class="mono">{d.u("departure")}</span><strong>{p["date"]}</strong></div><span class="more">{d.t("read")}{ARROW}</span></div></a>')
    return f'<main id="main" class="wrap inner-content"><div class="inner-breadcrumb">{d.button(d.u("home"),d.link("index.html"))}</div><header class="catalogue-heading"><div><p class="eyebrow">{d.u("pass")}</p><h1>{d.t("experience")}</h1><p>{d.t("exp_body")}</p></div></header><div class="boarding-passes">{"".join(passes)}</div></main>'


def story(b,post,lang):
    d=Design(b,lang,b['J']['path'](post))
    jt=lambda key:d.local(b['JUI'][key])
    parts=b['J']['story'](post,lang,d.current,d.link,b['JUI'],b['POSTS'],b['ENTITIES'],parts_only=True)
    covers=[]
    for key in [post['cover'][-1],post['cover'][0]]:
        photo=post['photos'][key]
        covers.append(photo_frame(d,photo,True))
    used={k for section in post['sections'] for k in section.get('photos',[])+section.get('documents',[])} | {post['cover'][0],post['cover'][-1]}
    extra=''.join(photo_frame(d,post['photos'][key]) for key in post['cover'] if key not in used)
    trip=f'<div class="story-ticket"><div><span class="mono">{d.u("story")}</span><strong>{d.local(post["period"])}</strong></div><span>{d.drawing("guide-experience")}</span></div>'
    by_time=sorted(b['POSTS'],key=lambda q:max((e['date'] for e in q.get('timeline',[])),default=q['date']))
    items=[]
    for q in by_time:
        date=max((e['date'] for e in q.get('timeline',[])),default=q['date'])
        items.append(dict(id=q['slug'],date=date,year=date[:4],meta=b['J']['text'](q['period'],lang),title=b['J']['text'](q['title'],lang),summary=b['J']['text'](q['intro'],lang),url=d.link(b['J']['path'](q))))
    dialog=f'<dialog class="photo-dialog" aria-label="{jt("photo")}" data-photo-label="{jt("photo")}" data-of-label="{jt("of")}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{jt("close")} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{jt("previous_photo")}">{b["icon"]("previous")}</button><button type="button" data-photo-next aria-label="{jt("next_photo")}">{b["icon"]("next")}</button></div></dialog>'
    return f'''<main id="main" class="wrap inner-content story-page"><div class="inner-breadcrumb">{d.button(jt('back'),d.link('index.html')+'#journal')}</div><article><header class="story-opening"><div class="story-opening-copy"><p class="eyebrow">{d.local(post.get('series',''))} · {d.local(post['period'])}</p><h1>{d.local(post['title'])}</h1><p class="story-subtitle">{d.local(post['subtitle'])}</p><p class="mono">{jt('photos_credit')}</p></div><div class="story-opening-photos">{''.join(covers)}{trip}</div></header><details class="story-contents"><summary>{jt('chapters')}</summary><nav aria-label="{jt('chapters')}">{parts['contents']}</nav></details><div class="journal-body"><div class="journal-prose journal-intro"><p>{d.local(post['intro'])}</p>{parts['technical']}</div>{parts['chapters']}{f'<div class="case-photo-slots">{extra}</div>' if extra else ''}<section class="lesson-envelope journal-closing"><div><div><h2 class="eyebrow">Par avion · {d.u('learned')}</h2><p>{d.local(post['closing'])}</p></div></div></section></div></article>{d.flight_path(items,post['slug'],'stories')}{dialog}</main>'''
