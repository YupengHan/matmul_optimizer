# Progress

## Objective

Beat the local CUTLASS baseline on the fixed-shape BF16 GEMM `fixed_bf16_gemm_v1`.

## Workflow state

- next node: `node_c`
- previous node: `node_b`
- status: `ready_for_node_c`
- current kernel path: `src/kernels/bf16_gemm_v1.cu`
- latest measured commit: `4bc0218b26dba8ac7adf77968d7d74314c47ed84`
- plateau counter: `4`
- round loop: `round 12/100`
- rounds remaining: `89`
- notes: `Node C is ready to implement diagnosis_20260420_233659:dir_01 via recommended selection for round 12/100.`

## Latest measured custom run

- run id: `20260420_233546_bf16_gemm_v1_4bc0218`
- run dir: `runs/20260420_233546_bf16_gemm_v1_4bc0218`
- correctness: `PASS`
- median runtime: `24.173968 ms`
- TFLOP/s: `30.074476 TFLOP/s`
- latest run summary: `state/latest_run.json`
- latest NCU summary: `state/latest_ncu_summary.json`

## Latest diagnosis state

- diagnosis status: `completed`
- diagnosis id: `diagnosis_20260420_233659`
- recommended direction: `dir_01`
- approved direction: `None`
- diagnosis notes: `Round 12/100 audit: the latest run's dominant hot-band launch is the non-PTX sibling `bf16_gemm_v1_tensor_core_fixed_hot_band_128x128_kernel<(int)452>`, and the current source confirms that `launch_bf16_gemm_v1` dispatches that sibling by default instead of the PTX microkernel that produced the 24.16435242 ms best-known run. That makes the current frontier ranking stale for one round: another PTX-local barrier or control retime would be reasoning about the wrong active surface. The diagnosis therefore leads with a coherent PTX restore, keeps one alternate PTX restore alive, and carries one orthogonal round-history fallback so the live search queue stays broad enough after the recent policy change.`
- dir_01: Restore The Best Measured PTX Grouping Window On The Accepted Surface | bottleneck: Search-surface drift between the currently measured non-PTX hot-band dispatch and the PTX microkernel surface that still owns the 24.164352 ms best-known runtime.
- dir_02: Restore accepted grouped_rows=8 hot-band consumer ordering | bottleneck: Consumer-side ordering and grouped-row locality inside the PTX hot-band microkernel, especially around grouped CTA mapping and the consumer/export handoff.
- dir_03: Retune The Auxiliary 256x128 Hot-Band K-Loop Schedule | bottleneck: Compute scheduling and latency hiding on the auxiliary 256x128 hot-band path, not DRAM bandwidth and not another grouped-row PTX locality retime.

## Active implementation direction

- direction id: `dir_01`
- selection mode: `recommended`
- status: `ready_for_implementation`
- notes: `Node C may now implement this one candidate.`

## Benchmark snapshot

- CUTLASS median runtime: `25.917889 ms`
- current best custom gap: `-1.753536 ms`, `0.932343x` slower than CUTLASS
