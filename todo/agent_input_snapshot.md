# Agent Input Snapshot

Prepared on `2026-04-18` for diagnosis of `fixed_bf16_gemm_v1`.

## Selected runs

- custom run dir: `runs/20260418_111959_bf16_gemm_v1_host_v0`
- CUTLASS run dir: `runs/20260418_115324_cutlass_ref_v0`

## Package contents

- machine-readable manifest: `todo/agent_input_manifest.json`
- custom `summary.json`: `runs/20260418_111959_bf16_gemm_v1_host_v0/summary.json`
- custom `summary.md`: `runs/20260418_111959_bf16_gemm_v1_host_v0/summary.md`
- custom perf JSON: `runs/20260418_111959_bf16_gemm_v1_host_v0/perf_case_00_seed_3407.json`
- custom NCU CSV: `runs/20260418_111959_bf16_gemm_v1_host_v0/ncu_metrics.csv`
- CUTLASS `summary.json`: `runs/20260418_115324_cutlass_ref_v0/summary.json`
- CUTLASS `summary.md`: `runs/20260418_115324_cutlass_ref_v0/summary.md`
- CUTLASS perf JSON: `runs/20260418_115324_cutlass_ref_v0/perf_case_00_seed_3407.json`
- CUTLASS NCU CSV: `runs/20260418_115324_cutlass_ref_v0/ncu_metrics.csv`
- optional human-review custom `.ncu-rep`: `runs/20260418_111959_bf16_gemm_v1_host_v0/ncu_profile.ncu-rep`
- optional human-review CUTLASS `.ncu-rep`: `runs/20260418_115324_cutlass_ref_v0/ncu_profile.ncu-rep`

## Benchmark snapshot

- custom median runtime: `802.8425598 ms`
- custom TFLOP/s: `0.9055566534`
- custom correctness: `PASS` on all 3 configured correctness cases
- CUTLASS median runtime: `25.91788864 ms`
- CUTLASS TFLOP/s: `28.05087373`
- CUTLASS correctness: `PASS` on all 3 configured correctness cases
- runtime gap: `776.92467116 ms`
- runtime ratio: custom is `30.97638743x` slower than CUTLASS on `case_00_seed_3407`

## Notable NCU metric differences

1. `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`: custom `0%`, CUTLASS `49.25%`. The custom kernel is not exercising Tensor Cores at all.
2. `dram__throughput.avg.pct_of_peak_sustained_elapsed` and `lts__throughput.avg.pct_of_peak_sustained_elapsed`: custom `9.29%` / `7.47%`, CUTLASS `42.76%` / `32.41%`. CUTLASS sustains a real data pipeline while the custom placeholder path does not.
3. `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct`: custom `57.07%`, CUTLASS `0.07%`. The custom kernel is spending a large share of warp issue slots blocked on MIO pressure.
4. `smsp__warp_issue_stalled_barrier_per_warp_active.pct` and `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`: custom `13.73%` / `12.70%`, CUTLASS `0.39%` / `0.17%`. The placeholder path pays much more synchronization and wait overhead.
5. `sm__warps_active.avg.pct_of_peak_sustained_active` and `launch__occupancy_limit_registers`: custom `99.94%` active warps with register limit `6`, CUTLASS `16.75%` active warps with register limit `2`. Occupancy is not the first problem to solve; CUTLASS wins with fewer resident warps because those warps are doing useful Tensor Core work.
6. `launch__registers_per_thread` and `launch__shared_mem_per_block_allocated`: custom `36` regs/thread and `3072` bytes/block, CUTLASS `228` regs/thread and `50176` bytes/block. The CUTLASS kernel spends far more resources on fragments and multistage staging, which is consistent with a real Tensor Core pipeline.

## Read order

- `docs/heuristics.md`
- `state/progress.md`
- `state/benchmark_baselines.md`
- custom `summary.json`, perf JSON, then `ncu_metrics.csv`
- CUTLASS `summary.json`, perf JSON, then `ncu_metrics.csv`
- open the `.ncu-rep` files only if a human wants to inspect details in `ncu-ui`

## Concrete question for the next agent

```text
Compare the latest custom kernel run against the latest CUTLASS baseline for fixed_bf16_gemm_v1. Based on summary.json, perf JSON, ncu_metrics.csv, docs/heuristics.md, and the current state files, propose exactly three optimization directions. For each direction, state the hypothesis, the bottleneck it targets, the code areas to change, the main risk, and the metrics to re-check after implementation.
```
