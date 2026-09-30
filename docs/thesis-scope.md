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

## Plan for October — first draft by 31 October

A first version of the plan, as shown in the week 40 slides. One focus per week, nothing overlapping,
so it is easy to see whether we are on track:

| Week | Focus | Done by the end of the week |
|---|---|---|
| 40 (28 Sep) | Scope, outline and literature review | Outline and literature review drafted |
| 41 (5 Oct) | Chapter 3: the Global Gas Model | Chapter 3 drafted |
| 42 (12 Oct) | Chapter 4: LLM agents | Chapter 4 drafted |
| 43 (19 Oct) | Chapter 5: where AI fits | Chapter 5 drafted |
| 44 (26 Oct) | Closing chapters and introduction | First full draft, 31 October |

Reading it through and sending it to the supervisors comes after this plan ends.

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
- Chapters 6–8 (design sketch, discussion, conclusion) — proposed, not yet confirmed by supervisors
- The format of chapter 5's summary figure
- Final hand-in dates for both theses — not yet recorded here
