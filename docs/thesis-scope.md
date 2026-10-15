# Thesis scope and phasing

What this project actually is, what stage it's at, and what that means for the work.

*Written 2026-09-15 from Jørgen's description. Scope is still being negotiated with supervisors —
items marked **(open)** are not settled.*

---

## Two theses, not one

| | Project thesis | Master's thesis |
|---|---|---|
| **When** | Autumn 2026 — current | Spring 2027 |
| **Nature** | Exploration and argument | Implementation |
| **Deliverable** | A written thesis | Working agent system + thesis |
| **Code** | None — no proof of concept this semester | The main contribution |

The two are continuous — the project thesis is groundwork that the master's builds on. But they have
different outputs, and conflating them leads to premature engineering.

## What the project thesis is

An **exploratory argument**, not a build. The thesis being advanced is roughly:

> There is potential to use LLM-based agents to automate parts of the workflow around the Global Gas
> Model — scenario generation, parameter curation, result interpretation, validation.

The work is establishing *whether* that is true, *where* it is true, and *what it would take* — not
doing it yet. Success is a well-argued, well-evidenced case, not running software.

The contribution is **a broad map of how and where AI can be used across the GGM workflow**, written
so that it can serve as the starting point for building the agents in the master's thesis.

## Known structure

Four sections are settled, in this order after the introduction. The rest is **(open)** and being
worked out with supervisors. Full proposal: [`project-thesis-structure.md`](project-thesis-structure.md).

### Literature review — chapter 2

Settled by supervisor feedback (recorded 2026-09-30): its own chapter, placed directly after the
introduction. It covers what has been done with agents on large domain models and ends by stating
the gap this thesis addresses — which the following chapters then answer.

