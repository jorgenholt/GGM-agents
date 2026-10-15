# Running GGM on the 2023 data

How to run the model on your own machine. This folder exists so that nothing inside `ggm/` is
changed. The model's own script, `ggm/ggm_2023.jl`, reads the data from `ggm/data_2023/`, and the
licensed 2023 data must not be copied there. `run.jl` here does the same run, but reads from
`data_2023/` and writes to `data/ggm-runs/`, which is gitignored.

## Once per computer

1. **Install Julia.** Either from julialang.org or with `brew install julia`.
2. **Install Gurobi and get a free academic licence.**
   1. Install Gurobi from gurobi.com.
   2. On the NTNU network (eduroam or the NTNU VPN), request a *Named-User Academic* licence on
      gurobi.com.
   3. Run the `grbgetkey` command it gives you, and save the licence to your home folder.
   4. The licence is tied to one machine, so each of us needs our own.
3. **Fetch the model**, which is stored as a git submodule. From the repo root:
   ```bash
   git submodule update --init
   ```
4. **Install the Julia packages.** From the repo root (takes a few minutes):
   ```bash
   julia --project=ggm-run -e 'using Pkg; Pkg.develop(path="ggm/GlobalGasModel"); Pkg.add(["Gurobi", "Dates"]); Pkg.precompile()'
   ```
   This writes a `Manifest.toml` here, which is gitignored.

## Each run

From the repo root:

```bash
julia --project=ggm-run ggm-run/run.jl NCA_NENO
```

The argument is `<demand scenario>_<network variant>`:

| Part | Options | Workbooks it picks |
|---|---|---|
| Demand scenario | `NCA`, `MCA`, `FFF`, `TZE` | `projected_data_*` and `calibrated_data_*` |
| Network variant | `NENO`, `SQAB`, `EUSD` | `general_data_*` |

**Expect a run to take about 25 minutes.** The first test, `NCA_NENO` on 15 October 2026 on an
M1 MacBook with 8 GB of RAM, took 24 minutes:

| Stage | Time |
|---|---|
| Load the data | 1 s |
| Build the model (1.9 million constraints, 5.5 million variables) | 2.5 min |
| Gurobi solve (131 barrier iterations) | 18 min |
| Write the results | 2 min |

It needed more memory than the machine has, so macOS compressed memory. It still worked, but
close other heavy apps while it runs.

What the codes mean is described in [`docs/ggm-data-2023.md`](../docs/ggm-data-2023.md).

Each run writes a new folder, `data/ggm-runs/<scenario>_<date-time>/`, containing:

| File or folder | What it holds |
|---|---|
| `run.log` | Progress messages and warnings. Read this first. Expect about a thousand warnings saying "Inf … set to 10000.0", mostly for production cost (`cost_pq`) at nodes with no capacity. These come from the loader's built-in fallback for division by zero; see [`docs/ggm-data-2023.md`](../docs/ggm-data-2023.md) §4 |
| `parameters/` | The inputs exactly as the model read them, as CSV |
| `results/` | The model's results, as CSV |

## If something goes wrong

**Julia can't find Gurobi.** Point it at the Gurobi installation and rebuild the Gurobi package.
Adjust the path to your Gurobi version.

```bash
export GUROBI_HOME=/Library/gurobi1201/macos_universal2
```

```bash
julia --project=ggm-run -e 'using Pkg; Pkg.build("Gurobi")'
```
