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

**For:** Franziska Holz, Lukas Barner · **Feeds:** GGM section, task-suitability analysis

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

**For:** Franziska Holz, Lukas Barner · **Feeds:** task-suitability analysis, validation argument

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
- Is a proof of concept wanted, or is a well-argued exploration sufficient on its own?
- Expected length, structure, and deadline
- Is there existing literature they would point to on LLM agents in modelling workflows?

---

## Parked — for the build phase (spring 2027)

**Input data access.** `ggm/data_2023/` ships empty; one complete scenario set
(`general_data_*`, `projected_data_*`, `calibrated_data_*`) is a hard prerequisite for the master's
thesis and would help any proof of concept. Not blocking this semester, but lead time is unknown, so
worth requesting early. `STEPS_NENO` is the scenario named in `ggm_2023.jl`.

**Production cost curve — does the Julia port redefine `q(r)`?** For Lukas. The doc's worked example
(base 12, `c=1`, `q=5`) gives marginal cost 60 at full capacity; the Julia formulation
(`cost_pq = base·q(r)/cap_p`, with ½ in the objective) gives 72. Either `q(r)` became an increment
above `c(r)` in the port, or the curves genuinely differ. Only matters once we generate or modify
production cost parameters ourselves — calibration data received from the authors is already
self-consistent with the code. Full derivation:
[`ggm-model.md` §9](ggm-model.md#production-cost-curve--open-discrepancy-with-the-doc).

---

## Resolved

### Flow units — mcm/day, not mcm/year — *2026-09-15*

The Julia variable comments say `mcm/yr`; they are wrong. `BCMA_TO_MCMD = 1000/365` is applied to
every capacity and reference quantity at load time, so internal units are **mcm/day**, matching the
2019 documentation. Workbook inputs are bcma; reported annual figures are bcm.

Resolved from the source, no human needed. Details in
[`ggm-model.md`](ggm-model.md#flow-units--resolved-mcmday).
