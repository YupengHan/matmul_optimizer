# GPU matmul optimization heuristics

This document is for the diagnosis and implementation agents.

The point is **not** to dump every CUDA trick.  
The point is to help the diagnosis node turn a profile into **three concrete next moves**.

## How to use this file

When reading a run:

1. identify the dominant bottleneck class,
2. select three directions from different families,
3. rank them by expected upside vs implementation risk,
4. avoid proposing three variants of the same idea.

## Fixed-shape mindset

This repository is not optimizing arbitrary GEMM.  
It is optimizing **one fixed GEMM shape**.

That means the kernel can exploit:

- compile-time constants for `m`, `n`, and `k`,
- specialized tile loops,
- minimized edge predicates,
- shape-aware stage counts,
- specialized epilogue assumptions,
- and offline-tuned launch parameters.

Do not throw that advantage away by defaulting to generic abstractions.

## Primary bottleneck classes

## 1. Tensor Core under-utilization

Typical symptom:

- runtime is poor,
- tensor pipe activity looks low,
- memory throughput is not obviously saturated.

Possible causes:

- poor warp-level MMA scheduling,
- not enough ready warps,
- register pressure too high,
- stage pipeline too shallow,
- tail/edge handling overhead,
- instruction mix diluted by scalar cleanup work.

Candidate directions:

- retune CTA / warp / MMA tile hierarchy,
- reduce predicates in the hot path,
- increase pipeline stages,
- reduce register pressure to improve active warps,
- specialize edge handling out of the main loop.

---

## 2. Global-memory bound

Typical symptom:

- DRAM or L2 throughput is high relative to compute activity,
- tensor pipe is starved,
- global load efficiency is weak,
- runtime barely changes with more aggressive math scheduling.

Possible causes:

- uncoalesced loads,
- weak vectorization,
- poor data reuse from shared memory,
- unnecessary rereads,
- too-small tiles causing low arithmetic intensity.

Candidate directions:

- vectorize global loads/stores,
- enlarge reuse tiles where register budget allows,
- use `cp.async` or equivalent staged global-to-shared copy path,
- improve shared-memory staging layout,
- reduce redundant movement of `A` / `B` fragments.

---

## 3. Shared-memory bottleneck

Typical symptom:

- shared-memory instructions dominate,
- bank-conflict behavior appears bad,
- warps stall around shared-memory communication,
- Tensor Cores are available but underfed.

Possible causes:

- poor shared layout for `ldmatrix` / fragment loads,
- insufficient swizzle or padding,
- too much shared traffic due to weak register reuse,
- stage count amplifies shared pressure.

Candidate directions:

- change shared-memory layout or swizzle,
- add padding to avoid bank conflicts,
- rebalance shared-vs-register reuse,
- reduce unnecessary shared round-trips,
- retune stage depth.

---

## 4. Occupancy or latency-hiding problem

Typical symptom:

- achieved occupancy or active warps are low,
- register usage per thread is high,
- kernel is latency-bound even without huge memory throughput,
- performance improves when work is split more finely.

Possible causes:

- over-unrolled inner loops,
- too-large tile shape,
- too many fragments resident at once,
- excessive accumulator footprint,
- local memory spills.

Candidate directions:

- reduce tile size,
- reduce unroll depth,
- reduce fragment count per thread,
- reduce epilogue complexity,
- remove spills before chasing other ideas.

---

## 5. Synchronization / barrier issue

Typical symptom:

- barrier stall metrics are large,
- pipeline depth is not paying off,
- CTA-level coordination interrupts math frequently.

Possible causes:

- too many stages,
- too-frequent block-wide sync,
- dataflow not aligned with warp responsibilities,
- generic path mixing hot and cold work.

Candidate directions:

- reduce sync frequency,
- use warp-specialized roles,
- simplify stage transitions,
- separate cleanup path from steady-state path.

---

## 6. Tail-handling overhead from generic code

Typical symptom:

- profile looks “okay” but total runtime is still disappointing,
- edge predicates or cleanup loops show up materially,
- shape is fixed and awkward relative to common tile sizes.

Possible causes:

- generic bounds checks inside the hot loop,
- generic launch grid,
- generic epilogue for arbitrary sizes,
- multiple code paths in the steady-state inner loop.

Candidate directions:

