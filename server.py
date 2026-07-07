import os, json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS_PATH = os.path.join(HERE, 'defaults.json')

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def do_POST(self):
        if self.path == '/save-defaults':
            length = int(self.headers.get('Content-Length', 0))
            data = self.rfile.read(length).decode('utf-8')
            try:
                json.loads(data)
            except Exception:
                self.send_error(400, 'Invalid JSON'); return
            with open(DEFAULTS_PATH, 'w', encoding='utf-8') as f:
                f.write(data)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_error(404)

if __name__ == '__main__':
    print('Serving on http://localhost:8787 (with /save-defaults)')
    ThreadingHTTPServer(('', 8787), Handler).serve_forever()
