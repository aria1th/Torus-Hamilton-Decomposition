# d=5 generic-late base splice: a symbolic 7-split theorem
Date: 2026-03-27

## Goal

Replace the earlier overbroad empirical candidate

```text
generic late base return P_t(a) ≡ a+2 (mod 3)   for all safe m
```

by a **symbolic theorem** with the correct arithmetic split.

The new conclusion is:

- if `7 ∤ M` (equivalently `7 ∤ m`), then the generic-late base return really does satisfy
  ```text
  P_t(a) ≡ a+2 (mod 3),
  ```
  so the base splice reduces from `m` points to `M=m/3` points by the abstract mod-3 reduction note;

- if `7 | M`, then the generic-late base return has many fixed points, so single-cycle base splicing is impossible.

So the base-splice frontier is not a universal mod-3 reduction.
It is a **7-split**.

---

## 1. Inputs used

Everything below is downstream of already-promoted local/source ingredients:

1. the generic-late compact source law on `H_m`,
2. the generic-late actual-entry theorem,
3. the generic-late double-top top-row law,
4. the full gate law at `c=m-2,d=m-1,e=m-1`,
5. the universal compact bridge `U -> H`.

For the full all-base-state drift theorem in Section 4, I also use the already-closed generic-late visibility statement (`H_m -> B_m` acyclicity), only to know that every source orbit from base eventually reaches a special source state.

---

## 2. The special source branch on double-top

Fix

```text
m = 3M >= 27,   5 ∤ m,
```

and let `t` be generic late.

Write compact source coordinates as usual:

```text
(A,e),   A = a - 1[e=m-1].
```

Let `s(A)` be the special row.
Start from the **special source state**

```text
(A, s(A)).
```

By the actual-entry theorem, the first top hit always lies on double-top (`e=m-1`), and the entry state is

```text
A != 4 :   (a,c,e) = (A, 3, m-1),
A = 4   :  (a,c,e) = (5, 2, m-1).
```

In both cases the top invariant

```text
w := a + c   (mod m)
```

starts at

```text
w_0 = A + 3   (mod m).
```

On generic-late double-top, the proved top-row law is

```text
if w = 0:
    (a,c) -> (a+3, c+4),
else:
    (a,c) -> (a+2, c+5).
```

Hence

```text
w -> w + 7   (mod m)
```

at every block.

So the special source branch is governed by a one-dimensional `w`-rotation of step `7`, and this is exactly where the divisibility by `7` enters.

---

## 3. The induced special-to-base map

Define

```text
S_m(A)
```

to be the compact `A`-coordinate of the eventual base state obtained by starting from the special source state `(A,s(A))` and following the compact `H`-return until base is reached.

The next theorem computes `S_m` symbolically.

## Theorem 3.1 (generic-late special branch: 7-split)

Assume `t` is generic late.

### (A) The case `7 ∤ m`

Let `r_m` be the least residue in `{0,...,m-1}` solving

```text
5 r_m ≡ -4   (mod m),
```

and set

```text
Delta_m := 7 (r_m + 1)   (mod m).
```

Then for every `A in Z/mZ`,

```text
S_m(A) = A + Delta_m   (mod m).
```

Moreover,

```text
Delta_m ≡ 2   (mod 3).
```

### (B) The case `7 | m`

If `A ≠ 4 (mod 7)`, then

```text
S_m(A) = A.
```

In particular, on six of the seven `A`-cosets modulo `7`, the special branch returns to the same compact base coordinate.

---

### Proof of Theorem 3.1(A)

Assume `7 ∤ m`.

#### Step 1. The ordinary generic case `A != 4`

The double-top entry state is `(A,3,m-1)`, so before the gate the column satisfies

```text
c_n = 3 + 5n - 1[n > j(A)],
```

where `j(A)` is the unique time with

```text
A + 3 + 7 j(A) ≡ 0   (mod m).
```

Because `7` is invertible modulo `m`, this `j(A)` is unique modulo `m`.

To hit the gate `c = m-2`, we need

```text
3 + 5n - 1[n > j(A)] ≡ m-2   (mod m).
```

If `n > j(A)`, this becomes

```text
5n ≡ -4   (mod m),
```

so the relevant solution is `n ≡ r_m (mod m)`.

The least admissible gate time is therefore

```text
n_A = r_m          if j(A) < r_m,
n_A = r_m + m      if j(A) >= r_m.
```

Either way,

```text
w_gate
=
A + 3 + 7 n_A
≡
A + 3 + 7 r_m
(mod m).
```

#### Step 2. The anomaly `A = 4`

Now the double-top entry state is `(5,2,m-1)`.
So

```text
w_0 = 7,
c_n = 2 + 5n
```

until the gate.
The first gate time is again determined by

