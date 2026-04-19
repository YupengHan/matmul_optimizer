# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `5`
- completed rounds: `1`
- remaining rounds: `4`
- current round label: `round 2/5`
- auto use recommended: `no`
- accepted base run id: `20260419_122438_bf16_gemm_v1_15d63b2`
- accepted base measured commit: `15d63b2993c6eecc3a912dc4a648de6294e82efc`
- accepted base runtime: `35.725824 ms`
- started at: `2026-04-19T12:25:01-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 2/5. Node A will measure the result next.`

## Last completed round

- round: `1/5`
- direction: `dir_01`
- direction name: `Warp-specialize the peeled 64x384 hot loop into producer and consumer warps`
- verdict: `regressed`
- runtime delta: `+6.534143 ms`
- TFLOP/s delta: `-3.146468 TFLOP/s`
- run dir: `runs/20260419_123228_bf16_gemm_v1_1dd4420`
- ncu rep path: `runs/20260419_123228_bf16_gemm_v1_1dd4420/ncu_profile.ncu-rep`
