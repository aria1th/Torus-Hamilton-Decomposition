Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
After the `014` double negative, prune both
[
\text{layer-2-only exact-signature refinement}
]
and
[
\text{exact-bit-alone coupled mode-switch},
]
and move to the smallest still-live branch:
use the exact bit only as a **secondary refinement inside the validated `wu2` layer-3 twist gadget**, not as a standalone controller.

Known assumptions:

* I unpacked and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/sigma2_summary.json`
  * `data/sterility_diagnostic.json`
  * `data/stage_a_rule_rows.json`
  * `data/stage_b_rule_rows.json`
  * `data/validation_candidates.json`
  * `data/validation_summary.json`
* Exact signature outcome on both layers `2` and `3`:

  * exact signature classes: `12`
  * named coarse cells: `9`
  * the exact signature is generated exactly by:

    * the current named 4-bit partition
    * plus one new bit
* The unique new exact bit is:

  * `pred_sig1_phase_align`
  * “phase_align on the predecessor in color-relative direction `1`”
* The only named cells split by the exact bit are masks:

  * `1`
  * `5`
  * `9`
* These split cells differ only at exact-signature coordinates `2` and `6`.
* Importantly, two of the three split masks are already `wu2`-active cells:

  * mask `5 = pred_any_phase_align + pred_sig1_wu2`
  * mask `9 = pred_any_phase_align + pred_sig4_wu2`
* Stage A in `014`:

  * local diagnostic:
    the exact bit is locally real; inside split cells it can change the 3-step low-layer word and 3-step increment under fixed bases
  * exact layer-2 one-bit search:

    * total rules: `16`
    * clean strict survivors: `4`
    * mixed survivors: `4`
    * improved mixed survivors: `0`
    * new pilot regimes: `0`
  * the only clean survivors are the four constant tables:

    * `q=-1:2/4`
    * `q=-1:4/2`
    * `w+u=2:2/4`
    * `w+u=2:4/2`
  * each gives the old mixed baseline total pilot cycle count `21`
* Stage B in `014`:

  * the exact bit was used as the layer-3 controller
  * `stage_b1`:

    * rules: `18`
    * clean strict survivors: `6`
    * all `6` are `cycle_only`
    * improved mixed survivors: `0`
  * `stage_b2`:

    * rules: `36`
    * clean strict survivors: `12`
    * all `12` are `cycle_only`
    * improved mixed survivors: `0`
  * `stage_b3`:

    * rules: `54`
    * clean strict survivors: `0`
* Strongest exact Stage B fact:

  * every clean Stage B survivor has `mode_p0 = mode_p1`
  * so every clean survivor ignores the exact bit completely on layer `3`
  * the only surviving slice rules are constant choices:

    * `0/3`
    * `3/0`
    * `3/3`
* Validation:

  * total validated candidates: `34`
  * all `34/34` match search summary
  * all `34/34` are full-color Latin on `m=5,7,9`
  * all clean candidates remain strict
  * top `18` Stage B stability checks on `m=11,13` remain `cycle_only` with total cycle count `24`
  * top `18` control-twist checks keep the same cycle signature
* Scope note:

  * the counts above are bundle-backed
  * I also checked directly that the clean Stage B survivors are exactly the p-trivial constant-slice rules
  * I did not rerun the search scripts from scratch in this turn

Attempt A:
Idea:
Treat `014` as a clean pruning result for the old `014` plan and for the “exact bit as standalone coupled controller” variant.

What works:

* This is a genuine double negative, not just another inconclusive local failure.
* The exact predecessor-tail refinement on layer `2` is not fake:
  it adds one real bit and changes local low-layer words/increments in split cells.
* But at the pilot-return level, in the fixed-twist / pure-alt-4 branch, that exact bit is sterile:
  the only clean layer-2 rules are the old constant tables and they produce no new regime.
* On layer `3`, the exact bit is even more sharply negative as a standalone controller:
  every clean survivor ignores it, and the tiny synchronized layer-2 flip destroys clean survivors entirely.
* So two branches should now be pruned:

  1. broad layer-2-only exact-signature search,
  2. one-bit coupled mode-switch built from `pred_sig1_phase_align` alone.

Where it fails:

* It does **not** say the exact bit is useless in every role.
* It only says:

  * the bit is not the missing bulk/carry controller by itself,
  * and it is not a viable standalone twist controller by itself.

Attempt B:
Idea:
Use the exact bit only as a **secondary refinement inside the already-live `wu2` twist gadget**.

What works:

* The split masks `5` and `9` are precisely the masks where the current successful twist machinery already lives:
  they combine phase-align information with `pred_sig1_wu2` or `pred_sig4_wu2`.
* So the strongest structural reading of `014` is not “the exact bit is dead,” but:
  **the exact bit is too weak when asked to act alone.**
* This suggests the next smallest live family:
  keep the validated `wu2` layer-3 controller active, and let the exact bit refine it.
* That is much smaller and more plausible than reopening a large layer-2-only exact-signature table search.
* It also matches the project-wide pattern:
  the surviving progress has come from coupling geometry and twist, not from merely increasing state count on one layer.

Where it fails:

* We do not yet know whether the exact bit can survive clean/strict as a secondary controller inside the `wu2` gadget.
* It may still collapse to the old `wu2`-only mixed regime, or kill clean-frame as soon as it becomes genuinely active.
* So this is the next exact computation, not yet a theorem.

Candidate lemmas:

* [C] In `014`, the exact predecessor-tail signature on layers `2` and `3` is exactly the named 4-bit partition plus one new bit `pred_sig1_phase_align`.
* [C] The only split named cells are `1,5,9`; among them, `5` and `9` are already `wu2`-active cells.
* [C] In the fixed-twist / pure-alt-4 branch, the exact one-bit layer-2 search is pilot-return sterile: only the four old constant tables survive clean/strict, and they produce no new pilot regime.
* [C] In the first coupled use of the exact bit on layer `3`, every clean survivor collapses to `mode_p0 = mode_p1`; the exact bit is ignored.
* [F] Broad layer-2-only exact-signature exhaustive search is still the main branch.
* [F] `pred_sig1_phase_align` can serve as the missing controller by itself.
* [H] The next smallest live branch is a layer-3 controller of the form
  [
  (\texttt{pred_sig1_wu2},, \texttt{pred_sig1_phase_align})
  \quad\text{or}\quad
  (\texttt{pred_sig4_wu2},, \texttt{pred_sig1_phase_align}),
  ]
  over a fixed strong cycle-capable layer-2 base.
* [H] If that still fails, the first widening should be a tiny synchronized layer-2 flip on one such controller class, not another broad layer-2 table search.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Keep the canonical anchors fixed:

  * layer `0 -> 1`
  * layer `1 -> 4`
  * layer `4+ -> 0`
* Keep one strong cycle-capable layer-2 base fixed:

  * primary: `w+u=2 : 2/4`
  * control: `w+u=2 : 4/2`
* Keep the validated layer-3 twist palette:
  [
  {0/3,\ 3/0,\ 3/3}.
  ]
* Use the already-live layer-3 predecessor controller
  [
  r \in {\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2}}
  ]
  and refine it by the exact bit
  [
  p=\texttt{pred_sig1_phase_align}.
  ]
* Search a 4-state layer-3 table
  [
  (r,p)\in{0,1}^2 \mapsto {0/3,3/0,3/3}.
  ]
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
* Only if the pure layer-3 refinement fails:
  allow one designated synchronized layer-2 flip
  [
  2/4 \leftrightarrow 4/2
  ]
  on one chosen `(r,p)` class.

Next branching options:

1. Main branch:
   4-state layer-3 controller `(wu2\text{-flag}, exact\text{-bit})` over a fixed strong layer-2 base.
2. Secondary branch:
   if that yields only old regimes or p-trivial survivors, allow one tiny synchronized layer-2 flip on one controller class.
3. Side theorem branch:
   formalize the `014` double negative:

   * the exact bit is locally real but pilot sterile on layer `2`,
   * and it is not a standalone coupled controller on layer `3`.

Claim status labels:
[P] `014` gives a clean double negative for the old `014` main plan
[C] the exact signature contributes exactly one new bit, `pred_sig1_phase_align`
[C] that bit is pilot-sterile on layer-2-only search and collapses on layer-3-only coupled use
[H] the next smallest live branch is to use the exact bit only as a secondary refinement of the validated `wu2` twist gadget
[F] exact-bit-alone widening is the main breakout route
[O] full Hamilton decomposition remains open

The short synthesis is:

`014` is stronger than “still negative.”
It says:

* the exact bit is **real but pilot-sterile** on layer `2`, and
* the exact bit **cannot carry twist by itself** on layer `3`.

So the next honest move is not a larger layer-2 exact-signature search. It is to ask whether that exact bit can matter only as a **secondary refinement of the already-working `wu2` twist controller**.
