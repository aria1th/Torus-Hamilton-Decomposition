Task ID:
D5-ALT4-TWO-FLAG-GEOMETRY-012

Question:
With the twist gadget fixed to the exact mixed representative, can a four-state layer-2 predecessor partition using the pair
`(\texttt{pred_sig1_wu2}, \texttt{pred_sig4_wu2})`
repair the sign of the alt-`4` geometry mechanism and produce a clean strict mixed witness with improved cycle compression on `m=5,7,9`?

Purpose:
`011` proves that fixed twist plus a one-flag layer-2 switch does not improve the mixed baseline, and that twist sign is geometrically irrelevant there. It also shows that every non-baseline geometry profile lives entirely inside the alt-`4` layer-2 pool. So the smallest live next family is to keep twist frozen and refine only the layer-2 predecessor state within that alt-`4` pool.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`

- fixed canonical layer-3 twist gadget:
  - layer-3 flag: `pred_sig1_wu2`
  - layer-3 old bit: `q+u=-1`
  - slice pair:
    - `p3=0 -> 0/3`
    - `p3=1 -> 3/0`

- control twist for best-survivor checks only:
  - `p3=0 -> 3/0`
  - `p3=1 -> 0/3`

- layer-2 local state:
  \[
  c_2=(\texttt{pred\_sig1\_wu2},\ \texttt{pred\_sig4\_wu2})\in\{00,01,10,11\}
  \]

- Stage 1 layer-2 mode pool:
  \[
  A_4=
  \{
  q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2
  \}
  \]

- Stage 1 rule family:
  - choose one mode in `A_4` for each of the four `c_2`-states
  - total raw rules:
    \[
    4^4 = 256
    \]

- Stage 2 widening only if needed:
  - enlarge the layer-2 mode pool to
    \[
    A_4 \cup
    \{
    q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2
    \}
    \]
  - total raw rules:
    \[
    8^4 = 4096
    \]

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
- comparison against:
  - current mixed baseline total pilot cycle count `21`
  - earlier strongest cycle-only baseline total pilot cycle count `15`
- control-twist verification only on the best surviving rules

Success criteria:
1. Find a clean strict mixed survivor on `m=5,7,9`.
2. Keep nonzero monodromy on every pilot modulus.
3. Improve cycle structure beyond the current mixed baseline:
   - total pilot `U_0` cycle count `< 21`, or
   - fewer than `m` cycles on at least one pilot modulus.
4. Stronger success:
   move substantially toward the earlier cycle-only compression baseline `15` while preserving nonzero monodromy.
5. Save the explicit layer-2 four-state table and the full validation summary.

Failure criteria:
- every clean strict mixed survivor still has total pilot cycle count `>= 21`, or
- every geometry-changing rule in the four-state alt-`4` family is still anti-compressive or monodromy-destroying, or
- no clean strict mixed survivors remain under the four-state refinement

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by four-state layer-2 assignment
- validation outputs
- proof-supporting computations

Return format:
- exact canonical twist gadget used
- exact four-state layer-2 assignments tested
- survivor counts by assignment
- best mixed witness found
- comparison with:
  - the `008/009/010/011` mixed baseline
  - the earlier strongest cycle-only witness
- strongest supported conclusion
- recommended Stage 2 widening if the pure alt-`4` four-state family still fails

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries for all tested four-state assignments
- exact validation script for every reported survivor
- explicit comparison against the current mixed baseline and the earlier cycle-only baseline
