# GGM Agent System

## What this is

NTNU Industrial Economics, by Jørgen Holt and Save Brautaset.
Supervised by Franziska Holz; Lukas Barner (TU Berlin, wrote the Julia port of
GGM) advises and meets weekly.

The end goal is LLM-based agents (Python, Claude API) wrapping the Global Gas
Model (GGM) — a Julia partial equilibrium model for global natural gas markets —
automating scenario generation, parameter curation, result interpretation, and
validation. GGM itself stays untouched.

**Current phase: project thesis (autumn 2026) — exploration and writing, not
building.** The implementation is the master's thesis, spring 2027. See
`docs/thesis-scope.md` before proposing work: code written this semester should
be illustrative and disposable, and the deliverable is a written argument.

## GGM

- Source: https://github.com/Franziska-Holz/GGM_public (MIT, Julia/JuMP)
- Included here as a git submodule in `ggm/`
- Do not modify GGM source — our work is the agent layer around it
- **A scenario *is* three Excel workbooks.** There is no config layer, so a
  bridge must read and write `.xlsx` — not JSON
- Solving requires **Gurobi** (free academic licence)
- Input data is NOT in the repo (`ggm/data_2023/` is empty) — must be requested
  from the GGM authors
- **Model reference: `docs/ggm-model.md`** — read before touching model
  parameters. `docs/README.md` indexes the rest

## Stack

- Python for agents (Anthropic SDK)
- Julia for GGM (JuMP, called via subprocess)
- Git for collaboration (feature branches, PRs)

## Conventions

- Code and comments in English
- Feature branches off `main`, merge via PR
- API keys in `.env`, never committed
- Large data files go in `data/` (gitignored)

## Documenting findings

When something non-obvious about GGM is worked out — a unit convention, a
discrepancy between the docs and the code, why a parameter behaves unexpectedly
— **write it down, don't just say it in chat.** Chat is lost next session.

- `docs/README.md` says which file it belongs in
- Always cite the source line or PDF page that proves it
- State what was *verified* vs. what is still *assumed* — record an unresolved
  discrepancy as unresolved rather than smoothing it over
- Keep the analysis in one place and link to it; don't restate it across files
