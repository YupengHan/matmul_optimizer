# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 40/100` with `61` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_013539`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 40/100 should be ranked around restoring the accepted round-38 branch first, because round 39 isolated a decisive causal signal: keeping the padded PTX export scratch while reverting the active PTX branch back to the baseline accumulate helper regressed from 25.974272 ms at commit e26d834 to 26.733056 ms at commit 98fb432 and restored the older stall shape of barrier 8.09, short_scoreboard 1.78, and mio_throttle 4.54. That means the accepted win depends on the aggressive consumer-side B-reuse branch being present, not on export-path padding alone. Human-idea audit for this round: Tiling is rejected as the primary move because the active 256x128 CTA / 64x64 warp promotion already regressed badly on the real default path; Coalescing Access is accepted as already implemented through 16-byte async copy and wide shared staging, but it is not the next differentiator; Data Reuse is accepted and remains central because the accepted branch's advantage disappears when the warp-local B-fragment reuse path is removed; Async Copy is accepted only as the current working baseline and a deeper rewrite is deferred because earlier x32 and deeper-stage variants regressed; Bank Conflict is accepted and ranked primary through consumer-side B delivery and padded export scratch; L2 Cache is deferred because grouped ordering helped an earlier branch but does not explain the round-38 versus round-39 split; Register Reuse is accepted and primary because the best remaining upside is keeping more value from each loaded B fragment without reintroducing old mio pressure; Pg2s is accepted as already in place; Ps2r is accepted and primary because the next move is warp-local consume sequencing rather than CTA repack; Stage is deferred or rejected for now because barrier is already material and the recent evidence favors smarter consume ordering over deeper pipeline machinery. The ranking stays centered on the 20 ms target rather than merely edging out the 25.92 ms CUTLASS result.`
- dir_01: Restore The Accepted PTX B-Reuse Branch And Clean Up Warp-Local Sequencing | bottleneck: Warp-local consumer orchestration inside the active 128x128 K16 PTX hot loop, not CTA tiling or global-memory staging. The accepted branch drove mio_throttle down to 0.55% but paid 5.87% short_scoreboard and 11.13% barrier; the reverted branch restored the older 4.54% mio pattern. The highest-upside low-risk follow-up is to preserve the full reuse path and retime how B fragments are loaded and consumed within the warp.
- dir_02: Restore The Accepted PTX B-Reuse Branch And Tighten The Padded Export Scratch | bottleneck: Shared export overhead after the hot loop, especially c_shared bank writes and LSU wavefront pressure in the PTX-only export helpers. Once the accepted branch has already collapsed mio_throttle, additional time is more likely trapped in export scratch movement than in another CTA-level staging rewrite.
- dir_03: Restore The Accepted PTX B-Reuse Branch And Push A More Explicit PTX Steady-State Sequence | bottleneck: Instruction scheduling and fragment-residency overhead inside the active PTX hot-band loop. The round-38 accepted branch already showed that explicit warp-local B delivery can beat the restored baseline; the next ceiling-raising step is to make the PTX sequence itself more deliberate rather than relying on the current recursive helper structure forever.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
