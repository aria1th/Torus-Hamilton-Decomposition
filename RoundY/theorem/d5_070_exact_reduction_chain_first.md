# D5 exact reduction: chain first, quotient second

This note works only on the **exact reduction** side.

It takes as already packaged:

- the structural theorem up to first exit,
- the regular/exceptional split,
- the raw lifted candidate orbit,
- and the theorem-side phase package.

The goal is to pin down the right exact object before discussing realization.

The main conclusion is:

> The safe first exact reduction object is a **marked length-`m` chain** on the
> regular corridor.
>
> A literal `m`-cycle is a secondary **periodization** of that chain, not the
> first exact object on actual states.

After that, the correct quotient to study is the quotient induced by the
intended local/admissible class **on that chain itself**.

---

## 1. Setup

Fix odd `m >= 5` and the regular family (`rho != 4`).

By the structural reduction already packaged, the actual active branch agrees
with the lifted candidate orbit up to first exit, and on the regular family the
first exit occurs at

```text
A = (m-1, m-2, 1).
```

Write the lifted coordinates as

```text
(q, w, u, Theta)
```

with the candidate evolution

```text
(q,w,u,0)     -> (q+1, w,                 u,   1)
(q,w,u,1)     -> (q,   w,                 u+1, 2)
(q,w,u,2)     -> (q,   w + 1_{q=m-1},     u,   3)
(q,w,u,Theta) -> (q,   w,                 u,   Theta+1)   for 3 <= Theta <= m-1.
```

We use the current carry mark

```text
c = 1_{q = m-1}.
```

---

## 2. The exact marked chain on the regular corridor

### Lemma 2.1 (the `Theta = 2` slice has a closed first-return law before exit)

On the candidate orbit, every pre-exit state with `Theta = 2` satisfies

```text
u = q + rho mod m.
```

Hence the pre-exit `Theta = 2` states are determined by `(q,w)` alone.

#### Proof

At a `Theta = 2` state, the previous state has `Theta = 1` with the same `q,w`
and `u-1`. The phase-1 invariant on the candidate orbit is

```text
q = (u-1) - rho + 1 = u - rho mod m.
```

So `u = q + rho mod m` on every `Theta = 2` state. ∎

### Lemma 2.2 (first-return map on the `Theta = 2` slice)

Let `R` be the first-return map to the slice `Theta = 2` along the candidate
orbit, before first exit. Then

```text
R(q,w,2) = (q+1, w, 2)                 if q != m-1,
R(m-1,w,2) = (0, w+1, 2)               if q = m-1,
```

as long as the return occurs before first exit.

#### Proof

From `(q,w,u,2)`, one step at phase `2` gives

```text
(q, w + 1_{q=m-1}, u, 3).
```

The subsequent steps through phases `3,4,...,m-1` leave `q,w,u` unchanged and
return to phase `0`. Then phase `0` increments `q` by `1`, and phase `1`
increments `u` by `1`, returning to phase `2`. Projecting to `(q,w,Theta)`
yields the displayed formula. ∎

### Theorem 2.3 (regular corridor = concatenation of exact marked chains)

Define, for each

```text
w = 2,3,...,m-3,
```

the block

```text
C_w = { x_{w,q} : 0 <= q <= m-1 },
```

where `x_{w,q}` is the unique pre-exit active state with lifted coordinates

```text
(q, w, Theta) = (q, w, 2).
```

Then:

1. every `C_w` exists on the actual regular branch;
2. on `C_w`, the first-return dynamics is
   ```text
   x_{w,q} -> x_{w,q+1}     for 0 <= q <= m-2;
   ```
3. the unique carry-marked state in `C_w` is `x_{w,m-1}`;
4. after the endpoint `x_{w,m-1}`, the next `Theta = 2` return is the start of
   the next block:
   ```text
   x_{w,m-1} -> x_{w+1,0};
   ```
5. there are exactly `m-4` such full blocks before regular exit.

So each `C_w` is an exact **marked length-`m` chain** with a unique carry
endpoint, and the regular corridor is the concatenation

```text
C_2, C_3, ..., C_{m-3}
```

followed by a final partial block at `w = m-2`.

#### Proof

Start from the post-entry state `(m-1,1,2)`. One full return to `Theta = 2`
passes through the phase-`2` carry increment at `q=m-1`, so the first returned
`Theta = 2` state is `(0,2,2)`. By Lemma 2.2, while `q != m-1` the return map
increments `q` and keeps `w` fixed. Thus for each fixed `w`, the slice states
are visited in the order

