# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 8/50` with `43` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_184841`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 8/50 diagnosis for 20260420_184822_bf16_gemm_v1_2ab9365. Human-review audit: state/human_review.md still contains workflow and approval policy only, with no explicit user-supplied idea-family bullets to accept or reject one by one, so the ranking remains measured-evidence-driven. Accepted for this round: bounded micro-tuning on the new grouped-row 128x128 sibling family, because the latest run is correct and only 4.608 microseconds slower than the accepted 2e4dd24 best. The profile shows this is a parity-quality base, not a regression: hot-band kernel time is 32.831584 ms versus 32.801760 ms on 2e4dd24, tensor active is 48.21% versus 48.16%, barrier stalls are 5.62% versus 5.61%, and long-scoreboard stalls are 7.41% versus 7.43%. Deferred: alternate PTX-family handoff retimes, which still have some historical upside but are no longer the first choice now that the sibling branch has reached parity. Rejected for this round: large family pivots such as the 256x128 auxiliary branch, which just failed at 29.10046387 ms and 0/3 correctness on 9144f92, and the broad fixed-main override family, whose autotune evidence belongs to an older surface and whose modern current-regime validations remain far from the 24.44 ms band. The main ranking consequence is that the next move should be a narrow export/shared or seam refinement on the new sibling base, not a restart into a different kernel family.`
- dir_01: Trim The Grouped-Row 128x128 Sibling Export Scratch To The PTX-Style Single Stage | bottleneck: The likely residual bottleneck is shared export/writeback overhead rather than math scheduling. If the single-stage export trim works, it should lower the sibling's shared footprint and reduce the tiny hot-band gap without harming the already-matched barrier and long-scoreboard profile.
- dir_02: Retune The 6400-Row Hot/Peeled Seam On The New Grouped-Row Sibling Base | bottleneck: This branch is constrained by the peeled 64x384 residual path becoming the dominant overhead. If the seam moves the wrong way, total hot-band plus peeled time will worsen even if one kernel improves in isolation.
- dir_03: Reopen The Accepted PTX Handoff Window As The Alternate Control Family | bottleneck: The risk here is that the PTX base is already very close to its local optimum, so a handoff retime may simply move stalls between barrier, scoreboard, and export without producing a real win over the new sibling result.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
