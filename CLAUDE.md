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
- Julia↔Python bridge: subprocess calls with JSON files, keep it thin
- **Model reference: `docs/ggm-model.md`** — sets, variables, constraints, input
  files, calibration, and parameter defaults, with page pointers into
  `docs/ggm-documentation-v3.0.pdf`. Read it before touching model parameters.
- Input data is NOT in the repo (`ggm/data_2023/` is empty) — must be requested
  from the GGM authors

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

- Findings about how GGM actually works → `docs/ggm-model.md`, in the relevant
  section, with a pointer to the source line or PDF page that proves it
- Questions that need a human → `docs/questions-for-weekly-meeting.md`
- State what was *verified* vs. what is still *assumed* — an unresolved
  discrepancy is worth recording as unresolved, not silently smoothed over
