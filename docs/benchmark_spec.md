# Fixed benchmark specification

## Workload

We start with **one hero GEMM shape** instead of a benchmark suite.

- `A[m, k] * B[k, n] = C[m, n]`
- `m = 6464`
- `n = 7776`
- `k = 7232`
- layout: row-major for `A`, `B`, and `C`
- input dtype: BF16
- reference accumulation dtype: FP32
- stored reference output:
  - `C_ref_fp32`
  - `C_ref_bf16`

## Why this shape

### 1. It is large enough for stable timing

The total floating-point work is:

- `2 * m * n * k = 727,019,421,696 FLOPs`

That is large enough that kernel launch overhead is negligible relative to math and memory behavior.

### 2. It is still practical on a 3070 laptop-class setup

Per case, approximate file sizes are:

- `A_bf16`: 89.16 MiB
- `B_bf16`: 107.26 MiB
- `C_ref_bf16`: 95.87 MiB
- `C_ref_fp32`: 191.74 MiB

This is large, but reasonable for a local fixed dataset that is generated once and reused many times.

### 3. It is intentionally awkward for generic tiling

All three dimensions are multiples of 32, so Tensor Core-friendly fragments remain possible.

But:

- `m = 6464` is **not** divisible by 128
- `n = 7776` is **not** divisible by 128
- `k = 7232` is **not** divisible by 128

That creates an opening for a shape-specialized kernel to remove some generic control-path overhead.

## Cases

Use one shape and multiple seeds.

### Recommended seeds

- `3407`
- `9713`
- `1729`

### Policy

- use `case_00_seed_3407` as the **performance benchmark case**
- use all three cases for **correctness**
- do not average timing across different seeds; the point is to stabilize the benchmark loop

## Distribution

For now, keep the data simple and bounded:

- distribution: uniform
- range: `[-1.0, 1.0]`

Why:

- simple to regenerate,
- no tricky corner cases in v1,
- values stay bounded and numerically tame for BF16 experiments.

## File format

Use raw binary + JSON metadata so both Python and C++ loaders stay simple.

For each case:

```text
case_xx_seed_xxxx/
├── meta.json
├── A.bf16.bin
├── B.bf16.bin
├── C_ref_fp32.bin
├── C_ref_bf16.bin
└── checksums.json
```

### Binary encoding

- `A.bf16.bin`: row-major BF16 payload stored as raw `uint16` BF16 bit patterns
- `B.bf16.bin`: row-major BF16 payload stored as raw `uint16` BF16 bit patterns
- `C_ref_fp32.bin`: row-major raw `float32`
- `C_ref_bf16.bin`: row-major BF16 payload stored as raw `uint16` BF16 bit patterns

### Why not `.npy`

Raw binary is easier to read from a C++/CUDA benchmark binary without bringing in a NumPy parser.

## Correctness policy

Initial recommendation:

- primary comparison target: `C_ref_fp32`
- compare kernel output promoted to FP32
- start with:
  - `rtol = 1e-2`
  - `atol = 1.5e-1`

Also log:

- max absolute error,
- mean absolute error,
- max relative error,
- whether BF16 output matches `C_ref_bf16` exactly or not.

### Important note

Do **not** permanently lock the tolerance until after the first CUTLASS or cuBLAS sanity check on this exact shape. Different accumulation orders can change the error profile.

## Timing policy

For the performance case:

- preload dataset once
- exclude file I/O from timed measurements
- warm up before timing
- clear cache or overwrite a scratch buffer between iterations
- use median runtime as the headline metric
- also log p10 and p90

Suggested starting point:

- warmup iterations: `10`
- timed iterations: `30`
- cache flush scratch size: `256 MiB`

## What should be committed

Commit:

- config JSON,
- generator code,
- checksums or manifests,
- benchmark summaries,
- performance history.

Do **not** commit by default:

- generated data,
- `.rep` files,
- raw NCU CSV dumps,
- large logs.
