Return the research note:
Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Absorb `D5-TWO-OLD-BIT-CYCLE-MONODROMY-006`, identify the exact obstruction it proves, and choose the smallest next family that is still genuinely untested.

Known assumptions:

* I unpacked the bundle and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Exact searched family:

  * ordered pair `(s2,s3)` from
    [
    S={q=-1,\ q+u=1,\ w+u=2,\ q+u=-1,\ u=-1}
    ]
  * layer 2 uses seed anchor `2` versus alternate `a in {0,3,4}`
  * layer 3 uses seed anchor `3` versus alternate `0`
  * both layers are `s`-only
  * `phase_align,b1,b2` excluded
* Exact bundle outcome on pilot moduli `m=5,7,9`:

  * total rules searched: `300`
  * clean survivors: `200`
  * strict survivors: `200`
  * combined cycle+monodromy survivors: `0`
  * cycle-only survivors: `200`
  * monodromy-only survivors: `0`
  * trivial survivors: `0`
* Stronger structural fact from my extra pass over the validated survivors:

  * the `200` survivors factor exactly as
    [
    20\ \text{surviving layer-2 patterns} \times 10\ \text{arbitrary layer-3 choices},
    ]
    where the `10` layer-3 choices are
    `5` old-bit names times `2` orientations.
  * So for each surviving layer-2 rule, **all** layer-3 choices survive.
* Even stronger:

  * grouping the `200` validated survivors by return-data signature gives exactly **one** dynamical signature:
    on each of `m=5,7,9`,
    [
    U_0 = m \text{ cycles of length } m,\qquad \text{all monodromies } 0.
    ]
  * Thus in this family, layer 3 is not merely “insufficient”; it is dynamically invisible at the pilot return level once the layer-2 cycle split is present.
* Surviving layer-2 patterns are exactly:

  * `q=-1`: alternates `0,3,4`, both orientations
  * `q+u=1`: alternates `0,3`, both orientations
  * `q+u=-1`: alternates `0,3`, both orientations
  * `u=-1`: alternates `0,3`, both orientations
  * `w+u=2`: alternate `4`, both orientations
* Important cross-session comparison from my earlier direct classification of the validated `005` tables:

  * the only monodromy-only witnesses that already coexist with a moving layer-2 split use layer-3 tables `3/2` or `2/3`;
  * the layer-3 tables `3/0` or `0/3` give monodromy-only only against constant layer 2.
* Scope note:

  * the exact `006` counts above are bundle-backed;
  * the Cartesian-product factorization and “single dynamical signature” statements are from my own direct classification of `validation_summary.json`;
  * the `3/2` vs `3/0` comparison comes from my earlier direct classification of the validated `005` survivors;
  * I did not rerun the exhaustive searches from scratch in this turn.

Attempt A:
Idea:
Read `006` as an exact no-go for the minimal decoupled two-old-bit family with layer-3 alternate anchor fixed to `0`.

What works:

* This closes that specific branch cleanly.
* The result is stronger than the README headline:
  it is not merely that no combined witness exists; the whole family collapses to the pure layer-2 cycle regime.
* Exact strengthening:

  * `200 = 20 × 10`
  * every successful layer-2 rule survives with every layer-3 choice
  * all survivors have identical pilot return data
* So in this family the layer-3 bit choice and the layer-3 orientation do not affect clean/strict survivorship or the observed `U_0` dynamics.

Where it fails:

* This does **not** yet rule out richer layer-3 palettes.
* In particular, `006` only tested layer-3 alternate `0`.
* It does not test the one layer-3 alternate that earlier pilot data already singled out as capable of carrying monodromy under a moving layer-2 split: alternate `2`.

Attempt B:
Idea:
Use the comparison with `005` to identify the smallest genuinely untested family: keep the successful decoupled layer-2 cycle split, but enrich layer 3 from palette `{0}` to palette `{0,2}`.

What works:

* This is more surgical than jumping immediately to predecessor-tail.
* It uses an exact clue from validated data rather than a fresh guess:
  the known moving-layer-2 monodromy witnesses in `005` use `3/2` or `2/3`, not `3/0` or `0/3`.
