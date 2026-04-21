# Node C context

Node C is the implementation node. Implement exactly one approved or explicitly selected recommended direction.

## Selected direction

- direction id: `dir_01`
- direction name: `Retune The Active One-K 128x128 Hot-Band Copy Cadence`
- selection mode: `recommended`
- source diagnosis id: `diagnosis_20260420_200135`
- round loop: `round 16/50`
- hypothesis: `Round 16/50 still has no extra user-authored idea family in `state/human_review.md` beyond the approval gate and the exactly-one-direction rule, so the next move should follow the latest measured evidence as narrowly as possible. The current source surface already matches the recorded best-custom kernel source in `src/kernels/bf16_gemm_v1.cu` (no kernel diff between `1181247` and `e6fdb8b`), and the latest NCU capture shows the dominant `128x128` hot-band kernel is the only branch that is even slightly behind that best reference: hot-band time is `32,917,184 ns` now versus `32,868,864 ns` on `1181247`, while the peeled and tail kernels are not slower in the current capture. The remaining gap is narrow and still looks like feed/shared-stage friction inside the active one-K loop (`7.73%` long-scoreboard now versus `7.49%` on `1181247`, `13.02%` DRAM versus `12.84%`, with `196` regs/thread and only `16.64%` active warps), so the best next move is a bounded retune of the current K16 copy/wait cadence and B-stage handoff instead of another family pivot.`
- expected bottleneck: `A narrow hot-band feed-latency and shared-stage handoff gap inside the active one-K `128x128` kernel, not the peeled `64x384` residual rows or the `64x96` tail.`
- code locations: `src/kernels/bf16_gemm_v1.cu:1071-1102, src/kernels/bf16_gemm_v1.cu:1844-1947, src/kernels/bf16_gemm_v1.cu:2090-2138`
- risk: `Low to moderate. This stays on the current best-known source family and only retunes the active hot-band loop, but the measured gap versus `1181247` is already small, so the upside is bounded and an over-aggressive wait/order change can easily erase the recovered win.`
- metrics to re-check: `end-to-end median runtime versus the current `25.325055 ms` run and the recorded best `24.422464 ms`, hot-band `gpu__time_duration.sum` versus the current `32,917,184 ns` and the `1181247` reference `32,868,864 ns`, hot-band `smsp__warp_issue_stalled_long_scoreboard_per_warp_active.pct`, hot-band `sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active`, hot-band `dram__throughput.avg.pct_of_peak_sustained_elapsed`, hot-band `l1tex__data_bank_reads.avg.pct_of_peak_sustained_elapsed` and `l1tex__data_bank_writes.avg.pct_of_peak_sustained_elapsed``

## Allowed edit surface

- `src/kernels/*`
- `src/runner/main.cpp` when the direction requires runner glue
- `include/*` when a stable interface change is required
- `CMakeLists.txt` only if the build path genuinely needs it
- `scripts/graph.py` or `scripts/sweep_fixed_main_tiles.py` only when the direction requires minimal workflow glue

## Required commands

- edit code for one direction only
- then run `python scripts/graph.py node_c --finalize`
- default behavior after a successful node_c finalize is to auto-run node_a

## Dirty working tree snapshot before node_c finalize

- no tracked dirty paths at prepare time