```text
(0,w,2), (1,w,2), ..., (m-1,w,2).
```

At `q=m-1`, Lemma 2.2 increments `w`, so the next returned `Theta = 2` state is
`(0,w+1,2)`.

Because the actual regular branch exits at the phase-1 state `(m-1,m-2,1)`, the
full returned `Theta = 2` blocks are exactly those with `w=2,...,m-3`. The next
block `w=m-2` is only partial, since from `(m-2,m-2,2)` the branch reaches the
exit state `(m-1,m-2,1)` before returning to `Theta = 2`.

The carry mark is `c = 1_{q=m-1}`, so within each full block the unique
carry-marked state is the endpoint `q=m-1`. Since actual branch = candidate
orbit up to first exit, the statement holds on the actual branch as well. ∎

### Corollary 2.4 (the first exact object is a chain, not yet a cycle)

Let

```text
L_m = ({0,1,...,m-1}, sigma, c)
```

with

```text
sigma(i) = i+1   for 0 <= i <= m-2,
```

and endpoint mark

```text
c(i) = 1_{i=m-1}.
```

Then each full block `C_w` is canonically isomorphic to `L_m` as a deterministic
marked object.

So the correct first exact reduction theorem is a theorem about `L_m`, not about
a literal cyclic return section on actual states.

---

## 3. Why a cycle is only a later strengthening

The actual block law is

```text
x_{w,m-1} -> x_{w+1,0},
```

not

```text
x_{w,m-1} -> x_{w,0}.
```

So on actual states, a fixed block is not closed under successor.

There is a natural *periodization* of the abstract chain `L_m`, obtained by
replacing the endpoint exit by wraparound:

```text
sigma_bar(i) = i+1 mod m.
```

Call the resulting marked cycle `Lbar_m`.

This `Lbar_m` is mathematically natural, but it is **not** the first exact
object extracted from actual branch states. It appears only after one performs a
secondary identification that forgets which full block `C_w` one is in.

So the right order is:

1. prove the exact marked-chain theorem on actual states;
2. define the quotient induced by the intended class on that chain;
3. only then ask whether that quotient is already blind to block index and so
   descends further to the periodized cycle.

That is the precise sense in which the chain is the safer first object and the
cycle is a later strengthening.

---

## 4. The exact quotient induced by the intended class

The next object should be defined on the chain `L_m`, not on the whole active
branch.

### Definition 4.1 (restricted observable of the intended class)

Fix the intended local/admissible class, and let

```text
o_m : L_m -> Omega_m
```

be its current-state descriptor restricted to one full chain block.

This could be:

- the actual local state produced by the intended mechanism, or
- any canonical current descriptor that the intended class exposes.

The only requirement here is that it be evaluated **on the chain states**.

### Definition 4.2 (accessible quotient induced by the intended class)

Define an equivalence relation `~_m` on `L_m` by

```text
i ~_m j
```

iff for every forward time `t` for which both `sigma^t(i)` and `sigma^t(j)` are
still inside `L_m`, one has

```text
o_m(sigma^t(i)) = o_m(sigma^t(j)).
```

Equivalently, `i` and `j` have the same entire forward observation word inside
the chain.

Then the quotient

```text
Q_m = L_m / ~_m
```

is the coarsest deterministic quotient of `L_m` through which the intended
class factors on that block.

This `Q_m` is the correct first quotient to study.

### Why this is the right quotient

- It is taken on the exact reduction object itself.
- It is deterministic by construction.
- It ignores the rest of the raw rule space.
- It is the exact analogue of the minimal right-congruence / Nerode quotient for
  the chain dynamics.

So any theorem about the intended class should first be stated for `Q_m`.

---

## 5. Rigidity on the chain: exact carry forces injectivity

The chain already carries a strong exactness theorem.

### Proposition 5.1 (any exact carry quotient of the marked chain is injective)

Let `pi : L_m -> Q` be a deterministic quotient of the marked chain `L_m`.
Assume the carry mark factors exactly through `pi`, i.e. there exists

```text
chi : Q -> {0,1}
```

such that

```text
c = chi o pi.
```

Then `pi` is injective. In particular,

```text
|Q| >= m.
```

#### Proof

Suppose `pi(i) = pi(j)` with `i < j`.
Let

```text
t = m-1-j.
```

Then after `t` chain steps,

```text
sigma^t(j) = m-1,
```

so `c(sigma^t(j)) = 1`, while

