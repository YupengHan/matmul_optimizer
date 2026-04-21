# Human review queue

## Current workflow gate

- next node: `node_a`
- status: `ready_for_node_a`
- round loop: `round 3/50` with `48` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_180213`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 3/50 diagnosis anchored to run `20260420_180146_bf16_gemm_v1_2e4dd24`, which is now the accepted base and the first custom result faster than the local CUTLASS baseline. The ranking therefore stays on the winning grouped-rows-4 PTX surface instead of reopening broad structural pivots. Accepted as the primary family: steady-state hot-band handoff / consume retiming, because the dominant kernel still carries 7.43% long scoreboard and 5.61% barrier stall with tensor active only 48.16%. Accepted as the secondary materially different family: register/export lifetime trimming, because the win did not move the 200-register occupancy wall. Deferred to tertiary: a bounded seam repivot, because the peeled+tail kernels are still barrier-heavy but prior seam evidence remains weaker than the hot-band families. Rejected for this round: reopening K32 or broad fixed-main control families, because the latest measured evidence already beat CUTLASS on the current surface and those broader pivots are not the best next tradeoff.`
- dir_01: Retune The Hot-Band Steady-State Handoff On The New Grouped-Rows-4 Base | bottleneck: Steady-state cp.async handoff latency and fragment-consume ordering inside the active 128x128 PTX hot-band loop, which is still leaving tensor issue on the table after the grouped-row locality fix.
- dir_02: Trim PTX Accumulator And Export Live Range On The New Best Surface | bottleneck: Register pressure and export-side live-state lifetime in the PTX hot-band microkernel, which is capping occupancy before the kernel reaches a memory-throughput limit.
- dir_03: Probe A Bounded Hot-Band Seam Repivot Around The Grouped-Rows-4 Winner | bottleneck: Boundary placement between the 128x128 PTX hot-band kernel and the peeled 64x384 row-band launch, especially whether the fixed 6400-row split is leaving avoidable barrier-heavy work in the secondary kernels.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`
