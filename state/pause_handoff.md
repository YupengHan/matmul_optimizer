# Pause Handoff

- paused at: `2026-04-21T12:54:35-07:00`
- pause reason: `explicit_user_redirect`
- paused loop position: `round 11/100`
- completed rounds in this loop: `10`
- remaining rounds preserved: `90`

## Latest measured state

- latest run: `20260421_124420_bf16_gemm_v1_fc400df`
- measured commit: `fc400df814258c9927aa72a78b213b2e9325787f`
- median runtime: `45.920258 ms`
- correctness: `PASS`
- latest barrier-retime delta versus previous run: `-0.136190 ms`

## Latest rich NCU read

- current kernel is now worse on the local occupancy/barrier seam than the prior correct anchor
- headline regressions after the barrier retime:
  - `Registers Per Thread = 208`
  - `sm__warps_active.avg.pct_of_peak_sustained_active = 16.58`
  - `smsp__warp_issue_stalled_barrier_per_warp_active.pct = 8.09`
  - `smsp__warp_issue_stalled_mio_throttle_per_warp_active.pct = 5.00`
- primary interpretation:
  - the round-10 barrier family should not remain the default top direction
  - the current 128x128 PTX anchor is still far from the accepted fast surface

## Most useful search information to preserve

- accepted fast current-workload base still lives at:
  - run `20260421_105134_bf16_gemm_v1_8dcab81`
  - runtime `24.186960 ms`
- historical best correct custom run remains:
  - run `20260420_235922_bf16_gemm_v1_489574e`
  - runtime `24.164272 ms`
- frontier head at pause:
  - `diagnosis_20260421_013125:dir_02`
  - family `legacy::restore_the_best_measured_ptx_grouping_window_on_the_accepted_surface`
  - meaning: exact `489574e` PTX surface restore / re-anchor

## High-value family not to lose

- keep the low-register PTX writer/export family alive even though the current round is paused
- why:
  - round 7 (`20260421_122942_bf16_gemm_v1_3eed315`) hit `43.250160 ms`
  - that run failed correctness, but it also showed:
    - `Registers Per Thread = 104`
    - `sm__warps_active.avg.pct_of_peak_sustained_active = 33.2`
    - `launch__occupancy_limit_registers = 4`
- interpretation:
  - a correctness-safe recovery of that low-register surface is still one of the few signals with genuine jump potential

## Workflow invariants to preserve on resume

- keep using the latest workflow code on HEAD
- implementation restores must not rewind workflow/workload support files
- rich NCU handoff remains required for node_b / node_c
- loop selection cadence remains:
  - rounds `1, 6, 11, ...` => `frontier`
  - other rounds => `recommended`

## Resume recommendation

1. Start from `node_b`, not `node_c`.
2. Re-read `state/latest_ncu_summary.md`, `state/node_b_context.md`, and this handoff.
3. For the first resumed selection, prefer re-anchoring on the fast restore family unless newer evidence clearly dominates it.
4. Keep the low-register writer family in the live queue as a high-upside correctness-repair branch.
