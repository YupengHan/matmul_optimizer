# Round loop

- active: `yes`
- status: `awaiting_measurement`
- total rounds: `100`
- completed rounds: `49`
- remaining rounds: `51`
- current round label: `round 50/100`
- auto use recommended: `yes`
- accepted base run id: `20260420_074331_bf16_gemm_v1_17a33b2`
- accepted base measured commit: `17a33b29fc2405c9fb3c5602d09a1c52bc42b32d`
- accepted base runtime: `25.529328 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Build passed for round 50/100. Node A will measure the result next.`

## Last completed round

- round: `49/100`
- direction: `dir_01`
- direction name: `Retune The Accepted Grouped-Row=8 PTX Hot Band Around Stage Cadence`
- verdict: `regressed`
- runtime delta: `+5.968479 ms`
- TFLOP/s delta: `-5.309118 TFLOP/s`
- run dir: `runs/20260420_075705_bf16_gemm_v1_47484fa`
- ncu rep path: `runs/20260420_075705_bf16_gemm_v1_47484fa/ncu_profile.ncu-rep`
