# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 10/30` with `21` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260419_222558`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 10/30 starts from the clearest negative branch in several rounds. Splitting copy ownership across half the CTA spiked registers and both major staging stalls while slowing the dominant hot-band kernel, so there is no value in refining it. Recommended direction dir_01 therefore restores the pre-split surface immediately. Dir_02 records the next orthogonal family to try after that restore: trimming the hot-band export path instead of touching the copy path again. Dir_03 is a stricter baseline re-anchor if measurement drift remains confusing.`
- dir_01: Restore the restored best surface and discard the split-ownership staging branch | bottleneck: Not a new bottleneck attack; this is a branch reset after a strongly negative staging-ownership experiment.
- dir_02: After the restore, trim the hot-band export path instead of the copy path | bottleneck: Hot-band epilogue / export LSU and shared-memory round-trip overhead.
- dir_03: Re-anchor the loop explicitly at the recorded best custom measurement `5dd9f0d` | bottleneck: Workflow / baseline drift rather than a specific micro-bottleneck.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
