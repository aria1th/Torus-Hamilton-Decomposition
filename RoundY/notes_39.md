Here is the current picture:

The mixed witness is now reduced enough that the remaining obstruction is no longer mysterious.
It is **not** “we still need a better cocycle.” The cocycle is already canonical up to gauge.
It is **not** “we still need a better base odometer.” The base is already there.

The remaining issue is:

[
U(s,u,v)=(s+1,\ u,\ v+\phi(s)),
]

so the grouped return is already transitive on each fixed-`u` fiber, but it does **not** couple different `u`-fibers.
Equivalently: in the mixed witness, each first return has exactly one direction-4 move, so

[
du=1
]

on every first return, hence grouped return leaves `u` invariant mod `m`.

That gives a very concrete next target: **find the smallest mechanism that creates state-dependent extra direction-4 events without destroying the `(q,s)` carry system and the skew-odometer on `(s,v)`**.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Promote the mixed witness to an explicit D5 return-map model, and reformulate the next search as:

**break grouped `u`-invariance while preserving the reduced carry/skew-odometer structure.**

Known assumptions:

* From `017` and `018`, for the canonical mixed witness `mixed_008`:

  * first return reduces exactly to
    [
    (q,s),\qquad s=w+u \pmod m,
    ]
  * grouped return reduces exactly to
    [
    s=w+u \pmod m,
    ]
  * and on the checked moduli `m=5,7,9,11,13` with direct replay extended to `15,17,19`,
    [
    R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr),
    ]
    [
    dv(q,s)=1 \iff \bigl(q\neq m-2 \land s=1\bigr)\ \text{or}\ \bigl(q=m-2 \land s\neq 0\bigr),
    ]
    [
    \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}\pmod m.
    ]
* The cocycle is cohomologous to the one-defect form
  [
  -2,\mathbf 1_{s=2}.
  ]
* On each fixed `u`, the grouped return on `(s,v)` is therefore a single orbit of length `m^2` for odd `m`, since the cycle sum is `m-2 ≡ -2`.
* From direct derivation from the `mixed_008` rule payload:

  * layer `0` contributes direction `1`,
  * layer `1` contributes direction `4`,
  * layer `2` contributes direction `2` iff `q=m-2`, else `0`,
  * layer `3` contributes direction `3` exactly when
    [
    (q\neq m-2 \land s=1)\ \text{or}\ (q=m-2 \land s\neq 0),
    ]
    else `0`,
  * all remaining steps are direction `0`.
* Therefore the mixed witness first-return low-layer word is exactly
  [
  (1,\ 4,\ 2\mathbf 1_{q=m-2},\ 3,dv(q,s)),
  ]
  and in particular **contains exactly one direction-4 move on every first return**.
* Hence
  [
  u' = u+1
  ]
  on every first return, so grouped return leaves `u` invariant.

Attempt A:
Idea:
Derive the reduced first return directly from the `mixed_008` witness rule, rather than only from quotient tables.

What works:

* Write the section state as
  [
  x=\bigl(-q-w-v-u,\ q,\ w,\ v,\ u\bigr)\pmod m.
  ]
* For color `0`, the `mixed_008` rule is:

  * layer `0`: anchor `1`,
  * layer `1`: anchor `4`,
  * layer `2`: anchor `0/2` depending on `q=-1`,
  * layer `3`: anchor `0/3` or `3/0` depending on the predecessor `wu2` flag and again on `q=-1`,
  * layer `4+`: anchor `0`.
* Reading these four low layers directly gives:

  1. step 1 increments `q`,
  2. step 2 increments `u`,
  3. step 3 increments `w` iff `q=m-2`,
  4. step 4 increments `v` exactly on the Boolean condition above.
* Hence
  [
  q' = q+1,\qquad
  w' = w+\mathbf 1_{q=m-2},\qquad
  u' = u+1,\qquad
  v' = v+dv(q,s),
  ]
  and with `s=w+u`,
  [
  s' = s+1+\mathbf 1_{q=m-2}.
  ]
* This is the first genuinely rule-derived D5 carry system.

Where it fails:

* I have not yet written it up as a formal proof note with every coordinate check expanded.
* But the derivation is now straightforward and no longer depends on guessing the quotient.

Attempt B:
Idea:
Use the explicit first-return word to isolate the exact remaining obstruction.

What works:

* Because the first-return word is
  [
  (1,\ 4,\ 2\mathbf 1_{q=m-2},\ 3,dv(q,s)),
  ]
  there is exactly one direction-4 event per return.
* Therefore
  [
  du=1
  ]
  identically, so after grouping `m` returns,
  [
  u \mapsto u+m = u \pmod m.
  ]
* This explains the whole current baseline:
  [
  U(s,u,v)=(s+1,\ u,\ v+\phi(s)).
  ]
* The grouped dynamics are already canonical on `(s,v)` and completely passive on `u`.
* So the next missing ingredient is no longer abstract. It is:
  **state-dependent extra `4`-moves (or an equivalent grouped `u`-carry mechanism).**

Where it fails:

* We do not yet know the smallest local perturbation that introduces grouped `u`-carry while preserving the `(q,s)` carry system and the skew cocycle.
* The existing controls suggest such perturbations are easy to make destructively, but not yet in a controlled way.

Candidate lemmas:

* [P] For `mixed_008`, the reduced first return is exactly
  [
  (q,s,u,v)\mapsto \bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr)
  ]
  with `dv(q,s)` as above.
* [P] For `mixed_008`, the grouped return is exactly
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  \qquad
  \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}.
  ]
