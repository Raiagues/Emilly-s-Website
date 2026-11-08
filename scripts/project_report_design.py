"""Visual case studies built around the supplied reports' original drawings."""
import html
import json
import runpy

E = html.escape


def render(b, project, lang):
    d = b['DESIGN']['Design'](b, lang, b['detail'](project))
    content = runpy.run_path(str(b['ROOT'] / 'content/project_visuals.py'))
    visual = content['VISUALS'][project['id']]
    report = b['REPORTS'][project['id']]
    t = lambda key: E(content['TEXT'][key][lang])
    local = lambda value: E(value[lang])
    assets = {a['file']: a for a in json.loads((b['ROOT'] / 'content/project-reports/assets.json').read_text())}
    sections = [*visual['new_sections'], *[
        {**s, **visual['sections'].get(s['id'], {})} for s in report['sections']
    ]]
    figure_index = 0

    def figure(item, *, eager=False):
        nonlocal figure_index
        figure_index += 1
        asset = assets[item['file']]
        title = local(item.get('title', content['TEXT']['original']))
        caption = local(item['caption'])
        return f'''<figure class="report-figure">
<a href="{d.r(item['file'])}" data-gallery data-caption="{caption}" aria-label="{t('expand')}: {title}">
<span class="report-image"><img src="{d.r(item['file'])}" width="{asset['width']}" height="{asset['height']}" loading="{'eager' if eager else 'lazy'}" decoding="async" alt="{caption}"></span>
<span class="figure-expand" aria-hidden="true">{t('expand')} <span>↗</span></span></a>
<figcaption><span class="figure-number">FIG. {figure_index:02}</span><strong>{title}</strong><p>{caption}</p></figcaption></figure>'''

    hero = figure(visual['hero'], eager=True)
    metrics = ''.join(f'<div><dt>{local(label)}</dt><dd>{E(value)}</dd></div>' for value, label in report['metrics'])
    contents = ''.join(f'<a href="#{s["id"]}"><span>{i:02}</span>{local(s.get("nav", s["title"]))}</a>' for i, s in enumerate(sections, 1))
    contributions = ''.join(f'<li><span>{i:02}</span><p>{local(item)}</p></li>' for i, item in enumerate(project['contributions'], 1))
    back = d.button(d.t('all_projects'), d.link('projects.html'), attrs=f'data-back-results="{project["id"]}" data-directory-kind="projects"', back=True)

    def switcher(items, name):
        buttons = ''.join(f'<button type="button" id="{name}-tab-{i}" data-report-choice="{i}" aria-controls="{name}-panel-{i}">{local(item["title"])}</button>' for i, item in enumerate(items))
        panels = ''.join(f'<div id="{name}-panel-{i}" data-report-panel>{figure(item)}</div>' for i, item in enumerate(items))
        return f'<div class="report-switcher report-switcher-{name}" data-report-switcher><div class="report-choices" data-report-choices hidden aria-label="{t("choose")}">{buttons}</div><div class="report-panels">{panels}</div></div>'

    def pipeline():
        labels = [('inputs', 'a3 · a4'), ('execute', 'ADD → a6'), ('compare', 'a5 ↔ a6'), ('record', 'PASS / FAIL')]
        return '<ol class="report-pipeline">' + ''.join(f'<li><span>{i:02}</span><strong>{t(key)}</strong><code>{label}</code></li>' for i, (key, label) in enumerate(labels, 1)) + '</ol>'

    def results_table(data):
        heads = ''.join(f'<th scope="col">{local(cell)}</th>' for cell in data['headers'])
        rows = ''.join('<tr><th scope="row">'+E(row[0])+'</th>'+''.join(f'<td>{E(cell)}</td>' for cell in row[1:])+'</tr>' for row in data['rows'])
        bars = ''.join(f'<li><div><strong>{E(row[0])}</strong><span>{E(row[1])} / {E(row[3])} {t("passed")}</span></div><div class="result-track" aria-hidden="true"><span style="width:{int(row[1])/int(row[3])*100:.4f}%"></span></div></li>' for row in data['rows'])
        return f'<div class="report-results"><p class="eyebrow">{t("manual")}</p><ul class="report-result-bars">{bars}</ul><details class="report-table"><summary>{t("table")}</summary><table><caption>{local(data["caption"])}</caption><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table></details></div>'

    chapters = []
    for index, section in enumerate(sections, 1):
        sid = section['id']
        paragraphs = section['paragraphs']
        prose = ''.join(f'<p>{local(paragraph)}</p>' for paragraph in paragraphs)
        images = section.get('figures', [])
        heading = f'<header class="report-heading"><span class="chapter-number" aria-hidden="true">{index:02}</span><div><p class="eyebrow">{E(visual["code"])}</p><h2>{local(section["title"])}</h2></div></header>'
        if section.get('switcher'):
            layout = f'<div class="report-intro">{prose}</div>{switcher(images, section["switcher"])}'
        elif len(images) == 1:
            layout = f'<div class="report-split"><div class="report-prose">{prose}{pipeline() if sid == "test-automation" else ""}</div>{figure(images[0])}</div>'
        elif images:
            # Keep each original drawing next to the explanation it supports.
            layout = f'<div class="report-intro report-columns">{prose}</div><div class="report-figure-grid figures-{len(images)}">'+''.join(figure(item) for item in images)+'</div>'
        else:
            layout = f'<div class="report-intro">{prose}</div>'
        if section.get('after_figures'):
            layout += '<div class="report-figure-grid report-after-figures">'+''.join(figure(item) for item in section['after_figures'])+'</div>'
        if section.get('table'):
            layout += results_table(section['table'])
        chapters.append(f'<section class="report-section" id="{sid}">{heading}{layout}</section>')

    skills = d.keywords(project['tech'])
    peers = [p for p in b['PROJECTS'] if p['kind'] == 'projects']
    links = ''.join(d.button(d.t(label), url, i == 0, attrs='target="_blank" rel="noopener noreferrer"') for i, (label, url) in enumerate(project['links']))
    dialog = f'''<dialog class="photo-dialog" aria-label="{t('figures')}" data-photo-label="{t('figure')}" data-of-label="{t('of')}">
<div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button class="photo-close" autofocus>{t('close')} ×</button></div>
<figure><img alt="" width="1280" height="900"><figcaption id="photo-caption"></figcaption></figure>
<div class="photo-controls"><button data-photo-prev aria-label="{t('previous')}">← {t('previous')}</button><button data-photo-next aria-label="{t('next')}">{t('next')} →</button></div></dialog>'''
    return f'''<main id="main" class="wrap inner-content case-page report-page" data-case-kind="projects" data-report="{project['id']}">
<div class="inner-breadcrumb">{back}<span class="mono">{d.t(project['category'])} · {project['date']}</span></div>
<header class="case-boarding report-cover" data-case-id="{project['id']}">
<div class="report-cover-copy"><p class="eyebrow">{E(visual['code'])} · {E(project['place'])}</p><h1>{local(visual['title'])}</h1><p class="report-cover-lead">{local(visual['lead'])}</p>{skills}<a class="btn btn-solid" href="#{sections[0]['id']}">{t('read')} <span aria-hidden="true">↓</span></a></div>
<div class="report-cover-art"><span class="report-art-label mono">{t('original')} / {project['date']}</span>{hero}</div>
<dl class="report-metrics">{metrics}</dl></header>
<section class="report-context" id="contribution"><div><p class="eyebrow">{t('why')}</p><h2 class="visually-hidden">{t('why')}</h2><p class="report-why">{local(visual['why'])}</p></div><aside class="report-role"><h3>{t('work') if project['id'] == 'project_2' else t('team')}</h3><ol>{contributions}</ol></aside></section>
<nav class="report-contents" aria-label="{d.t('contents')}">{contents}</nav>
<div class="project-report">{''.join(chapters)}</div>
<section id="results" class="report-takeaway"><p class="eyebrow">{t('scope')}</p><h2>{t('result')}</h2><p>{local(project['outcome'])}</p></section>
<div class="report-colophon"><p class="report-source">{t('source')} <cite>{E(report['source'])}</cite>.</p>{f'<div class="actions">{links}</div>' if links else ''}</div>
{d.flight_path(b['INNER']['route_items'](d, peers), project['id'], 'projects')}{b['INNER']['case_pagination'](d, project, peers)}{dialog}</main>'''
