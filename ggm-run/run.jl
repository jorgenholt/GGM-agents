# Runs GGM on the 2023 data without touching ggm/.
# Usage, from the repo root: julia --project=ggm-run ggm-run/run.jl NCA_NENO
# The argument is <demand scenario>_<network variant>: NCA/MCA/FFF/TZE and NENO/SQAB/EUSD.
using GlobalGasModel, Dates, Gurobi

scen = ARGS[1]
root = normpath(joinpath(@__DIR__, ".."))
out  = joinpath(root, "data", "ggm-runs", scen * "_" * Dates.format(now(), "yyyy-mm-dd_HH-MM"))
mkpath(out)
log  = joinpath(out, "run.log")

sets, params = get_GGM_inputs(scen, 2020:5:2060;
    data_file_path   = joinpath(root, "data_2023"),
    store_parameters = joinpath(out, "parameters"),
    store_log        = log)

model = build_GGM(sets, params, Gurobi.Optimizer;
    store_log = log, solver_options = Dict("NumericFocus" => 1))

model, results = solve_GGM(model; store_result = joinpath(out, "results"), store_log = log)
