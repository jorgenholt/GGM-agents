# Project thesis — proposed structure

A structure to propose to supervisors and argue around, plus the prior work it should sit on.

*Drafted 2026-09-15. Revised 2026-09-30: literature review moved to chapter 2 on supervisor
feedback. Everything else here is still a proposal, not a decision.*

> **On the references:** found by literature search and skimmed, not read in full. Verify every claim
> against the source before citing. Treat this as a reading list with reasons, not a literature review.

---

# The short version

**The argument, in one sentence:**

> GGM's workflow carries a documented expert burden. Some of it suits an LLM agent, some belongs in
> ordinary code, and some should not be automated at all. This thesis works out which is which.

**Six chapters:**

| # | Chapter | In one line |
|---|---|---|
| 1 | Introduction | The problem, the question, and what this thesis does and doesn't do |
| 2 | Literature review | What has been done with agents on large domain models — and the gap left open |
| 3 | The Global Gas Model | What it is, and where the manual work actually goes |
| 4 | LLM agents | What they are good at, what they are bad at |
| 5 | **Where AI fits** | The core chapter — a step-by-step walk through the workflow, and where AI could help at each step |
| 6 | Conclusion | What we'd build in the master's thesis |

No proof of concept this semester — that is left for the master's thesis.

The detailed outline, and the slides shown in week 40, split chapter 6 into three: 6 Design sketch,
7 Discussion, 8 Conclusion and plan for spring.

**Why this order:** chapter 2 places the thesis in the field and ends by stating the gap. Chapters 3
and 4 are the two halves of the problem — the model and the tool. Chapter 5 is where they meet, and
it is the actual contribution. Everything else supports it.

**Still to decide with supervisors:** how narrow the research question should be.

**Decided:**

- The literature review is its own chapter, placed second — supervisor feedback, recorded 2026-09-30.
- No proof of concept this semester; it moves to the master's thesis — our decision, 2026-09-30.
- Chapter 4 is a general chapter on LLMs; the link to GGM is made in chapter 5 — 2026-09-30.
- Chapter 5 is a step-by-step walk through the workflow (details below) — agreed 2026-09-30.

---

*Everything below is supporting detail for the six chapters above. Skip it unless you want the
reasoning or the reading list.*

---

## 1. The argument the thesis should make

Before structure, the spine. A weak version of this thesis says *"AI agents are promising, and GGM
exists, so let's combine them."* A strong version says:

> The GGM workflow contains a documented, substantial expert burden. That burden decomposes into
> tasks with different properties. Some are mechanical and belong in ordinary code. Some require
> judgment over unstructured context and are a genuine fit for an LLM. Some should not be automated
> at all, because the failure mode is a plausible-looking wrong answer. Here is a map of how and where
> AI can be used, and what it implies for the system we build next.

The contribution this semester is **a broad map of how and where AI can be used across the GGM
workflow**, and the reasoning behind it — not just a sorting of tasks into boxes, not enthusiasm, and
not a build. It is meant to be the starting point for building the agents in the master's thesis.

Arguing that parts of the workflow *should not* be automated is what will make this credible rather
than promotional. The GGM documentation hands you the argument: it warns that a wrongly calibrated
model produces biased results that look like market logic (PDF pp. 28–32). That is precisely the
error class an LLM is worst at catching.

---

## 2. Proposed section structure — expanded form

**This is the six-chapter outline above, split finer.** Chapters 6–8 here are what the short version
folds into its chapter 6. Use whichever granularity the supervisors prefer:

| Short version | Expanded form |
|---|---|
| 1 Introduction | 1 Introduction |
| 2 Literature review | 2 Literature review |
| 3 The Global Gas Model | 3 Background: the Global Gas Model |
| 4 LLM agents | 4 LLM agents |
| 5 Where AI fits | 5 Where AI fits in the GGM workflow |
| 6 Conclusion | 6 Design sketch · 7 Discussion · 8 Conclusion |

Chapters 3 and 4 (GGM and LLM agents) are the two Jørgen and Save first identified; chapter 2's
position was set by supervisor feedback. The rest is scaffolding around them.

### 1. Introduction
Problem, research question(s), scope boundary (exploration, not implementation), contribution,
and structure. State plainly that building is the master's thesis — it frames expectations.

