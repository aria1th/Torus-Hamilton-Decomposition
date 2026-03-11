Task ID:
D5-ALT4-THREE-FLAG-GEOMETRY-013

Question:
With the twist gadget fixed to the exact mixed representative, can adding one extra named predecessor flag to the current two-flag layer-2 state produce a clean strict mixed witness with improved cycle compression on `m=5,7,9`?

Purpose:
`012` proves that the current two-flag pure alt-`4` family is fully admissible and genuinely geometry-active, but every new geometry class still has the wrong sign. It also shows that widening the layer-2 mode pool is not the answer. The next smallest live step is therefore to widen only the layer-2 local state.

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
  c_3=(\texttt{pred\_sig1\_wu2},\texttt{pred\_sig4\_wu2},p_{\mathrm{extra}})
  \in\{0,1\}^3
  \]

- extra named predecessor flag, tested separately:
  - `pred_any_phase_align`
  - `pred_sig0_phase_align`

- pure layer-2 mode pool:
  \[
  A_4=
  \{
  q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2
  \}
  \]

- Stage 1 rule family for each `p_extra`:
  - choose one mode in `A_4` for each of the eight `c_3` states
  - total raw rules per `p_extra`:
    \[
    4^8 = 65536
    \]
  - total raw rules across the two named flags:
    \[
    2\cdot 4^8 = 131072
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
- classification of effective layer-2 state dependence
  - constant / one-flag / xor / genuine multi-state / genuine eight-state
- comparison against the existing exact baselines:
  - mixed baseline `21`
  - anti-compressive classes `35,39,57,119,137`
  - monodromy-only class `155`
  - earlier cycle-only compression baseline `15`
- control-twist verification only on the best surviving rules

Success criteria:
1. Find a clean strict mixed survivor on `m=5,7,9`.
2. Keep nonzero monodromy on every pilot modulus.
3. Improve cycle structure beyond the current mixed baseline:
   - total pilot `U_0` cycle count `< 21`, or
   - fewer than `m` cycles on at least one pilot modulus.
4. Stronger success:
   move materially toward the earlier cycle-only compression baseline `15` while preserving nonzero monodromy.
5. Save the explicit eight-state layer-2 table and full validation summary.

Failure criteria:
- every clean strict mixed survivor still has total pilot cycle count `>= 21`, or
- every new geometry class remains anti-compressive, or
- neither extra named predecessor flag yields any improvement over the current `21` mixed baseline

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by extra predecessor flag and eight-state layer-2 assignment
- validation outputs
- proof-supporting computations

Return format:
- exact canonical twist gadget used
- exact extra predecessor flags tested
- survivor counts by eight-state layer-2 assignment
- best mixed witness found
- comparison with:
  - the `008/009/010/011/012` mixed baselines
  - the earlier strongest cycle-only witness
- strongest supported conclusion
- recommended exact predecessor-tail local-signature follow-up if both named three-flag families fail

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries for all tested eight-state assignments
- exact validation script for every reported survivor
- explicit comparison against the current mixed baseline and the earlier cycle-only baseline
