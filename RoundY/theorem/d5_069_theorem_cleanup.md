# D5 theorem cleanup 069

This note turns the `068` organization into a cleaner manuscript-facing theorem
package.

It does **not** add compute, new theorem objects, or new search. It only:

1. freezes notation,
2. separates imported inputs from derived statements,
3. writes the structural theorem and phase-corner theorem in a clean order,
4. demotes countdown/reset formulas to corollaries,
5. keeps `beta` only as a gauge remark.

The baseline organizational position is the `068` package: theorem side near
closure in shape, clock route still live. This note is just theorem cleanup.

## 1. Notation freeze

Fix odd `m >= 5` and the active best-seed branch.

### 1.1 Main theorem object

The theorem object should remain

```text
(B, tau, epsilon4),
```

with

```text
B = (s, u, v, lambda, family).
```

Here `lambda` is the current theorem-side layer coordinate.

### 1.2 Auxiliary proof gauges

The following coordinates are auxiliary and should stay out of the main theorem
statement:

- lifted raw corridor coordinates `(q, w, u, Theta)`;
- source residue `rho = u_source + 1 mod m`;
- theorem clock
  ```text
  kappa = q + s + v + lambda mod m;
  ```
- constructive clock
  ```text
  beta = -kappa mod m.
  ```

The only notation cleanup that really matters is:

- use `lambda` for the theorem-object layer inside `B`;
- use `Theta` for the lifted corridor phase.

Those two should not be conflated.

### 1.3 Current carry bit

Define

```text
c = 1_{q = m-1}.
```

The main phase theorem is read in the gauge `(kappa, c)`.

## 2. Imported inputs vs derived outputs

The theorem package is now clean enough that the dependency split should be
stated explicitly.

### 2.1 Imported inputs

For the present package, treat the following as imported.

**(I1) Explicit trigger family from `033`.**

```text
H_{L1} = {(q,w,u,Theta) = (m-1,m-1,u,2) : u != 2}.
```

**(I2) Mixed-witness `B`-scheduler package from `059`.**

On `B`-labelled active states, the mixed-witness machine yields the current
small scheduler in the phase gauge `(kappa, c, s)`, together with the
one-step corner transition data needed for countdown/reset corollaries.

**(I3) Finite-cover compatibility from `059`.**

```text
B <- B+c <- B+c+d.
```

The point is that the theorem-side current-state machine propagates through
that finite-cover chain.

### 2.2 Derived outputs

From those imported inputs, the theorem package should derive only:

1. the structural reduction theorem;
2. the phase-corner theorem;
3. the countdown theorem;
4. the reset theorem;
5. the gauge remark `beta = -kappa`.

That is the full theorem package. Nothing else should be promoted to equal
status.

## 3. Structural reduction theorem

This is the right first theorem in the manuscript.

### Theorem 3.1 (structural reduction / pre-exit `B`-region invariance)

Let the post-entry active lifted state be

```text
x_0 = (q,w,u,Theta) = (m-1,1,u_source,2),
```

and set

```text
rho = u_source + 1 mod m.
```

Define the candidate lifted orbit `F` by

```text
F(q,w,u,0)     = (q+1, w,                 u,   1)
F(q,w,u,1)     = (q,   w,                 u+1, 2)
F(q,w,u,2)     = (q,   w + 1_{q=m-1},     u,   3)
F(q,w,u,Theta) = (q,   w,                 u,   Theta+1)   for 3 <= Theta <= m-1,
```

with all residues read modulo `m`.

Then:

1. every phase-1 candidate state satisfies
   ```text
   q = u - rho + 1 mod m;
   ```
2. the only phase-1 candidate states that can alternate into `H_{L1}` are
   ```text
   A = (m-1,m-2,1),
   B = (m-2,m-1,1);
   ```
3. their `u`-coordinates are
   ```text
   u(A) = rho - 2 mod m,
   u(B) = rho - 3 mod m;
   ```
4. therefore the first exit is universal:
   ```text
   T_reg = (m-1,m-2,1)   if rho != 4,
   T_exc = (m-2,m-1,1)   if rho = 4;
   ```
5. every candidate state before that first exit is `B`-labelled;
6. therefore the actual active branch agrees with the candidate orbit up to
   first exit.

In particular, the active branch has universal first exits and stays in the
unmodified `B` region before exit.

#### Proof

The first phase-1 candidate state is `(0,2,u_source,1)`, so

```text
q = u - rho + 1 mod m
```

holds there. From one phase-1 state to the next, the lifted orbit increments
`u` once at phase `1` and increments `q` once later at phase `0`. So the
relation is preserved on all phase-1 candidate states.

