"""Build the data file behind the project overview page.

Reads the repo's own documents and git history and writes
overview/data/overview.json. The page (overview/index.html) renders only
what this file contains, so the repo stays the single source of truth:
edit the docs, rerun this script, republish the page.

    python3 overview/build.py

What it reads:
    docs/literature-sources.md          -> sources, sections, relations
    docs/thesis-scope.md                -> timeline (the plan table)
    docs/project-thesis-structure.md    -> the argument and chapter list
    docs/workflow-task-inventory.md     -> workflow steps and stage verdicts
    docs/questions-for-weekly-meeting.md-> open, parked and resolved questions
    docs/README.md                      -> document index and filing rules
    agents/registry.json (optional)     -> agents, once there are any
    git ls-files / git log              -> file tree, last change per file

Nothing from data_2023/ is read or copied: the folder is summarised by
file count only, because the data is licensed.
"""

import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "overview" / "data" / "overview.json"

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CHAPTER_NAMES = {
    "1": "Introduction",
    "2": "Literature review",
    "3": "The Global Gas Model",
    "4": "LLM agents",
    "5": "Where AI fits",
    "6": "Design sketch",
    "7": "Discussion",
    "8": "Conclusion",
    "M": "Master's thesis",
}
# Keyword -> chapter-5 workflow step. Matched against a source's "use" text.
STEP_KEYWORDS = [
    ("source", ["get source data", "extraction from reports", "source reports"]),
    ("prepare", ["prepare the data", "wrangling", "aggregation", "spreadsheet edits", "too big to paste"]),
    ("scenario", ["set up the scenario", "scenario setup", "scenario design", "scenario generation", "narrative"]),
    ("calibrate", ["calibrat", "priors"]),
    ("run", ["run the model", "infeasible", "pre-run", "debugging"]),
    ("results", ["read the results", "explain", "results"]),
]


# ---------------------------------------------------------------- helpers


def read(path):
    return path.read_text(encoding="utf-8")


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def strip_md(text):
    """Markdown cell -> plain text (links keep their label)."""
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = text.replace("`", "")
    return re.sub(r"\s+", " ", text).strip()


