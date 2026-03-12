These results are enough to pivot cleanly.

My read is:

* `021` says the first paired `4↔2` family built from the standard one-bit atoms is still too weak.
* `022` says even the larger **single affine surface** paired family is still too weak, and more sharply, every valid pair avoids `u` entirely.
* `023` says the first honest reduced 2D perturbation is already known: a **moving adjacent transposition along a diagonal or anti-diagonal** `u = ±s + b`.

So the project is no longer asking “what kind of perturbation might work?”
It is asking a much sharper question:

**what is the smallest local mechanism whose grouped effect emulates the diagonal moving transposition from `023`, and then adds one controlled defect that breaks the residual invariant diagonal?**

There is one extra point I think is now crucial.

If we only merge the two base orbits from `023` into one base orbit of size `m^2`, but keep the old cocycle
[
\phi(s)
]
depending on `s` alone, then over one full base orbit the total cocycle is
[
m\sum_{s\in\mathbb Z_m}\phi(s)=m(m-2)\equiv 0 \pmod m.
]
So the `v`-lift would no longer contribute an extra factor `m`. In other words:

**a diagonal-breaking defect in the base alone is not enough.**
The defect must also create a genuinely 2D cocycle effect, or at least a cocycle defect that does not collapse over the merged base orbit.

That is the main new structural lesson from combining `019` and `023`.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Use the explicit reduced return model from `019` together with the negative local results `021/022` and the positive reduced perturbation `023` to define the next real branch:

**locally emulate the diagonal moving adjacent transposition from `023`, then add one controlled defect that both**

1. **breaks the residual invariant diagonal/anti-diagonal on the grouped base**, and
2. **prevents the cocycle from collapsing back to an `s`-only sum over the merged base orbit.**

Known assumptions:

* From `019`, the canonical mixed witness already has explicit reduced first return
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
  with
  [
  s=w+u,
  ]
  and grouped return
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  \qquad
  \phi(s)\sim -2,\mathbf 1_{s=2}.
  ]
* The present obstruction is grouped `u`-invariance.
* From `020`, single binary carry-swaps are too weak: every valid binary grouped `u`-update collapses to an `s`-only cocycle.
* From `021`, the first paired `4↔2` mechanism built from the standard one-bit atoms still gives no genuine 2D grouped base coordinate.
* From `022`, the larger affine one-surface paired family also gives no genuine 2D grouped base coordinate:

  * `93` selectors,
  * `8649` ordered pairs,
  * `900` valid pilot pairs at `m=11`,
  * `0` genuine 2D candidates,
  * every valid pair avoids `u` entirely.
* From `023`, the first genuine reduced 2D perturbation is the moving adjacent transposition along
  [
  u=\pm s+b.
  ]
  Across `m=5,7,9,11,13,15,17,19`, it gives:

  * grouped base orbit sizes
    [
    [m,\ m(m-1)],
    ]
  * full grouped orbit sizes on `(s,u,v)`
    [
    [m^2,\ m^2(m-1)].
    ]
* The residual obstruction in `023` is explicit:
  one invariant diagonal or anti-diagonal orbit remains, documented in `diagonal_orbit_samples.json`.

Attempt A:
Idea:
Treat `023` as the correct first 2D reduced target and stop looking for generic one-surface or one-bit selectors.

What works:

* `021` and `022` together now prune the whole obvious local selector neighborhood:
  standard one-bit atoms are too weak, and even single affine surfaces are too weak.
* `023` gives the first explicit 2D grouped-base model:
  [
  B_{\varepsilon,b}(s,u)=\bigl(s+1,\ \tau_{\varepsilon s+b}(u)\bigr),
  ]
  where `\tau_a` swaps `a` and `a+1`.
* This is already almost transitive on the grouped base: one orbit of size `m(m-1)` and one orbit of size `m`.
* So the next search should be formulated as **local emulation of this reduced model**, not as a blind expansion of selector catalogs.

Where it fails:

* `023` is still only a reduced perturbation family.
* It does not yet identify a locally realizable D5 mechanism that produces this grouped effect.

Attempt B:
Idea:
Combine the `023` base model with the `019` cocycle model to identify the true remaining obstruction.

What works:

* The old grouped cocycle is still
  [
  \phi(s)\sim -2,\mathbf 1_{s=2},
  ]
  depending only on `s`.
* On a grouped base orbit of size `km`, the total cocycle sum is
  [
  k\sum_s \phi(s)=k(m-2)\equiv -2k \pmod m.
  ]
