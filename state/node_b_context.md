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
        - `runs/20260420_002119_bf16_gemm_v1_c26ac4f/summary.json`
        - `runs/20260420_002119_bf16_gemm_v1_c26ac4f/ncu_metrics.csv`
        - `runs/20260420_002119_bf16_gemm_v1_c26ac4f/ncu_details.csv`
        - `runs/20260420_002119_bf16_gemm_v1_c26ac4f/ncu_profile.ncu-rep`

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

        - round loop: `round 28/50`
        - rounds remaining after this one: `22`
        - latest run id: `20260420_002119_bf16_gemm_v1_c26ac4f`
        - median runtime: `27.022336 ms`
        - TFLOP/s: `26.904388 TFLOP/s`
        - measured commit: `c26ac4fdc00ad89cefc324b30d4fc8758fb4d0af`
        - existing diagnosis status: `pending_generation`
