# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 38/100` with `63` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_011928`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 38/100 diagnoses run 20260420_011851_bf16_gemm_v1_f8e7058 at 26.150880 ms on the active 128x128 K16 PTX hot-band branch. The branch had previously recovered to 26.093568 ms. Then two bounded consumer-side B-reuse iterations failed to produce an end-to-end win: round 36 moved to 26.128304 ms while collapsing mio_throttle from 4.45% to 0.48%, but short-scoreboard rose from 1.67% to 5.89% and barrier from 8.05% to 10.95%; round 37 removed the next_b_frag lookahead and still landed at 26.150880 ms with short-scoreboard 5.88%, barrier 10.90%, long-scoreboard 1.15%, tensor-active 48.05%, DRAM 36.56%, L2 31.14%, and mio_throttle still 0.48%. Treat that as the stop condition for consumer-side B reuse as the current primary path: the feed-side signal is real, but the current form is not paying off end to end. Human-idea audit for this round, family by family: Tiling is rejected as the primary family because the real 256x128 promotion already regressed badly and the active 128x128 PTX path remains the best live branch. Coalescing Access is deferred because the active path already uses 16-byte cp.async global movement and the latest regressions are not explained by under-packed global transactions. Data Reuse is accepted only in the existing shared-memory baseline plus a bounded narrower consumer-side fallback; CTA-level repack remains rejected. Async Copy is accepted only as the current two-stage non-blocking baseline; no deeper rewrite is recommended this round. Bank Conflict is accepted and now promoted through the export-path lens because once mio_throttle collapsed, c_shared bank writes and export-side shared behavior became a more plausible next limiter. L2 Cache is deferred; grouped launch-order work was useful earlier, but the current evidence still points inside the active PTX branch before another L2-oriented pass. Register Reuse is accepted in two bounded forms: lighter export live-set and a narrower consumer-side fallback, not another broader fusion. Pg2s is accepted only as the existing baseline. Ps2r is accepted only for narrower warp-local consume cleanup, not as the mainline direction after two failed B-reuse rounds. Stage is deferred beyond the current two-stage baseline because deeper stage experiments already lost badly. The target remains 20 ms, not merely the 25.917889 ms CUTLASS baseline, so the ranking stays centered on the active PTX hot-band branch and now prefers export-path / c_shared / shared-bank-overhead work as the next primary family.`
- dir_01: Trim the active PTX export path and c_shared round-trip before touching feed again | bottleneck: Shared-memory export overhead on the active PTX hot-band branch, especially c_shared bank writes, LSU wavefront pressure, and synchronization after the MMA loop.
- dir_02: Back off to a narrower consumer-side B-reuse variant instead of the current two-row-pair fusion | bottleneck: Over-extended warp-local fragment lifetime in the active PTX consumer path, where the current B reuse removes MIO pressure but turns it into short-scoreboard dependency chains and exposed synchronization.
- dir_03: Do one explicit fixed-shape PTX sequencing cleanup pass without adding deeper stages | bottleneck: Fixed-shape orchestration overhead in the active PTX K16 loop, where wait-group choice and block-wide synchronization may still be too generic for a 452-tile steady state.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
