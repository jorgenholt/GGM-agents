# thesis

The project thesis text, in LaTeX. **We write it on the hub** (the Writing tab of
https://claude.ai/artifact/FqBcHUumqgnmVJMQ5Xevbh); these files are where it ends up.

## How writing reaches this folder

1. On the hub, each section opens in a Word-like editor. Text is saved as you type, in the page's
   shared storage on claude.ai, so the other person sees it straight away.
2. Every three hours a routine runs `thesis/sync.py`, which converts the edited sections to LaTeX,
   writes them here and commits **straight to `main`**. The commit message says who edited.
3. The same run rebuilds the hub, so text written here (by hand or by Claude) shows up there too.

**Nothing is ever overwritten.** A hub edit is applied only if the file here is still the version
the edit started from. If someone changed the file in the meantime, the sync leaves it alone and
the hub shows "Needs attention" on that section, with a choice between the two versions.

## Layout

| Path | What it is |
|---|---|
| `main.tex` | The document. Placeholder layout until we know whether IØT has a template |
| `chapters/NN-name/_title.txt` | The chapter title |
| `chapters/NN-name/NN-section.tex` | One section. Order follows the file names |
| `chapters/NN-name/_chapter.tex`, `chapters.tex` | Generated: the chapter heading and `\input` lines |
| `references.bib` | Generated from `docs/literature-sources.md`. Fix entries there, not here |
| `sync.py` | The converter and sync. `python3 thesis/sync.py check` tests every section |

## Editing these files directly

Allowed, and Claude does it. Keep to what the hub editor understands, or the hub shows it as a
grey "LaTeX" block: `\subsection`, `\subsubsection`, paragraphs, `\textbf`, `\emph`, `itemize` and
`enumerate`, `\href`/`\url`, `\citep`/`\citet`, `\footnote`, and `% TODO:` notes. Anything else
(maths, tables, figures) is fine but appears as raw LaTeX on the hub. Write one sentence per line;
it keeps git diffs and merges clean. Run `python3 thesis/sync.py check` afterwards.

## Compiling

Not set up yet. Overleaf or a local LaTeX install can compile `main.tex` with BibTeX.
