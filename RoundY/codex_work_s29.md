Task ID:
D5-LAYER2-GEOMETRY-UNDER-FIXED-TWIST-011

Question:
With the twist gadget fixed to one exact mixed representative, can a better-signed layer-2 local switch produce a clean strict mixed witness with improved cycle compression on the pilot range `m=5,7,9`?

Purpose:
The explanatory analysis of `008/009` shows that the current layer-3 gadget is a holonomy gadget in the fixed-seed graft family. The exact `010` computation shows that geometry can change once the predecessor state acts on layer `2`, but all observed changes are anti-compressive. The next minimal search should therefore freeze twist and optimize geometry directly on layer `2`.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`

- fixed canonical layer-3 twist gadget:
  - predecessor flag on layer `3`: `pred_sig1_wu2`
  - layer-3 old bit: `q+u=-1`
  - Stage 1 canonical ordered slice pair:
    - `p_3=0 -> 0/3`
    - `p_3=1 -> 3/0`
  - control twist for sign check:
    - `p_3=0 -> 3/0`
    - `p_3=1 -> 0/3`

- layer-2 local switch:
  - layer-2 predecessor/local flag candidate
    \[
    p_2 \in \{\texttt{pred\_sig1\_wu2},\ \texttt{pred\_sig4\_wu2}\}
    \]
  - ordered layer-2 slice pair
    \[
    (L2_0,L2_1)\in M_2\times M_2
    \]
    with
    \[
    M_2=
    \{
    q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2,\ 
    q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2
    \}.
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
- comparison against the current mixed baseline:
  - total pilot cycle count `21`
  - uniform nonzero monodromy
- staged widening only if needed:
  - Stage 1: the `8`-mode layer-2 pool above with one fixed twist gadget
  - Stage 2: restore the full layer-3 twist family only if Stage 1 finds geometry improvement
  - Stage 3: if Stage 1 fails, widen layer-2 local state rather than layer 3

Success criteria:
1. Find a clean strict mixed survivor on `m=5,7,9`.
2. Keep nonzero monodromy on every pilot modulus.
3. Improve cycle structure beyond the current mixed baseline:
   - total pilot `U_0` cycle count `< 21`, or
   - fewer than `m` cycles on at least one pilot modulus.
4. Stronger success:
   approach the earlier cycle-only compression baseline `15` while preserving nonzero monodromy.
5. Save the explicit layer-2 and layer-3 rule tables plus the full validation summary.

Failure criteria:
- every clean strict mixed survivor still has total pilot cycle count `>= 21`, or
- every geometry-changing rule is anti-compressive or monodromy-destroying, or
- no clean strict mixed survivors remain under the fixed canonical twist.

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by layer-2 local flag and layer-2 slice pair
- validation outputs
- proof-supporting computations

Return format:
- exact canonical twist gadget used
- exact layer-2 local flags tested
- exact layer-2 slice pairs tested
- survivor counts by layer-2 flag and slice pair
- best mixed witness found
- comparison with:
  - the `008/009/010` mixed baseline
  - the earlier strongest cycle-only witness
- strongest supported conclusion
- recommended widening if no geometry improvement is found

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per layer-2 local flag
- exact validation script for every reported survivor
- explicit comparison against the current mixed baseline and the earlier cycle-only baseline
