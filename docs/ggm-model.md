# GGM — model reference

Condensed reference for the Global Gas Model, for use while building the agent layer.

**Source document:** [`ggm-documentation-v3.0.pdf`](ggm-documentation-v3.0.pdf) — Egging & Holz,
*Global Gas Model: Model and Data Documentation v3.0*, DIW Data Documentation 100, May 2019.

**Page references below are PDF page numbers** (what a viewer's page box expects). The document's
own printed footer number is always 2 lower, so PDF p. 48 shows "46" at the bottom.

> **Important:** the PDF documents the **GAMS v3.0 (2019)** implementation. The `ggm/` submodule is a
> later **Julia/JuMP port** using 2023 data. The economics are the same; file names, sheet names,
> solver, and some constraints differ. Divergences are listed in the last section — check there before
> trusting the PDF on anything implementation-level.

---

## 1. What the model is

A multi-period **partial equilibrium** model of the global natural gas market. It finds production,
consumption, trade, storage use, and infrastructure expansion that maximise a welfare-like objective,
while allowing some exporters to exert **market power**.

- Formulated as a **quadratic program** (quadratic production costs, linear inverse demand).
- Not a pure social-welfare maximisation — a *market power adjustment* (MPA) term makes the solution
  correspond to an imperfect-competition equilibrium (PDF p. 51).
- Coverage: 90+ countries in 9 regions. 2019 dataset had 109 consumption nodes, 93 production nodes,
  50 storage nodes, 28 liquefaction, 50 regasification nodes (PDF p. 40).
- Horizon: 5-year steps. The 2019 doc runs 2015–2060; the Julia entry point runs **2020–2060**.

Value chain: production → (pipeline | liquefaction → shipping → regasification) → consumption, with
storage at geographical nodes (PDF p. 10, Figure 1).

### Regions

`NAM` North America · `SAM` South America · `EU` EU28 · `ROE` Other Europe · `AFR` Africa ·
`RUS` Russia · `CAS` Caspian · `MEA` Middle East · `ASP` Asia Pacific (PDF p. 16, Table 8).

USA, Canada, Russia, China and India are split into multiple nodes (PDF pp. 26–27).

---

## 2. Mathematical formulation

Full formulation: **Appendix B, PDF pp. 48–52**. Sets/parameters/variables tables: PDF pp. 48–49
(Tables 37–40).

### Sets

| Symbol | Meaning |
|---|---|
| `T` | Suppliers (traders) `t` |
| `N` | Geographical nodes `n` (subsets: `N_c` consumption, `N_p` production) |
| `A` | Transmission arcs `a` — pipelines, liquefiers, LNG ships, regasifiers |
| `R` | Production resource types `r` (R1, R2, R3) |
| `W` | Storage facility types `w` (SEAS, PEAK, LNGS) |
| `D` | Seasons `d` (low / high / peak) |
| `Y` | Years `y` |

Liquefaction and regasification are modelled as **arcs between auxiliary nodes**, not as node
attributes — so a country exporting both by pipeline and as LNG doesn't get two identical arcs
(PDF p. 51).

### Variables

| Doc | Julia | Meaning |
|---|---|---|
| `q^S_tndy` | `Q_S` | Quantity sold |
| `q^P_tnrdy` | `Q_P` | Quantity produced, by resource |
| `f^A_tzdy` | `F_A` | Arc flow |
| `f^I` / `f^X` | `F_I` / `F_X` | Storage injection / extraction |
| `Δ^A`, `Δ^X`, `Δ^W` | `D_A`, `D_X`, `D_W` | Capacity expansion (arc, extraction, working gas) |
| `p_ndy` | `P` (expression) | Market price (auxiliary) |

### Objective

Maximise `REV + CS − TC − MPA` (Eq. 0.12, PDF p. 52; [`Model.jl:142`](../ggm/GlobalGasModel/src/SubModules/Model.jl#L142)):

- **REV** — sales revenue, priced off the linear inverse demand curve `INT − SLP·ΣQ_S`
- **CS** — consumer surplus, `½ · SLP · (ΣQ_S)²` (Eq. 0.5, PDF p. 50)
- **TC** — production costs (linear + quadratic) + arc/storage operating costs + investment costs
- **MPA** — market power adjustment, `½ · SLP · cv · (Q_S)²` (Eq. 0.7, PDF p. 51)

All terms discounted by `disc[y]` and weighted by season length `days_d[d]`.

### Constraints

| Doc | Julia | What it does |
|---|---|---|
| Eq. 0.2 | `eq_cap_p` ([Model.jl:172](../ggm/GlobalGasModel/src/SubModules/Model.jl#L172)) | Production ≤ capacity, per resource |
| Eq. 0.3 | `eq_mass_bal` ([Model.jl:150](../ggm/GlobalGasModel/src/SubModules/Model.jl#L150)) | Nodal mass balance, loss-adjusted inflows |
| Eq. 0.4 | `eq_stor_cycle` ([Model.jl:162](../ggm/GlobalGasModel/src/SubModules/Model.jl#L162)) | Injections (loss-adjusted) = extractions, within each year |
| Eq. 0.10 | `eq_cap_a`, `eq_cap_x` | Arc / extraction flow ≤ capacity + prior expansions |
| Eq. 0.11 | `eq_cap_w` | Loss-corrected injections ≤ working gas capacity |
| Eq. 0.9 | `eq_lim_a/x/w` | Expansion ≤ per-period maximum |
| — | `eq_lim_sales` ([Model.jl:193](../ggm/GlobalGasModel/src/SubModules/Model.jl#L193)) | **Not in the 2019 doc** — sales cap per trader/node/year |

Two modelling conventions worth remembering:

- **All storage losses are assigned to injection**; extraction loss is zero (PDF p. 50).
- **One-period gap** between investment decision and capacity availability — expansions decided in
  year `y` are usable from `y+1` onward (PDF p. 16 footnote 5; visible as `y2 < y` in the Julia code).
- Production capacity is **exogenous** — only transport and storage expand endogenously (PDF p. 50).

---

## 3. Market power

Conjectural variation approach (PDF p. 22, §3.6; PDF p. 50, §9.4). Parameter `cv ∈ [0,1]` per
supplier / node / year:

- `0` = perfectly competitive
- `1` = Cournot
- in between = partial market power

In the data, `0` must be entered as `EPS` (a literal zero breaks the reader), and an overriding zero
must be written as a small positive number like `0.001`.

Market power **decays over time** by a per-supplier factor, floored at a ratio:

```
value(period) = base_value × MAX(factor ^ n_periods, ratio)
```

2019 values (PDF p. 23, Table 15) — NOR/QAT/DZA/NGA/RUS carry export market power 0.25–0.5, all with
`factor = 0.70`, `ratio = 0.50`. Russia has node-specific overrides (full power in Ukraine, none in
China/Belarus).

---

## 4. Demand side

Each consumption node gets a **linear inverse demand curve per season**, built from reference
consumption, reference price, sector shares, seasonal load, and sector elasticities
(PDF pp. 34–35, §6.2).

Per sector: `int = price_ref · (1 − 1/elas)`, `slp = −price_ref / (elas · cons_ref)`.
Sector curves are then aggregated to node level by harmonic-style summation of slopes — an
approximation, since the true aggregate curve is piecewise linear (PDF p. 35, footnote 19).

**Price elasticities** (fixed, same for every country — *not* adjusted during calibration, PDF p. 14):

| Sector | Elasticity |
|---|---|
| Residential (`RES`) | −0.25 |
| Industry (`IND`) | −0.40 |
| Power (`POW`) | −0.75 |
| Transport (`TRA`) | −0.25 |

**Seasons** (EU perspective, PDF p. 14): low `L` = 183 days, high `H` = 120 days, peak `P` = 62 days.

---

## 5. Key parameter defaults

From `data.xlsx` sheet O (PDF p. 14, **Table 6**) — the single most useful table in the document.
Literature ranges behind these numbers are in Appendices C–E.

| Parameter | Value | Unit | Meaning |
|---|---|---|---|
| `BFPipe` | 7 | €/kcm/1000 km | Pipeline operating tariff |
| `BICPipe` | 109 500 | €/kcm/1000 km/y | Pipeline investment cost (onshore) |
| `BLPipe` | 0.020 | per 1000 km | Pipeline loss fraction |
| `BIPipeOffshMult` | 2 | — | Offshore investment cost multiplier |
| `BFLiq` / `BFReg` | 20 / 10 | €/kcm | Liquefaction / regasification tariff |
| `BICLiq` / `BICReg` | 365 000 / 182 500 | €/kcm/y | Liquefaction / regasification investment |
| `BLLiq` / `BLReg` | 0.100 / 0.015 | — | Liquefaction / regasification loss |
| `BFShip` / `BLShip` | 8 / 0.003 | per 1000 sea miles | Shipping cost / loss |
| `BIStorX` / `BIStorW` | 5 000 / 150 | €/kcm/y, €/kcm | Storage extraction / working gas investment |
| `DistCutOff` | 15 | 1000 sea miles | Max shipping distance (currently non-binding) |
| `CostInfl` / `PriceInfl` | 0.0275 | — | Yearly cost / price inflator |
| `Real` / `DiscRate` | 0.05 / 0.07888 | — | Real / nominal discount rate |
| `YearStep` | 5 | years | Period length |

Literature ranges for sanity-checking: pipelines PDF p. 53 (Table 41), LNG PDF p. 55 (Table 45),
storage PDF p. 63 (Table 59).

### Units

Model units are **kcm / mcm / mcm-per-day**, costs and prices in **€/kcm**. Input files use **bcm** or
**bcma**; storage working gas in mcm, extraction in mcm/d. Conversion `bcm/y → mcm/d` is
`× 1000/365`. Higher heating values throughout. Full unit table: PDF p. 9 (Tables 1–2).

---

## 6. Input data

The Julia port reads **three Excel workbooks** from `ggm/data_2023/`, selected by scenario name.
The scenario string is split on `_`: for `STEPS_NENO`, `scens[1] = "STEPS"` and `scens[2] = "NENO"`.

| Workbook | Sheets | Doc equivalent |
|---|---|---|
| `general_data_<scens[2]>.xlsx` | Other Assumptions, Nodes, Arcs, Vessel Distances, Storages, General Market Power, Specific Market Power, Seasons, Resources, Sales Restrictions | `data.xlsx` sheets O/N/A/V/W/M — PDF pp. 13–23 |
| `projected_data_<scens[1]>.xlsx` | Reference Quantities, Sector Consumption Distribution, Season Consumption Distribution, Consumption Sectors | `data_proj.xlsx` — PDF pp. 24–27 |
| `calibrated_data_<scens[1]>.xlsx` | Global Losses, Production Cost Calibration, Production Capacity Calibration, Price Calibration | `data_calib.xlsx` (GlobLoss / PCostCalib / PCapCalib / PriceCalib) — PDF pp. 28–32 |

Loading code: [`data_load.jl:21–38`](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L21).

**The data is not in the repo.** `ggm/data_2023/` contains only `message.txt`: *"please contact the
authors to receive the data for this run."* Getting it is a prerequisite for any actual model run.

Scenario naming: the 2019 doc uses IEA WEO scenarios `NPS` (New Policies) and `SDS` (Sustainable
Development), combined with SET-Nav EU pathways (`Ref`, `Vision`). The 2023 data uses `STEPS`, the
IEA's rename of NPS.

---

## 7. Calibration

**Read PDF pp. 28–32 before touching calibration parameters** — this is the part most likely to be
done wrong, and the doc is explicit that a badly calibrated model gives biased results that look
plausible.

Key points:

- Calibration adjusts **production costs and capacities, reference prices, and market power**.
  Elasticities are *not* adjusted.
- Base year is calibrated first and alone; future years afterwards.
- Budget realistically: *"several days"* for an experienced analyst, *"several weeks"* after a major
  data revision (PDF p. 28).
- The global market behaves as communicating vessels — changing one country's production cost spills
  over into consumption everywhere.

**Production cost curve** (PDF pp. 29–30, 33–34): the older logarithmic Golombek function was replaced
by a piecewise-linear approximation over three resources. Capacity shares are fixed globally at
R1 = 50%, R2 = 46%, R3 = 4%; the steep tail comes from a high cost multiplier on the small R3 slice.
Only the `base cost` per node is tuned. Slack capacity should be 3–5% above reference production.

**Global losses** (`GlobLoss`, PDF p. 29): outlooks project equal global production and consumption,
but GGM has value-chain losses. Non-European consumption is scaled down by a tuned percentage to
reconcile this. Must be recalibrated per scenario, since LNG volumes vary a lot between scenarios.

The model emits calibration reports comparing outcomes to reference values at country and region
level (PDF pp. 42–43).

---

## 8. Outputs

Result tables written by [`solve_GGM`](../ggm/GlobalGasModel/src/SubModules/Model.jl#L207) to
`ggm/results/outputs/` as `.csv` or `.xlsx`: `D_A`/`D_X`/`D_W` (expansions), `Q_P`/`Q_S`/`Q_C`
(production, sales, consumption), `F_A`/`F_I`/`F_X` (flows), `P` (prices), plus annualised variants.

The 2019 doc describes the equivalent GAMS reports and their layouts — mass balances, calibration
reports, infrastructure utilisation — at PDF pp. 41–47. Useful as a guide to what a sensible result
table looks like, and for the utilisation-rate definitions.

---

## 9. Where the Julia port differs from the PDF

| | PDF (GAMS v3.0, 2019) | `ggm/` (Julia, 2023) |
|---|---|---|
| Language | GAMS | Julia + JuMP |
| Solver | CPLEX (QCP) | **Gurobi** (Ipopt also a dependency) |
| Horizon | 2015–2060 | **2020–2060** ([`ggm_2023.jl:7`](../ggm/ggm_2023.jl#L7)) |
| Input files | `data.xlsx`, `data_proj.xlsx`, `data_calib.xlsx` | `general_data_*`, `projected_data_*`, `calibrated_data_*` |
| Sheet names | `O`, `N`, `A`, `V`, `W`, `M` | Full words — see §6 |
| Scenarios | `NPS-Ref`, `SDS-Vision` | `STEPS_*` — underscore-separated, split into two parts |
| Sales restrictions | absent | `eq_lim_sales` constraint + "Sales Restrictions" sheet |
| Resources, seasons | hardcoded in sheet O | own sheets, so configurable |

Both solvers are commercial. Gurobi has a free academic licence — relevant for NTNU.

### Flow units — resolved: mcm/day

The Julia variable comments say `mcm/yr`
([`Model.jl:31–40`](../ggm/GlobalGasModel/src/SubModules/Model.jl#L31)). **They are wrong.** The
model works in **mcm/day**, matching the doc (PDF p. 9).

`BCMA_TO_MCMD = 1000/365` is applied to every capacity and reference quantity on load —
`cap_a` ([data_load.jl:125](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L125)), `ref_prod`
([:99](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L99)), `sectoral_reference_consumption`
([:172](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L172)), `d_a_max` ([:127](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L127)).
Annual figures are then recovered as `Σ_d days_d[d] · Q / 1000` → bcm
([Model.jl:137](../ggm/GlobalGasModel/src/SubModules/Model.jl#L137)).

So: **workbook inputs are bcma, internal units are mcm/day, reported annuals are bcm.**

### Production cost curve — open discrepancy with the doc

The Julia code builds the quadratic term as
([data_load.jl:104](../ggm/GlobalGasModel/src/SubModules/data_load.jl#L104)):

```
cost_pq[n,r,y] = base_cost · q(r) · year_factor · inflator / cap_p[n,r,y]
```

and the objective uses `cost_pl·Q_P + ½·cost_pq·Q_P²`, giving marginal cost

```
MC(Q) = cost_pl + cost_pq·Q      ⇒  MC at full capacity = base · (c(r) + q(r)) · factors
```

The doc's worked example (PDF pp. 33–34) instead gives **MC at full capacity = base · q(r)**: with
`base = 12`, `c = 1`, `q = 5` it states 12 at the first unit and **60** at capacity. The Julia
formulation yields **72** for the same inputs.

Either the port redefined `q(r)` as an increment above `c(r)`, or the curves genuinely differ. This
changes the steepness of every production cost curve, so **confirm with the port author before
calibrating anything**. The port is by Lukas Barner (TU Berlin) per
[`GlobalGasModel/Project.toml`](../ggm/GlobalGasModel/Project.toml).

### Workbook schemas are recoverable without the data

`data_load.jl` references every workbook column by literal string, so the full expected schema of all
three files can be read straight out of the source even though `data_2023/` is empty — e.g.
`"Reference Production <year>"`, `"<year> Capacity (bcma)"`, `"Length (1000 km)"`,
`"Base Cost (EUR/kcm)"`, `"c(<resource>)"`, `"Maximum Expansion First Period"`. Enough to build
synthetic fixtures and develop against them before the real data arrives.

---

## 10. Quick page index

| Topic | PDF pages |
|---|---|
| Units and conversions | 9 |
| Model structure overview | 10 |
| Base parameter table (Table 6) | 14 |
| Nodes, regions | 15–16 |
| Arcs: pipelines, liquefaction, regasification | 16–19 |
| LNG shipping distances | 19–20 |
| Storage data and types | 20–22 |
| Market power data | 22–23 |
| Production & consumption projections | 24–27 |
| Calibration | 28–32 |
| Parameter calculations (prod, cons, arcs, storage) | 33–36 |
| References | 37–38 |
| How to run (GAMS) | 39–41 |
| Output reports and layouts | 41–47 |
| **Mathematical formulation** | **48–52** |
| Pipeline cost/loss literature | 53–54 |
| LNG value chain literature | 55–62 |
| Storage literature | 63 |
