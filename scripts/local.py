"""Build and manage this checkout's loopback-only preview, without PID guessing."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, ProxyHandler

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / '.runtime'
STATE = RUNTIME / 'server.json'
LOG = RUNTIME / 'server.log'
HTTP = build_opener(ProxyHandler({}))


def request(state, action='health'):
    req = Request(f'http://127.0.0.1:{state["port"]}/_portfolio/{action}',
                  headers={'Authorization': 'Bearer ' + state['token']},
                  method='POST' if action == 'stop' else 'GET')
    try:
        with HTTP.open(req, timeout=1) as response:
            return response.status == 204
    except (URLError, TimeoutError, OSError):
        return False


def read_state():
    try:
        state = json.loads(STATE.read_text())
        if (state.get('root') == str(ROOT) and isinstance(state.get('port'), int)
                and 0 < state['port'] < 65536 and isinstance(state.get('token'), str)):
            return state
    except (OSError, ValueError, AttributeError):
        pass
    return None


def build():
    for script in ['build.py', 'check.py']:
        subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], cwd=ROOT, check=True)


def start(port):
    state = read_state()
    if state and request(state):
        print(f'O site já está rodando em http://127.0.0.1:{state["port"]}/pt/')
        return
    build()
    state = {'root': str(ROOT), 'port': port, 'token': secrets.token_urlsafe(32)}
    with LOG.open('w') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'serve', str(port)],
                                   cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                   start_new_session=True,
                                   env={**os.environ, 'PORTFOLIO_PREVIEW_TOKEN': state['token']})
    for _ in range(100):
        if process.poll() is not None:
            raise RuntimeError(f'Não foi possível abrir a porta {port}. Tente ./start 8137.\n' + LOG.read_text())
        if request(state):
            temporary = STATE.with_suffix('.tmp')
            temporary.write_text(json.dumps(state))
            temporary.chmod(0o600)
            temporary.replace(STATE)
            print(f'Site rodando em http://127.0.0.1:{port}/pt/')
            print('Pode fechar este terminal. Para encerrar, execute ./stop.')
            return
        time.sleep(.05)
    process.terminate()
    process.wait(timeout=5)
    raise RuntimeError(f'O servidor não respondeu. Consulte {LOG}.')


def stop():
    state = read_state()
    if not state or not request(state):
        STATE.unlink(missing_ok=True)
        print('O site já está parado.')
        return
    if not request(state, 'stop'):
        raise RuntimeError('Não foi possível encerrar o servidor. Tente ./stop novamente.')
    for _ in range(100):
        if not request(state):
            STATE.unlink(missing_ok=True)
            print('Site encerrado.')
            return
        time.sleep(.05)
    raise RuntimeError('O servidor ainda está encerrando. Tente ./stop novamente.')


def serve(port):
    token = os.environ['PORTFOLIO_PREVIEW_TOKEN']

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(ROOT / 'dist'), **kwargs)

        def end_headers(self):
            self.send_header('Cache-Control', 'no-store')
            super().end_headers()

        def list_directory(self, path):
            self.send_error(404)

        def control(self, stopping=False):
            if not secrets.compare_digest(self.headers.get('Authorization', ''), 'Bearer ' + token):
                self.send_error(403)
                return
            self.send_response(204)
            self.end_headers()
            if stopping:
                threading.Thread(target=self.server.shutdown, daemon=True).start()

        def do_GET(self):
            if urlsplit(self.path).path == '/_portfolio/health':
                self.control()
            else:
                super().do_GET()

        def do_POST(self):
            if self.path == '/_portfolio/stop':
                self.control(stopping=True)
            else:
                self.send_error(404)

    with ThreadingHTTPServer(('127.0.0.1', port), Handler) as server:
        server.serve_forever(poll_interval=.1)


def main():
    parser = argparse.ArgumentParser(description='Servidor local do portfólio')
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['start', 'serve']:
        command_parser = sub.add_parser(command)
        command_parser.add_argument('port', nargs='?', type=int, default=os.environ.get('PORT', '8000'))
    sub.add_parser('stop')
    sub.add_parser('build')
    args = parser.parse_args()
    if hasattr(args, 'port') and not 0 < args.port < 65536:
        parser.error('A porta deve estar entre 1 e 65535.')
    if args.command == 'serve':
        serve(args.port)
        return
    RUNTIME.mkdir(exist_ok=True)
    with (RUNTIME / 'control.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.command == 'start':
            start(args.port)
        elif args.command == 'stop':
            stop()
        else:
            build()


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
