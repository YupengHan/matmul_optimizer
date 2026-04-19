# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 2/20` with `19` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_222017`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Retune the tensor tile so each warp does more MMA work per shared-memory feed | bottleneck: Shared-memory / fragment-load issue pressure with too little MMA work per warp and too few ready warps to hide it.
- dir_02: Rewrite the A/B shared-memory layout for lower-friction WMMA fragment loads | bottleneck: Shared-memory layout inefficiency on the WMMA load path, especially the B-fragment feed, causing excessive MIO throttling before Tensor Cores can be kept busy.
- dir_03: Retune the async pipeline handoff to reduce per-K synchronization bubbles | bottleneck: Stage-transition overhead from the double-buffered `cp.async` pipeline, where full-CTA waits and barriers are now a secondary limiter after global-load widening.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
