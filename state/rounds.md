# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `5`
- completed rounds: `4`
- remaining rounds: `1`
- current round label: `round 5/5`
- auto use recommended: `yes`
- accepted base run id: `20260419_104631_bf16_gemm_v1_8346b48`
- accepted base measured commit: `8346b48ca5272beb86282fa09eb346dc73ab9f68`
- accepted base runtime: `34.655231 ms`
- started at: `2026-04-19T10:16:39-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 5/5. Node A will measure the result next.`

## Last completed round

- round: `4/5`
- direction: `dir_01`
- direction name: `Micro-retune the single-level B skew in the peeled 64x384 hot kernel`
- verdict: `regressed`
- runtime delta: `+0.310865 ms`
- TFLOP/s delta: `-0.186510 TFLOP/s`
- run dir: `runs/20260419_105226_bf16_gemm_v1_edb3741`
- ncu rep path: `runs/20260419_105226_bf16_gemm_v1_edb3741/ncu_profile.ncu-rep`
