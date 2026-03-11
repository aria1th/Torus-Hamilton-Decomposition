I unpacked the bundle, read `README.md`, `data/search_summary.json`, `data/validation_summary.json`, and `data/validation_candidates.json`, and I also did one extra classification pass over the validated rule tables to see which context features are actually being used.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining dynamical degeneracy after the exact tail-bit refinements.

Current target:
Absorb the `D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005` result and choose the smallest next active family. The frontier has moved again: we now have exact strict witnesses with nontrivial `U_0`; the missing step is to combine orbit-structure and monodromy in one witness.

Known assumptions:

* I read the uploaded bundle’s `README.md`, `data/search_summary.json`, `data/validation_summary.json`, and `data/validation_candidates.json`.
* I also classified every validated survivor by its actual dependence on the 10 contexts
  [
  (\text{align_s0},\text{align_s1},00_s0,00_s1,01_s0,01_s1,10_s0,10_s1,11_s0,11_s1).
  ]
* Exact bundle scope:

  * old bits tested:

    * `q=-1`
    * `q+u=1`
    * `w+u=2`
    * `q+u=-1`
    * `u=-1`
  * pilot moduli: `m=5,7,9`
  * one-layer-active families plus full two-layer families
  * search runtime `91.31s`
  * validation runtime `35.59s`
* Exact global outcomes:

  * family-aggregated clean survivors: `723`
  * family-aggregated strict survivors: `723`
  * unique clean survivors: `328`
  * unique strict survivors: `328`
  * unique context-dependent clean survivors: `248`
  * unique context-dependent strict survivors: `248`
  * unique strict survivors with nontrivial `U_0`: `240`
  * all `328` validated survivors are full-color Latin on `m=5,7,9`
* Every tested old bit already gives one-layer-active context-dependent clean survivors.
* `q=-1` is the richest single bit on the pilot range:

  * total unique survivors: `100`
  * unique nontrivial-`U_0` survivors: `82`
* Crucial extra classification fact from the validated rule tables:

  * **all 248 context-dependent survivors ignore `phase_align`, `b1`, and `b2`;**
  * every context-dependent survivor depends only on the added old quotient bit `s`.
* Exact survivor taxonomy from the validated tables:

  * `80` are constant on both layers
  * `80` are `s`-only on layer 2 and constant on layer 3
  * `80` are constant on layer 2 and `s`-only on layer 3
  * `88` are `s`-only on both layers
  * there are **0** surviving rules with genuine dependence on `phase_align`, `b1`, or `b2`
* Dynamical split:

  * `192` strict survivors are cycle-only:
    nontrivial `U_0` cycles but all monodromies `0`
  * `48` strict survivors are monodromy-only:
    fixed-point `U_0` but nonzero monodromy
  * `0` validated survivors combine nontrivial cycles with nonzero monodromy
* Representative cycle seed:

  * extra bit `s=q=-1` (equally similar witnesses exist for other old bits)
  * layer 2 uses anchor `2` on `s=0`, anchor `0` on `s=1`
  * layer 3 stays constant at anchor `3`
  * on `m=5,7,9`, this is full-color Latin, clean-frame, strict-clock, and
    [
    U_0 = m \text{ cycles of length } m,
    \qquad \text{all monodromies } 0.
    ]
* Representative monodromy seed:

  * extra bit `s=q=-1`
  * layer 2 stays constant at anchor `2`
  * layer 3 uses anchor `3` on `s=0`, anchor `0` on `s=1`
  * on `m=5,7,9`, this is full-color Latin, clean-frame, strict-clock, and
    [
    U_0 = m^2 \text{ fixed points},
    \qquad \text{all monodromies } -1 \pmod m
    ]
    i.e. monodromies `4,6,8` for `m=5,7,9`.
* Scope note:

  * the counts above are bundle-backed
  * the “all survivors are `s`-only” statement is from my own direct classification of the validated tables in `validation_summary.json`
  * I did not rerun the exhaustive search from scratch in this turn.

Attempt A:
Idea:
Treat Session 23 as the exact point where the project leaves the `U_0`-trivial regime.

What works:

* This is a genuinely stronger milestone than the previous session.
* We now have many exact pilot witnesses that are simultaneously:

  * full-color Latin,
  * clean-frame,
  * strict-clock,
  * and nontrivial in `U_0`.
* One-layer-active families already suffice.
* So the previous clean-frame barrier is not merely cracked; it is decisively broken.
* The simplest successful witnesses already realize a clean first nontrivial section dynamic:
  [
  U_0 \cong m \text{ cycles of length } m.
  ]
* Moreover, strict clock is no longer fragile in this branch:
  every validated clean survivor is also strict on `m=5,7,9`.

Where it fails:

* The new witnesses split into two disjoint dynamical modes:

  * cycle-only,
  * or monodromy-only.
* No witness in the exact searched family achieves both:

  * some cycle length `>1`,
  * and some nonzero monodromy.
* So the next bottleneck is now precise:
  **couple orbit-structure and monodromy in the same return system.**

Attempt B:
Idea:
Compress the validated survivors by actual table dependence, not by the nominal context vocabulary, and infer the minimal missing degree of freedom.

