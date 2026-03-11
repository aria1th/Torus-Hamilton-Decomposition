Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining dynamical degeneracy after the exact tail-bit refinements.

Current target:
Absorb the `D5-STRICT-PALETTE-CONTEXT-004` result and identify the smallest next active family that can survive beyond the current clean-frame barrier.

Known assumptions:

* I read the uploaded bundle’s `README.md`, `data/search_summary.json`, `data/validation_summary.json`, and `data/validation_candidates.json`.
* Exact search scope in the bundle:

  * `16` strict-friendly anchor families `(a,b)` with
    [
    a,b\in{0,2,3,4}
    ]
  * `1024` raw 5-context tables per family
  * total raw rules searched: `16384`
  * contexts:

    * `phase_align`
    * nonzero `00,01,10,11` from `(b1,b2)`
* Global exact outcome on pilot moduli `m=5,7,9`:

  * `49` family-aggregated clean survivors
  * `49` family-aggregated strict survivors
  * these collapse to exactly `16` unique actual rules
  * all `16` unique survivors are context-independent constant pairs
    [
    (a,b)\in{0,2,3,4}^2
    ]
  * all `16` are full-color Latin, clean-frame, and strict-clock on `m=5,7,9`
  * all `16` have trivial section dynamics:
    `U_0` has exactly `m^2` fixed points and monodromy `0`
* Crucial negative fact:

  * `0` context-dependent clean survivors
  * `0` context-dependent strict survivors
  * `0` nontrivial-`U_0` survivors
* Important refinement of the earlier reading:

  * the failure is not purely local-Latin at the first filter stage
  * the search summary shows large families of color-0-Latin tables that later collapse to constant pairs at the clean-frame stage
  * example: family `(a,b)=(0,3)` has many color-0-Latin tables but only `2` effective clean survivors, both constant
* Scope note:

  * I did not rerun the exhaustive search from scratch in this turn
  * the conclusions above are bundle-backed.

Attempt A:
Idea:
Read `STRICT-PALETTE-CONTEXT-004` as an exact no-go for the entire context-only strict-friendly two-anchor branch based on `(\text{phase\_align},b_1,b_2)`.

What works:

* This closes the branch cleanly on the pilot range `m=5,7,9`.
* It is stronger than the earlier seed/1-palette failure:
  even after allowing all strict-friendly alternates `{0,2,3,4}`, every full survivor is still a constant pair.
* The surviving constant pairs are not fragile:
  all `16` of them are full-color Latin, clean-frame, and strict-clock.
* None of them changes `U_0`; all remain `m^2` fixed points with monodromy `0`.

Where it fails:

* This does not yet rule out active grammars that use one extra old quotient bit.
* It also does not yet rule out predecessor-tail information or a slightly richer finite transducer state.
* So it kills the context-only family, but not the next minimal enriched family.

Attempt B:
Idea:
Use the family counts to locate the real obstruction stage.

What works:

* The bundle shows the obstruction is subtler than “Latin immediately forbids context dependence.”
* In several families, context-dependent tables survive the preliminary color-0 Latin filter in large numbers.
* But after clean-frame / first-return testing, all surviving rules collapse to constant anchor pairs.
* So the actual barrier in this branch is:
  **context dependence does not survive clean-frame compatibility**, not merely the first local Latin prefilter.
* This is the key update for the next search design:
  the next family should be optimized first for the existence of a context-dependent clean survivor, before worrying about `U_0`.

Where it fails:

* The current artifact does not identify which extra local bit is best suited to break the clean-frame rigidity.
* So the next step is still a search problem, but a much narrower one than before.

Candidate lemmas:

* [C] In the exact strict-friendly context-only two-anchor family driven by `(\text{phase\_align},b_1,b_2)`, there are no context-dependent clean survivors on `m=5,7,9`.
* [C] The only unique full survivors in that family are the `16` constant anchor pairs
  [
  (a,b)\in{0,2,3,4}^2.
  ]
* [C] All `16` constant pairs are full-color Latin, clean-frame, and strict-clock on `m=5,7,9`.
* [C] All `16` constant pairs are `U_0`-trivial: exactly `m^2` fixed points and monodromy `0`.
* [C/H] The preliminary color-0 Latin filter is not the decisive obstruction; the decisive obstruction in this branch is the clean-frame stage, which eliminates all context dependence.
* [H] Therefore the next minimal credible family is not “more tail-only contexts,” but “one extra old quotient bit on top of ((\text{phase_align},b_1,b_2)).”
* [H] The next search objective should be lexicographic:

  1. find any context-dependent clean survivor,
  2. then preserve strict clock,
  3. then seek nontrivial `U_0`.
* [F] Dependence on `(\text{phase\_align},b_1,b_2)` alone is sufficient to create a nonconstant clean tail grammar in the strict-friendly two-anchor family.
* [F] Changing strict-friendly anchor values alone can make `U_0` nontrivial.

Needed computations/search:

* Identify the nonredundant old atom bits already present in the current quotient signature.

  * Most plausible candidates are the existing low-bit atoms not already encoded by the current `phase_align` branch; in the prior notes these include the `wu2`-type atoms.
* For each such old bit `s`, search the smallest enriched active family where layer-2/3 output depends on
  [
  (\text{phase_align}, b_1, b_2, s).
  ]
* Use strict-friendly two-anchor palettes first:

  * layer `2`: seed anchor `2` versus alternate `a\in\{0,2,3,4\}`
  * layer `3`: seed anchor `3` versus alternate `b\in\{0,2,3,4\}`
* Natural staged search:

  1. one-layer-active families `(a,3)` and `(2,b)`,
  2. then full two-layer families `(a,b)`.
* For each family, record:

  * color-0 Latin survivors
  * clean survivors
  * strict survivors
  * context-dependent clean survivors
  * nontrivial-`U_0` witnesses
* If every one-old-bit family still has zero context-dependent clean survivors, the next branch should be:

  * predecessor-tail + old-bit hybrid contexts, or
  * a small finite transducer state rather than a pure Boolean refinement.

Next branching options:

1. Main branch:
   add one nonredundant old quotient bit to the active grammar and search for the first context-dependent clean survivor.
2. Secondary branch:
   if that fails, enrich the grammar with predecessor-tail information as well.
3. Side theorem branch:
   prove a clean-frame rigidity theorem for all context-only two-anchor grammars based on `(\text{phase\_align},b_1,b_2)`.

Claim status labels:
[P] [C] [H] [F] [O]

The sharpest update is:
the strict-friendly context-only branch did **not** fail because anchor choices were too narrow; it failed because any dependence on `(\text{phase_align},b_1,b_2)` gets wiped out at the clean-frame stage. The next honest move is therefore one extra old quotient bit, with “context-dependent clean survivor” as the first target.
