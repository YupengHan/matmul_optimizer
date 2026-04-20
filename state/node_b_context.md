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
        - `runs/20260419_191708_bf16_gemm_v1_b13027c/summary.json`
        - `runs/20260419_191708_bf16_gemm_v1_b13027c/ncu_metrics.csv`
        - `runs/20260419_191708_bf16_gemm_v1_b13027c/ncu_details.csv`
        - `runs/20260419_191708_bf16_gemm_v1_b13027c/ncu_profile.ncu-rep`

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

        - round loop: `round 16/20`
        - rounds remaining after this one: `4`
        - latest run id: `20260419_191708_bf16_gemm_v1_b13027c`
        - median runtime: `30.052768 ms`
        - TFLOP/s: `24.191430 TFLOP/s`
        - measured commit: `b13027cdde2a90d1f00f3bd9b1e6b355ea15f2d9`
        - existing diagnosis status: `pending_generation`
