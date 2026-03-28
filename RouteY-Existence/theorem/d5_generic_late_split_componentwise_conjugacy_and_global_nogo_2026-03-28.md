# d=5 generic-late split branch: componentwise odometer conjugacy for `N_t`, and why a single global odometer for `g_t` cannot be the universal theorem
Date: 2026-03-28

## Goal

Try the conjugacy route suggested by the D3/D4 reading, but do it honestly.

The March 27/28 notes already give a complete split-branch theorem for the
first-special-hit map

```text
N_t : Z_M -> Z_M
```

in the good arithmetic classes

```text
m=3M >= 33,
5∤m,
7∤M,
m ≡ 3 or 9 (mod 15),
M ≡ 2 (mod 3).
```

This note repackages that result as an explicit **componentwise odometer
conjugacy theorem**.  It then explains why the hoped-for stronger statement

```text
g_t = τ_{δ_M} ∘ N_t  is globally conjugate to a single translation on Z_M
```

cannot be the universal theorem for the split branch.

So the positive result here is theorem-order.
The negative result is also mathematically decisive, but only as a **no-go for a
uniform global odometer statement**; it does not yet replace the still-open final
cycle theorem for `g_t`.

---

## 1. Imported inputs

Assume throughout:

```text
m=3M >= 33,
5∤m,
7∤M,
m ≡ 3 or 9 (mod 15),
M ≡ 2 (mod 3),
t is generic late.
```

Write

```text
Q := (M-2)/3.
```

Then the already-proved generic-late active theorem says that the active
permutation `p_gen` has cycle type

```text
Q, Q+1, Q+1.
```

Let:

- `C_*` be the unique active cycle containing `u=1`;
- `C_Q` be the nondefect active cycle of length `Q`;
- `C_{Q+1}` be the remaining nondefect active cycle of length `Q+1`.

The March 28 split-branch theorem for `N_t` proves:

1. on `C_Q`, one has
   ```text
   N_t|_{C_Q} = p_gen^5;
   ```
2. on `C_{Q+1}`, one has
   ```text
   N_t|_{C_{Q+1}} = p_gen^{-4};
   ```
3. on the defect cycle `C_*`, after removing the distinguished point `u_0=1`,
   the map becomes a rigid translation on the remaining `Q` points.

We now package this as a conjugacy theorem.

---

## 2. Straightening coordinates on the three active circles

Index the defect cycle in `p_gen`-order as

```text
C_* = (u_0,u_1,...,u_Q),
u_0 = 1,
u_{j+1}=p_gen(u_j).
```

Let

```text
x : C_* \ {u_0} -> Z_Q
```

be the coordinate

```text
x(u_j)=j-1      (1 <= j <= Q).
```

Likewise, choose `p_gen`-order coordinates

```text
y : C_Q -> Z_Q,
z : C_{Q+1} -> Z_{Q+1},
```

so that `p_gen` becomes translation by `+1` in the `y`- and `z`-coordinates.

### Proposition 2.1 (split defect circle = fixed point plus odometer)

In the split branch, the defect component of `N_t` is conjugate to a fixed point
plus a rigid rotation on `Z_Q`.

More precisely:

- if `m=15r+3` with `r ≡ 2 (mod 3)`, set
  ```text
  a_* := (r+1)/3.
  ```
  Then
  ```text
  x(N_t(u_j)) = x(u_j) - a_*    (mod Q)
  ```
  for every `1 <= j <= Q`;

- if `m=15r+9` with `r ≡ 1 (mod 3)`, set
  ```text
  a_* := (r-1)/3.
  ```
  Then
  ```text
  x(N_t(u_j)) = x(u_j) + a_*    (mod Q)
  ```
  for every `1 <= j <= Q`.

In both cases `u_0` is fixed.

#### Proof

This is exactly the content of the March 28 split defect propositions, rewritten
in the coordinate `x=j-1`.

- In the class `15r+3`, the proof there shows that on `{1,...,Q}` the map is
  `x -> x-a_* (mod Q)`.
- In the class `15r+9`, the proof there shows that on `{1,...,Q}` the map is
  `x -> x+a_* (mod Q)`.

The point `u_0` is fixed in both formulas. ∎

### Proposition 2.2 (nondefect circles are odometers)

In the same coordinates, one has

```text
y ∘ N_t ∘ y^{-1}(ξ) = ξ + 5           (mod Q),
z ∘ N_t ∘ z^{-1}(η) = η - 4           (mod Q+1).
```

#### Proof

This is the already-proved nondefect power law

```text
N_t|_C = p_gen^{m-1 mod |C|},
```

together with

```text
m-1 = 9Q+5,
m-1 ≡ 5    (mod Q),
m-1 ≡ -4   (mod Q+1).
```

Because the `y`- and `z`-coordinates were chosen so that `p_gen` is `+1`, the
displayed formulas follow. ∎

---

## 3. The conjugacy theorem for `N_t`

Define the model space

```text
S_Q := {⋆} ⊔ Z_Q^{(def)} ⊔ Z_Q^{(nd)} ⊔ Z_{Q+1},
```

where `⋆` is a singleton, the superscripts only distinguish the two copies of
`Z_Q`, and the model map `T_Q : S_Q -> S_Q` by

