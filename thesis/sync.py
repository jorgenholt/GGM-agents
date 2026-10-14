"""Sync between the thesis text written on the hub and the LaTeX files in this repo.

The hub (overview/index.html) lets us write in a Word-like editor. What we type is
saved as simple HTML in the page's shared storage on claude.ai. This script is the
bridge to git:

    python3 thesis/sync.py export --db DIR --out DIR
        Apply hub edits to thesis/chapters/. DIR holds the page's `drafts` and
        `receipts` collections as JSON files (one file per document). Writes the
        changed .tex files, regenerates chapters.tex and references.bib, and puts
        a commit message and the receipts to record in --out.

    python3 thesis/sync.py check
        Round-trip every section (LaTeX -> hub HTML -> LaTeX) and report any that
        would not survive unchanged. Run it after editing .tex files by hand.

The repo is the record. The hub only ever proposes an edit to a section; a section
is written only if the repo copy is still the one the edit started from. Otherwise
the edit is reported as a conflict and nothing is overwritten.

The editor supports a subset of LaTeX: subsections, paragraphs, bold, italic, lists,
links, citations, footnotes, TODO notes. Anything else (maths, tables, figures,
custom commands) is kept verbatim as a "LaTeX block" or inline LaTeX, so a file
written by hand survives a round trip through the hub.
"""

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

THESIS = Path(__file__).resolve().parent
ROOT = THESIS.parent
CHAPTERS = THESIS / "chapters"


# ---------------------------------------------------------------- sections


def file_hash(path):
    return hashlib.sha1(path.read_bytes()).hexdigest()[:12] if path.exists() else "none"


def section_id(chapter_key, stem):
    return f"{chapter_key}.{stem}"


def split_section(tex):
    """'\\section{Title}\\n\\nbody' -> (title, body)."""
    m = re.match(r"\s*\\section\*?\{((?:[^{}]|\{[^{}]*\})*)\}\s*\n?", tex)
    if not m:
        return "", tex
    return unescape_text(m.group(1)), tex[m.end():].lstrip("\n")


def list_sections():
    """Every chapter and section in the repo, in order."""
    chapters = []
    for cdir in sorted(p for p in CHAPTERS.iterdir() if p.is_dir()):
        title_file = cdir / "_title.txt"
        title = title_file.read_text(encoding="utf-8").strip() if title_file.exists() else cdir.name
        sections = []
        for f in sorted(cdir.glob("*.tex")):
            if f.name.startswith("_"):
                continue
            tex = f.read_text(encoding="utf-8")
            stitle, body = split_section(tex)
            sections.append(
                {
                    "sid": section_id(cdir.name, f.stem),
                    "file": str(f.relative_to(ROOT)),
                    "title": stitle,
                    "hash": file_hash(f),
                    "tex": tex,
                    "html": tex_to_html(body),
                    "words": count_words(body),
                    "todos": len(re.findall(r"^%\s*TODO", body, re.M)),
                }
            )
        chapters.append({"key": cdir.name, "n": cdir.name.split("-")[0].lstrip("0"), "title": title, "sections": sections})
    return chapters


# ---------------------------------------------------------------- text helpers

ESCAPES = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
    ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
]


def escape_text(s):
    out = []
    for ch in s:
        for a, b in ESCAPES:
            if ch == a:
                out.append(b)
                break
        else:
            out.append("~" if ch == "\u00a0" else ch)
    return "".join(out)


def unescape_text(s):
    s = s.replace("~", "\u00a0")  # an unescaped ~ is a non-breaking space in LaTeX
    s = s.replace(r"\textbackslash{}", "\\").replace(r"\textasciitilde{}", "~").replace(r"\textasciicircum{}", "^")
    return re.sub(r"\\([&%$#_{}])", r"\1", s)


def split_sentences(text):
    """One sentence per line, so git merges and diffs work sentence by sentence."""
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(\\])", text.strip())
    return "\n".join(p.strip() for p in parts if p.strip())


def count_words(tex):
    t = re.sub(r"(?m)^%.*$", "", tex)                 # comments and TODO notes
    t = re.sub(r"\\begin\{(\w+\*?)\}.*?\\end\{\1\}", " ", t, flags=re.S)  # raw environments
    t = re.sub(r"\\(cite[pt]?|ref|label|url)\{[^}]*\}", " x ", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)
    t = re.sub(r"[{}\[\]$]", " ", t)
    return len(re.findall(r"[^\W\d_][\w'’-]*|\d+", t))


# ---------------------------------------------------------------- LaTeX -> HTML


