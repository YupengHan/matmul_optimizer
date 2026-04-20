# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 64/100` with `37` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_091413`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Anchored to run 20260420_091330_bf16_gemm_v1_863f60f at 25.934336 ms. Rejected this round: grouped_rows=16 active path, grouped_rows=4 active path, unroll 1 active path, warmup-order reopen, K32 cadence, extra-live B lookahead, CTA-level B repack, broad shared-memory rewrites, split sweep, and full mirrored sweep.`
- dir_01: Restore accepted grouped_rows=8 base, then test 8->6 hot-band narrowing | bottleneck: Locality loss in the hot-band PTX consumer ordering and row reuse window, not the broader sweep or sync structure.
- dir_02: Restore accepted base, then probe a very narrow overlap-recovery tweak | bottleneck: Residual consumer-to-producer overlap loss at the handoff boundary rather than the main sweep or row-group structure.
- dir_03: Restore accepted base, then revisit a very local consumer-order closure | bottleneck: A small ordering inefficiency in the consumer sequence inside the right-left sweep family.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
