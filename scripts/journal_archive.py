"""The full diary, independently accessible in every locale without JavaScript."""
def render(b, lang):
    design = b['DESIGN']['Design'](b, lang, 'journal.html')
    posts, journal, ui = b['POSTS'], b['J'], b['JUI']
    local = design.local
    title = local(ui['home'])
    cards = []
    for post in posts:
        photo = post['photos'][post['cover'][-1]]
        cards.append(f'''<li id="archive-{post['slug']}"><a href="{design.link(journal['path'](post))}"><div class="archive-photo">{journal['photo_html'](photo, lang, design.current)}</div><span class="eyebrow">{local(post['period'])}</span><h2>{local(post['title'])}</h2><p>{local(post['intro'])}</p><span class="more">{local(ui['read'])}{b['DESIGN']['ARROW']}</span></a></li>''')
    events = sorted(((event, post) for post in posts for event in post.get('timeline', [])), key=lambda pair: pair[0]['date'], reverse=True)
    timeline = ''.join(f'<li><time datetime="{event["date"]}">{local(event["label"])}</time><a href="{design.link(journal["path"](post))}{"#" + event["section"] if event.get("section") else ""}">{local(event["title"])}</a></li>' for event, post in events)
    return f'''<main id="main" class="wrap inner-content journal-archive-page"><div class="inner-breadcrumb">{design.button(design.u('home'), design.link('index.html#journal'))}</div><header class="archive-heading"><h1>{title}</h1><span class="mono">{len(posts):02} · {title}</span></header><section class="story-archive" aria-label="{title}"><ol>{''.join(cards)}</ol></section><details class="journal-timeline"><summary>{local(ui['timeline'])}</summary><nav aria-label="{local(ui['timeline'])}"><ol>{timeline}</ol></nav></details></main>'''
