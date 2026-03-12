The summary is sufficient, so I did not reopen the tar.

My main thought is that `025` finally turns the next step into a **very small local emulation problem**.

The best reformulation is not in `(s,u)` but in `(s,w)`.

Because
[
s=w+u,
]
the diagonal moving transposition along
[
u=s+b
]
is exactly the same as a **fixed adjacent transposition on the two `w`-values**
[
w_0=-b,\qquad w_0-1=-b-1.
]

So `025` is telling us that the next honest local target is:

* on grouped base: a fixed adjacent transposition on one adjacent `w`-pair,
* omitted on one row `s=s_0`,
* plus a one-point or two-point cocycle defect at an omitted-edge endpoint.

That is much smaller and cleaner than “search for another selector family.”

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Use `025` to stop broad selector exploration and move to the first genuinely targeted local realization problem:

**locally emulate the `025` reduced normal form, preferably in the diagonal branch rewritten as a fixed adjacent transposition on a `w`-pair, omitted on one `s`-row, with an edge-tied point cocycle defect.**

Known assumptions:

* I am taking your summary of `025` as sufficient for this turn; I did not reopen the tar.
* From `019`, the canonical mixed witness already has reduced first return
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
  and grouped return
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  \qquad
  \phi(s)\sim -2,\mathbf 1_{s=2}.
  ]
* From `021/022`, the standard one-bit paired family and the affine one-surface paired family do not produce a genuine 2D grouped base coordinate.
* From `023`, the first genuine 2D reduced grouped perturbation is the moving adjacent transposition along a diagonal or anti-diagonal
  [
  u=\pm s+b,
  ]
  giving grouped base orbit sizes `[m,\,m(m-1)]` and full grouped orbit sizes `[m^2,\,m^2(m-1)]`.
* From `025`, omitting one row of that moving transposition merges the grouped base into a **single orbit of size `m^2`**.
* Also from `025`, adding a one-point cocycle defect at either omitted-edge endpoint, or the two-point omitted-edge defect, yields a **single full grouped orbit of size `m^3`** on every checked odd
  [
  m=5,7,9,11,13,15,17,19.
  ]
* Row-sized and graph-sized cocycle defects fail because their total contribution over the unique base orbit is `0 mod m`.
* Therefore the reduced normal-form target is now explicit:
  [
  \text{omit-base} + \text{edge-tied point cocycle defect}.
  ]

Attempt A:
Idea:
Rewrite the diagonal `023/025` target in a stationary coordinate so the local realization problem is no longer “moving.”

What works:

* For the diagonal branch
  [
  u=s+b,
  ]
  one has
  [
  w=s-u=-b.
  ]
* So the moving adjacent transposition on the `u`-line
  [
  u=s+b \leftrightarrow s+b+1
  ]
  is exactly a **fixed adjacent transposition** on
  [
  w_0=-b,\qquad w_0-1=-b-1.
  ]
* In grouped `(s,w)` coordinates, the base map becomes
  [
  (s,w)\mapsto \bigl(s+1,\ \tau_{w_0-1,w_0}(w)+1\bigr),
  ]
  where `\tau_{a,b}` swaps `a` and `b`.
* The `025` omit-base target is then:

  * apply this fixed adjacent transposition on every row,
  * except on one omitted row `s=s_0`, where the swap is removed.
* This is much simpler than thinking in moving diagonal language.

Where it fails:

* This is a reduced-model equivalence, not yet a local realization.
* It does not yet tell us which raw first-return word changes realize the fixed `w`-pair transposition while preserving clean frame.

Attempt B:
Idea:
Derive the minimal raw local palette that would emulate the `025` reduced target around `mixed_008`.

What works:

* On the carry slice `q=m-2`, the baseline mixed witness has one low-layer carry word with relative grouped effect
  [
  (\Delta w,\Delta u)=(1,1).
  ]
