Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Absorb the clean negative from `D5-LAYER2-GEOMETRY-UNDER-FIXED-TWIST-011` and choose the smallest next family that is still genuinely live. The main issue is now very sharp: fixed twist plus a one-flag layer-2 switch does not repair the sign of geometry.

Known assumptions:

* I unpacked and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Exact searched family:

  * fixed anchors:

    * layer `0 -> 1`
    * layer `1 -> 4`
    * layer `4+ -> 0`
  * fixed canonical twist gadget:

    * layer-3 flag `pred_sig1_wu2`
    * layer-3 old bit `q+u=-1`
    * slice pair `0/3 , 3/0`
  * control twist:

    * same layer-3 flag and old bit
    * sign-reversed slice pair `3/0 , 0/3`
  * layer-2 local flag:

    * `pred_sig1_wu2`
    * `pred_sig4_wu2`
  * layer-2 ordered slice pair drawn from
    [
    M_2=
    {
    q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2,\
    q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2
    }.
    ]
* Exact search sizes:

  * canonical twist: `128` rules
  * control twist: `128` rules
  * Stage 2 widening was not triggered
* Exact canonical-twist outcomes on `m=5,7,9`:

  * clean strict survivors: `48`
  * mixed: `46`
  * monodromy-only: `2`
  * cycle-only: `0`
  * improved mixed: `0`
* Exact regime distribution among the `48` canonical clean strict survivors:

  * `34` mixed with total pilot cycle count `21`
  * `10` mixed with total pilot cycle count `39`
  * `2` mixed with total pilot cycle count `137`
  * `2` monodromy-only with total pilot cycle count `155`
* Exact control comparison:

  * same clean counts as canonical
  * same cycle signatures on all `128 / 128` rules
  * same total pilot cycle count on all `128 / 128` rules
  * same profile-kind on all `128 / 128` rules
  * so twist sign is completely irrelevant to geometry in this family
* Per-layer2-flag summary:

  * `pred_sig1_wu2`:

    * `24` clean strict survivors
    * `22` mixed
    * `2` monodromy-only
    * all `137` and all `155` cases occur here
  * `pred_sig4_wu2`:

    * `24` clean strict survivors
    * `24` mixed
    * `0` monodromy-only
    * only `21` and `39` appear here
* Representative anti-compressive mixed rule:

  * layer-2 flag `pred_sig1_wu2`
  * `p2=0 -> q=-1:2/4`
  * `p2=1 -> q=-1:4/2`
  * pilot cycle counts:

    * `m=5: 9`
    * `m=7: 13`
    * `m=9: 17`
* Representative monodromy-only rule:

  * layer-2 flag `pred_sig1_wu2`
  * `p2=0 -> w+u=2:2/4`
  * `p2=1 -> w+u=2:4/2`
  * pilot return:

    * `m=5: 25` fixed points
    * `m=7: 49` fixed points
    * `m=9: 81` fixed points
* Stronger exact fact from my direct pass over `validation_summary.json`:

  * every non-baseline geometry in `011` comes entirely from the four alt-`4` layer-2 modes
    [
    A_4={q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2};
    ]
  * the four simple `q=-1` modes
    [
    {q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2}
    ]
    appear only in baseline `21` mixed survivors.
* Scope note:

  * the main counts above are bundle-backed
  * the “all non-baseline geometry is alt-`4`-only” statement is from my own direct pass over the validated candidates
  * I did not rerun the search from scratch in this turn.

Attempt A:
Idea:
Read `011` as an exact no-go for the fixed-twist, one-flag layer-2 geometry program over the current `8`-mode pool.

What works:

* This is a clean negative.
* The fixed-twist family does not merely fail to beat the mixed baseline; it shows that twist sign has no geometric effect at all here.
* Every geometry profile already comes entirely from layer-2 local data.
* So widening layer 3 is no longer a credible primary branch.
* The top mixed survivors stay on the baseline profile under spot-checks at `m=11,13`, so the failure is stable, not a pilot fluke.

Where it fails:

* It does not rule out finer layer-2 predecessor resolution.
* It also does not rule out richer layer-2 state built from the already available named predecessor flags.
* So it kills one-flag layer-2 geometry under fixed twist, not layer-2 geometry itself.

Attempt B:
Idea:
Use the validated survivors to isolate where nontrivial geometry actually lives, then enlarge only that part.

What works:

* The direct classification is sharper than the README alone:
  every non-baseline profile `39,137,155` comes from the four alt-`4` modes and never from the simple `q=-1` modes.