* [P] The cocycle is cohomologous to the pure one-defect form
  [
  -2,\mathbf 1_{s=2}.
  ]
* [C] Each fixed-`u` grouped fiber is a single orbit on `(s,v)` for odd `m`.
* [C] The only passive grouped coordinate in the mixed witness is `u`.
* [C] The immediate reason for grouped `u`-invariance is that every first return contains exactly one direction-4 move.
* [H] The next real task is not more quotient discovery, but identifying the smallest perturbation that creates state-dependent extra direction-4 events while preserving the reduced `(q,s)` carry system.
* [F] The main remaining difficulty is still “finding the right cocycle.”
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No big exhaustive search is needed right now.
* The next structural work is:

  1. write the direct derivation of the `mixed_008` first-return formula from the witness rule;
  2. derive the grouped cocycle formula symbolically from that reduced return;
  3. package the exact obstruction as:

     * the skew-odometer on `(s,v)` is already correct,
     * grouped `u`-carry is absent because `du=1` identically;
  4. analyze the control witnesses in the same language to identify where extra direction-4 events first appear and why they currently destroy the clean reduced model.
* Only after that should there be any targeted search, and its objective should be explicit:
  **introduce state-dependent extra direction-4 events without breaking the `(q,s)` carry system.**

Next branching options:

1. Main branch:
   theorem extraction for the mixed witness plus a formal “grouped `u`-invariance obstruction” statement.
2. Secondary branch:
   control diagnosis in the same reduced coordinates, aimed at locating the first appearance of extra direction-4 events.
3. Only then:
   a tiny targeted perturbation search whose success criterion is
   “break grouped `u`-invariance while preserving the `(q,s)` carry and the one-defect skew cocycle.”

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-U-CARRY-MECHANISM-020

```
Question:
What is the smallest perturbation of `mixed_008` that can introduce grouped `u`-carry — equivalently, state-dependent extra direction-4 events in first return — while preserving the reduced carry system on `(q,s)` and the one-defect skew-odometer on `(s,v)`?

Purpose:
`017` and `018` identify the D5 mixed witness normal form, and the current remaining obstruction is now explicit: the grouped return is canonical on `(s,v)` but leaves `u` invariant. The next progress should therefore target the mechanism of `u`-carry directly, not another broad local-family search.

Inputs / Search space:
- Primary witness:
  - `mixed_008`
- Controls:
  - `cycle_007`
  - `monodromy_008`
  - `anti_mixed_010`
- Existing exact artifacts:
  - `017`
  - `018`
- Reduced coordinates:
  \[
  (q,s,u,v),\qquad s=w+u
  \]
- Known reduced formulas for `mixed_008`:
  \[
  q' = q+1,\qquad
  s' = s+1+\mathbf 1_{q=m-2},\qquad
  u' = u+1,\qquad
  v' = v+dv(q,s)
  \]
- Low-layer word for `mixed_008`:
  \[
  (1,\ 4,\ 2\mathbf 1_{q=m-2},\ 3\,dv(q,s))
  \]
- Pilot moduli:
  - `m in {5,7,9,11,13}`
- Stability moduli:
  - `m in {15,17,19}` if needed

Allowed methods:
- exact replay of the mixed and control witnesses
- extraction of first-return direction-count vectors
- extraction of where direction `4` occurs beyond the fixed layer-1 step
- grouped-return reduction in the same `(q,s,u,v)` language
- comparison of control witnesses to isolate the first appearance of extra `4`-moves
- very small targeted perturbation search only if a concrete candidate mechanism is identified
- no broad local-family sweep

Success criteria:
1. Prove directly that in `mixed_008`, each first return has exactly one direction-4 move.
2. Express grouped `u`-invariance as a precise obstruction statement.
3. Identify, in the control witnesses, the smallest local event or rule change that creates additional direction-4 contribution.
4. Determine whether any such event can coexist with the reduced `(q,s)` carry system and the skew cocycle on `(s,v)`.
5. If yes, formulate the smallest targeted perturbation family that tests exactly that mechanism.
6. If no, state the sharpest supported no-go for the current local neighborhood.

Failure criteria:
- the control analysis does not isolate any coherent extra-`4` mechanism,
- or every candidate extra-`4` mechanism necessarily destroys the reduced `(q,s)` carry system,
- or the apparent obstruction is shown not to be equivalent to grouped `u`-invariance.
- If failure occurs, identify the next missing grouped-return coordinate or mechanism.

Artifacts to save:
- code
- raw logs
- summary report
- direction-count tables per first-return state
- grouped `u`-carry tables
- control-comparison tables in reduced coordinates
- candidate perturbation tables
- proof-supporting computations

Return format:
- exact reduced coordinates used
- proof that `mixed_008` has exactly one direction-4 event per first return
- grouped `u`-invariance obstruction statement
- control diagnosis of extra-`4` mechanisms
- smallest plausible targeted perturbation family, if one emerges
- strongest supported conclusion if no such family survives

Reproducibility requirements:
- fixed witness definitions
- fixed moduli `5,7,9,11,13,15,17,19`
- deterministic extraction order
- saved JSON/CSV for direction-count and grouped-carry tables
- exact scripts for replay and reduced-coordinate comparison
- explicit separation of:
  - theorem-derived facts for `mixed_008`
  - computation-derived control diagnosis
```

No additional files are needed for this next step. No big compute is needed either. The current `017` and `018` artifacts are enough to finish the normal-form extraction and to turn the next question into a very small, precise `u`-carry diagnosis.
