# D5 theorem package continuation after concentrated handoff 067

This note continues only the **theorem side** of the `067` handoff. It does
not include compute support and it does not reopen the clock-descent or
rigidity branches.

The goal is to turn the theorem side into a compact manuscript package with:

1. one structural reduction theorem,
2. one main odometer theorem,
3. countdown/reset laws presented strictly as corollaries,
4. the canonical `beta` clock recorded only as a gauge-equivalence remark.

## 1. Scope and exact dependency bookkeeping

The theorem-side package is now best organized around the chain

- `033 -> 062 -> 059 -> phase-corner theorem -> countdown/reset corollaries`.

What is treated here as **imported**:

- the explicit trigger family from `033`;
- the mixed-witness scheduler on `B` and its finite-cover propagation from
  `059`.

What is treated here as **derived/packageable**:

- the universal first-exit theorem `062` from the trigger family;
- pre-exit `B`-region invariance;
- the main phase-corner theorem;
- the countdown law and the branchwise reset laws;
- the gauge equivalence `beta = -kappa`.

So this note is manuscript-facing, but still conditional on the upstream
statements just listed.

## 2. Main theorem object and proof gauges

The theorem object should remain minimal:

- `B = (s,u,v,layer,family)`;
- `tau`;
- `epsilon4`.

The following are proof or constructive gauges only:

- raw corridor coordinates `(q,w,u,Theta)`;
- source residue `rho = u_source + 1`;
- theorem clock `kappa = q+s+v+layer mod m`;
- constructive clock `beta = -kappa mod m`.

The main theorem should not be stated in terms of `rho`, `Theta`, or `beta`.
Those coordinates are useful only in the proof.

## 3. Structural reduction theorem

### Imported trigger input (`033`)

Adopt the lifted-corridor notation `(q,w,u,Theta)`. The exact trigger family is

```text
H_{L1} = {(q,w,u,Theta) = (m-1,m-1,u,2) : u != 2}.
```

This is the only nonlocal structural input needed to determine the first exit.

### Candidate lifted orbit

Fix odd `m >= 5`, the best seed, and the post-entry active state

```text
x_0 = (q,w,u,Theta) = (m-1,1,u_source,2).
```

Set

```text
rho := u_source + 1 mod m.
```

On `B`-labelled current states, the mixed-witness rule induces the lifted step

```text
F(q,w,u,0)     = (q+1, w,                 u,   1)
F(q,w,u,1)     = (q,   w,                 u+1, 2)
F(q,w,u,2)     = (q,   w + 1_{q=m-1},     u,   3)
F(q,w,u,Theta) = (q,   w,                 u,   Theta+1)   for 3 <= Theta <= m-1
```

with `Theta` read modulo `m`.

### Lemma 3.1 (phase-1 invariant)

Every phase-1 state on the candidate lifted orbit satisfies

```text
q = u - rho + 1 mod m.
```

#### Proof

The first phase-1 state is `(0,2,u_source,1)`, so the identity holds there.
From one phase-1 state to the next, exactly one `u` increment occurs at phase
`1` and exactly one `q` increment occurs later at phase `0`. So both sides
increase by one. ∎

### Lemma 3.2 (only two possible trigger sites)

Only two phase-1 states can enter `H_{L1}` in one alternate step:

```text
A = (m-1,m-2,1),
B = (m-2,m-1,1).
```

#### Proof

The target family lies at phase `Theta = 2`, so only a phase-1 state can step
into it. Reaching `q' = w' = m-1` in one alternate step leaves only the two
listed possibilities. ∎

### Lemma 3.3 (universal first exits)

At the two possible trigger sites,

```text
u(A) = rho - 2 mod m,
u(B) = rho - 3 mod m.
```

Since `H_{L1}` requires `u != 2`, the first actual exit target is

```text
T_reg = (m-1,m-2,1)   if rho != 4,
T_exc = (m-2,m-1,1)   if rho = 4.
```

#### Proof

