Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
After `015`, do **not** reopen larger one-bit exact refinements of the current fixed-base `wu2` gadget. The exact bit
[
p=\texttt{pred_sig1_phase_align}
]
is now ruled out in every one-layer role tested:

* not as layer-2-only exact refinement (`014A`),
* not as layer-3 standalone controller (`014B`),
* not as one-bit secondary refinement inside the live `wu2` twist gadget (`015`).

The smallest still-live branch is now a **minimally synchronized two-layer family**: keep the validated `wu2` controller alive, but let the same controller state `(r,p)` act on both layers at once, with only a tiny p-dependent layer-2 flip on the active `wu2` slice.

Known assumptions:

* I unpacked and read the `015` bundle:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Bundle-backed `015` counts:

  * Stage 1 (`324` rules):

    * clean strict survivors: `36`
    * mixed: `24`
    * cycle-only: `12`
    * monodromy-only: `0`
    * improved mixed: `0`
  * Stage 2 (`972` rules):

    * clean strict survivors: `108`
    * mixed: `72`
    * cycle-only: `36`
    * monodromy-only: `0`
    * improved mixed: `0`
* Bundle-backed dependency classes:

  * Stage 1:

    * `constant`: `12`
    * `p_trivial_within_r`: `24`
  * Stage 2:

    * `constant`: `36`
    * `p_trivial_within_r`: `72`
* So in `015` there are:

  * `0` clean survivors with genuine `p`-dependence inside an active `wu2` slice,
  * `0` clean survivors with any new pilot regime,
  * and every clean survivor stays on total pilot cycle count `21`.
* Validation is clean:

  * all validated candidates match the search summary,
  * all clean candidates are full-color Latin on `m=5,7,9`,
  * all clean candidates remain strict,
  * checked survivors stay on the same cycle signature under control-twist reversal.
* From `014`, also already established:

  * the exact predecessor-tail local signature contributes exactly one new bit beyond the named partition:
    [
    p=\texttt{pred_sig1_phase_align},
    ]
  * that bit is locally real: inside its split cells it changes 3-step low-layer words and increments,
  * but as a layer-2-only refinement it was pilot-return sterile,
  * and as a standalone layer-3 controller it collapsed to p-trivial clean survivors.
* Structural consequence of `014+015`:
  the exact bit is **not fake**, but it is dynamically sterile in every one-layer role tested so far.

Attempt A:
Idea:
Promote `015` from “another negative” to a pruning theorem for one-bit exact refinements around the current `wu2` mechanism.

What works:

* This is now a three-part exact pruning chain:

  1. `014A`: exact bit fails as layer-2-only refinement,
  2. `014B`: exact bit fails as standalone layer-3 controller,
  3. `015`: exact bit fails even as a one-bit secondary refinement inside the live `wu2` twist gadget.
* The failure is not because admissibility kills the branch immediately:
  `015` still has many clean strict survivors.
* The failure is also not because the bit disappears combinatorially:
  the search sees it, but every clean survivor collapses to being p-trivial inside each `wu2` branch.
* So a larger layer-2-only exhaustive search on this same one exact bit is no longer a credible main branch.

Where it fails:

* It does **not** yet prove the exact bit is useless in every possible role.
* One role remains genuinely untested:
  the exact bit acting **synchronously** on geometry and twist together.

Attempt B:
Idea:
Use the exact bit only in a minimally synchronized two-layer family: the same controller state `(r,p)` controls layer-3 mode and also flips layer-2 orientation on the active `wu2` slice.

What works:

* This is the smallest remaining use of the exact bit that matches the project-wide coupled-mechanism hypothesis.
* It directly addresses the lesson from `005`–`015`:
  progress has come from coupling orbit structure and twist, not from merely increasing one-layer state count.
* It also uses the exact new information efficiently:
  `p` is already known to split cells that intersect the active `wu2` region.
* This is smaller and better motivated than jumping immediately to a larger exact local-signature state.

Where it fails:

* We do not yet know whether any clean survivor with genuine p-dependence survives once the layer-2 flip is allowed.
* If this synchronized family still collapses to p-trivial or baseline-only behavior, then the exact-bit route is close to fully exhausted, and the next honest move will be a second exact local bit or a larger exact local-signature controller.

Candidate lemmas:

* [C] In `015`, every clean survivor is either `constant` or `p_trivial_within_r`; no clean survivor shows genuine `p`-dependence inside an active `wu2` slice.
* [C] In `015`, every clean strict mixed survivor remains on the old baseline total pilot cycle count `21`.
* [C] Combining `014` and `015`, the exact bit `pred_sig1_phase_align` is locally real but dynamically sterile in all one-layer roles tested.
* [H] The only still-plausible role for this exact bit is a synchronized two-layer role where it acts on geometry and twist together.
* [H] The next smallest live branch is therefore a minimally synchronized `(r,p)` family, not another broad layer-2-only exact-signature search.
* [F] One-bit exact refinement of the present fixed-base `wu2` gadget is still the main breakout route.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Keep canonical anchors fixed:

  * layer `0 -> 1`
  * layer `1 -> 4`
  * layer `4+ -> 0`
* Keep the exact bit
  [
  p=\texttt{pred_sig1_phase_align}
  ]
  and the live `wu2` controller
  [
  r\in{\texttt{pred_sig1_wu2},\texttt{pred_sig4_wu2}}.
  ]
