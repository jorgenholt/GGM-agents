"""Render the thesis's figures and tables to SVG so the hub can show them.

The hub page can't run LaTeX, so a TikZ figure (thesis/figures/*.tex) or a table
(a table environment with a \\label in thesis/chapters) would otherwise appear only
as its source. Figures exported from HTML (thesis/figures/*.pdf) are converted too. This script compiles each one on its own and writes
overview/figures/<name>.svg, which build.py embeds in the hub's data file. Run it
after changing a figure or a table, commit the SVGs, and the next sync shows them:

    python3 overview/render_figures.py                # everything
    python3 overview/render_figures.py ch5-hormuz     # one figure
    python3 overview/render_figures.py tab:agents     # one table, by its label

Needs tectonic and pdftocairo (brew install tectonic poppler). The cloud routine
has neither, so the SVGs are rendered locally and committed.

manifest.json records a fingerprint of each source (and the shared style), so
build.py can tell the hub when a preview is older than what it shows.
"""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "thesis" / "chapters"
FIGS = ROOT / "thesis" / "figures"
OUT = ROOT / "overview" / "figures"
STYLE = FIGS / "style.tex"


TEXTWIDTH = "12.65cm"  # the thesis's text width (report, 11pt, a4)
TABLE_RE = re.compile(r"\\begin\{table\*?\}.*?\\end\{table\*?\}", re.S)
LABEL_RE = re.compile(r"\\label\{(tab:[^}]+)\}")


def fingerprint(text: str) -> str:
    """The source plus the shared style: what the picture depends on."""
    h = hashlib.sha1(text.encode() + b"\0" + STYLE.read_bytes())
    return h.hexdigest()[:12]


def figure_sources():
    """TikZ figures (*.tex) and figures exported from HTML (*.pdf, see thesis/figures/html)."""
    return sorted(p for p in [*FIGS.glob("*.tex"), *FIGS.glob("*.pdf")] if p != STYLE)


def table_sources():
    """Labelled table environments in the chapters, as {label: block}."""
    tables = {}
    for path in sorted(CHAPTERS.rglob("*.tex")):
        for block in TABLE_RE.findall(path.read_text(encoding="utf-8")):
            m = LABEL_RE.search(block)
            if m:
                tables[m[1]] = block
    return tables


def sources():
    """Every preview the hub can show: {name: (file stem, LaTeX body, fingerprint)}."""
    out = {}
    for src in figure_sources():
        if src.suffix == ".pdf":
            fp = hashlib.sha1(src.read_bytes()).hexdigest()[:12]
            out[src.stem] = (src.stem, f"\\includegraphics{{{src.as_posix()}}}", fp)
            continue
        text = src.read_text(encoding="utf-8")
        out[src.stem] = (src.stem, f"\\input{{{src.as_posix()}}}", fingerprint(text))
    for label, block in table_sources().items():
        out[label] = (label.replace(":", "-"), table_body(block), fingerprint(block))
    return out


def drop_command(text: str, name: str) -> str:
    """Remove \\name{...} with balanced braces."""
    i = text.find(f"\\{name}{{")
    while i >= 0:
        j, depth = i + len(name) + 1, 0
        for j in range(j, len(text)):
            depth += {"{": 1, "}": -1}.get(text[j], 0)
            if depth == 0:
                break
        text = text[:i] + text[j + 1:]
        i = text.find(f"\\{name}{{")
    return text


def table_body(block: str) -> str:
    """The table without its float and caption; the hub sets the caption itself."""
    body = re.sub(r"\\(begin|end)\{table\*?\}(\[[^\]]*\])?", "", block)
    body = drop_command(drop_command(body, "caption"), "label")
    return f"\\begin{{minipage}}{{{TEXTWIDTH}}}{body}\\end{{minipage}}"


def preamble() -> str:
    """The thesis's own preamble (packages, table style, figure style), minus what a
    standalone picture doesn't need, so previews look like the PDF."""
    main = (ROOT / "thesis" / "main.tex").read_text(encoding="utf-8")
    head = main[main.index("\n", main.index("\\documentclass")) + 1 : main.index("\\title")]
    skip = ("inputenc", "babel", "natbib", "hyperref")
    lines = [l for l in head.splitlines() if not any(f"{{{p}}}" in l for p in skip)]
    return "\n".join(lines).replace("\\input{figures/style}", f"\\input{{{STYLE.as_posix()}}}")


def render(stem: str, body: str, tmp: Path) -> str:
    tex = tmp / f"{stem}.tex"
    tex.write_text(
        "\\documentclass[11pt,border=8pt]{standalone}\n"
        f"{preamble()}\n"
        "\\begin{document}\n"
        f"{body}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    run = subprocess.run(["tectonic", "-X", "compile", tex.name], cwd=tmp, capture_output=True, text=True)
    if run.returncode:
        sys.exit(f"LaTeX failed on {stem}:\n{run.stderr[-2000:]}")
    svg = tmp / f"{stem}.svg"
    subprocess.run(["pdftocairo", "-svg", tex.with_suffix(".pdf").name, svg.name], cwd=tmp, check=True)
    text = svg.read_text(encoding="utf-8")
    # Two decimals are plenty for coordinates and cut the file by about a third. Transform
    # matrices are left alone: their scale factors (e.g. 0.744601) multiply every coordinate
    # inside them, so rounding them shifts arrowheads off their lines and fills off their boxes.
    parts = re.split(r"(matrix\([^)]*\))", text)
    text = "".join(p if p.startswith("matrix(") else re.sub(r"(\d+\.\d\d)\d+", r"\1", p) for p in parts)
    # pdftocairo numbers its ids from 0 in every file; prefix them so two figures on one page don't clash.
    text = re.sub(r'id="([^"]+)"', lambda m: f'id="{stem}-{m[1]}"', text)
    text = re.sub(r'(href|xlink:href)="#([^"]+)"', lambda m: f'{m[1]}="#{stem}-{m[2]}"', text)
    text = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{stem}-{m[1]})", text)
    return text


def main(names):
    every = sources()
    todo = {k: v for k, v in every.items() if not names or k in names}
    missing = set(names) - set(every)
    if missing:
        sys.exit(f"No such figure or table: {', '.join(sorted(missing))}")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    with tempfile.TemporaryDirectory() as tmp:
        for name, (stem, body, fp) in todo.items():
            svg = render(stem, body, Path(tmp))
            (OUT / f"{stem}.svg").write_text(svg, encoding="utf-8")
            manifest[name] = fp
            print(f"{stem}.svg  {len(svg) // 1024} KB")
    # Drop previews whose figure or table no longer exists.
    for name in [n for n in manifest if n not in every]:
        del manifest[name]
        (OUT / f"{name.replace(':', '-')}.svg").unlink(missing_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
