Task ID:
D5-SYNCHRONIZED-WU2-EXACT-016

Question:
Can the exact bit
\[
p=\texttt{pred\_sig1\_phase\_align}
\]
survive only in a synchronized two-layer role, where the same controller state `(r,p)` both chooses the layer-3 twist mode and flips the layer-2 orientation on the active `wu2` slice, thereby producing a clean strict mixed witness with improved cycle compression on `m=5,7,9`?

Purpose:
`014` and `015` rule out the exact bit in every one-layer role tested so far. The smallest honest remaining test is to let it act on geometry and twist together, but only through a tiny synchronized family.

Inputs / Search space:
- Fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- Exact bit:
  - `p = pred_sig1_phase_align`
- Live `wu2` controller:
  - `r = pred_sig1_wu2`
  - `r = pred_sig4_wu2`
- Layer-2 base orientations:
  - primary base: `const_2/4 = w+u=2 : 2/4`
  - control base: `const_4/2 = w+u=2 : 4/2`
- Layer-3 old bit:
  - Stage 1: `q+u=-1`
  - Stage 2 only if needed: `{q+u=1, q+u=-1, u=-1}`
- Layer-3 slice palette:
  - `{0/3, 3/0, 3/3}`
- Controller state:
  - `(r,p) in {0,1}^2`
- Layer-3 rule:
  - assign one slice mode in `{0/3,3/0,3/3}` to each controller state
  - total tables per `(base,r,oldbit)`: `3^4 = 81`
- Synchronized layer-2 rule:
  - inactive `r=0` slice fixed at the chosen base orientation
  - active `r=1` slice uses one of two genuine `p`-dependent patterns:
    - `p=0 -> base`, `p=1 -> flip(base)`
    - `p=0 -> flip(base)`, `p=1 -> base`

Exact search sizes:
- Stage 1:
  - `2 x 2 x 1 x 2 x 81 = 648`
- Stage 2:
  - `2 x 2 x 3 x 2 x 81 = 1944`

Pilot moduli:
- `m in {5,7,9}`

Optional stability spot-checks:
- `m in {11,13}` for the best survivors

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- exact `U_0` cycle and monodromy analysis
- classify survivors by:
  - combined synchronized rule
  - layer-3 dependence class
- compare against existing exact baselines:
  - mixed baseline `21`
  - anti-compressive classes `35,39,57,119,137`
  - monodromy-only `155`
  - earlier cycle-only compression baseline `15`
- control-twist verification only on the best surviving rules

Success criteria:
1. Find a clean strict mixed survivor on `m=5,7,9`.
2. Keep nonzero monodromy on every pilot modulus.
3. Produce a genuinely new positive mixed regime:
   - total pilot `U_0` cycle count `< 21`, or
   - fewer than `m` cycles on at least one pilot modulus.
4. Save explicit synchronized layer-2 / layer-3 rule tables and full validation summary.

Failure criteria:
- every clean strict mixed survivor stays on the old baseline `21`, or
- every synchronized rule that genuinely changes the geometry destroys clean-frame or strict-clock, or
- the synchronized family only produces anti-compressive or baseline regimes.

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by base, controller flag, old bit, synchronized flip pattern, and layer-3 table
- validation outputs
- proof-supporting computations

Return format:
- exact bases tested
- exact controller flags tested
- exact synchronized layer-2 flip patterns tested
- survivor counts by layer-3 table and flip pattern
- whether any clean survivor improves the mixed baseline
- best mixed witness found
- comparison with:
  - the `015` secondary-refinement negative
  - the `008` mixed baseline
  - the earlier strongest cycle-only witness
- strongest supported conclusion
- recommended next widening only if the synchronized `(r,p)` family still fails

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries for all tested synchronized rules
- exact validation script for every reported survivor
- explicit comparison against the current mixed baseline and earlier cycle-only baseline
