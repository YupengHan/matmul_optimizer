# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4ad2ee7d36377ef1e9439df15b623c6617384aba`
- plateau counter: `11`
- round loop: `round 2/5`
- rounds remaining: `4`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260419_131756_bf16_gemm_v1_4ad2ee7`
- run dir: `runs/20260419_131756_bf16_gemm_v1_4ad2ee7`
- correctness: `PASS`
- median runtime: `35.417503 ms`
- TFLOP/s: `20.527122 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260419_131829`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `All three directions stay inside the 64x384 hot-band PTX microkernel branch. The 64x96 tail remains unchanged. Ranking is anchored on the current accepted PTX base 4ad2ee7: runtime improved materially over the WMMA base, mio dropped to 5.53, but the hot kernel now runs at 172 registers/thread with occupancy_limit_registers=1 and only 16.47 active warps. That makes occupancy and live-state recovery the main guardrail for round 2, while still pushing deeper into explicit PTX fragment/load/export control rather than reverting to generic WMMA tuning.`
- dir_01: Explicit ldmatrix PTX microkernel with smaller hot-band live set | bottleneck: Register footprint and live-fragment residency inside the current PTX hot-band compute body are limiting occupancy and latency hiding; explicit fragment control is needed to lower that footprint without abandoning the PTX branch.
- dir_02: Wrapper-level PTX accumulator phasing before full ldmatrix rewrite | bottleneck: The dominant cost is accumulator live-set size, not the cp.async path and not the tail kernel, so reducing simultaneously resident PTX accumulator tiles should help occupancy first.
- dir_03: Register-first PTX export path after compute-body control | bottleneck: The hot-band export path is still consuming shared/LSU budget and can become the next limiter once mio has already been cut; taking control of export is the natural PTX-branch follow-on after compute-body control.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve or use-recommended-direction after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `8.737343 ms`, `1.337116x` slower than CUTLASS
