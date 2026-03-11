Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Use the positive `D5-LAYER3-MODE-SWITCH-008` result to move from the **first mixed regime** to a **strong mixed regime**: keep nonzero monodromy while importing the stronger cycle structures already seen in the best layer-2 cycle seeds from Sessions `005/007`.

Known assumptions:

* I unpacked the bundle and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Exact searched representative family:

  * layer `0` anchor `1`
  * layer `1` anchor `4`
  * layer `4+` anchor `0`
  * representative old bit on layers `2,3`: `q=-1`
  * layer `2` fixed to alternate `0`, with both orientations:

    * `0/2`
    * `2/0`
  * layer `3` depends on one predecessor flag `p`
  * for each `p`-slice choose one mode from

    * `0/3`
    * `3/0`
    * `2/3`
    * `3/2`
    * `3/3`
  * simple predecessor flags tested:

    * `pred_any_phase_align`
    * `pred_sig0_phase_align`
    * `pred_sig1_wu2`
    * `pred_sig4_wu2`
* Exact pilot outcome on `m=5,7,9`:

  * raw rules searched: `200`
  * clean survivors: `64`
  * strict survivors: `64`
  * combined cycle+monodromy survivors: `24`
  * cycle-only survivors: `32`
  * monodromy-only survivors: `8`
  * trivial survivors: `0`
* All validated clean survivors are full-color Latin on `m=5,7,9`, and all validated clean survivors are also strict-clock on `m=5,7,9`.
* The exact predecessor-local-signature fallback was **not** needed.
* Per-flag regime counts:

  * `pred_any_phase_align`:

    * `10` clean strict survivors
    * `0` combined
    * `8` cycle-only
    * `2` monodromy-only
  * `pred_sig0_phase_align`:

    * `10` clean strict survivors
    * `0` combined
    * `8` cycle-only
    * `2` monodromy-only
  * `pred_sig1_wu2`:

    * `22` clean strict survivors
    * `12` combined
    * `8` cycle-only
    * `2` monodromy-only
  * `pred_sig4_wu2`:

    * `22` clean strict survivors
    * `12` combined
    * `8` cycle-only
    * `2` monodromy-only
* So the positive mechanism is concentrated entirely in the two `wu2` predecessor flags.
* Strong exact structural fact from the validated mixed witnesses:

  * the `24` combined survivors are exactly the rules with

    * predecessor flag `pred_sig1_wu2` or `pred_sig4_wu2`
    * layer `2` orientation `0/2` or `2/0`
    * layer-3 slice pair `(M_0,M_1)` an ordered pair of **distinct** modes from
      [
      {0/3,\ 3/0,\ 3/3}.
      ]
  * There are `2 × 2 × 6 = 24` such rules, and all of them survive.
* Every combined witness has the same cycle profile on the pilot range:

  * `m=5`: `U_0` has `5` cycles, all length `5`
  * `m=7`: `U_0` has `7` cycles, all length `7`
  * `m=9`: `U_0` has `9` cycles, all length `9`
* The monodromy in the mixed regime is uniform on every cycle, and depends only on the ordered pair `(M_0,M_1)`:

  * `(0/3,3/0)` gives monodromy `-2 mod m`
  * `(3/0,0/3)` gives monodromy `+2 mod m`
  * `(0/3,3/3)` and `(3/3,3/0)` give monodromy `-1 mod m`
  * `(3/0,3/3)` and `(3/3,0/3)` give monodromy `+1 mod m`
* This dependence is independent, on the pilot data, of:

  * the layer-2 orientation `0/2` versus `2/0`
  * the choice `pred_sig1_wu2` versus `pred_sig4_wu2`
* Representative combined witness:

  * predecessor flag `pred_sig1_wu2`
  * layer `2`: `0/2`
  * layer `3`, `p=0`: `0/3`
  * layer `3`, `p=1`: `3/0`
  * pilot return:

    * `m=5`: `5` cycles of length `5`, all monodromies `3`
    * `m=7`: `7` cycles of length `7`, all monodromies `5`
    * `m=9`: `9` cycles of length `9`, all monodromies `7`
