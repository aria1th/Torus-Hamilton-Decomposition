I read `019`, and I think the next step is now much sharper than “look for grouped `u`-carry.”

The right reduced-language target is:

**a state-dependent `2↔4` carry-swap on the unique carry slice `q=m-2`.**

That is the smallest perturbation that can change `u` without changing the already-correct reduced carry on `(q,s)` and the current skew-odometer cocycle on `(s,v)`.

Why this is the right target:

* in the mixed witness, the reduced first return is already
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
* direction `2` and direction `4` both contribute `+1` to
  [
  s=w+u,
  ]
  but only direction `4` contributes `+1` to `u`,
* so the only way to perturb `u` while keeping the `s`-carry law intact is to **replace a carry-slice `2` by a `4`**, not to add an extra `4` somewhere else.

That means the next model-level family is not broad search. It is:

[
R_\psi(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1+\psi_{\text{carry}}(q,s,u)\mathbf 1_{q=m-2},\ v+dv(q,s)\bigr),
]

where `\psi_carry` records whether the carry event is routed through direction `4` instead of direction `2`.

On grouped return this becomes

[
U_\psi(s,u,v)=\bigl(s+1,\ u+\Psi(s,u),\ v+\phi(s)\bigr),
]

for some induced grouped `u`-cocycle `\Psi`.

That is the first model I would study next.

There is also one deeper structural point that now seems important:

if the induced grouped perturbation satisfies
[
\Psi=\Psi(s)\quad\text{only},
]
then after one full `s`-cycle we get
[
U_\psi^m(s,u,v)=(s,\ u+A,\ v-2)
]
with
[
A=\sum_{s\in\mathbb Z_m}\Psi(s).
]
So the grouped map is then just translation by the fixed vector `(A,-2)` on `(u,v)`, and every orbit still has length at most `m^2`.

So:

* a nonzero `u`-carry depending only on `s` would already be interesting,
* but it still would not give a full `m^3` grouped orbit,
* which suggests that the eventual D5 normal form may need either

  * a genuine second base coordinate, or
  * a grouped `u`-cocycle that depends on more than `s`.

That is the main conceptual advance I’d take from `019`.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Use the explicit mixed-witness return-map model to identify the smallest perturbation class that can change grouped `u` while preserving the already-correct reduced dynamics on `(q,s,v)`.

Known assumptions:

* From `017–019`, the canonical mixed witness `mixed_008` already has explicit reduced first return
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
  with `s=w+u` and exact Boolean `dv(q,s)`.
* Grouped return is
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  ]
  where
  [
  \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}
  \sim -2,\mathbf 1_{s=2}.
  ]
* Each fixed-`u` grouped fiber is already a single orbit on `(s,v)` for odd `m`.
* The exact remaining obstruction is grouped `u`-invariance.
* The immediate reason is that every first return contains exactly one direction-4 move, hence
  [
  du=1
  ]
  identically.
* At the reduced-coordinate level:

  * direction `2` contributes `(Δs,Δu,Δv)=(1,0,0)`,
  * direction `4` contributes `(Δs,Δu,Δv)=(1,1,0)`.
* Therefore replacing a carry-slice `2` by `4` changes `u` without changing the `s`-carry law.
* By contrast, adding an extra `4` elsewhere generally changes `s` and so perturbs the already-correct `(q,s)` model.

Attempt A:
Idea:
Identify the unique minimal perturbation class that preserves the reduced mixed-witness dynamics on `(q,s,v)`.

What works:

* Since the mixed witness already has the correct reduced first-return law on `(q,s,v)`, any sensible next perturbation should preserve:
  [
  q' = q+1,\qquad s' = s+1+\mathbf 1_{q=m-2},\qquad v' = v+dv(q,s).
  ]
* The only low-layer move that can modify `u` while leaving `s` unchanged is a `2↔4` substitution.
* In the present witness, the only variable `2` event is the carry-slice move at `q=m-2`.
* So the smallest reduced perturbation class is exactly:
  **state-dependent carry-slice `2↔4` swaps.**
