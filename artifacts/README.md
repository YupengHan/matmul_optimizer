# Local artifacts

This directory is for locally generated, non-git-tracked artifacts.

Examples:

- generated dataset binaries
- benchmark run outputs
- Nsight Compute reports
- CSV summaries
- logs
- temporary build outputs

Recommended structure:

```text
artifacts/
├── datasets/
│   └── fixed_bf16_gemm_v1/
└── ...
```

Large binaries should stay local unless you intentionally use a release artifact or external storage.
