"""Serve the build at its GitHub Pages subpath for a realistic local check."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Handler(SimpleHTTPRequestHandler):
    base_path = "/open-security-courses/"

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/":
            self.send_response(302)
            self.send_header("Location", self.base_path)
            self.end_headers()
            return
        if not path.startswith(self.base_path):
            self.send_error(404)
            return
        super().do_GET()

    def translate_path(self, path):
        path = unquote(urlsplit(path).path)
        if path.startswith(self.base_path):
            path = "/" + path[len(self.base_path):]
        return super().translate_path(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--site-dir", type=Path, default=Path("site"))
    args = parser.parse_args()
    site = args.site_dir.resolve()
    if not (site / "index.html").is_file():
        parser.error("Build the site before starting this server.")
    server = ThreadingHTTPServer(("127.0.0.1", args.port), partial(Handler, directory=str(site)))
    print(f"Preview: http://127.0.0.1:{args.port}{Handler.base_path}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
