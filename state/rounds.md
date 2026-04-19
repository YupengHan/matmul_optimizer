# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `20`
- completed rounds: `15`
- remaining rounds: `5`
- current round label: `round 16/20`
- auto use recommended: `yes`
- accepted base run id: `20260418_235548_bf16_gemm_v1_01d0040`
- accepted base measured commit: `01d00409efc03fdf555fef3ea7cc4efd403a720a`
- accepted base runtime: `43.697664 ms`
- started at: `2026-04-18T22:03:53-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 16/20. Node A will measure the result next.`

## Last completed round

- round: `15/20`
- direction: `dir_02`
- direction name: `Retile CTA and warp partition to trim per-warp N baggage`
- verdict: `regressed`
- runtime delta: `+14.435743 ms`
- TFLOP/s delta: `-4.119578 TFLOP/s`
- run dir: `runs/20260419_005208_bf16_gemm_v1_8fbd2e5`
- ncu rep path: `runs/20260419_005208_bf16_gemm_v1_8fbd2e5/ncu_profile.ncu-rep`
