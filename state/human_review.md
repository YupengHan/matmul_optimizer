# Human review queue

## Pending decisions

### 1. Benchmark shape lock

Proposed hero shape:

- `m=6464, n=7776, k=7232`

Reason:

- large enough for stable timing,
- all dimensions multiples of 32,
- none are multiples of 128,
- still practical for a single 3070 laptop-class GPU.

Status: IMPLEMENTED DEFAULT

---

### 2. Initial correctness tolerance policy

Proposed starting policy:

- compare promoted output against `C_ref_fp32`
- start with `rtol=1e-2`, `atol=1.5e-1`
- recalibrate after the first CUTLASS sanity run

Status: IMPLEMENTED DEFAULT

---

### 3. CUTLASS baseline cadence

Proposed policy:

- run once early,
- refresh every ~10 non-improving rounds,
- refresh after major kernel rewrites

Status: PENDING AFTER FIRST VALID BASELINE
