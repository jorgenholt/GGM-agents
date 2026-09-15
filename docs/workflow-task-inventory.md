# GGM workflow — task inventory

A first-pass decomposition of the work around GGM, with a provisional read on what could be
automated and where human judgment is likely irreducible.

*Drafted 2026-09-15 **from the documentation only**. Nobody here has watched the workflow being
performed. Treat every "automatable" verdict as a hypothesis to test against Franziska and Lukas —
see [`questions-for-weekly-meeting.md`](questions-for-weekly-meeting.md) Q1.*

This is intended as the backbone of chapter 5 in
[`project-thesis-structure.md`](project-thesis-structure.md).

---

## The task is ETL, not file generation

Worth stating plainly, because it is easy to get wrong: GGM's inputs are **not invented**. They are
published real-world data — IEA World Energy Outlook, PRIMES, ENTSOG, EIA, GIIGNL, GIE, BP, Cedigaz —
extracted from heterogeneous sources, converted between units, aggregated to the model's node
structure, and loaded into workbooks.

So the work is **extract, transform, load, with domain judgment at each step** — closer to a data
engineering pipeline with expert supervision than to anything generative. Most of the DIW data
documentation (PDF pp. 13–32) is a description of this pipeline.

That distinction matters for the thesis. It separates you from the "LLM writes an optimisation model"
literature, and it gives a much more concrete task description than "configuring a model."

---

## The four layers of input

Not all GGM input is the same kind of thing. Most of it is simply collected; only one layer involves
real judgment. Getting this straight matters, because it is where the automation argument divides.

| Layer | What it is | Where it comes from | Changes when | Workbook |
|---|---|---|---|---|
| **1. Physical facts** | Pipeline capacities and lengths, LNG terminal capacities, storage working gas and withdrawal rates, shipping distances, node definitions | ENTSOG, EIA, GIIGNL, GIE, IEA, Cedigaz, port distances | The world changes — a terminal is built | `general_data_*` |
| **2. Projections** | Reference production and consumption per year, sector shares, seasonality | IEA WEO, PRIMES — read off a chosen outlook | A different outlook is chosen | `projected_data_*` |
| **3. Literature parameters** | Elasticities, base pipeline/LNG/storage costs and loss rates, inflators, discount rate | Published studies; the Table 6 block (PDF p. 14) | Almost never | `general_data_*` (Other Assumptions) |
| **4. Calibrated quantities** | Production costs, production capacity slack, reference prices, market power values, `GlobLoss` | **Nothing. They are inferred** by tuning until the model reproduces observed reality | Every scenario | `calibrated_data_*` |

**Layers 1–3 are collected and used nearly as-is.** Effort there is volume, not difficulty: find the
current report, extract the table, convert units, map to nodes, paste in. Tedious, repetitive,
error-prone in a *loud* way — a wrong unit conversion usually shows up as an absurd number.

**Layer 4 is not collected at all.** The documentation is explicit that detailed production cost and
capacity data is unavailable, so values are derived from assumptions supported by limited information
(PDF p. 29). Market power values are likewise tuned, not observed. This layer is *inferred by making
the model match the world* — and it is where every hard judgment lives.

Two of the three workbooks are therefore largely mechanical. One is entirely judgment.

### A scenario is a specified departure from layers 1 and 2

This is a useful way to describe scenario design. Layers 1–2 describe the world as it is and as some
outlook expects it to become. A scenario says: *hold all that, except these specified changes* —
these arcs lose capacity, this demand path replaces that one. Then layer 4 usually has to be
re-tuned, because the calibration that reproduced the old world may not hold in the new one.

### Why this splits the automation argument

The two layers point at different agent designs, and they are worth treating as separate
contributions rather than one:

- **Layers 1–3 — high volume, low risk.** Heterogeneous sources including annual report PDFs, exactly
  the extraction work LLMs are strong at, with mistakes that are relatively easy to catch
  automatically. This is where most of the *hours* probably go, and the safest place to start.
- **Layer 4 — low volume, high risk.** Small number of numbers, enormous consequence, quiet failure.
  This is where the *difficulty* is, and where the interesting thesis claim lives.

Worth confirming against practice which layer actually consumes the days-to-weeks. The documentation
suggests calibration, but data updating may quietly dominate in ordinary use.

---

## The inventory

Legend for **Verdict**: **Code** = deterministic, belongs in ordinary software · **Agent** = benefits
from reading, reasoning, or judgment over unstructured input · **Human** = judgment that should not
be delegated · **Mixed** = split across the above.

