# GGM Agent System

## What this is

Master's thesis project (NTNU, Industrial Economics) by Jørgen Holt and Save.
Supervised by Franziska Holz.

We are building LLM-based agents (Python, Claude API) that wrap around the
Global Gas Model (GGM) — a Julia partial equilibrium model for global natural
gas markets. The agents automate scenario generation, parameter curation,
result interpretation, and validation. GGM itself stays untouched.

## GGM

- Source: https://github.com/Franziska-Holz/GGM_public (MIT, Julia/JuMP)
- Included here as a git submodule in `ggm/`
- Do not modify GGM source — our work is the agent layer around it
- Julia↔Python bridge: subprocess calls with JSON files, keep it thin

## Stack

- Python for agents (Anthropic SDK)
- Julia for GGM (JuMP, called via subprocess)
- Git for collaboration (feature branches, PRs)

## Conventions

- Code and comments in English
- Feature branches off `main`, merge via PR
- API keys in `.env`, never committed
- Large data files go in `data/` (gitignored)
