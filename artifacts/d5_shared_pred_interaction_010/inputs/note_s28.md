Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining return-dynamics bottleneck after the exact tail-bit refinements.

Current target:
Absorb `D5-STRONG-CYCLE-MIX-009`, identify the strongest exact negative it proves, and choose the smallest next family that is still genuinely live.

Known assumptions:

* I unpacked the bundle and read:

  * `README.md`
  * `data/search_summary.json`
  * `data/validation_summary.json`
  * `data/validation_candidates.json`
* Exact searched family:

  * fixed anchors:

    * layer `0` anchor `1`
    * layer `1` anchor `4`
    * layer `4+` anchor `0`
  * layer-2 seed chosen from the exact `20` previously validated cycle-capable seeds:

    * `q=-1`: alternates `0,3,4`, both orientations
    * `q+u=1`: alternates `0,3`, both orientations
    * `q+u=-1`: alternates `0,3`, both orientations
    * `u=-1`: alternates `0,3`, both orientations
    * `w+u=2`: alternate `4`, both orientations
  * Stage 1:

    * representative layer-3 old bit `q=-1`
    * predecessor flag in
      `{\texttt{pred\_sig1\_wu2},\texttt{pred\_sig4\_wu2}}`
    * ordered distinct layer-3 slice pair from
      [
      {0/3,\ 3/0,\ 3/3}
      ]
    * raw rules searched: `240`
  * Stage 2:

    * same layer-2 seeds
    * same predecessor flags
    * same ordered slice-pair family
    * widen layer-3 old bit to
      [
      {q=-1,\ q+u=1,\ q+u=-1,\ u=-1}
      ]
    * raw rules searched: `960`
* Exact pilot outcome on `m=5,7,9`:

  * Stage 1:

    * clean survivors: `240`
    * strict survivors: `240`
    * mixed survivors: `192`
    * cycle-only survivors: `48`
    * monodromy-only survivors: `0`
    * trivial survivors: `0`
  * Stage 2:

    * clean survivors: `960`
    * strict survivors: `960`
    * mixed survivors: `912`
    * cycle-only survivors: `48`
    * monodromy-only survivors: `0`
    * trivial survivors: `0`
  * improved mixed survivors: `0`
* All validated clean survivors are full-color Latin on `m=5,7,9`, and all validated clean survivors are also strict-clock on `m=5,7,9`.
* Stability spot-checks on the top `12` mixed survivors at `m=11,13` remain mixed, with the same non-compressing profile.
* Stronger exact fact from my direct pass over `validation_summary.json`:

  * **every clean survivor in the entire `009` family has the same orbit structure**
    [
    U_0 = m \text{ cycles of length } m
    ]
    on each pilot modulus `m=5,7,9`.
  * So the strong cycle-compression mechanism from the earlier alt-`4` seeds is not merely incompatible with twist here; it is completely flattened by the graft family.
* Exact structural classification from my direct pass:

  1. The mixed/cycle-only classification depends only on
     [
     (\text{layer-2 seed},\ \text{layer-3 old bit}),
     ]
     and is independent of predecessor flag and independent of the ordered slice pair.
  2. Precisely:

     * the `16` non-alt-`4` layer-2 seeds are always mixed for all four layer-3 old bits;
     * the four alt-`4` seeds
       [
       (q=-1,4,2/4),\ (q=-1,4,4/2),\ (w+u=2,4,2/4),\ (w+u=2,4,4/2)
       ]
       are cycle-only for layer-3 bit `q=-1`, and mixed for layer-3 bits
       [
       q+u=1,\ q+u=-1,\ u=-1.
       ]
  3. Among mixed survivors, the monodromy value depends only on the ordered layer-3 slice pair, exactly as in Session `008`:

     * `(0/3,3/0)` gives uniform monodromy `-2 mod m`
     * `(3/0,0/3)` gives uniform monodromy `+2 mod m`
     * `(0/3,3/3)` and `(3/3,3/0)` give uniform monodromy `-1 mod m`
     * `(3/0,3/3)` and `(3/3,0/3)` give uniform monodromy `+1 mod m`
  4. This monodromy law is independent, on the validated data, of:

     * the layer-2 seed,
     * the layer-3 old bit,
     * the choice of predecessor flag.
