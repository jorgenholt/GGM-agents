# Project thesis — proposed structure

A structure to propose to supervisors and argue around, plus the prior work it should sit on.

*Drafted 2026-09-15. Everything here is a proposal, not a decision.*

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
| 2 | The Global Gas Model | What it is, and where the manual work actually goes |
| 3 | LLM agents | What they are good at, what they are bad at |
| 4 | Related work | Who has tried this on other models, and how it went |
| 5 | **Which GGM tasks fit** | The core chapter — the mapping, and the reasoning behind it |
| 6 | Conclusion | What we'd build in the master's thesis |

Optionally a small **proof of concept** between 5 and 6, if the supervisors want one.

**Why this order:** chapters 2 and 3 are the two halves of the problem. Chapter 4 shows we know the
field. Chapter 5 is where they meet, and it is the actual contribution. Everything else supports it.

**Three things to decide with supervisors:**

1. How narrow should the research question be?
2. Is a proof of concept wanted, or is a well-argued exploration enough?
3. How much related work is enough — a section, or a full chapter?

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
> at all, because the failure mode is a plausible-looking wrong answer. Here is the mapping, and here
> is what it implies for a system design.

The contribution is **the mapping and its justification** — not enthusiasm, and not a build.

Arguing that parts of the workflow *should not* be automated is what will make this credible rather
than promotional. The GGM documentation hands you the argument: it warns that a wrongly calibrated
model produces biased results that look like market logic (PDF pp. 28–32). That is precisely the
error class an LLM is worst at catching.

---

## 2. Proposed section structure

Sections 3 and 4 are the two Jørgen and Save already identified. The rest is scaffolding around them.

### 1. Introduction
Problem, research question(s), scope boundary (exploration, not implementation), contribution,
and structure. State plainly that building is the master's thesis — it frames expectations.

### 2. Background: the Global Gas Model
The reader does not know what GGM is and cannot be assumed to.

- What the model is and what question it answers — partial equilibrium, multi-period, market power
- Structure: nodes, arcs, suppliers, seasons; the LNG and pipeline value chains
- Inputs: the three workbooks and what they contain
- **The workflow around the model** — this is the part that matters, and it is what the documentation
  covers least. Fill it from the weekly meetings (see
  [`questions-for-weekly-meeting.md`](questions-for-weekly-meeting.md) Q1).
