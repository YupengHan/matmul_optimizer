# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `28`
- remaining rounds: `22`
- current round label: `round 29/50`
- auto use recommended: `yes`
- accepted base run id: `20260420_002119_bf16_gemm_v1_c26ac4f`
- accepted base measured commit: `c26ac4fdc00ad89cefc324b30d4fc8758fb4d0af`
- accepted base runtime: `27.022336 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 28/50. Continue with node_b for round 29/50. Accepted base: 20260420_002119_bf16_gemm_v1_c26ac4f at 27.022336 ms.`

## Last completed round

- round: `28/50`
- direction: `dir_01`
- direction name: `Keep the current best branch and raise the hot-band K16 loop to the next small unroll factor`
- verdict: `regressed`
- runtime delta: `+2.640384 ms`
- TFLOP/s delta: `-2.394855 TFLOP/s`
- run dir: `runs/20260420_002230_bf16_gemm_v1_7c672be`
- ncu rep path: `runs/20260420_002230_bf16_gemm_v1_7c672be/ncu_profile.ncu-rep`
