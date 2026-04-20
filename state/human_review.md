# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 9/30` with `22` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_222312`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 9/30 starts from the restored pre-sweep surface. The hot-band kernel still dominates, the warp-local consumer variants and CTA-order clue are both negative, and the previous stage-peeling attempt failed correctness. That leaves the copy pipeline as the clearest remaining human-idea family to test. Recommended direction dir_01 therefore tries a bounded ownership split inside the existing two-stage hot-band copy path: lower warps stage A, upper warps stage B, while all warps still participate in compute. Dir_02 is the restore fallback if that schedule fails quickly, and dir_03 records that steady-state peeling should only be revisited after the copy schedule becomes easier to reason about.`
- dir_01: Human idea async copy: split hot-band copy ownership so lower warps stage A and upper warps stage B | bottleneck: Global-to-shared staging issue regularity and LSU pressure in the hot-band copy phase.
- dir_02: Restore-only fallback if split ownership fails quickly | bottleneck: Not a direct bottleneck attack; this is a branch repair fallback.
- dir_03: Human idea stage: revisit steady-state peeling later, but only on a simpler copy schedule | bottleneck: Fixed-shape stage-transition overhead once the staging schedule itself is cleaner.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