* So the failure of `006` is best read as:
  “decoupling plus layer-3 alt `0` is too weak,”
  not as
  “any decoupled two-old-bit layer-3 mechanism is impossible.”
* The next family is still tiny and exact.

Where it fails:

* We do not yet know whether layer-3 alternate `2` will produce:

  * combined cycle+monodromy,
  * monodromy-only,
  * or another collapse to the cycle regime.
* So this remains the next computation, not a theorem.

Candidate lemmas:

* [C] In the exact `006` family, clean/strict survivorship depends only on the layer-2 rule.
* [C] In the exact `006` family, all `200` validated survivors have the same pilot return signature:
  [
  U_0 = m \text{ cycles of length } m,\qquad \text{all monodromies } 0
  ]
  for `m=5,7,9`.
* [C] Hence the minimal decoupled family with layer-3 alternate `0` factors through the layer-2 cycle mechanism.
* [C/H] The obstruction in `006` is not “two-old-bit decoupling fails completely”; it is “the `3/0`-type layer-3 twist is neutralized once the cycle split is active.”
* [C] In the validated `005` data, the only monodromy-only witnesses compatible with a moving layer-2 split use layer-3 tables `3/2` or `2/3`.
* [H] Therefore the smallest credible next family is a decoupled two-old-bit search with layer-3 alternate palette `{0,2}`, not immediate predecessor-tail enrichment.
* [F] The negative result of `006` rules out all decoupled two-old-bit layer-3 mechanisms.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Run the next exact family:

  * ordered pair `(s2,s3) in S^2`
  * layer 2:

    * seed anchor `2`
    * alternate `a in {0,3,4}`
    * orientations `2/a`, `a/2`
  * layer 3:

    * seed anchor `3`
    * alternate `b in {0,2}`
    * orientations `3/b`, `b/3`
  * still `s2`-only on layer 2 and `s3`-only on layer 3
  * still exclude `phase_align,b1,b2`
* Two natural exact search sizes:

  1. full family:
     [
     25 \times 3 \times 2 \times 2 \times 2 = 600
     ]
     rules;
  2. smaller follow-on from the already successful `006` layer-2 patterns:
     [
     20 \times 5 \times 4 = 400
     ]
     rules.
* Primary evaluation targets:

  1. `clean_frame=True` on `m=5,7,9`
  2. `strict_clock=True` on `m=5,7,9`
  3. both

     * some cycle length `>1`
     * some nonzero monodromy
* Secondary targets:

  * fewer than `m` cycles
  * longer cycles
  * larger monodromy support
* If the `{0,2}` layer-3 palette still fails, then the next branch should be:

  * keep one successful layer-2 cycle split fixed,
  * add one predecessor-tail flag to layer 3 only.

Next branching options:

1. Main branch:
   exact decoupled two-old-bit search with layer-3 alternate palette `{0,2}`.
2. Secondary branch:
   if `{0,2}` still gives no combined witness, add one predecessor-tail bit to layer 3 only.
3. Side theorem branch:
   formalize the exact `006` factorization statement that the entire alt-`0` decoupled family collapses to the layer-2 cycle regime.

Claim status labels:
[P] `006` gives an exact no-go for the minimal decoupled family with layer-3 alternate `0`
[C] the `006` survivor set factors as `20` layer-2 patterns times `10` arbitrary layer-3 choices
[C] all `200` validated survivors in `006` have identical cycle-only pilot dynamics
[H] the next smallest live branch is layer-3 palette enrichment from `{0}` to `{0,2}`
[F] `006` rules out all decoupled two-old-bit layer-3 mechanisms
[O] the full decomposition problem remains open

The sharpest update is:
`006` did not show that two-old-bit decoupling is hopeless. It showed something narrower and stronger: with layer-3 alternate fixed to `0`, the whole family collapses to the pure layer-2 cycle mechanism. The smallest honest next move is therefore to enrich layer 3 to include alternate `2`, because that is the one exact palette element the earlier validated data already singled out as monodromy-capable under a moving layer-2 split.
