# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_a`
- previous node: `node_c`
- status: `ready_for_node_a`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `c859cd06456e600a76778265983f0cd6da925481`
- plateau counter: `1`
- round loop: `round 1/10`
- rounds remaining: `10`
- notes: `Node C build succeeded for round 1/10. Node A will now measure the new code path.`

## Latest measured custom run

- run id: `20260421_133418_bf16_gemm_v1_c859cd06`
- run dir: `runs/20260421_133418_bf16_gemm_v1_c859cd06`
- correctness: `PASS`
- median runtime: `24.407552 ms`
- TFLOP/s: `29.786659 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_133418_round01_c859cd06`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `No additional human-review-only idea family is queued yet on this clean refactor branch. For round 1/10 the ranking stays tightly coupled to the live profile: test the existing 128x128x32 staged hot-band sibling first, keep the PTX wait-cadence rewrite as the higher-risk second lever, and reserve the 64x384 split rebalance as the third alternative.`
- dir_01: Promote The Existing 128x128x32 Staged Hot-Band Kernel | bottleneck: synchronization_barrier_issue and long_scoreboard latency in the current hot-band 128x128 PTX microkernel
- dir_02: Collapse The PTX Microkernel Wait-And-Sync Cadence | bottleneck: per-tile cp.async wait plus CTA barrier cadence in the PTX hot-band microkernel
- dir_03: Push More Hot-Band Rows Into The 64x384 Peeled Path | bottleneck: hot-band decomposition choice is leaving too much work on the slower 128x128 PTX hotspot instead of the best historical 384-wide family

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `implemented_pending_measurement`
- notes: `Build passed. Node A must measure this implementation next.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.289920 ms`
- current best custom gap vs cuBLAS: `1.874352 ms`, `1.084090x` of cuBLAS runtime (slower)