* Scope note:

  * the `240/960/912/48/0/0` counts and the no-improvement result are bundle-backed;
  * the “all clean survivors have universal orbit structure `m` cycles of length `m`” statement and the exact factorization of classification data are from my direct pass over `validation_summary.json`;
  * I did not rerun the search from scratch in this turn.

Attempt A:
Idea:
Read `009` as an exact no-go for the whole “twist graft onto stronger cycle seeds” program in its current noninteractive form.

What works:

* The negative result is stronger than the README headline.
* It is not only that no mixed survivor improves the cycle baseline.
* The sharper fact is:
  **the entire `009` family collapses to one universal orbit structure**
  [
  U_0 = m \text{ cycles of length } m
  ]
  on `m=5,7,9`, regardless of whether the survivor is mixed or cycle-only.
* So the current graft family does not preserve the stronger cycle-compression mechanism even in the cycle-only cases.
* Stage 2 successfully restores twist on the alt-`4` seeds for three of the four layer-3 bits, but the restored mixed witnesses still live in the same universal `m`-cycle regime.

What works:

* This gives a clean computational no-go for the whole fixed-seed graft branch:
  strong cycle compression is destroyed before any twist-versus-compression competition can even happen.

Where it fails:

* This does not rule out genuinely interactive local families.
* It only kills the family where the layer-2 seed is fixed and the layer-3 twist gadget is grafted on top.

Attempt B:
Idea:
Extract the exact separability law from `009` and use it to identify the smallest next live branch.

What works:

* The validated data show that the `009` family is dynamically separable:

  1. orbit structure is frozen universally to the simple `m`-cycle regime;
  2. mixed versus cycle-only is determined only by `(layer-2 seed, layer-3 old bit)`;
  3. once mixed, the monodromy value is determined only by the ordered layer-3 slice pair.
* In particular:

  * predecessor-flag choice is irrelevant to the final pilot classification in `009`;
  * layer-2 seed has no effect on orbit structure once the graft is present;
  * layer-3 slice-pair choice affects only the monodromy label, not the cycle structure.
* So the present family has no real layer-2/layer-3 interaction left.

What works:

* This points very sharply to the next smallest live branch:
  **layer 2 must participate in the same local mode switch as layer 3.**
* A merely wider one-bit layer-3 graft is no longer a credible primary direction.

Where it fails:

* The current artifact does not tell us which shared local flag or which layer-2 slice pool is best.
* That is the next exact search problem.

Candidate lemmas:

* [C] In `009`, every clean survivor is strict-clock and full-color Latin on `m=5,7,9`.
* [C] In `009`, every clean survivor has pilot orbit structure
  [
  U_0 = m \text{ cycles of length } m
  ]
  for `m=5,7,9`.
