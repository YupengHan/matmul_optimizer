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
        - `runs/20260419_232036_bf16_gemm_v1_0c0ee9b/summary.json`
        - `runs/20260419_232036_bf16_gemm_v1_0c0ee9b/ncu_metrics.csv`
        - `runs/20260419_232036_bf16_gemm_v1_0c0ee9b/ncu_details.csv`
        - `runs/20260419_232036_bf16_gemm_v1_0c0ee9b/ncu_profile.ncu-rep`

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

        - round loop: `round 13/50`
        - rounds remaining after this one: `37`
        - latest run id: `20260419_232036_bf16_gemm_v1_0c0ee9b`
        - median runtime: `30.695935 ms`
        - TFLOP/s: `23.684550 TFLOP/s`
        - measured commit: `0c0ee9b007ed96d28f6b3c89a113cc8d68fe88c6`
        - existing diagnosis status: `completed`
