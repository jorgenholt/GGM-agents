# Sources: GDPval presentation

All sources used for the deck so far, with what each one is used for.
"Slide" numbers refer to the current 17-slide version (live test moved to slides 13–14). Accessed October 2026.

## The paper

| Source | Used for |
|---|---|
| Patwardhan et al. (2026), *GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks*, ICLR 2026. [arXiv:2510.04374](https://arxiv.org/abs/2510.04374) · [ICLR proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/290c2430f91912204f30bbcc990fff1d-Paper-Conference.pdf) | The core of slides 1–7: literature context, dataset (1,320 tasks, 44 occupations, 9 sectors), method (blind pairwise expert grading), headline results (Fig. 5), speed/cost (Table 2), failure modes (Fig. 8, 14), task length (Fig. 13), prompt tuning (Fig. 9), grader agreement (66% vs. 71%), limitations. 2025 per-occupation baseline (Fig. 11). |
| OpenAI, [GDPval blog post](https://openai.com/index/gdpval/) (Sep 2025) | Confirms how grading works (blind expert comparison, "better / as good as / worse") and that the 220-task gold set is public. |
| OpenAI, [GDPval dataset on Hugging Face](https://huggingface.co/datasets/openai/gdpval) | Confirms the 220 public tasks include prompts, reference files, the experts' own deliverables and rubrics (contamination point, slide 9). No license is stated, so no expert deliverable is quoted. |

## Newer expert-graded results (same test as the paper)

| Source | Used for |
|---|---|
| OpenAI, [Introducing GPT-5.2](https://openai.com/index/introducing-gpt-5-2/) (Dec 2025) | GPT-5.2 at 70.9% wins or ties "according to expert human judges"; GPT-5 baseline 38.8% matches the paper (slides 8–9). Internal investment-banking spreadsheet test 59.1% → 68.4%. |
| OpenAI, [Introducing GPT-5.4](https://openai.com/index/introducing-gpt-5-4/) (Mar 2026) | GPT-5.4 at 83.0%; wins-only split (GPT-5.4 70.8% vs. GPT-5.2 49.8%); reasoning-effort footnote (slides 8, 11). |
| OpenAI, [Introducing GPT-5.5](https://openai.com/index/introducing-gpt-5-5/) (Apr 2026) | GPT-5.5 at 84.9%; OpenAI's grading of Claude Opus 4.7 (80.3%) and Gemini 3.1 Pro (67.3%); investment-banking test 88.5%; FrontierMath tier 1–3 at 51.7% (slides 8, 11). |
| OpenAI, [GPT-5.6](https://openai.com/index/gpt-5-6/) | Shows OpenAI switched to reporting GDPval-AA (AI-graded, Elo) instead of the expert-graded score (slides 8–9). |
| OpenAI, [GPT-6 Astra](https://openai.com/index/gpt-6-astra/) | Launch page has no GDPval result at all (slide 8). |
| OpenAI GDPval leaderboard, `evals.openai.com/gdpval/leaderboard`, now [offline](https://evals.openai.com/gdpval/leaderboard). Data recovered from the [Internet Archive copy of the site code (May 2026)](https://web.archive.org/web/20260515070620/https://evals.openai.com/assets/index-DG7KYAk4.js); search for "Accountants and Auditors" | Expert-graded results per sector and occupation for the paper's models plus GPT-5.2, Claude Opus 4.5 (59.6%), Claude Sonnet 4.5 (50.3%) and Gemini 3 Pro (53.5%), last updated Dec 2025. Basis for slide 10 (accountants 24% → 56%) and the takedown point (slide 12). Extracted data: [`../leaderboard-data/gdpval_leaderboard_archive.csv`](../leaderboard-data/gdpval_leaderboard_archive.csv). Model names are inferred from internal IDs (e.g. "claude-45"). |
| Actrix Financial Technology, [Are LLMs Now at Par with Industry Experts?](https://actrixft.com/are-llms-now-at-par-with-industry-experts-what-the-latest-gdpval-results-show/) (Dec 2025) | Independent confirmation that the leaderboard existed, with screenshots of the sector and occupation charts. |
| Ethan Mollick, [GPT-5.4 chart](https://x.com/alexolegimas/status/2029643085752275090) (retweeted by Alex Imas) | Secondary confirmation that GPT-5.4's score is "as judged by other experts". |
| Vellum, [Everything you need to know about GPT-5.5](https://www.vellum.ai/blog/everything-you-need-to-know-about-gpt-5-5) | Secondary source for the GPT-5.5 table before it was checked on OpenAI's page. |
| The Next Web, [GPT-5.4 sets new records](https://thenextweb.com/news/openai-gpt-54-launch-computer-use-benchmarks) | Secondary source for GPT-5.4's 83%. |

## Not comparable: GDPval-AA and look-alikes

| Source | Used for |
|---|---|
| Artificial Analysis, [GDPval-AA methodology](https://artificialanalysis.ai/evaluations/gdpval-aa) | Same 220 tasks, but an LLM judge compares models with each other and gives Elo scores; no human baseline and no occupation breakdown (slide 9). |
| Artificial Analysis, [Benchmarking GPT-6 Astra](https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra) | Astra drops about 45 Elo on GDPval-AA vs. GPT-5.6 Sol (context for OpenAI not reporting GDPval). |
| Artificial Analysis, [DeepSeek V4](https://artificialanalysis.ai/articles/deepseek-is-back-among-the-leading-open-weights-models-with-v4-pro-and-v4-flash) and [Grok 4.5](https://artificialanalysis.ai/articles/grok-4-5-brings-spacexai-to-the-the-intelligence-frontier) | Shows open-weights and xAI models only report GDPval-AA (slides 8–9). |
| Anthropic, [Claude Opus 4.7](https://www.anthropic.com/news/claude-opus-4-7) | Anthropic reports GDPval-AA only, not the expert-graded test (slide 9). |
| Enterprise DNA, [xAI's GDPval+ claim](https://enterprisedna.co/resources/ai-pulse/ai-pulse-2026-07-22-xai-claims-grok-4-5-plus-its-grok-build-agent-beat-gpt-5-5-a/) | Example of a "look-alike" benchmark (Snorkel's GDPval+) used in marketing (slide 9). |
| Forbes, [OpenAI launches GPT-6 Astra](https://www.forbes.com/sites/ronschmelzer/2026/09/03/openai-announces-gpt-6-astra-or-does-it/) · VentureBeat, [GPT-6 Astra launch](https://venturebeat.com/technology/welcome-to-the-agi-era-openai-launches-gpt-6-astra) | Press noting the missing GDPval score at the Astra launch. |

## The "Be the grader" comparison (slides 13–14)

| Source | Used for |
|---|---|
| Huppmann & Holz (2015), *What about the OPEC Cartel?*, DIW Roundup: Politik im Fokus No. 58, March 11, 2015. [English PDF (EconStor)](https://www.econstor.eu/bitstream/10419/111843/1/DIW_Roundup_58_en.pdf) · [German version (DIW)](https://www.diw.de/de/diw_01.c.501073.de/publikationen/roundup/2015_0058/ist_die_opec_ein_effektives_kartell.html) | Deliverable B: the paragraph starting "Even though OPEC is sometimes used as a textbook example of a cartel" (p. 2, section "The cartel that isn't"), with only the web address removed. Chosen before Claude was run, because it answers the task's question directly. No open license (EconStor terms: scholarly use only), so it is quoted for teaching with attribution and should not be published online. |
| Deliverable A | Claude Opus 5.5 with high reasoning, fresh chat (October 2026), first answer to the exact prompt shown on slide 14 (summarised on slide 13) (same date, role, length and question as the authors; no hints about their answer). Not a published source. A/B order decided at random. |
| Holz, Barner, Kemfert & von Hirschhausen (2024), DIW Weekly Report 21/2024, [doi:10.18723/diw_dwr:2024-21-1](https://doi.org/10.18723/diw_dwr:2024-21-1) (CC BY 4.0) | Earlier version of the comparison, dropped because it reported their own Global Gas Model results, which Claude could not have. Still useful background on what the GGM is used for. |
| Bernanke (2006), [Energy and the Economy](https://www.federalreserve.gov/newsevents/speech/bernanke20060615a.htm), Federal Reserve | First version of the comparison (dropped). Public domain. |
| Holz's CV, [DIW](https://www.diw.de/documents/dokumentenarchiv/17/diw_01.c.85299.de/diwcvlong_de_fholz.pdf) | Used to find her shorter, blog-style publications (DIW Roundup, DIW aktuell). |

## Thesis (slides 15–16)

| Source | Used for |
|---|---|
| Our repo `ggm-agents` (`CLAUDE.md`, `docs/thesis-scope.md`, `docs/how-it-would-work.md`, `docs/project-thesis-structure.md`) | Thesis title, supervisor, GGM description (Julia/JuMP + Gurobi, three Excel workbooks, calibration takes days to weeks), the "prepare, check, explain" design. |
| Egging & Holz, *Global Gas Model: Model and Data Documentation* (DIW), cited via `docs/ggm-documentation-v3.0.pdf` | GGM background and the calibration burden. |

## Literature mentioned on slide 3

| Source | Used for |
|---|---|
| Brynjolfsson et al. (2017, 2025), Acemoglu (2025), David (1990) | "Economic statistics lag" (as cited in the paper). |
| Hendrycks et al. (2020) MMLU; Rein et al. (2023) GPQA; Phan et al. (2025) Humanity's Last Exam | "Exam-style benchmarks" (as cited in the paper). |
| Miserendino et al. (2025), SWE-Lancer | "Single-domain work tests" (as cited in the paper). |

## Other background consulted

| Source | Used for |
|---|---|
| [Justified Posteriors podcast on GDPval](https://empiricrafting.substack.com/p/evaluating-gdpval-openais-eval-for) (Nov 2025) | Cross-check of the paper's figures; general critique. |
| [Faster AI, Uneven Frontier (arXiv 2607.12125)](https://arxiv.org/abs/2607.12125) | Checked for newer GDPval numbers; none found. Not used on slides. |
| guizang-ppt-skill ([op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill), AGPL-3.0) | Slide template and design system. |