- specialize for the fixed `(m, n, k)`,
- peel edge tiles away from the hot path,
- split main kernel vs cleanup kernel,
- hardcode loop trip counts where safe.

## Symptom -> action map

| Symptom | Likely class | First directions to try |
|---|---|---|
| low tensor activity, low DRAM | compute scheduling / occupancy | tile retune, register-pressure reduction, deeper steady-state pipeline |
| high DRAM, low tensor activity | global-memory bound | vectorized loads, better staging, larger reuse tile |
| high shared stalls / bank conflict hints | shared-memory bottleneck | swizzle/padding, layout rewrite, reduce shared round-trips |
| high barrier stalls | synchronization issue | fewer stages, warp specialization, hot/cold path split |
| low active warps, spills, weak latency hiding | occupancy issue | smaller tile, less unroll, fewer live fragments |
| decent metrics but still weak absolute time | generic overhead | shape-specialization, edge peeling, launch retune |

## Optimization families to search over

## A. CTA / warp / MMA tile shape

Questions:

- is the CTA tile too large for a mobile 3070 register budget?
- is the warp tile aligned with the target shape?
- does the tile choice create too much tail waste?

Look for:

- tensor activity,
- active warps,
- register pressure,
- tail tile count.

---

## B. Copy pipeline depth

Questions:

- are loads arriving late?
- are there enough stages to hide latency?
- did extra stages create more barriers and shared pressure than they solved?

Look for:

- scoreboard stalls,
- barrier stalls,
- memory-vs-compute overlap.

---

## C. Global load/store vectorization

Questions:

- are global accesses aligned?
- are transactions efficiently packed?
- can each lane move more useful bytes per instruction?

Look for:

- global load efficiency,
- memory throughput,
- instruction count.

---

## D. Shared-memory layout

Questions:

- do fragment loads map cleanly to shared banks?
- is swizzle or padding needed?
- are `A` and `B` staged in the most tensor-core-friendly layout?

Look for:

- shared stalls,
- replay/bank-conflict signs,
- tensor starvation with moderate DRAM.

---

## E. Register pressure management

Questions:

- are accumulators or temporaries too large?
- is the compiler spilling?
- is occupancy collapsing because the kernel tries to hold too much state?

Look for:

- launch occupancy limits,
- local memory traffic,
- active warps.

---

## F. Shape-specialized cleanup strategy

Questions:

- can the main path assume exact trip counts?
- can edge predicates be moved out of the hot loop?
- should the benchmark shape use a dedicated kernel entry point?

Look for:

- branch overhead,
- scalar cleanup work,
- instruction mix in the steady-state loop.

## What the diagnosis agent must output

The diagnosis node should always output exactly **three** directions and use this structure:

### Direction template

- **Name**
- **Family ID**
- **Subfamily ID**
- **Mode**: `exploit`, `explore`, or `restore`
- **Hypothesis**
- **Why now**
- **Expected upside**
- **Implementation surface**
- **Main risk**
- **Action fingerprint**
- **Search score v1**
- **Score breakdown**
- **Predicted gain (ms)**
- **Predicted fail risk**
- **Ranking notes**
- **Metrics to re-check**
- **Stop condition**

Each direction is also a structured search candidate.

That means:

- keep a numeric score for deterministic fallback ordering
- keep `score_breakdown` and `ranking_notes` so later LLM or fuzzy rerank logic can reinterpret close decisions without relying on fake precision
- prefer coarse, auditable numbers over overfit decimal detail

## What the implementation loop must record

After trying one direction, record:

- compile status,
- correctness status,
- runtime delta,
- TFLOP/s delta,
- what changed in code,
- whether the hypothesis was supported or falsified.

## Anti-patterns

Do not recommend these unless the current profile clearly demands them:

- broad kernel fusion unrelated to the benchmark,
- host-side preprocessing that changes the benchmark definition,
- changing the dataset to make the kernel look better,
- mixing many optimization ideas into one unexplained commit,
- comparing against CUTLASS on a different shape or different correctness target.

## Plateau policy

If three consecutive direction attempts do not improve the best runtime:

1. refresh the CUTLASS baseline artifacts,
2. compare the current custom kernel profile against CUTLASS,
3. ask whether the gap is mainly:
   - compute-pipe efficiency,
   - memory movement,
   - occupancy,
   - or generic-control overhead.

Then generate the next three directions again.
