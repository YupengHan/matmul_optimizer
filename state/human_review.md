# Human review queue

## Current workflow gate

- next node: `node_c`
- status: `ready_for_node_c`
- round loop: `round 63/100` with `38` rounds remaining

## Direction approval policy

- explicit approval: `python scripts/graph.py approve --direction dir_02`
- continue with recommended direction: `python scripts/graph.py use-recommended-direction`
- node_c should implement exactly one selected direction

## Latest diagnosis

- diagnosis id: `diagnosis_20260420_091130`
- diagnosis status: `completed`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Diagnosis anchored to run 20260420_091028_bf16_gemm_v1_1d9b03e at 25.281983 ms; exactly three ranked directions recorded for round 63/100.`
- dir_01: Restore accepted base, then retest finer issue granularity on the hot band | bottleneck: Issue granularity and instruction pressure inside the hot-band loop, not higher-level locality. The evidence suggests grouped_rows=4 is still slower than the accepted base and also raises DRAM to 13.05, while nearby consumer/refill variants remain negative.
- dir_02: Accepted base plus narrow overlap recovery behind the one-sync handoff | bottleneck: A short post-handoff gap rather than the broader locality structure. This is the smallest safe tweak after the accepted base is restored.
- dir_03: Small locality closure on the restored grouped_rows=8 base | bottleneck: Residual locality and reuse loss, but only as a secondary issue after the accepted base is back in place.

## Active direction

- selected direction: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one direction.`
