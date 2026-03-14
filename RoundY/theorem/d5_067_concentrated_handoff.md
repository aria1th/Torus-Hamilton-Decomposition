# D5 Concentrated Handoff 067

This note supersedes the older `065/066` concentrated handoffs.

The D5 frontier is now best organized into three parts:

1. theorem package,
2. clock route,
3. compute support.

The key change from `066` is that the clock route is no longer best described
as "positive vs negative." It is one canonical clock viewed in two ways:

- **descent / realization:** can the clock be exposed in the intended
  local/admissible class?
- **rigidity / necessity:** must any exact realization already carry that same
  clock on its accessible exact part?

## 1. Current position

The D5 problem is no longer a broad search problem.

The theorem side has compressed into a near-manuscript package. The remaining
live question is about one canonical cyclic clock. The right top-level split
is therefore:

- **Theorem package**
  phase-corner theorem, countdown/reset corollaries, structural spine
- **Clock route**
  the canonical `beta` clock, seen as lifted-clock descent on one side and
  exact-clock rigidity on the other
- **Compute support**
  validate the exact reduction object and the exact reduction data, without
  reopening generic search

## 2. Theorem package

### 2.1 The theorem object

The theorem object remains minimal:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

Auxiliary coordinates such as `rho`, `alpha`, `delta`, `kappa`, `Theta`, and
`beta` should be treated as proof or constructive gauges.

### 2.2 Main theorem

The central theorem is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

Concretely, on the active nonterminal branch define

- `kappa = q + s + v + layer mod m`
- `c = 1_{q = m-1}`

Then:

1. `kappa' = kappa + 1 mod m`
2. the current event `epsilon4` is determined by `(kappa, c, s)` by the small
   phase-corner scheduler
3. among flat states, the only short reset occurs at the corner `(kappa, s) = (2, 2)`

This is the conceptual center of the theorem side. Countdown and reset laws
should be presented as corollaries.

### 2.3 Corollaries

From the phase-corner theorem one derives:

- the countdown law for `tau`
- the branchwise reset laws for `wrap`, `carry_jump`, `other_1000`,
  `other_0010`
- compatibility with the finite-cover chain
  `B <- B+c <- B+c+d`

### 2.4 Structural spine

The best current structural spine is:

1. explicit trigger family
2. universal first-exit targets
3. pre-exit `B`-region invariance
4. mixed-witness scheduler on `B`
5. phase-corner theorem
6. countdown/reset corollaries

The clean compressed form is:

- `033 -> 062 -> 059`

with the exact trigger theorem feeding the universal first exits, and those
feeding `B`-region invariance and the theorem-side scheduler.

So the theorem package is no longer exploratory. It is close to manuscript
completion in shape.

### 2.5 Exact theorem targets

The theorem-side target should now be read as the following package:

- **Structural reduction theorem**
  universal first exits plus pre-exit `B`-region invariance on the active
  branch
- **Phase-corner theorem**
  `kappa' = kappa + 1`, current event determined by `(kappa,c,s)`, and one
  short flat corner
- **Countdown corollary**
  `tau' = tau - 1` away from the boundary
- **Reset corollary**
  `wrap`, `carry_jump`, `other_1000`, `other_0010` as current-state
  consequences of the phase-corner theorem
- **Gauge remark**
  `beta = -kappa`

## 3. Clock route

The remaining live frontier is about one canonical clock.

### 3.1 Canonical clock

The constructive coordinate

- `beta`

is the correct clock variable.

It is not merely compatible with the theorem-side phase. It is the same
machine in another gauge:

- theorem gauge: `kappa`
- constructive gauge: `beta`

with

- `beta = -kappa mod m`

on the active branch.

So the phase-corner theorem and the beta-controller theorem are equivalent
descriptions of the same object.

### 3.2 Lifted-clock descent

The strongest `067` positive sharpening is:

> the canonical `beta` clock already exists on the exact lifted active
> corridor as `beta = -Theta`.

So the positive route is no longer:

> invent a controller that works.

It is now:

> prove that the already-existing lifted phase / lifted beta descends to the
> intended local/admissible class.