* So the sign problem sits entirely inside the alt-`4` geometry pool.
* The two named predecessor flags behave differently there:

  * `pred_sig1_wu2` is the destructive coarse partition,
  * `pred_sig4_wu2` is the milder partition.
* That points to the smallest live branch:
  refine layer-2 predecessor state by using both flags together, while keeping the twist fixed.
* This gives a four-state layer-2 local switch without introducing any new synthetic predicate.

Where it fails:

* We do not yet know whether the two-flag refinement repairs the sign or merely reproduces the same `39/137/155` regimes more finely.
* So this is still the next exact computation, not yet a theorem.

Candidate lemmas:

* [C] In `011`, canonical twist and sign-reversed control have identical clean/strict survivorship and identical cycle signatures on all `128` layer-2 rules.
* [C] Therefore geometry in the `011` family is insensitive to twist sign.
* [C] In `011`, every non-baseline geometry profile (`39`, `137`, `155`) uses only modes from
  [
  A_4={q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2}.
  ]
* [C] The simple `q=-1` modes
  [
  {0/2,\ 2/0,\ 2/3,\ 3/2}
  ]
  never produce non-baseline geometry in `011`.
* [C] All `137` and `155` profiles in `011` occur under `pred_sig1_wu2`; `pred_sig4_wu2` never produces them.
* [H] The next minimal live branch is a four-state layer-2 geometry search using the pair
  [
  (\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2})
  ]
  under fixed twist.
* [H] Stage 1 of that search should use only the alt-`4` pool `A_4`, because all non-baseline geometry already lives there.
* [H] If the two-flag alt-`4` search still fails, the next widening should be on layer-2 local state or exact predecessor-tail signatures, not on layer-3 twist.
* [F] Fixed twist plus a one-flag layer-2 switch over the current `8`-mode pool can beat the mixed baseline.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Freeze the canonical exact mixed twist gadget:

  * layer-3 flag `pred_sig1_wu2`
  * layer-3 old bit `q+u=-1`
  * slice pair
    [
    p_3=0 \to 0/3,\qquad p_3=1 \to 3/0
    ]
  * use the sign-reversed twist only as a control on the best survivors
* Define the two-bit layer-2 predecessor state
  [
  c_2=(\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2})\in{00,01,10,11}.
  ]
* Stage 1 layer-2 mode pool:
  [
  A_4={q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2}.
  ]
* Search all assignments
  [
  c_2 \mapsto A_4,
  ]
  i.e. `4^4 = 256` exact rules.
* Evaluate:

  * full-color Latin
  * clean frame
  * strict clock
  * exact `U_0` cycle counts and cycle lengths
  * monodromy on `m=5,7,9`
* Primary target:
  find a clean strict mixed witness with total pilot cycle count `< 21`.
* Stronger target:
  get closer to the earlier cycle-only baseline `15` while keeping nonzero monodromy.
* Stage 2 only if Stage 1 fails:
  enlarge the layer-2 pool to
  [
  A_4 \cup {q=-1:0/2,\ q=-1:2/0,\ q=-1:2/3,\ q=-1:3/2},
  ]
  giving `8^4 = 4096` exact rules.
* If that still fails:
  replace the named two-flag state by an exact predecessor-tail local-signature bit or small local-signature state on layer `2`.

Next branching options:

1. Main branch:
   two-flag four-state layer-2 geometry search on the pure alt-`4` pool under fixed twist.
2. Secondary branch:
   widen the layer-2 mode pool to `8` modes if the pure alt-`4` four-state search still gives no improvement.
3. Side theorem branch:
   formalize the `011` clean negative:
   twist sign is geometrically irrelevant, and every non-baseline geometry comes from the alt-`4` layer-2 pool.

Claim status labels:
[P] `011` gives a clean exact negative for fixed-twist one-flag layer-2 geometry
[C] twist sign is geometrically irrelevant throughout the searched `011` family
[C] all non-baseline geometry in `011` is alt-`4`-only
[C] `pred_sig1_wu2` carries all `137/155` destructive cases
[H] the next smallest live branch is a two-flag four-state layer-2 search on the alt-`4` pool
[F] one-flag fixed-twist layer-2 geometry can beat the mixed baseline in the current pool
[O] the full Hamilton decomposition remains open

The sharpest synthesis is:

`011` did not say geometry is dead. It said something narrower and cleaner:
with twist frozen, geometry is entirely a layer-2 issue, twist sign does not matter, and every non-baseline geometry effect sits inside the alt-`4` layer-2 pool.
So the smallest honest next move is to refine layer `2` itself — first by the two named `wu2` predecessor flags, and only then by any heavier local signature machinery.