```text
2 + 5n ≡ m-2   (mod m),
```

which is the same congruence

```text
5n ≡ -4   (mod m).
```

So the anomaly also gates at `n = r_m`, and

```text
w_gate = 7 + 7 r_m = A + 3 + 7 r_m.
```

Thus the same gate value formula holds for **every** `A`:

```text
w_gate ≡ A + 3 + 7 r_m   (mod m).
```

#### Step 3. Pass through the gate and the `U -> H` bridge

On generic-late double-top, the full gate law at `c=m-2` sends the state to raw `U` with

```text
(a_U, e_U)
=
(w_gate + 3, 0),
```

except in the three interface cases where the raw `H`-output is one of

```text
(m-1,1),   (2,1),   (3,m-1).
```

In compact coordinates, all three interface outputs have compact `A` equal to

```text
w_gate + 4.
```

The ordinary `U -> H` bridge also sends the non-interface gate output to compact coordinate

```text
w_gate + 4.
```

Therefore the first compact `H`-return after the special branch always has compact coordinate

```text
w_gate + 4
=
A + 7(r_m + 1)
=
A + Delta_m.
```

If the returned state is already in base, we are done.
If it is one of the three interface states, its compact coordinate is still `A + Delta_m`, and that coordinate is nonactive.
So the subsequent ordinary source evolution keeps `A` fixed until the next special hit, and the eventual base coordinate is still `A + Delta_m`.

Hence

```text
S_m(A) = A + Delta_m
```

for every `A`.

#### Step 4. `Delta_m mod 3`

Reduce the defining congruence modulo `3`.
Since `m ≡ 0 (mod 3)`, we get

```text
5 r_m ≡ -4   (mod m)
==>
2 r_m ≡ 2   (mod 3)
==>
r_m ≡ 1   (mod 3).
```

Therefore

```text
Delta_m
=
7(r_m+1)
≡
r_m + 1
≡
2
(mod 3).
```

This proves Part (A). ∎

---

### Proof of Theorem 3.1(B)

Assume `7 | m`, and let `A ≠ 4 (mod 7)`.

Then

```text
w_0 = A + 3
```

is **not** divisible by `7`.
Since `w` evolves by

```text
w -> w + 7   (mod m),
```

the orbit of `w` never hits `0`.
So there is no anomaly block on double-top.

Hence, before the gate,

```text
c_n = 3 + 5n,
```

and the first gate time is the least solution of

```text
3 + 5n ≡ m-2   (mod m),
```

namely

```text
n = m - 1.
```

At that time,

```text
w_gate
=
A + 3 + 7(m-1)
≡
A - 4
(mod m).
```

After the gate and the `U -> H` bridge, the compact `A`-coordinate becomes

```text
w_gate + 4 ≡ A.
```

Again, the only possible non-base outputs are the three interface states, but in compact coordinates they still have the same `A`.
Since this `A` is nonactive, the source ordinary branch fixes it until base.

So the eventual base coordinate is exactly `A`.
That is,

```text
S_m(A) = A
```

for every `A ≠ 4 (mod 7)`. ∎

---

## 4. Explicit consequences for the base permutation on nonactive residues

Let

```text
P_t : B_m -> B_m
```

be the generic-late base next-return permutation.

On base we have compact coordinate `A = a`.

The compact source law has the same ordinary formula at `e=0`, because

```text
s(A) in {3,4,5,6},
```

so `e=0` is still ordinary.
Therefore the first compact `H`-return from base is

```text
(A,0) -> (A, rho(A))          if A ≠ 1 (mod 3),
(A,0) -> (p_gen(A), rho(A))   if A ≡ 1 (mod 3),
```

with

```text
rho(A) = m-5 + 1[A=0] + 2[A=4].
```

Hence, on the nonactive classes `A ≠ 1 (mod 3)`, the compact coordinate `A` stays fixed until the orbit reaches the special row.

This gives an immediate explicit base map on the nonactive residues.

## Corollary 4.1 (nonactive part of the generic-late base map)

Assume `t` is generic late.

### (A) If `7 ∤ m`, then for every nonactive residue `A ≠ 1 (mod 3)`,

```text
P_t(A) = A + Delta_m.
```

### (B) If `7 | m` and `A ≠ 1 (mod 3)` and `A ≠ 4 (mod 7)`, then

```text
P_t(A) = A.
```

So in the bad `7|m` regime, the nonactive part already contributes many fixed points.

∎

---

## 5. The corrected mod-3 drift theorem

The earlier March 27 base-splice reduction note observed from samples that generic late seemed to satisfy

```text
P_t(a) ≡ a+2   (mod 3).
```

That statement is **not** universally true.
The correct symbolic theorem is the following.

## Theorem 5.1 (generic-late base drift when `7 ∤ m`)

Assume

