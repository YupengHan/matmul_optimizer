# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 1/100` with `100` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- select the top frontier candidate: `python scripts/graph.py select-next`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260421_105526`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Re-evaluated the active live queue using the richer NCU diagnosis handoff; promoted register- and barrier-aligned families and demoted export-only families.`
- dir_01: Transplant low-register half-panel staging into the correctness-safe 256x128 pivot | bottleneck: occupancy_latency_hiding_issue with tensor_core_underutilization driven by register pressure and oversized live state
- dir_02: Trim live state inside the active 128x128 PTX control path before more epilogue work | bottleneck: occupancy_latency_hiding_issue on the accepted PTX hot-band path, with a smaller synchronization_barrier_issue component
- dir_03: Collapse PTX wait-group and sync cadence without growing the shared-memory footprint | bottleneck: synchronization_barrier_issue with smaller occupancy side-effects on the PTX 128x128 microkernel

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