- Where the effort goes: calibration takes an experienced analyst days to weeks
  ([`ggm-model.md` §7](ggm-model.md#calibration-effort--citable-evidence-of-manual-burden))

Source material is largely assembled in [`ggm-model.md`](ggm-model.md).

### 3. LLM agents: what they are and where they hold up
Written **toward the problem**, not as a general survey. Every capability discussed should earn its
place by mapping onto something in section 2.

- What distinguishes an agent from a prompt: tool use, iteration, feedback from execution
- Capabilities that matter here: reading unstructured documentation, applying written heuristics,
  proposing and revising under numeric feedback, explaining reasoning
- Limits that matter here: hallucination, no ground truth about physical reality, weak arithmetic,
  non-determinism, context limits
- Model selection and cost — see §4 below for how to keep this concrete
- **Which tasks suit an LLM and which are better as ordinary code** — the analytical core; develop it
  here, apply it in section 5

### 4. Related work
Agents applied to configuring, calibrating, and operating large domain models. See §3 of this
document for candidates.

Organise by *what the agent was asked to do*, not by application domain — it keeps the section
pointed at your problem instead of drifting into an energy-AI survey.

### 5. Task suitability analysis for the GGM workflow
**The core contribution.** Take the workflow from section 2, decompose it, and classify each task
against the criteria from section 3.

Suggested axes for classification:

| Axis | Question |
|---|---|
| Determinism | Is there one correct answer, checkable by rule? |
| Context | Structured data, or does it need documentation and intent? |
| Failure visibility | Does a mistake announce itself, or does it look plausible? |
| Reversibility | Cheap to catch and redo, or does it contaminate downstream results? |
| Verifiability | Can the output be checked automatically, or only by an expert? |

Tasks where the answer is *deterministic, structured, loud failure* belong in code. Tasks that are
*judgment-based, unstructured, quiet failure* are where an agent may help — but exactly where it needs
a human gate. That tension is the interesting finding, and it should be stated as one.

### 6. Design sketch for the master's thesis
What a system implied by section 5 would look like — component responsibilities, where humans sit in
the loop, what gets verified and how. A sketch establishing feasibility, not a specification.

### 7. Proof of concept **(if in scope)**
See §5 of this document for a scoping suggestion.

### 8. Discussion
Risks, limitations, and what the analysis does not settle. Include what should *not* be automated and
why — this is a feature of the argument, not a hedge.

### 9. Conclusion and plan for the master's thesis
What was established, what remains open, and what spring should build. This section is partly a
project plan, and supervisors will read it as one.

---

## 3. Related work — candidates

Three clusters, from closest to your problem outward.

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

## 4. Making the AI section concrete rather than generic

The risk in section 3 is writing a generic explainer on LLMs. Anchor every claim to GGM. Some
concrete angles:

**Context budget as a real design constraint.** GGM produces results across ~109 consumption nodes,
~93 production nodes, 9 years and 3 seasons. A full result set does not fit in a context window, and
would be expensive and error-prone even if it did. So *what gets summarised, and by what?* That is a
genuine architectural question with a defensible answer, not a survey topic.

**Cost modelling tied to the workflow.** Calibration is iterative. The grey-box paper converged in
~16 evaluations. If GGM calibration takes N agent iterations, each carrying model description,
parameter bounds, and residual history — what does that cost, and how does it compare to days of
analyst time? That comparison is the argument for the thesis's premise, in numbers.

**Model tiering as a finding.** Structural validation, diagnostic reasoning, and prose generation
have very different difficulty and very different cost. Arguing that a system should use different
models for different stages is more interesting and more useful than benchmarking models against
each other.

**Determinism and reproducibility.** A thesis result must be reproducible. An LLM in the loop is
non-deterministic. How do you make agent-assisted calibration reproducible enough to publish? The
grey-box paper flags this as an open limitation — engaging with it seriously is a real contribution.

---

## 5. Catching errors before a run — a worked example

Jørgen asked *how* an agent would catch errors before running. Working this through makes a good
worked example for section 5, because it shows the classification doing real work rather than
being asserted.

**Tier 1 — structural consistency. Ordinary code, not an LLM.**
Node identifiers in the Arcs sheet exist in the Nodes sheet; every liquefaction and regasification
node appears in the Vessel Distances matrix; nodes flagged for storage in Nodes appear in Storages;
required columns present with correct types. One correct answer, cheap to check, loud failure. An
LLM here is slower, costlier and less reliable than fifty lines of Python — **a clean example of a
task that is better coded.**

**Tier 2 — numerical feasibility. Code detects, LLM explains.**
Does global reference production match global reference consumption after `GlobLoss`? Is production
capacity 3–5% above reference production, per the calibration guidance? Is export capacity adequate
for projected net exports?

Note that **GGM already does some of this**: `data_load.jl` emits `"Insufficient export capacity
detected"` and `"Insufficient import capacity detected"` warnings during loading
([data_load.jl:245](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L245)). That is existing prior
art inside the model, and it is worth citing — it shows the model's own authors saw the need for
pre-run checks. The gap is not detection but *interpretation and repair*, which is where an agent
earns its place.

**Tier 3 — narrative coherence. Genuinely an LLM.**
Does the scenario's parameters match the story it claims to tell? A decarbonisation scenario with
rising gas demand in 2050 is internally incoherent in a way no schema check catches. Are market power
assumptions consistent with the stated geopolitical premise? Have two changes been made that interact
badly — raising an exporter's market power while also cutting its export capacity? This needs world
knowledge and inference about intent. No amount of ordinary code substitutes.

**Tier 4 — diagnostic interpretation. The strongest case, and a ready-made benchmark.**
After a run, output deviates from reference values. Why?

The DIW documentation contains **explicit expert diagnostic reasoning** (PDF p. 28): if Russia
under-produces while consuming enough, its exports are too low, which could be (1) production costs
too high, (2) willingness to pay in export markets too low, or (3) Russian market power too high. A
parallel worked example is given for Chinese consumption with six candidate causes.

This is unusually valuable for a thesis, because those heuristics are **written down**. That gives
you a ground truth to evaluate an agent against, rather than only subjective judgement — a documented
expert reasoning chain, and a measurable question: does the agent reproduce it?

The tiering also *is* the contribution in miniature: the same workflow spans tasks that should be
plain code, tasks where code detects and an agent explains, and tasks that only an agent can attempt.

---

## 6. Proof of concept — scoping suggestion **(if in scope)**

If a PoC happens, Tier 4 is the strongest candidate. Reasons:

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
- Whether a proof of concept is in scope, and whether Tier 4 is the right target
- How much weight the related-work section carries relative to the analysis
- Whether the master's design sketch belongs in this thesis or is deferred
- Whether workflow interviews with Franziska and Lukas can be cited as a source, and if so how
