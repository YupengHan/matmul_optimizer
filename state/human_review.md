# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 39/100` with `62` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_013034`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 39/100 audits the human-idea families against the latest measured evidence as follows. Tiling: rejected for this round, because the true active 256x128 CTA plus 64x64 warp path already measured around 31.61 ms and is far behind the current 25.974272 ms active 128x128 K16 PTX branch. Coalescing Access: deferred, because the active branch already uses 16-byte cp.async global-to-shared movement and the current profile is not DRAM- or L2-led. Data Reuse: accepted only in a narrower warp-local form on the active PTX branch; CTA-side B repack remains rejected. Async Copy: deferred to the current working non-blocking two-stage baseline instead of reopening deeper pipeline work. Bank Conflict: accepted and promoted, because the export scratch change already paid off and the remaining issue mix still points at shared delivery and shared export behavior. L2 Cache: deferred; grouped launch ordering helped earlier, but the present stall mix points inside the active PTX branch before another L2-oriented pass. Register Reuse: accepted as the primary family, because the best current explanation is that feed pressure was improved while fragment lifetime and consume ordering stayed too expensive. Pg2s: deferred beyond the existing double-buffer baseline. Ps2r: accepted as part of the narrower consumer-side fallback and the sequencing-cleanup reserve path. Stage: rejected as a primary direction for this round, because deeper or alternative stage experiments already regressed badly. The goal remains 20 ms, not merely the 25.917889 ms CUTLASS baseline, so the ranking stays centered on the active 128x128 K16 PTX hot-band branch and recommends keeping the export-path gain while first testing a narrower consumer-side B-reuse fallback that may give back some of the current short-scoreboard and barrier cost.`
- dir_01: Keep the export-path gain and narrow the active PTX consumer-side B reuse | bottleneck: Warp-local dependency chains and synchronization exposure in the active PTX consume path, where the current B-fragment reuse shape keeps feed pressure low but still leaves short-scoreboard and barrier cost too high.
- dir_02: Refine the active PTX export path again without reopening feed | bottleneck: Shared-memory export overhead after the MMA loop on the active PTX branch, especially c_shared bank traffic, LSU wavefront pressure, and warp-local synchronization inside the paired export helpers.
- dir_03: Do a fixed-shape PTX sequencing cleanup on the active hot loop | bottleneck: CTA-level orchestration overhead in the active PTX hot loop, where fixed-shape staging and synchronization may still be more generic than necessary and continue to surface as barrier cost.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
