"""Serve dist under a project prefix to catch GitHub Pages path regressions."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]/'dist'
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        if not urlsplit(self.path).path.startswith('/Emilly-s-Website/'):
            self.send_error(404); return
        self.path=self.path.removeprefix('/Emilly-s-Website')
        super().do_GET()
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
print(f'http://127.0.0.1:{server.server_port}/Emilly-s-Website/',flush=True)
server.serve_forever()
