# D5 review 075 — current progress and overall direction

## Scope

I reviewed the current picture against:

- `d5_075_reviewer_brief.md`
- `d5_075_threeway_handoff.md`
- the shared `071/072` bridge context
- the four `074` notes, with their included support summaries

I did **not** run new bridge-search or validation jobs. This is a reviewer pass on
claims, dependencies, and theorem/support boundaries.

---

## Executive assessment

The current three-way split is the right one.

The branch is no longer confused about whether some bridge might exist. The real
question is now much narrower:

> what is the exact deterministic global quotient for current `epsilon4`, and
> how much of the present odometer picture is theorem-level versus checked-range
> support?

My main review conclusion is:

> the safest **canonical theorem object** today is the abstract boundary
> right-congruence state `rho` of the future `epsilon4` word, not yet the
> concrete coordinate `delta = q + m sigma`.
>
> The dynamic odometer `(beta,q,sigma)` / `(beta,delta)` is the best
> **compute-supported coordinate model** for that object, but the package should
> still distinguish that coordinate identification from the theorem-level
> canonical quotient.

So I think the current direction is good, but one cleanup is still needed:

- **canonical theorem object:** `(beta,rho)`
- **best checked coordinate realization:** `(beta,q,sigma)` or `(beta,delta)`

If those are kept separate, the current program becomes much cleaner.

---

## What I believe is already theorem-ready

### 1. The abstract realization theorem is essentially ready

The `074` realization note isolates the right statement:

- if `Q` is a deterministic quotient,
- and current `epsilon4` is exact on `Q`,
- then the short-corner detector descends automatically;
- if every accessible orbit meets the descended short-corner set again,
  then the canonical clock descends uniquely by corner-time modulo `m`.

This looks theorem-ready in its **abstract** form. Its proof uses only:

- determinism,
- current-symbol exactness,
- the accepted phase-corner package upstairs,
- and an explicit recurrence hypothesis.

It does **not** depend on the concrete odometer coordinates.

That is the cleanest theorem-level result currently visible.

### 2. The abstract minimal exact quotient is theorem-ready

Researcher 2’s right-congruence viewpoint is the right canonical abstraction.
Given a deterministic quotient exact for current `epsilon4`, equality of future
`epsilon4` words is the unavoidable equivalence relation. So on an accessible
regular component, the minimal deterministic exact quotient is the boundary
future-word / right-congruence state `rho`, together with the coarse clock
`beta`.

This gives a theorem-level statement of the form:

> the canonical exact bridge is `(beta,rho)`, where `rho` is the boundary
> right-congruence class of the future `epsilon4` word.

That statement is stronger and safer than saying the canonical bridge is already
`(beta,q,sigma)`.

### 3. The conditional bridge-construction lemma is ready

Researcher 1’s conditional construction is also useful and ready in the
following form:

> if the D5 regular union admits boundary coordinates `(q,sigma)` with fixed
> in-chain behavior, splice update
> `(q,sigma) -> (q+1, sigma + 1_{q=m-1})`, and the current-event readout
> formulas from `072/074`, then `(beta,delta)` with `delta=q+m sigma` is a
> deterministic exact quotient for current `epsilon4`.

That is a good theorem schema.

What is **not** yet theorem-ready is the D5-specific identification of the true
boundary state with those concrete coordinates.

### 4. The coarse `beta` bridge should continue to be treated as settled context

The current handoff is right to treat the coarse carry / distance-to-endpoint
bridge as accepted context rather than the live frontier.

---

## What still depends on checked support

### 1. The concrete D5 identification `rho ≅ (q,sigma) ≅ delta`

This is still the main non-theorem step.

What is checked:

- on the frozen `047` range `m=5,7,9,11`, the splice-compatible exact bridge
  `(beta,q,sigma)` works;
- the splice law matches the odometer rule there;
- the current `epsilon4` readout matches there;
- short-corner exactness matches there.

What is **not** yet proved uniformly:

- that the actual D5 accessible exact object really admits those global
  coordinates;
- that the dynamic boundary state is literally the two-digit odometer for all
  odd `m`.

So `delta = q + m sigma` is still a checked coordinate model, not yet a proved
D5 theorem object.

