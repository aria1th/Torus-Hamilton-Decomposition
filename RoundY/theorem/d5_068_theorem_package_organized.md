# D5 Theorem Package Organized 068

This note freezes the current theorem-side status after the `067/068`
packaging work.

The point is simple:

> the theorem package now looks close enough to closure in shape that it should
> no longer be treated as the main open frontier.

The live frontier has shifted to the clock route and its exact reduction.

## 1. What the theorem package is

The theorem package should now be read as four layers:

1. one structural reduction theorem,
2. one main phase-corner theorem,
3. countdown/reset laws as corollaries,
4. the canonical `beta` clock only as a gauge-equivalence remark.

That is the right manuscript order.

## 2. Minimal theorem object

The theorem object remains:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

The following should stay auxiliary:

- raw lifted coordinates `(q, w, u, Theta)`
- source residue `rho`
- theorem clock `kappa = q+s+v+layer mod m`
- constructive clock `beta = -kappa mod m`

So the main theorem should not be stated in `rho`, `Theta`, or `beta`.

## 3. Imported inputs

At the current packaging level, the theorem side treats the following as
imported inputs rather than re-deriving them from scratch:

- the explicit trigger family from `033`
- the mixed-witness scheduler on `B` from `059`
- finite-cover compatibility `B <- B+c <- B+c+d`

This is acceptable for the current manuscript-facing package. The point is to
organize the theorem cleanly, not to restart the entire upstream derivation.

## 4. Derived theorem package

From those imported inputs, the current package derives:

- the universal first-exit theorem (`062`)
- pre-exit `B`-region invariance
- the main phase-corner theorem
- the countdown law for `tau`
- the branchwise reset laws
- the gauge-equivalence remark `beta = -kappa`

So the theorem side is no longer “find the right theorem.” The right theorem
package is already visible.

## 5. Main theorem shape

The conceptual center is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

That statement is read in the phase gauge

- `kappa = q + s + v + layer mod m`
- `c = 1_{q = m-1}`

with:

1. `kappa' = kappa + 1 mod m`
2. current event determined by the small phase-corner scheduler
3. one short flat corner at `(kappa, s) = (2, 2)`

This should be the main theorem, not the reset formulas.

## 5A. Exact theorem statements to isolate

The theorem package is sharp enough that the exact statements should now be
isolated explicitly:

1. **Structural reduction theorem**
   The active branch has universal first exits and stays in the unmodified
   `B` region before exit.
2. **Phase-corner theorem**
   On the active nonterminal branch, `kappa` advances by `+1`, the current
   event is determined by `(kappa,c,s)`, and there is one short flat corner.
3. **Countdown theorem**
   `tau = 0` on nonflat states, `tau = 1` at the short corner, and otherwise
   `tau` is the ordinary phase countdown.
4. **Reset theorem**
   The reset values for `wrap`, `carry_jump`, `other_1000`, and `other_0010`
   are corollaries of the phase-corner scheduler.
5. **Gauge equivalence remark**
   `beta = -kappa` should be recorded as a useful equivalence, not promoted to
   the main theorem statement.

## 6. Structural reduction shape

The clean structural spine is:

- explicit trigger family
- universal first exits
- pre-exit `B`-region invariance
- mixed-witness scheduler on `B`
- phase-corner theorem
- countdown/reset corollaries

In compressed form:

- `033 -> 062 -> 059`

That is the theorem-side backbone.

## 6A. What to dig for on the theorem side

The remaining theorem-side digging should be narrow:

- make the structural reduction theorem completely clean in manuscript form
- isolate the exact imported inputs vs derived conclusions
- present reset laws as consequences, not as separate main theorems
- keep the theorem object minimal and relegate `rho`, `Theta`, and `beta` to
  proof or gauge remarks

What should *not* be reopened on the theorem side:

- new theorem objects
- new scheduler extraction
- new broad support computations
- new controller-search-inspired reformulations

## 7. What no longer seems like the main theorem-side job

The theorem side does **not** currently look blocked on:

- searching for a different theorem object
- reopening boundary-reset extraction
- reopening phase-scheduler extraction
- reopening broad support computation

The remaining theorem-side work is mostly:

- sharpening statements,
- tightening dependency bookkeeping,
- manuscript organization,
- and only local proof cleanup where needed.

That is why the theorem package should now be treated as near-stable.

## 8. What is still genuinely open

The main unresolved work is no longer the theorem package itself.

It is:

1. **Clock descent / realization**
   Can the canonical lifted clock be exposed in the intended local/admissible
   class?

2. **Clock rigidity**
   Does exact reduction force any exact realization to carry that same clock on
   its accessible exact part?

3. **Compute support for the exact reduction**
   Validate chain vs cycle, accessible quotient, and `(B,beta)` exactness /
   drift on larger moduli.

So the theorem package is now the base platform, not the main live research
question.

## 8A. What to dig for on the live parts

Once the theorem package is treated as fixed enough, the next digging targets
are:

- **Clock descent / realization**
  find the exact quotient criterion under which the lifted phase collapses to a
  single phase per accessible local state
- **Clock rigidity**
  prove the exact marked chain/cycle injectivity statement, then transport the
  whole theorem-side machine, not just carry
- **Compute support**
  validate the exact reduction object, then validate `(B,beta)` and the
  induced accessible quotient on that object

## 9. Recommended use

Use this note when handing work to collaborators who should **not** spend time
reopening the theorem side.

The best split is:

- theorem readers:
  read this package and treat it as the current manuscript backbone
- clock-route researchers:
  work on descent / realization or rigidity
- compute-support researchers:
  validate the exact reduction object and the clock on that object

## 10. Bottom line

The current D5 organization should now be read as:

- theorem package: near-closed in shape
- clock route: still live
- compute support: validate the reduction, not the old broad search space

That is the clean `068` position.