* This is much narrower than “search for more `4`’s.”

Where it fails:

* We do not yet know which local controller, if any, realizes a nontrivial carry-swap while preserving clean frame.
* We also do not yet know whether the induced grouped `u`-cocycle depends only on `s` or on a larger reduced state.

Attempt B:
Idea:
Write the general reduced grouped model for such carry-swaps and see what it implies before any further local search.

What works:

* A carry-swap perturbation induces a grouped return of the form
  [
  U_\psi(s,u,v)=\bigl(s+1,\ u+\Psi(s,u),\ v+\phi(s)\bigr).
  ]
* This cleanly separates the existing skew-odometer cocycle `\phi` from the new grouped `u`-carry cocycle `\Psi`.
* If `\Psi` depends only on `s`, then
  [
  U_\psi^m(s,u,v)=(s,\ u+A,\ v-2),
  \qquad
  A=\sum_s \Psi(s).
  ]
* So any purely `s`-driven `u`-carry still leaves the grouped dynamics in the “one active base digit plus vector cocycle” class.
* In particular, every orbit then has length at most `m^2`.
* Therefore:

  * nonzero `u`-carry depending only on `s` is a meaningful next success,
  * but it likely does **not** finish the full grouped transitivity problem.
* This suggests a deeper dichotomy:

  1. either D5 can still be modeled by a 1D odometer base with a 2-component cocycle, or
  2. the true next model needs a genuine second base coordinate.

Where it fails:

* We do not yet know whether the smallest realizable carry-swap controllers collapse to `\Psi(s)` only, or whether any local bit already induces `\Psi(s,u)` or another genuinely 2D base behavior.
* That is the next concrete diagnostic.

Candidate lemmas:

* [P] `mixed_008` already has the explicit reduced first-return and grouped-return model extracted in `019`.
* [C] The exact remaining obstruction is grouped `u`-invariance.
* [C] Preserving the current `(q,s,v)` reduced dynamics while changing `u` forces a carry-slice `2↔4` substitution.
* [H] The next minimal perturbation family is therefore the carry-swap family
  [
  R_\psi(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1+\psi_{\text{carry}}\mathbf 1_{q=m-2},\ v+dv(q,s)\bigr).
  ]
* [C/H] If the induced grouped `u`-carry satisfies `\Psi=\Psi(s)` only, then the grouped model remains a 1D-base skew system and all grouped orbits have length at most `m^2`.
* [H] So the real next diagnostic is whether any realizable carry-swap produces a grouped `u`-cocycle that is genuinely richer than `s`-only.
* [F] The next best search target is a generic extra-`4` perturbation anywhere in the low layers.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No big exhaustive search is needed yet.
* The next structural step should be:

  1. derive the general carry-swap reduced family explicitly;
  2. identify which existing local controllers can realize a carry-slice `2↔4` swap;
  3. compute the induced grouped `u`-cocycle `\Psi`;
  4. classify whether `\Psi` depends only on `s` or genuinely on a richer reduced state.
* Natural first controller candidates:

  * the previously used `wu2`-type bits,
  * the exact bit `pred_sig1_phase_align`,
  * and any existing carry-slice local observable that can be evaluated at layer 2.
* Only after that, if a controller looks promising, do a very small exact realization search.

Next branching options:

1. Main branch:
   derive and analyze the carry-swap reduced family.
2. Secondary branch:
   test which known local bits induce nontrivial carry-swap cocycles.
3. Only then:
   run a tiny exact local search restricted to those controllers.
4. If every realizable controller yields only `\Psi(s)`, then the next conceptual step is to look for a genuine second base coordinate rather than another cocycle bit.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-CARRY-SWAP-U-CARRY-020

