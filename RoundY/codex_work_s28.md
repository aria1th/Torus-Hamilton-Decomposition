Task ID:
D5-SHARED-PRED-INTERACTION-010

Question:
Can a shared predecessor-based mode switch on both layers `2` and `3` break the universal `m`-cycle collapse proved by `009`, producing a clean strict witness with both nonzero monodromy and improved cycle compression on the pilot range `m=5,7,9`?

Purpose:
`009` shows that the current fixed-seed twist graft is dynamically separable: orbit structure is frozen to
\[
U_0 = m \text{ cycles of length } m,
\]
while monodromy is only a layer-3 label. The next minimal untested family is one where layer `2` participates in the same local predecessor switch as layer `3`.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- shared predecessor flag:
  \[
  p \in \{\texttt{pred\_sig1\_wu2},\ \texttt{pred\_sig4\_wu2}\}
  \]
- Stage 1 layer-2 slice-mode pool:
  - `q=-1 : 2/4`
  - `q=-1 : 4/2`
  - `w+u=2 : 2/4`
  - `w+u=2 : 4/2`
  - choose an ordered pair
    \[
    (L2_0,L2_1)
    \]
    from this pool for the `p=0` and `p=1` slices
- Stage 2 widening, only if Stage 1 fails:
  - add the minimal representative non-alt-`4` layer-2 modes
    - `q=-1 : 0/2`
    - `q=-1 : 2/0`
    - `q=-1 : 2/3`
    - `q=-1 : 3/2`
- layer 3:
  - layer-3 old bit from
    \[
    \{q+u=1,\ q+u=-1,\ u=-1\}
    \]
  - predecessor flag = the same shared `p`
  - ordered layer-3 slice pair
    \[
    (L3_0,L3_1)
    \]
    any ordered distinct pair from
    \[
    \{0/3,\ 3/0,\ 3/3\}
    \]
- pilot moduli:
  - `m in {5,7,9}`
- optional stability spot-checks for best survivors:
  - `m in {11,13}`

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- exact `U_0` cycle and monodromy analysis
- comparison against:
  - the mixed baseline from `008/009`:
    total pilot cycle count `21`
  - the strongest earlier cycle-only baseline:
    total pilot cycle count `15`

Success criteria:
1. Find a clean strict survivor on `m=5,7,9`.
2. Keep nonzero monodromy on every pilot modulus.
3. Improve cycle structure beyond the `008/009` mixed baseline:
   - total pilot `U_0` cycle count `< 21`, or
   - fewer than `m` cycles on at least one pilot modulus.
4. Stronger success:
   preserve substantial cycle compression while keeping twist, ideally approaching the earlier cycle-only total `15`.
5. Save the explicit rule tables and full validation summaries.

Failure criteria:
- every clean strict survivor still has universal orbit structure
  \[
  U_0 = m \text{ cycles of length } m
  \]
  on `m=5,7,9`, or
- every monodromy-bearing survivor loses cycle compression completely, or
- no clean strict survivors remain once layer 2 joins the predecessor switch.

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by shared predecessor flag, layer-2 slice pair, and layer-3 gadget
- validation outputs
- proof-supporting computations

Return format:
- exact shared predecessor flags tested
- exact layer-2 slice pairs tested
- exact layer-3 gadgets tested
- survivor counts by layer-2 slice pair and layer-3 gadget
- best mixed witness found
- comparison with:
  - the `008/009` mixed baseline
  - the strongest earlier cycle-only witness
- strongest supported conclusion
- recommended Stage-2 widening if the strong alt-`4` shared-switch family still collapses

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per shared predecessor flag and layer-2 slice pair
- exact validation script for every reported survivor
- explicit comparison against the `008/009` mixed baseline and the earlier cycle-only baseline