* Cross-session comparison still relevant:

  * the strongest known cycle-only seeds from earlier sessions, especially the `w+u=2` layer-2 split with alternate `4`, already reduced pilot cycle count below the simple `m`-cycle regime, e.g. `3` cycles on `m=9`.
* Scope note:

  * the `200/64/64/24/32/8/0` counts are bundle-backed
  * the exact description of the `24` mixed witnesses and the ordered-pair monodromy law comes from my direct pass over `validation_summary.json`
  * I did not rerun the search from scratch in this turn.

Attempt A:
Idea:
Treat `008` as the first exact mixed-regime success and extract the smallest reusable layer-3 “twist gadget”.

What works:

* This is a genuinely positive step: one extra local predecessor flag already suffices to combine moving `U_0` cycles with nonzero monodromy.
* The positive mechanism is not fragile:

  * it appears for both layer-2 orientations,
  * for both `wu2` predecessor flags,
  * and for all six ordered off-diagonal pairs from
    [
    {0/3,3/0,3/3}.
    ]
* The mixed witnesses are clean, strict, and full-color Latin on the pilot range.
* The exact predecessor-local-signature fallback was unnecessary, so the mechanism already lives inside the simple named predecessor-flag family.
* The ordered layer-3 slice pair controls the monodromy value in a clean way: the gadget can realize uniform twist `\pm 1` or `\pm 2`.

What works:

* The clean-frame barrier is now decisively broken in the mixed direction.
* The next local tool is clear:
  the layer-3 predecessor-based mode switch is now an **exact twist gadget**.

Where it fails:

* The cycle structure of the current mixed witnesses is still simple:
  [
  U_0 = m \text{ cycles of length } m.
  ]
* So the bottleneck has moved again:
  not “can we get twist at all?” but
  “can we keep twist while importing the stronger cycle compression already known from the best layer-2 seeds?”

Attempt B:
Idea:
Graft the exact `008` twist gadget onto the strongest previously validated layer-2 cycle seeds, instead of keeping the representative `q=-1` / alt-`0` base.

What works:

* Earlier sessions already produced stronger cycle-only layer-2 seeds, especially the `w+u=2` alternate-`4` family.
* `008` gives a very small twist family:

  * predecessor flag `pred_sig1_wu2` or `pred_sig4_wu2`
  * layer-3 slice pair any ordered distinct pair from
    [
    {0/3,3/0,3/3}
    ]
* So the natural next search is no longer broad; it is a tiny transplant search.
* If the gadget survives on the stronger cycle seeds, the next milestone would be:
  a clean strict witness with

  * nonzero monodromy,
  * and better-than-`m` cycle structure.

What works:

* This uses the exact positive mechanism already found instead of inventing a new family.
* It is the smallest branch that can plausibly improve the current mixed witness.

Where it fails:

* The current bundle only searched the representative layer-2 base `q=-1` with alternate `0`.
* It gives no evidence yet about the stronger cycle seeds, including the best `w+u=2` / alt-`4` regime.
* So this is the next computation, not yet a theorem.

Candidate lemmas:

* [P] The first clean strict mixed regime has been achieved exactly on the pilot range `m=5,7,9`.
* [C] In the representative one-flag family of `008`, the `24` mixed survivors are exactly the rules with predecessor flag `pred_sig1_wu2` or `pred_sig4_wu2`, layer-2 orientation `0/2` or `2/0`, and ordered distinct slice pair from
  [
  {0/3,3/0,3/3}.
  ]
* [C] In that same family, the phase-align predecessor flags `pred_any_phase_align` and `pred_sig0_phase_align` produce no mixed witnesses.
* [C] Every mixed witness in `008` has pilot cycle profile
  [
  U_0 = m \text{ cycles of length } m
  ]
  on `m=5,7,9`.
