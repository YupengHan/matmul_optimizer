        # Node B context

        Node B is the diagnosis node. Read the files below, then write exactly three directions to `state/latest_diagnosis.json`.

        ## Read order

        - `state/latest_run.md`
        - `state/latest_ncu_summary.md`
        - `docs/heuristics.md`
        - `state/progress.md`
        - `state/current_focus.md`
        - `state/human_review.md`
        - `src/kernels/bf16_gemm_v1.cu`
        - `runs/20260420_163357_bf16_gemm_v1_a64854a/summary.json`
        - `runs/20260420_163357_bf16_gemm_v1_a64854a/ncu_metrics.csv`
        - `runs/20260420_163357_bf16_gemm_v1_a64854a/ncu_details.csv`
        - `runs/20260420_163357_bf16_gemm_v1_a64854a/ncu_profile.ncu-rep`

- `state/autotune_round18_main_tiles.json`
- `state/autotune_round18_main_tiles.md`


        Use the raw detailed CSV when the headline summary is too shallow to explain pipeline, memory, or bank-conflict behavior.
        Use the autotune sweep summaries when present to anchor direction ranking in measured tile-width data instead of only one run snapshot.

        ## Output contract

        - write exactly 3 directions
        - preserve `direction_id` values `dir_01`, `dir_02`, `dir_03`
        - each direction must include:
          - `hypothesis`
          - `expected_bottleneck`
          - `code_locations`
          - `risk`
          - `metrics_to_recheck`
        - set `recommended_direction_id`
        - after editing the diagnosis file, run `python scripts/graph.py node_b --finalize`

        ## Current source snapshot

        - round loop: `round 14/17`
        - rounds remaining after this one: `3`
        - latest run id: `20260420_163357_bf16_gemm_v1_a64854a`
        - median runtime: `33.964544 ms`
        - TFLOP/s: `21.405246 TFLOP/s`
        - measured commit: `a64854a656796209b16d18c89ea94794379b4ed6`
        - existing diagnosis status: `pending_generation`
