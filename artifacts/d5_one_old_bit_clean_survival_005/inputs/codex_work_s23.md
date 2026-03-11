Task ID:
D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005

Question:
Can adding one existing nonredundant old quotient bit `s` to the active layer-2/3 grammar produce any context-dependent clean survivor on the pilot range `m=5,7,9` within strict-friendly two-anchor palettes?

Purpose:
Determine the smallest local augmentation that survives the clean-frame barrier, since the exact context-only family based on `(\text{phase_align},b_1,b_2)` has already been exhausted.

Inputs / Search space:
- base fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- layer `2` seed anchor `2`
- layer `3` seed anchor `3`
- exact pilot bits:
  - `phase_align`
  - `b1`
  - `b2`
- one extra old quotient bit `s`
  - test each nonredundant candidate separately
- strict-friendly alternates:
  - layer `2` alternate `a in {0,2,3,4}`
  - layer `3` alternate `b in {0,2,3,4}`
- contexts:
  - aligned branch split by `s` if `s` varies there
  - nonzero branch split by `(ctx,s)` where `ctx = 2*b1 + b2`
  - total context count expected: `8` to `10`, depending on the aligned branch treatment
- pilot moduli:
  - `m in {5,7,9}`

Allowed methods:
- exact exhaustive enumeration
- quotient-based color-0 Latin prefilter
- clean-frame / strict-clock / `U_0` evaluation on the pilot range
- staged search:
  - first one-layer-active families `(a,3)` and `(2,b)`
  - then full two-layer families `(a,b)`
- deduplication by actual anchor tables
- validation of all surviving unique rules on the full torus and all five colors

Success criteria:
1. Find at least one context-dependent clean survivor on `m=5,7,9`.
2. Preferably keep `strict_clock=True`.
3. Ideally find a witness with nontrivial `U_0`:
   - fewer than `m^2` cycles, or
   - some cycle length `>1`, or
   - some nonzero monodromy.
4. Save the best rule and the complete survivor counts by bit choice and anchor family.

Failure criteria:
- every clean survivor is still context-independent, or
- context-dependent clean survivors exist but every strict survivor remains `U_0`-trivial.

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by old-bit choice and anchor family
- validation outputs
- proof-supporting computations

Return format:
- list of old-bit candidates tested
- survivor counts for each old-bit / anchor-family combination
- first context-dependent clean survivor, if any
- best strict survivor, if any
- any nontrivial-`U_0` witness
- strongest supported conclusion
- recommended follow-up if all one-old-bit families fail

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per old-bit / anchor-family combination
- exact validation script for every reported unique survivor