* This explains the current orbit sizes:

  * small orbit: `k=1`, extra `v`-factor `m`;
  * large orbit: `k=m-1`, extra `v`-factor `m`;
  * hence `023` gives `[m^2, m^2(m-1)]`.
* But if a defect merged the two base orbits into a single base orbit of size `m^2` (`k=m`) **while keeping the old `s`-only cocycle**, then the total cocycle over one base orbit would be
  [
  -2m \equiv 0 \pmod m,
  ]
  so the `v`-lift would contribute no extra factor at all.
* Therefore the next target is not merely:
  “break the residual diagonal.”
* It is:
  **break the residual diagonal and simultaneously create a cocycle defect that is not `s`-only over the merged base orbit.**

Where it fails:

* We do not yet know the smallest local mechanism that realizes both effects together.
* But the reduced target is now explicit enough that the next search can be very narrow.

Candidate lemmas:

* [C] The paired one-bit family `021` and the affine one-surface family `022` both fail to produce a genuine 2D grouped base map.
* [C] In `022`, every valid affine pair avoids `u` entirely.
* [P] The first genuine 2D reduced grouped perturbation is the moving adjacent transposition family from `023` along
  [
  u=\pm s+b.
  ]
* [C] This family has grouped base orbit sizes `[m, m(m-1)]` and full grouped orbit sizes `[m^2, m^2(m-1)]`.
* [C] The residual small orbit is an explicit invariant diagonal or anti-diagonal.
* [H] The next smallest honest local target is a mechanism whose grouped effect emulates the diagonal moving transposition.
* [H] A base-only diagonal-breaking defect is not enough if the cocycle remains `s`-only; the defect must also create nontrivial second-coordinate cocycle behavior.
* [F] The next main branch should still be a larger one-surface or one-bit selector sweep.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No broad compute is justified yet.
* The next step should be split into two tightly focused stages.

1. **Reduced-model stage**

   * Define the reduced diagonal transposition family
     [
     B_{\varepsilon,b}(s,u)=\bigl(s+1,\ \tau_{\varepsilon s+b}(u)\bigr).
     ]
   * Add the smallest defect family:

     * row defect: shift the swapped edge on one chosen `s=s_0`,
     * omission defect: remove one row swap,
     * double-edge defect: add one adjacent second swap on one chosen row.
   * For each such base defect, compute:

     * grouped base orbit structure,
     * whether the invariant diagonal survives,
     * orbit lengths on `(s,u)`.

2. **Cocycle-defect stage**

   * On top of the base-defected family, add the smallest cocycle defect:
     [
     \phi(s,u)=\phi(s)+\kappa,\mathbf 1_{(s,u)\in D}
     ]
     for a tiny defect set `D` tied to the same diagonal mechanism.
   * Determine which defects produce:

     * a single grouped base orbit of size `m^2`,
     * and a nonzero total cocycle over that orbit, so that the full grouped orbit can exceed `m^2`.
   * This gives the reduced normal-form target that the local realization should emulate.

3. **Only after those reduced targets are classified**

   * build a tiny local emulation search:

     * non-affine or predecessor-style paired carry mechanism,
     * explicitly targeted at the chosen reduced diagonal defect model,
     * not a broad selector sweep.

Next branching options:

1. Main branch:
   classify one-defect diagonal/anti-diagonal transposition families at the reduced level, including cocycle defects.
2. Secondary branch:
   design the smallest non-affine or predecessor-style local paired mechanism that could emulate the best reduced target.
3. Only then:
   run a very small exact realization search on that targeted family.

Claim status labels:
[P] first genuine 2D reduced grouped-base model identified (`023`)
[C] standard one-bit and affine one-surface local families are now pruned (`021/022`)
[C] the residual obstruction in `023` is one invariant diagonal/anti-diagonal orbit
[H] the next target is a local emulation of the diagonal moving transposition, plus a cocycle-aware one-defect correction
[F] another broad selector expansion is the right next main branch
[O] full Hamilton decomposition remains open

Work Template:
Task ID:
D5-DIAGONAL-DEFECT-SKEW-024

