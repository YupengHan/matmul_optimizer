# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 76/100` with `25` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_113413`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Latest measured run 20260420_113238_bf16_gemm_v1_ef8cb27 is a strong negative for the round-75 64x384 default promotion: runtime regressed to 33.59487915 ms from 24.6968317 ms, tensor active fell to 36.06, barrier jumped to 16.62, DRAM throughput rose to 54.20, and launch__occupancy_limit_registers dropped to 1. That closes the 64x384 promotion family for this round. The prior PTX-helper flattening family remains effectively closed-negative as well. Ranking therefore shifts back to restoring a fast default path through the distinct auxiliary 256x128 family first, with the exact PTX default fallback and staged 128x128x32 as lower-rank alternatives.`
- dir_01: Restore The Fast Auxiliary 256x128 Default Hot-Band Path | bottleneck: The 64x384 promotion is exposing DRAM overfetch and barrier amplification rather than compute throughput, so the fix is to return to the lower-overhead 256x128 schedule and recover tensor utilization.
- dir_02: Reinstate The Exact PTX Default Path As The Baseline Fallback | bottleneck: Residual register pressure and scheduler friction in the PTX default hot-band path, but without the wide-tile DRAM blowup seen in the 64x384 promotion.
- dir_03: Try The Staged 128x128x32 Hot-Band Family | bottleneck: Stage synchronization and live-range pressure in a smaller-granularity hot-band kernel, especially under the new barrier-heavy profile.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
