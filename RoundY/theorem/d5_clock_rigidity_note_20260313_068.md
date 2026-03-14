# D5 clock rigidity note (2026-03-13)

This note works on the `067` rigidity route.

The key point of `067` is that the rigidity side should no longer be phrased as
just a size lower bound. The intended statement is stronger:

> once the exact reduction object is fixed, any exact realization must transport
> every theorem-side coordinate on its accessible exact part.

The route note says the reason should be:

1. exact carry words separate states on the reduced object;
2. therefore any exact realization is injective there;
3. therefore every theorem-side coordinate, especially the canonical `beta`
   clock, transports uniquely.

The result below makes that precise.

---

## 1. General word-separation rigidity lemma

Let `(X,F,c)` be a deterministic dynamical system with binary readout
`c : X -> {0,1}`.
Let `A subset X` be a set on which the iterates `F^t` are defined for
`0 <= t < L`.
Define the length-`L` carry word map

```text
W_L(x) = ( c(x), c(Fx), ..., c(F^{L-1}x) ).
```

Assume `W_L` is injective on `A`.

Now let

```text
pi : A -> Q
```

be a putative exact realization on `A`, meaning there exists a transition map
`Fhat` on `pi(A)` and readout `chi : pi(A) -> {0,1}` such that, for every
`x in A` and every `0 <= t < L` for which `F^t x` stays in `A`,

```text
pi(Fx) = Fhat(pi(x)),
chi(pi(x)) = c(x).
```

Then `pi` is injective on `A`.

### Proof

If `pi(x)=pi(y)`, then by induction on `t` one gets

```text
pi(F^t x) = Fhat^t(pi(x)) = Fhat^t(pi(y)) = pi(F^t y)
```

for all `0 <= t < L` for which both sides are defined. Applying `chi` gives

```text
c(F^t x) = chi(pi(F^t x)) = chi(pi(F^t y)) = c(F^t y).
```

So `W_L(x)=W_L(y)`. Since `W_L` is injective on `A`, one gets `x=y`. ∎

---

## 2. Cycle rigidity theorem

Let

```text
C_m = {x_0, ..., x_{m-1}}
```

with cyclic map

```text
R(x_q) = x_{q+1 mod m}
```

and one-marked carry label

```text
c(x_q) = 1_{q=m-1}.
```

Then the length-`m` carry word map `W_m` is injective on `C_m`.
Indeed,

```text
W_m(x_q)
```

is the cyclic shift of `(0,0,...,0,1)` whose unique `1` occurs in position
`m-1-q`.
Different `q` give different positions of that unique `1`.

Therefore any exact realization

```text
pi : C_m -> Q,
pi o R = Rhat o pi,
c = chi o pi,
```

is injective.

This sharpens the older lower-bound proposition. One does not merely get
`|Q| >= m`; one gets that every exact quotient on the marked cycle is actually
one-to-one.

---

## 3. Chain rigidity theorem

The `067` note says the chain version is probably the safer first exact object:

a marked length-`m` chain extracted from the regular corridor.

So let

```text
P_m = {x_0, ..., x_{m-1}}
```

with successor map

```text
T(x_i) = x_{i+1}     for 0 <= i < m-1,
```

and one-marked terminal carry label

```text
c(x_i) = 1_{i=m-1}.
```

Suppose an exact realization on this chain is given by

```text
pi : P_m -> Q,
pi(Tx) = That(pi(x))  for 0 <= i < m-1,
c = chi o pi.
```

Then `pi` is injective on `P_m`.

### Proof

Assume `pi(x_i)=pi(x_j)` with `i<j`.
Apply the semiconjugacy `m-1-j` times. Then

```text
pi(x_{i+m-1-j}) = pi(x_{m-1}).
```

Applying `chi`,

```text
c(x_{i+m-1-j}) = c(x_{m-1}) = 1.
```

But `i+m-1-j < m-1` because `i<j`, so the left-hand side is actually `0`.
Contradiction. Hence `pi` is injective. ∎

Again, this is stronger than `|Q| >= m`. It says the exact quotient cannot
merge any two positions of the chain at all.

---

## 4. Transport corollary

Once injectivity is known, the advertised rigidity statement becomes formal.

Let `X_m` be either the marked cycle `C_m` or the marked chain `P_m`, and let
`pi : X_m -> Q` be an exact realization as above.
If `pi` is injective, then every coordinate

```text
f : X_m -> A
```

transports uniquely to `pi(X_m)` by

```text
fbar(pi(x)) := f(x).
```

This is well-defined because `pi` is injective.
It is the unique function on `pi(X_m)` satisfying

```text
f = fbar o pi.
```

So on the accessible exact part, an exact realization transports **all**
coordinates of the reduced object, not just the marked carry readout.

That is the precise version of the `067` slogan:

> exact carry words separate states;
> therefore exact realizations are injective;
> therefore every theorem-side coordinate transports uniquely.

---

## 5. D5 clock-rigidity corollary

Now specialize only at the level that the current handoffs justify.

Assume that for each odd `m` one has an accessible exact reduction object
`X_m` extracted from the active D5 branch, where `X_m` is either:

1. a one-marked cyclic section of size `m`, or
2. a one-marked length-`m` chain.

Assume also that on `X_m` the theorem-side coordinates are defined, in
particular the canonical clock coordinate

```text
beta : X_m -> Z/mZ,
```

with the theorem-side identification `beta = -kappa mod m` coming from the
phase-corner package.

Then any exact realization of the reduced dynamics on `X_m` that preserves the
marked carry observable is injective on `X_m`, and therefore transports
`beta` uniquely.

So the realization cannot carry merely “some compressed shadow” of the clock.
It must already carry **that same theorem-side clock** on its accessible exact
part.

This is exactly the rigidity claim sought in the current handoff.

---

## 6. Relation to the older lower-bound route

The older `064` proposition gave only

```text
|Q| >= m
```

for exact quotients of a one-marked cyclic section.

The injectivity theorem proved above strictly sharpens that:

```text
pi is injective on the exact section/chain.
```

The size lower bound is then immediate, but injectivity gives much more:

- it rules out every nontrivial exact collapse on the accessible exact part;
- it forces transport of every theorem-side coordinate;
- it identifies clock rigidity as a transport theorem, not merely a counting
  argument.

So the old “negative route” really is better read as rigidity.

---

## 7. What remains open

This note does **not** prove the D5-specific extraction of the exact reduction
object.

The remaining D5-specific tasks are still:

1. extract and validate the correct accessible exact object `X_m`
   (chain first seems safer than cycle);
2. prove the intended local/admissible class factors through a quotient of that
   exact object;
3. then apply the rigidity theorem above.

So the abstract rigidity theorem is done, but the D5-specific reduction step is
still the live frontier.

---

## 8. Clean theorem to target next

The best next theorem now looks like this.

### D5 exact-chain rigidity theorem

For each odd `m`, let `X_m` be the accessible marked length-`m` exact chain
extracted from the regular corridor of the active best-seed branch.
Suppose a local/admissible mechanism is exact on `X_m` in the sense that it
induces a semiconjugate quotient preserving current carry.
Then the induced quotient is injective on `X_m`.
Consequently every theorem-side coordinate on `X_m`, in particular the
canonical `beta` clock, transports uniquely to the realization.

This is, in my view, the right first rigidity theorem. The cycle theorem is
then a later strengthening if the chain is shown to close up as a literal
cyclic return section.
