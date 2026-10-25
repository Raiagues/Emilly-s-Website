"""Real case studies and stories in the supplied project/experience/story layouts."""
import html
import re
import runpy
from pathlib import Path

C=runpy.run_path(str(Path(__file__).with_name('redesign_components.py')))
Design, chronological, E, ARROW, STAR=(C[k] for k in ('Design','chronological','E','ARROW','STAR'))


def route_items(d, peers):
    return [dict(id=q['id'],date=q['date'],year=q['date'],meta=q['place']+' · '+q['date'],title=q['title'][d.lang],summary=q['summary'][d.lang],url=d.link(d.b['detail'](q)),art=d.art(q['art'],item_id=q['id'])) for q in chronological(peers)]


def photo_frame(d, photo, eager=False):
    ratio=photo['width']/photo['height']
    return f'<figure class="polaroid" style="--photo-ratio:{ratio:.6f}">{d.b["J"]["photo_html"](photo,d.lang,d.current,eager)}<figcaption>{d.local(photo["caption"])}</figcaption></figure>'


def case(b, p, lang):
    d=Design(b,lang,b['detail'](p))
    peers=[q for q in b['PROJECTS'] if q['kind']==p['kind']]
    back=d.button(d.t('all_projects') if p['kind']=='projects' else d.t('all_experience'), d.link(p['kind']+'.html'), attrs=f'data-back-results="{p["id"]}" data-directory-kind="{p["kind"]}"', back=True)
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
{d.flight_path(route_items(d,peers),p['id'],p['kind'])}{case_pagination(d,p,peers)}</main>'''
    return body


def case_pagination(d, p, peers):
    ordered = chronological(peers)
    index = ordered.index(p)
    links = []
    for offset, direction in [(-1,'previous'),(1,'next')]:
        if not 0 <= index + offset < len(ordered):
            continue
        target = ordered[index+offset]
        label = d.t(direction) if p['kind']=='projects' else d.u(direction+'_experience')
        arrow = C['BACK_ARROW'] if offset < 0 else ARROW
        links.append(f'<a class="case-neighbour neighbour-{direction}" rel="{"prev" if offset < 0 else "next"}" href="{d.link(d.b["detail"](target))}">{arrow}<span><small>{label}</small><strong>{E(target["title"][d.lang])}</strong></span></a>')
    return f'<nav class="case-pagination" aria-label="{d.u("continue")}">{"".join(links)}</nav>'


def directory(b,lang,kind):
    d=Design(b,lang,kind+'.html')
    work=list(reversed(chronological([p for p in b['PROJECTS'] if p['kind']==kind])))
    categories=['all']+[key for key in ['space','hardware','control','software','outreach'] if any(p['category']==key for p in work)]
    filters=''.join(f'<button type="button" class="chip" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{d.t(key)} <span>{sum(key=="all" or p["category"]==key for p in work)}</span></button>' for key in categories)
    cards=[]
    for p in work:
        search=' '.join([p['title'][lang],p['summary'][lang],p['place'],*p['tech'],*[b['SKILLS'][key][lang] for key in p['skills']]])
        cards.append(f'<article class="catalogue-item" id="{p["id"]}" data-project data-category="{p["category"]}" data-search="{E(search,quote=True)}"><a class="project-card" href="{d.link(b["detail"](p))}" data-result-link aria-labelledby="title-{p["id"]}"><div class="art">{d.art(p["art"],item_id=p["id"])}<span class="art-date">{p["date"]}</span></div><p class="eyebrow">{d.t(p["category"]) if kind=="projects" else E(p["place"])}</p><h2 id="title-{p["id"]}">{p["title"][lang]}</h2><p>{p["summary"][lang]}</p>{d.keywords(p["tech"][:4])}</a></article>')
    search_label=d.t('search') if kind=='projects' else d.u('search_experience')
    result_label=d.t('results') if kind=='projects' else d.u('experience_results')
    description=d.t('work_body' if kind=='projects' else 'exp_body')
    title=d.t('projects') if kind=='projects' else d.u('experiences')
    prefix=d.u('all_projects_prefix' if kind=='projects' else 'all_experience_prefix')
    empty=d.t('empty') if kind=='projects' else d.u('no_experience')
    return f'''<main id="main" class="wrap inner-content project-directory" data-directory-kind="{kind}"><div class="inner-breadcrumb">{d.button(d.u('home'),d.link('index.html#'+('current-work' if kind=='projects' else 'experience')),back=True)}<span class="mono">{d.t(kind)}</span></div><header class="catalogue-heading poster-heading"><div><p class="eyebrow">{d.u('logbook')}</p><h1><span>{prefix}</span><strong>{title}</strong></h1><p>{description}</p></div><div class="catalogue-route" aria-hidden="true">{d.drawing('catalogue-route')}<div><span>{E(work[-1]['date'])}</span><span>{E(work[0]['date'])}</span></div></div></header><div class="project-tools" data-project-tools hidden><div class="filters" role="group" aria-label="{d.t('filter_label')}">{filters}</div><div class="catalogue-utility"><label class="search-label" for="project-search"><span class="visually-hidden">{search_label}</span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg><input id="project-search" type="search" placeholder="{d.t('search_short')}" autocomplete="off" maxlength="120"></label><div class="filter-status"><p id="results-count" aria-live="polite" data-label="{result_label}"></p><button class="chip" id="reset-filters" type="button">{d.t('reset')}</button></div></div></div><div id="project-grid" class="catalogue-grid">{''.join(cards)}</div><div id="empty-state" hidden><h2>{empty}</h2></div></main>'''


def projects(b,lang):
    return directory(b,lang,'projects')


def experience(b,lang):
    return directory(b,lang,'experience')


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
    archive = runpy.run_path(str(Path(__file__).with_name('journal_archive.py')))
    place = archive['place_for'](post,lang) or archive['date_of'](post)[:4]
    trip=f'<div class="story-ticket"><div><span class="mono">{d.u("story")}</span><strong>{E(place)}</strong><span class="mono">{d.local(post["period"])}</span></div><span>{d.drawing("guide-experience")}</span></div>'
    dialog=f'<dialog class="photo-dialog" aria-label="{jt("photo")}" data-photo-label="{jt("photo")}" data-of-label="{jt("of")}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button type="button" class="photo-close" autofocus>{jt("close")} ×</button></div><figure><img alt="" width="1280" height="1280"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button type="button" data-photo-prev aria-label="{jt("previous_photo")}">{b["icon"]("previous")}</button><button type="button" data-photo-next aria-label="{jt("next_photo")}">{b["icon"]("next")}</button></div></dialog>'
    return f'''<main id="main" class="wrap inner-content story-page"><div class="inner-breadcrumb">{d.button(jt('back'),d.link('journal.html'),back=True)}</div><article><header class="story-opening"><div class="story-opening-copy"><p class="eyebrow">{d.local(post.get('series',''))} · {d.local(post['period'])}</p><h1>{d.local(post['title'])}</h1><p class="story-subtitle">{d.local(post['subtitle'])}</p></div><div class="story-opening-photos">{''.join(covers)}{trip}</div></header><details class="story-contents"><summary>{jt('chapters')}</summary><nav aria-label="{jt('chapters')}">{parts['contents']}</nav></details><div class="journal-body"><div class="journal-prose journal-intro"><p>{d.local(post['intro'])}</p>{parts['technical']}</div>{parts['chapters']}{f'<div class="case-photo-slots">{extra}</div>' if extra else ''}<section class="lesson-envelope journal-closing"><div><div><h2 class="eyebrow">Par avion · {d.u('learned')}</h2><p>{d.local(post['closing'])}</p></div></div></section></div></article>{archive['explorer'](b,d,post['slug'])}{dialog}</main>'''
