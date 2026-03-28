# d=5 generic-late good branch: the explicit three-block defect-cycle theorem in the `15r+3` / `15r+9` branches
Date: 2026-03-27

## Goal

This note upgrades the March 27 three-block **candidate** for the Proposition 5.1
defect-cycle minimization to a theorem-order statement in the two residue classes

```text
m ≡ 3,9 (mod 15).
```

The new `+5` carrier note was the structural hint: in these two classes the common
carrier sees zero or at most two internal splice points, so a three-block defect
pattern was the right thing to expect.

The actual proof below is **directly from Proposition 5.1**.  We do not need the
missing symbolic bridge to the carrier return.  Instead, we solve the Proposition 5.1
congruence by a finite `q`-table in each residue class and compare candidate times.

So this note does two things:

1. it proves the explicit three-block formulas conjectured in
   `d5_generic_late_defect_three_block_formula_candidate_2026-03-27.md`;
2. it shows that the generic-late defect cycle in the `15r+3` / `15r+9` classes is
   already an explicit three-block cyclic interval-translation machine.

What this note does **not** yet close is the final cycle theorem for the whole reduced
base map `g_t`.

---

## 1. Imported inputs

Assume throughout

```text
m = 3M >= 27,
5∤m,
7∤m,
t is generic late,
m ≡ 3 or 9 (mod 15).
```

Let `C_*` be the active defect cycle of `p_gen`, indexed in `p_gen`-order by

```text
C_* = (u_0,...,u_{L-1}),
u_0 = 1,
u_{j+1} = p_gen(u_j),
```

and write

```text
N_t(u_j) = u_{j+b_j},
```

with indices modulo `L` and `0 <= b_j < L`.

The March 27 odometer-reduction note proved:

```text
eta := 2 - 5L   (mod m),
d_j := (L-j) mod L,
```

and for each starting index `j`, the first-special-hit offset `b_j` is determined by
the minimum of

```text
n = Lq + b
```

over solutions of

```text
q eta ≡ 5(b+1) - 2 * 1[b >= d_j]    (mod m).
```

We also use the already-proved active cycle lengths:

- if `M ≠ 2 (mod 3)`, the active permutation is unsplit and the defect cycle length is
  `L=M`;
- if `M ≡ 2 (mod 3)`, the active permutation splits into three cycles and the defect
  cycle length is `L=(M+1)/3`.

---

## 2. A useful interval lemma

For `j=0` one has `d_0=0`.
For `1 <= j <= L-1` one has

```text
d_j = L-j.
```

So for a candidate pair `(b,I)` with `I in {0,1}` the condition

```text
I = 1[b >= d_j]
```

is equivalent to:

- if `I=0`, then
  ```text
  1 <= j <= L-b-1;
  ```
- if `I=1`, then
  ```text
  j=0   or   L-b <= j <= L-1.
  ```

Thus every explicit solution `(q,b,I)` of the Proposition 5.1 congruence produces one
explicit interval (or cyclic tail-plus-origin block) on the index circle.

We use this repeatedly below.

---

## 3. The main theorem

## Theorem 3.1 (explicit three-block defect formula)

Let `m`, `t`, `C_*`, `L`, and `b_j` be as above.

### (i) The branch `m = 15r+3`

#### (i.a) The unsplit active case `r \not\equiv 2 (mod 3)`

Here

```text
M = 5r+1,
L = 5r+1,
eta = 5r+3.
```

Then the offset function `j -> b_j` is

```text
b_j = 3r       for j=0 or 2r+1 <= j <= 5r,
b_j = 3r+2     for 1 <= j <= 2r-2,
b_j = r+2      for 2r-1 <= j <= 2r.
```

Equivalently, its cyclic run decomposition is

```text
(3r,   3r+1),
(3r+2, 2r-2),
(r+2,  2).
```

#### (i.b) The split active case `r \equiv 2 (mod 3)`

Here

```text
M = 5r+1,
L = (M+1)/3 = (5r+2)/3,
eta = (20r+5)/3.
```

Then

```text
b_0 = 0,
b_j = (4r-2)/3    for 1 <= j <= (r+1)/3,
b_j = (4r+1)/3    for (r+4)/3 <= j <= L-1.
```

Equivalently, the cyclic run decomposition is

```text
(0,              1),
((4r-2)/3, (r+1)/3),
((4r+1)/3, (4r-2)/3).
```

### (ii) The branch `m = 15r+9`

#### (ii.a) The unsplit active case `r \not\equiv 1 (mod 3)`

Here

```text
M = 5r+3,
L = 5r+3,
eta = 5r+5.
```

If `r=2` (that is `m=39`), then

```text
b_0 = 0,
b_j = 2    for 1 <= j <= 10,
b_j = 3    for 11 <= j <= 12.
```

Equivalently, the cyclic run decomposition is

```text
(0,1), (2,10), (3,2).
```

If `r >= 6`, then

