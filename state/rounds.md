# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `50`
- completed rounds: `26`
- remaining rounds: `24`
- current round label: `round 27/50`
- auto use recommended: `yes`
- accepted base run id: `20260420_001707_bf16_gemm_v1_8a2834a`
- accepted base measured commit: `8a2834ad9966fb75ef7c310ad5850de8c925ec5e`
- accepted base runtime: `27.227264 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 27/50. Node A will measure the result next.`

## Last completed round

- round: `26/50`
- direction: `dir_01`
- direction name: `Keep the current best branch and peel the fixed 452-tile K loop into steady-state plus epilogue`
- verdict: `regressed`
- runtime delta: `+3.775360 ms`
- TFLOP/s delta: `-3.251636 TFLOP/s`
- run dir: `runs/20260420_001930_bf16_gemm_v1_b4f4a28`
- ncu rep path: `runs/20260420_001930_bf16_gemm_v1_b4f4a28/ncu_profile.ncu-rep`