**Extra job now that the literature review comes second:** the introduction has to give just enough
GGM for chapter 2 to be readable — a paragraph on what the model is, and why operating it takes
expert effort. The full treatment waits for chapter 3.

### 2. Literature review
Agents applied to configuring, calibrating, and operating large domain models. See §3 of this
document for candidates.

- Organise by *what the agent was asked to do*, not by application domain — it keeps the chapter
  pointed at the problem instead of drifting into an energy-AI survey.
- **Write for a reader who has only had the introduction's sketch of GGM.** Frame the chapter around
  the general problem class; GGM specifics belong in chapter 3.
- **End by stating the gap** (§3, "The gap to claim"). Chapters 3–5 then address it, which gives the
  thesis a clean line: here is the field, here is what's missing, here is how we tackle it.
- Introduce each paper once, here, and cite back to it later. The grey-box calibration paper, for
  instance, matters again in chapter 5 — describe it here, reference it there.

### 3. Background: the Global Gas Model
The reader does not know what GGM is and cannot be assumed to.

- What the model is and what question it answers — partial equilibrium, multi-period, market power
- Structure: nodes, arcs, suppliers, seasons; the LNG and pipeline value chains
- Inputs: the input workbooks and what they contain
- **The workflow around the model** — this is the part that matters, and it is what the documentation
  covers least
