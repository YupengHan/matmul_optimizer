# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `5ab5302bd23e8cd1ff2fcd97dbfd5a35b1701ca9`
- plateau counter: `0`
- round loop: `round 1/5`
- rounds remaining: `5`
- notes: `Node C build succeeded for round 1/5. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260419_101256_bf16_gemm_v1_5ab5302`
- run dir: `runs/20260419_101256_bf16_gemm_v1_5ab5302`
- correctness: `PASS`
- median runtime: `36.517889 ms`
- TFLOP/s: `19.908583 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`
- result: `NEW BEST CUSTOM RUN`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_101657`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/5 diagnosis prepared from the current best custom run 20260419_101256_bf16_gemm_v1_5ab5302 at 36.517889 ms. Recent history is applied explicitly: broad B-feed rewrites and phased live-set rewrites regressed, while the winning move was peeled hot-kernel specialization plus trimmed export. Ranking therefore builds on the current peeled 64x384 kernel and favors complementary overlap, tail specialization, and only a tightly bounded single-skew B follow-up.`
- dir_01: Deepen single-skew cp.async overlap in the fixed peeled 64x384 hot kernel | bottleneck: Copy-latency exposure and in-loop feed overlap in the peeled 64x384 hot kernel.
- dir_02: Peel and specialize the fixed 64x96 tail kernel to match the hot path | bottleneck: Residual fixed-shape tail overhead from using the generic 64x96 tensor-core kernel on the last 96 columns.
- dir_03: Try a bounded single-skew B-stride retune on the peeled hot kernel | bottleneck: Residual B-side staging pressure inside the current single-skew peeled hot kernel, not a full feed-path redesign.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `10.600000 ms`, `1.408984x` slower than CUTLASS
