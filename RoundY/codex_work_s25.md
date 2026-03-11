Task ID:
D5-LAYER3-ALT2-DECOUPLED-007

Question:
Can a decoupled two-old-bit family combine the exact layer-2 cycle mechanism with nonzero monodromy once layer 3 is allowed to use alternate anchor `2` as well as `0`?

Purpose:
Test the smallest genuinely untried extension of `006`. The exact negative result of `006` only covers the layer-3 alt-`0` twist family, while validated `005` data indicate that moving-layer-2 monodromy can already occur with layer-3 tables `3/2` or `2/3`.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- old-bit pool:
  - `q=-1`
  - `q+u=1`
  - `w+u=2`
  - `q+u=-1`
  - `u=-1`
- choose ordered pair `(s2,s3)` from the old-bit pool
- layer `2`:
  - seed anchor `2`
  - alternate `a in {0,3,4}`
  - orientations `2/a` and `a/2`
  - depends only on `s2`
- layer `3`:
  - seed anchor `3`
  - alternate `b in {0,2}`
  - orientations `3/b` and `b/3`
  - depends only on `s3`
- exclude `phase_align`, `b1`, `b2` in this step
- pilot moduli:
  - `m in {5,7,9}`

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- exact clean-frame and strict-clock validation
- exact `U_0` cycle and monodromy analysis
- deduplicate by actual rule table and save all survivors

Success criteria:
1. Find a clean strict witness on `m=5,7,9` with both:
   - some cycle length `>1`
   - some nonzero monodromy
2. Preferably improve beyond the current cycle regime:
   - fewer than `m` cycles, or
   - longer cycles on some pilot modulus
3. Save complete survivor counts by ordered bit pair, layer-2 pattern, and layer-3 orientation.

Failure criteria:
- every strict survivor is still cycle-only, or
- every monodromy-bearing rule destroys the cycle mechanism, or
- no clean strict survivors remain after the layer-3 palette enrichment

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by ordered bit pair and orientation
- validation outputs
- proof-supporting computations

Return format:
- ordered bit pairs tested
- survivor counts by pair and layer-3 palette choice
- best cycle+monodromy witness, if any
- best cycle-only witness
- best monodromy-only witness
- strongest supported conclusion
- recommended layer-3-only predecessor-tail follow-up if `{0,2}` fails

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per ordered bit pair
- exact validation script for every reported survivor
