The summary is enough. I did not reopen the tar.

My main thought is:

**`020` already tells us what the next reduced-language object must be.**
Not another binary selector, and not even an arbitrary ternary profile in the abstract.

The next honest target is:

**a grouped adjacent transposition on `u` at fixed `s`.**

That is the smallest genuinely new base motion beyond the current one-dimensional skew-odometer.

Why I think this is the right reformulation:

* binary `{0,1}` updates are too weak, as `020` showed;
* a ternary `{-1,0,1}` update on `u` that is permutation-valid is not arbitrary;
* on the cycle graph, the only permutation cycles compatible with step set `{-1,0,1}` are:

  * fixed points,
  * adjacent 2-cycles,
  * or the full translation cycle `u\mapsto u\pm1`.

So the first nontrivial same-`s` mechanism is not “some ternary profile”; it is exactly a product of adjacent transpositions, with the smallest case being a **single adjacent swap**.

That leads to a much cleaner next-stage picture.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Replace “look for grouped `u`-carry” by the sharper reduced-language target:

**realize the smallest nontrivial grouped permutation on `u` while preserving the current reduced `(q,s,v)` structure.**

The smallest such grouped permutation is an **adjacent transposition** in `u` at fixed `s`.

Known assumptions:

* From `019`, the canonical mixed witness has reduced first return
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
  with
  [
  s=w+u.
  ]
* Grouped return is
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  ]
  with
  [
  \phi(s)\sim -2,\mathbf 1_{s=2}.
  ]
* The exact current obstruction is grouped `u`-invariance.
* From `020`, single binary carry-swaps induce grouped updates
  [
  U_\Psi(s,u,v)=\bigl(s+1,\ u+\Psi(s,u),\ v+\phi(s)\bigr),
  \qquad \Psi\in{0,1},
  ]
  and permutation-validity forces `\Psi` to be constant in `u` for each fixed `s`.
* Therefore binary grouped `u`-updates collapse to one-dimensional `s`-only cocycles.
* The natural second reduced coordinate remains
  [
  d=u-w=2u-s,
  ]
  so `(s,d)` is equivalent to `(w,u)` because `m` is odd.

Attempt A:
Idea:
Classify all permutation-valid same-`s` grouped `u`-updates with step set `\{-1,0,1\}`.

What works:

* For fixed `s`, write
  [
  f_s(u)=u+\eta_s(u),
  \qquad \eta_s(u)\in{-1,0,1}.
  ]
* This is a permutation of `\mathbb Z_m` only if its cycle decomposition lives in the cycle graph with loops.
* In that graph, the only possible permutation cycles are:

  1. loops (`u\mapsto u`);
  2. adjacent 2-cycles (`u\leftrightarrow u+1`);
  3. the full translation cycle (`u\mapsto u+1` or `u\mapsto u-1` on all of `\mathbb Z_m`).
* Therefore every nontranslation valid ternary profile is a product of disjoint adjacent transpositions and fixed points.
* This cleanly generalizes the binary obstruction from `020`.
* So the first genuinely new grouped base motion is not generic ternary behavior; it is an adjacent transposition.

Where it fails:

* This is a reduced-model classification, not yet a local realization theorem inside the D5 witness family.
* It does not yet say which local paired `2\leftrightarrow4` / `4\leftrightarrow2` mechanism realizes such a transposition.

Attempt B:
Idea:
Analyze the orbit consequences of such grouped `u`-permutations before doing any further local search.

What works:

* Suppose grouped return takes the form
  [
  U_f(s,u,v)=\bigl(s+1,\ f_s(u),\ v+\phi(s)\bigr),
  ]
  with `f_s` a permutation of `u`.
* Over one full `s`-cycle,
  [
  U_f^m(s,u,v)=\bigl(s,\ F(u),\ v-2\bigr),
  \qquad
  F=f_{m-1}\circ\cdots\circ f_0.
  ]
* If `u` lies in an `F`-cycle of length `L`, then because `-2` is invertible mod odd `m`, the orbit size under `U_f` on that block is
  [
  m\cdot \mathrm{lcm}(L,m).
  ]
* Consequences:

  * current mixed witness: `L=1`, orbit size `m^2`;
  * a single grouped adjacent transposition gives `L=2`, hence orbit size
    [
    2m^2
    ]
    for odd `m`;
  * more complicated products of adjacent transpositions can give larger `L`, hence larger grouped orbits.
* So a grouped adjacent transposition is already a real dynamical advance beyond the baseline.
* At the same time, as long as the grouped cocycle remains `\phi(s)` only, one is still in a constrained skew-product class:
  [
  U_f^m(s,u,v)=(s,F(u),v-2).
  ]
* So this next step would be a **true second grouped base coordinate**, but probably not yet the final D5 normal form.

Where it fails:

* We do not yet know whether the smallest locally realizable paired mechanism gives:

  * one adjacent transposition,
  * a translation,
  * or only the old trivial `u`-behavior.
* We also do not yet know whether any such realization preserves the current reduced `(q,s,v)` structure cleanly.

Candidate lemmas:

* [P] If
  [
  f(u)=u+\eta(u),\qquad \eta(u)\in{-1,0,1},
  ]
  is a permutation of `\mathbb Z_m`, then its cycle decomposition consists only of:

  * fixed points,
  * adjacent transpositions,
  * or the global translation cycle `u\mapsto u\pm1`.
* [C] Hence every nontranslation ternary same-`s` grouped update is a product of disjoint adjacent transpositions and fixed points.
* [C] The binary obstruction from `020` is the special case where adjacent transpositions cannot occur because the value `-1` is absent.
* [P] For grouped maps
  [
  U_f(s,u,v)=\bigl(s+1,f_s(u),v+\phi(s)\bigr),
  ]
  one has
  [
  U_f^m(s,u,v)=\bigl(s,F(u),v-2\bigr),
  \qquad
  F=f_{m-1}\circ\cdots\circ f_0.
  ]
