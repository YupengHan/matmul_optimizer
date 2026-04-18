# TODO Plan

These markdown files are written to be executed one by one by another coding agent in VSCode chat.

Execution order:

1. `01_first_host_gpu_run.md`
2. `02_cutlass_runner.md`
3. `03_cutlass_baseline_and_ncu.md`
4. `04_prepare_agent_inputs.md`

Rules:

- Do not change the fixed benchmark shape.
- Reuse the existing runner contract and artifact layout.
- Prefer small, reviewable commits after each completed step.
- Do not claim performance progress until correctness passes and a real host-side GPU run is recorded under `runs/`.
- Keep all generated run artifacts local under `runs/` and `artifacts/`.

Expected end state:

- one successful host-side custom-kernel run with `summary.json`, `summary.md`, `ncu_profile.ncu-rep`, and `ncu_metrics.csv`
- one working `cutlass_runner`
- one successful CUTLASS baseline run with matching artifact layout
- a compact package of files that can be fed to an agent for diagnosis