```text
b_j = 3      for j=0 or 5r <= j <= 5r+2,
b_j = r      for 1 <= j <= 4r+2,
b_j = r+4    for 4r+3 <= j <= 5r-1.
```

Equivalently, the cyclic run decomposition is

```text
(3,   4),
(r,   4r+2),
(r+4, r-3).
```

#### (ii.b) The split active case `r \equiv 1 (mod 3)`

Here

```text
M = 5r+3,
L = (M+1)/3 = (5r+4)/3,
eta = (20r+13)/3.
```

Then

```text
b_0 = 0,
b_j = (r-1)/3    for 1 <= j <= (4r+2)/3,
b_j = (r+2)/3    for (4r+5)/3 <= j <= L-1.
```

Equivalently, the cyclic run decomposition is

```text
(0,            1),
((r-1)/3, (4r+2)/3),
((r+2)/3, (r-1)/3).
```

---

## 4. Proof

We solve the Proposition 5.1 congruence by a finite `q`-table in each subcase.

Because `0 <= b < L`, once an explicit candidate with time `n_*` is known, any
candidate with `q >= Q` satisfying `QL > n_*` is irrelevant for the minimum.
That is why the `q`-search below is genuinely finite.

### 4.1. Class `m = 15r+3`, unsplit active case

Here `L=5r+1` and `eta=5r+3`.
The candidate `(q,b)=(7,r+2)` gives time

```text
n = 7L + (r+2) = 36r+9.
```

So any candidate with `q >= 8` has

```text
Lq+b >= 8L > 36r+9
```

and cannot be minimal.

Now solve the congruence for `0 <= q <= 7`.
A direct check yields exactly the following solutions:

| `q` | indicator `I` | `b` | candidate time `Lq+b` | valid indices from §2 |
|---:|:---:|---:|---:|---|
| `0` | `1` | `3r` | `3r` | `j=0` or `2r+1 <= j <= 5r` |
| `1` | `1` | `r` | `6r+1` | `j=0` or `4r+1 <= j <= 5r` |
| `6` | `0` | `3r+2` | `33r+8` | `1 <= j <= 2r-2` |
| `7` | `0` | `r+2` | `36r+9` | `1 <= j <= 4r-2` |
| `7` | `1` | `4r+3` | `39r+10` | `j=0` or `r-2 <= j <= 5r` |

No other solution occurs for `0 <= q <= 7`.

Now compare candidate times on overlaps.

- On `j=0` or `2r+1 <= j <= 5r`, the `q=0` candidate is valid and strictly smaller
  than every other candidate.
- On `1 <= j <= 2r-2`, the `q=6` candidate is valid and beats the two `q=7`
  candidates.
- On `2r-1 <= j <= 2r`, the `q=6` candidate is no longer valid, while the `q=7`,
  `I=0` candidate remains valid; it therefore wins there.
- The `q=1` and `(q,I)=(7,1)` candidates are never minimal: each is valid only where
  a smaller candidate above is also valid.

This gives the displayed formula and cyclic run decomposition.

---

### 4.2. Class `m = 15r+3`, split active case

Here

```text
L = (5r+2)/3,
eta = (20r+5)/3.
```

The explicit candidate `(q,b)=(10,(4r+1)/3)` gives time

```text
10L + (4r+1)/3 = 18r+7,
```

so any `q >= 11` is irrelevant.

For `0 <= q <= 10`, the congruence has exactly these solutions:

| `q` | `I` | `b` | candidate time | valid indices |
|---:|:---:|---:|---:|---|
| `1` | `0` | `(4r-2)/3` | `3r` | `1 <= j <= (r+1)/3` |
| `9` | `1` | `0` | `15r+6` | `j=0` |
| `10` | `1` | `(4r+1)/3` | `18r+7` | `j=0` or `(r+1)/3 <= j <= L-1` |

Now compare.

- At `j=0`, the `q=9` candidate wins.
- On `1 <= j <= (r+1)/3`, the `q=1` candidate wins.
- At the boundary `j=(r+1)/3`, both `q=1` and `q=10` are valid, but `3r < 18r+7`,
  so `q=1` wins.
- Therefore the `q=10` candidate takes over exactly on
  ```text
  (r+4)/3 <= j <= L-1.
  ```

This is exactly the stated three-block formula.

---

### 4.3. Class `m = 15r+9`, unsplit active case

Here `L=5r+3` and `eta=5r+5`.

#### The edge case `r=2`

This is `m=39`.  A direct `q`-table from Proposition 5.1 gives the only relevant
candidates:

| `q` | `I` | `b` | candidate time | valid indices |
|---:|:---:|---:|---:|---|
| `1` | `0` | `2` | `15` | `1 <= j <= 10` |
| `8` | `1` | `0` | `104` | `j=0` |
| `9` | `1` | `3` | `120` | `j=0` or `10 <= j <= 12` |
| `10` | `1` | `6` | `136` | `j=0` or `7 <= j <= 12` |