def md_inline(text):
    """Markdown cell -> a small, safe HTML subset (bold, italic, code, links)."""
    out = (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.startswith("http"):
            return f'<a href="{href}" target="_blank" rel="noopener">{label}</a>'
        return f"<span class=\"repo-ref\" title=\"{href}\">{label}</span>"

    out = LINK_RE.sub(link, out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


def table_rows(lines):
    """Yield the cells of each body row in a markdown table."""
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # drop the header row


def split_sections(text, level):
    """Split markdown into (heading, body) at the given heading level."""
    marker = "#" * level + " "
    parts, current, body = [], None, []
    for line in text.splitlines():
        if line.startswith(marker):
            if current is not None:
                parts.append((current, body))
            current, body = line[len(marker):].strip(), []
        elif current is not None:
            body.append(line)
    if current is not None:
        parts.append((current, body))
    return parts


# ---------------------------------------------------------------- sources


def parse_source_cell(cell):
    links = [{"label": strip_md(l), "url": u} for l, u in LINK_RE.findall(cell)]
    plain = strip_md(cell)
    year_m = re.search(r"\((\d{4})", plain)
    year = int(year_m.group(1)) if year_m else None
    authors, title = "", ""
    if year_m:
        authors = plain[: year_m.start()].strip().rstrip(".")
        rest = plain[plain.find(")", year_m.start()) + 1:].lstrip(". ").strip()
        # A linked title (grey literature) is the first link's label.
        first_link = LINK_RE.search(cell[cell.find(")", cell.find("(" + str(year))):])
        if first_link and rest.startswith(strip_md(first_link.group(1))):
            title = strip_md(first_link.group(1))
        else:
            title = re.split(r"\.\s|\s(?=arXiv:)|\s·\s", rest, maxsplit=1)[0]
    else:
        title = links[0]["label"] if links else plain
        authors = ""
    title = title.strip().rstrip(".")
    url = next((l["url"] for l in links if l["url"].startswith("http")), "")
    return {
        "authors": authors,
        "year": year,
        "title": title,
        "citation": plain,
        "citationHtml": md_inline(cell),
        "links": links,
        "url": url,
    }


GENERIC_HANDLES = {"Human", "Global Gas Model", "The World Gas Model", "From transformers to LLMs", "LLM-based multi-agents"}


def short_name(title, authors):
    """A recognisable handle: a named system if the title has one."""
    m = re.search(r"\(([A-Z][\w-]+(?:-[\w]+)?)\)", title)
    if m and m.group(1) not in GENERIC_HANDLES:
        return m.group(1)
    if ":" in title:
        head = title.split(":")[0].strip()
        if head not in GENERIC_HANDLES and len(head) <= 28 and (
            any(c.isupper() for c in head[1:]) or len(head.split()) <= 3
        ):
            return head
    return ""


STOP = set("""a an the and or of in on for to with by from as at is are be not this that it its into
than over under via using use used our we they their there these those what which who how when
where why can could would should will may also more most less only one two three new based towards toward
ch ch2 ch3 ch4 ch5 ch6 ch7 ch8 thesis chapter chapters cite cited citing paper papers source sources
line one optional useful already list old""".split())


def words(text):
    return [w for w in re.findall(r"[a-z][a-z0-9-]{2,}", text.lower()) if w not in STOP]


def similarity_edges(sources, exclude, per_node=3, threshold=0.14):
    """Computed links: TF-IDF cosine over title, 'covers' and 'use' text."""
    import math
    docs = [words(" ".join([s["title"], s["covers"], s["use"]])) for s in sources]
    df = {}
    for d in docs:
        for w in set(d):
            df[w] = df.get(w, 0) + 1
    n = len(docs)
    vecs = []
    for d in docs:
        tf = {}
        for w in d:
            tf[w] = tf.get(w, 0) + 1
        v = {w: (c / len(d)) * math.log(n / df[w]) for w, c in tf.items() if df[w] > 1}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({w: x / norm for w, x in v.items()})
    pairs = {}
    for i in range(n):
        scores = []
        for j in range(n):
            if i == j:
                continue
            a, b = vecs[i], vecs[j]
            if len(a) > len(b):
                a, b = b, a
            sim = sum(x * b.get(w, 0.0) for w, x in a.items())
            if sim >= threshold:
                scores.append((sim, j))
        for sim, j in sorted(scores, reverse=True)[:per_node]:
            key = tuple(sorted((sources[i]["id"], sources[j]["id"])))
            if key in exclude:
                continue
            pairs[key] = max(pairs.get(key, 0), sim)
    return [{"a": a, "b": b, "kind": "similar", "score": round(sc, 3)} for (a, b), sc in sorted(pairs.items())]


def first_surname(authors):
    a = re.split(r"[,&(]| et al", authors)[0].strip()
    return a.split()[-1] if a else ""


def parse_type(cell):
    t = strip_md(cell).lower()
    venue = ""
    m = re.search(r"\(([^)]+)\)", strip_md(cell))
    if m:
        venue = m.group(1)
    for key in ("preprint", "peer", "book", "wp", "grey"):
        if t.startswith(key):
            return ("WP" if key == "wp" else key), venue
    return "peer", venue


def chapters_in(text):
    found = {d for d in re.findall(r"\b[Cc]h(\d)", text)}
    if re.search(r"[Mm]aster's", text):
        found.add("M")
    return found


def section_chapters_in(text):
    """'For chapter 2' / 'chapters 5, 6 and 7' in a section intro."""
    found = set()
    for m in re.finditer(r"chapters?\s+(\d+(?:\s*(?:,|and)\s*\d+)*)", text, re.I):
        found |= set(re.findall(r"\d", m.group(1)))
    if re.search(r"master's", text, re.I):
        found.add("M")
    return found & set(CHAPTER_NAMES)


def steps_in(text):
    low = text.lower()
    return [step for step, words in STEP_KEYWORDS if any(w in low for w in words)]


def parse_literature():
    text = read(DOCS / "literature-sources.md")
    sections, sources = [], []
    reading_list = []

    # The "read these first" table: rank -> names mentioned.
    for heading, body in split_sections(text, 2):
        if heading.startswith("The short version"):
            for cells in table_rows(body):
                if len(cells) >= 3:
                    reading_list.append(
                        {"rank": int(cells[0]), "label": strip_md(cells[1]), "why": strip_md(cells[2])}
                    )

    for heading, body in split_sections(text, 2):
        m = re.match(r"([A-N])\. (.+)", heading)
        if not m:
            continue
        letter, name = m.groups()
        intro = []
        for line in body:
            if line.startswith("|") or line.startswith("###"):
                break
            if line.strip():
                intro.append(line.strip())
        intro_text = " ".join(intro)
        section_chapters = sorted(section_chapters_in(strip_md(intro_text)))
        sections.append(
            {"id": letter, "name": name, "intro": md_inline(intro_text), "chapters": section_chapters}
        )

        # Sub-headings (### ...) inside section N group its tables.
        groups, current_group, current_lines = [], "", []
        for line in body:
            if line.startswith("### "):
                groups.append((current_group, current_lines))
                current_group, current_lines = line[4:].strip(), []
            else:
                current_lines.append(line)
        groups.append((current_group, current_lines))

        for group, lines in groups:
            header = next((l for l in lines if l.strip().startswith("| Source")), None)
            if not header:
                continue
            ncols = len(header.strip().strip("|").split("|"))
            for cells in table_rows(lines):
                if ncols == 5 and len(cells) >= 5:
                    src_cell, type_cell, covers, use, stars = cells[:5]
                    typ, venue = parse_type(type_cell)
                elif ncols == 4 and len(cells) >= 4:
                    src_cell, covers, use, stars = cells[:4]
                    typ, venue = "grey", ""
                else:
                    continue
                info = parse_source_cell(src_cell)
                key = info["url"] or info["title"]
                sid = hashlib.sha1(key.encode()).hexdigest()[:10]
                chapters = chapters_in(use) | set(section_chapters)
                sources.append(
                    {
                        "id": sid,
                        "section": letter,
                        "group": group,
                        **info,
                        "type": typ,
                        "venue": venue,
                        "covers": strip_md(covers),
                        "coversHtml": md_inline(covers),
                        "use": strip_md(use),
                        "useHtml": md_inline(use),
                        "priority": stars.count("★"),
                        "chapters": sorted(chapters, key=lambda c: (c == "M", c)),
                        "steps": steps_in(use) if "5" in chapters else [],
                        "titleOnly": "(title only)" in covers,
                        "onOldList": "old list" in use,
                        "short": short_name(info["title"], info["authors"]),
                        "surname": first_surname(info["authors"]),
                    }
                )

    # Relations: a source whose text names another source's handle.
    surname_counts = {}
    for s in sources:
        surname_counts[s["surname"]] = surname_counts.get(s["surname"], 0) + 1
    handles = []
    for s in sources:
        names = set()
        if s["short"] and len(s["short"]) >= 3:
            names.add(s["short"])
        if s["surname"] and len(s["surname"]) >= 5 and surname_counts[s["surname"]] == 1:
            names.add(s["surname"])
        if s["authors"].startswith("METR"):
            names.add("METR")
        if "grey-box" in s["title"].lower():
            names.add("grey-box")
        handles.append((s, names))
    edges = set()
    for s in sources:
        hay = " ".join([s["covers"], s["use"]])
        for other, names in handles:
            if other is s:
                continue
            for n in names:
                if re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", hay):
                    edges.add(tuple(sorted((s["id"], other["id"]))))
    relations = [{"a": a, "b": b, "kind": "mentions"} for a, b in sorted(edges)]
    relations += similarity_edges(sources, exclude=edges)

    # Match each reading-list entry (possibly "A · B") to its best source.
    for item in reading_list:
        ids = []
        for part in item["label"].split(" · "):
            best, best_score = None, 0
            pwords = set(words(part))
            for s in sources:
                score = len(pwords & set(words(s["title"] + " " + s["short"]))) * 2
                score += len(pwords & set(words(s["authors"])))
                if s["year"] and str(s["year"]) in part:
                    score += 2
                if score > best_score:
                    best, best_score = s, score
            if best and best_score >= 3:
                ids.append(best["id"])
        item["ids"] = ids

    # The "not found" list and the gap note, for the gap panel.
    not_found, gap_note = [], ""
    for heading, body in split_sections(text, 2):
        if heading.startswith("What was searched for"):
            for line in body:
                if line.startswith("- "):
                    not_found.append(md_inline(line[2:].strip()))
    for heading, body in split_sections(text, 3):
        if heading.startswith("Note on the gap claim"):
            paras, buf = [], []
            for line in body:
                if line.startswith("---") or line.startswith("## "):
                    break
                if line.strip():
                    buf.append(line.strip())
                elif buf:
                    paras.append(md_inline(" ".join(buf)))
                    buf = []
            if buf:
                paras.append(md_inline(" ".join(buf)))
            gap_note = paras

    return {
        "sections": sections,
        "sources": sources,
        "relations": relations,
        "readingList": reading_list,
        "notFound": not_found,
        "gapNote": gap_note,
    }


# ---------------------------------------------------------------- timeline


def iso_week_monday(year, week):
    return dt.date.fromisocalendar(year, week, 1)


def parse_timeline():
    text = read(DOCS / "thesis-scope.md")
    plan = []
    for heading, body in split_sections(text, 2):
        if not heading.startswith("Plan"):
            continue
        for cells in table_rows(body):
            if len(cells) < 3:
                continue
            weeks = [int(w) for w in re.findall(r"\d{2}", cells[0].split("(")[0])[:2]]
            if not weeks:
                continue
            start_w, end_w = weeks[0], weeks[-1]
            plan.append(
                {
                    "weeks": strip_md(cells[0]),
                    "startWeek": start_w,
                    "endWeek": end_w,
                    "start": iso_week_monday(2026, start_w).isoformat(),
                    "end": (iso_week_monday(2026, end_w) + dt.timedelta(days=6)).isoformat(),
                    "focus": strip_md(cells[1]),
                    "done": strip_md(cells[2]),
                }
            )
    milestones = []
    # The two dates the plan names explicitly.
    if "29 November" in text:
        milestones.append({"date": "2026-11-29", "label": "Full draft to supervisors"})
    if "13 December" in text:
        milestones.append({"date": "2026-12-13", "label": "Hand-in"})
    open_items = []
    for heading, body in split_sections(text, 2):
        if heading.startswith("Open items"):
            open_items = [md_inline(l[2:].strip()) for l in body if l.startswith("- ")]
    return {"plan": plan, "milestones": milestones, "openItems": open_items}


# ---------------------------------------------------------------- structure


def parse_structure():
    text = read(DOCS / "project-thesis-structure.md")
    argument = ""
    m = re.search(r"\*\*The argument, in one sentence:\*\*\s*\n\s*\n> (.+)", text)
    if m:
        argument = strip_md(m.group(1))
    lines = text.splitlines()
    m2 = re.search(r"> (GGM's workflow.+?)\n> (.+?)\n", text)
    if m2:
        argument = strip_md(m2.group(1) + " " + m2.group(2))
    chapters = []
    for heading, body in split_sections(text, 1):
        if heading.startswith("The short version"):
            for cells in table_rows(body):
                if len(cells) >= 3 and cells[0].isdigit():
                    chapters.append({"n": cells[0], "name": strip_md(cells[1]), "line": strip_md(cells[2])})
            break
    decided = []
    for i, line in enumerate(lines):
        if line.strip() == "**Decided:**":
            for l in lines[i + 1:]:
                if l.startswith("- "):
                    decided.append(md_inline(l[2:].strip()))
                elif l.strip() and not l.startswith("- "):
                    break
            break
    return {"argument": argument, "chapters": chapters, "decided": decided}


def parse_workflow():
    text = read(DOCS / "workflow-task-inventory.md")
    step_map, stages = [], []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("| Chapter 5 step"):
            for cells in table_rows(lines[i:]):
                step_map.append({"step": strip_md(cells[0]), "stages": strip_md(cells[1])})
            break
    for heading, body in split_sections(text, 2):
        if heading.startswith("The inventory"):
            for cells in table_rows(body):
                if len(cells) >= 5 and cells[0].isdigit():
                    stages.append(
                        {
                            "n": int(cells[0]),
                            "stage": strip_md(cells[1]),
                            "involves": strip_md(cells[2]),
                            "verdict": strip_md(cells[3]),
                            "why": md_inline(cells[4]),
                        }
                    )
    keys = ["source", "prepare", "scenario", "calibrate", "run", "results"]
    steps = []
    for idx, row in enumerate(step_map):
        nums = [int(n) for n in re.findall(r"(\d+)\s", row["stages"] + " ")]
        steps.append({"key": keys[idx] if idx < len(keys) else f"s{idx}", "name": row["step"], "stages": nums})
    return {"steps": steps, "stages": stages}


def parse_questions():
    text = read(DOCS / "questions-for-weekly-meeting.md")
    out = {"now": [], "parked": [], "resolved": []}
    for heading, body in split_sections(text, 2):
        bucket = (
            "now" if heading.startswith("Now")
            else "parked" if heading.startswith("Parked")
            else "resolved" if heading.startswith("Resolved")
            else None
        )
        if not bucket:
            continue
        for sub, _ in split_sections("\n".join(body), 3):
            out[bucket].append(strip_md(sub))
        if bucket == "parked" and not out["parked"]:
            out["parked"] = [strip_md(m) for m in re.findall(r"^\*\*(.+?)\*\*", "\n".join(body), re.M)]
    return out


def parse_docs_index():
    text = read(DOCS / "README.md")
    docs, rules = [], []
    for heading, body in split_sections(text, 2):
        if heading.startswith("Read in this order"):
            for cells in table_rows(body):
                if len(cells) >= 3:
                    name = strip_md(cells[0])
                    docs.append({"file": "docs/" + name, "what": strip_md(cells[1]), "when": strip_md(cells[2])})
        if heading.startswith("Which file"):
            rules = [md_inline(l[2:].strip()) for l in body if l.startswith("- ")]
    return docs, rules


# ---------------------------------------------------------------- repository


FOLDER_NOTES = {
    "": "Repository root",
    "docs": "Working documents for the project thesis. Start with docs/README.md",
    "ggm": "The Global Gas Model, as a git submodule (fork of Franziska-Holz/GGM_public). Never modified here",
    "data_2023": "The real 2023 input data from the GGM authors. Licensed: private repo only, never copied elsewhere",
    "supervisor-meetings": "Slides shown at supervisor meetings, by week",
    "gdpval-presentation": "The GDPval paper presentation (October 2026) and its sources",
    "overview": "This overview page, its build script and its data",
    "agents": "Agent definitions (none yet)",
    "thesis": "The thesis text in LaTeX, one file per section. Written on the hub and synced here; see thesis/README.md",
}


def parse_repo(docs_index):
    tracked = [p for p in git("ls-files").splitlines() if p]
    describe = {d["file"]: d["what"] for d in docs_index}
    describe.update(
        {
            "CLAUDE.md": "Project instructions: what this is, conventions, where findings go",
            "README.md": "Repository readme with setup steps",
            ".gitmodules": "Points the ggm/ submodule at the GGM fork",
            ".gitignore": "Files git ignores (scratch data in data/, .env)",
            "demo.py": "Early scratch script (disposable)",
            "hello.py": "Early scratch script (disposable)",
        }
    )
    files, data_count = [], 0
    for path in tracked:
        if path.startswith("data_2023/"):
            data_count += 1
            continue
        if path.startswith("ggm/") or path == "ggm":
            continue
        if path.startswith("overview/data/"):
            continue
        if Path(path).name.startswith("~$") or Path(path).name == ".DS_Store":
            continue
        log = git("log", "-1", "--format=%cs%x09%s", "--", path).strip()
        date, _, subject = log.partition("\t")
        files.append(
            {
                "path": path,
                "folder": path.split("/")[0] if "/" in path else "",
                "date": date,
                "subject": subject,
                "what": describe.get(path, ""),
            }
        )
    folders = []
    seen = {f["folder"] for f in files} | {"ggm", "data_2023"}
    for name in sorted(seen, key=lambda n: (n != "", n)):
        folders.append({"name": name, "note": FOLDER_NOTES.get(name, "")})
    commits = []
    for line in git("log", "-25", "--format=%h%x09%cs%x09%an%x09%s").splitlines():
        h, date, author, subject = line.split("\t", 3)
        commits.append({"hash": h, "date": date, "author": author, "subject": subject})
    return {
        "files": files,
        "folders": folders,
        "dataFileCount": data_count,
        "commits": commits,
        "head": git("rev-parse", "--short", "HEAD").strip(),
        "branch": git("rev-parse", "--abbrev-ref", "HEAD").strip(),
    }


def parse_writing(sources):
    """The thesis text in thesis/chapters, its word counts, and how they grew over time."""
    sys.path.insert(0, str(ROOT / "thesis"))
    import sync  # thesis/sync.py

    keys = sync.cite_keys(sources)
    for s in sources:
        s["citeKey"] = keys[s["id"]]
    chapters = sync.list_sections()
    for ch in chapters:
        ch["words"] = sum(sec["words"] for sec in ch["sections"])

    main_tex = (ROOT / "thesis" / "main.tex").read_text(encoding="utf-8")
    def tex_arg(cmd):
        m = re.search(r"\\" + cmd + r"\{([^}]*)\}", main_tex)
        return sync.unescape_text(m.group(1)).replace("\\and", "and").strip() if m else ""

    # Words per chapter at the end of each day that changed the thesis.
    history, seen = [], set()
    log = git("log", "--format=%H%x09%cs", "--", "thesis/chapters").splitlines()
    for line in log:  # newest first
        commit, date = line.split("\t")
        if date in seen:
            continue
        seen.add(date)
        by_chapter = {}
        for path in git("ls-tree", "-r", "--name-only", commit, "thesis/chapters").splitlines():
            name = Path(path).name
            if not name.endswith(".tex") or name.startswith("_"):
                continue
            tex = git("show", f"{commit}:{path}")
            _, body = sync.split_section(tex)
            ch = Path(path).parent.name
            by_chapter[ch] = by_chapter.get(ch, 0) + sync.count_words(body)
        history.append({"date": date, "words": sum(by_chapter.values()), "byChapter": by_chapter})
    history.reverse()
    return {
        "title": tex_arg("title"),
        "author": re.sub(r"\s+", " ", tex_arg("author")),
        "date": tex_arg("date"),
        "chapters": chapters,
        "words": sum(ch["words"] for ch in chapters),
        "history": history,
        "citedKeys": sorted(
            {k.strip() for ch in chapters for sec in ch["sections"]
             for m in re.finditer(r'data-keys="([^"]+)"', sec["html"]) for k in m.group(1).split(",")}
        ),
    }


def parse_agents():
    path = ROOT / "agents" / "registry.json"
    if not path.exists():
        return []
    return json.loads(read(path))


# ---------------------------------------------------------------- main


def main():
    docs_index, filing_rules = parse_docs_index()
    literature = parse_literature()
    data = {
        "builtAt": dt.datetime.now().isoformat(timespec="minutes"),
        "chapterNames": CHAPTER_NAMES,
        "structure": parse_structure(),
        "timeline": parse_timeline(),
        "workflow": parse_workflow(),
        "questions": parse_questions(),
        "literature": literature,
        "writing": parse_writing(literature["sources"]),
        "docsIndex": docs_index,
        "filingRules": filing_rules,
        "repo": parse_repo(docs_index),
        "agents": parse_agents(),
    }
    # A fingerprint of everything except the build time, so a scheduled
    # rebuild can tell whether anything changed since the last publish.
    data["contentHash"] = hashlib.sha1(
        json.dumps({k: v for k, v in data.items() if k != "builtAt"}, sort_keys=True).encode()
    ).hexdigest()[:16]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    lit = data["literature"]
    print(
        f"Wrote {OUT.relative_to(ROOT)}: {len(lit['sources'])} sources in "
        f"{len(lit['sections'])} sections, {len(lit['relations'])} relations, "
        f"{len(data['timeline']['plan'])} plan rows, {len(data['repo']['files'])} files, "
        f"{len(data['agents'])} agents, {data['writing']['words']} thesis words\ncontentHash {data['contentHash']}"
    )


if __name__ == "__main__":
    main()
