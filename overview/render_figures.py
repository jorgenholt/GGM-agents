"""Render the thesis's TikZ figures to SVG so the hub can show them.

The hub page can't run LaTeX, so a figure written as TikZ in thesis/figures/*.tex
would otherwise appear only as its source. This script compiles each figure on
its own and writes overview/figures/<name>.svg, which build.py embeds in the
hub's data file. Run it after changing a figure, commit the SVGs, and the next
sync shows them:

    python3 overview/render_figures.py            # every figure
    python3 overview/render_figures.py ch5-hormuz # just one

Needs tectonic and pdftocairo (brew install tectonic poppler). The cloud routine
has neither, so the SVGs are rendered locally and committed.

manifest.json records a fingerprint of each figure's source (and the shared
style), so build.py can tell the hub when a preview is older than its figure.
"""

import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGS = ROOT / "thesis" / "figures"
OUT = ROOT / "overview" / "figures"
STYLE = FIGS / "style.tex"


def fingerprint(src: Path) -> str:
    """The figure's source plus the shared style: what the picture depends on."""
    h = hashlib.sha1(src.read_bytes() + b"\0" + STYLE.read_bytes())
    return h.hexdigest()[:12]


def figure_sources():
    return sorted(p for p in FIGS.glob("*.tex") if p != STYLE)


def render(src: Path, tmp: Path) -> str:
    tex = tmp / f"{src.stem}.tex"
    tex.write_text(
        "\\documentclass[11pt,border=8pt]{standalone}\n"
        "\\usepackage[T1]{fontenc}\\usepackage{lmodern}\n"
        f"\\input{{{STYLE.as_posix()}}}\n"
        "\\begin{document}\n"
        f"\\input{{{src.as_posix()}}}\n"
        "\\end{document}\n",
        encoding="utf-8",
    )
    run = subprocess.run(["tectonic", "-X", "compile", tex.name], cwd=tmp, capture_output=True, text=True)
    if run.returncode:
        sys.exit(f"LaTeX failed on {src.name}:\n{run.stderr[-2000:]}")
    svg = tmp / f"{src.stem}.svg"
    subprocess.run(["pdftocairo", "-svg", tex.with_suffix(".pdf").name, svg.name], cwd=tmp, check=True)
    text = svg.read_text(encoding="utf-8")
    # Two decimals are plenty on screen and cut the file by about a third.
    text = re.sub(r"(\d+\.\d\d)\d+", r"\1", text)
    # pdftocairo numbers its ids from 0 in every file; prefix them so two figures on one page don't clash.
    text = re.sub(r'id="([^"]+)"', lambda m: f'id="{src.stem}-{m[1]}"', text)
    text = re.sub(r'(href|xlink:href)="#([^"]+)"', lambda m: f'{m[1]}="#{src.stem}-{m[2]}"', text)
    text = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{src.stem}-{m[1]})", text)
    return text


def main(names):
    sources = figure_sources()
    if names:
        sources = [s for s in sources if s.stem in names]
        missing = set(names) - {s.stem for s in sources}
        if missing:
            sys.exit(f"No such figure: {', '.join(sorted(missing))}")
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    with tempfile.TemporaryDirectory() as tmp:
        for src in sources:
            svg = render(src, Path(tmp))
            (OUT / f"{src.stem}.svg").write_text(svg, encoding="utf-8")
            manifest[src.stem] = fingerprint(src)
            print(f"{src.stem}.svg  {len(svg) // 1024} KB")
    # Drop previews whose figure no longer exists.
    live = {s.stem for s in figure_sources()}
    for name in [n for n in manifest if n not in live]:
        del manifest[name]
        (OUT / f"{name}.svg").unlink(missing_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1:])
