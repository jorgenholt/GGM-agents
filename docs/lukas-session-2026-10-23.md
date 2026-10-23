# Workflow session with Lukas Barner — 23 October 2026

Notes from a 2 h 46 min Teams session in which Lukas walked Jørgen and Save through the three GGM
workbooks on his own machine, explained where each part comes from, and described how he would
structure an agent workflow.

**Sources.** Recording and transcript are in `data/lukas-session/` (local only, gitignored).
The transcript was made locally with Whisper (large-v3-turbo), because the Teams transcript came out
as Norwegian. Screens were read from 509 frames extracted at every screen change; workbook values were
checked against our copy in `data_2023/` where he showed the 2023 data.

**How to read this.** Timestamps `[h:mm]` point into the recording. Statements are what Lukas *said*
unless marked **[screen]** (seen on his screen) or **[interpretation]** (our reading, not his words).
Whisper does not separate speakers; questions are attributed to "we" (Jørgen or Save). Lukas consented
to the recording at [0:07].

---

## The short version

1. **The projections workbook is the most judgment-heavy part, not the calibration alone.** Reference
   production and consumption are a *storyline* loosely aligned with an outlook (IEA WEO, or Energy
   Institute statistics), adjusted node by node by the analysts. "All of the data in this are made up"
   apart from the anchoring aggregates [0:18]; you cannot reverse-engineer it from, or into, the IEA
   data [0:19]. Franziska does most of this; about a week full time [0:31]. Lukas thinks it is the
   least suited to automation, and there may be "a good reason for potentially not touching this" [0:35].
2. **Elasticities, sector shares and seasonality are also judgment.** No data set exists for them
   anywhere [0:39, 0:47]. They are copied from earlier work, or rebuilt per project.
3. **The general workbook is "the more agent-friendly" one** [1:14]: mostly factual data (ENTSOG, EIA,
   Global Energy Monitor, shipping distances), adjusted by scenario assumptions such as Nord Stream or
   the Strait of Hormuz being open or closed. Lukas already uses AI for the mapping work here [1:46].
4. **Calibration is done entirely by hand, with no script, and takes several days full time** [2:12].
   It is a two-sided problem (production costs and prices), and every change has knock-on effects, so
   it is trial and error with a model run between each step [2:13–2:15]. He calibrates two scenarios in
   parallel: adjusting one while the other runs [2:15]. He would find an agent that runs the model
   locally and adjusts the factors "kind of cool" [2:05].
5. **Market power is "gut feeling plus some type of calibration"** [2:00], set per scenario, and also
   used to encode long-term contracts and to correct implausible results [2:01].
6. **His proposed agent workflow** [2:26–2:31]: agree baseline scenarios → propose a node structure
   (human review) → production and consumption (review) → elasticities (review) → seasonality (review) →
   general data from sources → initial calibration values researched → run locally and let the agent
   adjust. Every value should carry its source and a confidence level [0:55, 2:35]. Model runs should
   happen on local hardware, not inside the agent system [2:31].

---

## 1. How the data are organised

- **[screen] [0:08]** His `GGM` folder holds one data folder per project, each with its own run script:
  `data_2023`, `data_2023_milan`, `data_2023_no_ruegen`, `data_2023_PARIS`, `data_2023_TAI`,
  `data_2023_with_links`, `data_2025_new`, `data_hormuz`, `data_old`; scripts `ggm_2023.jl`,
  `ggm_2023_no_ruegen.jl`, `ggm_hormuz.jl`; and `results`, `results_no_ruegen`.
  **[interpretation]** A new study is set up by copying a data folder and a run script, not through
  any tooling.
- **[screen] [1:22]** His `data_2023` folder also contains `general_data_UPIF.xlsx` and a
  `_dropboxdata` folder, neither of which is in our copy.
