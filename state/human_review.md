# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/5` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_101657`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 1/5 diagnosis prepared from the current best custom run 20260419_101256_bf16_gemm_v1_5ab5302 at 36.517889 ms. Recent history is applied explicitly: broad B-feed rewrites and phased live-set rewrites regressed, while the winning move was peeled hot-kernel specialization plus trimmed export. Ranking therefore builds on the current peeled 64x384 kernel and favors complementary overlap, tail specialization, and only a tightly bounded single-skew B follow-up.`
- dir_01: Deepen single-skew cp.async overlap in the fixed peeled 64x384 hot kernel | bottleneck: Copy-latency exposure and in-loop feed overlap in the peeled 64x384 hot kernel.
- dir_02: Peel and specialize the fixed 64x96 tail kernel to match the hot path | bottleneck: Residual fixed-shape tail overhead from using the generic 64x96 tensor-core kernel on the last 96 columns.
- dir_03: Try a bounded single-skew B-stride retune on the peeled hot kernel | bottleneck: Residual B-side staging pressure inside the current single-skew peeled hot kernel, not a full feed-path redesign.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
