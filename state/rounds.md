# Round loop

- active: `yes`
- status: `running`
- total rounds: `20`
- completed rounds: `12`
- remaining rounds: `8`
- current round label: `round 13/20`
- auto use recommended: `yes`
- accepted base run id: `20260418_235548_bf16_gemm_v1_01d0040`
- accepted base measured commit: `01d00409efc03fdf555fef3ea7cc4efd403a720a`
- accepted base runtime: `43.697664 ms`
- started at: `2026-04-18T22:03:53-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 12/20. Continue with node_b for round 13/20. Accepted base: 20260418_235548_bf16_gemm_v1_01d0040 at 43.697664 ms.`

## Last completed round

- round: `12/20`
- direction: `dir_01`
- direction name: `Stage 32-wide K macro-tiles so each sync feeds two MMA slices`
- verdict: `regressed`
- runtime delta: `+1.923071 ms`
- TFLOP/s delta: `-0.689384 TFLOP/s`
- run dir: `runs/20260419_002116_bf16_gemm_v1_134df29`
- ncu rep path: `runs/20260419_002116_bf16_gemm_v1_134df29/ncu_profile.ncu-rep`