* [P] If `u` lies in an `F`-cycle of length `L`, then the corresponding `U_f`-orbit length is
  [
  m\cdot \mathrm{lcm}(L,m).
  ]
* [H] The next smallest real target is therefore a locally realizable grouped adjacent transposition on `u`.
* [H] If such a transposition can be realized cleanly, then the D5 reduced model has genuinely left the one-dimensional base regime.
* [H] Even after that, the eventual full normal form may still need additional `u`-dependence in the grouped cocycle or a further grouped coordinate.
* [F] The next step should still be another binary selector search.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No big computation is needed right now.
* The right next work is theoretical and very small-scale:

  1. write up the exact classification of permutation-valid ternary `u`-updates;
  2. rewrite the grouped return in `(s,d,v)` coordinates with
     [
     d=2u-s;
     ]
  3. identify which local paired mechanisms could realize:

     * an adjacent transposition,
     * or a short product of adjacent transpositions,
       while preserving the reduced `(q,s,v)` dynamics;
  4. only then do a tiny exact realization test.
* The right local ingredients to inspect are now very specific:

  * same-`s` `2\to4` rerouting for `+1`,
  * same-`s` `4\to2` rerouting for `-1`,
  * paired on neighboring `u`-states so that the grouped slice map becomes an adjacent transposition rather than an invalid binary shift.

Next branching options:

1. Main branch:
   prove the ternary permutation classification and reframe the reduced model in terms of grouped `u`-permutations.
2. Secondary branch:
   identify the smallest locally plausible adjacent-transposition mechanism.
3. Then:
   run a tiny exact realization search for that specific grouped transposition family.
4. If no adjacent transposition is locally realizable:
   conclude that the next missing ingredient is not just a richer value range, but a different grouped coordinate or a less rigid preserved structure.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-GROUPED-U-TRANSPOSITION-021

```
Question:
Can the D5 mixed return-map model be perturbed so that, at grouped return, one `s`-slice acts by an **adjacent transposition** on `u` while preserving the existing reduced carry/skew-odometer structure on `(q,s,v)`?

More generally:
can one realize
\[
U_f(s,u,v)=\bigl(s+1,\ f_s(u),\ v+\phi(s)\bigr),
\]
where at least one slice map `f_s` is a nontrivial product of adjacent transpositions, rather than identity or translation?

Purpose:
`020` proved that binary grouped `u`-updates are too weak. The reduced-model classification shows that the first genuine new grouped base motion is an adjacent transposition. So the next exact local test should target that mechanism directly, instead of searching generic ternary families.

Inputs / Search space:
- Existing reduced mixed model from `019`
- Binary obstruction from `020`
- Reduced coordinates:
  \[
  s=w+u,\qquad d=u-w=2u-s
  \]
- Fixed grouped cocycle:
  \[
  \phi(s)\sim -2\,\mathbf 1_{s=2}
  \]
  held unchanged at Stage 1
- Candidate local ingredients:
  - same-`s` `2\to4` rerouting for relative `+1`
  - same-`s` `4\to2` rerouting for relative `-1`
  - paired use of existing current-state / predecessor bits as controllers
- Small target grouped slice maps:
  - one adjacent transposition
  - two disjoint adjacent transpositions
  - short products thereof
- Checked moduli:
  - `m in {5,7,9,11,13,15,17,19}`

Allowed methods:
- theorem-level classification of ternary permutation profiles
- reduced-model derivation in `(s,d,v)` coordinates
- tiny exact local realization tests for specific adjacent-transposition targets
- direct full-color Latin / clean-frame / strict-clock validation only for those tiny targets
- grouped orbit analysis via
  \[
  U_f^m(s,u,v)=\bigl(s,F(u),v-2\bigr)
  \]
- no broad local-family sweep

Success criteria:
1. Prove the ternary grouped `u`-permutation classification.
2. Identify the smallest locally plausible adjacent-transposition target.
3. Find a clean strict realization on `m=5,7,9` with grouped slice map nontrivial on `u`.
4. Show that the resulting grouped orbit size exceeds the baseline `m^2`.
5. Preserve the reduced `(q,s,v)` structure at least to first order.

Failure criteria:
- no adjacent transposition is locally realizable while preserving clean-frame,
- or every realizable paired mechanism collapses to identity/translation on `u`,
- or every nontrivial grouped `u`-permutation destroys the reduced mixed structure.
- If failure occurs, state clearly whether the next missing ingredient is:
  - a different grouped coordinate, or
  - relaxing the requirement that the existing `(q,s,v)` model remain unchanged.

Artifacts to save:
- code
- raw logs
- summary report
- ternary permutation-classification note
- grouped slice-map tables
- reduced `(s,d,v)` transition tables
- orbit-size tables
- validation outputs
- proof-supporting computations

Return format:
- exact ternary classification statement
- exact reduced `(s,d,v)` formulation
- target grouped slice maps tested
- smallest clean strict nontrivial realization, if any
- grouped orbit-size comparison with the baseline
- strongest obstruction if none survives

Reproducibility requirements:
- fixed reduced model from `019`
- fixed checked moduli `5,7,9,11,13,15,17,19`
- deterministic extraction order
- saved JSON/CSV for grouped slice maps and reduced transitions
- exact scripts for orbit analysis
- explicit separation of:
  - theorem-derived facts
  - realization-tested facts
```

The short strategic conclusion is:

**`020` did not just say “binary is too weak.”
It implicitly identified the next real object: grouped adjacent transpositions on `u`.**
That is the first nontrivial second-base motion compatible with the reduced D5 model, and it is the right thing to target next.
