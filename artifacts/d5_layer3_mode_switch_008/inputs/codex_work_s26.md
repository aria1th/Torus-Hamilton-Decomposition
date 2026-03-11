Task ID:
D5-LAYER3-MODE-SWITCH-008

Question:
Can one extra layer-3 local flag switch the exact `007` decoupled trichotomy into a genuine mixed regime, producing a clean strict pilot witness with both moving `U_0` cycles and nonzero monodromy on `m=5,7,9`?

Purpose:
Test the smallest credible extension beyond `007`. The exact `007` data show that layer 3 already has the right anchor palette `{0,2}`, but one old bit alone is too coarse to mix the cycle-preserving and monodromy-producing submodes.

Inputs / Search space:
- fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`
- fix layer 2 to one bifurcation-capable cycle split from
  \[
  T=\{q=-1,\ q+u=1,\ q+u=-1,\ u=-1\}
  \]
  with alternate `0` and orientation `0/2` or `2/0`
- first-stage representatives:
  - `s_2 = q=-1`
  - both layer-2 orientations as controls
- layer 3:
  - choose representative `s_3` from `T`, starting with `q=-1`
  - add one extra local flag `p`
  - initial candidate pool for `p`:
    - `pred_any_phase_align`
    - `pred_sig0_phase_align`
    - `pred_sig1_wu2`
    - `pred_sig4_wu2`
  - if all fail, replace `p` by an exact predecessor-tail local-signature bit
- layer-3 contexts:
  \[
  (s_3,p)\in\{0,1\}^2
  \]
- layer-3 allowed slice rules per `p`:
  - `0/3`, `3/0`, `2/3`, `3/2`
  - optional constant `3` as a control
- pilot moduli:
  - `m in {5,7,9}`

Allowed methods:
- exact exhaustive enumeration over the small layer-3 mode-switch family
- clean-frame filtering first
- then strict-clock validation
- then exact `U_0` cycle / monodromy analysis
- save all survivors and their full pilot signatures
- only if all simple predecessor flags fail, derive and test an exact predecessor-tail local-signature flag

Success criteria:
- find a clean strict witness on `m=5,7,9` with both
  - some cycle length `>1`
  - some nonzero monodromy
- preferably retain or improve the stronger cycle regime already seen in the best cycle-only witnesses
- save the explicit layer-3 rule table and full validation summary

Failure criteria:
- every clean survivor still falls into one of the old three regimes:
  - cycle-only
  - monodromy-only
  - trivial
- or every monodromy-bearing survivor destroys the moving-cycle regime

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by predecessor flag and layer-3 mode table
- validation outputs
- proof-supporting computations

Return format:
- fixed layer-2 base used
- predecessor flags tested
- survivor counts by layer-3 mode table
- best cycle+monodromy witness, if any
- best cycle-only witness
- best monodromy-only witness
- strongest supported conclusion
- recommended two-bit layer-3 follow-up if all one-flag families fail

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries per predecessor flag
- exact validation script for every reported survivor
