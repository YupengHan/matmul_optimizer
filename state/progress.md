# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `6dd39ad50b8e36dd035ae435800103257053f6a2`
- plateau counter: `4`
- round loop: `round 5/5`
- rounds remaining: `1`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_100457_bf16_gemm_v1_6dd39ad`
- run dir: `runs/20260419_100457_bf16_gemm_v1_6dd39ad`
- correctness: `PASS`
- median runtime: `37.373951 ms`
- TFLOP/s: `19.452571 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_100543`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 5/5 diagnosis prepared from near-hit run 20260419_100457_bf16_gemm_v1_6dd39ad. Evidence hierarchy: accepted base 16a98f7 remains nominally best at 37.285807 ms; round 1 two-level B staging regressed badly; round 2 phased 64x384 micro-panels regressed badly; round 3 warp-specialized staging improved one symptom but stayed much slower; round 4 fixed-shape peeled hot kernel nearly matched the base at 37.373951 ms while raising tensor active and lowering barrier stall. Final-round ranking therefore treats the peeled hot path as the most credible basis and prioritizes complementary one-round changes over reopening the clearly failed rewrite families.`
- dir_01: Re-land the peeled hot kernel and trim the c_shared export path | bottleneck: Epilogue-side shared/export traffic after the peeled steady-state loop improves control overhead.
- dir_02: Re-land the peeled hot kernel and deepen single-skew cp.async overlap | bottleneck: Copy-latency / short-scoreboard exposure in the peeled steady-state loop.
- dir_03: Re-land the peeled hot kernel with a bounded single-skew B stride retune | bottleneck: Residual B-side staging inefficiency in the current single-skew layout, not a full feed-path redesign.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `11.367918 ms`, `1.438613x` slower than CUTLASS