* There are two natural same-`s` perturbations:

  * `2\to4` on the carry slot:
    [
    (\Delta w,\Delta u)=(0,2),
    ]
    i.e. relative `(+1)` in `u` and `(-1)` in `w`;
  * `4\to2` on the always-present layer-1 slot:
    [
    (\Delta w,\Delta u)=(2,0),
    ]
    i.e. relative `(-1)` in `u` and `(+1)` in `w`.
* So there is a natural 3-word local palette on the carry slice:

  * baseline `B`,
  * plus-shift `P`,
  * minus-shift `M`.
* Using `P` on one fixed `w` state and `M` on the adjacent fixed `w` state produces exactly the grouped adjacent transposition on the `w`-pair.
* Omitting this on one `s`-row gives the `025` base target.
* Then toggling the layer-3 `dv` contribution at one omitted-edge endpoint gives the one-point cocycle defect.
* This is the first local family that is directly derived from the reduced target, not from a generic selector ansatz.

Where it fails:

* We do not yet know whether clean-frame survives under this tiny targeted palette.
* We also do not yet know whether the point cocycle defect can be localized to exactly one omitted-edge endpoint without spilling into nearby states.
* So this is still the next exact search, not a theorem.

Candidate lemmas:

* [P] `025` gives an explicit reduced normal-form target: omit-base plus an edge-tied point cocycle defect yields a single grouped orbit of size `m^3` on all checked odd moduli.
* [C] In the diagonal branch, the moving adjacent transposition along `u=s+b` is equivalent to a fixed adjacent transposition on the `w`-pair
  [
  {w_0-1,w_0},\qquad w_0=-b.
  ]
* [C] The `025` base defect is therefore just “omit one application of a fixed adjacent transposition on row `s=s_0`.”
* [C] The successful cocycle defects in `025` are pointwise or omitted-edge two-point defects; row-sized and graph-sized defects fail because their total contribution over the unique base orbit is `0 mod m`.
* [H] The next smallest honest local branch is not another selector expansion, but a targeted `B/P/M` carry-slice palette search emulating the `025` reduced signature.
* [H] The diagonal branch should be prioritized over the anti-diagonal branch because it becomes stationary in `w`.
* [F] Another broad affine / one-surface / generic selector sweep is the right next main branch.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No broad computation is needed first.
* The next step should be a tiny exact local realization search, directly tied to the `025` reduced target.
* Priority reduced target:

  1. diagonal branch only;
  2. fixed adjacent `w`-pair ({w_0-1,w_0});
  3. omitted row `s=s_0`;
  4. one-point cocycle defect at one omitted-edge endpoint, with two-point omitted-edge defect as the control.
* Minimal raw local palette on the carry slice:

  * `B`: baseline carry word,
  * `P`: `2\to4` on the carry slot,
  * `M`: `4\to2` on the layer-1 slot.
* Target grouped effect:

  * use `P` on one of the two `w`-states,
  * use `M` on the adjacent `w`-state,
  * omit both on the single defect row `s_0`,
  * add the smallest layer-3 toggle at one omitted-edge endpoint.
* Primary verification:

  * clean frame,
  * strict clock,
  * grouped base orbit size `m^2`,
  * full grouped orbit size `m^3`,
  * reduced grouped signature matching the `025` target, at least on `m=5,7,9`, with `m=11` as the first control.

Next branching options:

1. Main branch:
   diagonal/fixed-`w` local emulation of the `025` reduced normal form.
2. Secondary branch:
   if diagonal/fixed-`w` fails, try the anti-diagonal branch in its stationary coordinate.
3. Only then:
   widen to a predecessor/non-affine micro-family around the same reduced target, not a generic selector family.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-FIXED-W-OMIT-DEFECT-026

