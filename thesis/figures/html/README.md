# Figures drawn in HTML

Some thesis figures are drawn as small web pages and exported to PDF, instead of in TikZ. The
browser does the layout: boxes grow to fit their text, gaps are even, and arrows attach to the
boxes' real edges. With hand-placed TikZ coordinates, each of those was a guess.

| File | What it is |
|---|---|
| `<name>.html` | one figure; `#fig` is exactly the thesis text width (126.5 mm) |
| `fig.css` | the shared look: colours (same as `../style.tex`), panels, chips, spacing |
| `fig.js` | arrows between elements, and the icon set |
| `fonts/` | Latin Modern Sans, the thesis's sans-serif, from the LaTeX distribution (GUST Font License) |
| `export.py` | prints each page to `thesis/figures/<name>.pdf` with headless Chrome |

The chapter includes the PDF with `\includegraphics{figures/<name>}`.

## Changing a figure

1. Edit `<name>.html`. To look at it while you work, serve the folder and open
   <http://127.0.0.1:8766/ch5-system.html> in a browser:

   ```bash
   cd thesis/figures/html && python3 -m http.server 8766
   ```

2. Export it to PDF, and refresh the hub's copy of it:

   ```bash
   python3 thesis/figures/html/export.py ch5-system
   python3 overview/render_figures.py ch5-system
   ```

3. Commit the HTML, the PDF and the SVG in `overview/figures/`.

## Rules that keep the figures clean

- Panel titles sit inside their panel, never on its border.
- Spacing comes from `--gap` in `fig.css`; avoid one-off margins.
- Body text is 8.5 pt, small text 7.5 pt. Nothing smaller.
- Arrows go between element ids with `arrow("#a:b", "#b:t", {...})`; use `straight: true` for a
  clean vertical or horizontal line. Put a label on the side with free space.
- Check the exported PDF at full size before committing, not just the page in the browser.