Only a phase-1 state can alternate into `H_{L1}`, because the target has
`Theta = 2`. To land in `(m-1,m-1,*,2)` in one alternate move, the source must
have `(q,w) = (m-1,m-2)` or `(m-2,m-1)`. These are exactly the two displayed
phase-1 states `A` and `B`.

Plugging `q(A)=m-1` and `q(B)=m-2` into the phase-1 invariant gives

```text
u(A) = rho - 2 mod m,
u(B) = rho - 3 mod m.
```

Since `H_{L1}` requires `u != 2`, the state `A` exits unless `rho = 4`. In the
exceptional case `rho = 4`, one has `u(A)=2` and `u(B)=1`, so `A` is blocked
and `B` is the first exit.

It remains to show that no patched class is visited before that first exit.
Along the candidate orbit, `w` starts at `1`, changes only at phase `2` with
`q = m-1`, and never decreases. Hence every patched class with `w = 0` is
impossible. The `w = 1, Theta = 3` patch also never occurs, because the branch
enters at `Theta = 2`. For the `L1`-type patched class `(m-1,m-1,1)`, the
regular family exits already at `(m-1,m-2,1)`, while on the exceptional family
the branch exits at `(m-2,m-1,1)` before it can reach `(m-1,m-1,1)`.
Therefore every pre-exit candidate state is `B`-labelled.

On `B`-labelled states the current rule is unmodified, so the actual branch and
candidate orbit have the same next step. Induction now gives actual branch =
candidate orbit up to first exit. ∎

### Cleanup remark

The structural theorem should be presented as the clean content of `062`, with
`033` quoted only for the exact trigger family. It should not be mixed with the
countdown or reset formulas.

## 4. Phase-corner theorem

This is the conceptual center of the theorem package.

### Theorem 4.1 (phase-corner theorem: D5 is an odometer with one corner)

On the active nonterminal branch define

```text
kappa = q + s + v + lambda mod m,
c = 1_{q = m-1}.
```

Then:

1. the phase advances uniformly,
   ```text
   kappa' = kappa + 1 mod m;
   ```
2. the current event `epsilon4` is determined by the current triple
   `(kappa, c, s)` through the scheduler
   ```text
   kappa = 0  -> wrap,
   kappa = 1  -> carry_jump,
   kappa = 2  -> other_1000 iff c = 1, else flat,
   kappa = 3  -> other_0010 iff (c = 0 and s = 2) or (c = 1 and s != 2), else flat,
   kappa = 4,...,m-1 -> flat;
   ```
3. among flat states, the unique short corner is
   ```text
   (kappa, s) = (2,2).
   ```

So on the active nonterminal branch, D5 is an odometer with one corner.

#### Proof

By Theorem 3.1, the active branch remains in the unmodified `B` region before
first exit. On that region, the imported `B`-scheduler package from `059`
provides the displayed phase machine in the gauge `(kappa, c, s)`. The imported
finite-cover compatibility then propagates the same current-state machine along

```text
B <- B+c <- B+c+d,
```

so the scheduler holds across the whole active nonterminal branch.

The only flat state at `kappa = 2` occurs when `c = 0`, and the only place
where the flat corridor is shortened is the branch with `s = 2`. Hence the
unique short flat corner is exactly `(kappa, s) = (2,2)`. ∎

### Cleanup remark

This is the main theorem. The theorem section should revolve around this
statement, not around the reset table.

## 5. Countdown theorem

The countdown should be isolated as a corollary of the phase theorem, with the
small remaining one-step information read from the imported corner data.

### Corollary 5.1 (countdown law)

Along the active nonterminal branch,

```text
tau = 0      on nonflat states,
tau = 1      at the short flat corner (kappa, s) = (2,2),
tau = m-kappa on all other flat states.
```

In particular,

```text
tau' = tau - 1
```

whenever `tau > 0`.

#### Proof

The nonflat cases are exactly the branch-reset states, so `tau = 0` there. By
Theorem 4.1, flat states away from `(kappa, s) = (2,2)` follow the ordinary
odometer phase, so the remaining time to the next nonflat event is `m-kappa`.
At `(kappa, s) = (2,2)`, the corridor is shortened by one step, giving
`tau = 1`.

The corner-by-corner verification that no other shortening occurs is part of
the imported one-step `B`-scheduler package from `059`. Once that is fixed,
`kappa' = kappa + 1` gives `tau' = tau - 1` for every positive countdown,
including the boundary case `kappa = m-1`, where the next state is wrap and
`tau' = 0`. ∎

