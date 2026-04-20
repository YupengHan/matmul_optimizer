# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 10/10` with `1` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_214233`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Final-round audit after the round-9 regression and restore to the stronger round-8 implementation surface: Tiling remains accepted at the 64x384 hot-band shape; Coalescing Access, Data Reuse, Async Copy, and Pg2s remain baseline; L2 Cache, fixed-shape Stage, and the footprint-neutral B shared permutation are all now explicitly treated as tested-negative for this loop; the round-8 streaming B-consumer branch remains the best recent positive signal because it improved runtime and feed-side metrics without increasing registers or shared memory. That means the strongest remaining final-round bet is not another tiny B-layout permutation, but a more orthogonal complement on top of the restored round-8 feed branch. Recommended direction dir_01 therefore spends the last round on producer/consumer warp specialization over the round-8 streaming path: if the feed path is cleaner and the result is still occupancy-limited, the remaining upside is likely orchestration rather than another narrow layout tweak.`
- dir_01: Warp-specialized producer/consumer on top of the restored round-8 streaming B branch | bottleneck: All-warps staging and handoff overhead after the most obvious warp-local B feed pressure has already been reduced.
- dir_02: Human idea Ps2r on the restored round-8 streaming branch: one-fragment shared-to-register lookahead | bottleneck: Residual shared-to-register feed latency inside the hot-band 64x64 micro-tile after the round-8 consumer refactor.
- dir_03: Trim the hot-band export path so the feed-side gains are not spent back in the epilogue | bottleneck: Epilogue/export LSU and shared-memory round-trip overhead after the feed path has already been partially improved.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