### 2. The event readout formulas are still checked-range facts

The formulas

- `other_1000` at `beta=m-2` iff `q=m-1`
- `other_0010` at `beta=m-3` iff
  `(q+sigma=1 mod m)` or `(q=m-1 and sigma!=1)`

are strongly supported on the checked frozen range, but they are not yet a
uniform theorem consequence of the D5 structure.

### 3. The splice law is still checked-range support, not theorem

Likewise, the law

```text
(q,sigma) -> (q+1 mod m, sigma + 1_{q=m-1} mod m)
```

is currently a data-supported law, not yet a structural theorem derived from the
D5 chain package.

### 4. The accessible-image question is unresolved in theorem form

The handoff is completely right that the accessible subset `A` is not yet cleanly
packaged.

What is checked:

- for `m=7,9,11`, the frozen rows realize the full `m^2` `(q,sigma)` grid;
- for `m=5`, the frozen rows miss two boundary pairs, so the saved sample is not
  closed.

What is not yet proved:

- whether the actual accessible quotient-image is uniformly the full odometer;
- or, if not phrased that way, what the exact accessible quotient-image is.

### 5. Minimality of the **abstract** quotient is theorem-level, but minimality of the **odometer coordinates** is not yet fully theorem-level

This distinction matters.

What is theorem-level already:

- the canonical exact quotient on a component is the right-congruence quotient
  `(beta,rho)`.

What is only checked / conditional:

- that `rho` is exactly represented by `(q,sigma)` or `delta=q+m sigma` in the
  D5 system;
- that the Moore-minimal symbolic odometer model is the real D5 quotient-image,
  not just a supported symbolic completion.

So “minimal exact quotient exists” is theorem-level.
“that minimal quotient is exactly `(beta,q,sigma)` / `(beta,delta)`” is still a
bridge theorem target.

### 6. Extension beyond the frozen splice range is still missing

The dynamic bridge has not yet been extended beyond the frozen `047` splice
range. Larger-modulus support currently belongs only to the already-settled
coarse `beta` / marked-chain picture.

---

## The single most dangerous hidden assumption

The most dangerous hidden assumption is the current ambiguity around the
accessible subset `A`.

Here is the precise issue.

Several notes now speak as if all three of the following can be used at once:

1. `delta` is a state in `Z/m^2` (equivalently `(q,sigma)` on the full `m x m`
   grid);
2. the successor on boundary states is literally `delta -> delta + 1 mod m^2`;
3. the actually accessible quotient-image might still be a proper splice-invariant
   subset `A` of that odometer.

Those three statements do **not** coexist cleanly.

If the boundary successor really is `delta -> delta+1` on `Z/m^2`, then this is
one single `m^2`-cycle. Therefore any nonempty forward-invariant subset is
already the whole `Z/m^2`.

So the final theorem language must choose one of two forms:

### Form A: abstract accessible image first

State the bridge theorem with an abstract boundary state `rho` (or abstract
accessible image `A`) and successor `S`, without yet identifying `A` with a
subset of `Z/m^2`.

Then later prove that:

- `A` is isomorphic to `Z/m^2`, and
- under that isomorphism, `S` becomes `+1`.

### Form B: full odometer theorem

Prove directly that the D5 accessible bridge image is the full odometer
`Z/m^2`, so the separate “accessible subset `A`” language disappears.

At the moment the notes sometimes slide between these two forms. That is the
single point most likely to make a theorem claim look stronger than the current
proof/support base actually warrants.

---

## Other hidden assumptions / pressure points

### 1. Gap between the symbolic odometer model and the actual accessible D5 image

Researcher 4’s minimization result is important, but it is a statement about the
**supported symbolic splice automaton**.

That is not automatically the same thing as:

- the actual accessible quotient-image of D5 for all `m`, or
- a proved quotient-image even on the checked range.

The distinction matters especially because:

- `m=5` uses a symbolic completion beyond the observed saved sample;
- larger moduli have not yet been checked on the dynamic splice bridge.

So “no smaller factor is visible on the supported symbolic model” is good and
useful, but it is not yet the same as a uniform D5 theorem that no smaller exact
factor exists.

### 2. Canonicity of `(beta,q,sigma)` is not yet theorem-level

