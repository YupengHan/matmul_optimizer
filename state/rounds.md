# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `5`
- completed rounds: `4`
- remaining rounds: `1`
- current round label: `round 5/5`
- auto use recommended: `no`
- accepted base run id: `20260419_122438_bf16_gemm_v1_15d63b2`
- accepted base measured commit: `15d63b2993c6eecc3a912dc4a648de6294e82efc`
- accepted base runtime: `35.725824 ms`
- started at: `2026-04-19T12:25:01-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 5/5. Node A will measure the result next.`

## Last completed round

- round: `4/5`
- direction: `dir_01`
- direction name: `Use a warp-local consumer-side B load swizzle on the peeled 64x384 hot path`
- verdict: `regressed`
- runtime delta: `+450.342323 ms`
- TFLOP/s delta: `-16.017567 TFLOP/s`
- run dir: `runs/20260419_125107_bf16_gemm_v1_52747c0`
- ncu rep path: `runs/20260419_125107_bf16_gemm_v1_52747c0/ncu_profile.ncu-rep`
