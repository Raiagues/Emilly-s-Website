#!/usr/bin/env python3
"""Check generated HTML, local links, translations and publish boundaries."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import sys
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs=[]; self.ids=set(); self.errors=[]; self.h1=0; self.lang=None; self.forms=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if 'id' in a:
            if a['id'] in self.ids: self.errors.append('duplicate id: '+a['id'])
            self.ids.add(a['id'])
        if tag=='form': self.forms.append(a)
        if tag=='img' and 'alt' not in a: self.errors.append('image missing alt')
        if a.get('target')=='_blank' and 'noopener' not in a.get('rel',''): self.errors.append('external link missing noopener')
        for key in ['href','src']:
            if key in a: self.refs.append(a[key])
pages={}
errors=[]
for file in ROOT.rglob('*.html'):
    if any(p in {'node_modules','dist','.git'} for p in file.relative_to(ROOT).parts): continue
    parsed=Page(); source=file.read_text(); parsed.feed(source); pages[file]=parsed
    if 'exemple' not in file.name and parsed.h1!=1: parsed.errors.append('expected one h1')
    if parsed.lang not in ['en','pt','fr','es']: parsed.errors.append('missing supported language')
    if 'your-video-id' in source or 'Lorem ipsum' in source: parsed.errors.append('placeholder content')
    for form in parsed.forms:
        if form.get('action')!='https://formsubmit.co/emillyraianerodrigues@gmail.com' or form.get('method')!='POST': parsed.errors.append('incorrect contact destination')
    errors.extend(f'{file.relative_to(ROOT)}: {error}' for error in parsed.errors)
for file,parsed in pages.items():
    for ref in parsed.refs:
        url=urlsplit(ref)
        if url.scheme or url.netloc: continue
        if url.path.startswith('/'): errors.append(f'{file.relative_to(ROOT)}: root-absolute URL breaks project Pages: {ref}'); continue
        target=(file.parent/unquote(url.path)).resolve() if url.path else file
        if not target.exists(): errors.append(f'{file.relative_to(ROOT)}: missing {ref}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{file.relative_to(ROOT)}: missing fragment {ref}')
for bad in ['.git','content','scripts','tests','node_modules','.env','package.json']:
    if (ROOT/'dist'/bad).exists(): errors.append(f'Unwanted build artifact: {bad}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS: {len(pages)} HTML pages; local assets, links, fragments, headings, languages, form destination and artifact boundaries.')
