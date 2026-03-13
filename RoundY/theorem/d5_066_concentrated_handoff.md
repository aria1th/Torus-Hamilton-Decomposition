# D5 Concentrated Handoff 066

This note records the current D5 frontier in the simplest top-level split:

1. theorem package,
2. clock route,
3. compute support.

The goal is to concentrate the project into the smallest number of real moving
parts.

## 1. Current position

The D5 problem is no longer a broad design/search problem.

The structural branch has been compressed enough that it now looks like a
theorem package waiting to be finished, while the remaining live frontier is
best understood as a question about one canonical cyclic clock.

So the right top-level organization is:

- **Theorem package**
  phase-corner theorem, countdown/reset corollaries, structural chain
- **Clock route**
  realization of the canonical `beta` clock, plus rigidity showing that any
  exact realization must carry that same clock on its accessible part
- **Compute support**
  validate the exact reduction object and stress-test the clock identities,
  without reopening generic search

## 2. Theorem package

### 2.1 The theorem object

The theorem object remains minimal:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

Auxiliary coordinates such as `rho`, `alpha`, `delta`, `kappa`, and `beta`
should be treated as proof or constructive coordinates only.

### 2.2 Main theorem

The central theorem is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

Concretely, on the active nonterminal branch one defines

- `kappa = q + s + v + layer mod m`
- `c = 1_{q = m-1}`

and proves:

1. `kappa' = kappa + 1 mod m`
2. the current event `epsilon4` is determined by `(kappa, c, s)` by the small
   phase-corner scheduler
3. among flat states, the only short reset occurs at the corner `(kappa, s) = (2, 2)`

This is the conceptual center of the theorem side. The branchwise reset laws
should be treated as corollaries, not as primary independent statements.

### 2.3 Corollaries

From the phase-corner theorem one derives:

- countdown law for `tau`
- branchwise reset formulas for `wrap`, `carry_jump`, `other_1000`,
  `other_0010`
- compatibility with the finite-cover chain
  `B <- B+c <- B+c+d`

### 2.4 Structural chain

The structural proof spine is:

1. explicit trigger family
2. universal first-exit targets
3. pre-exit `B`-region invariance
4. mixed-witness scheduler on `B`
5. phase-corner theorem
6. countdown/reset corollaries

So the theorem package is now close to “manuscript completion,” not to open
exploration.

## 3. Clock route

The remaining live frontier is best described as a question about one canonical
clock.

### 3.1 Canonical clock

The constructive coordinate

- `beta`

is now the right clock variable.

It is not merely compatible with the theorem-side phase. It is the same machine
in another gauge:

- theorem gauge: `kappa`
- constructive gauge: `beta`

with

- `beta = -kappa mod m`

on the active branch.

So the phase-corner theorem and the beta-controller theorem are equivalent
descriptions of the same object.

### 3.2 Realization side

The positive side is now:

> can the canonical `beta` clock be realized locally/admissibly?

This is no longer an open-ended controller design problem. It is a realization
problem for the canonical controller already determined by the theorem package.

The desired properties are:

- universal birth
- unit drift: `beta' = beta - 1 mod m`
- exact current readout of `q`, `c`, `epsilon4`, `tau`, and `next_tau` from
  `(B, beta)`

### 3.3 Rigidity side

The old “negative route” is now better read as rigidity:

> any exact local realization must already carry such a cyclic clock on its
> accessible exact part.

The core principle is:

- on a one-marked cyclic section, any exact quotient is injective
- therefore any exact realization must already contain the full clock, not just
  some compressed shadow of it

So the rigidity side does not compete with the positive side. It supports it by
explaining why an `m`-scale clock is structurally forced.

### 3.4 Chain vs cycle nuance

The only remaining nuance in the rigidity route is whether the D5 reduction
should first be stated on:

- a literal cyclic `m`-section, or
- a marked length-`m` chain extracted from the regular corridor

The current compute evidence suggests the chain statement may be the safer
first exact object, with the cycle statement as a possible strengthening later.

## 4. Compute support

The compute route is now sharply constrained.

It should do only the following kinds of work:

### 4.1 Validate the exact reduction object

This means:

- determine whether the correct exact reduction is a cycle or a chain
- extract the accessible section/chain cleanly
- validate the induced return object directly

### 4.2 Validate the canonical clock

This means:

- test `(B, beta)` exactness on larger moduli
- test unit drift `beta' = beta - 1`
- test exact readout of
  `q`, `c`, `epsilon4`, `tau`, `next_tau`, and, where relevant, `next_B`

### 4.3 Validate the reduction for the local class

This means:

- compute the accessible quotient induced by the intended local/admissible
  class
- identify whether it is bounded on the relevant section
- reduce future compute to validating that quotient, not exploring the whole
  local rule space

### 4.4 What compute must not do

- no generic search
- no reopening broad local-controller families
- no fresh witness hunting

Compute is now support for the reduction, not a replacement for it.

## 5. Recommended division of labor

### Researcher A: theorem package

Aim:

- finish the phase-corner theorem cleanly
- package countdown/reset laws as corollaries
- write the structural chain in manuscript form

### Researcher B: clock realization

Aim:

- realize the canonical `beta` clock locally/admissibly
- treat this as realization of the theorem-side machine, not as free design

### Researcher C: rigidity

Aim:

- prove the exact section/chain rigidity statement
- prove the intended local class reduces to the relevant accessible quotient
- conclude that any exact realization must carry an `m`-scale clock

### Researcher D: compute support

Aim:

- validate cycle vs chain
- validate `(B, beta)` exactness on larger moduli
- validate the accessible quotient for the intended local class

## 6. Honest frontier

The theorem package now looks close to closure in shape.

So the real unresolved part is not the abstract machine anymore. It is:

> can the intended local class realize the canonical `beta` clock, or does the
> exact reduction force any realization to carry such a clock in a way the
> local class cannot support?

That is the clean current frontier.
