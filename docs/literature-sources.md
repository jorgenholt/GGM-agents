# Literature and sources

Every source found so far that could matter for the project thesis, grouped by what it is about,
with what it covers and where in the thesis it would be used.

*Compiled 2026-10-13 by literature search (arXiv, OpenAlex, Semantic Scholar, Crossref) and web
search for grey literature. Builds on, and supersedes, the candidate list in
[`project-thesis-structure.md` §3](project-thesis-structure.md#3-literature-review--candidates); the
gap argument still lives there.*

> **How far this has been checked.** Every entry below was confirmed to exist, with title, authors,
> year and identifier checked against arXiv, Crossref or OpenAlex. Grey-literature pages were opened
> or confirmed reachable. **Descriptions are based on abstracts or the page itself, not full reads.**
> Entries marked *(title only)* had no abstract available. Verify a claim against the source before
> citing it.

**Legend**

- **Type:** `peer` peer-reviewed · `preprint` arXiv/SSRN, not yet peer-reviewed · `book` ·
  `WP` working paper or institute report · `grey` blog, company guide, documentation
- **Chapters:** 2 literature review · 3 GGM · 4 LLM agents · 5 where AI fits · 6–8 design sketch,
  discussion, conclusion
- **Priority:** ★★★ read in full, likely cited · ★★ cite and skim · ★ background, optional

Many of the closest papers are **2026 preprints**. That is unavoidable in a field moving this fast,
but say so in chapter 2. Where a preprint and a peer-reviewed version both exist, cite the
peer-reviewed one.

---

## Contents

- [The short version: read these first](#the-short-version-read-these-first)
- [A. GGM and its lineage](#a-ggm-and-its-lineage)
- [B. Energy-modelling practice](#b-energy-modelling-practice)
- [C. LLM agents that calibrate existing simulation models](#c-llm-agents-that-calibrate-existing-simulation-models)
- [D. LLM agents that set up and run existing simulation codes](#d-llm-agents-that-set-up-and-run-existing-simulation-codes)
- [E. LLMs and optimisation models](#e-llms-and-optimisation-models)
- [F. LLMs and agents in the energy sector](#f-llms-and-agents-in-the-energy-sector)
- [G. Agents in scientific and economic research](#g-agents-in-scientific-and-economic-research)
- [H. Agent foundations](#h-agent-foundations)
- [I. Limits and failure modes](#i-limits-and-failure-modes)
- [J. Measuring capability, evaluation and cost](#j-measuring-capability-evaluation-and-cost)
- [K. The task-based economics of automation](#k-the-task-based-economics-of-automation)
- [L. Human oversight of automation](#l-human-oversight-of-automation)
- [M. Data preparation and spreadsheets](#m-data-preparation-and-spreadsheets)
- [N. Non-scientific sources](#n-non-scientific-sources)
- [What was searched for and not found](#what-was-searched-for-and-not-found)
- [Corrections to the earlier list](#corrections-to-the-earlier-list)

---

## The short version: read these first

If there is only time for about fifteen sources, these carry the most weight, in rough reading order:

| # | Source | Why it matters |
|---|---|---|
| 1 | Egging & Holz (2019), GGM documentation [A] | The source of truth for chapter 3 and the calibration-burden evidence |
| 2 | Gómez-Guillén et al. (2026), agentic calibration of grey-box models [C] | The closest single paper: an LLM as the calibration optimiser |
| 3 | Zhu et al. (2026), *(Human) Attention Is (Still) All You Need* [G] | Experimental evidence for "LLMs reason, code computes, humans gate", our design principle |
| 4 | Zhu et al. (2026), pAI-Econ-claude [G] | Names our gap almost word for word: no machine-readable correctness signal. **Must be addressed in chapter 2** |
| 5 | Li et al. (2026), HydroAgent [C] | Frontier LLMs fall short of expert calibrators. The best counter-evidence |
| 6 | Samigullin et al. (2026), PetroGraph history matching [C] | Calibration in an energy domain, with human checkpoints |
| 7 | Abulawi et al. (2026), AutoSAM [D] | Input generation from documents, with assumed values labelled |
| 8 | Li et al. (2026), MOOSEnger [D] | The harness matters more than the model; running is not the same as being right |
| 9 | Li et al. (2023), OptiGuide · Chen et al. (2026), OptiChat [E] | LLMs that explain and diagnose an *existing* optimisation model |
| 10 | Schluntz & Zhang (2024), *Building effective agents* [N] | The workflow-versus-agent distinction chapter 4 needs |
| 11 | Eloundou et al. (2024) · Autor, Levy & Murnane (2003) [K] | The task-based framework that chapter 5's step-by-step method implicitly uses |
| 12 | Parasuraman, Sheridan & Wickens (2000) [L] | The standard vocabulary for "where a person stays involved" |
| 13 | Dell'Acqua et al. (2026), jagged frontier [K] | Why suitability must be judged per task, not per job |
| 14 | Silvast et al. (2020), ethnography of energy modellers [B] | What modellers' tacit judgment actually is: the thing that resists automation |
| 15 | Chen et al. (2024), ScienceAgentBench [G] | Argues for assessing agents step by step in a scientific workflow before claiming end-to-end automation, which is chapter 5's method |

---

## A. GGM and its lineage

The model itself, its predecessors, and recent applications. Mostly for **chapter 3**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Egging, R. & Holz, F. (2019). *Global Gas Model: Model and Data Documentation v3.0*. DIW Data Documentation 100. [doi:10.18723/diw_ddc:2019-100](https://doi.org/10.18723/diw_ddc:2019-100) · local copy [`ggm-documentation-v3.0.pdf`](ggm-documentation-v3.0.pdf) | WP | The model, its data and calibration. States that calibration takes an experienced analyst days to weeks (PDF pp. 28–32) | Ch3 backbone; ch5 evidence of manual burden; ch2 intro sketch | ★★★ |
| Egging, R. et al. (2010). The World Gas Model: A multi-period mixed complementarity model for the global natural gas market. *Energy* 35. [doi:10.1016/j.energy.2010.03.053](https://doi.org/10.1016/j.energy.2010.03.053) | peer | The direct predecessor of GGM: players, MCP structure, illustrative results | Ch3: where the model comes from and why it is an MCP | ★★★ |
| Egging, R., Baltensperger, T. & Tomasgård, A. (2020). Solving oligopolistic equilibrium problems with convex optimization. *European Journal of Operational Research* 284(1), 44–52. [doi:10.1016/j.ejor.2020.01.025](https://doi.org/10.1016/j.ejor.2020.01.025) | peer | *Added 2026-10-28.* Shows that partial equilibrium models with market power (Cournot or conjectural variations) can be written as one optimisation problem by adding market power terms to welfare maximisation; equivalent to the complementarity form and orders of magnitude faster to solve | Ch3: why GGM is solved as a single quadratic programme (§3.2) | ★★ |
| Egging, R. et al. (2008). A complementarity model for the European natural gas market. *Energy Policy* 36. [doi:10.1016/j.enpol.2008.01.044](https://doi.org/10.1016/j.enpol.2008.01.044) | peer | The European forerunner (GASMOD lineage) | Ch3 history, one sentence | ★ |
| Egging, R. G. & Gabriel, S. A. (2006). Examining market power in the European natural gas market. *Energy Policy* 34. [doi:10.1016/j.enpol.2005.04.018](https://doi.org/10.1016/j.enpol.2005.04.018) | peer | Market power representation in gas equilibrium models | Ch3: why market power values exist and why they are judgment, not data | ★★ |
| Gabriel, S. A. et al. (2005). A mixed complementarity-based equilibrium model of natural gas markets. *Operations Research* 53. [doi:10.1287/opre.1040.0199](https://doi.org/10.1287/opre.1040.0199) | peer | Foundational MCP gas-market model (North America) | Ch3: methodological roots | ★ |
| Gabriel, S. A. et al. (2013). *Complementarity Modeling in Energy Markets*. Springer. [doi:10.1007/978-1-4419-6123-5](https://doi.org/10.1007/978-1-4419-6123-5) | book | The textbook on MCP energy models; has a chapter on natural gas market modelling | Ch3: cite for MCP basics instead of explaining from first principles | ★★ |
| Conejo, A. J. et al. (2020). Complementarity, not optimization, is the language of markets. *IEEE Open Access Journal of Power and Energy*. [doi:10.1109/oajpe.2020.3029134](https://doi.org/10.1109/oajpe.2020.3029134) | peer | Short argument for why market models are complementarity problems | Ch3: one-paragraph justification of the MCP form for a non-specialist reader | ★ |
| Huppmann, D. & Egging, R. (2014). Market power, fuel substitution and infrastructure – a large-scale equilibrium model of global energy markets. *Energy* 75. [doi:10.1016/j.energy.2014.08.004](https://doi.org/10.1016/j.energy.2014.08.004) | peer | Multi-fuel extension of the same modelling family | Ch3: context, optional | ★ |
| Huppmann, D. (2013). Endogenous production capacity investment in natural gas market equilibrium models. *EJOR* 231. [doi:10.1016/j.ejor.2013.05.048](https://doi.org/10.1016/j.ejor.2013.05.048) | peer | Investment decisions inside gas equilibrium models | Ch3: only if capacity expansion is discussed | ★ |
| Egging, R. (2013). Benders decomposition for multi-stage stochastic MCPs – applied to a global natural gas market model. *EJOR* 226. [doi:10.1016/j.ejor.2012.11.024](https://doi.org/10.1016/j.ejor.2012.11.024) | peer | Solution methods for large stochastic versions | Ch3: only if solve time or model size is discussed | ★ |
| Holz, F., Richter, P. M. & Egging, R. (2015). A global perspective on the future of natural gas: resources, trade, and climate constraints. *Review of Environmental Economics and Policy* 9. [doi:10.1093/reep/reu016](https://doi.org/10.1093/reep/reu016) | peer | A GGM application written for a policy audience | Ch3: what kind of question GGM answers | ★★ |
| Holz, F. (2015). Modeling coal and natural gas markets. *Emerging Trends in the Social and Behavioral Sciences*. [doi:10.1002/9781118900772.etrds0223](https://doi.org/10.1002/9781118900772.etrds0223) | book | Overview of how coal and gas market modelling has developed, from optimisation to complementarity | Ch3: compact overview chapter by our supervisor | ★★ |
| Barner, L., Holz, F., von Hirschhausen, C. & Kemfert, C. (2025). Is Russian gas still needed in the European Union? Model-based analysis of long-term scenarios. *Energy Strategy Reviews* 58, 101646. [doi:10.1016/j.esr.2025.101646](https://doi.org/10.1016/j.esr.2025.101646) · earlier SSRN preprint (2024) [doi:10.2139/ssrn.4843902](https://doi.org/10.2139/ssrn.4843902) | peer | Recent GGM scenario study: Russian supply levels against climate ambition. *Published 2025 — found 2026-10-15; cite this version, not the preprint* | Ch1/ch3: a concrete recent use; ch5: a real example of "set up the scenario" | ★★★ |
| Holz, F., von Hirschhausen, C. & Kemfert, C. (2008). A strategic model of European gas supply (GASMOD). *Energy Economics* 30(3), 766–788. [doi:10.1016/j.eneco.2007.01.018](https://doi.org/10.1016/j.eneco.2007.01.018) | peer | *Added 2026-10-15.* Holz's earlier strategic (oligopoly) model of European gas supply, a direct forerunner of GGM's market-power representation | Ch1/ch3: the modelling lineage our supervisor comes from | ★ |
| Holz, F., Barner, L., Kemfert, C. & von Hirschhausen, C. (2024). DIW Weekly Report 21/2024. [doi:10.18723/diw_dwr:2024-21-1](https://doi.org/10.18723/diw_dwr:2024-21-1) | WP | Policy-facing GGM results (already used in the GDPval talk) | Ch3/ch5: what the "read the results" output looks like in practice | ★★ |
| Egging-Bratseth, R. et al. (2026). Developing the Global Oil and Gas Market Model. *EEM 2026*. [doi:10.1109/eem68581.2026.11589638](https://doi.org/10.1109/eem68581.2026.11589638) | peer | Extension of the GGM family to oil and gas, by GGM's co-author *(title only)* | Ch3: the model family is still developing. Ruud Egging-Bratseth is, as far as we know, at NTNU, so possibly a useful local contact. Confirm | ★ |
| Hecking, H. & Panke, T. (2012). COLUMBUS – a global gas market model. EWI WP 12/06. [PDF](https://www.ewi.uni-koeln.de/cms/wp-content/uploads/2017/01/EWI-WP-12-06-COLUMBUS%E2%80%93A-global-gas-market-model.pdf) | WP | A competing global gas model (Cologne) | Ch3: "GGM is one of several". Optional | ★ |
| Chyong, C. K. et al. (2023). Market power and long-term gas contracts: the case of Gazprom in Central and Eastern European gas markets. *The Energy Journal* 44. [doi:10.5547/01956574.44.1.cchy](https://doi.org/10.5547/01956574.44.1.cchy) | peer | Another global gas simulation model, applied to a competition case | Ch3: the same alternative-models point | ★ |
| [GGM_public on GitHub](https://github.com/Franziska-Holz/GGM_public) and [DIW Berlin: Models & Tools](https://www.diw.de/en/diw_01.c.599753.en/models___tools.html) | grey | The Julia code (MIT licence). DIW's page confirms the current version is in Julia and lists Barner's HydrOGEnMod | Ch3: cite the code version used | ★★ |

---

## B. Energy-modelling practice

How energy models are built, used and trusted. Supports **chapter 3** (the workflow and its judgment)
and **chapter 7** (what should stay with people).

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Silvast, A. et al. (2020). What do energy modellers know? An ethnography of epistemic values and knowledge models. *Energy Research & Social Science* 66. [doi:10.1016/j.erss.2020.101495](https://doi.org/10.1016/j.erss.2020.101495) | peer | Ethnographic study of what energy modellers actually know and value | Ch3/ch5: the tacit judgment in the workflow, from outside our own reading of the docs. Strong support for "some steps stay with people" | ★★★ |
| DeCarolis, J. et al. (2017). Formalizing best practice for energy system optimization modelling. *Applied Energy* 194, 184–198. [doi:10.1016/j.apenergy.2017.03.001](https://doi.org/10.1016/j.apenergy.2017.03.001) | peer | Principles and steps for an energy-model analysis: research question, boundaries, running, uncertainty, communication | Ch3: an external description of the modelling workflow to set against GGM's; ch5: the steps line up with ours | ★★★ |
| Pfenninger, S. et al. (2018). Opening the black box of energy modelling: strategies and lessons learned. *Energy Strategy Reviews* 19. [doi:10.1016/j.esr.2017.12.002](https://doi.org/10.1016/j.esr.2017.12.002) | peer | Transparency, documentation and reproducibility of energy models | Ch5/ch7: agent actions must be at least as traceable as a human's | ★★ |
| Pfenninger, S. et al. (2017). The importance of open data and software: is energy research lagging behind? *Energy Policy* 101. [doi:10.1016/j.enpol.2016.11.046](https://doi.org/10.1016/j.enpol.2016.11.046) | peer | Licensing and openness of energy data | Ch3: why GGM's public repo ships without data, and what that means for an agent | ★ |
| Süsser, D. et al. (2021). Model-based policymaking or policy-based modelling? How energy models and energy policy interact. *Energy Research & Social Science* 75. [doi:10.1016/j.erss.2021.101984](https://doi.org/10.1016/j.erss.2021.101984) | peer | How scenario choices and model results feed into policy, and back | Ch7: scenario design is a value-laden choice, so a human sets it | ★★ |
| Elder, I. D. et al. (2026). Energy systems models are diagnostic tools, not projection machines. arXiv:[2604.19676](https://arxiv.org/abs/2604.19676) | preprint | Argues models should be used to explain and explore uncertainty, not to predict | Ch5 "read the results": supports an agent that explains results rather than asserting forecasts | ★★ |
| Cao, K.-K. et al. (2016). Raising awareness in model-based energy scenario studies — a transparency checklist. *Energy, Sustainability and Society*. [doi:10.1186/s13705-016-0090-z](https://doi.org/10.1186/s13705-016-0090-z) | peer | A checklist of what a scenario study must document | Ch5/ch6: a ready-made spec for what a scenario-setup agent must record | ★★ |
| Garb, Y. et al. (2008). Scenarios in society, society in scenarios: toward a social scientific analysis of storyline-driven environmental modeling. *Environmental Research Letters* 3. [doi:10.1088/1748-9326/3/4/045015](https://doi.org/10.1088/1748-9326/3/4/045015) | peer | How narrative storylines get translated into model parameters | Ch5 "set up the scenario": a narrative-to-parameters translation is exactly what an LLM would be asked to do | ★ |
| Kotzur, L. et al. (2021). A modeler's guide to handle complexity in energy systems optimization. *Advances in Applied Energy* 4. [doi:10.1016/j.adapen.2021.100063](https://doi.org/10.1016/j.adapen.2021.100063) | peer | Aggregation and complexity reduction in energy models | Ch5 "prepare the data": spatial and temporal aggregation | ★ |

### Calibration before LLMs

*Added 2026-10-15* to give chapter 2 its historical context: automated calibration and the debate
over what calibration can establish predate LLMs by decades.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Kydland, F. E. & Prescott, E. C. (1996). The computational experiment: an econometric tool. *Journal of Economic Perspectives* 10(1), 69–85. [doi:10.1257/jep.10.1.69](https://doi.org/10.1257/jep.10.1.69) | peer | The case for calibrating model economies to answer quantitative questions | Ch2: calibration as an established, and contested, method in economics | ★★ |
| Hansen, L. P. & Heckman, J. J. (1996). The empirical foundations of calibration. *Journal of Economic Perspectives* 10(1), 87–104. [doi:10.1257/jep.10.1.87](https://doi.org/10.1257/jep.10.1.87) | peer | Questions whether calibrated parameters are well founded; asks that parameter uncertainty and sensitivity be reported routinely | Ch2 gap / ch7: a calibration is a set of choices that must be documented and tested for sensitivity | ★★ |
| Dawkins, C., Srinivasan, T. N. & Whalley, J. (2001). Calibration. In *Handbook of Econometrics* 5, 3653–3703. [doi:10.1016/S1573-4412(01)05011-5](https://doi.org/10.1016/S1573-4412(01)05011-5) | book | Survey of calibration in applied general equilibrium models: choosing parameters so the model reproduces a benchmark, and its limits | Ch2 gap: the economics reference for calibrating equilibrium models | ★★ |
| Beven, K. (2006). A manifesto for the equifinality thesis. *Journal of Hydrology* 320(1–2), 18–36. [doi:10.1016/j.jhydrol.2005.07.007](https://doi.org/10.1016/j.jhydrol.2005.07.007) | peer | Many different parameter sets can reproduce observations equally well (equifinality) | Ch2 gap: non-unique calibrations are known in hydrology too; what differs for GGM is that the parameters carry economic meaning | ★★ |
| Duan, Q., Sorooshian, S. & Gupta, V. K. (1992). Effective and efficient global optimization for conceptual rainfall-runoff models. *Water Resources Research* 28(4), 1015–1031. [doi:10.1029/91WR02985](https://doi.org/10.1029/91WR02985) | peer | The SCE-UA algorithm; notes that unique optimal parameter values are often impossible to find | Ch2: automatic calibration is three decades old; SCE-UA is a baseline in the LLM calibration papers | ★ |
| Oliver, D. S. & Chen, Y. (2011). Recent progress on reservoir history matching: a review. *Computational Geosciences* 15(1), 185–221. [doi:10.1007/s10596-010-9194-2](https://doi.org/10.1007/s10596-010-9194-2) | peer | Review of automated history matching | Ch2: background to PetroGraph | ★ |
| Kennedy, M. C. & O'Hagan, A. (2001). Bayesian calibration of computer models. *Journal of the Royal Statistical Society B* 63(3), 425–464. [doi:10.1111/1467-9868.00294](https://doi.org/10.1111/1467-9868.00294) | peer | Calibration as statistical inference about uncertain parameters of a computer model | Ch2: background to the Bayesian baselines | ★ |

---

## C. LLM agents that calibrate existing simulation models

**The closest cluster to this thesis.** All are recent, and most are preprints. For **chapter 2**,
with chapter 5 citing back to it for the calibration step.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Gómez-Guillén, D. et al. (2026). Agentic calibration of grey-box simulation models: an LLM-driven alternative. arXiv:[2607.18308](https://arxiv.org/abs/2607.18308) | preprint | An LLM acts as the optimiser for calibrating a disease simulation model (anal cancer), against Nelder–Mead and Bayesian optimisation. Constraints are given in plain language; each iteration comes with a written rationale, so the search is auditable. Fewer model evaluations, but more inference time per iteration | Ch2 anchor paper. Ch5 calibration: "constraints as text" and an auditable rationale match GGM's judgment-heavy calibration. Its target is still an *observed* quantity, which is our gap. *Read in full 2026-10-15:* 10 parameters; targets are age-specific incidence from a published meta-analysis; LLM is Qwen3.6 27B run locally; 16 evaluations vs 110 (BO) and 486–21,917 (Nelder–Mead), but 4–7× BO's wall-clock time; rationales argued to be auditable but not tested with human reviewers (§3.1.5, §4, §5) | ★★★ |
| Li, Z. et al. (2026). HydroAgent: closing the gap between frontier LLMs and human experts in hydrologic model calibration via simulator-grounded RL. arXiv:[2605.17792](https://arxiv.org/abs/2605.17792) | preprint | Benchmarks nine frontier LLMs (Claude, GPT, Gemini) calibrating the US National Weather Service's flash-flood model. None reaches the human expert, except one model on one gauge. The authors blame missing domain grounding, not model size, and fine-tune a small model on 2,576 calibration trajectories (*corrected 2026-10-15:* distilled from GPT-5 runs, not from human experts) | Ch2/ch7: the strongest evidence that off-the-shelf LLMs do *not* yet match expert calibrators. Use it to keep the argument honest | ★★★ |
| Zhu, Z. et al. (2026). Large language models as calibration agents in hydrological modeling: feasibility and limitations. *Geophysical Research Letters* 53. [doi:10.1029/2025gl120043](https://doi.org/10.1029/2025gl120043) | peer | Five LLMs against two classical optimisers (SCE-UA, NSGA-III). DeepSeek-R1 converged near-optimally within 200 iterations (vs >1,200 and >2,200) with physically interpretable parameters; the other four LLMs did worse than both baselines (abstract) | Ch2: the peer-reviewed counterpart to HydroAgent; shows results depend heavily on which model | ★★ |
| Zhao, Y. et al. (2026). LLM-driven diagnostic reasoning for distributed hydrological model calibration (MADR). Research Square. [doi:10.21203/rs.3.rs-10106384/v1](https://doi.org/10.21203/rs.3.rs-10106384/v1) | preprint | *(title only)* Multi-agent diagnostic reasoning for calibration | Ch5: parallels the idea of an agent that applies written-down diagnostic heuristics (GGM docs, PDF p. 28) | ★ |
| Samigullin, L. et al. (2026). Multi-agentic approach for history matching of oil reservoirs (PetroGraph). arXiv:[2605.15028](https://arxiv.org/abs/2605.15028) | preprint | Reservoir history matching (calibration under another name) split into agents for model review, planning, parameterisation, optimisation, simulation and summary. Validates edited input decks and has human checkpoints. Mismatch falls 95% on a synthetic case but only 13% on the real Norne field | Ch2: calibration in an *energy* domain, with a Norwegian field as test case. Ch6: its agent split is a template to compare against. The synthetic-versus-real drop is worth quoting. *Read in full 2026-10-15:* the human checkpoints were **skipped in all reported experiments** (Table 1), there is no baseline optimiser, and the LLM is Qwen3.5-397B run locally | ★★★ |
| Bai, Y. et al. (2026). LLM-informed efficient Bayesian calibration of building energy simulation models under limited data. *IBPSA conference*. [doi:10.26868/30680611.2026.1308](https://doi.org/10.26868/30680611.2026.1308) | peer | Uses an LLM to choose which parameters to calibrate and to set priors, then calibrates with standard Bayesian methods | Ch5: a middle path, where the LLM supplies the judgment (priors, parameter choice) and ordinary methods do the search | ★★ |

---

## D. LLM agents that set up and run existing simulation codes

Agents that write input files for, run, and repair an existing model, without changing the model
itself. That is the same relationship as ours to GGM. For **chapter 2** and **chapter 6**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Abulawi, Z. et al. (2026). AutoSAM: an agentic framework for automating input file generation for the SAM code with multi-modal RAG. arXiv:[2603.24736](https://arxiv.org/abs/2603.24736) | preprint | Builds nuclear-reactor simulation inputs from PDFs, diagrams and spreadsheets. Extracts parameters into a **human-auditable intermediate representation** (a YAML file experts can edit), flags missing data and labels assumed values. *Read in full 2026-10-15:* a **single** ReAct agent with seven tools, one of which is a rule-based input validator (not a separate agent); 45 of 51 items extracted from PDF text (~88%); verification largely qualitative (§3, §4.5, §6) | Ch2: closest analogue to building GGM workbooks from source reports. Ch5 "prepare the data": the intermediate representation and labelled assumptions are design ideas to borrow | ★★★ |
| Li, M. et al. (2026). MOOSEnger: a simulation-aware AI agent framework for the MOOSE ecosystem. arXiv:[2603.04756](https://arxiv.org/abs/2603.04756) | preprint | A generate–check–repair–run harness around a multiphysics code. Executable success rose from 5% to 89.5% with the harness. The authors stress that running successfully does not establish scientific correctness | Ch4: the system around the model matters more than the model. Ch7: a run that completes is not a right answer | ★★★ |
| Zhang, T. et al. (2025). MooseAgent: an LLM-based multi-agent system for automating MOOSE simulation. SSRN. [doi:10.2139/ssrn.5342542](https://doi.org/10.2139/ssrn.5342542) | preprint | Earlier multi-agent system for the same code *(title only)* | Ch2: optional | ★ |
| Yue, L. et al. (2026). Foam-Agent: an LLM-based multi-agent framework for automating CFD workflows. *Computer Methods in Applied Mechanics and Engineering* 461. [doi:10.1016/j.cma.2026.119271](https://doi.org/10.1016/j.cma.2026.119271) · v2.0 preprint arXiv:[2509.18178](https://arxiv.org/abs/2509.18178) | peer | Multi-agent setup, running and debugging of OpenFOAM fluid simulations | Ch2: the pattern holds in fluid dynamics too | ★★ |
| Pandey, S. et al. (2025). OpenFOAMGPT: a RAG-augmented LLM agent for OpenFOAM-based CFD. *Physics of Fluids* 37. [doi:10.1063/5.0257555](https://doi.org/10.1063/5.0257555) | peer | Retrieval over documentation for configuring a simulation code | Ch2: RAG over model docs (we would do the same over the DIW documentation) | ★ |
| Jiang, G. et al. (2024). EPlus-LLM: an LLM-based computing platform for automated building energy modeling. *Applied Energy* 367. [doi:10.1016/j.apenergy.2024.123431](https://doi.org/10.1016/j.apenergy.2024.123431) | peer | Natural-language building descriptions turned into EnergyPlus models. Heavily cited | Ch2: the most-cited energy-modelling example | ★★ |
| Zhang, L. et al. (2025). Automatic building energy model development and debugging using LLMs agentic workflow. *Energy and Buildings* 327. [doi:10.1016/j.enbuild.2024.115116](https://doi.org/10.1016/j.enbuild.2024.115116) | peer | Agentic workflow that builds and **debugs** EnergyPlus models | Ch5: debugging corresponds to "interpret and repair" pre-run warnings | ★★ |
| Lu et al. (2025). Automated building energy modeling for energy retrofits using an LLM-based multi-agent framework. *iScience*. [doi:10.1016/j.isci.2025.113867](https://doi.org/10.1016/j.isci.2025.113867) | peer | Multi-agent building models for retrofit scenarios. The system is called **Data2BEM** and includes a data-driven *calibration* step against measured performance. Abstract reports total modelling time down by over 90% (48 min versus 8–32 h) with minimal human input, for one Cambridge office building. *Read in full 2026-10-15:* agents are GPT-4-based, but the **calibration search itself is a genetic algorithm** the agents configure; the fit meets ASHRAE Guideline 14 (NMBE 2.91%, CV-RMSE 0.139); the 8–32 h are logged times of one junior and one senior human modeller, 40% of whose time went on calibration | Ch2: an LLM organising calibration while a conventional optimiser searches | ★★ |
| Li, H. et al. (2025). EnergyPlus-MCP: a Model Context Protocol server for AI-driven building energy modeling. *SoftwareX* 32. [doi:10.1016/j.softx.2025.102367](https://doi.org/10.1016/j.softx.2025.102367) | peer | Wraps a simulation engine as MCP tools an LLM can call | Ch6: what "GGM as a tool" might look like technically | ★★ |
| Lee, G. et al. (2026). A knowledge-based multi-agent system using LLMs for automated building energy modeling and simulation service. *Energy and Buildings* 367. [doi:10.1016/j.enbuild.2026.117688](https://doi.org/10.1016/j.enbuild.2026.117688) | peer | *(title only)* | Ch2: optional | ★ |
| Yoo, H. et al. (2026). A validation-aware framework for LLM-driven simulation automation. SSRN. [doi:10.2139/ssrn.7428738](https://doi.org/10.2139/ssrn.7428738) | preprint | *(title only)* | Ch5/ch7: check whether it has a general treatment of validation | ★ |
| Jia, M. et al. (2025). Enhancing LLMs for power system simulations: a feedback-driven multi-agent framework. *IEEE Transactions on Smart Grid* 16. [doi:10.1109/tsg.2025.3589114](https://doi.org/10.1109/tsg.2025.3589114) · arXiv:[2411.16707](https://arxiv.org/abs/2411.16707) | peer | Agents running power-system simulations, with error feedback | Ch2: energy-domain example in a strong journal | ★★ |
| Mao, S. et al. (2027). A trustworthy intent-driven LLM-agent workflow with state verification for power system simulation. *Applied Energy* 427. [doi:10.1016/j.apenergy.2026.128868](https://doi.org/10.1016/j.apenergy.2026.128868) | peer | *(title only)* Checks the simulation's state after each agent action | Ch5/ch6: state verification is the same idea as checking workbook consistency after each edit | ★★ |
| Jin, H. et al. (2025). GridMind: LLM-powered agents for power system analysis and operations. arXiv:[2509.02494](https://arxiv.org/abs/2509.02494) | preprint | Agents coordinate deterministic solvers (AC optimal power flow, contingency analysis) through natural language | Ch4: "the LLM orchestrates, the solver computes" | ★★ |
| Hu, Y. et al. (2025). From natural language to solver-ready power system optimization: an LLM-assisted, validation-in-the-loop framework. arXiv:[2508.08147](https://arxiv.org/abs/2508.08147) | preprint | Argues against letting the LLM produce solutions directly. It should produce a formulation that a solver can handle | Ch4: supports "judgment in, arithmetic out" | ★ |

---

## E. LLMs and optimisation models

Two strands. Most of the literature has LLMs **formulate** models from scratch, which is not our
problem. A smaller strand has LLMs **explain and diagnose an existing model**, which is. For
**chapter 2**, with the second strand reused in **chapter 5** (run the model, read the results).

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Li, B. et al. (2023). Large language models for supply chain optimization (OptiGuide). arXiv:[2307.03875](https://arxiv.org/abs/2307.03875) | preprint | Answers what-if questions about an **existing** optimisation model by having the LLM write code that re-runs the solver. Built so that **proprietary data is never sent to the LLM**: the LLM sees the question and helper-code documentation and writes code that the solver runs locally (§3.1, Fig. 2). 93% average accuracy with GPT-4 on its own benchmark; deployed in Azure's server-placement supply chain | Ch2/ch5: the closest "existing model" analogue. The privacy design matters given our licensed 2023 data | ★★★ |
| Chen, H. et al. (2026). OptiChat: bridging optimization models and practitioners with LLMs. *INFORMS Journal on Data Science* 5. [doi:10.1287/ijds.2025.0074](https://doi.org/10.1287/ijds.2025.0074) · earlier version arXiv:[2308.12923](https://arxiv.org/abs/2308.12923) | peer | Chat interface for **diagnosing infeasible models**. The solver finds the irreducible infeasible subset and the LLM explains it and suggests fixes | Ch5: when a GGM run is infeasible, this is the pattern. Solver gives the facts, LLM gives the explanation | ★★★ |
| Li, Z. et al. (2026). OptArgus: a multi-agent system to detect hallucinations in LLM-based optimization modeling. arXiv:[2605.11738](https://arxiv.org/abs/2605.11738) | preprint | Shows that matching the reference objective value does **not** prove a formulation is correct | Ch7: the direct parallel is that reproducing reference prices does not prove a calibration is right | ★★ |
| AhmadiTeshnizi, A., Gao, W. & Udell, M. (2024). OptiMUS: scalable optimization modeling with (MI)LP solvers and large language models. *ICML 2024*, PMLR 235, 577–596. [proceedings](https://proceedings.mlr.press/v235/ahmaditeshnizi24a.html) · earlier preprint arXiv:[2310.06116](https://arxiv.org/abs/2310.06116) · OptiMUS-0.3 arXiv:[2407.19633](https://arxiv.org/abs/2407.19633) | peer | LLM agent that formulates, codes and debugs MILPs from text | Ch2: the standard reference for the "from scratch" strand we distinguish ourselves from | ★★ |
| Xiao, Z. et al. (2024). Chain-of-Experts: when LLMs meet complex operations research problems. *ICLR 2024*. [proceedings](https://proceedings.iclr.cc/paper_files/paper/2024/hash/d45ee77826332c100a1e15f7765b99ff-Abstract-Conference.html) | peer | Multi-agent OR modelling with a conductor agent coordinating specialists | Ch6: an architecture to compare the design sketch against | ★★ |
| Huang, C. et al. (2025). ORLM: a customizable framework in training large models for automated optimization modeling. *Operations Research*. arXiv:[2405.17743](https://arxiv.org/abs/2405.17743) | peer | Fine-tuned models for optimisation formulation | Ch2: peer-reviewed in an OR flagship journal; one line | ★ |
| Xiao, Z. et al. (2025). A survey of optimization modeling meets LLMs: progress and future directions. *IJCAI 2025*. [doi:10.24963/ijcai.2025/1192](https://doi.org/10.24963/ijcai.2025/1192) | peer | Survey of the formulation strand | Ch2: cite the survey instead of a dozen individual papers | ★★ |
| Xiu, X. et al. (2026). Large language models for operations research: a comprehensive survey. arXiv:[2605.20849](https://arxiv.org/abs/2605.20849) | preprint | Broader, more recent survey | Ch2: alternative to the IJCAI survey | ★ |

---

## F. LLMs and agents in the energy sector

Places the thesis in its field. Mostly power systems and buildings, since **nothing was found on gas
markets** (see [what was not found](#what-was-searched-for-and-not-found)). For **chapter 2**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Majumder, S. et al. (2024). Exploring the capabilities and limitations of LLMs in the electric energy sector. *Joule* 8. [doi:10.1016/j.joule.2024.05.009](https://doi.org/10.1016/j.joule.2024.05.009) | peer | Capabilities and limits of LLMs for energy work, in a high-profile journal. *Read in full (arXiv:2403.09125) 2026-10-15:* tests mostly GPT models; limits listed are scarce domain data, no safety guardrails or uncertainty information, no adherence to physical laws, and cybersecurity/privacy exposure (§3); recommends embedding power-system tools and retrieval | Ch2/ch4: a citable energy-specific "good at / bad at" | ★★★ |
| Forootani, A. et al. (2025). RE-LLM: integrating LLMs into renewable energy systems. arXiv:[2512.01392](https://arxiv.org/abs/2512.01392) | preprint | LLMs built into an energy-system modelling workflow to **explain results to non-expert stakeholders**, alongside optimisation and surrogates | Ch5 "read the results": a direct precedent | ★★ |
| Ren, X. et al. (2025). Can large language model agents balance energy systems? arXiv:[2502.10557](https://arxiv.org/abs/2502.10557) | preprint | LLM agent generates wind scenarios for stochastic unit commitment | Ch2: already on the old list. An LLM generating scenario inputs for an optimisation model | ★★ |
| Akinpelu, D. et al. (2026). How do tool-augmented LLM agents perform on real-world energy analytics tasks? arXiv:[2606.26346](https://arxiv.org/abs/2606.26346) | preprint | Benchmark of 243 expert-curated energy-market tasks with live data tools, regulatory search and optimisation models | Ch4: empirical evidence on agent performance in *energy-market* analysis, the nearest thing to our domain | ★★ |
| Trashchenkov, S. (2026). Power Systems Agent Benchmark: executable evaluation of AI agents in electric power engineering. arXiv:[2606.20950](https://arxiv.org/abs/2606.20950) | preprint | An evaluator recomputes the engineering quantities instead of grading the agent's prose | Ch6/master's: a model for how to evaluate GGM agents with deterministic checks | ★★ |
| Rojas, D. et al. (2026). LLMs and agentic AI systems for smart grids: a tutorial on architectures and applications. arXiv:[2607.18147](https://arxiv.org/abs/2607.18147) | preprint | Tutorial on agent architectures in an energy context | Ch4: an energy-flavoured overview to cite alongside the general surveys | ★ |
| Antonesi, G. et al. (2025). From transformers to LLMs: a systematic review of AI applications in the energy sector towards agentic digital twins. arXiv:[2506.06359](https://arxiv.org/abs/2506.06359) | preprint | Systematic review | Ch2: cite for breadth | ★ |
| Mirshekali, H. et al. (2025). A review of large language models for energy systems. *IEEE Access*. [doi:10.1109/access.2025.3610994](https://doi.org/10.1109/access.2025.3610994) | peer | Review: applications, challenges, prospects | Ch2: peer-reviewed alternative to the preprint reviews | ★ |
| Sommer, A. et al. (2025). Adaptive self-improvement for smarter energy systems using agentic policy search. arXiv:[2501.19340](https://arxiv.org/abs/2501.19340) | preprint | LLMs propose control code, improved through system feedback | Ch2: optional | ★ |
| Golden, D., Indelicato, B., Varshney, L. R., Messina, C. D. & Thornsbury, S. (2026). Agentic AI orchestration of heterogeneous economic models for rapid, multi-scenario analysis of energy crises. arXiv:[2607.23313](https://arxiv.org/abs/2607.23313) | preprint | *Added 2026-10-15, read in full.* An LLM turns a crisis narrative (Strait of Hormuz closure) into scenarios and model-specific inputs for up to 16 existing economic and energy models (CGE, partial-equilibrium, LNG, oil); a deterministic executor runs them and passes outputs downstream. "The language model generates no quantitative results" (abstract). Three mandatory analyst checkpoints; "no autonomous mode". Models are used with existing calibrations, many as literature-calibrated reductions. **Its model registry lists a "Global Gas Model (GGM)", GAMS + CPLEX, status "Real (cfg)", but GGM was not among the models that ran** (§8 Table 2, Fig. 10) | Ch2: the closest paper to this thesis found so far — agents around existing energy-market models, scenario translation, human checkpoints. It orchestrates and does not calibrate, which keeps our gap. Ch6: its architecture (LLM maps, code computes, analyst gates) is our design principle | ★★★ |
| Faiud, I., Khaleghy, H., Schukat, M. & Mason, K. (2026). LLM-assisted behavioural and scenario augmentation for agent-based energy adoption models. arXiv:[2609.04866](https://arxiv.org/abs/2609.04866) | preprint | *Added 2026-10-15.* An LLM writes bounded behavioural rubrics and scenario specifications **offline** for an existing calibrated agent-based model of PV adoption; it is never queried during the simulation, explicitly to protect "reproducibility, interpretability, calibration validity" (§1, §3.2) | Ch2: a second example of keeping the LLM outside a calibrated model and using it for scenario inputs | ★★ |
| Takrouri, M. et al. (2026). WattCouncil: context-aware household energy scenario generation with governed LLMs. *BuildSys 2026*. arXiv:[2607.10720](https://arxiv.org/abs/2607.10720) | peer | Scenario generation by LLMs under explicit governance rules | Ch5 "set up the scenario": the idea of governed scenario generation | ★ |

---

## G. Agents in scientific and economic research

How research workflows are being automated, and how the human role is being argued for. **Chapter 2**
outer ring, and the most important support for **chapters 5 and 7**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Zhu, C. et al. (2026). (Human) attention is (still) all you need: human oversight makes AI-assisted social science reliable. arXiv:[2606.12848](https://arxiv.org/abs/2606.12848) | preprint | Pre-specified 2×4 factorial experiment (the paper says pre-specified, not pre-registered), 280 research runs, one model (Claude Sonnet 4.6). An unconstrained multi-agent pipeline failed critically in 72% of runs. With three rules (LLMs reason but do not execute data work, computation is deterministic, three human decision gates) failures fell to 16%. Code and human gates each help independently | Ch5/ch7: **the experimental evidence for our "judgment in, arithmetic out" principle.** Probably the single most useful paper for the argument | ★★★ |
| Zhu, C. et al. (2026). pAI-Econ-claude: a gated human-in-the-loop multi-agent architecture for AI-assisted economic theory development. arXiv:[2607.21268](https://arxiv.org/abs/2607.21268) | preprint | Starts from the problem that economics tasks have "no cheap, task-complete, machine-readable correctness signal". Gates diagnose failures without certifying correctness; humans keep decisions that are costly to reverse | Ch2 gap: **this overlaps our headline gap claim** (contestable, not measurable). Cite it and narrow our claim: they address economic *theory*, we address calibrated *model parameters* in an existing equilibrium model. See [the note below](#note-on-the-gap-claim) | ★★★ |
| Zhu, C. et al. (2026). HLER: human-in-the-loop economic research via multi-agent pipelines for empirical discovery. arXiv:[2603.07444](https://arxiv.org/abs/2603.07444) | preprint | The pipeline studied in the experiment above: data audit, hypothesis, econometrics, drafting, with human gates. Reports a cost of $0.8–1.5 per run | Ch2: already on the old list. Ch4: a concrete cost figure | ★★ |
| Korinek, A. (2023). Generative AI for economic research: use cases and implications for economists. *Journal of Economic Literature* 61(4). [doi:10.1257/jel.20231736](https://doi.org/10.1257/jel.20231736) | peer | Twenty-five LLM use cases for economists | Ch2/ch4: the standard economics-discipline reference | ★★ |
| Korinek, A. (2025). AI agents for economic research. NBER WP 34202. [doi:10.3386/w34202](https://doi.org/10.3386/w34202) | WP | Practical guide to building research agents (literature, code, data). *Abstract checked 2026-10-15:* includes working code for literature review, econometric coding and data retrieval, using LangGraph | Ch4: how economists are told to build agents. Accessible | ★★ |
| Chen, Z. et al. (2025). ScienceAgentBench: toward rigorous assessment of language agents for data-driven scientific discovery. *ICLR 2025*. arXiv:[2410.05080](https://arxiv.org/abs/2410.05080) | peer | Argues agents should be assessed on **individual tasks in a scientific workflow** before claims of end-to-end automation | Ch5: methodological support for walking through the workflow one step at a time | ★★★ |
| Ren, S. et al. (2025). Towards scientific intelligence: a survey of LLM-based scientific agents. arXiv:[2503.24047](https://arxiv.org/abs/2503.24047) | preprint | Survey | Ch2: anchor the general framing | ★★ |
| Bran, A. M. et al. (2024). Augmenting large language models with chemistry tools (ChemCrow). *Nature Machine Intelligence* 6. [doi:10.1038/s42256-024-00832-8](https://doi.org/10.1038/s42256-024-00832-8) | peer | LLM given expert software tools, with no retraining | Ch4: the "LLM plus domain tools" pattern in a top journal | ★★ |
| Boiko, D. A. et al. (2023). Autonomous chemical research with large language models (Coscientist). *Nature* 624. [doi:10.1038/s41586-023-06792-0](https://doi.org/10.1038/s41586-023-06792-0) | peer | Agent plans and runs lab experiments through tools | Ch2: the landmark example of agents operating scientific equipment | ★ |
| Gottweis, J. et al. (2026). Accelerating scientific discovery with Co-Scientist. *Nature*. [doi:10.1038/s41586-026-10644-y](https://doi.org/10.1038/s41586-026-10644-y) | peer | *(title only)* Google's multi-agent research assistant | Ch2: the current high-profile example | ★ |
| Lu, C. et al. (2024). The AI Scientist: towards fully automated open-ended scientific discovery. arXiv:[2408.06292](https://arxiv.org/abs/2408.06292) | preprint | Fully autonomous research pipeline | Ch2: the "full autonomy" pole we argue against | ★ |
| Gao, C. et al. (2024). LLMs empowered agent-based modeling and simulation: a survey and perspectives. *Humanities and Social Sciences Communications*. [doi:10.1057/s41599-024-03611-3](https://doi.org/10.1057/s41599-024-03611-3) | peer | LLMs *inside* agent-based models | Ch4 terminology: see the note below | ★ |
| Larooij, M. et al. (2025). Validation is the central challenge for generative social simulation. *Artificial Intelligence Review* 59. [doi:10.1007/s10462-025-11412-6](https://doi.org/10.1007/s10462-025-11412-6) | peer | Critical review: LLM-driven simulations are hard to validate | Ch7: validation as the binding constraint, even though their setting differs | ★ |

**Terminology trap for chapter 4.** "Agent" means three things in this literature: an LLM agent
(ours), an agent in an agent-based simulation (Gao et al.; Larooij), and a market player in an
equilibrium model (GGM's producers and traders). Define it once, early.

### Note on the gap claim

The current gap headline ([`project-thesis-structure.md` §3](project-thesis-structure.md#the-gap-to-claim))
says the closest work always calibrates against an observable target, while GGM tunes contestable
economic quantities. That still holds for the **calibration** papers in section C: all of them
calibrate against observations (incidence rates, streamflow, well production).

But pAI-Econ-claude and the HLER experiment show that the "no machine-readable correctness signal"
problem **is now recognised in AI-for-economics**. The defensible version of our gap is narrower:
nobody has looked at it for **calibrating an existing equilibrium model whose parameters encode
market judgment**, where part of the target is observable (reference prices and flows) and part is
not (market power, willingness to pay). That mix is the distinctive feature.

---

## H. Agent foundations

Standard references for **chapter 4**: what an LLM is, what makes it an agent.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Vaswani, A. et al. (2017). Attention is all you need. arXiv:[1706.03762](https://arxiv.org/abs/1706.03762) | peer (NeurIPS) | The transformer architecture | Ch4: one sentence on where LLMs come from | ★ |
| Brown, T. B. et al. (2020). Language models are few-shot learners. arXiv:[2005.14165](https://arxiv.org/abs/2005.14165) | peer (NeurIPS) | GPT-3; learning from instructions and examples in the prompt | Ch4: why prompting works at all | ★ |
| Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. arXiv:[2203.02155](https://arxiv.org/abs/2203.02155) | peer (NeurIPS) | RLHF and instruction following | Ch4: why models follow instructions. Also the root of sycophancy (section I) | ★ |
| Wei, J. et al. (2022). Chain-of-thought prompting elicits reasoning in LLMs. arXiv:[2201.11903](https://arxiv.org/abs/2201.11903) | peer (NeurIPS) | Step-by-step reasoning in text | Ch4: reasoning; written rationales (cf. the grey-box paper) | ★★ |
| Yao, S. et al. (2023). ReAct: synergizing reasoning and acting in language models. arXiv:[2210.03629](https://arxiv.org/abs/2210.03629) | peer (ICLR) | Interleaving reasoning with tool actions: the basic agent loop | Ch4: **the** reference for what an agent does | ★★★ |
| Schick, T. et al. (2023). Toolformer: language models can teach themselves to use tools. arXiv:[2302.04761](https://arxiv.org/abs/2302.04761) | peer (NeurIPS) | Tool use; explicitly motivated by LLMs being weak at arithmetic and lookup | Ch4: why arithmetic goes to tools | ★★ |
| Gao, L. et al. (2022). PAL: program-aided language models. arXiv:[2211.10435](https://arxiv.org/abs/2211.10435) | peer (ICML 2023) | The LLM writes code and the interpreter computes the answer | Ch4: early evidence for "judgment in, arithmetic out" | ★★ |
| Lewis, P. et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. arXiv:[2005.11401](https://arxiv.org/abs/2005.11401) | peer (NeurIPS) | RAG: retrieve documents, then generate | Ch4: how an agent would use the DIW documentation | ★★ |
| Shinn, N. et al. (2023). Reflexion: language agents with verbal reinforcement learning. arXiv:[2303.11366](https://arxiv.org/abs/2303.11366) | peer (NeurIPS) | Agents improving from written feedback on their failures | Ch4: iterative repair loops (calibration, debugging) | ★ |
| Wang, L. et al. (2024). A survey on LLM-based autonomous agents. *Frontiers of Computer Science*. [doi:10.1007/s11704-024-40231-1](https://doi.org/10.1007/s11704-024-40231-1) | peer | The most-cited agent survey | Ch4: cite for the general anatomy of an agent | ★★★ |
| Xi, Z. et al. (2023). The rise and potential of LLM based agents: a survey. arXiv:[2309.07864](https://arxiv.org/abs/2309.07864) | preprint | Second major survey | Ch4: alternative or companion to Wang et al. | ★ |
| Guo, T. et al. (2024). LLM-based multi-agents: a survey of progress and challenges. *IJCAI 2024*. [doi:10.24963/ijcai.2024/890](https://doi.org/10.24963/ijcai.2024/890) | peer | Multi-agent systems | Ch4/ch6: single versus multiple agents | ★★ |
| Wu, Q. et al. (2023). AutoGen: enabling next-gen LLM applications via multi-agent conversation. arXiv:[2308.08155](https://arxiv.org/abs/2308.08155) · Hong, S. et al. (2023). MetaGPT. arXiv:[2308.00352](https://arxiv.org/abs/2308.00352) | preprint | The two best-known multi-agent frameworks | Ch4: examples, one line each | ★ |

---

## I. Limits and failure modes

What LLMs are bad at. For **chapter 4** (good and bad at) and **chapter 7** (risks).

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Huang, L. et al. (2025). A survey on hallucination in LLMs. *ACM Transactions on Information Systems*. [doi:10.1145/3703155](https://doi.org/10.1145/3703155) · arXiv:[2311.05232](https://arxiv.org/abs/2311.05232) | peer | Taxonomy of hallucination | Ch4: the reference for "plausible but wrong" | ★★★ |
| Liu, N. F. et al. (2024). Lost in the middle: how language models use long contexts. *TACL*. [doi:10.1162/tacl_a_00638](https://doi.org/10.1162/tacl_a_00638) | peer | Models miss information placed in the middle of long inputs | Ch4: why you cannot just paste three workbooks into the prompt | ★★ |
| Mirzadeh, I. et al. (2024). GSM-Symbolic: understanding the limitations of mathematical reasoning in LLMs. arXiv:[2410.05229](https://arxiv.org/abs/2410.05229) | peer (ICLR 2025) | Arithmetic reasoning is fragile under small changes | Ch4: weak arithmetic, so calculations go to code | ★★ |
| Sharma, M. et al. (2023). Towards understanding sycophancy in language models. arXiv:[2310.13548](https://arxiv.org/abs/2310.13548) | peer (ICLR 2024) | Models tend to agree with the user's stated beliefs | Ch7: an agent reviewing a modeller's calibration may agree too easily | ★★ |
| Kadavath, S. et al. (2022). Language models (mostly) know what they know. arXiv:[2207.05221](https://arxiv.org/abs/2207.05221) | preprint | Whether models can judge their own correctness | Ch4: can an agent flag its own uncertainty? Partly | ★ |
| Steyvers, M. et al. (2025). What large language models know and what people think they know. *Nature Machine Intelligence*. [doi:10.1038/s42256-024-00976-7](https://doi.org/10.1038/s42256-024-00976-7) | peer | Gap between model confidence and how confident people think it is | Ch7: reviewers over-trust fluent explanations | ★★ |
| Cemri, M. et al. (2025). Why do multi-agent LLM systems fail? arXiv:[2503.13657](https://arxiv.org/abs/2503.13657) | preprint | Taxonomy of multi-agent failures; gains over single agents often small | Ch6: argue for few agents, not many | ★★ |
| Mitchell, M. et al. (2025). Fully autonomous AI agents should not be developed. arXiv:[2502.02649](https://arxiv.org/abs/2502.02649) | preprint | Position paper: risks grow with autonomy level | Ch7: the ethical case for human gates | ★ |

Non-determinism has no good peer-reviewed reference yet. See Thinking Machines (2025) in
[section N](#n-non-scientific-sources).

---

## J. Measuring capability, evaluation and cost

How good agents are, how that is measured, and what it costs. For **chapter 4** (model choice and
cost) and for the master's thesis (how to evaluate).

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Kwa, T. et al. (2025). Measuring AI ability to complete long tasks. *NeurIPS 2025*. arXiv:[2503.14499](https://arxiv.org/abs/2503.14499) | peer | METR's "time horizon": length of task an AI completes with 50% success, doubling roughly every seven months | Ch4: how fast capability is moving. Pair with METR's 2026 caveats note (section N) | ★★★ |
| Patwardhan, T. et al. (2025). GDPval: evaluating AI model performance on real-world economically valuable tasks. arXiv:[2510.04374](https://arxiv.org/abs/2510.04374) | peer (ICLR 2026) | Expert-graded comparison on real occupational tasks. Fully worked up in [`../gdpval-presentation/assets/sources.md`](../gdpval-presentation/assets/sources.md) | Ch4: what models can do on expert work. Reuse the presentation material | ★★ |
| Kapoor, S. et al. (2024). AI agents that matter. arXiv:[2407.01502](https://arxiv.org/abs/2407.01502) | preprint | Agent benchmarks ignore cost; accuracy must be reported together with cost | Ch4: the cost section. Justifies comparing token cost with analyst time | ★★★ |
| Jimenez, C. E. et al. (2024). SWE-bench: can language models resolve real-world GitHub issues? arXiv:[2310.06770](https://arxiv.org/abs/2310.06770) | peer (ICLR) | The benchmark that defined agentic coding | Ch4: one line on how agent capability is measured | ★ |
| Zheng, L. et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. arXiv:[2306.05685](https://arxiv.org/abs/2306.05685) | peer (NeurIPS) | Using LLMs to grade LLMs, and its biases | Master's: whether an LLM may grade a calibration rationale | ★ |
| Yehudai, A. et al. (2026). A survey on evaluation of LLM-based agents. *Findings of ACL 2026*. [doi:10.18653/v1/2026.findings-acl.1330](https://doi.org/10.18653/v1/2026.findings-acl.1330) | peer | Survey of agent evaluation | Ch6/master's: how to know an agent worked | ★★ |

---

## K. The task-based economics of automation

**A framework the thesis does not use yet, and probably should.** Chapter 5 splits a workflow into
tasks and asks which an AI can do. That is exactly the method of the task-based literature in labour
economics, and citing it gives chapter 5 an established economic basis, which suits an Industrial
Economics thesis. For **chapter 4** (which tasks suit an LLM) and **chapter 5**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Autor, D. H., Levy, F. & Murnane, R. J. (2003). The skill content of recent technological change: an empirical exploration. *QJE* 118(4). [doi:10.1162/003355303322552801](https://doi.org/10.1162/003355303322552801) | peer | The routine/non-routine task framework | Ch5: the origin of "decompose jobs into tasks, ask which are automatable". GGM's layers 1–3 are routine; layer 4 is not | ★★★ |
| Acemoglu, D. & Restrepo, P. (2019). Automation and new tasks: how technology displaces and reinstates labor. *JEP* 33(2). [doi:10.1257/jep.33.2.3](https://doi.org/10.1257/jep.33.2.3) | peer | Automation removes some tasks and creates new ones | Ch7: agents create new tasks too (reviewing agent output, writing specifications) | ★★ |
| Eloundou, T. et al. (2024). GPTs are GPTs: labor market impact potential of LLMs. *Science* 384. [doi:10.1126/science.adj0998](https://doi.org/10.1126/science.adj0998) | peer | Rates each occupational task by LLM "exposure", with and without tools | Ch5: **the closest methodological template** — a task-by-task suitability rating, distinguishing LLM alone from LLM plus software | ★★★ |
| Dell'Acqua, F. et al. (2026). Navigating the jagged technological frontier. *Organization Science* 37. [doi:10.1287/orsc.2025.21838](https://doi.org/10.1287/orsc.2025.21838) | peer | Field experiment with consultants. AI helps a lot on tasks inside its frontier and *hurts* on tasks just outside, which look similar | Ch4/ch5: why suitability must be judged task by task. Ch7: the danger of the task that looks automatable but is not | ★★★ |
| Brynjolfsson, E., Li, D. & Raymond, L. (2025). Generative AI at work. *QJE* 140. [doi:10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044) | peer | Productivity effects in a customer-support field study; biggest gains for the least experienced | Ch7: who benefits. A new analyst gains more than Franziska would | ★★ |
| Noy, S. & Zhang, W. (2023). Experimental evidence on the productivity effects of generative AI. *Science* 381. [doi:10.1126/science.adh2586](https://doi.org/10.1126/science.adh2586) | peer | Writing-task experiment | Ch4: one line on measured productivity effects | ★ |
| Handa, K. et al. (2025). Which economic tasks are performed with AI? Evidence from millions of Claude conversations. arXiv:[2503.04761](https://arxiv.org/abs/2503.04761) | preprint | The Anthropic Economic Index: what tasks people actually use AI for, mapped to O*NET | Ch4: what AI is used for in practice, as opposed to what it could do | ★ |
| Tolan, S. et al. (2021). Measuring the occupational impact of AI: tasks, cognitive abilities and AI benchmarks. *JAIR*. [doi:10.1613/jair.1.12647](https://doi.org/10.1613/jair.1.12647) | peer | Links tasks to cognitive abilities to AI benchmarks | Ch5: a way to connect "what the step needs" to "what AI can do" | ★ |

---

## L. Human oversight of automation

The classic human-factors literature. Gives chapter 5's fourth question ("where a person stays
involved") a theoretical basis. For **chapters 5, 6 and 7**.

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Parasuraman, R., Sheridan, T. B. & Wickens, C. D. (2000). A model for types and levels of human interaction with automation. *IEEE Trans. SMC – Part A* 30. [doi:10.1109/3468.844354](https://doi.org/10.1109/3468.844354) | peer | Four functions (gather information, analyse, decide, act), each automated to a different level | Ch5: a ready-made scale for the summary figure. Each GGM step gets a level per function | ★★★ |
| Bainbridge, L. (1983). Ironies of automation. *Automatica* 19. [doi:10.1016/0005-1098(83)90046-8](https://doi.org/10.1016/0005-1098(83)90046-8) | peer | Automating the routine parts leaves people with the hardest parts and less practice at them | Ch7: if agents do routine calibration, who keeps the skill to catch a bad one? | ★★★ |
| Parasuraman, R. & Manzey, D. H. (2010). Complacency and bias in human use of automation. *Human Factors* 52. [doi:10.1177/0018720810376055](https://doi.org/10.1177/0018720810376055) | peer | Automation bias: people over-rely on automated advice | Ch7: a human sign-off gate is weak if the human rubber-stamps | ★★ |
| Simkute, A. et al. (2024). Ironies of generative AI: understanding and mitigating productivity loss in human-AI interactions. arXiv:[2402.11364](https://arxiv.org/abs/2402.11364) | preprint | Bainbridge's ironies applied to generative AI | Ch7: the modern restatement | ★★ |
| Feng, K. J. K., McDonald, D. W. & Zhang, A. X. (2025). Levels of autonomy for AI agents. arXiv:[2506.12469](https://arxiv.org/abs/2506.12469) | preprint | Five autonomy levels defined by the user's role (operator, collaborator, consultant, approver, observer) | Ch5/ch6: an agent-specific alternative to Parasuraman's levels | ★★ |

---

## M. Data preparation and spreadsheets

A GGM scenario *is* three Excel workbooks, and most of the input work is extract-transform-load. For
**chapter 5** steps "get source data" and "prepare the data".

| Source | Type | What it covers | Use in thesis | ★ |
|---|---|---|---|---|
| Narayan, A. et al. (2022). Can foundation models wrangle your data? *PVLDB* 16(4). [doi:10.14778/3574245.3574258](https://doi.org/10.14778/3574245.3574258) | peer | LLMs on data cleaning, entity matching and imputation | Ch5 "prepare the data": early evidence LLMs can do wrangling tasks | ★★ |
| Ma, Z. et al. (2024). SpreadsheetBench: towards challenging real world spreadsheet manipulation. *NeurIPS 2024*. arXiv:[2406.14991](https://arxiv.org/abs/2406.14991) | peer | Benchmark from real user spreadsheet questions; models perform far below humans | Ch5: realistic capability on spreadsheet edits | ★★ |
| Zhu, J. et al. (2026). SpreadsheetBench 2: evaluating agents on end-to-end business spreadsheet workflows. arXiv:[2606.29955](https://arxiv.org/abs/2606.29955) | preprint | Whole workflows rather than single edits | Ch5: the more recent, workflow-level numbers | ★★ |
| Li, H. et al. (2023). SheetCopilot: bringing software productivity to the next level through LLMs. arXiv:[2305.19308](https://arxiv.org/abs/2305.19308) | peer (NeurIPS) | LLM controls a spreadsheet application through defined actions | Ch5: a tool interface rather than free-form editing | ★ |
| Dong, H. et al. (2024). Encoding spreadsheets for large language models (SpreadsheetLLM). *EMNLP 2024*. [doi:10.18653/v1/2024.emnlp-main.1154](https://doi.org/10.18653/v1/2024.emnlp-main.1154) | peer | How to fit large spreadsheets into a model's context | Ch5: GGM workbooks are too big to paste in whole | ★ |
| Schilling-Wilhelmi, M. et al. (2024). From text to insight: LLMs for chemical data extraction. *Chemical Society Reviews*. [doi:10.1039/d4cs00913d](https://doi.org/10.1039/d4cs00913d) | peer | Review of extracting structured numbers from documents with LLMs | Ch5 "get source data": a domain where extraction from reports is well studied | ★ |
| Panko, R. R. (2016). What we don't know about spreadsheet errors today. arXiv:[1602.02601](https://arxiv.org/abs/1602.02601) · Powell, S. G. et al. (2009). Impact of errors in operational spreadsheets. *Decision Support Systems*. [doi:10.1016/j.dss.2009.02.002](https://doi.org/10.1016/j.dss.2009.02.002) | WP / peer | Human spreadsheet error rates | Ch5/ch7: **the human baseline is not error-free.** An agent should be compared with a person, not with perfection | ★★ |

---

## N. Non-scientific sources

Company engineering guides, practitioner blogs, institutional reports and documentation. On agent
*design* these are often ahead of the papers, and several are cited widely in academic work too.
Cite them as grey literature with the access date.

### Agent design guidance

| Source | What it covers | Use in thesis | ★ |
|---|---|---|---|
| Schluntz, E. & Zhang, B. (2024, Dec 19). [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). Anthropic | **Workflows** (predefined code paths) versus **agents** (the LLM directs its own process). Start with the simplest solution; agents trade cost and latency for flexibility. Five workflow patterns | Ch4: the clearest definition of the distinction. Ch5: most GGM steps are *workflows*, not agents. That is a useful finding in itself | ★★★ |
| Anthropic (2025, Jun 13). [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | Multi-agent beat single-agent by 90.2% on their research eval, but used about 15× the tokens of chat. Poor fit when agents must share context or depend on each other | Ch4: concrete cost numbers. Ch6: GGM's tightly coupled workbooks are the "shared context" case where multi-agent is a poor fit | ★★★ |
| Anthropic (2025, Sep 11). [Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Few well-scoped tools; clear naming; return useful context and actionable errors | Ch6: how GGM's functions would be exposed as tools | ★★ |
| Anthropic (2025, Sep 29). [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Curating what is in the model's context, beyond prompt wording | Ch4: managing context limits with large workbooks and long documentation | ★★ |
| Yan, W. (2025, Jun 12). [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents). Cognition · follow-up (2026, Apr 22) [Multi-agents: what's actually working](https://cognition.com/blog/multi-agents-working) | Share full context; conflicting decisions between agents give bad results. The 2026 follow-up: multiple agents can contribute, but writes should stay single-threaded | Ch6: an industry counterweight to multi-agent designs. Only one agent should edit the workbooks | ★★ |
| OpenAI (2025, Apr). [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Layered guardrails; escalate to a human on repeated failure or high-risk actions | Ch5/ch6: practical rules for when the agent hands over to a person | ★★ |
| Weng, L. (2023, Jun 23). [LLM powered autonomous agents](https://lilianweng.github.io/posts/2023-06-23-agent/) | The planning–memory–tool use anatomy of an agent | Ch4: a widely cited overview | ★ |
| Willison, S. (2025, Sep 18). [I think "agent" may finally have a widely enough agreed upon definition](https://simonwillison.net/2025/sep/18/agents/) | "An LLM agent runs tools in a loop to achieve a goal" | Ch4: a crisp working definition to quote | ★★ |
| Husain, H. (2024). [Your AI product needs evals](https://hamel.dev/blog/posts/evals/) | Practical evaluation: test cases, traces, when to trust LLM judges | Master's: building the evaluation | ★ |
| Anthropic (2024, Nov 25). [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | The standard for connecting LLMs to tools and data. Since donated to the Linux Foundation (Dec 2025, per Wikipedia) | Ch6: how GGM could be exposed to any model | ★ |

### Reliability, capability and cost

| Source | What it covers | Use in thesis | ★ |
|---|---|---|---|
| He, H. & Thinking Machines Lab (2025, Sep 10). [Defeating nondeterminism in LLM inference](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) | Same prompt, different answers even at temperature 0, mainly because server batch size changes the arithmetic | Ch4/ch7: reproducibility of agent-assisted calibration. A run cannot be reproduced by re-running the prompt; the decisions must be logged | ★★ |
| METR (Kwa, T.) (2026, Jan 22). [Clarifying limitations of time horizon](https://metr.org/notes/2026-01-22-time-horizon-limitations/) | A 50% time horizon is not a safe delegation threshold; error bars are about a factor of 2 | Ch4: use whenever the METR paper is cited | ★★ |
| Stanford HAI (2026). [AI Index Report 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report) | Annual state of AI. Secondary coverage reports large agent-benchmark gains but single-digit business deployment of agents | Ch4: a neutral, citable source for "where things stand". Check figures in the report itself | ★ |
| IEA (2025, Apr). [Energy and AI](https://www.iea.org/reports/energy-and-ai). World Energy Outlook special report | AI's energy demand and AI as a tool in the energy sector | Ch1/ch2: the energy establishment's view of AI. Mostly about data centres, so cite narrowly | ★ |

### Tools close to our setting

| Source | What it covers | Use in thesis | ★ |
|---|---|---|---|
| Open Energy Transition. [pypsa-mcp](https://github.com/open-energy-transition/pypsa-mcp) (GitHub) | MCP server letting an LLM build and run PyPSA energy models | Ch2/ch6: the nearest thing to an agent around an open energy-system model. Practitioner work, not a paper | ★★ |
| Anthropic, Claude for Excel; Microsoft, [Agent Mode in Excel](https://support.microsoft.com/topic/use-claude-with-agent-mode-in-excel-b2c3b3ec-154b-484b-84d0-914a80df395a) | LLMs reading, editing and building workbooks while tracking changes and formula dependencies | Ch5: since a GGM scenario is three workbooks, commercial spreadsheet agents now exist. Dates and model versions differ between sources, so check the official pages before citing | ★ |

---

## What was searched for and not found

Recorded so the gap claim rests on a search, not on an assumption. Searched 2026-10-13 in arXiv,
OpenAlex, Semantic Scholar and with web search. "Not found" means not in the top results of several
phrasings, not proof that nothing exists.

- **LLM agents applied to natural-gas market models, or to any partial-equilibrium or
  complementarity (MCP) energy-market model.** Nothing found on 2026-10-13. *Update 2026-10-15:* Golden et al. (2026, section F) orchestrate existing energy-market models, including partial-equilibrium and LNG models, and list a Global Gas Model in their registry without running it. Nobody has yet calibrated or configured such a model with an agent. The nearest are power-system dispatch
  (section F) and building energy simulation (section D).
- **LLM agents applied to large energy-system models** (TIMES, MESSAGEix, PyPSA-Eur, OSeMOSYS). Only
  the practitioner pypsa-mcp tool and RE-LLM's results-explanation layer. No paper on scenario setup
  or calibration of these models.
- **LLM agents for GAMS or other algebraic modelling languages** used in economics. Nothing found.
- **LLM-driven calibration where the target is not an observation.** The calibration papers in
  section C all have observed targets. The closest discussion of "no correctness signal" is in
  AI-for-economic-theory (pAI-Econ-claude, section G).
- **Earlier NTNU master's theses on LLM agents around energy models.** None found via web search.
  NTNU Open's own search was not tried and is worth a direct look.

---

## Corrections to the earlier list

Found while checking the candidate list in `project-thesis-structure.md` §3 (corrected there too):

- **Chain-of-Experts was linked to the wrong paper.** The link pointed to arXiv 2407.19633, which is
  *OptiMUS-0.3*. Chain-of-Experts is Xiao et al., ICLR 2024 (section E).
- **The EnergyPlus/iScience paper** now has authors and a DOI: Lu et al. (2025),
  [doi:10.1016/j.isci.2025.113867](https://doi.org/10.1016/j.isci.2025.113867).
- All other candidates in §3 were confirmed to exist with the titles given.
