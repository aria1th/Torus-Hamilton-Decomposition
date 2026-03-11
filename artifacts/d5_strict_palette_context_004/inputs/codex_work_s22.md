Task ID:
D5-STRICT-PALETTE-CONTEXT-004

Question:
Can a 5-context active layer-2/3 grammar depending only on
`phase_align, b1, b2`
produce nontrivial section dynamics if the alternate anchors are chosen from the strict-friendly set
`{0,2,3,4}` instead of `1`?

Purpose:
Determine whether the failure of Session 22 is specific to the seed/1 palette, or whether any context-only two-anchor family is inherently Latin-rigid / `U_0`-trivial.

Inputs / Search space:
- base layer anchors:
  - layer `0` = `1`
  - layer `1` = `4`
  - layer `4+` = `0`
- layer `2` seed anchor = `2`
- layer `3` seed anchor = `3`
- exact tail bits `b1, b2`
- active contexts:
  - `phase_align`
  - nonzero contexts `00, 01, 10, 11`
- alternate anchors:
  - `a` for layer `2`, chosen from `{0,2,3,4}`
  - `b` for layer `3`, chosen from `{0,2,3,4}`
- one 5-bit table for layer `2`
- one 5-bit table for layer `3`
- pilot moduli `m=5,7,9`

Allowed methods:
- exhaustive enumeration over all `(a,b)` and all 5-context bit tables
- first-stage Latin pruning
- second-stage clean-frame and strict-clock validation
- third-stage `U_0` cycle and monodromy analysis
- save best rules and complete survivor counts

Success criteria:
- find at least one context-dependent rule that is Latin and clean on `m=5,7,9`
- preferably keep `strict_clock=True`
- and ideally obtain nontrivial `U_0`:
  - fewer than `m^2` cycles, or
  - some cycle length `>1`, or
  - some nonzero monodromy

Failure criteria:
- every surviving rule is context-independent, or
- every strict survivor still has trivial `U_0`

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- tables of survivor counts by `(a,b)`
- proof-supporting computations

Return format:
- survivor counts for each `(a,b)`
- best Latin/clean rules
- best strict rules
- any nontrivial `U_0` witness
- strongest supported conclusion
- if all fail, recommended one-old-bit follow-up family

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per `(a,b)` family
- exact validation script for every reported survivor
