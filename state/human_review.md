# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 19/50` with `32` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_000335`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human-idea reflection for round 19: Register Reuse becomes the primary family because the last two rounds showed that increasing shared-memory footprint is what killed active warps, while the 128x128 K16 branch already has the best stage/data-reuse balance. Async Copy, Data Reuse, Pg2s, Ps2r, and Stage remain accepted background choices because the winning kernel depends on them; the point now is to preserve that machinery while giving the compiler a chance to reduce live register pressure. Tiling 256x128 and deeper multi-stage overlap are deferred after two measured regressions. Coalescing Access and Bank Conflict are still deferred because the better and worse runs are not separating primarily on those signals. The L2 clue remains deferred but stays on the board as the next orthogonal axis if CTA-local occupancy tuning stalls.`
- dir_01: Restore the 128x128 K16 winner and add a register-pressure / launch-bounds hint to chase higher occupancy | bottleneck: Register-limited occupancy in the accepted 128x128 K16 hot-band kernel. The target is to increase resident blocks or at least reduce register pressure enough to lift warps active and tensor active.
- dir_02: Keep the 128x128 K16 base and tighten the consume fence only where overwrite actually occurs | bottleneck: Barrier overhead in the accepted 128x128 K16 mainloop.
- dir_03: Hold the CTA-local kernel fixed and try the deferred L2-friendly block-order clue | bottleneck: Inter-CTA cache locality rather than within-CTA tensor feed.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
