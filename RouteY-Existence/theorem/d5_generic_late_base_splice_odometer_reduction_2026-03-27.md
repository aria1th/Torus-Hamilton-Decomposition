# d=5 generic-late good branch: an odometer reduction for the reduced base splice
Date: 2026-03-27

## Goal

Continue the March 27 generic-late base-splice program after the `7`-split theorem, now using the
d3/d4 odometer viewpoint.

Assume throughout

```text
m = 3M >= 27,   5 ∤ m,   7 ∤ m,
```

and let `t` be generic late.

The previous notes already proved:

1. the good-branch special-source theorem
   ```text
   S_m(A) = A + Delta_m,     Delta_m = 7 * 5^{-1} (mod m),
   ```
2. the mod-3 reduced base machine
   ```text
   g_t(u) = (P_t^3(3u+1)-1)/3,
   ```
3. the full active generic-late theorem for the ordinary source map `p_gen`.

What is missing is an odometer-style structural theorem for the reduced base machine itself.

This note proves an exact intermediate reduction:

- the reduced base map `g_t` factors as a **constant splice translation**
  after a purely active **first-special-hit map** `N_t`;
- on every active cycle of `p_gen` **not** containing the anomaly `A=4`, the map `N_t`
  is just a constant power of `p_gen`;
- on the unique active cycle containing `A=4`, the map `N_t` is given by an explicit
  one-dimensional congruence minimization problem.  This is the exact defect-cycle
  odometer equation.

So the remaining arithmetic burden is no longer the raw base return `P_t`, and not even
the full reduced map `g_t`; it is concentrated in a single explicit defect cycle.

---

## 1. The active first-special-hit map

Work on the active residue class

```text
A = 3u+1,    u in Z_M.
```

Starting from the compact base state

```text
(A,0),
```

follow the **ordinary compact source return** until the first time the special row is hit.
Let

```text
N_t(u) in Z_M
```

be the active label of that first special source coordinate.

Equivalently, if the first special source state reached from `(A,0)` is

```text
(A_*, s(A_*)),
```

then

```text
A_* = 3 N_t(u) + 1.
```

This is the right second section suggested by the d3/d4 reading:
`N_t` lives entirely on the active arithmetic machine before the special branch fires.

---

## 2. Exact factorization of the reduced base map

Let

```text
P_t : B_m -> B_m
```

be the generic-late base next-return permutation, and let

```text
Delta_m = 7 * 5^{-1} (mod m),
delta_M = Delta_m (mod M) = 7 * 5^{-1} (mod M).
```

## Theorem 2.1 (factorization through the first-special-hit map)

For every `u in Z_M` one has

```text
P_t^3(3u+1) = 3 N_t(u) + 1 + 3 Delta_m    (mod m),
```

and therefore

```text
g_t(u) = N_t(u) + delta_M    (mod M).
```

### Proof

Start from the active base point `A_0 = 3u+1`.

By definition of `N_t`, the first special source state reached from `(A_0,0)` has compact coordinate

```text
A_* = 3N_t(u)+1.
```

Now apply the good-branch special-source theorem:
the special branch returns to base at

```text
A_* + Delta_m.
```

This is the **first** base image `P_t(A_0)`.
Since `Delta_m ≡ 2 (mod 3)`, that image lies in the nonactive residue class `0 (mod 3)`.
On nonactive residues, the ordinary source branch fixes the compact coordinate until the next special hit,
so the second and third base returns are just additional `+Delta_m` translates.
Hence

```text
P_t^3(A_0) = A_* + 3 Delta_m = 3N_t(u)+1+3Delta_m.
```

Reducing by `u <-> 3u+1` gives

```text
g_t(u) = N_t(u) + delta_M.
```

∎

### Meaning

The reduced base machine is now split into two conceptually different parts:

1. `N_t`: an active-source odometer problem;
2. `+delta_M`: a constant final splice translation.

In the scaled coordinate

