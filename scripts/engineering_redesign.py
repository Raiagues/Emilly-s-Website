"""Interactive engineering case studies, using supplied documents and real captures."""
import html
import json
import runpy
from pathlib import Path

E = html.escape


class Case:
    def __init__(self, b, project, lang):
        self.b, self.project, self.lang = b, project, lang
        self.d = b['DESIGN']['Design'](b, lang, b['detail'](project))
        self.copy = runpy.run_path(str(b['ROOT'] / 'content/engineering_cases.py'))
        self.flight = project['id'] == 'flight-platform'
        self.strings = {**self.copy['COMMON'], **self.copy['FLIGHT' if self.flight else 'KERNEL']}
        self.drawings = runpy.run_path(str(b['ROOT'] / 'scripts/engineering_drawings.py'))
        self.figure_no = 0
        self.config = {}

    def text(self, key):
        return E(self.strings[key][self.lang])

    def local(self, value):
        return E(value[self.lang] if isinstance(value, dict) else value)

    def paragraph(self, key):
        return f'<p>{self.text(key)}</p>'

    def heading(self, index, title):
        return f'<header class="eng-heading"><span class="eng-number" aria-hidden="true">{index:02}</span><div><p class="eyebrow">{self.text("inside")}</p><h2>{self.text(title)}</h2></div></header>'

    def chapter(self, index, sid, title, body, intro=None):
        return f'<section class="eng-chapter" id="{sid}">{self.heading(index,title)}{f"<div class=eng-intro>{self.paragraph(intro)}</div>" if intro else ""}{body}</section>'

    def figure(self, path, title, caption, width=1280, height=720, eager=False):
        self.figure_no += 1
        return f'''<figure class="eng-figure"><a href="{self.d.r(path)}" data-gallery data-caption="{caption}" aria-label="{self.text('expand')}: {title}"><img src="{self.d.r(path)}" width="{width}" height="{height}" alt="{caption}" loading="{'eager' if eager else 'lazy'}" decoding="async"><span class="eng-expand">{self.text('expand')} ↗</span></a><figcaption><span>FIG. {self.figure_no:02}</span><div><strong>{title}</strong><p>{caption}</p></div></figcaption></figure>'''

    def select(self, sid, items, css=''):
        """All views remain in the document without scripting."""
        controls = ''.join(f'<button type="button" data-view-choice="{i}" id="{sid}-choice-{i}" aria-controls="{sid}-view-{i}">{label}</button>' for i,(label,_) in enumerate(items))
        views = ''.join(f'<div data-view="{i}" id="{sid}-view-{i}"><h3 class="eng-view-title">{label}</h3>{body}</div>' for i,(label,body) in enumerate(items))
        return f'<div class="eng-select {css}" data-select-group="{sid}"><div class="eng-choices" data-choices hidden aria-label="{self.text("select")}">{controls}</div><div class="eng-views">{views}</div></div>'

    def source_link(self, url, label=None):
        return f'<a class="eng-source-link" href="{E(url,quote=True)}" target="_blank" rel="noopener noreferrer">{label or self.text("view_code")} ↗</a>'

    def shell(self, chapters, navigation, hero, summary, metrics, footer):
        p,d=self.project,self.d
        back=d.button(d.t('all_projects'),d.link('projects.html'),attrs=f'data-back-results="{p["id"]}" data-directory-kind="projects"',back=True)
        toc=''.join(f'<a href="#{sid}"><span>{i:02}</span>{label}</a>' for i,(sid,label) in enumerate(navigation,1))
        metric_html=''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for value,label in metrics)
        peers=[q for q in self.b['PROJECTS'] if q['kind']=='projects']
        config=json.dumps(self.config,ensure_ascii=False).replace('<','\\u003c')
        return f'''<main id="main" class="wrap inner-content engineering-case {'flight-case' if self.flight else 'kernel-case'}" data-case-kind="projects">
<div class="inner-breadcrumb">{back}<span class="mono">{self.text('eyebrow')}</span></div>
<header class="eng-opening"><div class="eng-opening-copy"><p class="eyebrow">{E(p['place'])} · {p['date']}</p><h1>{self.text('title')}</h1><p class="eng-deck">{self.text('lead')}</p><p class="eng-lead">{self.text('intro')}</p>{d.keywords(p['tech'][:7])}<a class="btn btn-solid" href="#{navigation[0][0]}">{self.text('explore')} <span class="arr" aria-hidden="true">↓</span></a></div><figure class="eng-hero-drawing">{hero}<figcaption>{self.text('concept')}</figcaption></figure></header>
<aside class="case-boarding eng-pass"><div class="eng-pass-stamp" aria-hidden="true"><span>{'cFS' if self.flight else 'RV64'}</span><svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="25"/><path d="M5 32h54M32 7c-15 15-15 35 0 50M32 7c15 15 15 35 0 50M12 17h40M12 47h40"/></svg></div><div class="eng-pass-copy"><p class="eyebrow">{self.text('status')}</p><p>{summary}</p></div><div class="eng-pass-stub"><span class="mono">{p['date']}</span><strong>{'UFSM' if self.flight else 'PHELMA'}</strong><span class="eng-barcode" aria-hidden="true"></span></div></aside>
<dl class="eng-metrics">{metric_html}</dl><div class="eng-context"><p class="eyebrow">{self.text('context')}</p>{self.paragraph('why')}</div>
<nav class="eng-toc" aria-label="{self.text('read')}">{toc}</nav>
{chapters}
<section id="results" class="eng-result"><p class="eyebrow">{self.text('result')}</p><h2>{self.text('title')}</h2>{self.paragraph('outcome')}</section>
<section class="eng-sources" id="sources"><h2>{self.text('references')}</h2>{footer}</section>
{d.flight_path(self.b['INNER']['route_items'](d,peers),p['id'],'projects')}{self.b['INNER']['case_pagination'](d,p,peers)}
<script type="application/json" id="engineering-data">{config}</script>{self.dialog()}</main>'''

    def dialog(self):
        t=self.text
        return f'<dialog class="photo-dialog" aria-label="{t("figure")}" data-photo-label="{t("figure")}" data-of-label="{t("of")}"><div class="photo-dialog-bar"><p id="photo-counter" role="status"></p><button class="photo-close" autofocus>{t("close")} ×</button></div><figure><img alt="" width="1280" height="720"><figcaption id="photo-caption"></figcaption></figure><div class="photo-controls"><button data-photo-prev aria-label="{t("previous")}">← {t("previous")}</button><button data-photo-next aria-label="{t("next")}">{t("next")} →</button></div></dialog>'

    def flight_page(self):
        t=self.text
        repo='https://github.com/Raiagues/cfs_emulator'
        hero=self.drawings['flight_hero']({k:self.strings[k][self.lang] for k in ['web','backend','flight']} | {'commands':{'en':'COMMAND','pt':'COMANDO','fr':'COMMANDE','es':'COMANDO'}[self.lang], 'telemetry':{'en':'TELEMETRY','pt':'TELEMETRIA','fr':'TÉLÉMESURE','es':'TELEMETRÍA'}[self.lang]})
        runtime=self.flight_screens()
        first=1 if runtime else 0
        views=[]
        for code,label,detail,tech in [('web','web','web_detail','BROWSER / HTTP'),('backend','backend','backend_detail','PYTHON / API'),('flight','flight','flight_detail','cFS / UDP')]:
            views.append((t(label),f'<div class="eng-component-detail" data-arch-detail="{code}"><span class="eng-component-symbol" aria-hidden="true">{self.component_icon(code)}</span><div><p class="eyebrow">{tech}</p>{self.paragraph(detail)}</div></div>'))
        architecture=f'<div class="eng-architecture-route" aria-hidden="true"><span>WEB</span><i>HTTP / REST ⇄</i><span>PYTHON</span><i>UDP ⇄</i><span>cFS</span></div>'+self.select('architecture',views,'eng-component-selector')
        original=self.figure('img/flight-studio/platform-architecture-original.png',t('original'),t('architecture'),1510,260)
        architecture+=f'<details class="eng-original"><summary>{t("original")} · TCC</summary>{original}</details>'
        chapters=self.chapter(1,'flight-screens','screens',runtime,'screens_body') if runtime else ''
        chapters+=self.chapter(1+first,'architecture','architecture',architecture,'architecture_body')
        # An annotated cFS stack follows the documented application/service/port layers.
        stack=''.join(f'<div class="eng-layer eng-layer-{i}" data-stack-layer="{i}"><span>{label}</span><small>{sub}</small></div>' for i,(label,sub) in enumerate([('APPS','CI_LAB · TO_LAB · SCH_LAB'),('cFE','ES · SB · EVS · TBL · TIME'),('OSAL','API'),('PSP','LINUX / PLATFORM')]))
        layers=self.select('layers',[(t(key),self.paragraph(key+'_detail')) for key in ['apps','cfe','osal','psp']],'eng-layer-selector')
        layers=f'<div class="eng-layer-lab"><div class="eng-layer-stack" aria-hidden="true">{stack}<span class="eng-stack-base">HARDWARE / LINUX</span></div>{layers}</div>'
        original=self.figure('img/flight-studio/cfs-layered-architecture.png',t('original')+' · NASA cFS',t('original_layers_caption'),1245,867)
        layers+=f'<details class="eng-original"><summary>{t("original")} · NASA cFS</summary>{original}</details>'
        chapters+=self.chapter(2+first,'cfs-layers','layers',layers,'layers_body')
        steps=self.copy['FLIGHT_STEPS']
        self.config['flightSteps']=[{'id':key,'title':title[self.lang],'body':body[self.lang]} for key,title,body in steps]
        nodes=''.join(f'<a href="#message-step-{i}" data-step-select="{i}"><span class="eng-step-dot">{i+1:02}</span><strong>{label}</strong></a>' for i,(_,label,_) in enumerate([('','WEB',''),('','PYTHON',''),('','CI_LAB',''),('','SB → APP',''),('','TO_LAB',''),('','TELEMETRY','')]))
        details=''.join(f'<div id="message-step-{i}" data-step-view="{i}"><span class="eng-step-big" aria-hidden="true">{i+1:02}</span><div><h3>{self.local(title)}</h3><p>{self.local(body)}</p></div></div>' for i,(_,title,body) in enumerate(steps))
        journey=f'<div class="eng-message-lab" data-message-lab><div class="eng-message-top"><span class="mono">COMMAND → cFS → TELEMETRY</span><span class="eng-signal" aria-hidden="true"></span></div><nav class="eng-message-route" aria-label="{t("step")}">{nodes}</nav><div class="eng-step-views">{details}</div><div class="eng-player-controls" data-message-controls hidden><button type="button" data-message-prev aria-label="{t("previous")}">←</button><button type="button" data-message-play data-play-label="{t("play")}" data-pause-label="{t("pause")}">▶ {t("play")}</button><button type="button" data-message-next aria-label="{t("next")}">→</button><span data-message-count class="mono">1 / 6</span></div><p class="eng-disclosure">{t("journey_note")}</p></div>'
        chapters+=self.chapter(3+first,'message-flow','journey',journey+self.packet_inspector(),'journey_body')
        automation='<div class="eng-automation-grid">'+''.join(f'<article><div class="eng-workflow-art" aria-hidden="true">{self.automation_art(i)}</div><p class="eyebrow">0{i+1}</p><h3>{t(key)}</h3>{self.paragraph(key+"_body")}</article>' for i,key in enumerate(['create','discover','explain']))+'</div>'
        chapters+=self.chapter(4+first,'automation','automation',automation,'automation_body')
        chapters+=self.chapter(5+first,'virtual-sensors','sensors',self.sensor_lab(),'sensors_body')
        labels={key:self.strings[key][self.lang] for key in ['objective','application','command','telemetry']}
        mission=f'<div class="eng-mission-drawing" tabindex="0" role="group" aria-label="{t("mission")}">{self.drawings["mission_diagram"](labels)}</div><ol class="eng-mission-text">'+''.join(f'<li><span>0{i+1}</span>{t(key)}</li>' for i,key in enumerate(labels))+'</ol>'
        chapters+=self.chapter(6+first,'mission-planning','mission',mission,'mission_body')
        cards=[]
        for kind,items in self.copy['VALIDATION'].items():
            body='<div class="eng-criteria">'
            for value,label,description in items:
                val=self.local(self.copy['L'](value)) if ' | ' in value else E(value)
                body+=f'<article><span class="eyebrow">{t("target")}</span><strong>{val}</strong><h4>{self.local(self.copy["L"](label))}</h4><p>{self.local(self.copy["L"](description))}</p></article>'
            cards.append((t(kind),body+'</div>'))
        chapters+=self.chapter(7+first,'validation','validation',self.select('validation',cards),'validation_body')
        roadmap='<ol class="eng-roadmap">'+''.join(f'<li><span>{i+1:02}</span><h3>{t(key)}</h3><p>{t("documented" if i<3 else "implemented" if i==3 else "planned")}</p></li>' for i,key in enumerate(['research','analysis','design','implementation','evaluation']))+'</ol>'
        chapters+=self.chapter(8+first,'development','roadmap',roadmap)
        nav=[('architecture',t('design')),('cfs-layers','cFS'),('message-flow','CMD / TLM'),('automation',t('create')),('virtual-sensors',t('sensors_short')),('mission-planning',t('mission'))]
        if runtime:nav.insert(0,('flight-screens',t('screens_short')))
        nav.extend([('validation',t('evaluation')),('development',t('roadmap'))])
        snapshot=json.loads((self.b['ROOT']/'content/flight-studio/runtime/evidence.json').read_text())
        footer=self.paragraph('source_note')+f'<p class="mono">COMMIT {snapshot["commit"][:12]} · cFS / NATIVE / QEMU ARM64</p>'+self.source_link(repo,'GitHub · Flight Studio')
        footer+=''.join(self.source_link(ref['url'],E(ref['path'])) for ref in snapshot['source_refs'] if ref.get('url') and ref['path'] in ['ground_station/catalog.py','interface/backend/architecture_details.py','interface/static/app.js'])
        return self.shell(chapters,nav,hero,t('scope'),[('NASA cFS','CORE FLIGHT SYSTEM'),('Python + Web','UDP / HTTP'),('Linux','DESKTOP / RASPBERRY PI')],footer)

    def sensor_lab(self):
        import math
        t=self.text
        # Redraw the supplied sample() function; these are calculated values,
        # distinct from the preserved QMP capture shown in the evidence card.
        points=' '.join(f'{30+second*16:.1f},{135-65*math.sin(2*math.pi*second/30):.1f}' for second in [i/4 for i in range(121)])
        source=json.loads((self.b['ROOT']/'content/flight-studio/runtime/temperature-source.json').read_text())
        chart=f'''<div class="eng-signal-chart"><div class="eng-window-bar"><span>TMP105 · sample(t)</span><span>°C</span></div><svg viewBox="0 0 540 250" role="img" aria-label="{t('signal')}"><g stroke="#4E7F7B" stroke-width=".7" opacity=".5"><path d="M30 70H510M30 135H510M30 200H510M30 40V215M270 40V215M510 40V215"/></g><g fill="#D9E4DD" font-family="monospace" font-size="11"><text x="35" y="60">28.5</text><text x="35" y="125">23.5</text><text x="35" y="190">18.5</text><text x="30" y="238">0 s</text><text x="258" y="238">15 s</text><text x="484" y="238">30 s</text></g><polyline points="{points}" fill="none" stroke="#F2CBAE" stroke-width="3"/><path d="M110 40V215" stroke="#A9CBC5" stroke-dasharray="4 5" data-signal-guide/><circle cx="110" cy="78.7" r="7" fill="#D9694E" stroke="#FBF8F1" stroke-width="2" data-signal-dot/></svg><div class="eng-signal-values"><div><span>Python · °C</span><output data-signal-c>27.830</output></div><b aria-hidden="true">× 1000 →</b><div><span>QMP · m°C</span><output data-signal-mc>27830</output></div></div></div>'''
        control=f'<div class="eng-signal-copy"><h3>{t("signal")}</h3>{self.paragraph("signal_body")}<div class="eng-signal-slider" data-signal-controls hidden><label for="sensor-seconds">{t("elapsed")} <output data-signal-seconds>5.00 s</output></label><input id="sensor-seconds" data-signal-time type="range" min="0" max="30" step=".25" value="5"></div><code>23.5 + 5 × sin(2π × t / 30)</code><p class="eng-disclosure">{t("signal_note")}</p></div>'
        views=[(name,self.paragraph(key)) for name,key in [('Python','sensor_python'),('QMP / TMP105','sensor_qmp'),('I²C / Linux','sensor_i2c'),('cFS / Telemetry','sensor_cfs')]]
        route='<div class="eng-sensor-route" aria-hidden="true">'+''.join(f'<div data-sensor-node="{i}"><span>0{i+1}</span><strong>{name}</strong><code>{detail}</code></div>' for i,(name,detail) in enumerate([('PYTHON','sample(t) · °C'),('QMP','qom-set · m°C'),('I²C','bus 1 · 0x48'),('cFS','APP → SB → TO')]))+'</div>'
        body=f'<div class="eng-sensor-lab" data-sensor-lab><div class="eng-signal-lab">{chart}{control}</div>{route}{self.select("sensor-path",views,"eng-sensor-selector")}<aside class="eng-sensor-evidence"><span class="eng-qmp-ok">QMP · OK</span><div><h3>{t("observed")}</h3>{self.paragraph("sensor_evidence")}</div></aside><details class="eng-original"><summary>{t("code")} · sample()</summary>{self.code_block(source)}</details></div>'
        return body

    def component_icon(self, name):
        paths={'web':'<rect x="5" y="9" width="54" height="38" rx="3"/><path d="M5 19h54M21 56h22M32 47v9M12 14h1m5 0h1m5 0h1"/>','backend':'<rect x="12" y="4" width="40" height="16" rx="3"/><rect x="12" y="25" width="40" height="16" rx="3"/><rect x="12" y="46" width="40" height="14" rx="3"/><path d="M20 12h1m7 0h16M20 33h1m7 0h16M20 53h1m7 0h16"/>','flight':'<rect x="18" y="18" width="28" height="28" rx="3"/><path d="M24 18V7m8 11V7m8 11V7M24 46v11m8-11v11m8-11v11M18 24H7m11 8H7m11 8H7m39-16h11M46 32h11M46 40h11"/>'}
        return f'<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">{paths[name]}</svg>'

    def automation_art(self,i):
        if i==0:
            return '<svg viewBox="0 0 280 150"><g fill="#FBF8F1" stroke="#1F4A4F" stroke-width="1.5"><path d="M30 26h66l17 17v83H30z"/><path d="M96 26v19h17"/><path d="M165 36h65l17 17v83h-82z"/></g><g stroke="#4E7F7B" stroke-width="3"><path d="M44 63h44M44 77h30M44 91h39M180 72h45M180 86h27M180 100h37"/></g><path d="M119 80h36m-8-8 8 8-8 8" fill="none" stroke="#B04A32" stroke-width="2"/><text x="47" y="117" font-size="13" fill="#1F4A4F">APP</text></svg>'
        if i==1:
            return '<svg viewBox="0 0 280 150"><rect x="20" y="28" width="100" height="96" rx="5" fill="#1F4A4F"/><g stroke="#A9CBC5" stroke-width="3"><path d="M34 49h61M34 64h37M44 80h59M44 95h44"/></g><path d="M127 77h30m-7-7 7 7-7 7" fill="none" stroke="#B04A32" stroke-width="2"/><g fill="#FBF8F1" stroke="#1F4A4F"><rect x="168" y="28" width="92" height="25" rx="4"/><rect x="168" y="63" width="92" height="25" rx="4"/><rect x="168" y="98" width="92" height="25" rx="4"/></g><g font-size="12" fill="#1F4A4F"><text x="181" y="45">MSG ID</text><text x="181" y="80">CMD CODE</text><text x="181" y="115">PAYLOAD</text></g></svg>'
        return '<svg viewBox="0 0 280 150"><rect x="20" y="30" width="116" height="90" rx="5" fill="#FBF8F1" stroke="#1F4A4F"/><path d="M36 54h80M36 72h55M36 90h67" stroke="#4E7F7B" stroke-width="3"/><circle cx="213" cy="73" r="35" fill="#F2CBAE" stroke="#1F4A4F"/><path d="M202 64a11 11 0 1 1 15 10c-5 3-5 4-5 8m0 9v1M145 75h25" fill="none" stroke="#1F4A4F" stroke-width="3" stroke-linecap="round"/></svg>'

    def code_block(self, source):
        import re
        def highlight(line):
            pattern=r'//.*$|"(?:\\.|[^"\\])*"|\b(?:0x[0-9a-fA-F]+|[0-9]+)\b|\b(?:void|int|int32_t|uint32_t|uint64_t|uint8_t|char|static|volatile|const|if|else|for|while|return|switch|case|break|sizeof|typedef|struct|enum|sd|ld|csrr|csrw|ret)\b'
            out='';last=0
            for match in re.finditer(pattern,line):
                word=match[0];kind='comment' if word.startswith('//') else 'string' if word.startswith('"') else 'number' if word[0].isdigit() else 'keyword'
                out+=E(line[last:match.start()])+f'<span class="syntax-{kind}">{E(word)}</span>';last=match.end()
            return out+E(line[last:])
        lines=''.join(f'<span class="eng-code-line" data-line="{source["start_line"]+i}">{highlight(line) or " "}</span>' for i,line in enumerate(source['code'].splitlines()))
        return f'<div class="eng-code" data-source-path="{E(source["path"])}"><div class="eng-window-bar"><span class="eng-window-dots" aria-hidden="true">● ● ●</span><span>{E(source["path"])}</span><span>{E(source.get("language","C / ASM"))}</span></div><pre tabindex="0" aria-label="{E(source["path"])}"><code>{lines}</code></pre>{self.source_link(source["url"])}</div>'

    def kernel_page(self):
        t=self.text;d=self.d
        evidence=json.loads((self.b['ROOT']/'content/kernel-os/evidence.json').read_text())
        locale_path=self.b['ROOT']/'content/kernel-os/locales.json'
        locales=json.loads(locale_path.read_text()) if locale_path.exists() else {}
        if 'activities' in locales:locales=locales['activities']
        hero=self.drawings['kernel_hero']({'cpu':'CPU','memory':self.strings['vram'][self.lang],'console':self.strings['console'][self.lang],'uart':'UART','timer':'Timer'})
        self.config['kernel']=[]
        activities=[]
        for activity in evidence['activities']:
            aid=activity['id']; translated=locales.get(aid,{})
            title=t(aid)
            description=self.local(translated.get('description',activity['description']))
            notes=self.local(translated.get('notes',''))
            frames=[]
            for i,frame in enumerate(activity['frames']):
                tr=translated.get('frames',[])
                item=tr[i] if i<len(tr) else {}
                frames.append({**frame,'file':d.r(frame['file']),'label':self.local(item.get('label',frame['label'])),'focus':frame.get('focus_rect',activity['focus_rect'])})
            initial=activity.get('preview_frame',0)
            frame=frames[initial]
            focus=' '.join(str(v) for v in frame['focus'])
            config={'id':aid,'frames':[{**f,'label':html.unescape(f['label'])} for f in frames],'initial':initial,'focus':activity['focus_rect']}
            self.config['kernel'].append(config)
            source=self.select('source-'+aid,[(t('code'),self.code_block(activity['source'])),(t('test_call'),self.code_block(activity['demo_source']))],'eng-code-select')
            frame_links=''.join(f'<a href="{f["file"]}" data-gallery data-caption="{f["label"]}"><img src="{f["file"]}" alt="{f["label"]}" width="1280" height="720" loading="lazy"><span>{i+1:02} · {f["label"]}</span></a>' for i,f in enumerate(frames))
            terminal=E(frame.get('uart_display','').strip())
            tasks=frame.get('observed',{}).get('processes',[])
            task_cards=''.join(f'<div data-observed-task="{task["pid"]}"><strong>{E(task["name"])}</strong><span data-observed-state>{task["state_label"]}</span><code data-observed-sp>sp {task["saved_sp"]}</code></div>' for task in tasks)
            observed=f'<div class="eng-observed-tasks"><p>{t("observed_ram")}</p><div>{task_cards}</div></div>' if tasks else ''
            output=f'''<div class="eng-output"><div class="eng-window-bar"><span class="eng-window-dots" aria-hidden="true">● ● ●</span><span>QEMU CEP · 1280 × 720</span><span class="eng-record-dot">REC</span></div>
<div class="eng-frame-wrap"><svg class="eng-frame" data-frame viewBox="{focus}" role="img" aria-label="{frame['label']}"><image href="{frame['file']}" width="1280" height="720"/></svg></div>
<div class="eng-frame-caption"><span class="mono" data-frame-count>{initial+1:02} / {len(frames):02}</span><p data-frame-caption>{frame['label']}</p></div>
<div class="eng-player-controls" data-replay-controls hidden><button type="button" data-replay-prev aria-label="{t('previous')}">←</button><button type="button" data-replay-play data-play-label="{t('play')}" data-pause-label="{t('pause')}">▶ {t('play')}</button><button type="button" data-replay-next aria-label="{t('next')}">→</button><button type="button" data-replay-zoom aria-pressed="true">{t('detail_view')}</button><input type="range" data-replay-seek min="0" max="{len(frames)-1}" value="{initial}" aria-label="{t('frames')}"></div>
{observed}<details class="eng-uart"><summary>UART · {t('captured_output')}</summary><pre data-uart-output tabindex="0">{terminal}</pre></details></div>'''
            panels=f'<article class="eng-replay" data-replay="{aid}"><p class="eng-activity-intro">{description}</p><div class="eng-lab-windows">{source}{output}</div><p class="eng-disclosure">{t("record_note")}</p><details class="eng-capture-notes"><summary>{t("frames")} · {t("notes")}</summary><p>{notes}</p><div class="eng-capture-grid">{frame_links}</div><code class="eng-command">{E(activity["command"])}</code></details></article>'
            activities.append((title,panels))
        chapters=self.chapter(1,'execution-lab','lab',self.select('kernel-activities',activities,'eng-activity-tabs'),'lab_body')
        # The map is deliberately schematic; it uses the machine's actual MMIO addresses.
        map_ids=[('ram','ram','ram_detail'),('timer-cmp','compare','compare_detail'),('timer','clock','clock_detail'),('uart','uart','uart_detail'),('framebuffer-control','display','display_detail'),('framebuffer','vram','vram_detail')]
        memory={item['id']:item for item in evidence['memory']}
        map_views=[];map_rows=''
        for i,(mid,key,detail) in enumerate(map_ids):
            item=memory[mid]
            map_rows+=f'<div class="eng-memory-row" data-memory-row="{i}"><code>{item["address"].upper().replace("0X","0x")}</code><span>{t(key)}</span><i aria-hidden="true"></i></div>'
            map_views.append((t(key),f'<div class="eng-memory-detail"><span class="eng-large-address">{item["address"]}</span>{self.paragraph(detail)}{self.source_link(item["source"]["url"],item["source"]["path"])}</div>'))
        map_body=f'<div class="eng-memory-lab"><div class="eng-memory-map"><p class="eyebrow">MMIO / CEP</p>{map_rows}<p class="eng-disclosure">{t("map_note")}</p></div>{self.select("memory",map_views)}</div>'
        elf='<div class="eng-elf-map">'+''.join(f'<div><strong>{E(memory["kernel-"+key]["name"])}</strong><span>{memory["kernel-"+key]["address"]}</span><small>{memory["kernel-"+key]["size"]:,} B</small></div>' for key in ['text','rodata','data','bss'])+'</div>'
        map_body+=f'<div class="eng-elf"><h3>ELF · {t("this_build")}</h3>{elf}<p class="eng-disclosure">{t("build_addresses")}</p></div>'
        chapters+=self.chapter(2,'memory-map','memory',map_body,'memory_body')
        pixel=f'''<div class="eng-pixel-lab" data-pixel-lab><div class="eng-pixel-screen"><div class="eng-window-bar"><span>FRAMEBUFFER</span><span>1280 × 720</span></div><svg viewBox="0 0 640 360" role="img" aria-label="{t('pixel_title')}"><defs><pattern id="pixel-grid" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#426967" stroke-width=".5"/></pattern></defs><rect width="640" height="360" fill="#183B40"/><rect width="640" height="360" fill="url(#pixel-grid)"/><path d="M0 80H120V360" stroke="#F2CBAE" stroke-dasharray="5 5" fill="none" data-pixel-guide/><circle cx="120" cy="80" r="7" fill="#D9694E" stroke="#F4EEE2" stroke-width="2" data-pixel-dot/><text x="134" y="69" fill="#F4EEE2" font-size="16" font-family="monospace" data-pixel-coordinates>(240, 160)</text></svg><span class="eng-pixel-origin">0x80000000</span></div><div class="eng-pixel-controls"><h3>{t('pixel_title')}</h3>{self.paragraph('pixel_body')}<div class="eng-coordinate-inputs" data-pixel-inputs hidden><label>{t('column')}<input type="number" min="0" max="1279" value="240" data-pixel-x></label><label>{t('row')}<input type="number" min="0" max="719" value="160" data-pixel-y></label></div><div class="eng-address-equation"><code>0x80000000 + 4 × (1280 × <span data-y>160</span> + <span data-x>240</span>)</code><span>{t('address')}</span><output data-pixel-address>0x800C83C0</output><small>{t('offset')}: <span data-pixel-offset>820160</span> B</small></div></div></div>'''
        # Seed the exact arithmetic rather than a hand-authored displayed address.
        offset=4*(1280*160+240)
        pixel=pixel.replace('0x800C83C0',f'0x{0x80000000+offset:08X}').replace('820160',str(offset))
        glyphs=json.loads((self.b['ROOT']/'content/kernel-os/glyphs.json').read_text());self.config['glyphs']=glyphs
        cells=''.join(f'<span class="{"on" if glyphs["A"][row]>>col&1 else ""}" data-bit="{row*8+col}"></span>' for row in range(8) for col in range(8))
        bytes_html=''.join(f'<span data-glyph-byte>0x{n:02X}</span>' for n in glyphs['A'])
        choices=''.join(f'<button type="button" data-glyph="{E(char)}" aria-pressed="{str(char=="A").lower()}">{E(char)}</button>' for char in glyphs)
        glyph=f'<div class="eng-glyph-lab" data-glyph-lab><div><h3>{t("glyph_title")}</h3>{self.paragraph("glyph_body")}<div class="eng-choices" data-glyph-controls hidden aria-label="{t("glyph_title")}">{choices}</div>{self.source_link(evidence["font_example"]["source"]["url"],"font8x8_basic")}</div><div class="eng-glyph-display" aria-label="{t("glyph_title")}"><div class="eng-bitmap" aria-hidden="true">{cells}</div><div class="eng-glyph-bytes">{bytes_html}</div><code>(byte &gt;&gt; x) &amp; 1</code></div></div>'
        chapters+=self.chapter(3,'pixel-address','pixel_title',pixel+glyph)
        flow='<ol class="eng-interrupt-flow">'+''.join(f'<li><span>0{i+1}</span><strong>{name}</strong><code>{detail}</code></li>' for i,(name,detail) in enumerate([('CLINT','mtime ≥ mtimecmp'),('TRAP','mtvec → mon_traitant'),('C','trap_handler(mcause)'),('SCHEDULER','ordonnance()'),('CONTEXT','ctx_sw() / mret')]))+'</ol>'
        timer_drawing=''.join(f'<span class="{"eng-tick-major" if i%5==0 else ""}"></span>' for i in range(21))
        interrupt=f'<div class="eng-timer-strip"><div><span class="eng-timer-value">20 Hz</span><p>10 MHz ÷ 20 = 500 000 ticks</p></div><div class="eng-timer-ticks" aria-hidden="true">{timer_drawing}<span class="eng-timer-caption">0 s <b>50 ms / tick</b> 1 s</span></div></div>{flow}<details class="eng-original"><summary>{t("code")} · mon_traitant</summary>{self.code_block(evidence["context"]["trap_source"])}</details>'
        chapters+=self.chapter(4,'timer-interrupts','interrupt',interrupt,'interrupt_body')
        context=evidence['context']; regs=''.join(f'<span>{reg}</span>' for reg in context['registers'])
        stacks=''.join(f'<div class="eng-task-stack"><strong>{s["name"]}</strong><code>{s["end"]}</code><div class="eng-stack-slots"><i></i><i></i><i></i><i></i><span>sp ↓</span></div><code>{s["start"]}</code><small>32 KiB</small></div>' for s in context['stacks'])
        context_body=f'<div class="eng-context-switch"><div class="eng-register-bank"><p class="eyebrow">{t("save")}</p><h3>18 × 64 bits</h3><div>{regs}</div><p>144 B · ctxt.S</p></div><div class="eng-switch-arrow" aria-hidden="true">⇄<code>ctx_sw</code></div><div class="eng-task-stacks"><p class="eyebrow">{t("restore")}</p><div>{stacks}</div></div><p class="eng-shared-memory">{t("shared")} · {t("stack_pointer_note")}</p></div><details class="eng-original"><summary>{t("code")} · ctx_sw / processus_t</summary><div class="eng-two-columns">{self.code_block(context["switch_source"])}{self.code_block(context["task_record_source"])}</div></details>'
        chapters+=self.chapter(5,'context-switch','context_title',context_body,'context_body')
        states=self.select('states',[(name,self.paragraph(key)) for name,key in [('RUN','run_detail'),('RUNNABLE','ready_detail'),('WAIT','wait_detail'),('DIE','die_detail')]])
        state_svg='''<svg viewBox="0 0 660 300" class="eng-state-diagram" aria-hidden="true"><defs><marker id="state-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 7 3.5 0 7" fill="#4E7F7B"/></marker></defs><g fill="none" stroke="#4E7F7B" stroke-width="2" marker-end="url(#state-arrow)"><path d="M230 72H410"/><path d="M410 102H230"/><path d="M490 114V206"/><path d="M409 240H150V115"/><path d="M520 115Q640 150 573 210"/></g><g font-family="monospace" font-size="12" fill="#1E3A3D"><text x="274" y="56">ordonnance()</text><text x="291" y="125">timer</text><text x="502" y="170">dors()</text><text x="245" y="260">wake-up</text><text x="552" y="196">exit</text></g><g data-state-node="1"><rect x="70" y="55" width="160" height="60" rx="8" fill="#A9CBC5" stroke="#1F4A4F"/><text x="150" y="91" text-anchor="middle" fill="#1E3A3D" font-family="monospace" font-size="19">RUNNABLE</text></g><g data-state-node="0"><rect x="410" y="55" width="160" height="60" rx="8" fill="#F2CBAE" stroke="#1F4A4F"/><text x="490" y="91" text-anchor="middle" fill="#1E3A3D" font-family="monospace" font-size="19">RUN</text></g><g data-state-node="2"><rect x="409" y="210" width="125" height="60" rx="8" fill="#D8CCE0" stroke="#1F4A4F"/><text x="471" y="247" text-anchor="middle" fill="#1E3A3D" font-family="monospace" font-size="19">WAIT</text></g><g data-state-node="3"><rect x="552" y="210" width="100" height="60" rx="8" fill="#EADFC8" stroke="#1F4A4F"/><text x="602" y="247" text-anchor="middle" fill="#1E3A3D" font-family="monospace" font-size="19">DIE</text></g></svg>'''
        states=f'<div class="eng-state-lab">{state_svg}{states}</div>'
        whole=evidence['complete_kernel_run']
        whole_views=[(t(key),self.figure(frame['file'],t(key),t('whole_body'))) for frame,key in zip(whole['frames'],['whole_start','whole_end'])]
        states+=f'<details class="eng-original"><summary>{t("whole_kernel")}</summary>{self.select("whole-kernel",whole_views)}<div class="eng-code"><div class="eng-window-bar">UART · {t("whole_kernel")}</div><pre tabindex="0" aria-label="UART">{E(whole["log_text"])}</pre></div></details>'
        chapters+=self.chapter(6,'process-lifecycle','states',states,'states_body')
        nav=[('execution-lab',t('lab')),('memory-map',t('memory_short')),('pixel-address','Pixels'),('timer-interrupts','Timer'),('context-switch',t('context_short')),('process-lifecycle',t('processes'))]
        footer=f'<p>{t("source_note")}</p><p class="mono">COMMIT {evidence["commit"][:12]} · GCC 11.1.0 · QEMU CEP 6.2.50</p>{self.source_link(evidence["commit_url"],"GitHub · OS")}{self.source_link(evidence["provenance"]["license_url"],"GPL-2.0 / credits")}'
        return self.shell(chapters,nav,hero,t('runtime'),[('6',t('activities')),('32 KiB',t('stack')),('20 Hz',t('timer'))],footer)

    def packet_inspector(self):
        path=self.b['ROOT']/'content/flight-studio/runtime/evidence.json'
        if not path.exists(): return ''
        flow=json.loads(path.read_text())['command_flow']
        t=self.text
        fields=[('MID',0,2,'packet_mid'),('SEQ',2,2,'packet_seq'),('LENGTH',4,2,'packet_length'),('CC',6,1,'packet_cc'),('XOR',7,1,'packet_checksum')]
        hk_fields=[('MID',0,2,'packet_mid'),('SEQ',2,2,'packet_seq'),('LENGTH',4,2,'packet_length'),('TIME',6,10,'packet_time'),('CommandCounter',16,1,'packet_counter'),('CommandErrorCounter',17,1,'packet_error')]
        options=[('command','noop',flow['command_hex'],fields),('before','hk_before',flow['telemetry_hex_before'],hk_fields),('after','hk_after',flow['telemetry_hex_after'],hk_fields)]
        self.config['packets']=[{'id':key,'label':self.strings[label][self.lang],'hex':raw,'fields':[{'name':name,'start':start,'size':size,'description':self.strings[description][self.lang]} for name,start,size,description in cols]} for key,label,raw,cols in options]
        all_packets=''
        for key,label,raw,cols in options:
            cells=''.join(f'<span data-byte="{i//2}"><small>{i//2:02}</small><b>{raw[i:i+2].upper()}</b></span>' for i in range(0,len(raw),2))
            fields_html=''.join(f'<button type="button" data-packet-field="{i}" aria-pressed="{str(i==0).lower()}">{name}</button>' for i,(name,_,_,_) in enumerate(cols))
            descriptions=''.join(f'<div data-packet-explanation="{i}"><strong>{name}</strong><p>{t(description)}</p></div>' for i,(name,_,_,description) in enumerate(cols))
            all_packets+=f'<section data-packet-view="{key}"><h4>{t(label)}</h4><div class="eng-packet-bytes">{cells}</div><div class="eng-choices" data-packet-fields hidden>{fields_html}</div><div class="eng-packet-explanations">{descriptions}</div></section>'
        options_html=''.join(f'<button type="button" data-packet-kind="{key}" aria-pressed="{str(i==0).lower()}">{t(label)}</button>' for i,(key,label,_,_) in enumerate(options))
        return f'<div class="eng-packet-inspector" data-packet-inspector><div class="eng-packet-heading"><p class="eyebrow">CCSDS / CFE · {t("replay")}</p><h3>{t("packet_title")}</h3><p>{t("packet_body")}</p></div><div class="eng-choices" data-packet-kinds hidden>{options_html}</div>{all_packets}</div>'

    def flight_screens(self):
        # The runtime capture is populated after launching the user's local app.
        path=self.b['ROOT']/'content/flight-studio/runtime/evidence.json'
        if not path.exists():return ''
        data=json.loads(path.read_text())
        locale_path=path.with_name('locales.json')
        locales=json.loads(locale_path.read_text()) if locale_path.exists() else {}
        items=[]
        for screen in data.get('screenshots',[]):
            translation=locales.get(Path(screen['file']).stem,{})
            title=self.local(translation.get('title',screen.get('title',screen.get('label','Flight Studio'))))
            caption=self.local(translation.get('caption',screen.get('caption',screen.get('description',title))))
            items.append((title,self.figure(screen['file'],title,caption,screen.get('width',1440),screen.get('height',1000))))
        return self.select('screens',items,'eng-screen-gallery') if items else ''


def render(b, project, lang):
    case=Case(b,project,lang)
    return case.flight_page() if case.flight else case.kernel_page()