* [C] In `009`, mixed versus cycle-only classification depends only on `(layer-2 seed, layer-3 old bit)` and is independent of predecessor flag and independent of the ordered slice pair.
* [C] The `16` non-alt-`4` layer-2 seeds are always mixed; the four alt-`4` seeds are cycle-only exactly for layer-3 bit `q=-1` and mixed for layer-3 bits `q+u=1`, `q+u=-1`, `u=-1`.
* [C] Among mixed survivors, the uniform monodromy value depends only on the ordered layer-3 slice pair and follows the same `\pm1/\pm2` law as in `008`.
* [C/H] Therefore the entire `009` graft family is dynamically separable: orbit structure is locked, while monodromy is a separate layer-3 label.
* [H] The next minimal constructive family must make layer 2 and layer 3 respond to the same local flag, so that orbit structure and twist can interact.
* [F] Grafting the current layer-3 twist gadget onto stronger cycle seeds can preserve the stronger cycle-compression regime.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* The next exact search should introduce a **shared predecessor-based mode switch** on both layers `2` and `3`.
* Keep the exact successful layer-3 twist gadget class from `008/009`:

  * predecessor flag
    [
    p \in {\texttt{pred_sig1_wu2},\ \texttt{pred_sig4_wu2}}
    ]
  * layer-3 old bit initially from the twist-surviving Stage-2 pool
    [
    {q+u=1,\ q+u=-1,\ u=-1}
    ]
  * ordered layer-3 slice pair `(M_0,M_1)` any ordered distinct pair from
    [
    {0/3,\ 3/0,\ 3/3}
    ]
* New ingredient:
  let layer `2` also depend on the same predecessor flag `p`.
* Smallest credible layer-2 slice pool:
  use only exact previously validated strong alt-`4` cycle modes:
  [
  {q=-1:2/4,\ q=-1:4/2,\ w+u=2:2/4,\ w+u=2:4/2}.
  ]
* Let the layer-2 `p`-slices choose an ordered pair from this four-mode pool.
  This keeps the search entirely inside exact previously validated cycle-capable layer-2 modes while introducing genuine local interaction.
* Stage 1 raw search size:

  * layer-2 ordered slice pairs: `4 × 4 = 16`
  * predecessor flags: `2`
  * layer-3 old bits: `3`
  * layer-3 ordered slice pairs: `6`
  * total:
    [
    16 \times 2 \times 3 \times 6 = 576
    ]
    exact rules
* Primary evaluation targets:

  1. `clean_frame=True` on `m=5,7,9`
  2. `strict_clock=True` on `m=5,7,9`
  3. nonzero monodromy on every pilot modulus
  4. improved cycle structure:

     * total pilot `U_0` cycle count `< 21`, or
     * fewer than `m` cycles on at least one pilot modulus
* Stronger success target:
  approach the old cycle-only compression baseline `15` while keeping nonzero monodromy.
* If Stage 1 fails with the same universal `m`-cycle regime, then Stage 2 should widen only one notch:
  add exact non-alt-`4` layer-2 modes from the previously validated pool, e.g.
  `0/2, 2/0, 2/3, 3/2`, so that the shared local switch can mix strong and simple cycle modes.

Next branching options:

1. Main branch:
   exact shared-predecessor interaction search, with both layers `2` and `3` switching on the same predecessor flag and layer-2 slices drawn from the exact strong alt-`4` pool.
2. Secondary branch:
   if the strong alt-`4` shared-switch family still collapses to the universal `m`-cycle regime, widen the layer-2 slice pool by one notch to include exact non-alt-`4` cycle modes.
3. Side theorem branch:
   formalize the `009` separability theorem:
   universal orbit structure, mixed/cycle-only determined by `(layer-2 seed, layer-3 old bit)`, and monodromy value determined only by the ordered layer-3 slice pair.

Claim status labels:
[P] `009` gives a strong exact negative for the fixed-seed twist-graft program
[C] every clean survivor in `009` has the same pilot orbit structure `U_0 = m` cycles of length `m`
[C] mixed/cycle-only classification in `009` depends only on `(layer-2 seed, layer-3 old bit)`
[C] mixed monodromy in `009` depends only on the ordered layer-3 slice pair
[H] the next smallest live branch is a shared layer-2/layer-3 predecessor switch
[F] the current twist graft can preserve stronger cycle compression
[O] full Hamilton decomposition remains open

The sharpest update is:
`009` did not merely say “the strong-cycle graft failed.” It proved something stricter: the whole fixed-seed graft family collapses to a universal simple orbit structure, and only the monodromy label remains adjustable. So the next honest move is to make layer `2` join the same local predecessor switch as layer `3`.