What works:

* This reveals a much sharper structural fact than the bundle README alone:
  the successful family does **not** actually use the tail bits.
* All context-dependent survivors collapse to `s`-only tables:
  for each active layer, the table is constant on all `s=0` contexts and constant on all `s=1` contexts.
* So the first successful active branch is not really
  [
  (\text{phase_align},b_1,b_2,s),
  ]
  but simply
  [
  s.
  ]
* The dynamics then separate into two exact mechanisms:

  1. **cycle mechanism**:
     a layer-2 `s`-split such as `2/0`, `2/3`, or `2/4`
     gives
     [
     U_0 = m \text{ cycles of length } m,
     \quad \text{monodromy } 0;
     ]
  2. **monodromy mechanism**:
     a layer-3 `s`-split such as `3/0` or `0/3`
     gives fixed points with uniform nonzero monodromy `\pm 1`.
* There are also exact cancellations:
  `8` strict context-dependent survivors are still `U_0`-trivial, showing that same-bit two-layer coupling can neutralize rather than combine effects.

Where it fails:

* This is still pilot-exact evidence, not a general theorem beyond the searched family.
* It does not yet say which pair of local observables will combine the two mechanisms.
* But it does strongly suggest that the next step is **not** “more tail-only context,” and likely not even “same old bit on both layers.”

Candidate lemmas:

* [C] In the exact one-old-bit family searched on `m=5,7,9`, there are `248` unique context-dependent strict survivors and `240` of them have nontrivial `U_0`.
* [C] Every validated clean survivor in this family is also strict-clock on `m=5,7,9`.
* [C] Every validated context-dependent survivor in this family ignores `phase_align`, `b1`, and `b2`; all such survivors are `s`-only.
* [C] The exact pilot dynamics split into two modes:

  * cycle-only (`192` witnesses),
  * monodromy-only (`48` witnesses),
  * and there are no witnesses with both nontrivial cycles and nonzero monodromy.
* [C/H] Layer-2 `s`-splits generate the cycle mechanism, while layer-3 `s`-splits of `3/0` generate the monodromy mechanism.
* [H] The smallest credible next family is to decouple the two active layers by giving them **different old bits**, rather than adding more tail-only context.
* [H] If that fails, the next enrichment should be predecessor-tail or a second local bit on one layer.
* [F] The first successful active family genuinely uses the tail bits `phase_align`, `b1`, `b2` in an essential way.
* [F] One old bit within the current family is enough to combine cycle structure and nonzero monodromy in the same witness.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* First exact next search:

  * choose an ordered pair of old bits
    [
    (s_2,s_3)\in S^2,
    \qquad
    S={q=-1,\ q+u=1,\ w+u=2,\ q+u=-1,\ u=-1}
    ]
  * let layer 2 depend only on `s_2`
  * let layer 3 depend only on `s_3`
  * do **not** include `phase_align,b1,b2` initially, since the successful rules ignored them
* Use the smallest mechanism-combining palette first:

  * layer `2`: seed anchor `2` versus alternate `a\in\{0,3,4\}`
    because those are exact cycle-producing alternates
  * layer `3`: seed anchor `3` versus alternate `0`
    because that is the exact monodromy-producing alternate
  * allow both orientations on each layer:
    `2/a` or `a/2`, and `3/0` or `0/3`
* Primary evaluation targets:

  1. `clean_frame=True` on `m=5,7,9`
  2. `strict_clock=True` on `m=5,7,9`
  3. both

     * some cycle length `>1`
     * and some nonzero monodromy
* Secondary optimization:

  * fewer `U_0` cycles
  * longer `U_0` cycles
  * more nonzero monodromies
* If every ordered pair `(s_2,s_3)` still yields only cycle-only or monodromy-only behavior, then move to:

  * predecessor-tail × old-bit hybrids, or
  * a two-old-bit-plus-one-tail-bit family.

Next branching options:

1. **Main branch**
   Search the minimal two-old-bit decoupled family:
   one old bit drives the layer-2 cycle mechanism, a different old bit drives the layer-3 monodromy mechanism.
2. **Secondary branch**
   If the two-old-bit family still cannot combine the mechanisms, add predecessor-tail information to one layer only.
3. **Side theorem branch**
   Prove that every one-old-bit clean survivor is `s`-only and that same-bit two-layer coupling can realize only cycle-only, monodromy-only, or exact cancellation.

Claim status labels:
[P] Exact pilot search on `m=5,7,9` now reaches nontrivial `U_0`
[C] All validated context-dependent survivors in this family are `s`-only
[C] Cycle-only and monodromy-only mechanisms both exist exactly
[C] No witness in the one-old-bit family combines the two mechanisms
[H] Two independent old bits are the smallest credible next family
[F] Tail-bit dependence is essential in the first successful active family
[O] Full Hamilton decomposition remains open

The sharpest update is:
the one-old-bit branch is not just positive — it shows that the first nontrivial return dynamics come from an `s`-only mechanism, and that orbit structure and monodromy already appear separately. The most surgical next move is to try to **decouple those two mechanisms by layer**, before spending complexity on predecessor-tail or more tail bits.