This is a descent or exposure problem, not a design problem.

### 3.3 Exact-clock rigidity

The strongest `067` rigidity sharpening is:

> once the exact reduction object is fixed, any exact realization must
> transport every theorem-side coordinate on its accessible exact part.

So the realization must carry not just "some clock," but **that same canonical
clock**.

This is stronger than a size lower bound. It is a transport / injectivity
statement:

- exact carry words separate states on the reduced object
- therefore any exact realization is injective on the accessible exact part
- therefore every theorem-side coordinate, especially the canonical clock,
  transports uniquely

So the old negative route is now better read as **rigidity**.

### 3.4 Chain vs cycle nuance

The remaining nuance is whether the exact D5 reduction object should first be
stated as:

- a literal cyclic `m`-section, or
- a marked length-`m` chain extracted from the regular corridor

The current evidence suggests the chain statement may be the safer first exact
object, with the cycle statement a possible later strengthening.

But this no longer changes the conceptual picture: both forms carry the same
canonical clock.

### 3.5 Exact clock-route targets

The clock route is now narrow enough to state explicitly:

- **Descent / realization target**
  prove that the lifted clock `beta = -Theta` descends to the intended
  local/admissible quotient
- **Rigidity target**
  prove that any exact realization on the exact reduction object is injective
  on the accessible exact part and therefore transports the canonical clock
- **Reduction target**
  identify whether the first exact reduction object is a marked chain or a
  cycle, and state the clock theorem on that exact object first

## 4. Compute support

Compute is now tightly scoped. Its job is to validate the reduction, not to
search generically.

### 4.1 Validate the exact reduction object

This means:

- determine whether the right exact reduction object is a cycle or a chain
- extract the accessible section/chain cleanly
- validate the induced return object directly from branch data

### 4.2 Validate the canonical clock

This means:

- stress-test `(B, beta)` exactness on larger odd moduli
- stress-test unit drift `beta' = beta - 1`
- stress-test exact readout of
  `q`, `c`, `epsilon4`, `tau`, `next_tau`, and, where available, `next_B`

### 4.3 Validate the reduction for the intended class

This means:

- compute the accessible quotient induced by the intended local/admissible
  class
- identify whether it stays bounded on the relevant exact reduction object
- reduce future compute to validating that quotient, not exploring the whole
  local rule space

### 4.4 What compute must not do

- no generic search
- no reopening broad local-controller families
- no new witness hunting

Compute is now support for the exact reduction only.

### 4.5 What to dig for

For each live part, the next digging target is:

- **Theorem package**
  tighten dependencies and write the structural reduction theorem cleanly,
  rather than reopening upstream extraction
- **Clock descent**
  identify the smallest admissible quotient on which lifted phase fibers become
  singletons
- **Clock rigidity**
  prove injectivity on the exact marked chain/cycle and then transport the
  whole theorem-side machine
- **Compute support**
  validate chain vs cycle, accessible quotient behavior, and `(B,beta)`
  exactness / drift on larger moduli

## 5. Recommended division of labor

### Researcher A: theorem package

Aim:

- finish the phase-corner theorem cleanly
- package countdown/reset laws as corollaries
- write the `033 -> 062 -> 059` spine in manuscript form

### Researcher B: clock descent / realization

Aim:

- treat `beta` as the canonical clock already fixed by the theorem package
- prove or construct its descent from the lifted active corridor to the
  intended local/admissible class

### Researcher C: clock rigidity

Aim:

- prove the exact section/chain rigidity statement
- prove the intended local class reduces to the relevant accessible quotient
- conclude that any exact realization must carry the same canonical clock

### Researcher D: compute support

Aim:

- validate cycle vs chain
- validate `(B, beta)` exactness and drift on larger moduli
- validate the accessible quotient for the intended local/admissible class

## 6. Honest frontier

The theorem package now looks close to closure in shape.

So the real unresolved part is no longer the abstract machine itself. It is:

> can the intended local/admissible class expose the canonical lifted clock,
> or does exact reduction force that same clock in a way that the local class
> cannot support?

That is the clean current D5 frontier.
