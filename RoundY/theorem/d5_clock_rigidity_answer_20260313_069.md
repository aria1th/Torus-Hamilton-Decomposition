# D5 clock rigidity answer (2026-03-13)

This note pushes the rigidity route from “injectivity of exact quotients” to a
cleaner answer:

> on the exact marked chain/cycle, the canonical clock is not merely
> transportable; it is intrinsically reconstructible from the future carry word.

So once the exact reduction object exists, there is no clock-choice ambiguity
left.

---

## 1. Model exact objects

There are two candidate exact objects.

### Cycle model

Let

```text
C_m = {x_0, ..., x_{m-1}},
R(x_i) = x_{i+1 mod m},
c(x_i) = 1_{i=m-1}.
```

### Chain model

Let

```text
P_m = {x_0, ..., x_{m-1}},
T(x_i) = x_{i+1}   (0 <= i < m-1),
c(x_i) = 1_{i=m-1}.
```

The current route notes say the chain version may be the safer first exact
object, while the cycle is a possible later strengthening.

---

## 2. The intrinsic clock on the exact object

### Cycle case

For `x in C_m`, define

```text
j(x) := the unique t in {0,...,m-1} such that c(R^t x)=1.
```

This is well-defined because the marked cycle has exactly one carry in each
full period.

Then

```text
j(Rx) = j(x) - 1 mod m.
```

Indeed, the unique carry position in the next `m` steps shifts left by one when
we move one step forward.

Also `j(x_{m-1}) = 0`, and more generally

```text
j(x_i) = m-1-i mod m.
```

So `j` is the canonical cyclic countdown-to-carry clock.

### Chain case

For `x in P_m`, define

```text
t(x) := min { r >= 0 : c(T^r x)=1 }.
```

This is well-defined because the marked endpoint is eventually reached exactly
once.

Then for `i < m-1`,

```text
t(Tx_i) = t(x_i) - 1,
```

with `t(x_{m-1}) = 0`, and explicitly

```text
t(x_i) = m-1-i.
```

Thus the chain also carries a canonical countdown clock. Under the natural
identification `{0,...,m-1} subset Z/mZ`, this is the same clock as in the
cycle model.

So chain vs cycle does **not** create a clock ambiguity. It only affects
whether the final return edge has already been proved.

---

## 3. Uniqueness of the clock

Suppose `gamma_1, gamma_2 : C_m -> Z/mZ` both satisfy

```text
gamma_k(Rx) = gamma_k(x) - 1.
```

Then `d := gamma_1-gamma_2` satisfies `d(Rx)=d(x)`, hence is constant on the
whole cycle. So the clock is unique up to an additive constant.

The same proof works on the chain: if

```text
gamma_k(Tx) = gamma_k(x) - 1,
```

then `gamma_1-gamma_2` is constant along the chain.

If we normalize by requiring the marked carry state to have value `0`, then the
constant is fixed, so the canonical clock is unique.

Hence there is exactly one normalized unit-drift clock on the exact chain/cycle.

---

## 4. Exact realization rigidity, sharpened

Let `X_m` denote either `C_m` or `P_m`, and let

```text
pi : X_m -> Q
```

be an exact realization preserving current carry, with induced transition map on
`Q`.

Previous rigidity already showed: such a `pi` is injective on `X_m`.

But now we can say more.

Because exactness preserves the whole future carry word, the intrinsic clock can
be reconstructed **directly on `Q`**:

- in the cycle case, `j_Q(q)` is the position of the unique `1` in the next
  length-`m` carry word from `q`;
- in the chain case, `t_Q(q)` is the first time to the terminal carry.

These satisfy the same drift law as above and coincide with the transported
clock from `X_m`.

So the clock is not only transported uniquely after injectivity is known;
**it is definable from the exact carry future itself**.

This is the real rigidity answer.

---

## 5. D5 consequence

The route notes identify the constructive clock and theorem-side phase by

```text
beta = -kappa mod m.
```

Therefore, once the D5 exact reduction object is fixed as a marked length-`m`
chain or one-marked cyclic `m`-section, any exact realization must carry the
clock obtained from the future carry-word position. By uniqueness of normalized
unit-drift clocks, that clock is exactly the canonical `beta`.

So the D5 rigidity question has the following answer.

### Clock rigidity answer

If the accessible exact reduction object exists and is the expected marked
chain/cycle, then **yes**: exactness forces the canonical `beta` clock. There is
no room for a different exact `m`-clock.

The only remaining D5-specific gap is **not** clock ambiguity. It is the
reduction step:

1. extract/validate the exact marked chain or cycle from the active branch;
2. prove the intended local/admissible class factors through an exact quotient
   of that object.

After that, the clock is already determined.

---

## 6. Best next theorem statement

The clean theorem to target is:

### D5 intrinsic clock rigidity theorem

Let `X_m` be the accessible exact marked chain/cycle extracted from the active
best-seed branch. Let `Q` be any exact realization of current carry on `X_m`.
Then the function on `Q` given by the unique future-carry position (equivalently,
first time to marked carry) is the unique normalized unit-drift clock on the
accessible exact part. Under the theorem-side identification `beta = -kappa`,
this clock is exactly the canonical `beta`.

That is stronger than the earlier size lower bound, and stronger even than bare
injective transport.