| # | Stage | What it involves | Verdict | Why |
|---|---|---|---|---|
| 1 | **Source acquisition** | Pull production/consumption outlooks (WEO, PRIMES), pipeline capacities (ENTSOG, EIA), LNG terminals (GIIGNL, GIE), storage (IEA, GIE, EIA-191, Cedigaz), prices (BP), sea distances | Mixed | Structured databases → code. Extracting tables from annual report PDFs → genuinely good LLM task. Choosing *which* edition and table → judgment |
| 2 | **Unit conversion** | mtpa→bcm, mcf→bcm, TWh→bcm, bcma→mcm/d | Mixed | Arithmetic must be exact → code. But conversion factors **differ by country** because gas composition varies, so *selecting* the factor is domain knowledge. The documentation flags inconsistent conversion as a trap to avoid (PDF p. 24) |
| 3 | **Spatial aggregation** | Map country data onto GGM nodes; split USA/CAN/RUS/CHN/IND into sub-nodes by share; aggregate parallel pipelines; assign terminals to representative ports | Mixed | Applying a documented rule → code. New or ambiguous cases → agent proposes, human confirms. Contains real traps: US regional shares must use **marketed**, not gross, production — Alaskan gross is ~10× marketed (PDF p. 26) |
| 4 | **Temporal interpolation** | Fill missing years linearly; 2045 = Δ×0.9, 2050 = Δ×0.72; 2055–60 held flat | **Code** | Fully specified formula, no judgment. Clean example of a task an agent should not touch |
| 5 | **Structural validation** | Node IDs in Arcs exist in Nodes; LNG nodes present in distance matrix; storage flags consistent; required columns and types | **Code** | One correct answer, cheap to check, loud failure. Fifty lines of Python beats an LLM call on speed, cost and reliability |
| 6 | **Feasibility checks** | Global production ≈ consumption after `GlobLoss`; capacity ≥ reference production + slack; export capacity sufficient | Mixed | Detection is arithmetic → code. **GGM already does part of this** — `data_load.jl` warns on insufficient import/export capacity ([:245](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L245)). The gap is *interpretation and repair*, not detection |
| 7 | **Scenario definition** | Choose WEO scenario × EU pathway; adjust assumptions to fit the narrative | Mixed | The choice is human. Checking that parameters **cohere with the stated narrative** is a real agent task — a decarbonisation scenario with rising 2050 demand is incoherent in a way no schema check catches |
| 8 | **Calibration** | Tune base costs, capacity slack, reference prices, market power, `GlobLoss`; base year first, then future years; iterate | **Mixed — the interesting case** | See below |
| 9 | **Execution** | Run Julia + Gurobi, capture logs and outputs | **Code** | Orchestration. No judgment |
| 10 | **Result checking** | Mass balances, calibration deviation reports, utilisation rates | Mixed | Computing them → code. Explaining *why* a deviation sits where it does → agent |
| 11 | **Interpretation and write-up** | What does this scenario mean, what follows from it | **Human** | This is the research output. Agent assistance at most |

---

## Stage 8 is where the thesis lives

Calibration is the one stage that resists a clean verdict, and that is exactly why it is interesting.

**Why it isn't simply Human:** the documentation contains *written-down expert heuristics*. If Russia
under-produces while consuming enough, its exports are too low, which is one of three named causes:
production costs too high, willingness to pay in export markets too low, or market power too high. A
parallel six-cause example is given for Chinese consumption (PDF p. 28). Reasoning chains of that
shape are what LLMs do well — and because they are documented, an agent's output can be **evaluated
against them**.

**Why it isn't simply Agent:** the documentation is equally explicit that a wrongly calibrated model
produces biased results that look like market logic rather than like errors (PDF pp. 28–32). Quiet,
plausible failure is the exact error class an LLM is worst at catching, and worst at admitting to.

**What makes it different from the prior work:** in every close paper found so far, the calibration
target is an observable fact — a measured incidence rate, a metered building load. In GGM the tuned
quantities are **market power values and willingness to pay**. These are contestable economic
judgments, not measurements. Two competent analysts could defend different values, which means there
is no ground truth to score an agent against — only whether its reasoning is defensible.

That is the sharpest available argument for a human gate that does not dissolve as models improve.

---

## Where human input is likely irreducible

Answering Jørgen's question directly — provisional, and the thing to test in the meetings:

1. **Choosing the scenario narrative.** What future is being modelled is a research decision.
2. **Accepting a calibration as good enough.** Someone must own the judgment that the model
   adequately represents the world, because the failure mode is invisible.
3. **Contestable parameter values** — market power, willingness to pay. An agent can propose and
   justify; a human should decide, because the value is an argument rather than a measurement.
4. **Domain traps in data preparation.** Marketed versus gross production, country-specific
   conversion factors, which storages to exclude. These are knowable — once someone has written them
   down. Much of the value may lie in *eliciting* these rules, which is itself a good agent task.
5. **Interpreting results into claims.** The thesis output.

Note that (4) is the most optimistic item: it looks like human judgment today largely because it
lives in analysts' heads. Capturing it is a tractable and worthwhile target.

---

## What this inventory needs before it can be trusted

- **Validation against practice.** Built from documentation describing the 2019 GAMS workflow. The
  real 2023 Julia workflow may differ substantially.
- **Time weighting.** No idea which stages consume the days-to-weeks. Automating a stage that takes
  an afternoon is not worth much. Ask for rough proportions.
- **Frequency.** A stage repeated every scenario is worth far more than one done once per dataset
  revision.
- **Missing stages.** This is what the documentation describes; the lived workflow probably includes
  steps nobody wrote down.
