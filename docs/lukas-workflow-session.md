# Workflow session with Lukas — question guide

A guide for one long session with Lukas Barner. The goal is to gather everything chapter 3
(§3.4 workflow, §3.5 effort) and chapter 5 (*Where AI fits*) need.

*Drafted 2026-10-14. Builds on [`questions-for-weekly-meeting.md`](questions-for-weekly-meeting.md),
whose questions 2–5, 8 and 9 are folded in here. Afterwards, move the answers there under
**Resolved**, and correct [`workflow-task-inventory.md`](workflow-task-inventory.md) wherever
practice differs from the documentation.*

Chapter 5 asks four things of each workflow step:

1. What happens today?
2. What does the step need?
3. What could an agent do?
4. Where does a person stay involved?

Lukas can answer the first two and part of the fourth. The third is ours to argue. The questions
therefore focus on **what actually happens** and **what judgment it takes**.

★ marks the questions to keep if time runs short.

---

## How to run the session

- **Ask him to show rather than tell.** Have him share his screen and open the real files. Ask
  "What would you click next?" more than "How does it work?"
- **Follow one concrete case end to end.** Ideally this is how the 2023 dataset and its scenarios
  were built. If he didn't do that himself, use the last scenario he did build.
- **Ask whether you may record it.** Otherwise, one person asks and the other takes notes.
- **Ask whether you may cite him** as a personal communication (for example, "Barner, pers. comm.,
  October 2026"). Many of the claims in chapter 5 will rest on this session.
- **Bring:**
  - the list of sheets in the three workbooks;
  - the calibration table in [`ggm-data-2023.md` §5](ggm-data-2023.md#5-the-calibration--what-actually-gets-tuned);
  - the six-step diagram from the inventory.

---

## 0. Orientation

1. ★ **Which of the steps below have you done yourself?** Who did the rest: Franziska, someone at
   DIW, or a past student? Who should we ask about the parts you haven't done?
2. ★ **Is the 2019 documentation still accurate?** It describes the GAMS-era workflow. What changed
   with the Julia port, and what stayed the same?
3. **Who uses GGM today, and for what?** How many people, and are they mostly writing papers or
   doing commissioned studies?
4. ★ **Can you sketch the whole process for one project, from research question to published
   figure?** Draw it together, then check it against our six steps:
   - get source data
   - prepare the data
   - set up the scenario
   - calibrate
   - run the model
   - read the results

   What's missing or in the wrong order? What steps exist that nobody wrote down?
5. **Who built the 2023 dataset, when, and how long did it take overall?**

## 1. Getting source data

**Today**

1. ★ **For each sheet, which source does it come from?** Walk through the sheet list together.
   Which edition of the World Energy Outlook (WEO) and which PRIMES run is the 2023 data based on?
2. **Who has access to the proprietary sources** (IEA WEO, PRIMES, GIIGNL, Cedigaz)? Under what
   licence, and in what form do they arrive: PDF, Excel, or a database export?
3. **How do you notice that a source has been updated?** Is data refreshed on a schedule, or only
   when a project needs it?
4. ★ **When a new edition comes out, do you re-extract everything, or compare it with last year's?**
5. **Have any sources changed or disappeared since 2019?** For example, BP's Statistical Review is
   now published by the Energy Institute. What replaced them?
6. **Where are the raw downloads kept?** Is there an archive of exactly what the 2023 data was
   built from?

**What it needs**

7. **When two sources disagree, how do you choose?** Can you give an example?
8. **Which data is hardest to find or most often missing?** Which countries, and which kinds of
   infrastructure?
9. **Do you use anything that isn't a formal source** — news, company announcements, your own
   estimates? How are those recorded?

## 2. Preparing the data

**Today**

1. ★ **Are the three upstream spreadsheets still in use?** These are `WEO_Scenarios_Input_data.xlsx`,
   `gas_demand_production_europe.xlsx` and `regional_split.xlsx` (PDF p. 24). Can we see them?
2. **Are the regional split shares for USA, Canada, Russia, China and India still based on 2015, or
   have they been updated?**
3. **Which unit conversion factors are used, and where are they kept?** Do they differ by country?
4. **Are the interpolation rules still the documented ones** (2045 = Δ×0.9, 2050 = Δ×0.72, flat
   after 2055)?
5. ★ **How is new infrastructure added**, such as a new LNG terminal or pipeline? Who decides when a
   planned project counts — at final investment decision (FID), under construction, or only when in
   operation?
6. **How are parallel pipelines aggregated, and how are terminals assigned to representative
   ports?** Is this written down anywhere?
7. **Is any of this preparation done in code (Python, Julia, VBA) rather than spreadsheet formulas?**

**What it needs**

8. ★ **Which rules live only in someone's head?** The documentation names traps such as marketed
   versus gross production and country-specific conversion factors. What else belongs on that list?
9. **How do you check the prepared data before using it?** Do you have scripts, eyeball checks, or
   comparisons against the previous version?
10. **How long does a full data update take, and which part is slowest?**

## 3. Setting up a scenario

**Today**

1. ★ **What do the codes mean?** The scenarios are `NCA`, `MCA`, `FFF` and `TZE`; the variants are
   `NENO`, `SQAB` and `EUSD`. Which combination is the reference run? (Our guesses are in
   [`ggm-data-2023.md` §3–4](ggm-data-2023.md#3-the-three-general-variants).)
2. ★ **Walk us through creating a new scenario.** Do you copy the workbooks and edit them? Which
   sheets do you touch? Is there any tooling?
3. ★ **How do you turn a research question into model changes?** Take the Russia ban as the example:
   - Which arcs count as Russian supply to the EU?
   - When does the ban take effect, given the gap between investment and availability?
   - Do you also zero the expansion limits, or use sales restrictions instead (`EUSD`)?
4. **Which knock-on changes do you have to remember?** For example: expansion limits elsewhere,
   market power at zero volume, demand response. Is there a checklist, written or mental?
5. **Where do the market power values come from, and when are they changed?** They are the same in
   all four 2023 scenarios.
6. **How often do you build a genuinely new scenario, compared with running variations of an existing
   one?** How many scenarios does a typical paper use?
7. ★ **How do you keep track of versions?** File names, folders, git? Can you always tell which files
   produced which results?
8. **Who decides the scenario design** — the researcher, a client, or a co-author?

## 4. Calibration — the key part

Give this the most time. If possible, ask him to demonstrate on one country.

**Today**

1. ★ **What do you calibrate against?** Is it base-year production, consumption, prices or trade
   flows, and where do those observed values come from? For future years, are the targets simply the
   WEO projections?
2. ★ **What is the order?** Base year first, then future years? Which parameter do you touch first,
   and why?
3. ★ **Walk through one iteration:** run, compare, adjust, rerun. What exactly do you look at, and in
   which file or plot?
4. ★ **The documentation gives three causes when a country under-produces:** costs too high,
   willingness to pay too low, or market power too high (PDF p. 28). How do you decide which one it
   is?
5. **Do you work node by node or globally?** How do you handle changes spilling over to other
   countries?
6. ★ **How do you know when to stop?** Is "close enough" a number, and is it written down?
7. ★ **How many iterations and hours does it take?** Compare the base year with a new scenario's
   future years.
8. ★ **About 1,700–2,050 values change from one 2023 scenario to the next.** Are those tuned by hand,
   or derived by a formula or script? This answer decides whether that work is judgment or mechanics.
9. **Why is capacity slack 0–2.4 % when the documentation recommends 3–5 %?**
10. ★ **Is there a calibration script outside the public repo?** The code has an unused calibration
    hook (`GGM_CalibrationTargets`) and an unused input that scales demand (`calib_int`). Was this
    work started and then dropped?
11. **The model doesn't produce a calibration report.** How do you compare results with the reference
    values today?

**What it needs**

12. ★ **Do any records of past calibrations exist** — notes, intermediate files, emails? Could we get
    them? A trace of expert reasoning is the best possible benchmark for an agent.
13. **What does a failed calibration look like?** When do you stop tuning and change the input data
    instead?
14. **Would two experienced analysts end up with the same calibration?** How much room is there for
    defensible disagreement?
15. **Who decides that a calibration is good enough?**

## 5. Running the model

1. **How do you start a run** — a Julia script, the REPL, or a cluster? On which machine, and with
   which Gurobi licence?
2. **How long does one scenario take to run, and how much memory does it need?**
3. **How often do runs fail?** When the model is infeasible, how do you find the cause?
4. **Which warnings in the log do you read, and which do you ignore?** Is the ∞ → 10,000 fallback in
   `FFF` and `TZE` known and accepted?
5. **How do you run a batch of scenarios?**
6. ★ **Could you help us get a working setup**, so we can run the 2023 data ourselves?

## 6. Reading the results

1. ★ **Which output files does a run produce, and in what format?** Could we have one complete output
   set, for example `NENO` with `NCA`?
2. ★ **What do you look at first?** What are your sanity checks?
3. **How do you get from raw output to the figures and tables in a paper?** Are there scripts for
   that?
4. ★ **How do you tell a real result from a data error?** Can you give an example?
5. **Which parts of interpretation are routine** (describing what changed) **and which are
   judgment** (explaining why it matters)?

## 7. Where it goes wrong

1. ★ **Has a scenario ever solved cleanly but answered the wrong question?** That is, it ran fine and
   gave plausible numbers, but the setup didn't match what was intended. Push hardest on this one:
   one real example is the most valuable evidence the thesis can have.
2. **Which mistakes recur** in data preparation, scenario setup or calibration?
3. **How was a bad run caught, when it was caught?**
4. **Has an error ever been found after results were shared or published?**

## 8. Effort and frequency (for §3.5)

1. ★ **Roughly what share of the time goes to each of the six steps?** Ask separately for:
   - a full data update;
   - a new scenario on existing data.
2. **How often does each of those happen per year?**
3. **What is the most tedious part?** Which part would you most like to have automated?

## 9. Agents and human oversight (for "where a person stays involved" and chapter 6)

1. ★ **Which steps would you trust an agent with, if you reviewed the result?** Which would you never
   hand over?
2. **What would you need to see to trust an agent's output** — cited sources, a diff against the
   previous version, a log of its reasoning?
3. **What would make reviewing faster than doing the work yourself?**
4. ★ **Can licensed data be sent to a cloud LLM?** Would sending IEA or PRIMES data to the Claude API
   breach the licence terms? If so, this limits the design.

## 10. Earlier automation

1. **Are there scripts, macros or helper tools anyone has written around GGM?** These count as prior
   work we should credit, and they show which problems are already solved.
2. **What felt repetitive while you were porting the model to Julia?**

## 11. Loose ends in the 2023 dataset

Ask only if time allows. These are questions 8 and parked items in the weekly list.

- Is storage operating cost (OPEX) labelled in USD but used as EUR?
- Is `DistCutOff` unused on purpose?
- Shipping loss is set to 1 % per 1,000 sea miles, against a documented 0.25–0.4 %. Is that
  deliberate?
- The minimum market power ratio is 1, which switches off the market power decay. Intended?
- Are the production cost curves steeper than documented on purpose?

---

## Ask for these before you leave

- [ ] The three upstream spreadsheets, or whatever replaced them
- [ ] A list of the source behind each sheet in the 2023 data
- [ ] Any calibration notes, intermediate files or scripts
- [ ] One complete output set from a run
- [ ] Any scripts for pre-processing, calibration or post-processing
- [ ] Setup instructions for running the model ourselves
- [ ] Permission to cite him as a personal communication
- [ ] A later chance to watch a real data update or calibration, if one is coming up
- [ ] Who else to talk to about the steps he hasn't done himself