The values of `u(A)` and `u(B)` follow from Lemma 3.1. If `rho != 4`, then
`u(A) != 2`, so the earlier site `A` is active and is the first exit. If
`rho = 4`, then `u(A) = 2`, so `A` is blocked, while `u(B) = 1 != 2`, forcing
first exit at `B`. ∎

### Lemma 3.4 (pre-exit avoidance of patched classes)

Before the candidate first exit, no candidate current state lies in any patched
(non-`B`) current class.

#### Proof sketch

Three simple monotonicity/order facts are enough.

1. `w` starts at `1`, changes only at phase `Theta = 2` when `q = m-1`, and
   never decreases. Therefore every patched class with `w = 0` is impossible.
2. The value `w = 1` occurs only at the entry state, which has `Theta = 2`, so
   the patched class with `(w,Theta) = (1,3)` never occurs.
3. The `L1`-type patch `(q,w,Theta) = (m-1,m-1,1)` lies strictly after the
   universal exit target on both families:
   - on the regular family the orbit exits already at `A = (m-1,m-2,1)`;
   - on the exceptional family, once `w` first reaches `m-1`, the phase-1
     states with `w = m-1` appear in the order
     `(0,m-1,1), (1,m-1,1), ..., (m-2,m-1,1), (m-1,m-1,1)`,
     so the orbit exits at `B = (m-2,m-1,1)` before `L1` can occur.

Hence every pre-exit candidate current state is `B`-labelled. ∎

### Lemma 3.5 (actual branch equals candidate branch up to first exit)

The actual active branch agrees with the candidate lifted orbit up to first
exit.

#### Proof

The two branches start at the same post-entry state. Assume they agree at time
`n` before the candidate first exit. By Lemma 3.4 the common current state is
`B`-labelled, so the actual update is unmodified there and equals the
mixed-witness step used to define the candidate orbit. Therefore the two
branches also agree at time `n+1`. ∎

### Theorem 3.6 (structural reduction / B-region invariance)

On the active best-seed branch:

1. the first exit target is universal and equals `T_reg` or `T_exc` according
   to whether `rho != 4` or `rho = 4`;
2. every pre-exit active current state is `B`-labelled.

#### Proof

Combine Lemmas 3.3, 3.4, and 3.5. ∎

This theorem is the clean manuscript version of the `062` bridge.

## 4. Main theorem: D5 is an odometer with one corner

Define on the active nonterminal branch

```text
kappa := q + s + v + layer mod m,
c     := 1_{q = m-1}.
```

### Imported scheduler input (`059`)

On `B`-labelled active states, the mixed-witness rule yields the current-state
scheduler

```text
kappa' = kappa + 1 mod m,
```

and

```text
kappa = 0  -> wrap,
kappa = 1  -> carry_jump,
kappa = 2  -> other_1000 iff c = 1, else flat,
kappa = 3  -> other_0010 iff (c = 0 and s = 2) or (c = 1 and s != 2), else flat,
kappa = 4,...,m-1 -> flat.
```

This is the exact content imported from `059` in theorem gauge.

### Theorem 4.1 (phase-corner theorem)

Fix odd `m >= 5` and the best seed. On the active nonterminal branch,

1. `kappa' = kappa + 1 mod m`;
2. the current event `epsilon4` is determined by `(kappa,c,s)` through the
   scheduler above;
3. among flat states, the only short corner is `(kappa,s) = (2,2)`.

Equivalently: **on the active best-seed branch, D5 is an odometer with one
corner.**

#### Proof

By Theorem 3.6, every pre-exit active current state is `B`-labelled. Therefore
`059` applies there and gives the scheduler directly. Finite-cover
compatibility propagates that same current-state machine across the full active
nonterminal branch. The listed event table shows immediately that the only flat
state not governed by the ordinary odometer countdown is the corner
`(kappa,s) = (2,2)`. ∎

## 5. Countdown and reset corollaries

The theorem package should present these as consequences of Theorem 4.1, not as
separate primary theorems.

### Corollary 5.1 (countdown law)