- **Two scenario dimensions** [0:09–0:12, 1:20–1:24]:
  - *Climate scenarios* set the projections and calibration workbooks: NCA = no climate ambition
    (roughly IEA's Stated Policies; once called STEPS), MCA = moderate climate ambition, TZE = described as "a bit
    of a more ambitious version than the net zero emissions version of IEA" (wording unclear in the audio), FFF = "fossil and fissile free": ambitious climate policy
    plus a nuclear phase-out, so gas demand is higher in the interim and falls more steeply later.
  - *Geopolitical scenarios* set the general workbook: NENO = new normal, SQAB = status quo ante bellum,
    EUSD = European supply disruption. Explained in the 2025 paper (Barner et al., 2025) [1:22].
  - Runs combine the two as a matrix: three climate × three geopolitical scenarios = nine runs, or any
    chosen subset [1:20].
- **[screen] [1:22]** `ggm_2023.jl` takes the scenario from the command line (`scen = ARGS[1]`), with
  the old `"STEPS_NENO"` commented out. You pass e.g. `FFF_NENO` [1:23].
- **[screen] [0:46, 1:10]** `data_hormuz` (October 2026) has `projected_data_Baseline`,
  `calibrated_data_Baseline` and general variants `Hormuz`, `NoHormuz`, `NoHormuzRussia`,
  `NoHormuzRussiaEXP`. It is a one-year model run [0:09] with about 90 nodes instead of 137 [1:04],
  no seasonality and no storage [0:51].

## 2. Projected data (`projected_data_*`)

### Reference Quantities [0:13–0:36]

- One column of reference production and one of reference consumption per model year, for every
  production or consumption node [0:13].
- **Sourcing** [0:15–0:28]: "roughly based" on IEA World Energy Outlook scenarios, or in other studies on
  Energy Institute statistics [0:17]. The aggregates are kept "roughly similar", then the analysts
  deviate where they find the outlook implausible ("we rather think the US in total probably goes
  towards 920") and split country totals across nodes using state or regional statistics [0:24].
  "There is no wrong and right" [0:26]: scenarios tell a story, aligned with a known publication so
  readers can place it [0:24].
- **Granularity is a choice**: the node structure is not fixed (137 nodes in 2023, about 90 for Hormuz:
  three Russian nodes, one Canadian node, fewer US nodes) [1:04–1:05].
- **US split**: from state-level consumption (IEA/EIA statistics) mapped to model regions; for Hormuz the
  US regions follow the EIA's state-to-state pipeline capacity regions, which are close to but not
  the census regions [1:06–1:09]. **[screen] [1:09]** The EIA "Interregional Natural Gas Pipeline
  Capacity" map.
- **Russia**: regional consumption is "mostly made up", using GDP shares as a proxy; he once asked an AI
  to search Russian sources but could not verify the result [1:13].
- **Workload**: "a lot of manual work and it really takes a lot of time" [0:17]; back and forth between
  the analysts [0:30]; Franziska would need "maybe a week" full time [0:31]. Done by "somebody with a
  lot of experience in the sector": Franziska [0:23, 0:57].
- **Iteration**: they aim for a complete, coherent storyline before running, then make small
  corrections when results show something implausible, e.g. a short export boom that cannot justify
  the infrastructure [0:20–0:22, 0:31].
- **Scenarios are not meant to be likely**, but interesting and coherent: the Russian supply
  disruption scenarios were run long before anyone thought them realistic [0:33, 2:22].
- **Supporting spreadsheets**: "a thousand different non-standardized Excel sheets" lying around, many
  made by Ruud Egging [1:03].
- **[screen] [0:46]** The Hormuz projections sheet is at country level with columns *Reference
  Production 2025*, *Reference Consumption 2025* and *Unadjusted Reference Consumption 2025*; for some
  countries the two consumption columns differ (e.g. Qatar 37.9 vs 46.5).

### Consumption Sectors and Sector Consumption Distribution [0:36–0:47]

- Four sectors with fixed elasticities (residential, industry, power, transport); transport could be
  dropped [0:37]. The node's elasticity is weighted by its sector shares, which vary by year [0:41].
- For Hormuz he replaced the sectors with low/mid/high/very-high elasticity "sectors" and weights per
  node [0:40, 0:46].
- "There's not a global database" of gas demand elasticities, let alone projected ones; estimates come
  from scattered country studies of varying age [0:39, 0:45–0:47]. Missing nodes copy a similar country
  [0:42].

### Season Consumption Distribution [0:48–0:52]

- Multipliers on average daily consumption per season (e.g. Germany about 0.7 in the low season and 1.5
  in the peak). Taken from earlier work by Ruud [0:49]. For Hormuz seasonality was dropped, since
  storage costs are small relative to prices [0:50–0:51].

### Lukas on automating this workbook [0:52–0:56, 0:35]

- Least suited to automation of all the workbooks. An agent could collect data (regulators' websites,
  papers, similar countries) and produce "a halfway completed dataset", but it "would still require
  definitely manual oversight" [0:54].
- The agent must report **why** it chose each value: found on an official site and recent; from an old
  report; inferred from a similar country (and which similarities); or "a wild guess" [0:55].

## 3. General data (`general_data_*`) [1:14–2:02]

"The more agent friendly data sets": "a lot less manual guesswork… a lot more hard facts" [1:14–1:15].

| Sheet | What he said | Source | Time |
|---|---|---|---|
| Other Assumptions | Base fees, investment costs, loss rates, offshore multiplier (2–3), distance cut-off, year step, season days (183/120/62), storage costs, inflators. Values from the documentation, sometimes updated from company or government reports. Rarely changed for scenarios, though any value could be | GGM documentation, reports | [1:15–1:31] |
| Nodes | Flags for consumption, production, storage, liquefaction, regasification. Unneeded flags are set to false to keep the model sparse. LNG terminals are separate `L…`/`R…` nodes, linked by an arc of distance 1 whose capacity is the terminal capacity | Derived from other sheets | [1:34–1:39] |
| Arcs | Pipelines and LNG arcs, start capacity plus later capacity. Usage cost factor normally 1 and maximum expansion e.g. 100, raised by hand to stop implausible flows | ENTSOG (Europe), EIA state-to-state (US), Global Energy Monitor (rest of the world) | [1:39–1:48] |
| Storages | Working gas, extraction, opex (about 30 USD/kcm, under 10% of price). Seasonal, peak and LNG types | EIA; ENTSOG/GIE | [1:48–1:50] |
| Vessel Distances | Port-to-port distances, recomputed whenever a terminal is added. Very large distances used to block routes (the Hormuz runs) | Computed with the Python library *scgraph* from terminal coordinates (GEM) | [1:51–1:53] |
| Sales Restrictions | Sanctions and politically blocked trade, e.g. Russia to Finland; also to stop small Iranian sales into Europe through Turkey | Scenario choice | [1:57–1:59] |
| General and Specific Market Power | "Gut feeling plus some type of calibration"; scenario-based; specific values force outcomes (Russia–Belarus at 0) and stand in for long-term contracts | Judgment | [2:00–2:01] |
| Seasons, Resources | Season names and lengths (one "only season" works without code changes); three production cost blocks | Model design | [1:33, 2:01] |

- **Pipeline data in practice** [1:40–1:47]: capacities are reported per country pair or state pair and
  must be mapped to model nodes and aggregated. GEM data splits pipelines into segments at borders, so
  capacities sometimes need inferring by hand [1:44]. "This is what I'd say I have used AI most heavily
  in the past for": mappings and lookup tables [1:46].
  **[screen] [1:01]** A folder `GGM_data/arcs/pipelines` with `EIA_state_to_state.csv`,
  `ENTSOG_system_capacity.csv`, `GEM-GGIT-Gas-Pipelines-2025-11.xlsx` and a Julia script
  `run_pipe_extraction_stuff.jl` (June 2026). **[interpretation]** Part of the arc data preparation is
  already scripted.
- **Adding an LNG terminal** means a new node in Nodes, a line in Arcs, and new rows in Vessel Distances;
  the projections are untouched [1:57]. Zero-capacity terminals are kept as investment options (e.g.
  Germany before 2022, Ukraine, Estonia) [1:54–1:56].
- **Changing the model through data only**: the code was designed so that structural choices such as
  the number of seasons are made in the workbooks, not in Julia [1:33].

## 4. Calibrated data (`calibrated_data_*`) [2:02–2:19]

- **Global Losses**: a scaling constant to reconcile production, consumption and losses; zero here
  [2:02].
- **Production Cost Calibration**: linear (c) and quadratic (q) coefficients per cost block, usually
  left as they are, since there is no data to shape the curve [2:06–2:07]. A base cost per node times a
  year factor, tuned so that outcomes match the scenario: "no data at all… really tweaked based on the
  model outcomes" [2:05].
- **Production Capacity Calibration**: block shares 50/46/4% and a slack factor (e.g. 1.05; cheap
  producers more, such as 1.1–1.75; expensive ones close to 1) [2:07–2:09].
- **Price Calibration**: base reference price times a year factor [2:09]; seasonal price factors from
  historical spreads (e.g. Germany ±10%), normally the same across scenarios [2:10–2:12].
- **Process**: "Is there some sort of calibration script? Nope. I do this by hand… several days full
  time" [2:12]. On the ~2,000 values that change between 2023 scenarios: "sounds a bit too large but
  not entirely implausible" [2:13]. Two-sided calibration (costs and prices) is much harder than
  one-sided [2:13]. Runs two scenarios at a time, calibrating one while the other solves [2:15].
  Starts from the outcomes of an old run [2:16].
- **Diagnosing a deviation** [2:17–2:19]: first check whether production, consumption or both are off.
  If production is too high but consumption is right, exports are too high: either a data problem
  (export capacity that should not be there, or too cheap) or calibration (costs too low, or too much
  spare capacity). Then change the parameter that is closest to plausible. "This is like trial and error."
- **Pitfall for an LLM** [2:25]: official gas prices in countries with subsidised domestic consumption
  are far below the implied price the model needs; LLMs "are not super good at distinguishing" them.

## 5. Lukas's view of an agent workflow [2:26–2:41]

1. Agree on the baseline reference scenarios to model.
2. Propose a node structure from what country statistics and pipeline/LNG data exist (EIA, ENTSOG, GEM),
   including liquefaction and regasification nodes. **Human review.**
3. Production and consumption profiles for the scenario. **Human review.**
4. Elasticity weights. **Human review.**
5. Seasonal distribution. **Human review.**
6. General data, updated from the sources for the agreed node structure.
7. Initial calibration values: research base prices, seasonal spreads and production cost estimates;
   rough capacity slack.
8. Run the model locally and let the agent adjust the calibration. He is unsure whether this works and
   "would actually be interested to see" [2:30].

- **Run on local hardware**, exchanging only results with the agent; running inside the agent system
  would use up credits for no benefit [2:31–2:33].
- **Interface** [2:35–2:38]: show each value with its source and confidence category; offer alternative
  approaches side by side; let the reviewer upload an edited workbook with a column for overrides and
  notes ("I think this should be 5, check again"); allow looping back.
- **Architecture** [2:40]: separate workflows per workbook, sharing one node structure.
- **Summary in his words** [2:42–2:43]: everything in the projections has some judgment; the general data
  are factual data adjusted by scenario assumptions; in calibration, base prices and price spreads can be
  researched, "but for the rest this is again then trial and error".

## 6. Other remarks

- Setting up a new study is a real decision because of the effort: for the Hormuz runs they waited
  about a month to see whether the situation would last [2:39].
- Lukas recommends going through the workbooks ourselves "once or twice more" [2:41].
- People: Ruud Egging built much of the earlier data and seasonal patterns [0:49, 1:03]; Franziska does
  the projections; Lukas does calibration and the general data.

---

## What this changes in our work

**[interpretation]** for each item; the docs named here are updated accordingly.

- **The four-layer view of inputs needs correcting** (`workflow-task-inventory.md`). Projections are not
  "read off an outlook"; they are a judgment-heavy storyline. Elasticities, sector shares and
  seasonality are judgment, not literature parameters. Only the general workbook is mostly collected
  data. The judgment is in two places, not one: the projections (Franziska) and the calibration (Lukas).
- **Chapter 3 overstates how much input is collected.** §1.4, §3.3 and §3.5 say most input is collected
  and follows documented rules. That holds for the general workbook only. To fix.
- **Calibration practice is now confirmed**, no longer inferred: by hand, no script, several days, two
  scenarios in parallel, diagnosis by direction. The unused calibration hook in the code was not
  discussed; still open.
- **The thesis gap is strengthened.** Judgment is not only in calibration but in the scenario
  projections, which have no ground truth by design ("there is no wrong and right").
- **Agent design**: Lukas's eight-step workflow with review gates matches the "LLM proposes, code
  computes, person decides" principle from chapter 2; his provenance-and-confidence requirement is a
  concrete spec for chapter 5's job descriptions.
- **Open**: what `general_data_UPIF` is; whether the pipeline extraction script and the Hormuz data could
  be shared; whether the 2023 calibration started from an older run's calibration file.
