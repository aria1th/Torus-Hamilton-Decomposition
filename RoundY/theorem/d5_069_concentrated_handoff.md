# D5 Concentrated Handoff 069

This note supersedes the older `067/068` concentrated handoffs as the cleanest
statement of the current D5 frontier.

The project is now best organized into:

1. theorem package,
2. exact reduction,
3. realization,
4. support theorems and compute.

The main change from `067/068` is that the theorem package is no longer the
main live branch. It is close enough to closure in shape that the real work has
shifted to the exact reduction object and the realization problem over that
object.

## 1. Current position

The D5 problem is no longer:

- witness search,
- separator search,
- small transducer widening,
- or theorem-object discovery.

It is now:

- **Theorem package**
  near-stable and manuscript-shaped
- **Exact reduction**
  identify and validate the correct exact marked object and the quotient
  induced by the intended class
- **Realization**
  prove the canonical clock descends on that exact quotient
- **Support**
  rigidity and compute that make the exact reduction / realization step clean

So the real frontier is now very narrow.

## 2. Theorem package

### 2.1 Status

The theorem package should now be treated as the base platform, not the main
open branch.

Its minimal theorem object remains:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

Auxiliary coordinates remain:

- raw lifted coordinates `(q, w, u, Theta)`
- `rho`
- `kappa = q+s+v+layer mod m`
- `beta = -kappa mod m`

### 2.2 Main theorem

The conceptual center is still:

> **On the active best-seed branch, D5 is an odometer with one corner.**

Read in theorem gauge:

- `kappa = q + s + v + layer mod m`
- `c = 1_{q = m-1}`

with:

1. `kappa' = kappa + 1 mod m`
2. current event determined by the small phase-corner scheduler
3. one short flat corner at `(kappa, s) = (2, 2)`

Countdown and reset laws are corollaries of that theorem.

### 2.3 Structural spine

The structural reduction spine is:

- explicit trigger family
- universal first exits
- pre-exit `B`-region invariance
- mixed-witness scheduler on `B`
- phase-corner theorem
- countdown/reset corollaries

Compressed form:

- `033 -> 062 -> 059`

This is the theorem-side backbone.

### 2.4 What still remains on the theorem side

Mostly:

- statement cleanup,
- dependency bookkeeping,
- manuscript organization,
- and local proof cleanup where necessary.

So theorem work still exists, but it is no longer the main place where the D5
branch is conceptually open.

## 3. Exact reduction

This is the first real live focus.

### 3.1 Current best exact object

The strongest current evidence says:

- the safer first exact reduction object is a **marked length-`m` chain**
  extracted from regular carry-jump slices;
- a literal cycle is a possible later strengthening, not the first thing to
  force.

This is now supported by regenerated full active rows through `m = 21` and
branch-local support through `m = 41`.

### 3.2 Exact reduction target

The exact reduction target should now be stated explicitly:

1. extract the marked chain/cycle from the active branch;
2. prove its deterministic successor law;
3. identify the marked carry state(s);
4. identify the quotient induced by the intended local/admissible class on
   that object;
5. determine whether that quotient is exact for the current event `epsilon4`.

This is the D5-specific reduction step.

### 3.3 What to dig for

The next exact-reduction work should ask:

- is the first exact object a chain or a cycle?
- what is the smallest accessible quotient of the intended class on that
  object?
- is that quotient exact for `epsilon4`?
- does it already preserve the short corner?

This is more important than running broader support sweeps.

## 4. Realization

This is the second real live focus.

### 4.1 The clock is no longer the mystery

The canonical clock already exists:

- theorem gauge: `kappa`
- constructive gauge: `beta = -kappa`
- lifted exact corridor: `beta = -Theta`

So the realization problem is **not**:

> invent a new controller.

It is:

> prove that the intended local/admissible quotient exposes the already
> existing canonical clock.

### 4.2 The `069` sharpening

The key `069` realization upgrade is:

> if the intended quotient is already an exact deterministic quotient for the
> current event `epsilon4` on the marked chain/cycle, then the canonical clock
> is recovered intrinsically from the short corner.

More precisely:

- the short corner is the unique state with two-step event signature
  `(flat, other_0010)`;
- so any exact `epsilon4` quotient must see that corner;
- once that corner is seen, the canonical clock is just
  **time to the next short corner**,
  in the gauge `beta = -kappa`.

So the realization route has become much cleaner:

- prove exact deterministic `epsilon4` quotient on the exact reduction object,
- then the clock descent is essentially forced.

### 4.3 Exact realization target

The realization target should now be stated as:

1. prove the intended quotient is exact for `epsilon4` on the exact reduction
   object;
2. prove the short-corner detector descends;
3. define the descended clock by time-to-next-corner;
4. deduce the canonical `beta` clock on the accessible exact quotient.

This is much sharper than “transport a hidden carrier.”

## 5. Support theorems

These are no longer competing routes. They now support exact reduction and
realization.

### 5.1 Rigidity

The old negative route is best read as:

> once the exact marked chain/cycle is fixed, exactness forces the canonical
> clock.

`069` sharpens this further:

- the clock is not merely transported;
- it is intrinsically reconstructible from the future carry word on the exact
  marked object.

So rigidity now says:

- no clock ambiguity remains once the exact reduction object is fixed;
- the only D5-specific gap is reduction to that object and exactness of the
  intended quotient there.

### 5.2 Compute

Compute is now support for the exact reduction / realization step only.

The strongest current packaged support is:

- full regenerated active-row support on
  `m = 13, 15, 17, 19, 21`
- branch-local support on
  `m = 31, 33, 35, 37, 39, 41`

with:

- marked-chain validation,
- exact `(B,beta)` drift and readout,
- and first quotient diagnostics on the marked chains.

The right next compute is therefore:

- push the exact reduction / accessible quotient extraction further,
- not reopen generic controller search.

## 6. Exact theorem targets by part

### Theorem package

- Structural reduction theorem
- Phase-corner theorem
- Countdown theorem
- Reset theorem
- Gauge equivalence remark `beta = -kappa`

### Exact reduction

- Marked-chain / cycle theorem
- Exact deterministic successor on that object
- Exact current-event quotient theorem for the intended class

### Realization

- Short-corner visibility lemma on the quotient
- Time-to-next-corner clock theorem
- Canonical beta descent theorem

### Rigidity

- Injectivity / exactness theorem on the marked chain/cycle
- Intrinsic clock reconstruction from future carry word

## 7. Recommended division of labor

### Researcher A: theorem cleanup

Aim:

- finish manuscript packaging of the theorem side
- avoid reopening theorem discovery

### Researcher B: exact reduction

Aim:

- isolate the exact marked chain/cycle cleanly
- isolate the intended quotient on that object

### Researcher C: realization

Aim:

- prove the quotient is exact for `epsilon4`
- descend the short-corner detector
- derive the canonical clock as time-to-next-corner

### Researcher D: rigidity / compute support

Aim:

- prove intrinsic clock reconstruction on the exact object
- validate the exact reduction and quotient computationally

## 8. Honest frontier

The theorem package is no longer the main conceptual bottleneck.

The real D5 frontier is now:

> identify the exact marked reduction object and prove the intended quotient is
> exact enough there that the canonical clock descends.

Everything else now supports that.