* [C] The pilot monodromy of a mixed witness depends only on the ordered layer-3 slice pair:
  it is uniformly `\pm 1` or `\pm 2` on every cycle, independent of layer-2 orientation and independent of whether the predecessor flag is `pred_sig1_wu2` or `pred_sig4_wu2`.
* [C/H] Therefore the successful part of `008` can be regarded as a reusable layer-3 twist gadget.
* [H] The next bottleneck is cycle compression, not twist generation.
* [H] The smallest credible next branch is to transplant the `008` twist gadget onto the full exact list of previously validated cycle-capable layer-2 seeds, especially the strong `w+u=2` / alt-`4` seed.
* [F] A one-extra-flag layer-3 family can only produce cycle-only or monodromy-only behavior.
* [F] The exact predecessor-local-signature fallback is needed for the first mixed witness.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Fix the successful layer-3 twist gadget class from `008`:

  * predecessor flag
    [
    p \in {\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2}}
    ]
  * layer-3 old bit initially fixed to the representative `q=-1`
  * layer-3 slice pair `(M_0,M_1)` an ordered distinct pair from
    [
    {0/3,\ 3/0,\ 3/3}
    ]
* Vary layer `2` over the exact cycle-capable one-old-bit seeds already validated in the earlier chain:

  * `q=-1`: alternates `0,3,4`, both orientations
  * `q+u=1`: alternates `0,3`, both orientations
  * `q+u=-1`: alternates `0,3`, both orientations
  * `u=-1`: alternates `0,3`, both orientations
  * `w+u=2`: alternate `4`, both orientations
* That gives `20` exact layer-2 seeds.
* Stage 1 exact search:

  * layer-2 seed from the above `20`
  * predecessor flag `pred_sig1_wu2` or `pred_sig4_wu2`
  * layer-3 slice pair one of the `6` ordered off-diagonal pairs in
    [
    {0/3,3/0,3/3}
    ]
  * raw size:
    [
    20 \times 2 \times 6 = 240
    ]
    exact rules
* Primary evaluation targets:

  1. `clean_frame=True` on `m=5,7,9`
  2. `strict_clock=True` on `m=5,7,9`
  3. both nonzero monodromy and improved cycle structure
* Comparison baselines:

  * current mixed baseline from `008`:
    total pilot `U_0` cycle count `= 5+7+9 = 21`
  * strongest known cycle-only baseline from earlier sessions:
    total pilot `U_0` cycle count `= 15`, with `3` cycles on `m=9`
* Success target:
  find a clean strict mixed witness with

  * nonzero monodromy,
  * and total pilot `U_0` cycle count `< 21`,
    preferably with fewer than `m` cycles on at least one pilot modulus.
* If Stage 1 fails to improve beyond the representative mixed regime, Stage 2 should widen only one notch:

  * keep the same `240` twist-graft structure,
  * but widen the layer-3 old bit from representative `q=-1` to the full four-bit pool
    [
    T={q=-1,\ q+u=1,\ q+u=-1,\ u=-1}.
    ]

Next branching options:

1. Main branch:
   transplant the exact `008` layer-3 twist gadget onto all `20` validated cycle-capable layer-2 seeds and search for the first **strong mixed** witness.
2. Secondary branch:
   if the twist survives only in the simple `m`-cycle regime, widen the layer-3 old bit from `q=-1` to the full four-bit pool `T`.
3. Side theorem branch:
   formalize the exact `008` classification theorem for the representative family:
   diagonal / off-diagonal slice-pair law and the ordered-pair monodromy rule.

Claim status labels:
[P] first clean strict mixed regime achieved exactly on `m=5,7,9`
[C] mixed witnesses in `008` are exactly the `24` `wu2`-flag off-diagonal rules
[C] ordered slice pair controls uniform monodromy `\pm 1` or `\pm 2`
[H] the layer-3 predecessor mode-switch is now an exact twist gadget
[H] next bottleneck is cycle compression with twist preserved
[F] one extra predecessor flag can only yield cycle-only or monodromy-only behavior
[O] full Hamilton decomposition remains open
