Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Absorb the slight but clean negative from `D5-ALT4-TWO-FLAG-GEOMETRY-012` and choose the smallest next family that is still genuinely live. The key issue is now sharper: with twist frozen, a two-flag four-state layer-2 refinement creates new geometry classes, but all of them still have the wrong sign.

Known assumptions:

* I unpacked and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
  * `inputs/codex_work_s30.md`
  * `inputs/note_s30.md`
* Exact searched family:

  * fixed anchors:

    * layer `0 -> 1`
    * layer `1 -> 4`
    * layer `4+ -> 0`
  * fixed canonical layer-3 twist gadget:

    * layer-3 flag `pred_sig1_wu2`
    * layer-3 old bit `q+u=-1`
    * slice pair
      [
      p_3=0\to 0/3,\qquad p_3=1\to 3/0
      ]
  * control twist checked only on top validated survivors:

    * sign-reversed slice pair
      [
      p_3=0\to 3/0,\qquad p_3=1\to 0/3
      ]
  * layer-2 local state:
    [
    c_2=(\texttt{pred_sig1_wu2},\texttt{pred_sig4_wu2})\in{00,01,10,11}
    ]
* Stage 1 pool:
  [
  A_4=
  {
  q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2
  }
  ]
  with one mode assigned to each of the four `c_2` states.
* Stage 2 widening added
  [
  {q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2}.
  ]
* Exact search sizes:

  * Stage 1 raw rules: `256`
  * Stage 2 raw rules: `4096`
* Exact bundle-backed outcomes:

  * Stage 1 clean strict survivors: `256`
  * Stage 1 profile split:

    * `248` mixed
    * `8` monodromy-only
    * `0` cycle-only
    * `0` improved mixed
  * Total unique clean strict pool after Stage 2: `640`
  * Direct stage split inside validated candidates:

    * `256` stage-1 survivors
    * `384` new stage-2 survivors
  * Total profile split after Stage 2:

    * `608` mixed
    * `16` cycle-only
    * `16` monodromy-only
    * `0` improved mixed
* Exact total pilot cycle-count regimes in the validated pool:

  * baseline mixed `21`
  * new mixed `35`
  * new mixed `39`
  * new mixed `57`
  * new mixed `119`
  * destructive mixed `137`
  * monodromy-only `155`
* Representative new regimes:

  * `35` regime:
    [
    (00,01,10,11)=(q{-}1:2/4,\ q{-}1:4/2,\ q{-}1:4/2,\ q{-}1:2/4)
    ]
    with pilot counts `(5,7,23)`
  * `57` regime:
    [
    (q{-}1:2/4,\ w{+}u=2:2/4,\ w{+}u=2:4/2,\ q{-}1:2/4)
    ]
    with pilot counts `(13,19,25)`
  * `119` regime:
    [
    (w{+}u=2:2/4,\ q{-}1:2/4,\ q{-}1:2/4,\ q{-}1:2/4)
    ]
    with pilot counts `(17,37,65)`
  * monodromy-only `155` regime:
    [
    (w{+}u=2:2/4,\ w{+}u=2:2/4,\ w{+}u=2:4/2,\ q{-}1:2/4)
    ]
    giving fixed points `(25,49,81)`
* Stronger exact fact from my direct pass over the validated layer-2 tables:

  * Stage 1 is **admissibility-saturated**: all `256/256` pure alt-`4` assignments survive clean frame and strict clock on `m=5,7,9`.
  * Stage 1 does not collapse to one-bit dependence:

    * `4` constant tables
    * `12` `pred_sig1_wu2`-only
    * `12` `pred_sig4_wu2`-only
    * `12` xor-only
    * `48` two-value genuinely four-state tables
    * `144` three-value genuinely four-state tables
    * `24` four-value genuinely four-state tables
  * So `216/256` stage-1 survivors are genuinely four-state tables not factoring through constant / `pred_sig1_wu2` / `pred_sig4_wu2` / xor.
  * Stage 2 likewise does not collapse:

    * among the `384` new stage-2 survivors, `368` are genuine multi-state tables.
* Additional exact structural point:

  * the four simple added `q=-1` modes only contribute baseline `21`, cancellation `21` cycle-only, or copies of the old anti-compressive classes;
  * they never create a positive mixed class.
* Control-twist scope:

  * top `20` validated survivors were checked under the sign-reversed twist;
  * all `20/20` kept the same cycle signature.
* Scope note:

  * the raw counts and regime distributions are bundle-backed;
  * the dependence-class counts and “genuinely four-state” classification are from my direct pass over `validation_summary.json`;
  * I did not rerun the search from scratch in this turn.

Attempt A:
Idea:
Treat `012` as an exact no-go for the current fixed-twist, two-flag layer-2 geometry family.

What works:

* The negative is clean.
* Stage 1 already explores the whole pure alt-`4` four-state family, and every one of those `256` rules is admissible.
* So there is no hidden Latin / clean-frame bottleneck left in that family.
* The refinement is genuinely live: it creates new geometry classes `35`, `57`, and `119` that were not present in `011`.
* But every new class is still anti-compressive.
* Stage 2 mode-pool widening confirms this diagnosis:
  it adds no improved mixed witness, only more baseline copies, old anti-compressive regimes, and a small `21`-cycle-only cancellation regime.

