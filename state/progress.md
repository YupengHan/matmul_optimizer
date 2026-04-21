# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f198bbbac12d7c8ca3363403eb929e2abfb04b43`
- plateau counter: `7`
- round loop: `round 20/100`
- rounds remaining: `81`
- notes: `Node C is ready to implement diagnosis_20260421_003535:dir_01 via recommended selection for round 20/100.`

## Latest measured custom run

- run id: `20260421_003431_bf16_gemm_v1_f198bbb`
- run dir: `runs/20260421_003431_bf16_gemm_v1_f198bbb`
- correctness: `PASS`
- median runtime: `24.171520 ms`
- TFLOP/s: `30.077522 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_003535`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 20 applies the user's new strategy directly: treat sub-0.1 ms effects as noise and push the diagnosis toward more aggressive, profile-driven structural moves. The top set therefore drops the current PTX-local micro families and prioritizes 256x128 and sibling-surface branches with larger theoretical upside.`
- dir_01: Promote The Existing 256x128 Pivot Hot-Band Kernel | bottleneck: Structural latency hiding and control amortization on the hot band due to undersized effective work per scheduling decision, not just one more PTX microkernel handoff seam.
- dir_02: Port grouped-row traversal into the non-PTX 128x128 sibling | bottleneck: Surface-level control and locality inefficiency on the current PTX hot-band path rather than one more within-surface handoff detail.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: K-loop scheduling and latency hiding on the broader 256x128 hot-band regime rather than PTX-local handoff or export sequencing.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` slower than CUTLASS
