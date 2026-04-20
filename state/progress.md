# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `635342383cfd1f857eecd866e4878dfc14f10ac2`
- plateau counter: `23`
- round loop: `round 82/100`
- rounds remaining: `19`
- notes: `Node C build succeeded for round 82/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_115942_bf16_gemm_v1_6353423`
- run dir: `runs/20260420_115942_bf16_gemm_v1_6353423`
- correctness: `PASS`
- median runtime: `25.837568 ms`
- TFLOP/s: `28.138075 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_120042`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 82/100 diagnosis for run 20260420_115942_bf16_gemm_v1_6353423. The paired PTX export-helper experiment is now explicitly closed-negative: runtime regressed from 25.64300728 ms to 25.83756828 ms and long-scoreboard worsened to 8.09 even though DRAM and barrier stayed low. Keep the broad default-promotion family, the K32 staged family, and the paired-export-lifetime variant closed. The best current baseline remains the PTX microkernel default with zero export padding, so the next work should stay in bounded PTX-adjacent feed / grouping / control paths rather than re-opening any closed broad family.`
- dir_01: Bound The 128x128 Two-Stage Feed Cadence | bottleneck: Feed latency and stage handoff inside the 128x128 two-stage kernel, with the long-scoreboard rise indicating that the current baseline is still waiting too long on data readiness.
- dir_02: Tighten PTX Hot-Band Grouping And Peel Handoff | bottleneck: Hot-band orchestration overhead and peel coordination, especially around grouped-row mapping and the fixed tail handoff.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX export-side indirection versus a simpler two-stage feed path in the non-PTX 128x128 sibling.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
