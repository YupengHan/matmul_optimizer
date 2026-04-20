# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `af42390db4796a6bfb2b8e1b21751cf877ed7a86`
- plateau counter: `24`
- round loop: `round 83/100`
- rounds remaining: `18`
- notes: `Node C build succeeded for round 83/100. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260420_120349_bf16_gemm_v1_af42390`
- run dir: `runs/20260420_120349_bf16_gemm_v1_af42390`
- correctness: `PASS`
- median runtime: `25.904127 ms`
- TFLOP/s: `28.065776 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_120428`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 83/100 diagnosis for run 20260420_120349_bf16_gemm_v1_af42390. The bounded 128x128 two-stage cadence experiment is now effectively closed as a distinct next step: it was flat-to-slightly-negative versus the best PTX baseline, with runtime 25.90412712 ms, barrier 5.24, mio 3.00, but dram 30.18 and long scoreboard 7.22. The paired-export-lifetime variant remains closed-negative, and the best current baseline stays the PTX microkernel default with zero export padding. The next work should target long-scoreboard reduction at the PTX hot-band grouping / orchestration boundary or use another narrow PTX-adjacent control path, not reopen the closed broad families.`
- dir_01: Tighten PTX Hot-Band Grouping For Long-Scoreboard | bottleneck: Long-scoreboard stalls caused by hot-band orchestration, grouped-row mapping, and tail handoff in the PTX microkernel path.
- dir_02: Low-Risk PTX Export-Side Cleanup | bottleneck: Residual address-generation and scratch-lifetime overhead in the PTX store helpers.
- dir_03: Use The Non-PTX 128x128 Sibling As A Control | bottleneck: PTX export/store complexity versus a simpler non-PTX 128x128 feed path.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.347008 ms`, `0.948028x` slower than CUTLASS
