Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Reconcile the exact Codex result `D5-SHARED-PRED-INTERACTION-010` with the explanatory hypothesis in `D5-TWIST-GEOMETRY-ANALYSIS-010`, and choose the smallest next family that is still genuinely live.

Known assumptions:

* I unpacked and read both bundles:

  * `d5_shared_pred_interaction_010.tar.gz`
  * `d5_twist_geometry_analysis_010.tar.gz`
* The explanatory file is correct in its stated scope:

  * for Sessions `008/009`, the current layer-3 predecessor gadget behaves like a holonomy / twist gadget over a fixed base cycle geometry.
* But `010` shows that this must be scoped carefully:

  * once the predecessor switch is allowed to act on layer `2` as well, geometry is no longer frozen.
  * however, the geometry change observed in `010` is anti-compressive.
* Exact `010` search scope:

  * fixed anchors:

    * layer `0 -> 1`
    * layer `1 -> 4`
    * layer `4+ -> 0`
  * shared predecessor flag:

    * `pred_sig1_wu2`
    * `pred_sig4_wu2`
  * Stage 1 layer-2 slice pool:

    * `q=-1:2/4`
    * `q=-1:4/2`
    * `w+u=2:2/4`
    * `w+u=2:4/2`
  * Stage 2 added representative non-alt-`4` layer-2 slice modes:

    * `q=-1:0/2`
    * `q=-1:2/0`
    * `q=-1:2/3`
    * `q=-1:3/2`
  * layer-3 old bits:

    * `q+u=1`
    * `q+u=-1`
    * `u=-1`
  * layer-3 ordered off-diagonal slice pairs from
    [
    {0/3,\ 3/0,\ 3/3}.
    ]
* Exact `010` outcomes from the saved summaries:

  * Stage 1 raw rules searched: `576`
  * Stage 2 raw rules searched: `2304`
  * validated clean/strict candidate pool after deduplication: `864`
* Exact Stage 1 validated split:

  * `540` mixed
  * `36` monodromy-only
  * `0` cycle-only
  * total Stage 1 clean/strict survivors: `576`
* Exact Stage 1 cycle-count regimes:

  * `324` mixed with total pilot cycle count `21`
  * `180` mixed with total pilot cycle count `39`
  * `36` mixed with total pilot cycle count `137`
  * `36` monodromy-only with total pilot cycle count `155`
* Exact Stage 2 additions in the validated pool:

  * `240` mixed with total pilot cycle count `21`
  * `48` cycle-only with total pilot cycle count `21`
  * no new non-universal regimes
* So Stage 2 widening did not help; all new survivors stayed on the baseline `21`-cycle shape.
* Stronger exact fact from my direct pass over `validation_summary.json`:

  * in Stage 1, for fixed
    [
    (\text{layer-2 slice pair},\ \text{shared predecessor flag}),
    ]
    the pilot regime is independent of:

    * layer-3 old bit,
    * ordered layer-3 slice pair.
  * So in Stage 1, all geometry variation is controlled by layer `2` plus the shared flag, not by the layer-3 gadget.
* Even sharper Stage 1 classification:

  * `pred_sig1_wu2` is the geometry-destructive shared flag:
    it creates all `137` and all `155` cases.
  * `pred_sig4_wu2` never produces `137` or `155`; it only produces `21` or `39`.
* Representative non-universal mixed rule from `010`:

  * shared flag `pred_sig1_wu2`
  * layer 2:

    * `p=0 -> q=-1:2/4`
    * `p=1 -> q=-1:4/2`
  * layer 3:

    * old bit `q+u=1`
    * `p=0 -> 0/3`
    * `p=1 -> 3/0`
  * pilot cycle counts:

    * `m=5: 9`
    * `m=7: 13`
    * `m=9: 17`
  * total `39`
* Representative monodromy-only anti-compressive rule:

  * shared flag `pred_sig1_wu2`
  * layer 2:

    * `p=0 -> w+u=2:2/4`
    * `p=1 -> w+u=2:4/2`
  * layer 3:

    * any validated off-diagonal ordered pair
  * pilot return:

    * `m=5: 25` fixed points
    * `m=7: 49` fixed points
    * `m=9: 81` fixed points
* The explanatory `010` hypothesis bundle gives the right theorem-target for `008/009`:

  * in the fixed-seed twist-graft family, cycle geometry rigidifies to the universal `m`-cycle profile and the ordered layer-3 slice pair controls only holonomy.
* The correction forced by `010` is:

  * this is not a general theorem about predecessor gadgets,
  * only about the layer-3-only graft family.

Attempt A:
Idea:
Use the explanatory hypothesis exactly where it is supported, then correct its scope using the new Codex result.

What works:

* The twist-geometry analysis is a good reading of `008/009`.
* In that family:

  * mixed witnesses share one cycle signature,
  * the ordered layer-3 slice pair determines the monodromy law,
  * so “holonomy gadget over fixed base geometry” is the right language.
* This is genuinely useful because it isolates what `008/009` actually achieved.

Where it fails:

* If one overextends that diagnosis to all predecessor-based refinements, it becomes false.
* `010` shows that once the predecessor switch is admitted on layer `2`, the base geometry can change.
* So the explanatory hypothesis must be scoped to the fixed-seed layer-3 graft family.

Attempt B:
Idea:
Read `010` as a sign diagnosis for geometry, not as a failure of interaction.