### Cleanup remark

`tau` should be stated only after the phase-corner theorem. It is a readout of
the odometer-with-one-corner machine, not a competing theorem object.

## 6. Reset theorem

The reset table should be presented as a finite list of corollaries forced by
Theorem 4.1 and Corollary 5.1.

### Corollary 6.1 (branchwise reset laws)

On a current nonflat state, the next countdown value is

```text
wrap -> 0,
carry_jump -> 0    if c = 1,
carry_jump -> 1    if c = 0 and s = 1,
carry_jump -> m-2  if c = 0 and s != 1,
other_1000 -> m-3  if s = 1,
other_1000 -> 0    if s != 1,
other_0010 -> m-4.
```

#### Proof

Theorem 4.1 reduces the nonflat situations to the four corner events

```text
wrap, carry_jump, other_1000, other_0010.
```

The imported one-step corner transition data from `059`, combined with
Corollary 5.1, gives the successor countdown in each case. The values are
exactly the seven displayed branches above. ∎

### Cleanup remark

These reset laws should **not** be promoted to a separate main theorem. They
are the finite successor list forced by the phase-corner machine.

## 7. Finite-cover compatibility

It is useful to restate the imported propagation result once, but only after the
phase theorem has been fixed.

### Corollary 7.1 (finite-cover compatibility)

The current-state scheduler and the countdown/reset laws are compatible with

```text
B <- B+c <- B+c+d.
```

#### Proof

This is exactly the imported finite-cover propagation from `059`, now restated
at the level of Theorem 4.1 and Corollaries 5.1 and 6.1. ∎

## 8. Gauge remark: `beta` is the same clock in another gauge

`beta` should appear only after the main theorem package has been stated.

### Proposition 8.1 (gauge equivalence)

Define

```text
beta = -kappa mod m.
```

Then on the active nonterminal branch,

```text
beta' = beta - 1 mod m,
```

and the phase-corner scheduler becomes

```text
beta = 0     -> wrap,
beta = m-1   -> carry_jump,
beta = m-2   -> other_1000 iff c = 1, else flat,
beta = m-3   -> other_0010 iff (c = 0 and s = 2) or (c = 1 and s != 2), else flat,
beta = 1,...,m-4 -> flat.
```

So the theorem-side phase clock and the constructive `beta` controller are the
same canonical cyclic clock.

#### Proof

Immediate from Theorem 4.1 under the change of variables `beta = -kappa`. ∎

### Cleanup remark

This proposition belongs in a remark or short subsection after the theorem
package. It should not replace the phase-corner theorem as the main statement.

## 9. Dependency ledger for the manuscript

The manuscript should make the dependency chain visible once and then stop
repeating it.

### Imported

- `033`: exact trigger family `H_{L1}`;
- `059`: current `B`-scheduler package;
- `059`: finite-cover propagation.

### Derived

- Theorem 3.1: structural reduction / pre-exit `B`-region invariance;
- Theorem 4.1: phase-corner theorem;
- Corollary 5.1: countdown law;
- Corollary 6.1: reset law;
- Corollary 7.1: finite-cover compatibility (restated);
- Proposition 8.1: `beta = -kappa` gauge equivalence.

In short,

```text
033 -> 062 -> 059 -> phase-corner theorem -> countdown/reset corollaries.
```

If a shorter slogan is needed, use

```text
033 -> 062 -> 059.
```

## 10. Recommended theorem-section order

The clean manuscript order is now:

1. define the theorem object `(B, tau, epsilon4)`;
2. define the proof gauge `(kappa, c)`;
3. quote the trigger family from `033`;
4. prove Theorem 3.1 (structural reduction);
5. quote the `B`-scheduler package and finite-cover propagation from `059`;
6. prove Theorem 4.1 (phase-corner theorem);
7. derive Corollary 5.1 (countdown);
8. derive Corollary 6.1 (reset);
9. record Proposition 8.1 (`beta = -kappa`) only as a gauge remark.

That keeps the theorem side centered on one sentence:

> On the active best-seed branch, D5 is an odometer with one corner.

## 11. What not to reopen on the theorem side

The cleanup is specifically meant to avoid drifting back into broad theorem
search. The theorem side should **not** reopen:

- new theorem objects;
- new scheduler extraction;
- new boundary-reset extraction as a separate project;
- new broad support computations;
- controller-search reformulations.

The remaining theorem-side work is narrower:

- final statement polishing,
- proof compression,
- dependency bookkeeping,
- notation normalization.

That is why the theorem package should now be treated as near-stable in shape.