def read_group(s, i, open_ch="{", close_ch="}"):
    """s[i] == open_ch. Return (content, index after the closing bracket)."""
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], len(s)


def inline_to_html(s):
    out, i = [], 0
    text_buf = []

    def flush():
        if text_buf:
            out.append(html.escape(unescape_text("".join(text_buf)), quote=False))
            text_buf.clear()

    while i < len(s):
        c = s[i]
        if c == "$":
            flush()
            j = s.find("$", i + 1)
            j = len(s) - 1 if j < 0 else j
            raw = s[i:j + 1]
            out.append(f'<span class="tex">{html.escape(raw)}</span>')
            i = j + 1
            continue
        if c == "\\":
            m = re.match(r"\\([a-zA-Z]+\*?)", s[i:])
            if not m:
                # an escaped character like \% or \&
                text_buf.append(s[i:i + 2])
                i += 2
                continue
            name = m.group(1)
            j = i + len(m.group(0))
            if name in ("textbackslash", "textasciitilde", "textasciicircum") and s[j:j + 2] == "{}":
                text_buf.append(s[i:j + 2])
                i = j + 2
                continue
            if name in ("textbf", "emph", "textit", "footnote", "url") and j < len(s) and s[j] == "{":
                arg, k = read_group(s, j)
                flush()
                if name == "textbf":
                    out.append(f"<strong>{inline_to_html(arg)}</strong>")
                elif name in ("emph", "textit"):
                    out.append(f"<em>{inline_to_html(arg)}</em>")
                elif name == "footnote":
                    out.append(f'<span class="fn">{inline_to_html(arg)}</span>')
                else:
                    out.append(f'<a href="{html.escape(arg)}">{html.escape(arg)}</a>')
                i = k
                continue
            if name == "href" and j < len(s) and s[j] == "{":
                url, k = read_group(s, j)
                if k < len(s) and s[k] == "{":
                    label, k2 = read_group(s, k)
                    flush()
                    out.append(f'<a href="{html.escape(url)}">{inline_to_html(label)}</a>')
                    i = k2
                    continue
            if name in ("cite", "citep", "citet") and j < len(s) and s[j] == "{":
                keys, k = read_group(s, j)
                flush()
                mode = "t" if name == "citet" else "p"
                out.append(f'<span class="cite" data-keys="{html.escape(keys)}" data-mode="{mode}">[{html.escape(keys)}]</span>')
                i = k
                continue
            # Anything else: keep the command and its arguments verbatim.
            k = j
            while k < len(s) and s[k] in "[{":
                _, k = read_group(s, k, s[k], "]" if s[k] == "[" else "}")
            flush()
            out.append(f'<span class="tex">{html.escape(s[i:k])}</span>')
            i = k
            continue
        text_buf.append(c)
        i += 1
    flush()
    return "".join(out)


