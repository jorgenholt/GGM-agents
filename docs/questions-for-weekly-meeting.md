# Questions for weekly meeting

Running list of things that need a human answer. Each entry should stand alone — enough context to
ask cold, without rereading the session it came from.

Move answered items to **Resolved** at the bottom with the answer, so the reasoning is preserved.

---

## Open

### 1. Production cost curve — does the Julia port redefine `q(r)`?

**For:** Lukas Barner (wrote the Julia port) · **Raised:** 2026-09-15 · **Blocks:** calibration work

The documentation and the Julia code appear to produce different production cost curves for the same
calibration inputs.

**Doc** (PDF pp. 33–34, worked example for `USA_2`): base cost 12, resource R2 with `c = 1`, `q = 5`
gives marginal cost **12** at the first unit and **60** at full capacity — i.e.

```
MC at capacity = base · q(r)
```

**Julia** ([`data_load.jl:104`](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L104)) builds

```
cost_pq[n,r,y] = base_cost · q(r) · year_factor · inflator / cap_p[n,r,y]
```

and the objective ([`Model.jl:56–61`](../ggm/GlobalGasModel/src/SubModules/Model.jl#L56)) uses
`cost_pl·Q_P + ½·cost_pq·Q_P²`, so

```
MC(Q) = cost_pl + cost_pq·Q   ⇒   MC at capacity = base · (c(r) + q(r)) = 12 · (1 + 5) = 72
```

**Question:** was `q(r)` redefined in the port as an *increment above* `c(r)` (so the doc's 60 would
now be entered as `q = 4`), or do the two versions genuinely have different cost curves?

**Why it matters:** this sets the steepness of every production cost curve in the model. If we
calibrate against the doc's interpretation while the code uses the other, every production cost is
wrong by the `c(r)` term — small for R1, large for the steep R3 tail that does the rationing.

---

### 2. Input data access

**For:** Franziska Holz · **Raised:** 2026-09-15

`ggm/data_2023/` ships with only a note to contact the authors. We need one complete scenario set to
calibrate and validate against:

- `general_data_<scen>.xlsx`
- `projected_data_<scen>.xlsx`
- `calibrated_data_<scen>.xlsx`

A real scenario is more useful than a constructed example, and less work to provide. `STEPS_NENO` is
the scenario named in `ggm_2023.jl`.

Also worth confirming: which scenarios exist in the 2023 dataset, and whether the naming still splits
on `_` into (projection scenario, general-data variant) the way `data_load.jl` assumes.

---

## Resolved

### Flow units — mcm/day, not mcm/year — *2026-09-15*

The Julia variable comments say `mcm/yr`; they are wrong. `BCMA_TO_MCMD = 1000/365` is applied to
every capacity and reference quantity at load time, so internal units are **mcm/day**, matching the
2019 documentation. Workbook inputs are bcma; reported annual figures are bcm.

Resolved from the source, no human needed. Details in [`ggm-model.md`](ggm-model.md#flow-units--resolved-mcmday).
