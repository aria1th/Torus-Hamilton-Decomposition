Task ID:
D5-TWO-OLD-BIT-CYCLE-MONODROMY-006

Question:
Can two independent old quotient bits, used asymmetrically on layers 2 and 3, combine the exact cycle mechanism and the exact monodromy mechanism into a single strict clean witness with both nontrivial `U_0` cycles and nonzero monodromy on the pilot range `m=5,7,9`?

Purpose:
Test the smallest extension beyond the successful one-old-bit family. The current evidence suggests that one old bit can create either orbit structure or twist, but not both at once.

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
  - prioritize `s2 != s3`
  - include `s2 = s3` as controls
- layer `2`:
  - seed anchor `2`
  - alternate anchor `a in {0,3,4}`
  - decision rule depends only on `s2`
  - allow both orientations: `2/a` and `a/2`
- layer `3`:
  - seed anchor `3`
  - alternate anchor `0`
  - decision rule depends only on `s3`
  - allow both orientations: `3/0` and `0/3`
- initial family intentionally excludes `phase_align`, `b1`, `b2`
  because all exact one-old-bit survivors ignored them
- pilot moduli:
  - `m in {5,7,9}`

Allowed methods:
- exact exhaustive enumeration over ordered bit pairs, anchor choices, and orientations
- direct full-color Latin / clean-frame / strict-clock validation
- exact `U_0` cycle and monodromy analysis
- save all survivors and complete counts
- if the minimal family fails, optionally extend one layer by one predecessor-tail flag

Success criteria:
1. Find a witness with `clean_frame=True` on `m=5,7,9`.
2. Keep `strict_clock=True` on `m=5,7,9`.
3. Achieve both:
   - some cycle length `>1`
   - some nonzero monodromy
4. Preferably improve beyond the current best cycle regime:
   - fewer than `m` cycles, or
   - longer-than-`m` cycles on some pilot modulus
5. Save the explicit rule tables and full validation summary.

Failure criteria:
- every survivor is still only cycle-only or only monodromy-only
- or the two-old-bit decoupled family has no clean strict survivors
- or same-bit cancellation persists for all ordered pairs

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by ordered bit pair and anchor orientation
- validation outputs
- proof-supporting computations

Return format:
- ordered bit pairs tested
- survivor counts by pair and orientation
- best cycle+monodromy witness, if any
- best cycle-only witness
- best monodromy-only witness
- strongest supported conclusion
- recommended follow-up if all two-old-bit families fail

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per ordered bit pair
- exact validation script for every reported survivor