```
Question:
Can the `025` reduced normal form be realized locally by a tiny perturbation of `mixed_008` that, on the carry slice, uses the 3-word palette

- baseline `B`,
- plus-shift `P` (`2\to4` on the carry slot),
- minus-shift `M` (`4\to2` on the layer-1 slot),

so as to emulate:

1. a fixed adjacent transposition on one adjacent `w`-pair,
2. omitted on one grouped row `s=s_0`,
3. together with a one-point or two-point omitted-edge cocycle defect?

Purpose:
`025` has already identified the correct reduced target. The next honest step is not a broad rule search, but a very small local realization search aimed specifically at that target. In the diagonal branch, the target is stationary in `w`, which makes it the cleanest first branch.

Inputs / Search space:
- Base witness:
  - `mixed_008`
- Fixed anchors outside the tiny perturbation:
  - keep the `mixed_008` rule unchanged unless explicitly modified below
- Reduced target from `025`:
  - grouped base: single orbit of size `m^2`
  - full grouped orbit: `m^3`
  - cocycle defect tied to omitted edge endpoint(s)
- Diagonal branch only at Stage 1:
  - choose `w_0 in Z_m`
  - active adjacent `w`-pair:
    \[
    \{w_0-1,\ w_0\}
    \]
  - choose omitted row `s_0 in Z_m`
- Carry-slice palette on `q=m-2`:
  - `B`: baseline mixed carry word
  - `P`: replace carry `2` by `4`
  - `M`: replace layer-1 `4` by `2`
- Stage 1 local rule:
  - on row `s\neq s_0`:
    - use `P` on one chosen `w`-state of the active pair,
    - use `M` on the other chosen `w`-state,
    - use `B` everywhere else;
  - on the omitted row `s=s_0`:
    - use `B` on both states of the active pair.
- Layer-3 cocycle defect:
  - Stage 1a: toggle at one omitted-edge endpoint
  - Stage 1b: toggle at the other endpoint
  - Stage 1c: toggle at both endpoints
- Primary moduli:
  - `m in {5,7,9}`
- First control modulus:
  - `m = 11`

Allowed methods:
- exact exhaustive enumeration over:
  - `w_0`
  - `s_0`
  - choice of which endpoint gets `P` and which gets `M`
  - point / two-point cocycle defect choice
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- grouped orbit extraction in reduced coordinates
- comparison against the exact `025` reduced signature
- no broad selector sweep
- no widening beyond the diagonal/fixed-`w` target unless the whole tiny family fails

Success criteria:
1. Find a clean strict local realization on `m=5,7,9`.
2. Recover grouped base orbit size `m^2`.
3. Recover full grouped orbit size `m^3`.
4. Match the `025` reduced signature up to the obvious relabelings/gauge choices.
5. Preferably persist at `m=11`.

Failure criteria:
- no clean strict survivor exists in the tiny `B/P/M` family, or
- grouped base fails to reach a single orbit of size `m^2`, or
- point/two-point cocycle defects fail to realize the `m^3` lift, or
- the realized grouped signature does not match the `025` target.
- If failure occurs, report whether the next widening should be:
  - anti-diagonal stationary-coordinate realization,
  - or a predecessor/non-affine micro-family around the same target.

Artifacts to save:
- code
- raw logs
- summary report
- grouped orbit tables
- reduced signature comparison tables
- validation outputs
- discovered realizations / counterexamples
- proof-supporting computations

Return format:
- exact `w_0` and `s_0` choices tested
- exact endpoint assignments `P/M`
- exact cocycle defect choices tested
- clean/strict survivor counts
- grouped base orbit sizes
- full grouped orbit sizes
- best matching realization of the `025` target, if any
- strongest obstruction if none survives

Reproducibility requirements:
- fixed base witness `mixed_008`
- fixed moduli `5,7,9,11`
- deterministic enumeration order
- saved JSON summaries for all tested parameter choices
- exact scripts for grouped reduction and orbit extraction
- explicit comparison against the `025` reduced target
```

The short strategic conclusion is:

**`025` already solved the reduced problem.
So the next honest move is not another discovery search; it is a tiny realization search for exactly that reduced signature.
And in the diagonal branch, that target is stationary: a fixed adjacent transposition on one `w`-pair, omitted on one row, plus an edge-tied point defect.**
