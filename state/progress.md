# Progress

## Objective

Beat the local CUTLASS baseline on a **single fixed BF16 GEMM shape** on an RTX 3070 Laptop GPU.

## Fixed workload

- dataset: `fixed_bf16_gemm_v1`
- shape: `m=6464, n=7776, k=7232`
- benchmark case: `case_00_seed_3407`
- correctness cases:
  - `case_00_seed_3407`
  - `case_01_seed_9713`
  - `case_02_seed_1729`

## Current status

- dataset generation scaffold: READY
- local dataset generation: READY
- evaluation harness scaffold: READY
- custom CUDA runner: READY
- placeholder custom kernel: READY
- first end-to-end evaluation attempt: COMPLETE
- first host-side GPU run: COMPLETE
- CUTLASS baseline: TODO
- current best custom kernel: HOST BASELINE RECORDED
- gap to CUTLASS: UNKNOWN

## Verified snapshot

- configured and built successfully with `cmake -S . -B build` and `cmake --build build -j 4`
- local dataset summary exists under `artifacts/datasets/fixed_bf16_gemm_v1/generation_summary.json`
- total generated dataset size is `1452.1171875 MiB` across 3 cases
- latest accepted host-side evaluation is `runs/20260418_111959_bf16_gemm_v1_host_v0`
- correctness passed on all 3 configured cases under the current tolerance policy
- the recorded performance result for `case_00_seed_3407` is `802.8425598 ms` median runtime, `796.2209229 ms` p10, `807.9350769 ms` p90, and `0.9055566534 TFLOP/s`
- Nsight Compute completed successfully for the host-side run and wrote `ncu_profile.ncu-rep` plus `ncu_metrics.csv`
- the earlier sandbox-only run at `runs/20260418_021152_bf16_gemm_v1` still serves as a historical note about environment visibility, not a project-level CUDA failure

## Iteration log

### Iteration 0 - repository scaffold

- established one fixed benchmark shape
- decided to keep the execution path script-first
- split the former `agent_b` into:
  - diagnosis node
  - implementation loop node
- reserved branch-heavy exploration for `agent_d`

### Iteration 1 - dataset + runner bring-up

- implemented deterministic dataset generation and wrote local manifests/checksums
- implemented `custom_runner` with:
  - dataset loading
  - correctness checking against `C_ref_fp32` and `C_ref_bf16`
  - timed perf loop with cache flush and percentile summary
- wired `scripts/eval_kernel.py` to the runner contract and run artifact layout
- compiled the CUDA target successfully
- executed the first end-to-end run from the Codex sandbox
- observed a tooling-environment blocker instead of a kernel-level result:
  - `cudaMalloc: no CUDA-capable device is detected`
  - the failure came from sandbox GPU visibility, not from a confirmed host-side CUDA failure

### Iteration 2 - first host GPU run

- reran the existing `custom_runner` + `eval_kernel.py` pipeline on the host-visible RTX 3070 Laptop GPU
- recorded the first accepted custom-kernel artifacts under `runs/20260418_111959_bf16_gemm_v1_host_v0`
- correctness passed for:
  - `case_00_seed_3407`
  - `case_01_seed_9713`
  - `case_02_seed_1729`
- performance for `case_00_seed_3407` was recorded at `802.8425598 ms` median runtime and `0.9055566534 TFLOP/s`
- Nsight Compute completed and wrote both `ncu_profile.ncu-rep` and `ncu_metrics.csv`
- quick NCU read for the placeholder kernel:
  - `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active = 0`
  - `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 57.07`
  - `launch__occupancy_limit_registers = 6`
  - this is consistent with a stable but very slow placeholder implementation rather than a Tensor Core path

## Near-term next actions

1. add and measure a CUTLASS reference runner on the same host
2. record both baselines in `state/benchmark_baselines.md`
3. use the host-side Nsight Compute result to choose the first optimization direction
4. replace the placeholder GEMM path with a Tensor Core-aware implementation and re-measure