On the active nonterminal branch,

```text
tau = 0                                         on nonflat states,
tau = 1                                         at the flat corner (kappa,s) = (2,2),
tau = m-kappa                                  on all other flat states.
```

In particular,

```text
tau' = tau - 1
```

whenever `tau > 0`.

#### Proof

Nonflat states are exactly the branch-reset states, so `tau = 0` there. On flat
states away from the short corner, Theorem 4.1 says that the branch follows the
ordinary odometer phase; this gives `tau = m-kappa`. At `(kappa,s) = (2,2)` the
flat countdown is shortened by one step, so `tau = 1`. Since `kappa' = kappa+1`,
all positive flat countdowns decrease by one at the next step, including the
boundary case `kappa = m-1`, where the next state is wrap and `tau' = 0`. ∎

### Corollary 5.2 (branchwise reset laws)

The next countdown value on a current nonflat state is:

```text
wrap -> 0,
carry_jump -> 0    if c = 1,
carry_jump -> 1    if c = 0 and s = 1,
carry_jump -> m-2  if c = 0 and s != 1,
other_1000 -> m-3  if s = 1,
other_1000 -> 0    if s != 1,
other_0010 -> m-4.
```

#### Proof sketch

This is the one-step reset table obtained by combining Theorem 4.1 with the
current-to-next branch transition data already packaged in `059` and the
finite-cover chain `B <- B+c <- B+c+d`.

The point is that Theorem 4.1 reduces every reset computation to a small number
of corner cases at `kappa = 0,1,2,3`. The successor countdown is then read from
Corollary 5.1 after transporting the current event through the imported
one-step transition table. That case check yields exactly the displayed values:

- `wrap -> 0`;
- `carry_jump -> 0,1,m-2` according to `(c,s)`;
- `other_1000 -> m-3` if `s = 1`, else `0`;
- `other_0010 -> m-4`.

So the reset laws are not independent theorems. They are the finite list of
nonflat successor countdowns forced by the phase-corner machine. ∎

### Corollary 5.3 (finite-cover compatibility)

The current-state scheduler and the countdown/reset laws are compatible with

```text
B <- B+c <- B+c+d.
```

#### Proof sketch

This is the finite-cover propagation imported from `059`, now restated at the
level of Theorem 4.1 and Corollaries 5.1-5.2. The point is that the theorem-side
machine is not an auxiliary `B`-only formula; it is the same current-state
machine seen through the finite-cover chain. ∎

## 6. Canonical clock as a theorem-side gauge remark

The theorem package should keep `beta` out of the main statement, but it is
useful to record the gauge equivalence explicitly.

### Proposition 6.1 (`beta` is the same clock in another gauge)

Define

```text
beta := -kappa mod m.
```

Then on the active branch,

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

Immediate from Theorem 4.1 by the change of variables `beta = -kappa`. ∎

## 7. Recommended manuscript order

The theorem section can now be written in the following order.

1. State the theorem object `(B,tau,epsilon4)` and define the proof gauge
   `kappa = q+s+v+layer`.
2. Quote the explicit trigger theorem from `033`.
3. Prove the structural reduction theorem (Theorem 3.6), which is the clean
   content of `062`.
4. Quote the `059` scheduler on `B` and finite-cover propagation.
5. Promote those inputs to the phase-corner theorem (Theorem 4.1).
6. Derive the countdown law and reset table as corollaries.
7. Record `beta = -kappa` only as a gauge-equivalence remark.

This keeps the manuscript centered on one theorem: **D5 is an odometer with one
corner.**

## 8. Honest theorem-side frontier

The theorem side no longer looks exploratory. The remaining work is largely
editorial and dependency-cleanup:

- quote `033` in final form;
- quote `059` in the exact scheduler/cover-propagation form actually needed;
- streamline the proof of Theorem 3.6 into manuscript notation;
- keep `CJ`, `OTH`, and reset laws corollaries rather than parallel theorems.

So the theorem package now looks close to closure in shape.
