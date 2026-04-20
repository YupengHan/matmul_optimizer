# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_b`
- previous node: `node_a`
- status: `ready_for_node_b`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `84de30b73776656fed997f60535082ce957bc002`
- plateau counter: `25`
- round loop: `round 84/100`
- rounds remaining: `17`
- notes: `Node A completed round 83/100. Run node_b to continue round 84/100.`

## Latest measured custom run

- run id: `20260420_120552_bf16_gemm_v1_84de30b`
- run dir: `runs/20260420_120552_bf16_gemm_v1_84de30b`
- correctness: `PASS`
- median runtime: `25.944464 ms`
- TFLOP/s: `28.022141 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `pending_generation`
- diagnosis id: `None`
- recommended direction: `None`
- approved direction: `None`
- diagnosis notes: `Run node_b to produce exactly three directions from the latest measured run.`
- no directions recorded yet

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS

## Persisted handoff for the next terminal

- treat `20260420_115626_bf16_gemm_v1_469a12b` at `25.643007 ms` as the best active baseline in the current environment
- that baseline corresponds to the PTX microkernel default hot-band with `FixedHotBandTile128x128PtxExportScratch::kPadFloatsPerRow = 0`
- do not re-open pure baseline-restore work as a primary direction; the same source surface has already measured differently across sessions, so future rounds should target new bottlenecks rather than spend budget proving that again
- the current residual bottleneck shape after the export-padding win is:
- tensor active near `48%`
- barrier near `5.5%`
- DRAM near `10%`
- long scoreboard still elevated
- broad default hot-band promotions are closed-negative for now
- evidence: `64x384` default promotion -> `33.594879 ms`
- evidence: `256x128` default promotion -> `31.867904 ms`
- staged `128x128x32` K32 family is closed-negative for now
- evidence: `31.552928 ms`
- paired PTX export-lifetime helper is closed-negative for now
- evidence: `25.837568 ms` vs the `25.643007 ms` active baseline
- PTX grouped-row narrowing from `8` to `4` is closed or near-closed
- evidence: `25.944464 ms`
- bounded `128x128` two-stage feed-cadence retime is weak / flat, not a primary continuation line
- evidence: `25.904127 ms`
- the next useful diagnosis should prioritize narrow PTX-adjacent ideas that target `long_scoreboard` without reintroducing DRAM / barrier inflation