```text
K = 5u   (mod M),
```

the constant splice is simply

```text
K -> K + 7,
```

because `5 delta_M ≡ 7 (mod M)`.

This matches the already-known `+7` character of the generic-late special branch.

---

## 3. The active source skew product has only one defect

The ordinary active source dynamics is especially simple.

## Proposition 3.1 (active source skew product)

On the active class `A=3u+1`, the ordinary compact source return is

```text
u -> p_gen(u),
e -> e - 5 + 2 * 1[u=1]      (mod m),
```

and the special graph is

```text
e = 5 - 2 * 1[u=1].
```

So the only defect in the active skew product is the unique anomaly point

```text
u = 1    <->    A = 4.
```

### Proof

From the generic-late compact source formulas already established in the March 27 archive,

```text
rho(A) = m-5 + 2 * 1[A=4],
special_row(A) = 5 - 2 * 1[A=4]
```

on active coordinates, and the active `A`-map is exactly `p_gen`.
Since `A=3u+1`, the point `A=4` corresponds to `u=1`. ∎

This is the clean odometer picture:
there is a uniform `-5` cocycle and a single `+2` defect at one point.

---

## 4. Nondefect active cycles are solved exactly

Let `C` be a cycle of `p_gen` of length `L`.

## Proposition 4.1 (nondefect cycle formula)

Assume `1 notin C`, i.e. the cycle does **not** contain the anomaly point.
Then on `C` one has

```text
N_t|_C = p_gen^{r_C},
r_C ≡ m-1   (mod L),    0 <= r_C < L.
```

In words: on every nondefect active cycle, the first-special-hit map is just a constant power of the active permutation.

### Proof

If `1 notin C`, then Proposition 3.1 has no defect on that cycle.
So along the ordinary source orbit one simply has

```text
e_n = -5n    (mod m),
```

while the special graph is the constant row `e=5`.

Therefore the first special time is the least positive `n` such that

```text
-5n ≡ 5   (mod m),
```

equivalently

```text
n ≡ m-1   (mod m).
```

The position on the `p_gen`-cycle depends only on `n mod L`.
So the first special-hit offset is exactly

```text
r_C = (m-1) mod L,
```

and the special point is `p_gen^{r_C}(u)`. ∎

This completely closes all active cycles except the unique defect cycle.

---

## 5. Exact defect-cycle odometer equation

Now let `C_*` be the unique `p_gen`-cycle containing `u=1`.
Write its length as `L_*`, and index it in `p_gen`-order by

```text
C_* = (u_0, u_1, ..., u_{L_*-1}),
u_0 = 1,
u_{j+1} = p_gen(u_j).
```

For a starting point `u_r`, write the special-hit offset as

```text
N_t(u_r) = u_{r + b_r},
```

with indices modulo `L_*` and `0 <= b_r < L_*`.

Define

```text
eta_* := 2 - 5L_*    (mod m),
d_r   := (L_* - r) mod L_*.
```

Here `d_r` is the forward distance from the start `u_r` to the defect `u_0`.

## Proposition 5.1 (defect-cycle odometer equation)

For each pair `(r,b)` with `0 <= r,b < L_*` **for which the congruence below is solvable**, let `q_{r,b}` be the least nonnegative integer such that

```text
q_{r,b} * eta_* ≡ 5(b+1) - 2 * 1[b >= d_r]    (mod m)
```

and such that

```text
L_* q_{r,b} + b > 0.
```

Then the first special-hit time from `u_r` with base row `e=0` is

```text
n_r = min_{0 <= b < L_*} ( L_* q_{r,b} + b ),
```

and the corresponding minimizer `b_r` satisfies

```text
N_t(u_r) = u_{r+b_r}.
```

### Proof

Start at `u_r` with `e_0=0`.
After `n=qL_*+b` ordinary active steps, the cycle position is `u_{r+b}`.

The number of departures from the defect `u_0` during those `n` steps is

