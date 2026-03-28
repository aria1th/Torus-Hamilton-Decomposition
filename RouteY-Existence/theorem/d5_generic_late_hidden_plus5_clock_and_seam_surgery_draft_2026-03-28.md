# d=5 generic-late reduced arithmetic after the odometer pass: a main-flow synthesis and a draft seam-surgery theorem
Date: 2026-03-28

## Goal

This note is not another local proof packet.  Its purpose is to flatten the current
generic-late arithmetic story into one clean main flow.

The central point is now clear:

- the D3/D4 odometer viewpoint was the right direction;
- but the final D5 reduced base machine is **not** usually one global odometer;
- instead it is an explicit **odometer-with-seams** object.

So this note has two jobs.

1. Record the strongest theorem-order synthesis that is already justified by the March 27/28 notes.
2. State, honestly and without overclaiming, the remaining target theorem in the right language.

Throughout, assume

```text
m = 3M >= 33,
5 ∤ m,
t is generic late.
```

We separate the good branch `7 ∤ M` from the bad branch `7 | M`.

---

## 1. The proved backbone

### 1.1 Active arithmetic is closed

The generic-late active permutation `p_gen` is already fully understood.

- If `M ≢ 2 (mod 3)`, then `p_gen` is a single `M`-cycle.
- If `M ≡ 2 (mod 3)`, then with `Q=(M-2)/3`, the cycle type is
  ```text
  Q, Q+1, Q+1.
  ```

So the old mod-`5` active frontier is gone.

### 1.2 Base splice splits at `7`

For the generic-late base return `P_t` on `B_m`:

- if `7 ∤ M`, then
  ```text
  P_t(a) ≡ a+2 (mod 3),
  ```
  so the splice problem reduces exactly to an `M`-point permutation
  ```text
  g_t(u) := (P_t^3(3u+1)-1)/3;
  ```
- if `7 | M`, there is an explicit fixed-point obstruction, so single-cycle base splicing is impossible.

Thus the real arithmetic target is the good branch reduced machine `g_t`.

### 1.3 The reduced base machine factors through a first-special-hit map

On the good branch there is an exact factorization

```text
g_t = τ_{δ_M} ∘ N_t,
```

where

- `τ_{δ_M}(u)=u+δ_M` is a constant ambient splice translation,
- `N_t` is the active first-special-hit map,
- and in the scaled coordinate `K=5u`, the ambient splice is simply
  ```text
  K -> K+7.
  ```

So the final reduced map is “active odometer first, constant splice second”.

### 1.4 The active skew product has one defect only

On the active class `A=3u+1`, the ordinary source evolution is

```text
u -> p_gen(u),
e -> e-5 + 2 * 1[u=1].
```

So the fast clock is uniform `-5`, and the only defect is the single anomaly point `u=1`.

This is the structural origin of the D5 clock.

### 1.5 Nondefect active cycles are rigid

If an active cycle `C` does not contain `u=1`, then

```text
N_t|_C = p_gen^{m-1 mod |C|}.
```

So all nondefect active cycles are already exact rigid rotations.

### 1.6 The defect cycle is explicit in the `15r+3 / 15r+9` classes

In the arithmetic classes

```text
m ≡ 3,9 (mod 15),
7 ∤ M,
```

the unique defect cycle of `N_t` is an explicit **three-block cyclic interval-translation machine**.
That is the content of the March 27 defect three-block theorem.

So in these classes, there is no hidden local arithmetic left.

### 1.7 Split branch: componentwise odometer yes, one global odometer no

When `M ≡ 2 (mod 3)`, the split active case gives a particularly clear picture.

At the level of `N_t`, one gets a componentwise straightening:

- one fixed point,
- one `Q`-point rigid rotation on the defect remainder,
- one `Q`-point rigid rotation on the nondefect `Q`-cycle,
- one `(Q+1)`-point rigid rotation on the remaining nondefect cycle.

So the D3/D4 intuition survives **componentwise**.

However, the full reduced map `g_t = τ_{δ_M} ∘ N_t` is **not** universally conjugate to one global translation on `Z_M`.
Prime-size counterexamples already occur; for instance:

- `m=69`, `M=23`: cycle type `[17,3,3]`;
- `m=123`, `M=41`: cycle type `[31,5,5]`.

Hence the universal D5 theorem is not “one global odometer”.

---

## 2. The current synthesis theorem