```text
sigma^t(i) = m-1-(j-i) < m-1,
```

so `c(sigma^t(i)) = 0`.

Because `pi` is a deterministic quotient, equal states remain equal under every
common forward iterate:

```text
pi(sigma^t(i)) = pi(sigma^t(j)).
```

Applying `chi` gives

```text
c(sigma^t(i)) = c(sigma^t(j)),
```

a contradiction. Therefore no two distinct chain states can merge. ∎

### Corollary 5.2

If the intended class is exact enough on the chain to recover current carry,
then its induced quotient `Q_m` on the chain already has size at least `m`.

So the marked-chain theorem is already strong enough for the lower-bound side;
one does not need a literal cycle first.

---

## 6. Periodized cycle and the short-corner clock

The chain is the first exact object, but the cycle becomes useful once one asks
for the canonical clock.

### Definition 6.1 (periodized cycle)

Let `Lbar_m` be the periodization of `L_m` obtained by replacing the endpoint
exit by wraparound:

```text
sigma_bar(i) = i+1 mod m.
```

Assume `Lbar_m` is endowed with the current event label `epsilon4` coming from
the theorem-side phase-corner machine, so that there is a unique short-corner
state `r_m` characterized by the two-step signature

```text
(epsilon4(x), epsilon4(sigma_bar(x))) = (flat, other_0010).
```

(This is exactly the short-corner characterization suggested in the current
handoff.)

### Proposition 6.2 (exact `epsilon4` quotient recovers the canonical clock)

Let

```text
pi_bar : Lbar_m -> Qbar
```

be a deterministic quotient of the periodized cycle, and assume `epsilon4`
factors exactly through `pi_bar`.

Then the short corner descends to a unique quotient state `rbar`, and the
function

```text
beta_bar(y) = least t >= 0 with sigma_bar^t(y) = rbar
```

is well-defined on `Qbar`. Up to additive gauge, `beta_bar` is the canonical
cycle clock.

#### Proof

Because `epsilon4` factors exactly and the quotient is deterministic, the
current-next event pair

```text
(epsilon4(y), epsilon4(sigma_bar(y)))
```

also factors through `Qbar`. By assumption there is exactly one cycle state with
signature `(flat, other_0010)`, so its image `rbar` is the unique quotient state
with that signature.

Now take two cycle states `x,x'` with `pi_bar(x)=pi_bar(x')`. Determinism implies
that their entire future `epsilon4` words agree. Therefore the first time at
which the short-corner signature appears in the future is the same for `x` and
for `x'`. So distance to the next short corner depends only on the quotient
state.

On the cycle, that distance is exactly the canonical clock up to an additive
choice of origin. Hence `beta_bar` is the descended canonical clock. ∎

### Interpretation

This is the clean realization route:

1. first extract the exact chain `L_m`;
2. compute the quotient induced by the intended class on `L_m`;
3. if that quotient is already invariant enough to periodize to `Lbar_m` and is
   exact for `epsilon4`, then the short corner forces the canonical clock.

So the chain theorem comes first, and the clock theorem comes after exactness of
the quotient has been established.

---

## 7. Recommended theorem order

The theorem-side order now looks like this.

### Step A. Structural platform

Use the already packaged structural chain

```text
033 -> 062 -> 059
```

to obtain the regular corridor and the phase-corner machine.

### Step B. Exact reduction theorem

State and prove Theorem 2.3:

> the regular corridor contains exact marked length-`m` chains `C_w`, and the
> abstract exact reduction object is `L_m`.

### Step C. Quotient theorem

Define the induced accessible quotient `Q_m` of the intended class on `L_m`.
This is the first quotient that should be computed or proved about.

### Step D. Rigidity theorem on the chain

Use Proposition 5.1:

> any exact carry quotient on `L_m` is injective.

### Step E. Realization / clock descent

Only after chain exactness is under control, ask whether the intended quotient
periodizes to `Lbar_m` and is exact for `epsilon4`; then Proposition 6.2 gives
the canonical clock.

---

## 8. Bottom line

The right exact-object statement is:

> **First exact object:** a marked length-`m` chain `L_m` extracted from the
> regular corridor.
>
> **Second exact object (if justified):** its periodized cycle `Lbar_m`.
>
> **Correct first quotient:** the deterministic quotient induced by the intended
> local/admissible class on `L_m` itself.

So yes: the mathematically safe order really is

```text
marked chain first,
then induced quotient on that chain,
then cycle only as a later strengthening.
```
