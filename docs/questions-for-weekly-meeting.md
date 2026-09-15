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

### 1. What does the calibration workflow actually look like in practice?

**For:** Franziska Holz, Lukas Barner · **Feeds:** GGM section, task-suitability analysis

The documentation says calibration takes an experienced analyst days to weeks (PDF p. 28), but not
what the analyst actually *does*. The whole thesis premise rests on this, and it cannot be answered
from the documentation.

Worth asking concretely:

- Walk through calibrating one new scenario, start to finish. What are the actual steps?
- Which steps are mechanical — checking, adjusting, re-running, comparing against reference values?
- Which require genuine judgment, where the right move depends on market knowledge?
- How do you decide a run is "close enough" and stop?
- How many iterations does a typical calibration take?

This is the highest-value question on the list. It produces material for the GGM section *and* the
evidence base for which tasks suit an agent.

### 2. Where does it go wrong?

**For:** Franziska Holz, Lukas Barner · **Feeds:** task-suitability analysis, validation argument

Failure modes are where an automated check would earn its place, and they are concrete evidence
rather than speculation.

- What mistakes recur during calibration or scenario setup?
- Has a run ever produced plausible-looking but wrong results? How was it caught?
- What do you check first when output looks off?

### 3. Has anyone already tried to automate parts of this?

**For:** Lukas Barner (best placed — wrote the port) · **Feeds:** related work, scoping

Scripts, helper tooling, spreadsheet macros, anything. Two uses: it is prior art the thesis should
acknowledge, and it marks which problems are already solved and not worth claiming.

Also worth asking what he found repetitive while porting the model — that is a direct read on where
the friction lives.

### 4. Who else uses GGM, and how? **(open)**

**For:** Franziska Holz · **Feeds:** motivation, scope

How many people run this model, at DIW / NTNU / elsewhere? A workflow burden shared by many people
is a stronger motivation than one researcher's inconvenience.

### 5. Scope and expectations for the project thesis itself

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