def tex_to_html(body):
    lines = body.split("\n")
    blocks, para, i = [], [], 0

    def end_para():
        if para:
            blocks.append(f"<p>{inline_to_html(' '.join(l.strip() for l in para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        st = line.strip()
        if not st:
            end_para()
            i += 1
            continue
        m = re.match(r"%\s*TODO:?\s*(.*)$", st)
        if m:
            end_para()
            blocks.append(f'<p class="todo">{html.escape(m.group(1))}</p>')
            i += 1
            continue
        if st.startswith("%"):
            end_para()
            blocks.append(f'<pre class="tex">{html.escape(line)}</pre>')
            i += 1
            continue
        m = re.match(r"\\(sub)?subsection\*?\{(.*)\}\s*$", st)
        if m:
            end_para()
            tag = "h4" if m.group(1) else "h3"
            blocks.append(f"<{tag}>{inline_to_html(m.group(2))}</{tag}>")
            i += 1
            continue
        m = re.match(r"\\begin\{(itemize|enumerate)\}\s*$", st)
        if m:
            end_para()
            env, items, j = m.group(1), [], i + 1
            nested = False
            while j < len(lines) and not re.match(r"\s*\\end\{" + env + r"\}", lines[j]):
                l = lines[j].strip()
                if l.startswith("\\begin{"):
                    nested = True
                if l.startswith("\\item"):
                    items.append(l[5:].strip())
                elif l and items:
                    items[-1] += " " + l
                j += 1
            if nested:
                raw = "\n".join(lines[i:j + 1])
                blocks.append(f'<pre class="tex">{html.escape(raw)}</pre>')
            else:
                tag = "ul" if env == "itemize" else "ol"
                blocks.append(f"<{tag}>" + "".join(f"<li>{inline_to_html(it)}</li>" for it in items) + f"</{tag}>")
            i = j + 1
            continue
        m = re.match(r"\\begin\{([^}]+)\}", st)
        if m:
            end_para()
            env, j = m.group(1), i
            while j < len(lines) and ("\\end{" + env + "}") not in lines[j]:
                j += 1
            raw = "\n".join(lines[i:j + 1])
            blocks.append(f'<pre class="tex">{html.escape(raw)}</pre>')
            i = j + 1
            continue
        para.append(line)
        i += 1
    end_para()
    return "".join(blocks)


# ---------------------------------------------------------------- HTML -> LaTeX


class Node:
    def __init__(self, tag, attrs=None, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs or {}), parent, []


class TreeBuilder(HTMLParser):
    VOID = {"br", "img", "hr", "input", "meta"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in self.VOID:
            self.cur = node

    def handle_endtag(self, tag):
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def classes(node):
    return set((node.attrs.get("class") or "").split())


def text_of(node):
    if isinstance(node, str):
        return node
    if node.tag == "br":
        return "\n"
    return "".join(text_of(c) for c in node.children)


def inline_to_tex(nodes):
    out = []
    for n in nodes:
        if isinstance(n, str):
            out.append(escape_text(re.sub(r"\s+", " ", n)))
            continue
        cl = classes(n)
        if n.tag == "span" and "cite" in cl:
            keys = (n.attrs.get("data-keys") or "").strip()
            if keys:
                out.append(("\\citet{" if n.attrs.get("data-mode") == "t" else "\\citep{") + keys + "}")
        elif n.tag == "span" and "tex" in cl:
            out.append(text_of(n))
        elif n.tag == "span" and "fn" in cl:
            out.append("\\footnote{" + inline_to_tex(n.children).strip() + "}")
        elif n.tag in ("strong", "b"):
            inner = inline_to_tex(n.children)
            out.append("\\textbf{" + inner + "}" if inner.strip() else inner)
        elif n.tag in ("em", "i"):
            inner = inline_to_tex(n.children)
            out.append("\\emph{" + inner + "}" if inner.strip() else inner)
        elif n.tag == "a":
            href = n.attrs.get("href") or ""
            label = inline_to_tex(n.children)
            out.append("\\url{" + href + "}" if label.strip() in ("", escape_text(href)) else "\\href{" + href + "}{" + label + "}")
        elif n.tag == "br":
            out.append(" ")
        else:
            out.append(inline_to_tex(n.children))
    return "".join(out)


def html_to_tex(fragment):
    tb = TreeBuilder()
    tb.feed(fragment or "")
    blocks, loose = [], []

    def flush_loose():
        text = inline_to_tex(loose).strip()
        if text:
            blocks.append(split_sentences(text))
        loose.clear()

    for n in tb.root.children:
        if isinstance(n, str) or n.tag in ("strong", "b", "em", "i", "a", "span", "br"):
            if isinstance(n, Node) and n.tag == "span" and "tex" in classes(n):
                loose.append(n)
            else:
                loose.append(n)
            continue
        flush_loose()
        cl = classes(n)
        if n.tag == "pre" and "tex" in cl:
            raw = text_of(n).rstrip("\n")
            if raw.strip():
                blocks.append(raw)
        elif n.tag == "p" and "todo" in cl:
            t = re.sub(r"\s+", " ", text_of(n)).strip()
            if t:
                blocks.append("% TODO: " + t)
        elif n.tag in ("h1", "h2", "h3"):
            t = inline_to_tex(n.children).strip()
            if t:
                blocks.append("\\subsection{" + t + "}")
        elif n.tag in ("h4", "h5", "h6"):
            t = inline_to_tex(n.children).strip()
            if t:
                blocks.append("\\subsubsection{" + t + "}")
        elif n.tag in ("ul", "ol"):
            env = "itemize" if n.tag == "ul" else "enumerate"
            items = [inline_to_tex(li.children).strip() for li in n.children if isinstance(li, Node) and li.tag == "li"]
            items = [it for it in items if it]
            if items:
                blocks.append("\\begin{" + env + "}\n" + "\n".join("  \\item " + it for it in items) + "\n\\end{" + env + "}")
        else:  # p, div, anything else: a paragraph
            t = inline_to_tex(n.children).strip()
            if t:
                blocks.append(split_sentences(t))
    flush_loose()
    # Consecutive TODO notes and raw comment lines stay together without blank lines.
    out = []
    for b in blocks:
        if out and b.startswith("%") and out[-1].startswith("%") and "\n" not in out[-1]:
            out[-1] += "\n" + b
        else:
            out.append(b)
    return "\n\n".join(out) + ("\n" if out else "")


def section_tex(title, body_html):
    return "\\section{" + escape_text(title.strip() or "Untitled") + "}\n\n" + html_to_tex(body_html)


# ---------------------------------------------------------------- bibliography


def _ascii(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def cite_keys(sources):
    """Stable citation keys for the literature list: surname + year + first title word."""
    keys, used = {}, set()
    stop = {"a", "an", "the", "of", "on", "in", "for", "and", "to", "with", "is", "are", "can", "do", "how", "what", "why", "from"}
    for s in sources:
        sur = _ascii(s.get("surname") or s.get("short") or s.get("title", "x")).lower()
        sur = re.sub(r"[^a-z]", "", sur) or "anon"
        words = [w for w in re.findall(r"[a-z0-9]+", _ascii(s.get("title", "")).lower()) if w not in stop]
        base = f"{sur}{s.get('year') or 'nd'}{words[0] if words else ''}"
        key, n = base, 1
        while key in used:
            n += 1
            key = f"{base}{chr(96 + n)}"
        used.add(key)
        keys[s["id"]] = key
    return keys


def bib_authors(authors):
    a = authors.strip()
    if not a:
        return ""
    many = "et al" in a
    a = re.sub(r",?\s*et al\.?", "", a).replace(" & ", ", ")
    people = re.findall(r"\s*([^,]+?),\s*((?:[A-Z][a-z]?\.?\s?-?)+)(?=,|$)", a)
    if people:
        names = [f"{p.strip()}, {i.strip()}" for p, i in people]
        if many:
            names.append("others")
        return " and ".join(names)
    return "{" + a.strip() + "}" + (" and others" if many else "")


def bib_entry(key, s):
    def f(v):
        return v.replace("{", "").replace("}", "")
    fields = [("author", bib_authors(s.get("authors", ""))), ("title", "{" + f(s.get("title", "")) + "}")]
    if s.get("year"):
        fields.append(("year", str(s["year"])))
    venue = s.get("venue") or {"peer": "", "preprint": "Preprint", "WP": "Working paper", "book": "", "grey": "Online"}.get(s.get("type"), "")
    if venue:
        fields.append(("howpublished", f(venue)))
    url = s.get("url") or ""
    m = re.match(r"https?://doi\.org/(.+)", url)
    if m:
        fields.append(("doi", m.group(1)))
    elif url:
        fields.append(("url", url))
    body = ",\n".join(f"  {k} = {{{v}}}" for k, v in fields if v)
    return f"@misc{{{key},\n{body}\n}}\n"


def write_bib(sources, keys):
    out = ["% Generated by thesis/sync.py from docs/literature-sources.md. Do not edit by hand:",
           "% fix the entry in the literature list instead. Entries are rough and need checking before hand-in.\n"]
    for s in sources:
        out.append(bib_entry(keys[s["id"]], s))
    path = THESIS / "references.bib"
    text = "\n".join(out)
    changed = not path.exists() or path.read_text(encoding="utf-8") != text
    path.write_text(text, encoding="utf-8")
    return changed


def load_sources():
    sys.path.insert(0, str(ROOT / "overview"))
    import build  # noqa: E402  (overview/build.py)
    return build.parse_literature()["sources"]


# ---------------------------------------------------------------- chapter files


def write_chapter_files():
    """chapters/<key>/_chapter.tex and chapters.tex follow the files on disk."""
    changed = False
    inputs = []
    for cdir in sorted(p for p in CHAPTERS.iterdir() if p.is_dir()):
        title_file = cdir / "_title.txt"
        title = title_file.read_text(encoding="utf-8").strip() if title_file.exists() else cdir.name
        secs = sorted(f for f in cdir.glob("*.tex") if not f.name.startswith("_"))
        text = "% Generated by thesis/sync.py. Section order follows the file names.\n"
        text += "\\chapter{" + escape_text(title) + "}\n" + "".join(
            "\\input{chapters/" + cdir.name + "/" + f.stem + "}\n" for f in secs
        )
        path = cdir / "_chapter.tex"
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
            changed = True
        inputs.append("\\input{chapters/" + cdir.name + "/_chapter}")
    text = "% Generated by thesis/sync.py.\n" + "\n".join(inputs) + "\n"
    path = THESIS / "chapters.tex"
    if not path.exists() or path.read_text(encoding="utf-8") != text:
        path.write_text(text, encoding="utf-8")
        changed = True
    return changed


# ---------------------------------------------------------------- export


def load_collection(db_dir, name):
    d = Path(db_dir) / name
    out = {}
    if d.exists():
        for f in d.glob("*.json"):
            try:
                out[f.stem] = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return out


SID_RE = re.compile(r"^(\d\d-[a-z0-9-]+)\.(\d\d-[a-z0-9-]+)$")


def export(db_dir, out_dir):
    drafts = load_collection(db_dir, "drafts")
    receipts = load_collection(db_dir, "receipts")
    latest = {}
    for r in receipts.values():
        sid = r.get("sid")
        if sid and (sid not in latest or r.get("rev", 0) > latest[sid].get("rev", 0)):
            latest[sid] = r

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    written, deleted, conflicts, skipped, writes, editors = [], [], [], [], [], set()
    for sid, d in sorted(drafts.items()):
        rev = int(d.get("rev") or 0)
        last = latest.get(sid)
        if last and int(last.get("rev") or 0) >= rev:
            continue  # nothing new since the last sync
        m = SID_RE.match(sid)
        if not m or not (CHAPTERS / m.group(1)).is_dir():
            skipped.append(sid)
            continue
        path = CHAPTERS / m.group(1) / (m.group(2) + ".tex")
        current = file_hash(path)
        base_ok = current == d.get("baseHash") or (last and current == last.get("repoHash"))
        if d.get("deleted"):
            new_text = None
        else:
            new_text = section_tex(d.get("title", ""), d.get("html", ""))
        already = (new_text is None and not path.exists()) or (
            new_text is not None and path.exists() and path.read_text(encoding="utf-8") == new_text
        )
        receipt = {"sid": sid, "rev": rev, "at": now}
        if already:
            receipt["repoHash"] = file_hash(path)
        elif not base_ok:
            receipt.update({"conflict": True, "repoHash": current})
            conflicts.append(sid)
        elif new_text is None:
            path.unlink()
            receipt["repoHash"] = "none"
            deleted.append(sid)
        else:
            path.write_text(new_text, encoding="utf-8")
            receipt["repoHash"] = file_hash(path)
            written.append(sid)
        if d.get("by"):
            editors.add(d["by"])
        writes.append({"op": "set", "collection": "receipts", "doc_id": f"{sid}~{rev}", "data": receipt})

    chapters_changed = write_chapter_files()
    sources = load_sources()
    bib_changed = write_bib(sources, cite_keys(sources))

    changed = written or deleted
    msg = ""
    if changed:
        # {editors} is replaced with names by whoever runs the sync (the page stores
        # only account ids, which the routine resolves with ArtifactData "profiles").
        msg = "Edited on the hub by {editors}: " + ", ".join(written + deleted)
        if len(msg) > 200:
            msg = "Edited on the hub by {editors}: " + f"{len(written) + len(deleted)} sections"
    elif chapters_changed or bib_changed:
        msg = "Regenerate thesis chapter list and bibliography"

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "commit-message.txt").write_text(msg + "\n\nSynced by thesis/sync.py\n" if msg else "", encoding="utf-8")
    if writes:
        writes.append({"op": "set", "collection": "receipts", "doc_id": "run~" + re.sub(r"[^0-9T]", "", now),
                       "data": {"run": True, "at": now, "written": len(written), "deleted": len(deleted), "conflicts": len(conflicts)}})
    (out / "receipts.json").write_text(json.dumps(writes, ensure_ascii=False, indent=1), encoding="utf-8")
    report = {"written": written, "deleted": deleted, "conflicts": conflicts, "skipped": skipped,
              "commit": bool(msg), "editorIds": sorted(editors), "receiptCount": len(writes)}
    print(json.dumps(report, ensure_ascii=False))
    return report


def check():
    bad = 0
    for ch in list_sections():
        for s in ch["sections"]:
            title, body = split_section(s["tex"])
            again = section_tex(title, tex_to_html(body))
            if again != s["tex"]:
                bad += 1
                print(f"Would change: {s['file']}")
    print("All sections round-trip unchanged." if not bad else f"{bad} section(s) would be reformatted by the hub.")
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("export")
    e.add_argument("--db", required=True)
    e.add_argument("--out", required=True)
    sub.add_parser("check")
    args = ap.parse_args()
    if args.cmd == "export":
        export(args.db, args.out)
    else:
        sys.exit(1 if check() else 0)


if __name__ == "__main__":
    main()
