# Blog Bundle

This folder lives inside the optimization repo as a clean, publish-ready blog subdirectory.

Recommended placement:
- slug directory: `harness-engineering-human-in-the-loop-cuda-matmul`
- article filename inside that directory: `index.md`

What is inside:
- `index.md`: copied verbatim from `/home/aice/Desktop/blog/matmul_blog_draft_v5_all_insights.md`
- `render_round_tree_pretty.py`: updated offline-friendly tree renderer
- `matmul_optimization_tree_pretty.svg`
- `matmul_optimization_tree_pretty.png`

Rerun after the repo history changes:

```bash
python3 render_round_tree_pretty.py \
  --input /home/aice/Desktop/matmul_optimizer/state/round_history.jsonl \
  --cutlass-state /home/aice/Desktop/matmul_optimizer/state/benchmark_baselines.md \
  --output-dir .
```

Notes:
- The article body was not edited.
- The image filenames stay in the same directory as `index.md`, so the existing Markdown image link continues to work.
