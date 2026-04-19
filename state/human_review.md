# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/5` with `3` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_103511`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosed run 20260419_103438_bf16_gemm_v1_3eeb098 against the restored accepted base 2872f92. The named-barrier/subgroup stage-handoff retune is strong negative evidence: it cut barrier and mio stalls but ballooned the hot kernel to 167 registers/thread, dropped register-limited occupancy to one block per SM, and regressed to 41.745407 ms. The ranking therefore stays on bounded changes around the winning peeled 64x384 plus 64x96 split and does not continue the named-barrier path.`
- dir_01: Pairwise unroll the peeled 64x384 hot loop without changing the handoff model | bottleneck: Tensor issue underfill and loop/control overhead inside the fixed 64x384 hot kernel, with register growth as the main guardrail.
- dir_02: Add a fixed-K peeled 64x96 tail kernel | bottleneck: Residual barrier and scoreboard overhead in the generic 64x96 tail kernel; total upside is capped because the tail is only about 0.9 ms of GPU time today.
- dir_03: Micro-retune the single-level B skew inside the existing 64x384 pipeline | bottleneck: Shared-memory bank behavior and LSU pressure on B-fragment loads, with limited headroom before a mapping tweak starts hurting cp.async coalescing or reopens earlier feed-path regressions.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
