# How this would actually work

A concrete walkthrough: one scenario, run the way DIW runs it today, then the same scenario with
agent assistance. Intended to make the idea discussable without hand-waving.

*Drafted 2026-09-15. The mechanics of running the model are read from the code and are reliable.
**The workflow around it is inferred, not observed** — how an analyst actually works is
[question 1 for the meetings](questions-for-weekly-meeting.md). Expect to correct this.*

---

## What "running the model" means mechanically

Small and unglamorous. One command:

```
julia ggm_2023.jl STEPS_NENO
```

The scenario name splits on `_`. `STEPS` selects the projection and calibration workbooks, `NENO`
the general data workbook. The model reads three Excel files from `data_2023/`, builds a quadratic
program in JuMP, solves it with Gurobi, and writes result tables to `results/outputs/`.

**A "scenario" is not a script or a config flag. It is a set of Excel workbooks.** Creating a new
scenario means producing new workbooks — or editing copies of existing ones.

That is the whole interface, and it is why the interesting work is entirely in what surrounds it.

---

## The scenario

> *What happens if the EU bans Russian pipeline imports from 2030, while Russia is permitted to
> expand export capacity eastward?*

A question DIW plausibly cares about, and one that touches most of the workflow.

---

## Today (inferred)

**1. Decide what the question means in model terms.** Which arcs count as "Russian pipeline imports
to the EU"? Every `RUS_* → EU_*` arc, or also routes through Belarus, Ukraine and Turkey? Does the
ban start in the 2030 period or the one before, given the one-period gap between investment and
availability? *Judgment. Nothing automates this.*

**2. Find the affected rows.** Open `general_data_NENO.xlsx`, sheet Arcs. Locate every relevant arc
among hundreds of rows. Miss one and the ban leaks.

**3. Edit capacities.** Set `2030 Capacity (bcma)` onward to zero for those arcs. Also zero the
expansion limits, or the model may simply rebuild what was removed.

**4. Think through the knock-on effects.** Should eastward arcs get raised expansion limits? Does
Russian market power in Europe still make sense at zero volume? Does EU reference consumption stay
unchanged — and if so, is the model meant to ration by price, or is a demand response intended?
*This is where scenarios quietly go wrong.*

**5. Save as a new scenario** and run it.

**6. Did it solve?** If Gurobi reports infeasible, the cause could be a genuine physical
impossibility, or a typo in one cell.

**7. Do the results look sane?** Check mass balances. Have EU prices risen plausibly or absurdly? Has
LNG import filled the gap, and is the required regasification capacity realistic?

**8. Diagnose anything odd.** Is this a real model result or a data error? The documentation's
heuristics apply here — if a country under-produces, it's costs, willingness to pay, or market power.

**9. Iterate.** Steps 3–8, repeatedly.

**10. Recalibrate if needed**, then write up.

The mechanical steps (2, 3, 5, 6) are tedious rather than difficult. The judgment steps (1, 4, 8) are
where expertise lives. **Step 4 is the dangerous one** — an error there produces a model that solves
cleanly and answers a subtly different question than the one asked.

---

## With agent assistance

The analyst asks in plain language:

> *"Model an EU ban on Russian pipeline imports from 2030. Allow Russia to expand eastward capacity."*

**The agent identifies the affected arcs.** Reads the Nodes and Arcs sheets, finds every `RUS_* →
EU_*` pipeline arc, and — importantly — surfaces the ambiguous ones for a decision rather than
choosing silently:

> *Found 14 direct RUS→EU pipeline arcs. Also found 3 transit routes via Belarus and Ukraine and 1
> via Turkey. Include these? They are Russian gas reaching the EU, but not direct arcs.*

**It proposes a concrete diff, not a finished edit.** Which rows, which columns, which values, with
reasoning — expansion limits zeroed too, and why.

**It flags interactions the analyst didn't mention.** This is the step that earns its keep:

> *EU reference consumption is unchanged. Removing ~140 bcma of supply without a demand response
> means the model rations by price — EU prices may rise sharply. Intended, or should consumption
> adjust?*
>
> *Russian market power in EU nodes is still 0.5 with zero volume. Harmless mathematically, but
> inconsistent with the scenario narrative.*

**The analyst approves, edits, or rejects.** The gate stays human.

**It applies the change and runs the pre-run checks** from the task inventory — structural
consistency, then feasibility. Does global production still roughly match consumption? Is eastward
export capacity actually sufficient for the redirected volume, or has an infeasibility just been
created?

**It runs the model and reports back**, in the analyst's terms rather than as raw tables:

> *Solved. EU consumption falls 11% in 2030 versus reference; prices rise 34%. LNG imports rise
> 82 bcma, requiring regasification expansion of 31 bcma — above the historical build rate, so the
> result depends on that limit being realistic.*
>
> *Russian production falls 9% despite eastward expansion; Chinese import capacity binds from 2035.*

**Diagnosis when something is off.** If results deviate from expectation, it applies the documented
heuristics and proposes candidate causes — *without* deciding which is correct.

**The analyst decides what it means** and writes it up.

---

## What changed, and what deliberately didn't

**Removed:** finding rows in a spreadsheet, editing them consistently, remembering to zero expansion
limits, checking structural consistency, running the mechanics, assembling result tables.

**Added:** the interaction check at step 4. This is the real contribution — not speed, but catching
the class of error that produces a clean-looking run answering the wrong question. That error is
invisible today precisely because nothing fails.

**Deliberately unchanged:** defining what the scenario means, approving every edit, judging whether
results are believable, and writing conclusions. All still human.

A useful way to describe the target: **the agent does not run scenarios. It prepares them, checks
them, and explains them — and an analyst still runs them.**

---

## Why this shape and not "full automation"

Full automation is the obvious pitch and the wrong one here.

GGM's failure mode is not a crash. It is a model that solves, produces plausible numbers, and
answers a question nobody asked — because market power was left inconsistent, or a transit route was
missed, or reference consumption implied a demand response nobody intended. The documentation makes
this point directly about calibration: a badly calibrated model yields biased results stemming from
invalid parameter choices rather than market logic (PDF pp. 28–32).

An agent cannot be the last line of defence against that class of error, because it is exactly the
class it is worst at detecting in its own output. So the design puts it where it is strong — reading
heterogeneous sources, spotting inconsistencies between intent and configuration, applying written
diagnostic heuristics, explaining results — and leaves the human where the failure is quiet.

That constraint is a finding, not a limitation to apologise for. It is worth stating as one.

---

## Open questions this raises

- How does an analyst actually create a new scenario today — edit a copy of the workbooks, or is
  there existing tooling?
- How often is a genuinely new scenario built, versus re-running variations?
- Has a scenario ever gone wrong in the "solved cleanly, wrong question" way? *This is the most
  valuable single anecdote available for the thesis.*
- Where does the time actually go — the tedious steps, or the judgment ones?