```text
m = 3M >= 27,   5 ∤ m,   7 ∤ m,
```

and let `t` be generic late.
Then the base next-return permutation satisfies

```text
P_t(a) ≡ a + 2   (mod 3)
```

for every `a in Z/mZ`.

### Proof

Start from base compact coordinate `A_0 = a`.

Under the ordinary compact `H`-return:

- if `A ≠ 1 (mod 3)`, then `A` stays fixed;
- if `A ≡ 1 (mod 3)`, then `A` moves by the active permutation `p_gen`, which stays entirely inside the active residue class.

So every ordinary source step preserves the residue class of `A` modulo `3`.

By the already-closed generic-late source/visibility theorem, the orbit starting from base eventually reaches a special source state with some compact coordinate `A_*`.
Because ordinary steps preserve `A mod 3`, we have

```text
A_* ≡ A_0   (mod 3).
```

Now apply Theorem 3.1(A).
The special branch and all subsequent interface continuation return to base at compact coordinate

```text
A_* + Delta_m.
```

But `Delta_m ≡ 2 (mod 3)`.
Therefore

```text
P_t(a)
=
A_* + Delta_m
≡
A_0 + 2
=
a + 2
(mod 3).
```

This proves the drift law. ∎

---

## 6. Reduced arithmetic machine in the good case

Combine Theorem 5.1 with the abstract mod-3 base-splice reduction from

```text
d5_base_splice_mod3_reduction_note_2026-03-27.md.
```

## Corollary 6.1 (generic-late reduced base machine for `7 ∤ m`)

Assume

```text
m = 3M >= 27,   5 ∤ m,   7 ∤ m,
```

and let `t` be generic late.

Then the base-splice permutation `P_t` reduces to the `M`-point map

```text
g_t(u) := (P_t^3(3u+1)-1)/3,
```

and the cycle lengths of `P_t` are exactly three times the cycle lengths of `g_t`.

So in the good `7 ∤ m` regime, the generic-late splice problem really is an `M`-point reduced arithmetic machine.

---

## 7. Obstruction in the bad case `7 | m`

The bad `7|m` branch is not merely “different”.
It already blocks single-cycle splicing.

## Corollary 7.1 (fixed-point obstruction when `7 | m`)

Assume

```text
m = 3M >= 27,   5 ∤ m,   7 | m,
```

and let `t` be generic late.

Then every residue class satisfying

```text
A ≠ 1 (mod 3),
A ≠ 4 (mod 7)
```

is a fixed point of `P_t`.

Hence `P_t` has at least

```text
(2/3) * (6/7) * m = 4m/7
```

fixed points.
In particular, `P_t` is **not** a single cycle.

### Proof

This is exactly Corollary 4.1(B).
The residue conditions define `12` classes modulo `21`, and since `21 | m`, their total cardinality is `12m/21 = 4m/7`. ∎

---

## 8. Meaning for the proof program

This note changes the splice frontier in two important ways.

### What is now genuinely proved

- The earlier universal generic-late mod-3 drift candidate was too broad.
- The correct symbolic split is by `7`.
- In the regime
  ```text
  7 ∤ m,
  ```
  the generic-late base return really does admit the mod-3 reduction to an `M`-point machine.
- In the regime
  ```text
  7 | m,
  ```
  generic-late base single-cycle splicing is impossible, already because of explicit fixed points.

### What remains open

In the good branch `7 ∤ m`, the remaining arithmetic target is no longer the raw `m`-point splice map.
It is the reduced `M`-point permutation

```text
g_t : Z_M -> Z_M.
```

That reduced cycle theorem is still open here.

---

## 9. Verification scope

Companion files:

- `d5_generic_late_base_splice_7split_check_2026-03-27.py`
- `d5_generic_late_base_splice_7split_check_report_2026-03-27.txt`
- `d5_generic_late_base_splice_7split_check_report_2026-03-27.json`

### Symbolic scan

All safe moduli

```text
27 <= m <= 301,   3|m,   5∤m,
```

for generic-late row `t=4`.

What was checked:

- on every good modulus `7∤m`, the special-source induced base formula
  ```text
  S_m(A) = A + Delta_m
  ```
  for all `A`;
- on the same good moduli, the full base map `P_t` satisfies
  ```text
  P_t(a) ≡ a+2 (mod 3);
  ```
- on every bad modulus `7|m`, all residues
  ```text
  A ≠ 1 (mod 3),   A ≠ 4 (mod 7)
  ```
  are fixed by `P_t`.

### Raw exact comparisons

Full exact `B_m`-map comparisons against the archived next-return code at

```text
m = 33, 39, 51, 63,
```

and selected exact state checks at

```text
m = 147,   a in {0,1,4,7}.
```

All of those comparisons matched the symbolic formulas.

