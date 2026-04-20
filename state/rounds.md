# Round loop

- active: `yes`
- status: `running`
- total rounds: `50`
- completed rounds: `22`
- remaining rounds: `28`
- current round label: `round 23/50`
- auto use recommended: `yes`
- accepted base run id: `20260420_001122_bf16_gemm_v1_273d63c`
- accepted base measured commit: `273d63c0dca706eb94e279d165295463933a4b5c`
- accepted base runtime: `28.949504 ms`
- started at: `2026-04-19T22:34:28-07:00`
- completed at: `None`
- history path: `state/round_history.jsonl`
- notes: `Completed round 22/50. Continue with node_b for round 23/50. Accepted base: 20260420_001122_bf16_gemm_v1_273d63c at 28.949504 ms.`

## Last completed round

- round: `22/50`
- direction: `dir_01`
- direction name: `Keep the grouped CTA-order remap and increase the hot-band row-group size to deepen B-tile reuse`
- verdict: `regressed`
- runtime delta: `+0.370160 ms`
- TFLOP/s delta: `-0.317056 TFLOP/s`
- run dir: `runs/20260420_001248_bf16_gemm_v1_4fc47fd`
- ncu rep path: `runs/20260420_001248_bf16_gemm_v1_4fc47fd/ncu_profile.ncu-rep`
