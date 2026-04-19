# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `f237679f9fc0bed9c49d1043495794c187d0aea4`
- plateau counter: `3`
- round loop: `round 4/5`
- rounds remaining: `2`
- notes: `Node C build succeeded for round 4/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_095653_bf16_gemm_v1_f237679`
- run dir: `runs/20260419_095653_bf16_gemm_v1_f237679`
- correctness: `PASS`
- median runtime: `40.935423 ms`
- TFLOP/s: `17.760154 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_095729`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 4/5 diagnosis prepared from run 20260419_095653_bf16_gemm_v1_f237679. Evidence hierarchy: accepted base 16a98f7 at 37.285807 ms remains the reference; round-1 two-level B staging and round-2 phased 64x384 micro-panels both regressed badly; round-3 warp-specialized staging improved over those failed branches and cut mio_throttle sharply, but it still remained meaningfully slower than the accepted base, so it is treated as negative evidence for stacking forward. Ranking therefore pivots to base-oriented steady-state specialization, epilogue trimming, and only a bounded wait/barrier retune.`
- dir_01: Peel a fixed-shape steady-state hot kernel for 6464x7776x7232 | bottleneck: Generic steady-state loop/control overhead diluting tensor issue on the fixed-shape hot path.
- dir_02: Trim the c_shared epilogue/export path on the restored base | bottleneck: LSU/shared writeback pressure in the hot epilogue rather than feed-path or live-set shape.
- dir_03: Apply a bounded cp.async wait/barrier retune to the restored single-skew base | bottleneck: Copy-pipeline wait/barrier scheduling in the accepted base rather than B layout or live-set shape.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