```
Question:
Can one realize, first at the reduced level and then locally, a **one-defect diagonal moving transposition** whose grouped base dynamics merge the residual invariant diagonal/anti-diagonal orbit, while the grouped cocycle also acquires the smallest necessary second-coordinate defect so that the full grouped orbit can exceed the current `m^2(m-1)` barrier?

Purpose:
`023` identifies the first genuine 2D reduced grouped-base model. `021/022` show that the obvious one-bit and one-surface local families cannot realize it. The next honest step is therefore:
1. classify the smallest reduced one-defect diagonal families,
2. determine which of them can support a nontrivial 2D cocycle defect,
3. and only then search for a tiny local mechanism that emulates that target.

Inputs / Search space:
- Reduced mixed model from `019`:
  \[
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  \qquad
  \phi(s)\sim -2\,\mathbf 1_{s=2}.
  \]
- Negative local boundaries:
  - `021`: standard one-bit paired carry family
  - `022`: affine one-surface paired family
- Positive reduced 2D model:
  - `023`: moving adjacent transposition along
    \[
    u=\pm s+b
    \]
- Checked odd moduli:
  - `m in {5,7,9,11,13,15,17,19}`

Allowed methods:
- exact reduced-model analysis
- orbit decomposition on grouped base `(s,u)`
- cocycle-sum analysis on grouped orbits
- tiny targeted local realization search only after a reduced target is fixed
- no broad affine / one-surface / generic selector sweep

Stage 1: reduced base-defect family
- Start with
  \[
  B_{\varepsilon,b}(s,u)=\bigl(s+1,\tau_{\varepsilon s+b}(u)\bigr),
  \qquad \varepsilon\in\{\pm1\}.
  \]
- Add one defect of one of the following types:
  - row-shift defect:
    on one row `s=s_0`, swap `\tau_{\varepsilon s+b+\delta}` instead of `\tau_{\varepsilon s+b}`, with `\delta=\pm1`;
  - omission defect:
    on one row `s=s_0`, remove the swap;
  - double-edge defect:
    on one row `s=s_0`, compose with one additional adjacent transposition.
- Compute grouped base orbit sizes and determine whether the small invariant diagonal orbit survives.

Stage 2: cocycle-defect family
- Keep the base defect from Stage 1.
- Add the smallest cocycle defect
  \[
  \phi_D(s,u)=\phi(s)+\kappa\,\mathbf 1_{(s,u)\in D},
  \]
  where `D` is tied to the defect row / defect edge and `\kappa` is a small offset mod `m`.
- Determine which choices make the total cocycle over the merged base orbit nonzero mod `m`.

Stage 3: local emulation target
- Only after the best reduced target is identified:
  - search a tiny non-affine or predecessor-style paired carry family,
  - aimed specifically at emulating that reduced defect model,
  - not at generic survival.

Success criteria:
1. Find a reduced one-defect diagonal family whose grouped base has a single orbit of size `m^2`.
2. Find a matching cocycle defect so that the full grouped orbit exceeds `m^2`, ideally reaching `m^3`.
3. Identify the smallest reduced target that is strictly stronger than the current `023` baseline.
4. Formulate the smallest plausible local mechanism that could emulate it.
5. Preferably find a clean strict local realization on `m=5,7,9`.

Failure criteria:
- every one-defect diagonal base family still leaves a residual small orbit, or
- every merged base orbit forces the old `s`-only cocycle sum to vanish and no tiny cocycle defect repairs it, or
- no plausible non-affine / predecessor-style local mechanism can emulate the best reduced target.
- If failure occurs, state whether the next missing ingredient is:
  - a multi-defect diagonal family, or
  - a genuinely new grouped coordinate beyond `(s,u)`.

Artifacts to save:
- code
- raw logs
- summary report
- reduced base-defect orbit tables
- cocycle-defect orbit-sum tables
- candidate local-mechanism tables
- proof-supporting computations

Return format:
- exact reduced diagonal family used
- exact defect types tested
- grouped base orbit decompositions
- cocycle-sum analysis over grouped orbits
- smallest successful reduced target, if any
- smallest plausible local emulation mechanism
- strongest obstruction if none survives

Reproducibility requirements:
- fixed reduced model from `019`
- fixed checked moduli `5,7,9,11,13,15,17,19`
- deterministic enumeration order
- saved JSON/CSV for base-defect families, cocycle-defect families, and orbit tables
- explicit separation of:
  - reduced-model facts
  - local-realization facts
```

The short strategic conclusion is:

**`023` gives the right 2D reduced base model.
`021/022` show the obvious local families cannot realize it.
So the next honest branch is: defect the diagonal transposition at the reduced level, understand the cocycle consequence, and only then search for the smallest non-affine/predecessor-style local emulation.**