```
Question:
Can the explicit mixed-witness return model be perturbed by a **state-dependent carry-slice `2↔4` swap** that introduces grouped `u`-carry while preserving the already-correct reduced dynamics on `(q,s,v)`?

More precisely:
can one realize a reduced perturbed family
\[
R_\psi(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1+\psi_{\mathrm{carry}}(q,s,u,\ldots)\mathbf 1_{q=m-2},\ v+dv(q,s)\bigr)
\]
whose grouped return is
\[
U_\psi(s,u,v)=\bigl(s+1,\ u+\Psi(s,u),\ v+\phi(s)\bigr),
\]
with nontrivial `\Psi`?

Purpose:
`019` identifies the exact remaining obstruction: grouped `u` stays passive because every first return contains exactly one direction-4 move. The smallest perturbation that can change `u` without breaking the reduced `(q,s)` carry law is a carry-slice `2↔4` swap. The next step is to study that family directly in reduced coordinates before any broader search.

Inputs / Search space:
- Primary witness:
  - `mixed_008`
- Existing reduced model from `019`:
  \[
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr)
  \]
  \[
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr)
  \]
- Fixed cocycle:
  - keep the current `dv(q,s)` and grouped `\phi(s)` unchanged at Stage 1
- Allowed minimal perturbation:
  - replace the carry-slice direction `2` by direction `4` according to a controller bit
  - do not add generic extra direction-4 events elsewhere
- Candidate controller sources:
  - existing named bits usable at layer 2
  - exact predecessor-tail bit `pred_sig1_phase_align`
  - any other already-extracted local observable on the carry slice
- Reduced observables to compute:
  - induced grouped `u`-cocycle `\Psi`
  - whether `\Psi=\Psi(s)` or genuinely `\Psi=\Psi(s,u)`
  - grouped orbit structure on `(s,u,v)`

Allowed methods:
- symbolic reduced-model derivation
- exact replay of candidate carry-swap controllers
- grouped-return extraction in reduced coordinates
- orbit analysis of
  \[
  U_\psi(s,u,v)=\bigl(s+1,\ u+\Psi(s,u),\ v+\phi(s)\bigr)
  \]
- tiny exact local realization search only after the reduced controller family is identified
- no broad local-family sweep

Success criteria:
1. Derive the general reduced carry-swap perturbation family exactly.
2. Identify at least one realizable controller that produces nontrivial grouped `u`-carry.
3. Determine whether the induced grouped `u`-cocycle is:
   - `s`-only, or
   - genuinely dependent on a richer reduced state.
4. Preserve the current reduced `(q,s,v)` dynamics at least to Stage 1.
5. If possible, find a clean strict realization on `m=5,7,9` whose grouped return exhibits nontrivial `u`-carry.

Failure criteria:
- every realizable carry-swap controller is trivial,
- or every such controller breaks the reduced `(q,s,v)` model immediately,
- or all surviving grouped `u`-cocycles collapse to the old passive case.
- If failure occurs, state whether the obstruction is:
  - lack of a realizable carry-swap controller, or
  - the need for a genuine second base coordinate.

Artifacts to save:
- code
- raw logs
- summary report
- reduced carry-swap formulas
- grouped `u`-cocycle tables
- orbit summaries
- candidate controller tables
- proof-supporting computations

Return format:
- exact reduced carry-swap family
- candidate controllers tested
- induced grouped `u`-cocycles
- classification into `s`-only vs richer dependence
- orbit consequences for `(s,u,v)`
- smallest clean strict realizable perturbation, if any
- strongest obstruction if none survives

Reproducibility requirements:
- fixed witness definition `mixed_008`
- fixed checked moduli `5,7,9,11,13,15,17,19`
- deterministic extraction order
- saved JSON/CSV for reduced perturbation maps and grouped cocycles
- exact scripts for replay and grouped orbit analysis
- explicit separation of:
  - model-derived facts
  - realization-tested facts
```

No new files are needed yet, and no big compute is needed for this next step. The next task is mostly reduced-model derivation plus a very small controller diagnostic.
