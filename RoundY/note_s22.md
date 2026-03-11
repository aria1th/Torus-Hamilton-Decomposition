Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining dynamical degeneracy after the tail-bit refinements.

Current target:
Absorb the Session 22 result and choose the smallest credible next active family. The immediate question is no longer “can `(b1,b2)` be used actively at all?” but “what extra local freedom is minimally needed for context dependence to survive Latin and affect `U_0`?”

Known assumptions:

* From the uploaded `D5-ACTIVE-U0-MERGE-003` bundle:

  * the searched family had

    * layer `0` anchor fixed to `1`
    * layer `1` anchor fixed to `4`
    * layer `4+` anchor fixed to `0`
    * layer `2` nonzero branch chosen from `{2,1}` by `ctx=2*b1+b2`
    * layer `3` nonzero branch chosen from `{3,1}` by the same `ctx`
    * phase-aligned branches fixed at seed anchors `2,3`
  * exact search size: `256`
  * `Latin + clean_frame` survivors: `1`
  * `Latin + clean_frame + strict_clock` survivors: `1`
  * unique survivor = strict-clock seed itself:

    * layer `2` always anchor `2`
    * layer `3` always anchor `3`
  * for that survivor, on `m=5,7,9`, `U_0` has `m^2` fixed points and monodromy `0`
* I also ran one exact extension locally in this session:

  * allow the phase-aligned branch to vary too, so the active context is
    [
    (\mathbf 1_{\delta=0}, b_1,b_2)
    ]
    with five effective cases: `phase_align`, `00`, `01`, `10`, `11`
  * keep the same two-anchor palette:

    * layer `2` chooses from `{2,1}`
    * layer `3` chooses from `{3,1}`
  * this gives `2^10 = 1024` rules
* Exact outcome of that 1024-rule extension:

  * only `4` rules survive Latin on `m=5,7,9`
  * those `4` are exactly the context-independent constant tables:

    * layer `2` constant `2`, layer `3` constant `3`
    * layer `2` constant `2`, layer `3` constant `1`
    * layer `2` constant `1`, layer `3` constant `3`
    * layer `2` constant `1`, layer `3` constant `1`
  * all `4` have `clean_frame=True`
  * only the seed `(2,3)` has `strict_clock=True`
  * all `4` still have trivial `U_0` dynamics: `m^2` fixed points, monodromy `0`
* I also checked all `25` constant anchor pairs `(a,b)` for layers `(2,3)` with `a,b\in\mathbb Z_5`:

  * all `25` are Latin and clean on `m=5,7,9`
  * `strict_clock` fails exactly when `a=1` or `b=1`
  * all `25` have trivial `U_0`

Attempt A:
Idea:
Read Session 22 as an exact no-go for the smallest active two-bit family around the strict-clock seed.

What works:

* This is now stronger than “no nontrivial `U_0` was found.”
* In the 256-rule family from the bundle, every non-seed rule already dies before return-dynamics analysis: the only `Latin + clean_frame` survivor is the seed.
* So the searched `(b1,b2)`-only family is not merely dynamically weak; it is locally rigid.

Where it fails:

* That no-go only covers the family with phase-aligned branches frozen at seed anchors and with alternate anchor `1`.
* It does not yet rule out:

  * phase-align-active tables,
  * alternate anchors other than `1`,
  * dependence on old atom bits or predecessor-tail bits.

Attempt B:
Idea:
Test the natural next extension: let the phase-aligned branch vary too, but still keep the smallest two-anchor palette `{2,1}` / `{3,1}`.

What works:

* I ran that exact 1024-rule extension.
* Result: any genuine dependence on `(phase_align,b1,b2)` is killed by Latin in this palette.
* The only Latin survivors are the four context-independent constant tables.
* So hidden tail context by itself does not survive into the output grammar when the palette is “seed versus 1.”
* This is sharper than the bundle no-go, because it shows the obstruction is not just “frozen phase-align branch”; it is the whole seed/1 context-dependent palette.

Where it fails:

* It still leaves open two meaningful directions:

  1. context dependence with a strict-friendly alternate anchor `a\neq 1`, `b\neq 1`;
  2. context dependence that also uses one old atom bit, so Latin can discriminate states more finely.

Candidate lemmas:

* [C] In the Session 22 256-rule family, the unique `Latin + clean_frame` survivor on `m=5,7,9` is the strict-clock seed itself.
* [C] In the phase-align-activated 1024-rule family with layer-2 palette `{2,1}` and layer-3 palette `{3,1}`, the only Latin survivors are the four context-independent constant tables.
* [C] All four survivors of that 1024-rule family have trivial `U_0`; only the seed `(2,3)` is strict-clock.
* [C] For constant layer-2/3 anchors `(a,b)`, all `25` pairs are Latin and clean on `m=5,7,9`, and strict clock fails exactly when `a=1` or `b=1`.
* [H] The obstruction in the current branch is not the choice of anchor values alone; it is the failure of context dependence to survive Latin.
* [H] The smallest credible next branch is therefore:

  * either keep context-only dependence but move to strict-friendly alternate anchors `a,b\neq 1`,
  * or keep the seed palette small and add one old atom bit to the output grammar.
* [F] Tail-context dependence using only `(phase_align,b1,b2)` and the seed/1 palette can produce nontrivial `U_0`.
* [F] The smallest active `(b1,b2)` neighborhood around the seed is sufficient.

Needed computations/search:

* Exact next search:

  * contexts = `phase_align`, `00`, `01`, `10`, `11`
  * layer `2` chooses between seed anchor `2` and alternate anchor `a`
  * layer `3` chooses between seed anchor `3` and alternate anchor `b`
  * restrict to strict-friendly alternates
    [
    a,b \in {0,2,3,4}
    ]
  * search all `16` choices of `(a,b)`, with `1024` tables each
* For each `(a,b)` family:

  1. count Latin survivors
  2. count clean survivors
  3. count strict survivors
  4. test for nontrivial `U_0`
* If all such context-only strict-friendly families still collapse to constant tables or trivial `U_0`, then move to:

  * one-extra-atom families where layer-2/3 output depends on
    [
    (phase_align,b_1,b_2,s)
    ]
    for a single old atom bit `s` from the existing low-bit vocabulary.

Next branching options:

* Main branch:
  exhaustive search of the 5-context strict-friendly two-anchor families.
* Second branch:
  if context-only strict-friendly palettes still fail, add one old atom bit to the active grammar.
* Side no-go branch:
  prove a structural theorem that any context-only two-anchor layer-2/3 grammar is Latin-rigid or `U_0`-trivial.

Claim status labels:
[P] exact phase-align-activated seed/1-palette no-go on `m=5,7,9`
[C] Session 22 minimal active family has unique strict survivor = seed
[C] constant anchor pairs are all Latin+clean and always `U_0`-trivial
[H] next credible constructive branch is strict-friendly alternate anchors, then one-old-bit augmentation
[F] `(phase_align,b1,b2)`-only dependence with seed/1 palette can produce nontrivial `U_0`
[O] full Hamilton decomposition remains open

My read of the frontier:
The new fact is not just “the 256-rule family failed.” It is stronger:

**within the seed/1 palette, any real dependence on hidden tail context is already forbidden by Latin.**

So the next honest step is to test whether context dependence can survive at all with strict-friendly alternate anchors; if not, then the grammar needs one extra old atom.