```text
q + 1[b >= d_r] - 1[b = d_r].
```

Equivalently, it is `q` if the partial tail has not yet reached the defect, and `q+1`
once the tail reaches or passes it.  Using Proposition 3.1, the row coordinate after
`n=qL_*+b` steps is therefore

```text
e_n
=
-5(qL_*+b) + 2(q + 1[b > d_r])
=
q(2-5L_*) - 5b + 2 * 1[b > d_r].
```

The target special row at the final point `u_{r+b}` is

```text
5 - 2 * 1[b = d_r].
```

So the special-hit condition `e_n = 5 - 2*1[b=d_r]` is exactly

```text
q eta_*
≡
5(b+1) - 2 * 1[b >= d_r]
(mod m).
```

For each `b`, the least nonnegative solution gives the least candidate time `L_* q_{r,b} + b`
with that offset.
The actual first special hit is the minimum over all candidate offsets `b`.
By construction, the minimizing offset is precisely `b_r`, so

```text
N_t(u_r) = u_{r+b_r}.
```

∎

### Interpretation

This is the promised d3/d4-style second-return theorem.

- The defect cycle is not an arbitrary permutation problem.
- It is a one-dimensional odometer equation with clock increment encoded by `eta_*`.
- The only defect is the `-2` correction once the forward tail reaches the anomaly point.

So the generic-late good-branch reduced machine has now been lowered to:
one explicit defect-cycle congruence minimization problem, plus already-solved constant powers on every other active cycle.

---

## 6. Structural consequence for the reduced base map

Combine Theorem 2.1, Proposition 4.1, and Proposition 5.1.

## Corollary 6.1 (componentwise reduced base machine)

The generic-late good-branch reduced base map `g_t` is obtained as follows.

1. Decompose the active permutation `p_gen` into its cycles.
2. On each nondefect cycle `C`, apply the explicit power
   ```text
   p_gen^{(m-1 mod |C|)}.
   ```
3. On the unique defect cycle `C_*`, apply the explicit minimization map from Proposition 5.1.
4. Finally add the constant splice translation
   ```text
   +delta_M = 7 * 5^{-1}  (mod M).
   ```

This is an exact arithmetic machine for `g_t`.

What remains open is the final cycle theorem for that machine.

---

## 7. Verification scope

Companion files:

- `d5_generic_late_base_splice_odometer_reduction_check_2026-03-27.py`
- `d5_generic_late_base_splice_odometer_reduction_check_report_2026-03-27.txt`

What was checked symbolically:

- all good generic-late moduli
  ```text
  27 <= m <= 301,   3|m,   5∤m,   7∤m;
  ```
- exact factorization
  ```text
  g_t = N_t + delta_M;
  ```
- the nondefect-cycle power law of Proposition 4.1;
- the defect-cycle odometer equation of Proposition 5.1.

All of those checks matched on the full stated range.

### Selected examples

- `m=39`, defect cycle length `13`:
  the defect-cycle offsets are
  ```text
  [0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3].
  ```

- `m=81`, defect cycle length `27`:
  the defect-cycle offsets are
  ```text
  [11, 21, 21, 21, 21, 21, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11].
  ```

These are exactly the kinds of piecewise-constant defect patterns one expects from an odometer / finite-defect odometer viewpoint.

---

## 8. What this does and does not close

### What is now proved

- the reduced base map `g_t` factors through the active first-special-hit map `N_t`;
- the active skew product has only one defect;
- every nondefect active cycle is completely explicit;
- the defect cycle is reduced to an explicit one-dimensional congruence optimization problem.

### What is still open

- a closed cycle theorem for the defect-cycle map in Proposition 5.1;
- the final cycle theorem for the whole reduced base map `g_t`.

So this note does **not** yet finish the generic-late base splice theorem.
But it does replace the raw reduced permutation by an explicit odometer-style defect machine,
which is the correct next target.
