# D5 Route Organization 063

This note consolidates the four `063` documents into one organized picture:

- constructive route note:
  [d5_constructive_source_residue_route_063.md](./d5_constructive_source_residue_route_063.md)
- theorem / phase-machine note:
  [works_063_a.md](./works_063_a.md)
- structural assessment note:
  [works_063_b.md](./works_063_b.md)
- negative-route note:
  [works_063_c.md](./works_063_c.md)

The goal is to separate the current D5 problem into three clean branches:

1. the theorem / structural branch,
2. the positive constructive branch,
3. the negative / no-go branch.

## 1. Executive summary

The `063` cluster says the D5 frontier is no longer one mixed problem.

It has split into:

- a nearly closed structural theorem chain, conditional on the explicit
  `H_{L1}` trigger theorem from `033`;
- a positive constructive route through transported source residue `rho`;
- a negative route through a bounded-quotient or odometer-factor no-go.

The clean current interpretation is:

> theorem side: D5 looks like an odometer with one corner;
> constructive side: the real question is whether one can locally initialize
> and transport source residue;
> negative side: if that transport is impossible in the intended local class,
> prove a reduction lemma and kill it with the witness family.

## 2. What each `063` note contributes

### 2.1 `works_063_a`: the phase-corner theorem target

This note argues that the right theorem is not a fitted reset formula, but a
small phase machine in

- `kappa = q + s + v + layer mod m`.

Its proposed theorem is essentially:

- `kappa` advances by `+1 mod m`,
- nonflat behavior happens only at a tiny set of phases,
- the short reset comes from one corner state,
- `CJ` and `OTH` then become corollaries.

This is the cleanest theorem-side slogan:

> **D5 should be an odometer-with-one-corner theorem.**

### 2.2 `works_063_b`: the structural chain is nearly closed

This note argues that, conditional on the explicit `033` hole-family formula,
the structural route is almost complete.

The compressed spine is:

- `033 -> 062 -> 059`,

with `061` serving as a useful cross-check rather than a logically essential
input.

The key point is:

- `062` derives the universal first-exit targets from the explicit `H_{L1}`
  trigger theorem and the phase-1 source-residue invariant;
- once that is done, the candidate orbit agrees with the actual active branch
  up to exit;
- therefore pre-exit states stay in the unmodified `B` region;
- therefore the global phase scheduler follows from the mixed witness rule on
  `B`.

So `063B` says the structural branch is no longer the likely bottleneck.

### 2.3 `works_063_c`: the clean no-go target

This note identifies the real negative theorem to seek:

- not a vague impossibility theorem for all local rules,
- but a reduction lemma showing the intended admissible/local class collapses
  to bounded transition/reset data.

Once such a reduction lemma exists, the witness family from `047/048/050/052`
should kill the class.

This is the right negative-route statement:

> **prove a bounded-quotient collapse, then hit it with the persistent witness
> family.**

### 2.4 `d5_constructive_source_residue_route_063`: the positive route

This note provides the strongest current constructive refinement.

It says:

- theorem-side minimal object remains `(B, tau, epsilon4)`;
- constructive-side stronger object is `(B, rho)`, where
  `rho = u_source + 1 mod m`.

On the checked active branch, once `rho` is available:

- `q` becomes current-state exact,
- `c` becomes current-state exact,
- `tau` becomes current-state exact,
- `next_tau` becomes current-state exact.

So the constructive problem is no longer “predict the future.” It is:

> **initialize and transport `rho`.**

## 3. Theorem / structural route

The theorem-side route currently looks like this.

### 3.1 Minimal theorem object

The theorem object should stay minimal:

- `B = (s, u, v, layer, family)`
- `tau`
- `epsilon4`

No theorem statement should be written primarily in `rho`, `delta`, `kappa`,
or `Theta`. Those are proof coordinates.

### 3.2 Current strongest structural chain

Conditional on the explicit `033` trigger theorem, the current best structural
chain is:

1. `033`: exact `H_{L1}` trigger family;
2. `062`: universal first-exit targets from the trigger family and the
   phase-1 source-residue invariant;
3. candidate orbit agrees with actual active branch up to first exit;
4. therefore pre-exit current states stay in `B`;
5. therefore the mixed-witness rule induces the global active phase scheduler;
6. therefore `CJ` and likely `OTH` follow as corollaries.

