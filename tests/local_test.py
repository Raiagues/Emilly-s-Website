"""Exercise the public commands against an isolated fixture, including busy ports."""
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

SOURCE = Path(__file__).resolve().parents[1]


class LocalCommands(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='portfolio with spaces ')
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        for file in ['setup', 'start', 'stop', 'scripts/runtime.sh', 'scripts/local.py']:
            shutil.copy2(SOURCE / file, self.root / file)
        (self.root / 'scripts/build.py').write_text(
            'from pathlib import Path\np=Path("dist/pt"); p.mkdir(parents=True, exist_ok=True)\n'
            '(p/"index.html").write_text("<h1>Site pronto</h1>")\n')
        (self.root / 'scripts/check.py').write_text('print("Checked fixture")\n')
        (self.root / '.env').write_text('PRIVATE_FIXTURE=1')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            self.port = sock.getsockname()[1]

    def tearDown(self):
        self.run_command('stop')
        self.temp.cleanup()

    def run_command(self, command, *args):
        return subprocess.run([str(self.root / command), *map(str, args)],
                              cwd='/tmp', text=True, capture_output=True, timeout=20)

    def test_setup_start_repeat_and_stop_from_another_directory(self):
        self.assertEqual(self.run_command('setup').returncode, 0)
        start = self.run_command('start', self.port)
        self.assertEqual(start.returncode, 0, start.stderr)
        self.assertIn(f'http://127.0.0.1:{self.port}/pt/', start.stdout)
        state_path = self.root / '.runtime/server.json'
        state = state_path.read_text()
        self.assertIn('já está rodando', self.run_command('start', self.port).stdout)
        self.assertEqual(state, state_path.read_text())
        with urlopen(f'http://127.0.0.1:{self.port}/pt/') as response:
            self.assertIn(b'Site pronto', response.read())
        for path in ['/.env', '/scripts/local.py', '/.runtime/server.json', '/_portfolio/health']:
            with self.assertRaises(HTTPError):
                urlopen(f'http://127.0.0.1:{self.port}{path}')
        self.assertEqual(self.run_command('stop').returncode, 0)
        self.assertFalse(state_path.exists())
        self.assertIn('já está parado', self.run_command('stop').stdout)
        with socket.socket() as sock:
            self.assertNotEqual(sock.connect_ex(('127.0.0.1', self.port)), 0)

    def test_busy_port_and_stale_state_never_stop_another_server(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200); self.end_headers(); self.wfile.write(b'other server')
            def log_message(self, *args): pass
        with ThreadingHTTPServer(('127.0.0.1', self.port), Handler) as other:
            thread = threading.Thread(target=other.serve_forever, daemon=True)
            thread.start()
            try:
                result = self.run_command('start', self.port)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('8137', result.stderr)
                (self.root / '.runtime/server.json').write_text(json.dumps({
                    'root':str(self.root),'port':self.port,'token':'stale-token'}))
                self.assertEqual(self.run_command('stop').returncode, 0)
                with urlopen(f'http://127.0.0.1:{self.port}/') as response:
                    self.assertEqual(response.read(), b'other server')
            finally:
                other.shutdown()
                thread.join()

    def test_invalid_port_does_not_start_a_process(self):
        for port in ['0','65536','not-a-port']:
            self.assertNotEqual(self.run_command('start',port).returncode, 0)
        self.assertFalse((self.root / '.runtime/server.json').exists())


if __name__ == '__main__':
    unittest.main()
