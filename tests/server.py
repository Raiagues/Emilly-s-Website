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
        local=self.path.removeprefix('/Emilly-s-Website')
        # A previous deployment's CSS remains fresh in the browser for this regression.
        fixtures = {
            '/__legacy-cache.html': ('text/html', b'<html><head><link rel="stylesheet" href="style/style.css"></head><body>Previous release</body></html>'),
            '/style/style.css': ('text/css', b'body { background: rgb(255, 0, 255); } .hero { display: block; }'),
        }
        if local in fixtures:
            mime, body = fixtures[local]
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'public, max-age=31536000')
            self.end_headers()
            self.wfile.write(body)
            return
        self.path=local
        super().do_GET()
    def log_message(self,*args): pass
server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
print(f'http://127.0.0.1:{server.server_port}/Emilly-s-Website/',flush=True)
server.serve_forever()
