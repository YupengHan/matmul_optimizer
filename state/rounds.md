# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `4`
- remaining rounds: `46`
- current round label: `round 5/50`
- auto use recommended: `yes`
- accepted base run id: `20260420_180146_bf16_gemm_v1_2e4dd24`
- accepted base measured commit: `2e4dd246f55b505bd095c42b62c56dc497c8fde1`
- accepted base runtime: `24.444416 ms`
- started at: `2026-04-20T17:42:35-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 4/50. Continue with node_b for round 5/50. Accepted base: 20260420_180146_bf16_gemm_v1_2e4dd24 at 24.444416 ms.`

## Last completed round

- round: `4/50`
- direction: `dir_01`
- direction name: `Trim PTX Accumulator And Export Live Range On The Restored Grouped-Rows-4 Base`
- verdict: `regressed`
- runtime delta: `+0.014848 ms`
- TFLOP/s delta: `-0.016572 TFLOP/s`
- run dir: `runs/20260420_182305_bf16_gemm_v1_e003c0e`
- ncu rep path: `runs/20260420_182305_bf16_gemm_v1_e003c0e/ncu_profile.ncu-rep`
