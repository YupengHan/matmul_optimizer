# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f6d1219a34005d5ad19676734d636b07fa356b87`
- plateau counter: `12`
- round loop: `round 25/100`
- rounds remaining: `76`
- notes: `Node C is ready to implement diagnosis_20260421_010737:dir_01 via recommended selection for round 25/100.`

## Latest measured custom run

- run id: `20260421_010424_bf16_gemm_v1_f6d1219`
- run dir: `runs/20260421_010424_bf16_gemm_v1_f6d1219`
- correctness: `PASS`
- median runtime: `24.176016 ms`
- TFLOP/s: `30.071929 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_010737`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 25 intentionally overrides the frontier's current micro-family ordering. The plateaued PTX families are now treated as low-value noise-chasing, while the auxiliary 256x128 family is promoted as the best remaining structural probe after the half-panel closeout.`
- dir_01: Reopen The Auxiliary 256x128 Hot-Band Schedule As The Next Structural Probe | bottleneck: Hot-band CTA geometry, control amortization, and latency hiding on the wide 256x128 schedule family, not another PTX-local barrier or scoreboard seam on the already plateaued 128x128 winner surface.
- dir_02: Restore The Grouped-Row Non-PTX 128x128 Sibling Surface | bottleneck: PTX-microkernel-specific control and export coupling on the current winner surface, while preserving the same broad 128x128 footprint and grouped-row locality.
- dir_03: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: No new bottleneck is being attacked here; this is the exact baseline recovery path back to the best measured correct surface.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
