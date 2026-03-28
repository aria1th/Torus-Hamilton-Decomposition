# d=5 generic-late good branch: an explicit reduced base-machine theorem in the `15r+3` / `15r+9` classes
Date: 2026-03-27

## Goal

Combine the March 27 notes into one theorem-order statement that cleanly isolates what is
**already closed** for the generic-late reduced base machine in the two arithmetic classes

```text
m ≡ 3, 9 (mod 15).
```

The point is not to overstate a final cycle theorem for `g_t`.  That is still open.
The point is that, in these classes, the whole reduced base machine is now **explicit**:
there is no remaining local or hidden arithmetic.
What remains is only the global cycle analysis of an explicit finite permutation.

---

## 1. Setting and imported inputs

Assume throughout

```text
m = 3M >= 33,
5 ∤ m,
7 ∤ M,
t is generic late,
m ≡ 3 or 9 (mod 15).
```

Write the generic-late reduced base map as

```text
g_t(u) := (P_t^3(3u+1)-1)/3,
```

where `P_t : B_m -> B_m` is the base next-return permutation.

We use three already-proved ingredients.

1. **Good-branch factorization**
   ```text
   g_t(u) = N_t(u) + delta_M,
   delta_M = 7 * 5^{-1} (mod M),
   ```
   where `N_t` is the active first-special-hit map.

2. **Nondefect active cycles**
   On every active cycle `C` of `p_gen` not containing the anomaly `u=1`,
   ```text
   N_t|_C = p_gen^{r_C},
   r_C ≡ m-1 (mod |C|),
   0 <= r_C < |C|.
   ```

3. **Defect cycle theorem in the `15r+3` / `15r+9` classes**
   If `C_*=(u_0,...,u_{L-1})` is the unique `p_gen`-cycle containing `u_0=1`, indexed in
   `p_gen`-order, then
   ```text
   N_t(u_j)=u_{j+b_j}
   ```
   and the offset function `j -> b_j` is given by an explicit three-block formula.

So the only task here is to package those three inputs into one exact theorem.

---

## 2. A simple closed form for the splice translation

Because `M = m/3` and `m ≡ 3 or 9 (mod 15)`, we can write:

- `m = 15r+3`, so `M = 5r+1`;
- `m = 15r+9`, so `M = 5r+3`.

### Lemma 2.1 (explicit splice constants)
In the good branch `7 ∤ M` one has

```text
delta_M = 3r+2   if m = 15r+3,
delta_M = r+2    if m = 15r+9.
```

#### Proof
If `M=5r+1`, then `5^{-1} ≡ -r (mod M)`, hence
```text
delta_M = 7*(-r) ≡ 3r+2 (mod 5r+1).
```
If `M=5r+3`, then `5^{-1} ≡ 3r+2 (mod M)`, hence
```text
delta_M = 7*(3r+2) = 21r+14 ≡ r+2 (mod 5r+3).
```
∎

---

## 3. The explicit theorem

Let `p_gen` be the generic-late active permutation on `Z_M`, and let

```text
Z_M = C_* ⊔ C_1 ⊔ ... ⊔ C_s
```

be its cycle decomposition, where `C_*` is the unique cycle containing `u=1`.
For `i>=1`, write `L_i = |C_i|` and

```text
rho_i := (m-1) mod L_i.
```

### Theorem 3.1 (explicit reduced base machine in the `15r+3` / `15r+9` good branch)
Under the standing assumptions, the generic-late reduced base map is exactly

```text
g_t = tau_{delta_M} ∘ N_t,
```

where `tau_{delta_M}(u)=u+delta_M (mod M)` and the map `N_t` is given as follows.

#### (A) On every nondefect active cycle
For each `i>=1`,

```text
N_t|_{C_i} = p_gen^{rho_i}|_{C_i}.
```

So every nondefect component is already closed by a constant power of the active map.

#### (B) On the defect cycle `C_*`
Index `C_*` in `p_gen`-order as

```text
C_*=(u_0,...,u_{L-1}),
u_0=1,
u_{j+1}=p_gen(u_j),
```

and define `N_t(u_j)=u_{j+b_j}`.  Then `j -> b_j` is the following explicit three-block
cyclic interval-translation law.

##### (B1) The class `m = 15r+3`

If `r ≢ 2 (mod 3)` (unsplit active case), then `L=5r+1` and

```text
b_j = 3r       for j=0 or 2r+1 <= j <= 5r,
b_j = 3r+2     for 1 <= j <= 2r-2,
b_j = r+2      for 2r-1 <= j <= 2r.
```

If `r ≡ 2 (mod 3)` (split active case), then `L=(5r+2)/3` and

```text
b_0 = 0,
b_j = (4r-2)/3    for 1 <= j <= (r+1)/3,
b_j = (4r+1)/3    for (r+4)/3 <= j <= L-1.
```

##### (B2) The class `m = 15r+9`

If `r ≢ 1 (mod 3)` (unsplit active case), then `L=5r+3`.

- If `r=2` (that is `m=39`), then
  ```text
  b_0 = 0,
  b_j = 2    for 1 <= j <= 10,
  b_j = 3    for 11 <= j <= 12.
  ```

- If `r>=6`, then
  ```text
  b_j = 3      for j=0 or 5r <= j <= 5r+2,
  b_j = r      for 1 <= j <= 4r+2,
  b_j = r+4    for 4r+3 <= j <= 5r-1.
  ```

If `r ≡ 1 (mod 3)` (split active case), then `L=(5r+4)/3` and

```text
b_0 = 0,
b_j = (r-1)/3    for 1 <= j <= (4r+2)/3,
b_j = (r+2)/3    for (4r+5)/3 <= j <= L-1.
```

#### (C) Final explicit form of `g_t`
Therefore the reduced base map is the fully explicit permutation obtained by:

1. applying the constant power `p_gen^{rho_i}` on each nondefect active cycle `C_i`;
2. applying the explicit three-block cyclic interval-translation on the defect cycle `C_*`;
3. applying the ambient splice translation
   ```text
   u -> u + delta_M
   ```
   with
   ```text
   delta_M = 3r+2   if m=15r+3,
   delta_M = r+2    if m=15r+9.
   ```

In particular, in the classes `m ≡ 3,9 (mod 15)` the generic-late reduced base machine
has no remaining hidden local arithmetic.  The only unresolved issue is the global cycle
structure of this explicit finite permutation.

#### Proof
Part (A) is exactly the nondefect-cycle theorem from the odometer-reduction note.
Part (B) is exactly the three-block defect theorem.
Lemma 2.1 computes the ambient translation `delta_M` explicitly in the two residue
classes.  Combining these with the factorization

```text
g_t = tau_{delta_M} ∘ N_t
```

gives the stated explicit description of `g_t`. ∎

---

## 4. Honest consequence for the proof program

The remaining generic-late base-splice problem in the `15r+3` / `15r+9` good branch is
**not** to discover any further local formula.
That part is done.

What remains is only the global orbit analysis of the explicit permutation from Theorem 3.1.
So the next target should be one of the following.

1. Find an odometer / cohomological conjugacy for the whole explicit map `g_t`.
2. Or, if such a conjugacy does not exist uniformly, derive the exact cycle decomposition
   from the explicit piecewise-translation model.

Either way, the problem is now genuinely finite and explicit.

---

## 5. Scope

This note is deliberately narrow.
It does **not** claim a final cycle theorem for `g_t`.
It only packages what is already proved into a single exact theorem in the classes
`m ≡ 3,9 (mod 15)` and `7∤M`.
