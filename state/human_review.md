# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 71/100` with `30` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_105723`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 71 diagnosis is anchored to run 20260420_105642_bf16_gemm_v1_5a21584 at 25.90719986 ms. The target remains below 20 ms. The current reproducible exact base is the round-69 restore of the accepted surface at 25.49913597 ms, not the older historical 24.57088089 ms snapshot. Round 70 then tested a very narrow one-sync handoff closure by splitting only the final tile out of the hot loop, and it regressed badly while barrier dropped from 6.41 to 4.49 but long_scoreboard jumped from 3.98 to 12.11. That is treated as direct evidence that the handoff-closure family is closed-negative in this current exact-base regime: it mainly trades barrier for scoreboard and loses runtime. Closed-negative families for this round therefore include grouped_rows sweeps, snake locality, fixed-K peeling, export traversal changes, A-first refill, consumer-order sweeps, broad stage overexpansions, and the narrow handoff-closure family itself. Human-idea audit: tiling is already accepted only as the current fixed CTA / warp / 64x64 PTX microtile hierarchy, so retiling is deferred; coalescing and wide global access are already accepted through the current async-copy path; shared-memory reuse is already accepted in the staged A/B tiles; async copy is already accepted; bank-conflict work is accepted only insofar as it preserves the current right-left consume order and exact base semantics, so broad bank-conflict remaps are rejected; L2 locality is closed-negative for grouped_rows and snake-style launch-order variants; register reuse remains open only in a semantics-preserving compute-helper issue-grouping form, which is why dir_01 ranks first; Pg2s remains accepted in the current base; Ps2r remains closed if it implies extra-live staging or broader helper semantics changes; stage work is accepted only as the exact current one-sync base, and the handoff-closure family is now closed-negative in this regime. Ranking rationale: dir_01 is the best next move because it preserves the exact base and attacks the newly exposed long-scoreboard problem at the compute-helper issue-grouping level instead of reopening any closed family. Dir_02 keeps a low-priority export-lifetime check available but explicitly treats export-side second-sync removal as non-primary. Dir_03 keeps one more bounded helper-structure idea on the table without touching launch order, grouped_rows, handoff timing, or export traversal.`
- dir_01: Restore the exact round-69 base, then change PTX issue grouping inside the 64x64 compute helpers without changing accepted traversal semantics | bottleneck: PTX compute-helper issue grouping and scheduler behavior inside the accepted 64x64 hot-band microkernel, now exposed as long scoreboard after the handoff family was falsified.
- dir_02: Restore the exact round-69 base, then do only a low-priority export-scratch lifetime cleanup while keeping linear export order | bottleneck: Residual export scratch lifetime and writeback overhead on the exact accepted base, after accepting that second-sync removal alone does not buy real runtime.
- dir_03: Restore the exact round-69 base, then simplify PTX helper control structure without changing accepted loop or launch semantics | bottleneck: Helper-control and codegen overhead around the accepted PTX compute path rather than launch locality, handoff timing, or export order.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
