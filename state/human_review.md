# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 37/100` with `64` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_075421`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 37 explicitly chooses exploration over reflex recovery. The latest PTX control-path cleanup did not win, but it moved barrier and long-scoreboard in the right direction while staying within 0.02 ms of the restored base. That is exactly the kind of partial signal that justifies one more tightly bounded scheduler-seam retime before the loop falls back to restore or jumps to the broader 256x128 family.`
- dir_01: Steady-state Barrier / Handoff Retime | bottleneck: Residual wait-group and barrier cadence in the PTX hot-band steady-state loop, especially the seam between finishing the current MMA stage and refilling the reused stage buffer for the future tile.
- dir_02: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Known register-limited plateau on the accepted PTX hot-band surface, used here as a clean recovery anchor if the scheduler-seam follow-up loses signal.
- dir_03: Transplant The Half-Panel Register Budget Into The Correct 256x128 Pivot | bottleneck: Register footprint and synchronization strategy on the 256x128 hot-band path, plus correctness-sensitive writer ownership.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`
