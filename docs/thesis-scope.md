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
| **Code** | None required; small proof of concept possible | The main contribution |

The two are continuous — the project thesis is groundwork that the master's builds on. But they have
different outputs, and conflating them leads to premature engineering.

## What the project thesis is

An **exploratory argument**, not a build. The thesis being advanced is roughly:

> There is potential to use LLM-based agents to automate parts of the workflow around the Global Gas
> Model — scenario generation, parameter curation, result interpretation, validation.

The work is establishing *whether* that is true, *where* it is true, and *what it would take* — not
doing it yet. Success is a well-argued, well-evidenced case, not running software.

## Known structure

Two sections are certain. The rest **(open)** and being worked out with supervisors.

### 1. The Global Gas Model

The reader cannot be assumed to know what GGM is. This section has to explain it from scratch: what
the model does, how it is structured, what the workflow around it looks like, and — critically —
where that workflow is *effortful*, since that is what motivates the rest of the thesis.

Source material: [`ggm-model.md`](ggm-model.md) and [`ggm-documentation-v3.0.pdf`](ggm-documentation-v3.0.pdf).
The calibration discussion (PDF pp. 28–32) is especially relevant — the documentation states plainly
that calibration takes an experienced analyst days to weeks. That is the strongest available evidence
that there is real manual burden worth automating.

### 2. AI agents

Current thinking on what this covers:

- Why agents are a plausible fit for this problem specifically
- Which models, and on what basis to choose
- Token usage and cost analysis
- **Which tasks genuinely suit an LLM, and which are better as ordinary code** — this looks like the
  most substantive contribution of the section. It is a real question with a non-obvious answer, and
  answering it well requires understanding both the model and the tooling.

### 3. Proof of concept **(open)**

Possible, not committed. If it happens, deliberately small: agents against a very simple
configuration, or against one part of a configuration — enough to demonstrate feasibility, not to be
a working system.

---

## What this means for how we work

- **The output is prose and analysis, not production code.** Depth of understanding and clarity of
  explanation matter more than architecture.
- **Don't build ahead of the argument.** Infrastructure that would be right for the master's thesis
  is premature now. If code is written this semester it should be illustrative and disposable.
- **Real GGM input data is not urgent this semester.** It is needed for the master's, and would help
  a proof of concept, but exploration does not require a full calibrated dataset. This revises an
  earlier assessment made before the two-phase structure was known.
- **Citations matter more than usual.** A thesis needs a literature base — on gas market modelling,
  on LLM agents, on automation of scientific workflows. Worth accumulating as we go rather than
  reconstructing at the end.
- **Understanding GGM deeply is directly productive**, not preparation for productive work. It feeds
  section 1 and grounds the task-suitability analysis in section 2.

## Open items

- Precise scope and research question — in discussion with supervisors
- Whether a proof of concept is in scope, and how small
- Full thesis structure beyond the two known sections
- Deadlines for both theses — not yet recorded here