## Theorem 2.1 (current explicit reduced-machine synthesis)

Assume

```text
m = 3M >= 33,
5 ∤ m,
7 ∤ M,
t is generic late,
m ≡ 3 or 9 (mod 15).
```

Then the reduced base machine `g_t : Z_M -> Z_M` is an explicit finite seam-surgery of rigid odometer pieces, in the following precise sense.

1. **Exact factorization**
   ```text
   g_t = τ_{δ_M} ∘ N_t.
   ```

2. **Fast clock**
   In the scaled coordinate `K=5u`, the ambient splice is
   ```text
   K -> K+7.
   ```

3. **Nondefect components**
   On every active cycle not containing `u=1`, the map `N_t` is a rigid rotation, namely
   ```text
   N_t|_C = p_gen^{m-1 mod |C|}.
   ```

4. **Defect component**
   On the unique active cycle containing `u=1`, the map `N_t` is a cyclic three-block interval-translation with explicit run lengths and offsets.

5. **Split branch refinement**
   If `M ≡ 2 (mod 3)`, then after straightening the active circles in `p_gen`-order,
   the map `N_t` becomes a disjoint union of rigid rotations (plus one fixed point) on
   ```
   Z_Q, Z_Q, Z_{Q+1},
   ```
   where `Q=(M-2)/3`.

Consequently, in these classes the whole reduced base machine is already an **explicit finite permutation assembled from odometer pieces and a finite seam correction**.
What remains open is not local arithmetic, but only the global cycle structure of this explicit seam-glued permutation.

### Proof

Item (1) is the odometer-reduction theorem.
Item (3) is the nondefect power law from the same note.
Item (4) is the defect three-block theorem.
Item (5) is the split componentwise conjugacy theorem.
Item (2) is the `K=5u` restatement of the constant splice translation.
Combining them yields the stated synthesis. ∎

---

## 3. The correct slogan

The right D5 slogan is now:

> **Hidden `+5` clock, one defect source, finite seam surgery.**

This is strictly richer than the D3/D4 final picture.

- D3/D4 end at an odometer (or a finite-defect odometer) on the final return section.
- D5 seems to end at an explicit **odometer-with-seams** machine.

So the conceptual gain from the odometer pass is not that D5 collapses to the same theorem as D3/D4.
It is that the remaining complexity is now compressed into a finite seam-gluing problem.

---

## 4. Honest target theorem (not yet proved)

The natural remaining theorem is no longer a translation-conjugacy statement.

It should look more like this.

## Draft Theorem 4.1 (finite seam graph theorem for the reduced base machine)

In the generic-late good branch `7 ∤ M`, the reduced base machine `g_t` is conjugate to a finite combinatorial gluing of rigid odometer components.
Equivalently, there should exist a finite seam graph `Γ_{m,t}` and a finite set of seam data such that the cycle decomposition of `g_t` is exactly the cycle decomposition of the induced gluing operator on `Γ_{m,t}`.

In the classes `m ≡ 3,9 (mod 15)`, all local data needed to build `Γ_{m,t}` are already explicit.

This is only a **draft target theorem**.  It is not claimed as proved here.

---

## 5. What is and is not still open

### Already closed

- local visibility chain, in its dependency-clean form;
- generic-late active arithmetic;
- generic-late `7`-split for base splice;
- good-branch factorization `g_t = τ_{δ_M} ∘ N_t`;
- nondefect rigid law;
- explicit defect three-block law in the `15r+3 / 15r+9` classes;
- componentwise odometer structure in the split branch;
- failure of the universal global-translation-conjugacy strategy.

### Still open

- the final cycle theorem for the full reduced base machine `g_t`;
- the best language for the seam graph / gluing operator;
- the `5 | m` branch;
- manuscript integration.

---

## 6. Reading order

For the cleaned current flow, read in this order.

1. `d5_generic_late_base_splice_7split_theorem_2026-03-27.md`
2. `d5_generic_late_base_splice_odometer_reduction_2026-03-27.md`
3. `d5_generic_late_defect_three_block_theorem_2026-03-27.md`
4. `d5_generic_late_reduced_base_machine_15r3_15r9_theorem_2026-03-27.md`
5. `d5_generic_late_split_componentwise_conjugacy_and_global_nogo_2026-03-28.md`
6. the present synthesis note

This is the main reduced-arithmetic story after the odometer pass.
