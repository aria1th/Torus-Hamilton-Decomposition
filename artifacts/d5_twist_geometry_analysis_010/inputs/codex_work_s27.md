Task ID:
D5-STRONG-CYCLE-MIX-009

Question:
Can the exact layer-3 twist gadget discovered in `008` be grafted onto the stronger previously validated layer-2 cycle seeds, producing a clean strict witness with both nonzero monodromy and better-than-`m` cycle structure on the pilot range `m=5,7,9`?

Purpose:
Move from the first mixed regime to a stronger mixed regime. The exact `008` search already found a robust local twist mechanism; the next step is to preserve that twist while importing the stronger cycle compression seen in the best layer-2 seeds from the earlier chain.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- layer-2 seed list:
  - `q=-1`: alternates `0,3,4`, both orientations
  - `q+u=1`: alternates `0,3`, both orientations
  - `q+u=-1`: alternates `0,3`, both orientations
  - `u=-1`: alternates `0,3`, both orientations
  - `w+u=2`: alternate `4`, both orientations
- total layer-2 seeds: `20`
- layer 3:
  - initial representative old bit: `q=-1`
  - predecessor flag
    - `pred_sig1_wu2`
    - `pred_sig4_wu2`
  - allowed ordered slice pairs `(M_0,M_1)`:
    any ordered distinct pair from
    `{0/3, 3/0, 3/3}`
  - total layer-3 gadget choices in Stage 1:
    `2 × 6 = 12`
- pilot moduli:
  - `m in {5,7,9}`
- optional stability spot-checks for the best survivors:
  - `m in {11,13}`

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- exact `U_0` cycle and monodromy analysis
- comparison against stored baselines from `007` and `008`
- staged widening:
  - Stage 1: representative layer-3 old bit `q=-1`
  - Stage 2 only if needed: widen layer-3 old bit to
    `{q=-1, q+u=1, q+u=-1, u=-1}`

Success criteria:
- find a clean strict mixed witness on `m=5,7,9`
- keep nonzero monodromy on every pilot modulus
- improve cycle structure beyond the current mixed baseline:
  - total pilot `U_0` cycle count `< 21`, or
  - fewer than `m` cycles for at least one pilot modulus
- strongest success:
  preserve or approach the best known cycle-only compression while keeping nonzero monodromy
- save the explicit rule table and validation summary

Failure criteria:
- every mixed survivor still has the baseline profile
  \[
  U_0 = m \text{ cycles of length } m
  \]
  with no cycle compression
- or all stronger layer-2 seeds lose monodromy under the twist gadget
- or no clean strict mixed survivor remains after the layer-2 transplant

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by layer-2 seed and layer-3 gadget
- validation outputs
- proof-supporting computations

Return format:
- exact layer-2 seeds tested
- exact layer-3 gadgets tested
- survivor counts by seed/gadget pair
- best mixed witness found
- comparison with:
  - the `008` representative mixed witness
  - the strongest earlier cycle-only witness
- strongest supported conclusion
- recommended Stage 2 widening if no cycle improvement is found

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per layer-2 seed
- exact validation script for every reported survivor
- explicit comparison against the `007` and `008` baseline witnesses
