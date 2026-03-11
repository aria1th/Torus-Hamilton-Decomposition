Task ID:
D5-WU2-SECONDARY-EXACT-TWIST-015

Question:
Can the exact bit
`pred_sig1_phase_align`
act as a **secondary** layer-3 controller inside the already-validated `wu2` twist gadget — rather than replacing it — and thereby produce a clean strict mixed witness with improved cycle compression on `m=5,7,9`?

Purpose:
`014` proves two things exactly:
1. the exact predecessor-tail refinement is not the right next main branch for layer-2-only search;
2. the exact bit fails when used alone as a layer-3 controller.
The next smallest honest move is therefore to keep the successful `wu2` twist mechanism alive and ask whether the exact bit can refine that mechanism inside the cells where it already naturally appears.

Inputs / Search space:
- Fixed anchors:
  - layer `0` anchor `1`
  - layer `1` anchor `4`
  - layer `4+` anchor `0`

- Fixed strong cycle-capable layer-2 base:
  - primary base: `w+u=2 : 2/4`
  - control base: `w+u=2 : 4/2`

- Validated layer-3 predecessor controller:
  \[
  r \in \{\texttt{pred\_sig1\_wu2},\ \texttt{pred\_sig4\_wu2}\}
  \]

- Exact secondary bit:
  \[
  p = \texttt{pred\_sig1\_phase\_align}
  \]
  extracted from the exact predecessor-tail local signature

- Layer-3 controller state:
  \[
  c_3=(r,p)\in\{0,1\}^2
  \]

- Layer-3 old bit:
  - Stage 1: `q+u=-1`
  - Stage 2 only if needed:
    \[
    \{q+u=1,\ q+u=-1,\ u=-1\}
    \]

- Layer-3 slice palette:
  \[
  \{0/3,\ 3/0,\ 3/3\}
  \]

- Stage 1 rule family:
  - assign one slice mode to each of the four controller states `c_3`
  - total raw tables per `(base,r,oldbit)`:
    \[
    3^4 = 81
    \]
  - with `2` bases, `2` controllers, `1` old bit:
    \[
    2 \cdot 2 \cdot 81 = 324
    \]
    exact rules

- Stage 2 widening only if needed:
  - widen layer-3 old bit to
    \[
    \{q+u=1,\ q+u=-1,\ u=-1\}
    \]
  - total raw tables:
    \[
    2 \cdot 2 \cdot 3 \cdot 81 = 972
    \]

- Optional Stage 3 only if needed:
  - keep the best Stage 1/2 controller table
  - allow one designated synchronized layer-2 flip
    \[
    2/4 \leftrightarrow 4/2
    \]
    on one chosen controller class `c_3`
  - do not open a general layer-2 table search at this stage

- Pilot moduli:
  - `m in {5,7,9}`

- Optional stability spot-checks:
  - `m in {11,13}` for best survivors

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- exact `U_0` cycle and monodromy analysis
- classify survivors by effective dependence:
  - `p`-trivial inside each `r`-slice
  - genuinely `p`-dependent inside an active `wu2` slice
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
4. Show that at least one clean survivor is genuinely `p`-dependent inside an active `wu2` controller slice.
5. Save the explicit 4-state layer-3 controller table and full validation summary.

Failure criteria:
- every clean survivor is still `p`-trivial inside each `r`-slice, or
- every clean strict mixed survivor stays on the old baseline `21`, or
- every genuinely `p`-dependent controller destroys clean-frame or strict-clock, or
- the optional single synchronized layer-2 flip still yields no improvement

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- survivor-count tables by base, controller choice, old bit, and 4-state layer-3 table
- validation outputs
- proof-supporting computations

Return format:
- exact bases tested
- exact layer-3 controllers tested
- survivor counts by controller table
- whether any clean survivor is genuinely `p`-dependent inside a `wu2` slice
- best mixed witness found
- comparison with:
  - the `008` mixed baseline
  - the `014` double negative
  - the earlier strongest cycle-only witness
- strongest supported conclusion
- recommended next widening only if the `wu2 + exact-bit` branch still fails

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON summaries for all tested controller tables
- exact validation script for every reported survivor
- explicit comparison against the current mixed baseline and earlier cycle-only baseline
