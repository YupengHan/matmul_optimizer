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
- evaluation harness scaffold: READY
- CUTLASS baseline: TODO
- current best custom kernel: TODO
- gap to CUTLASS: TODO

## Iteration log

### Iteration 0 - repository scaffold

- established one fixed benchmark shape
- decided to keep the execution path script-first
- split the former `agent_b` into:
  - diagnosis node
  - implementation loop node
- reserved branch-heavy exploration for `agent_d`

## Near-term next actions

1. generate the dataset locally
2. connect `eval_kernel.py` to the first real CUDA runner
3. record the first CUTLASS baseline
4. start the first custom-kernel measurement
