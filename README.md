# GGM Agent System

LLM agents wrapping the [Global Gas Model](https://github.com/Franziska-Holz/GGM_public) for automated scenario analysis of European gas supply security.

NTNU master's thesis — Jørgen Holt & Save. Supervised by Anne Neumann.

## Setup

```bash
git clone --recursive <repo-url>
cd ggm-agents
python3 -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv
cp .env.example .env  # add your API keys
```