So `j=0` takes the `q=8` candidate, `1 <= j <= 10` takes the `q=1` candidate, and
`11 <= j <= 12` takes the `q=9` candidate.
That is exactly the displayed edge-case formula.

#### The generic subcase `r >= 6`

The explicit candidate `(q,b)=(10,r+4)` has time

```text
10L + (r+4) = 51r+34,
```

so any `q >= 11` is irrelevant.

For `0 <= q <= 10`, the congruence has exactly these solutions:

| `q` | `I` | `b` | candidate time | valid indices |
|---:|:---:|---:|---:|---|
| `1` | `0` | `r` | `6r+3` | `1 <= j <= 4r+2` |
| `2` | `0` | `2r+1` | `12r+7` | `1 <= j <= 3r+1` |
| `3` | `0` | `3r+2` | `18r+11` | `1 <= j <= 2r` |
| `4` | `0` | `4r+3` | `24r+15` | `1 <= j <= r-1` |
| `9` | `1` | `3` | `45r+30` | `j=0` or `5r <= j <= 5r+2` |
| `10` | `1` | `r+4` | `51r+34` | `j=0` or `4r-1 <= j <= 5r+2` |

Now compare.

- The `q=1` candidate is strictly smaller than the `q=2,3,4` candidates and is valid
  on a superset of all their index ranges.  So the latter are never minimal.
- The `q=9` candidate is strictly smaller than the `q=10` candidate wherever both are
  valid.
- Therefore:
  - `q=9` wins on `j=0` and on the tail `5r <= j <= 5r+2`;
  - `q=1` wins on `1 <= j <= 4r+2`;
  - the only indices where `q=10` survives are
    ```text
    4r+3 <= j <= 5r-1.
    ```

This is the stated three-block formula.

---

### 4.4. Class `m = 15r+9`, split active case

Here

```text
L = (5r+4)/3,
eta = (20r+13)/3.
```

The explicit candidate `(q,b)=(16,(r+2)/3)` has time

```text
16L + (r+2)/3 = 27r+22,
```

so any `q >= 17` is irrelevant.

For `0 <= q <= 16`, the congruence has exactly these solutions:

| `q` | `I` | `b` | candidate time | valid indices |
|---:|:---:|---:|---:|---|
| `7` | `0` | `(r-1)/3` | `12r+9` | `1 <= j <= (4r+2)/3` |
| `9` | `1` | `0` | `15r+12` | `j=0` |
| `14` | `0` | `(2r+1)/3` | `24r+19` | `1 <= j <= r` |
| `16` | `1` | `(r+2)/3` | `27r+22` | `j=0` or `(4r+2)/3 <= j <= L-1` |

Now compare.

- The `q=7` candidate is strictly smaller than the `q=14` candidate and is valid on a
  superset of the `q=14` range, so `q=14` is never minimal.
- At `j=0`, the `q=9` candidate wins.
- At the boundary `j=(4r+2)/3`, both `q=7` and `q=16` are valid, but `12r+9 < 27r+22`,
  so `q=7` wins there.

Hence:

- `j=0` gives `b_0=0`,
- `1 <= j <= (4r+2)/3` gives `b_j=(r-1)/3`,
- `(4r+5)/3 <= j <= L-1` gives `b_j=(r+2)/3`.

This is exactly the displayed three-block formula. ∎

---

## 5. Structural corollary

## Corollary 5.1 (the defect cycle is already a three-block interval-translation machine)

In each of the four subcases of Theorem 3.1, the defect-cycle map

```text
N_t : C_* -> C_*
```

is a cyclic interval-exchange with exactly three translation blocks (counted cyclically;
in the edge case `m=39` the three blocks have lengths `1,10,2`).

So the new carrier note was pointing in the right direction:
the open defect theorem in the `15r+3` / `15r+9` classes is indeed a
**three-block one-dimensional odometer machine**.

What is still open is not the local block structure, but the final cycle theorem for
the full reduced base map `g_t`.

---

## 6. What this supersedes

This note upgrades and supersedes

- `d5_generic_late_defect_three_block_formula_candidate_2026-03-27.md`

for the classes covered here.

It also sharpens the status of

- `d5_generic_late_defect_carrier_alignment_note_2026-03-27.md`

by showing that the three-block shape can already be proved directly from Proposition 5.1,
even before the defect-section / carrier-return bridge is written symbolically.

---

## 7. Verification scope

Companion files:

- `d5_generic_late_defect_three_block_theorem_check_2026-03-27.py`
- `d5_generic_late_defect_three_block_theorem_check_report_2026-03-27.txt`

The exact check compares the theorem formulas above against the exact March 27
symbolic/archived defect map on the range

```text
27 <= m <= 1501,
3|m,
5∤m,
7∤m,
m ≡ 3 or 9 (mod 15).
```

The theorem matched every tested modulus in that range.