Where it fails:

* It does not say layer-2 geometry is exhausted.
* It only kills the specific family with

  * fixed twist,
  * two named `wu2` predecessor flags,
  * and no further layer-2 state refinement.

Attempt B:
Idea:
Read `012` as evidence that the missing knob is **state resolution on layer 2**, not more modes and not more twist freedom.

What works:

* The strongest positive hidden in the negative is:
  the pure alt-`4` four-state family is fully admissible and genuinely uses the four states.
* That means local-state refinement is not being projected away by the clean/strict constraints.
* The new regimes `35/57/119` show that widening layer-2 state really does move geometry.
* Stage 2 then shows that simply enlarging the layer-2 mode pool is the wrong direction: it does not repair the sign.
* So the next minimal live branch is to keep the pure alt-`4` pool and add one more layer-2 state bit.

Where it fails:

* We do not yet know which extra state bit is best.
* The current bundle does not compare the remaining named predecessor flags as additional layer-2 refiners.
* So the next step is still an exact search problem.

Candidate lemmas:

* [C] In `012`, the pure alt-`4` two-flag Stage-1 family is admissibility-saturated: all `256` rules are full-color Latin, clean-frame, and strict-clock on `m=5,7,9`.
* [C] The two-flag state is genuinely used in `012`: `216/256` Stage-1 survivors are genuinely four-state tables not factoring through constant / `pred_sig1_wu2` / `pred_sig4_wu2` / xor.
* [C] The two-flag refinement generates new exact mixed regimes with total pilot cycle counts `35`, `57`, and `119`, in addition to the old `21/39/137/155` landscape.
* [C] Every non-baseline regime in `012` is anti-compressive; there is no mixed survivor with total pilot cycle count `< 21`.
* [C] Stage-2 mode-pool widening adds no improved mixed regime; it only adds more baseline `21`, more anti-compressive copies, and a small `21` cycle-only cancellation class.
* [H] Therefore the missing resolution is in layer-2 local state, not in layer-2 mode-pool widening and not in further layer-3 twist variation.
* [H] The next smallest live branch is an eight-state layer-2 search obtained by adding one extra named predecessor flag to the current two-flag state, while keeping the pure alt-`4` pool and fixed twist.
* [F] Fixed twist plus the current two-flag layer-2 refinement can repair the sign of the alt-`4` geometry mechanism.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Freeze the canonical exact mixed twist gadget:

  * layer-3 flag `pred_sig1_wu2`
  * layer-3 old bit `q+u=-1`
  * slice pair
    [
    p_3=0\to 0/3,\qquad p_3=1\to 3/0
    ]
* Keep the layer-2 mode pool pure:
  [
  A_4=
  {
  q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2
  }.
  ]
* Widen only the layer-2 local state.
* Test one extra named predecessor flag at a time:
  [
  c_3=(\texttt{pred_sig1_wu2},\texttt{pred_sig4_wu2},p_{\mathrm{extra}})\in{0,1}^3
  ]
  with
  [
  p_{\mathrm{extra}}\in{\texttt{pred_any_phase_align},\ \texttt{pred_sig0_phase_align}}.
  ]
* For each choice of `p_extra`, search all assignments
  [
  c_3 \mapsto A_4,
  ]
  i.e. `4^8 = 65536` exact rules.
* Primary objective:
  find a clean strict mixed survivor on `m=5,7,9` with total pilot cycle count `< 21`.
* Stronger objective:
  approach the earlier cycle-only baseline `15` while keeping nonzero monodromy.
* Secondary diagnostics:

  * classify whether the best survivors genuinely use all `8` states or collapse to a smaller effective partition;
  * compare against current baselines `21`, `35`, `39`, `57`, `119`, `137`, `155`.
* If both named three-flag families fail:
  move to an exact predecessor-tail local-signature bit or small local-signature state on layer `2`, still with the same fixed twist and pure alt-`4` pool.

Next branching options:

1. Main branch:
   three-flag eight-state layer-2 geometry search with `p_extra` tested separately as `pred_any_phase_align` and `pred_sig0_phase_align`, under fixed twist and pure alt-`4` pool.
2. Secondary branch:
   if both named three-flag families fail, replace `p_extra` by an exact predecessor-tail local-signature bit on layer `2`.
3. Side theorem branch:
   formalize the `012` negative as an admissibility-saturated but anti-compressive two-flag geometry family.

Claim status labels:
[P] The pure alt-`4` two-flag refinement is genuinely live and admissibility-saturated.
[C] It creates new exact geometry classes `35/57/119`, but all are anti-compressive.
[C] Mode-pool widening on layer `2` adds no improved mixed regime.
[H] The next smallest live branch is further layer-2 state refinement, not more modes and not more twist.
[F] The current two-flag fixed-twist family can repair the sign.
[O] Full Hamilton decomposition remains open.

The short synthesis is:

The negative from `012` is not “state refinement failed.”
It is narrower: **two flags were enough to create new geometry classes, but not enough to fix the sign.**
Since the pure alt-`4` family is already fully admissible and mode widening did not help, the smallest honest next move is to widen **layer-2 local state** again, before going to heavier exact local-signature machinery.