The canonical object is currently `rho`, the future-word / right-congruence
state.

The variables `q` and `sigma` are a **gauge choice** coming from the checked
normalization, especially `sigma = source_u + w mod m`.

Therefore the safest wording is:

- **canonical theorem object:** `(beta,rho)`;
- **best checked coordinate realization:** `(beta,q,sigma)` or `(beta,delta)`.

Calling `(beta,q,sigma)` itself “canonical” before the bridge theorem proves its
intrinsic status risks overstating the current result.

### 3. Recurrence of the descended short-corner set is not yet automatic in final form

The realization note isolates the right extra hypothesis: every accessible orbit
meets the visible short-corner set again.

That is the correct theorem-level hypothesis if the bridge object remains
abstract.

But it should not be silently dropped unless the final bridge theorem proves a
structure from which recurrence follows automatically — for example, a proved
full odometer cycle with the given event readout.

So the integrated theorem should keep recurrence explicit until the bridge
branch discharges it.

---

## What I would record as the current safest shared picture

I would phrase the current frontier like this:

### Safe current statement

1. The coarse `beta` clock is accepted.
2. The canonical exact deterministic bridge, in theorem form, is an abstract
   object `(beta,rho)` where `rho` is the boundary future-word right-congruence
   state.
3. The realization theorem is ready at that level: determinism + current
   `epsilon4` exactness + recurrence of the visible short-corner set imply
   descent of the canonical clock by corner-time modulo `m`.
4. The best current D5 coordinate candidate for `rho` is the dynamic odometer
   state `(q,sigma)` / `delta=q+m sigma`.
5. That coordinate model is strongly supported on the checked frozen splice
   range, but not yet uniformly proved.

This phrasing keeps the theorem package honest while still preserving the real
momentum of the current program.

---

## Recommended direction from here

### 1. Make the canonical theorem object abstract in the writeup

I would recommend that the shared theorem narrative stop saying “the canonical
bridge is `(beta,q,sigma)`” and instead say:

> the canonical exact bridge is `(beta,rho)`; compute strongly suggests that in
> D5 one can coordinatize `rho` by the odometer state `(q,sigma)`.

That single wording change would remove most of the current theorem/support
slippage.

### 2. Force a choice on the accessible-image issue

The bridge theorem branch should decide explicitly between:

- proving the full odometer image `Z/m^2`, or
- staying abstract and naming the accessible image without identifying it with a
  proper subset of `Z/m^2`.

Right now the notes sometimes try to do both.

### 3. Keep the realization theorem conditional until recurrence is discharged

The realization branch is in good shape. It should remain explicitly conditional
on the recurrence / hit hypothesis unless the bridge theorem proves a bridge
structure that makes that recurrence automatic.

### 4. Redirect compute toward the actual accessible image, not broader model search

The highest-value compute target now is not another search over bridge
candidates. It is:

- clarifying the actual accessible image of the dynamic bridge,
- checking whether symbolic minimality agrees with the observed accessible image,
- and extending direct dynamic-bridge support beyond the frozen range when safe.

---

## Precise bottom line

### What is already theorem-ready

- the abstract realization theorem over a deterministic current-`epsilon4` exact
  quotient with recurrent visible short corner;
- the abstract minimal exact quotient `(beta,rho)` defined by boundary
  right-congruence of future `epsilon4` words;
- the conditional bridge lemma: if D5 supplies odometer coordinates with the
  checked splice and readout laws, then `(beta,delta)` is an exact quotient.

### What still depends on checked support

- the D5 identification `rho ≅ (q,sigma) ≅ delta`;
- the odometer splice law as a uniform theorem;
- the current-event readout formulas as a uniform theorem;
- the exact accessible image / subset question;
- minimality of the concrete odometer coordinates as the actual D5 bridge;
- extension of dynamic-bridge validation beyond the frozen splice range.

### The single most dangerous hidden assumption

> treating the bridge simultaneously as a literal odometer
> `delta in Z/m^2` with successor `delta -> delta+1`, and also as though the
> actual accessible image could still be an unresolved proper splice-invariant
> subset `A` of that odometer.

That is the one place where the current writeup is most at risk of sounding more
proved than it is.

