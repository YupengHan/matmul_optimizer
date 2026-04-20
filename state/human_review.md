# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 13/50` with `38` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_232121`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 13/50 shifts away from the stage family because the 3-stage hot-band branch only moved the dominant kernel from about 41.11 ms to 41.18 ms while breaking correctness and driving barrier stalls much higher. The recommended next family is the user's consumer-side B feed idea under strict constraints: no extra shared footprint, no extra CTA barriers, and no CTA-level repack.`
- dir_01: Restore the accepted-correct hot-band surface and apply a warp-local B XOR/interleaved consumer swizzle with zero extra shared footprint | bottleneck: Shared-memory bank behavior and warp-local B operand delivery in the hot-band PTX consumer path.
- dir_02: Restore the accepted surface and start an explicit ldmatrix/mma.sync hot-band microkernel branch | bottleneck: Tensor Core under-utilization caused by the current WMMA-based fragment load and issue model rather than tile shape alone.
- dir_03: Restore the accepted-correct implementation surface before the next experiment | bottleneck: Not a bottleneck attack; this is the reset path that keeps later rounds interpretable.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
