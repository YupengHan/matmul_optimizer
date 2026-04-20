# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 6/10` with `5` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_210902`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 6 human-idea audit against the latest correct-branch evidence: Tiling stays accepted and fixed at 256x128 / 64x64; Coalescing Access, Data Reuse, Async Copy, and Pg2s stay accepted as baseline infrastructure already present in the kernel; Bank Conflict is still a valid correct-branch family, but round 5 showed that a first issue-order retune had only tiny overall signal and no hot-band win, so it is no longer the top choice; L2 Cache remains deferred because the branch is not L2-bound; Register Reuse is accepted only in the narrow internal-order sense on the correct branch, not as a return to half-panel; Ps2r remains a valid but higher-risk family because the branch is already at 167 regs/thread; Stage becomes the primary idea this round because the shape is fixed, the current loop still carries generic control, and the lower-risk layout/order experiments have not moved the true hotspot enough. Recommended direction dir_01 therefore specializes the fixed 452-tile hot loop before spending more rounds on higher-register feed tricks.`
- dir_01: Human idea 10 Stage: keep the correct hot kernel, but specialize the fixed 452-tile loop into explicit prologue / steady-state / epilogue control | bottleneck: Generic steady-state loop control and stage-transition overhead in the true hot-band kernel rather than operand layout.
- dir_02: Human idea 9 Ps2r: add a one-fragment shared-to-register lookahead inside the correct full-width sweep | bottleneck: Warp-local shared-to-register delivery latency inside the full-width hot-band sweep.
- dir_03: Human idea 5 bank-conflict follow-through: keep the correct branch and retune the warp-local B consumer again, but on a different pair schedule | bottleneck: Warp-local B-fragment order and bank behavior on the correct hot-band kernel.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
