"""Export the HTML figures to PDF for the thesis.

Each thesis/figures/html/<name>.html becomes thesis/figures/<name>.pdf, sized
exactly to the figure, which the chapter includes with \\includegraphics.

    python3 thesis/figures/html/export.py              # every figure
    python3 thesis/figures/html/export.py ch5-system   # just one

Uses the installed Google Chrome, headless. The page is served over a local
web server because browsers won't load fonts or scripts from file:// pages.
"""

import functools
import http.server
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(HERE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def export(name: str, port: int):
    pdf = OUT / f"{name}.pdf"
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--user-data-dir={profile}",
             "--virtual-time-budget=4000", "--run-all-compositor-stages-before-draw",
             f"--print-to-pdf={pdf}", f"http://127.0.0.1:{port}/{name}.html"],
            check=True, capture_output=True,
        )
    print(f"{pdf.relative_to(OUT.parent.parent)}  {pdf.stat().st_size // 1024} KB")


def main(names):
    pages = sorted(p.stem for p in HERE.glob("*.html"))
    todo = names or pages
    missing = set(todo) - set(pages)
    if missing:
        sys.exit(f"No such figure: {', '.join(sorted(missing))}")
    server = serve()
    try:
        for name in todo:
            export(name, server.server_address[1])
    finally:
        server.shutdown()


if __name__ == "__main__":
    main(sys.argv[1:])
