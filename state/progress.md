# Progress

## Objective

Beat cuBLAS and drive the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1` to `<= 18.000 ms`.
- target runtime: `<= 18.000 ms`
- comparison target: `cuBLAS`
- rebootstrap source: `20260420_235922_bf16_gemm_v1_489574e`, commit `489574ed5013268dbb79c634450d9a60155a294a`, historical runtime `24.164272 ms`

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `awaiting_direction_selection_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `35400d356bf46fb91f112282fe39c8fa1960b391`
- plateau counter: `15`
- round loop: `single-run`
- rounds remaining: `0`
- notes: `Node B completed. Approve a direction or explicitly use the recommended direction before node_c.`

## Latest measured custom run

- run id: `20260421_160557_bf16_gemm_v1_35400d35`
- run dir: `runs/20260421_160557_bf16_gemm_v1_35400d35`
- correctness: `PASS`
- median runtime: `24.691072 ms`
- TFLOP/s: `29.444627 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260421_163733`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Human guidance review for the current round: registers/thread jumped 34 after the round-10 wait-group collapse, collapsing occupancy to 2 CTAs/SM and regressing long_scoreboard and mio_throttle. The dominant lever is therefore Register Reuse on the existing PTX microkernel (dir_01), which maps the measured evidence onto the Right-Left-Right-Left warp tile guidance. Async Copy / Pg2s / Stage is kept alive on the same surface via dir_02 (3-stage cp.async pipeline) as the latency-hiding complement. The 256x128 Tiling branch remains the high-ceiling future move but is held at rank 3 because two previous reopens regressed; it should only be taken when dir_01 is exhausted or fails.`
- dir_01: Trim PTX 64x64 Microkernel Register Footprint Back To 3-CTA Class | bottleneck: Register-pressure-bound occupancy: 202 regs/thread caps SM residency at 2 CTAs, starving the long_scoreboard / mio_throttle latency hiding budget at 16.58% active warps.
- dir_02: Deepen PTX 128x128 Async Copy Pipeline To A 3-Stage Pg2s Buffer | bottleneck: Global-to-shared latency hiding at low occupancy: long_scoreboard 5.53 (+3.26 vs prev) and mio_throttle 4.0 (+2.23 vs prev) indicate warps are stalling on cp.async completion instead of making tensor-pipe progress.
- dir_03: Reopen 256x128 Half-Panel Register-Reuse Tiling Branch | bottleneck: Tile-granularity / register-reuse ceiling: at 128x128 the A panel is reloaded for every 128 columns; a 256x128 panel doubles A reuse per cp.async batch while keeping B staging compact.

## Active implementation direction

- direction id: `None`
- selection mode: `None`
- status: `idle`
- notes: `No direction selected yet. Use approve, use-recommended-direction, or select-next after node_b.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753616 ms`, `0.932340x` of CUTLASS runtime (faster)
- cuBLAS median runtime: `22.000000 ms`
- current best custom gap vs cuBLAS: `2.164272 ms`, `1.098376x` of cuBLAS runtime (slower)