- Where the effort goes: calibration takes an experienced analyst days to weeks
  ([`ggm-model.md` §7](ggm-model.md#calibration-effort--citable-evidence-of-manual-burden))
- Read against the gap from chapter 2: make explicit *why* GGM is a case the literature doesn't
  cover — its calibrated parameters are contestable economic judgments, not measurements

Source material is largely assembled in [`ggm-model.md`](ggm-model.md).

### 4. LLM agents: what they are and where they hold up
A **general** chapter on what LLMs and agents are, and what they are good and bad at. It does not
need to tie every point back to GGM — that happens in chapter 5. Where the literature review has
already covered something, cite back to chapter 2 rather than repeating it.

- What distinguishes an agent from a prompt: tool use, iteration, feedback from execution
- What they are good at: reading unstructured documentation, applying written rules of thumb,
  proposing and revising under numeric feedback, explaining their reasoning
- What they are bad at: hallucination, no ground truth about physical reality, weak arithmetic,
  non-determinism, context limits
- Which model to use, and what it costs
- **Which tasks suit an LLM and which are better as ordinary code** — developed here, and used in
  chapter 5 to answer "what could an agent do" at each step

### 5. Where AI fits in the GGM workflow
**The core contribution.** *Approach agreed 2026-09-30.*

Written **generally**, so it holds for any GGM configuration rather than one dataset. The chapter walks
through the workflow from chapter 3 in the order the work happens:

> Get source data → Prepare the data → Set up the scenario → Calibrate → Run the model → Read the
> results

Each step gets the same four questions:

1. **What happens today** — the step as the modellers do it now
2. **What the step needs** — reading, arithmetic, judgment or checking
3. **What an agent could do** — using what chapter 4 sets out
4. **Where a person stays involved** — judgment calls and sign-offs

**Along the way:** short examples from the 2023 data back up the points, so the chapter stays general
without being vague — for example, that restoring the Russian pipelines is a handful of capacity edits
in one sheet, or that a new demand scenario means re-tuning around 1,700 calibrated values. They
illustrate; they are not the backbone.

**At the end:**

- **A figure that sums it up** — where each step lands, from "automate" to "keep with a person".
  *Format not settled.* One candidate is a map with each step placed by how well it suits an LLM
  against how much judgment it needs and how quietly mistakes slip through.
- **A job description for each proposed agent** — what it gets, what it produces, which tools it
  uses, what it must never do (arithmetic in its head, changing calibrated values without sign-off),
  and how you would know it worked. This is the hand-over to the master's thesis.

**Why this approach:** it ties chapters 3 and 4 together one step at a time; it mirrors how the agents
would be built in spring, step by step; and it does not depend on details of the 2023 scenarios that
we don't know yet.

**Considered and set aside:**

- *Rating every task on a set of dimensions* — too granular, and too early to commit to a framework.
- *Using DIW's 2023 variants as case studies* — needs detailed knowledge of those scenarios. The
  variants can still serve as test cases for spring's agents (chapter 6 or 8).
- *Organising the chapter around design decisions and costs* — the most abstract option, resting on
  estimates. A short cost comparison can still be added if there is time.
- *Other layouts for a step-by-step chapter* — a table of steps against properties, or organising by
  kind of input. The walk-through reads most naturally and carries over best to the master's.

### 6. Design sketch for the master's thesis
What a system implied by section 5 would look like — component responsibilities, where humans sit in
the loop, what gets verified and how. A sketch establishing feasibility, not a specification.

### 7. Discussion
Risks, limitations, and what the analysis does not settle. Include what should *not* be automated and
why — this is a feature of the argument, not a hedge.

### 8. Conclusion and plan for the master's thesis
What was established, what remains open, and what spring should build. This section is partly a
project plan, and supervisors will read it as one.

---

## 3. Literature review — candidates

Source material for chapter 2. Three clusters, from closest to your problem outward.

### Closest: agents that configure or calibrate domain models

**[Agentic Calibration of Grey-Box Simulation Models](https://arxiv.org/html/2607.18308v1)** —
the single most relevant find. Uses an LLM as the optimizer in a calibration loop: it receives
parameter bounds with their *meanings*, calibration targets, and the history of guesses with signed
residuals, then proposes a new parameter vector with a written rationale. A harness mediates every
simulation call and checks feasibility, so the LLM never touches the simulation directly.

Why it matters to you: the authors' framing of a "grey-box" problem — model structure interpretable,
joint parameter effects analytically unpredictable, experts able to reason *directionally* from
residuals — is an almost exact description of GGM calibration as the DIW documentation describes it.
Reported results: ~16 evaluations versus 110 for Bayesian optimisation and hundreds to tens of
thousands for Nelder–Mead. Limitations they report (no convergence guarantees, reproducibility
dependent on backend determinism, reliance on domain knowledge from pretraining) are directly
transferable as risks to your discussion.

**[AutoSAM](https://arxiv.org/pdf/2603.24736)** — multi-agent generation of input files for a large
simulation code, using retrieval over mixed-format documentation, with a dedicated validation agent
checking schema, parameter dependencies and ranges *before* execution. The structural analogue to
generating GGM workbooks. Read it directly — verify the domain and details yourself.

**[Automated building energy modeling / EnergyPlus multi-agent](https://www.cell.com/iscience/fulltext/S2589-0042(25)02128-5)**
— agents transforming descriptions into runnable models for another configuration-heavy engineering
tool. Useful as evidence the pattern generalises beyond one domain.

### Middle: LLMs formulating and verifying optimisation models

**[OptiMUS](https://arxiv.org/abs/2310.06116)** — LLM agent that formulates MILPs from natural
language, writes and debugs solver code, and checks solution validity. Established enough to be a
standard reference point, with the NLP4LP benchmark.

**[Chain-of-Experts](https://arxiv.org/pdf/2407.19633)** — multi-agent operations-research framework
with a conductor coordinating specialists for terminology, modelling, programming and review. A
concrete architecture to compare your design sketch against.

**[OptArgus](https://arxiv.org/pdf/2605.11738)** — multi-agent detection of hallucinations in
LLM-based optimisation modelling. Relevant to your verification argument: this is a literature that
already takes the failure mode seriously.

Caveat worth stating in the thesis: this cluster formulates models *from scratch*. Your problem is
different and easier in one respect — the model already exists and is fixed — and harder in another:
the parameters carry economic meaning that must stay defensible.

### Outer: agents in scientific workflows, and human oversight

**[Towards Scientific Intelligence: A Survey of LLM-based Scientific Agents](https://arxiv.org/pdf/2503.24047)**
— a survey to anchor the general framing without rebuilding it yourself.

**[HLER: Human-in-the-Loop Economic Research](https://arxiv.org/pdf/2603.07444)** — multi-agent
pipeline decomposing empirical economics into stages while keeping humans at scientific decision
points. Closest to your discipline, and a model for how to argue about where the human sits.

**[Can Large Language Model Agents Balance Energy Systems?](https://arxiv.org/html/2502.10557v1)**
— energy-domain agent work, useful for situating the thesis in its field.

### The gap to claim

*This is how chapter 2 should end — the rest of the thesis answers it.*

**Headline: the tuned quantities are contestable, not measurable.**

In every close paper found so far, the calibration target is an observable fact — a measured
incidence rate, a metered building load. GGM's calibration tunes **market power values and
willingness to pay**: economic judgments that two competent analysts could defend differently. There
is no ground truth to score an agent against, only whether its reasoning is defensible.

That has consequences the existing literature does not address. Evaluation cannot be error-against-
target. Human oversight cannot be justified merely as a safety margin that shrinks as models improve,
because the thing being decided is an argument rather than a measurement.

Two supporting points, both narrower than they first appear:

- **Domain.** Nothing found addresses a global gas market equilibrium model with market power.
  True, but weak on its own — novelty of application is thin ground.
- **Workflow breadth.** Most prior work automates *one* task: input generation, or calibration, or
  dispatch. A systematic suitability analysis across a whole modelling workflow is less common.
  Frame this as appropriate scope for an exploratory thesis, **not** as novelty — claiming breadth as
  a contribution invites the question of what, specifically, is contributed.

What **not** to claim: that using agents to configure or calibrate an existing model is new. The
literature above establishes clearly that it is not. Distinguishing yourself from the
"LLM writes an optimisation model from scratch" cluster (OptiMUS, Chain-of-Experts) is worth doing,
but it places you inside the configure-an-existing-model cluster rather than outside all of them.

### A practical contribution is also a contribution

DIW Berlin wants this to work and would use it. For an applied discipline that is a genuine strength,
and a live institutional stakeholder with a real burden is a legitimate framing at IØT.

Keep the two ideas distinct, though. **Practical contribution:** reducing a real burden for a real
institute. **Academic contribution:** what is learned that generalises beyond DIW. A thesis needs
both — the second is what separates it from a consulting deliverable — but the first is not
second-best, and it should be stated confidently rather than apologised for.

---

## 4. Ideas for making chapter 4 GGM-specific — set aside

*Set aside 2026-09-30.* Chapter 4 is a general chapter; the link to GGM is made in chapter 5. An
earlier draft suggested tying chapter 4 to GGM through four angles — how much of GGM's output fits in
a model's context window, token cost against analyst time, using different models for different
jobs, and making agent-assisted calibration reproducible. They are not planned for chapter 4, but may
be useful in chapter 5 or in the master's thesis.

---

## 5. Source material for chapter 5

The analysis itself lives in **[`workflow-task-inventory.md`](workflow-task-inventory.md)** — that is
the working document for this chapter, and it should not be restated here. It contains:

- The **four layers of input** — physical facts, projections, literature parameters, calibrated
  quantities — and why only the last involves judgment
- An **eleven-stage breakdown** of the workflow, which groups into the chapter's six steps (mapping in
  the inventory), with a provisional Code / Agent / Human / Mixed read on each — raw material for the
  four questions, not the chapter's framework
- **Where the processing happens**, inside versus outside the model, verified from the code
- The **judgment in, arithmetic out** design principle
- Why calibration resists a clean verdict, and why that makes it the interesting case

Two findings from it are worth carrying into the thesis as headline points:

**GGM already performs some pre-run checks.** `data_load.jl` emits insufficient import/export
capacity warnings during loading. The authors saw the need. That reframes the contribution from
"add validation" to *interpretation and repair* — a sharper and more defensible claim.

**The documentation contains written-down expert diagnostic reasoning** (PDF p. 28). Because those
heuristics are on paper, an agent's reasoning can be evaluated against them rather than only judged
subjectively — rare, and useful for testing agents in the master's thesis.

---

## 6. Proof of concept — left for the master's thesis

*Dropped from the project thesis on 2026-09-30.* Kept here as a starting idea for spring: if a small
first agent is built, diagnostic interpretation — explaining why a run deviates from reference values,
using the documentation's written heuristics — is the strongest candidate. Reasons:

- It is where an LLM is least replaceable by ordinary code, so it tests the real hypothesis
- Ground truth exists in the documentation, so success is assessable
- It does not require a full calibrated dataset — the reasoning can be exercised on a constructed
  deviation pattern, which matters given the data situation
- It is genuinely small: one prompt design, a handful of test cases, an evaluation rubric

The weakest PoC would be generating a full valid workbook — mostly schema plumbing, high effort, and
it tests the part of the problem that is *not* the interesting claim.

---

## 7. Open decisions for the supervisors

- Research question wording, and how narrow to go
- Whether the master's design sketch belongs in this thesis or is deferred
- Whether workflow interviews with Franziska and Lukas can be cited as a source, and if so how