- `T_Q(⋆)=⋆`;
- on `Z_Q^{(def)}`:
  - `ξ -> ξ-a_*` in the class `15r+3`,
  - `ξ -> ξ+a_*` in the class `15r+9`;
- on `Z_Q^{(nd)}`:
  ```text
  ξ -> ξ+5;
  ```
- on `Z_{Q+1}`:
  ```text
  η -> η-4.
  ```

Let

```text
H : Z_M -> S_Q
```

be the bijection defined by:

- `H(u_0)=⋆`;
- `H(u_j)=x(u_j)` on `C_* \ {u_0}`;
- `H=v` on `C_Q` via `y`;
- `H=w` on `C_{Q+1}` via `z`.

### Theorem 3.1 (componentwise odometer conjugacy for the split first-special-hit map)

Under the standing assumptions,

```text
H ∘ N_t ∘ H^{-1} = T_Q.
```

Equivalently: in the split branch, `N_t` is **exactly conjugate** to the disjoint
union of

- one fixed point,
- one rigid odometer on `Q` points coming from the defect circle,
- one rigid `+5` odometer on `Q` points,
- one rigid `-4` odometer on `Q+1` points.

#### Proof

This is immediate from Propositions 2.1 and 2.2, because the four components are
disjoint and together exhaust `Z_M`. ∎

### Corollary 3.2 (the split-branch cycle theorem for `N_t`)

The cycle multiset of `N_t` is

```text
{1, Q}
∪ gcd(Q,5) copies of (Q/gcd(Q,5))
∪ gcd(Q+1,4) copies of ((Q+1)/gcd(Q+1,4)).
```

#### Proof

A translation by `s` on `Z_L` has `gcd(L,s)` cycles, all of length `L/gcd(L,s)`.
Apply that to the three odometer components in Theorem 3.1.

For the defect component we also use the already-proved gcd computation

```text
gcd(Q,a_*) = 1,
```

in both residue classes.  Hence the defect rotation is a single `Q`-cycle. ∎

So the conjugacy route **does succeed** at the `N_t` level.

---

## 4. Why this does not extend to a universal global odometer theorem for `g_t`

The final reduced base map is

```text
g_t = τ_{δ_M} ∘ N_t,
```

where `τ_{δ_M}(u)=u+δ_M`.

A priori one might hope that `g_t` itself is also conjugate to a single
translation

```text
x -> x+c
```

on `Z_M`.  But that cannot be the universal theorem, even inside the split
good branch.

### Lemma 4.1 (translation conjugacy forces equal cycle lengths)

If a permutation `F` of `Z_M` is conjugate to a translation

```text
x -> x+c   (mod M),
```

then all cycles of `F` have the same length

```text
M / gcd(c,M).
```

#### Proof

Conjugate permutations have the same cycle structure.  A translation by `c`
decomposes `Z_M` into `gcd(c,M)` cycles, all of the same length
`M/gcd(c,M)`. ∎

So any instance of `g_t` having unequal cycle lengths is an immediate obstruction.

### Proposition 4.2 (prime-size counterexamples to a global odometer theorem)

There are split-branch good moduli with prime `M` for which `g_t` has unequal
cycle lengths.  For example:

- `m=69`, `M=23` prime, and exact computation gives
  ```text
  cycle_type(g_t) = [17,3,3];
  ```
- `m=123`, `M=41` prime, and exact computation gives
  ```text
  cycle_type(g_t) = [31,5,5].
  ```

Hence in these moduli `g_t` is **not** conjugate to any translation on `Z_M`.

#### Proof

Because `M` is prime, any nonzero translation on `Z_M` is a single `M`-cycle,
while the zero translation is the identity.

But the displayed exact cycle types are neither `[M]` nor `[1,1,...,1]`.
So by Lemma 4.1 these examples cannot be translation-conjugate. ∎

This is enough to show that a **uniform global single-odometer theorem for `g_t`
is false**, even in the good split branch.

---

## 5. Evidence from the exact split-branch scan

Companion report:
`d5_generic_late_conjugacy_attempt_split_branch_report_2026-03-28.txt`

On the exact range

```text
33 <= m <= 1501,
5∤m,
7∤M,
m ≡ 3 or 9 (mod 15),
M ≡ 2 (mod 3),
```

there are `29` split-branch good moduli in the two residue classes covered by
the explicit reduced-base theorem.

Among them:

- only `5` give a single cycle for `g_t`;
- `24` are not single-cycle.

This does **not** prove a general theorem about `g_t`, but it strongly supports
the conclusion of Proposition 4.2: whatever the final theorem is, it is not
going to be a universal statement of the form

```text
g_t  is globally conjugate to one odometer on Z_M.
```

---

## 6. What survives from the conjugacy idea

The D3/D4 odometer idea is still valuable, but now in the right form.

### Closed here

- the split-branch map `N_t` is fully solved by an explicit odometer conjugacy;
- the hoped-for universal single-odometer theorem for `g_t` is decisively ruled
  out by prime-size counterexamples.

### What remains plausible

- a **piecewise** or **return-map** odometer conjugacy for `g_t`;
- or a hand analysis of the explicit finite permutation from the March 27 reduced
  base-machine theorem.

So the correct lesson is:

```text
odometer at the second section = yes,
single global odometer after the ambient splice translation = no, not uniformly.
```

That is exactly the sort of “some cases close by conjugacy, some by hand” split
that already appeared in the D3 proof.