What works:

* `010` is not another separability no-go.
* It proves genuine interaction exists:
  the shared predecessor switch can change the orbit partition.
* But the sign is wrong:
  every non-baseline change goes in the anti-compressive direction.
* Stage 1 already exhibits the full phenomenon:
  total pilot cycle counts `39`, `137`, and `155`.
* Stage 2 widening only adds more baseline-shape survivors and a small cycle-only cancellation regime.
* The exact direct classification is especially useful:
  in Stage 1, the pilot regime depends only on
  [
  (\text{layer-2 slice pair},\ \text{shared predecessor flag}),
  ]
  and not on layer-3 bit or ordered layer-3 slice pair.
* So the current family still has a sharp decomposition:

  * geometry is controlled by layer `2` plus predecessor state;
  * monodromy is still a layer-3 label.

Where it fails:

* It does not yet identify a positive-sign geometry switch.
* It only tells us very clearly where the next search must live:
  on the layer-2 side, with twist largely fixed.

Candidate lemmas:

* [C] In the fixed-seed twist-graft families `008/009`, all clean strict mixed survivors share the same pilot cycle profile
  [
  U_0 = m \text{ cycles of length } m,
  ]
  and the ordered layer-3 slice pair controls only the monodromy value.
* [C] In `010`, the shared predecessor switch breaks that universal-geometry law: Stage 1 produces non-universal clean strict regimes with total pilot cycle counts `39`, `137`, and `155`.
* [C] In Stage 1 of `010`, for fixed
  [
  (\text{layer-2 slice pair},\ \text{shared predecessor flag}),
  ]
  the pilot regime is independent of layer-3 old bit and independent of ordered layer-3 slice pair.
* [C] Therefore the geometry change seen in `010` is entirely layer-2-driven inside the searched family.
* [C] `pred_sig1_wu2` is the geometry-destructive shared flag in the Stage 1 pool: it produces all `137` and `155` regimes; `pred_sig4_wu2` does not.
* [H] The correct refined slogan is:

  * layer-3-only predecessor gadget = holonomy gadget;
  * shared predecessor action on layer 2 = geometry-active but currently anti-compressive.
* [H] The next minimal live branch is to fix a canonical twist gadget and search directly for a better-signed layer-2 geometry switch.
* [F] The predecessor gadget is holonomy-only in every currently relevant family.
* [F] More widening of the present layer-3 twist gadget is the primary route to better cycle compression.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Freeze a canonical exact mixed twist gadget from `008/010`, for example:

  * layer-3 predecessor flag `pred_sig1_wu2`
  * layer-3 old bit `q+u=-1`
  * ordered slice pair `(0/3, 3/0)` as the canonical `-2` twist
  * with `(3/0,0/3)` as the sign-reversed control.
* Search geometry on layer `2` directly.
* First candidate layer-2 local-state pool:

  * predecessor flag on layer `2`
    [
    p_2 \in {\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2}}
    ]
  * ordered `p_2`-slice pair chosen from the exact validated mode pool
    [
    M_2 =
    {
    q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2,\
    q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2
    }.
    ]
* Stage 1 exact search size with one fixed canonical twist:

  * `2` choices of layer-2 predecessor flag
  * `8 × 8 = 64` ordered layer-2 slice pairs
  * total `128` exact rules
* Stage 1 objective:
  find a clean strict mixed witness on `m=5,7,9` with

  * nonzero monodromy on every pilot modulus,
  * and total pilot cycle count `< 21`.
* Stage 2 only if Stage 1 gives any geometry improvement:
  re-open the full layer-3 monodromy law by restoring all six ordered off-diagonal pairs from
  [
  {0/3,\ 3/0,\ 3/3}
  ]
  and the three live layer-3 old bits
  [
  {q+u=1,\ q+u=-1,\ u=-1}.
  ]
* If Stage 1 fails completely, widen layer-2 local state, not layer 3:

  * either add the other named predecessor flags on layer `2`,
  * or use an exact predecessor-tail local-signature bit on layer `2`.

Next branching options:

1. Main branch:
   fix a canonical twist gadget and search for a better-signed layer-2 geometry switch.
2. Secondary branch:
   if no layer-2 predecessor flag works, replace the named layer-2 predecessor flag by an exact predecessor-tail local-signature bit.
3. Side theorem branch:
   formalize the two-step classification suggested by the data:

   * `008/009`: holonomy over fixed geometry;
   * `010`: geometry-active shared switch, but with geometry controlled entirely by layer-2 local data in the searched family.

Claim status labels:
[P] first mixed regime with nonzero monodromy was already exact in `008`
[C] the twist/holonomy explanation is correct for the fixed-seed graft family `008/009`
[C] `010` proves geometry can move once the predecessor switch acts on layer `2`
[C] in Stage 1 of `010`, geometry is layer-2-controlled and independent of layer-3 bit/pair
[H] next live branch is a layer-2 geometry search under fixed twist
[F] the predecessor gadget is holonomy-only in general
[O] full Hamilton decomposition remains open

The short synthesis of the two uploads is:

**The explanatory hypothesis is right for `008/009`: the layer-3 gadget is a holonomy gadget there.
But `010` shows the moment layer `2` joins the predecessor switch, geometry can move — just with the wrong sign.
So the next honest move is to freeze twist and search for a better-signed geometry switch on layer `2`.**
