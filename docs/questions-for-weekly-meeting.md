# Questions for weekly meeting

Running list of things that need a human answer. Each entry should stand alone — enough context to
ask cold, without rereading the session it came from.

Move answered items to **Resolved** with the answer, so the reasoning is preserved.

*Reoriented 2026-09-15 around the project thesis (exploration and writing — see
[`thesis-scope.md`](thesis-scope.md)). Build-phase questions are parked at the bottom.*

> The questions below are **suggestions, not a fixed agenda** — drafted from what the thesis argument
> appears to need. Cut freely.

---

## Now — project thesis

### 1. Does the four-layer view of the inputs hold?

**For:** Franziska Holz, Lukas Barner · **Feeds:** GGM chapter, chapter 5

From the documentation, GGM's inputs appear to divide into four kinds. **Ask whether this is right
before building on it** — full version in
[`workflow-task-inventory.md`](workflow-task-inventory.md#the-four-layers-of-input):

1. **Physical facts** — pipeline, LNG, storage capacities; distances. Collected from ENTSOG, EIA,
   GIIGNL, GIE, IEA. Change when the world changes.
2. **Projections** — reference production and consumption, read off a chosen WEO or PRIMES outlook,
   then split regionally and interpolated.
3. **Literature parameters** — elasticities, base costs, discount rates. Set once, rarely touched.
4. **Calibrated quantities** — production costs, reference prices, market power, `GlobLoss`. Not
   collected at all: inferred by tuning until the model reproduces observed reality.

Is this how you think about it? Is anything misplaced, or missing?

### 2. How is layer 4 actually done? — **the key question**

**For:** Lukas Barner (weekly) · **Feeds:** the core chapter

Layers 1–3 are collection and arithmetic — the optimisation target there is speed. Layer 4 is
reasoning, and it is where the thesis claim lives. The documentation says calibration takes days to
weeks (PDF p. 28) but not what the analyst *does*. This cannot be answered from documentation.

Concretely:

- **Walk through tuning one parameter.** What do you look at, what do you change, how do you know it
  worked?
- **Where do you start?** Which parameter first, and why that one?
- The documentation lists three candidate causes when a country under-produces — costs too high,
  willingness to pay too low, market power too high (PDF p. 28). **How do you decide which it is?**
- **One node at a time, or globally?** Given that the market behaves as communicating vessels.
- **How do you know when to stop** — what does "close enough" mean in practice?
- **What does a failed calibration look like**, and how do you recognise it?
- **Is there any record of past calibrations** — old files, notes, working spreadsheets? Would be
  extremely valuable: a trace of expert reasoning to evaluate an agent against.

### 3. Which layer actually eats the most time?

**For:** Lukas Barner, Franziska Holz · **Feeds:** scoping, and the motivation argument

The documentation points at calibration, but routine data updating may quietly dominate in ordinary
use. Rough proportions are enough.

This changes what is worth building first. Layers 1–2 are high volume and low risk; layer 4 is low
volume and high risk. If most hours go to updating data, that is the better first target even though
layer 4 is the more interesting problem.

Related: **how do you find out what has changed?** When a new EIA or GIIGNL report comes out, is it
re-read from scratch, or is there a diffing process against last year?

### 4. Where does it go wrong?

**For:** Franziska Holz, Lukas Barner · **Feeds:** chapter 5, "where a person stays involved"

Failure modes are where an automated check would earn its place, and they are concrete evidence
rather than speculation.

- **Has a scenario ever "solved cleanly but answered the wrong question"** — a run that completed
  fine and produced plausible numbers, but the configuration did not match what was intended?
  *Push hardest on this one.* It is the failure mode the whole thesis argument turns on, and one
  real example beats any amount of reasoning about what could happen in principle.
- What mistakes recur during calibration or scenario setup?
- What do you check first when output looks off?
- How was a bad run caught, when it was caught?

Also on scenario mechanics, relevant to
[`how-it-would-work.md`](how-it-would-work.md):

- How is a new scenario actually created — edit a copy of the workbooks, or is there tooling?
- How often is a genuinely new scenario built, versus re-running variations of an existing one?

### 5. Has anyone already tried to automate parts of this?

**For:** Lukas Barner (best placed — wrote the port) · **Feeds:** related work, scoping

Scripts, helper tooling, spreadsheet macros, anything. Two uses: it is prior art the thesis should
acknowledge, and it marks which problems are already solved and not worth claiming.

Also worth asking what he found repetitive while porting the model — that is a direct read on where
the friction lives.

### 6. Who else uses GGM, and how? **(open)**

**For:** Franziska Holz · **Feeds:** motivation, scope

How many people run this model, at DIW / NTNU / elsewhere? A workflow burden shared by many people
is a stronger motivation than one researcher's inconvenience.

### 7. Scope and expectations for the project thesis itself

**For:** both supervisors · **Feeds:** everything

Jørgen and Save have flagged that scope is still being negotiated. Worth pinning down:

- What does a strong project thesis look like here — how much breadth versus depth?
- *(Decided 2026-09-30: no proof of concept this semester — no need to ask.)*
- Expected length, structure, and deadline
- Is there existing literature they would point to on LLM agents in modelling workflows?

### 8. Questions about the 2023 dataset

**For:** Lukas Barner · **Raised:** 2026-09-30 · **Background:**
[`ggm-data-2023.md`](ggm-data-2023.md)

Things that came up when reading through the data. None of them block anything; they're about
understanding it correctly.

- **What do the codes stand for?** Scenarios `FFF`, `MCA`, `NCA`, `TZE`; general variants `NENO`,
  `SQAB`, `EUSD`. Which combination is the usual reference run?
- **Is market power meant to stay constant?** The minimum ratio is 1 for every trader, which switches
  off the 0.7-per-period decay entirely.
- **Storage OPEX is labelled USD** but used as EUR without conversion. Stale label, or a real mismatch?
- **FFF and TZE have zero demand from 2050.** The loader handles it by replacing infinities with a
  fallback value. Intended, and do those runs solve cleanly?
- **`DistCutOff` is in the sheet but never read by the code.** Deliberate?
- **Three defaults lie outside the ranges listed next to them** — most notably shipping loss at 1 % per
  1,000 sea miles against a stated 0.25–0.4 %. Calibrated on purpose?

### 9. What we still need in order to design agents

**For:** Lukas Barner · **Raised:** 2026-09-30

Reading the code and the 2023 data tells us *what* the configuration looks like, but not how it is
produced or used. These three gaps can only be filled by someone who works with the model.

- **Where does each number in the 2023 data come from?** For each sheet, which report, database or
  outlook it was built from, and what was done to it on the way. The files themselves don't say. An
  agent that updates data needs to know where to look and what to do with what it finds.
- **How do you calibrate, and did you start automating it?** This extends question 2. Beyond the
  step-by-step procedure (what you compare, which values you adjust and in what order, when you stop),
  the Julia code contains an unused calibration hook: a `GGM_CalibrationTargets` structure with
  target sales per country and a step size
  ([GlobalGasModel.jl:76](../ggm/GlobalGasModel/src/GlobalGasModel.jl#L76)), and a `calib_int` input
  that scales demand per node, season and year
  ([Model.jl:7](../ggm/GlobalGasModel/src/SubModules/Model.jl#L7)). Neither is ever called. Is there
  a calibration script outside the public repo, or was this started and dropped? Also, since the model
  produces no calibration report, how do you compare results with the reference values today?
- **What does a finished run look like, and how do you read it?** We can't run the model ourselves
  yet. An example set of output files from one run, and a quick walkthrough of what you look at
  first, would show what an agent interpreting results would actually be working with.

---

## Parked — for the build phase (spring 2027)

**Production cost curve — does the Julia port redefine `q(r)`?** For Lukas. The doc's worked example
(base 12, `c=1`, `q=5`) gives marginal cost 60 at full capacity; the Julia formulation
(`cost_pq = base·q(r)/cap_p`, with ½ in the objective) gives 72. Either `q(r)` became an increment
above `c(r)` in the port, or the curves genuinely differ. Only matters once we generate or modify
production cost parameters ourselves — calibration data received from the authors is already
self-consistent with the code. Full derivation:
[`ggm-model.md` §9](ggm-model.md#production-cost-curve--open-discrepancy-with-the-doc).
*Update 2026-09-30:* the 2023 data uses `q = 1, 5, 8` exactly as in 2019, so `q` was not redefined —
the curves really are steeper than documented. The question is now whether that was intended.

---

## Resolved

### Input data received — *2026-09-30*

The GGM authors provided the full 2023 dataset, and are fine with it being kept in our private repo.
It lives in [`data_2023/`](../data_2023/): 11 workbooks, 4 scenarios × 3 general variants. What is
in it is described in [`ggm-data-2023.md`](ggm-data-2023.md).

### Literature review goes second — *recorded 2026-09-30*

Supervisor feedback on the proposed structure: the literature review should be its own chapter,
placed directly after the introduction. This settles the earlier open question of whether related
work should be a section inside the LLM-agents chapter or a chapter of its own.

Knock-on changes are in [`project-thesis-structure.md`](project-thesis-structure.md): GGM moves to
chapter 3 and LLM agents to chapter 4; the introduction now carries a short GGM sketch so chapter 2
is readable; and chapter 2 ends by stating the gap the rest of the thesis addresses.

### Flow units — mcm/day, not mcm/year — *2026-09-15*

The Julia variable comments say `mcm/yr`; they are wrong. `BCMA_TO_MCMD = 1000/365` is applied to
every capacity and reference quantity at load time, so internal units are **mcm/day**, matching the
2019 documentation. Workbook inputs are bcma; reported annual figures are bcm.

Resolved from the source, no human needed. Details in
[`ggm-model.md`](ggm-model.md#flow-units--resolved-mcmday).