This is stronger than the earlier `061` framing because it treats first exits
as internally derived rather than imported.

### 3.3 Best theorem slogan

The best theorem-side slogan from the `063` cluster is:

> **On the active best-seed branch, D5 is an odometer with one corner.**

That means:

- one visible phase advances uniformly;
- all complicated behavior is concentrated in one tiny corner/event set;
- reset values are distances on that clock, with one short-circuit corner.

## 4. Positive constructive route

### 4.1 Why `rho` matters

The positive route is not “code `tau` directly.”

It is:

- transport `rho = u_source + 1`,
- then read out everything else from current state.

The checked formulas from `063` are:

- `q ≡ u - rho + 1_{epsilon4 = carry_jump} (mod m)`
- `c = 1_{q = m-1}`, hence exact on `(u, rho, epsilon4)`
- `tau` exact on `(s, u, v, layer, rho)`
- `next_tau` exact on `(s, u, layer, rho, epsilon4)`

This is the strongest positive constructive refinement currently visible.

The optional support pass `063A` now validates these explicit formulas through
`m = 13,15,17,19` as well; see
[artifacts/d5_constructive_source_residue_support_063a/README.md](../../artifacts/d5_constructive_source_residue_support_063a/README.md).

### 4.2 Natural gauge: `alpha = rho - u`

The constructive route becomes cleaner in the gauge

- `alpha := rho - u`.

Then:

- `q ≡ -alpha + 1_{epsilon4 = carry_jump} (mod m)`
- `c` becomes a current readout from `(alpha, epsilon4)`
- the residue
  `delta = rho - (s + u + v + layer)`
  becomes
  `delta = alpha - (s + v + layer)`.

So `alpha` is likely the better transport variable than raw `rho`.

It isolates the part of the source residue that survives after removing the
trivial current `u` drift.

### 4.3 Relation to the phase machine

The constructive and theorem-side clocks are not separate.

On checked flat states, the auxiliary residue and visible phase satisfy:

- `delta ≡ -kappa (mod m)`,

where

- `delta = rho - (s + u + v + layer)`,
- `kappa = q + s + v + layer`.

So the `delta` reduction from the constructive side and the `kappa` phase
machine from the theorem side are the same clock in two gauges.

This is the main conceptual unification from the `063` cluster.

### 4.4 Positive-route target

The smallest positive constructive theorem worth seeking is:

> There exists a local/admissible mechanism that initializes a source-residue
> carrier and transports it through the active branch.

In practice, the best version may be:

> transport `alpha = rho - u`,

because then the carry, phase, and trigger logic become current-state
readouts.

## 5. Negative / no-go route

The negative route should not try to disprove all local mechanisms at once.

The right target is:

1. define the intended admissible/local class clearly;
2. prove every mechanism in that class factors through bounded grouped
   transition/reset data, or a finite quotient of the active odometer word;
3. use the persistent witness family from `047/048/050/052` to contradict that
   factorization.

This is what `063C` is pushing toward.

The main negative-route insight is:

> if the class cannot transport source residue uniformly in `m`, it should
> collapse to a bounded quotient, and then the witness family should rule it
> out.

So the negative route is naturally an odometer-factor / Myhill-Nerode style
argument on the active branch.

## 6. Current status after combining the four notes

The four `063` documents together say:

- **structural branch:** likely close to closed, conditional on the explicit
  `033` trigger theorem;
- **theorem branch:** best current target is a phase-corner / odometer with one
  corner theorem;
- **positive constructive branch:** best target is transported source residue,
  preferably in the gauge `alpha = rho - u`;
- **negative branch:** best target is a bounded-quotient collapse theorem for
  the intended local class.

This is a much cleaner split than the older “code `tau` somehow” framing.

## 7. Recommended use

For another mathematician, the best use of this note is:

1. if they want theorem-side proof work:
   focus on `063A/063B`, especially the phase-corner theorem and the
   `033 -> 062 -> 059` structural chain;
2. if they want constructive work:
   focus on `063` proper and treat `rho`, or better `alpha = rho - u`, as the
   live transport variable;
3. if they want a no-go route:
   focus on `063C` and formulate the bounded-quotient reduction lemma.

## 8. Honest open point

The `063` cluster does **not** solve D5.

It does, however, make the remaining frontier very sharp:

- either transport the source residue,
- or prove that the admissible local class cannot do so uniformly.

That is the clean current formulation.
