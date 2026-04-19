# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 1/20` with `20` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260418_220408`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- dir_01: Widen the async staging path to 16-byte fixed-tile copies | bottleneck: Global-to-shared staging instruction pressure and MIO throttling from the current 8-byte async copy path, not a pure DRAM bandwidth ceiling.
- dir_02: Skew the shared tiles for bank-friendlier WMMA fragment loads | bottleneck: Shared-memory and fragment-load pressure around `wmma::load_matrix_sync`, currently surfacing as high `smsp__warp_issue_stalled_mio_throttle` with only moderate DRAM and L2 throughput.
- dir_03: Peel the fixed 7232-K loop into a branch-light steady-state pipeline | bottleneck: Synchronization and control overhead inside the generic per-slice K loop, showing up as persistent barrier and long-scoreboard stalls even after the round-4 reuse win.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