* Keep one strong cycle-capable layer-2 base fixed:

  * primary: `w+u=2 : 2/4`
  * control: `w+u=2 : 4/2`
* Let layer-3 depend on the 4-state controller
  [
  (r,p)\in{0,1}^2
  ]
  with slice palette
  [
  {0/3,\ 3/0,\ 3/3}.
  ]
* New ingredient:
  inside the active `wu2` slice `r=1`, allow a **p-dependent synchronized layer-2 flip**
  [
  2/4 \leftrightarrow 4/2
  ]
  while keeping the inactive `r=0` slice at the base orientation.
* Start with old bit `q+u=-1`; widen only if needed to
  [
  {q+u=1,\ q+u=-1,\ u=-1}.
  ]
* Primary targets:

  * clean-frame on `m=5,7,9`
  * strict-clock on `m=5,7,9`
  * nonzero monodromy on every pilot modulus
  * improved cycle structure:
    [
    \text{total pilot cycle count} < 21
    ]
    or fewer than `m` cycles on at least one pilot modulus
* Secondary target:
  find at least one clean survivor with genuine p-dependence.

Next branching options:

1. Main branch:
   minimally synchronized two-layer `(r,p)` family.
2. If that fails:
   treat the present exact bit as effectively exhausted in the current local neighborhood.
3. Then next:
   enlarge the exact local information itself, by introducing a second exact local bit or a larger exact predecessor-tail signature state rather than continuing one-bit refinements.

Claim status labels:
[P] `015` gives a clean negative for the exact bit as a one-bit secondary refinement inside the live `wu2` gadget
[C] every clean survivor in `015` is constant or `p_trivial_within_r`
[C] no `015` clean survivor improves the mixed baseline `21`
[H] the next smallest live branch is synchronized two-layer use of `(r,p)`
[F] one-bit exact refinement inside the current fixed-base `wu2` gadget is still the main breakout route
[O] full Hamilton decomposition remains open

Work Template:
Task ID:
D5-SYNCHRONIZED-WU2-EXACT-016

```
Question:
Can the exact bit
\[
p=\texttt{pred\_sig1\_phase\_align}
\]
survive only in a **synchronized two-layer role**, where the same controller state `(r,p)` both chooses the layer-3 twist mode and flips the layer-2 orientation on the active `wu2` slice, thereby producing a clean strict mixed witness with improved cycle compression on `m=5,7,9`?

Purpose:
`015` proves that the exact bit fails as a one-bit secondary controller inside the live `wu2` gadget when the layer-2 base is fixed. The smallest honest remaining test is therefore to let the exact bit act on geometry and twist together, but only in the weakest possible synchronized way.

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
  - Stage 2 only if needed:
    \[
    \{q+u=1,\ q+u=-1,\ u=-1\}
    \]

- Layer-3 slice palette:
  \[
  \{0/3,\ 3/0,\ 3/3\}
  \]

- 4-state controller:
  \[
  c=(r,p)\in\{0,1\}^2
  \]

- Layer-3 rule:
  - assign one slice mode in `{0/3,3/0,3/3}` to each of the 4 controller states
  - total tables per `(base,r,oldbit)`:
    \[
    3^4 = 81
    \]

- New synchronized layer-2 rule:
  - keep the inactive `r=0` slice fixed at the chosen base orientation
  - on the active `r=1` slice, allow only genuine `p`-dependent orientation patterns:
    1. `p=0 -> base`, `p=1 -> flip(base)`
    2. `p=0 -> flip(base)`, `p=1 -> base`
  - no general layer-2 table search

- Stage 1 raw rule count:
  - `2` bases
  - `2` controller flags `r`
  - `1` old bit
  - `2` synchronized layer-2 flip patterns
  - `81` layer-3 tables
  - total:
    \[
    2\cdot 2\cdot 1\cdot 2\cdot 81 = 648
    \]

- Stage 2 widening only if needed:
  - widen old bit to
    \[
    \{q+u=1,\ q+u=-1,\ u=-1\}
    \]
  - total:
    \[
    2\cdot 2\cdot 3\cdot 2\cdot 81 = 1944
    \]

- Pilot moduli:
  - `m in {5,7,9}`

- Optional stability spot-checks:
  - `m in {11,13}` for the best survivors

Allowed methods:
- exact exhaustive enumeration
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- exact `U_0` cycle and monodromy analysis
- classify survivors by effective dependence:
  - constant
  - `r`-only
  - `p_trivial_within_r`
  - genuine synchronized `(r,p)` dependence
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
4. Show that at least one clean survivor has genuine synchronized `(r,p)` dependence.
5. Save the explicit synchronized layer-2 / layer-3 rule tables and full validation summary.

Failure criteria:
- every clean survivor still collapses to `r`-only or `p_trivial_within_r`, or
- every clean strict mixed survivor stays on the old baseline `21`, or
- every genuinely synchronized `(r,p)` rule destroys clean-frame or strict-clock

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
- whether any clean survivor has genuine synchronized `(r,p)` dependence
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
```

The practical conclusion is:

`015` kills the exact bit as a one-layer controller.
So the next honest move is the last small exact-bit test that is still structurally live: let that bit act on **geometry and twist together**, but only through a tiny synchronized two-layer family.