Because it now comes *before* the GGM chapter, it has to be readable with only the introduction's
short sketch of the model. Candidates and the gap argument are in
[`project-thesis-structure.md` §3](project-thesis-structure.md#3-literature-review--candidates).

### The Global Gas Model — chapter 3

The reader cannot be assumed to know what GGM is. This section has to explain it from scratch: what
the model does, how it is structured, what the workflow around it looks like, and — critically —
where that workflow is *effortful*, since that is what motivates the rest of the thesis.

Source material: [`ggm-model.md`](ggm-model.md) and [`ggm-documentation-v3.0.pdf`](ggm-documentation-v3.0.pdf).
The calibration discussion (PDF pp. 28–32) is especially relevant — the documentation states plainly
that calibration takes an experienced analyst days to weeks. That is the strongest available evidence
that there is real manual burden worth automating.

### AI agents — chapter 4

A **general** chapter on LLMs and agents — it does not need to tie every point back to GGM, since
chapter 5 does that. Where the literature review has covered something, cite back to it. Current
thinking on what it covers:

- What agents are, and how they differ from a single prompt
- What LLMs are good and bad at
- Which models to use, and what they cost
- **Which kinds of tasks suit an LLM, and which are better as ordinary code** — chapter 5 builds on
  this at each step of the workflow

### Where AI fits — chapter 5

Approach agreed 2026-09-30: a general, step-by-step walk through the GGM workflow — get source data,
prepare it, set up the scenario, calibrate, run, read the results — asking of each step what happens
today, what it needs, what an agent could do, and where a person stays involved. Short examples from
the 2023 data as evidence; a summary figure (format open) and a job description per proposed agent at
the end. Details in
[`project-thesis-structure.md`](project-thesis-structure.md#5-where-ai-fits-in-the-ggm-workflow).

### Proof of concept — not this semester

Dropped from the project thesis on 2026-09-30 and left for the master's. A starting idea for spring
is kept in [`project-thesis-structure.md` §6](project-thesis-structure.md#6-proof-of-concept--left-for-the-masters-thesis).

---

## Plan — hand-in 13 December

Revised 2026-10-05 (slides: `supervisor-meetings/week41-revised-plan.pptx`). The week 40 plan gave
each chapter one week and aimed for a draft by 31 October; that was too tight. Now each chapter gets
about two weeks, consecutive chapters overlap by a week (one is being finished while the next is
started), and chapter 5 — the core — gets three. The literature review comes first: it sets out the
gap chapters 3–5 answer, and chapter 4 cites back to it. The introduction is written last.

| Weeks | Focus | Done by the end |
|---|---|---|
| 40 (28 Sep) | Scope and outline | Outline done |
| 41–42 | Chapter 2: literature review | Chapter 2 drafted |
| 42–43 | Chapter 3: the Global Gas Model | Chapter 3 drafted |
| 43–44 | Chapter 4: LLM agents | Chapter 4 drafted |
| 45–47 | Chapter 5: where AI fits | Chapter 5 drafted |
| 47–48 | Chapter 6: discussion and conclusion | — |
| 48 | Introduction and abstract | Full draft to supervisors, 29 November |
| 49–50 | Supervisor feedback, revise, hand in | **Hand-in, 13 December** |

Hand-in date 13 December as stated by Jørgen (2026-10-05).

## Length targets

*Set 2026-10-15.* A first full draft of chapters 1–2 came to 24 pages, which projected to over 100
pages for the whole thesis — master's-thesis length. These targets keep it to about **36 pages of main
text** (roughly 45 with front matter and bibliography). IØT publishes no page limit for TIØ4500, so
**confirm with Franziska** ([question 7](questions-for-weekly-meeting.md)).

Words per page are measured, not guessed: the current LaTeX layout (`report`, 11pt, A4) gives about
**390 words per page** without citations and about **380 with author-year citations**. Check a chapter with `tectonic` or by counting words before calling it done.

| Chapter | Pages | Words | Sources | Note |
|---|---|---|---|---|
| 1 Introduction | 3 | ~950–1,150 | ~10 | Written: 950 words, 7 sources, 3 pages |
| 2 Literature review | 5 | ~1,900–2,000 | ~20–25 | Written: 1,910 words, 24 sources, 5 pages. Breadth lives in `literature-sources.md`, not in the chapter |
| 3 The Global Gas Model | 5 | ~1,700 + table | ~12 | Drafted 2026-10-15: 1,690 words, 12 sources, 5 pages. Only what chapters 5–6 need; details stay in `ggm-model.md` |
| 4 LLM agents | 7 | ~2,700 | | Deliberately longer than chapter 3: central to the argument |
| 5 Where AI fits | 12 | ~4,700 | | The core — about a third of the thesis |
| 6 Discussion and conclusion | 4 | ~1,550 | | Merges the earlier chapters 6–8 |
| **Main text** | **36** | **~14,000** | | |

**Section budgets for the written chapters** (words): introduction — problem 450, research question
150, scope 150, GGM in brief 250, contribution and structure 200. Literature review — approach 250,
setting up and running models 350, calibration 600, energy and economic models 250, dividing the work
250, gap 450.

**Rules of thumb for writing to length**

- Decide what is *must-have* (carries the argument) before writing; *nice-to-have* material goes to
  the working docs, where it is not lost.
- A source earns a place in the thesis by backing a specific claim, not by showing breadth.
- No summary subsections inside a 5-page chapter; the last section does that job.
- If a chapter runs over by more than about 20%, cut before moving on — the overrun compounds.

**Sources cut from chapter 2 that later chapters should pick up** (2026-10-15). They were dropped for
length, not because they are wrong; each backs a specific point elsewhere:

| Chapter | Sources | For |
|---|---|---|
| 3 GGM | Holz (2015); Holz, von Hirschhausen & Kemfert (2008, GASMOD); Gabriel et al. (2005); Silvast et al. (2020); Süsser et al. (2021) | The model's lineage, and the judgment in energy-modelling practice |
| 4 LLM agents | Wang et al. (2024); Schluntz & Zhang (2024); Majumder et al. (2024); Hu et al. (2025); Rojas et al. (2026); Korinek (2023, 2025); Kapoor et al. (2024) | What an agent is, workflows versus agents, energy-specific limits, "the solver computes", agents for economists, cost |
| 5 Where AI fits | Eloundou et al. (2024); Dell'Acqua et al. (2026); Autor, Levy & Murnane (2003) | The task-by-task method of the chapter |
| 5 (read the results) | Forootani et al. (2025, RE-LLM); Li et al. (2026, OptArgus) | Explaining results; a close fit is not a correct model |
| 6 Discussion | Parasuraman & Manzey (2010); Kydland & Prescott (1996); Kennedy & O'Hagan (2001) | Automation bias at human gates; calibration as method |

---

## What this means for how we work

- **The output is prose and analysis, not production code.** Depth of understanding and clarity of
  explanation matter more than architecture.
- **Don't build ahead of the argument.** Infrastructure that would be right for the master's thesis
  is premature now. If code is written this semester it should be illustrative and disposable.
- **The real 2023 input data arrived on 2026-09-30** ([`ggm-data-2023.md`](ggm-data-2023.md)). This
  semester it is useful for describing the model accurately and for putting numbers on the
  calibration burden. Running the model is still for spring.
- **Citations matter more than usual.** The literature review is now chapter 2 — the first
  substantive chapter a reader meets, so it sets the tone for everything after it. Worth accumulating
  sources as we go rather than reconstructing them at the end.
- **Understanding GGM deeply is directly productive**, not preparation for productive work. It feeds
  the GGM chapter directly and grounds the walk-through in chapter 5. The point is to understand how
  the model and its configuration *work* — well enough to design agents — not to audit the values.

## Open items

- Precise scope and research question — in discussion with supervisors
- Chapter 6 (discussion and conclusion, merging the earlier proposed chapters 6–8 on 2026-10-15) — not yet confirmed by supervisors
- Expected length of the project thesis — targets below assume about 36 pages of main text; confirm with Franziska
- The format of chapter 5's summary figure
- Final hand-in date for the master's thesis — not yet recorded here
