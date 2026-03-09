# Further proof progress toward the `suggestion_d` rework

## Executive summary

Using the two new feedback notes, I pushed in exactly the two directions they suggest:

1. a **critical-lane / affine-height** lemma that explains why the transversal splits automatically into arithmetic families with constant itinerary;
2. a sharper **primary-geometry obstruction** result showing that the original Case I defect arrangement already works for colors 0 and 2 for all even `m`, and fails only for color 1 when `m ≡ 4 (mod 6)`.

This is the cleanest new conceptual progress so far.

The strongest genuinely proved statement in this round is:

> If one extends the **primary** (Case I) layer-0 Route E rule to all even `m`, then color 2 is unchanged, color 0 still has the same Hamiltonian first-return structure for every even `m`, and color 1 has the same first-return formula as in Case I for every even `m`.  For `m ≡ 4 (mod 6)`, that color-1 lane map splits into **three closed residue-3 strands**, so the extra Case II affine family is structurally forced by color 1.

This is much stronger conceptually than “the extra family seems to help”: it isolates the **first place the primary geometry breaks**.

I also checked a stronger deletion experiment inside the *actual* Case II rule: if one removes just the added Case II affine family from Definition 4 and leaves the other Case II points untouched, then the induced lane maps for colors 1 and 0 cease to be injective.  I have exact closed forms for those modified maps, verified by direct computation for all even `m ≤ 100`, but I am treating that part as **evidence** for now, not as a finished paper-proof.

---

## 1. A critical-lane lemma from affine height functions

This is the abstract version of the “height-order + defect itinerary” idea.

### Lemma (critical lanes from affine defect heights)
Let the generic bulk map on a working frame be
\[
G(u,t)=(u,t+1)
\]
on `L = { (u,0) : u ∈ Z_m }`, and suppose the defect branches are finitely many maps
\[
D_\alpha(u,t)=(u+\Delta_\alpha,\, t+\tau_\alpha)
\qquad (\alpha \in \mathcal D),
\]
supported on finitely many affine defect components.
Assume:

1. every orbit starting from `L` meets at most `M` defects before first return to `L`;
2. for each defect component, the possible hit-heights on a start lane are given by finitely many affine functions of the lane parameter, each defined on an arithmetic sublattice (for Route E these are parity classes at worst);
3. isolated boundary corrections contribute only finitely many additional exceptional lanes.

Then the set of lanes `x ∈ {0,…,m−1}` decomposes into finitely many arithmetic families such that on each family:

- the ordered defect itinerary is constant;
- the first-return map is affine;
- the return time is affine/constant.

#### Proof
At stage 0, the next defect is whichever candidate height is the smallest one strictly above the current clock value `0`.
The candidates are finitely many affine functions of the lane parameter `x`, defined on finitely many arithmetic supports.
The identity of the minimum can change only when:

- two candidate heights become equal;
- a candidate hits the boundary (`0` or `m`);
- one crosses into or out of its support;
- one reaches an isolated boundary-correction lane.

So after removing finitely many such **critical lanes**, the identity of the first defect is constant on each remaining arithmetic family.

Now fix one such family and suppose the first defect is always `α_1` there.
Then after that defect, the new lane is `x + Δ_{α_1}` and the new clock is an affine function of `x`.
Therefore the candidates for the *second* defect are again finitely many affine functions of `x`, and the same argument applies.

Iterating this for at most `M` defect steps produces only finitely many additional critical lanes.
Hence after deleting the union of all critical lanes, the full defect itinerary is constant on each remaining arithmetic family.
Once the itinerary is fixed, the induced first-return map and return time are just the sums of the corresponding lane and clock increments, so they are affine/constant on that family.

---

### Route E interpretation
For Route E this lemma is already enough to justify the slogan

> affine defect geometry ⇒ arithmetic lane families with constant itinerary.

The only nontrivial denominators are `2`, so the families are simply intervals intersected with parity classes.
In particular, the long interior families for colors 1 and 0 are not ad hoc discoveries; they are forced by the affine height comparisons.

---

## 2. The primary-geometry theorem: colors 0 and 2 survive, color 1 fails exactly at `m ≡ 4 (mod 6)`

Define the **primary Route E geometry** to mean:

- layers `S ≥ 3`, `S = 2`, `S = 1` exactly as in Definition 4;
- on layer `S = 0`, use the **Case I** families `X_{102}, X_{021}, X_{210}` for **all** even `m`.

So this is the original low-complexity defect arrangement, without the extra Case II affine family.

This gives a valid coloring for every even `m ≥ 6`, because each assigned direction triple is still a permutation of `(0,1,2)`.

### 2.1 Color 2 is unchanged
For color 2, the added Case II family never changes the color-2 letter of the triple.
So the color-2 return map is exactly the same as in the current manuscript for all even `m`.
Hence color 2 remains Hamiltonian for all even `m ≥ 6`.

### 2.2 Color 0 still follows the old Case I formulas for all even `m`
The derivation of Proposition `R0-caseI-data` uses only the primary lines `t = 0` and `u = t + 1` and their boundary corrections; it does **not** use `m ≡ 0,2 (mod 6)`.
Therefore the same first-return formulas hold for the primary geometry for every even `m`:
\[
T_0^{\mathrm{pri}}(x)=
\begin{cases}
 m-2,&x=0,\\
 x+2,&1\le x\le m-5,\\
 m-1,&x=m-4,\\
 2,&x=m-3,\\
 1,&x=m-2,\\
 0,&x=m-1.
\end{cases}
\]
The splice proof from the current appendix then shows that `T_0^{pri}` is a single `m`-cycle for every even `m`, with the same block order
\[
(0,m-2\mid 1,3,5,\dots,m-3 \mid 2,4,6,\dots,m-4 \mid m-1).
\]
Thus color 0 stays Hamiltonian in the primary geometry for every even `m ≥ 6`.

### 2.3 Color 1 also follows the old Case I formulas for all even `m`
Likewise, the proof of Proposition `R1-caseI` uses only the primary defect pair
\[
u+t=0,
\qquad
u+2t=m-1,
\]
and their primary boundary corrections.
So the same first-return formulas hold for the primary geometry for every even `m`:
\[
T_1^{\mathrm{pri}}(x)=
\begin{cases}
2,&x=0,\\
x+3,&1\le x\le m-4,\\
1,&x=m-3,\\
0,&x=m-2,\\
3,&x=m-1.
\end{cases}
\]

The difference now lies entirely in the splice pattern.

---

### Proposition (primary color-1 obstruction)
Let `m = 6q + 4` with `q ≥ 1`, and let `T_1^{pri}` be the color-1 induced lane map for the primary geometry above.
Then `T_1^{pri}` is **not** a single `m`-cycle.  In fact it splits into the three closed cycles
\[
(0,2,5,8,\dots,m-2),
\]
\[
(1,4,7,10,\dots,m-3),
\]
\[
(3,6,9,12,\dots,m-1).
\]

#### Proof
For `m = 6q+4`, the three arithmetic progressions relevant to the generic rule `x \mapsto x+3` terminate at
\[
m-2 \equiv 2 \pmod 3,
\qquad
m-3 \equiv 1 \pmod 3,
\qquad
m-1 \equiv 0 \pmod 3.
\]
So the natural ordered blocks are exactly
\[
F_1=(0,2,5,8,\dots,m-2),
\]
\[
F_2=(1,4,7,10,\dots,m-3),
\]
\[
F_3=(3,6,9,12,\dots,m-1).
\]
For all nonterminal points in each block, `T_1^{pri}` applies the generic successor rule `x \mapsto x+3`.
At the terminal points, the special values give
\[
T_1^{\mathrm{pri}}(m-2)=0,
\qquad
T_1^{\mathrm{pri}}(m-3)=1,
\qquad
T_1^{\mathrm{pri}}(m-1)=3.
\]
So each terminal point maps back to the *first point of the same block*.
Thus the splice permutation on `{F_1,F_2,F_3}` is the identity, and each block is a closed cycle.

Therefore `T_1^{pri}` has three cycles and is not Hamiltonian.

---

### Corollary (the extra Case II family is structurally forced by color 1)
The primary Route E geometry already gives the desired Hamiltonian behavior for colors 2 and 0 for every even `m ≥ 6`, but for color 1 it fails exactly when `m ≡ 4 (mod 6)`.
Therefore the extra Case II affine family should be understood as a **repair forced by color 1**.

This is the first clean theorem-level explanation I have for the `m mod 6` split.

---

## 3. What the current Case II repair does to color 1

In the actual manuscript, the added Case II layer-0 family becomes the extra defect line
\[
u+t=1
\]
in the color-1 bulk coordinates.
Together with the primary pair
\[
u+t=0,
\qquad
u+2t=m-1,
\]
it changes the interior dynamics as follows:

- on even interior lanes, the old generic shift `+3` becomes `+2`;
- on odd interior lanes, the old generic shift `+3` becomes `+6`.

So the repair is **not** a cosmetic boundary patch; it changes the macroscopic arithmetic family structure.
The resulting three family-blocks are the current ones from the splice proposition:
\[
(0,2,5,11,\dots,m-5,1),
\]
\[
(3,9,15,\dots,m-1,7,13,\dots,m-3),
\]
\[
(4,6,8,\dots,m-2),
\]
and the splice permutation becomes the 3-cycle `(1 2 3)`.

So the clean story is now:

> primary geometry gives three self-closing residue-3 strands when `m ≡ 4 (mod 6)`;
> the added affine family changes the interior arithmetic rule and turns those three strands into one cyclic splice.

This is the advisor-style explanation I was hoping for.

---

## 4. The color-0 `mod 12` split really is only an ordering phenomenon

The current color-0 Case II proof can now be read as follows.

- The extra Case II family becomes the defect line
  \[
  u = 1 + 2t,
  \]
  with lower/upper defect heights
  \[
  r_-(u)=\frac{u-1}{2},
  \qquad
  r_+(u)=\frac{u-1}{2}+\frac m2
  \]
  on odd lanes.
- The interior generic shift is `+4`, so the bulk arithmetic families are the four residue-4 classes.
- The only difference between `m ≡ 4 (mod 12)` and `m ≡ 10 (mod 12)` is which odd residue-4 family reaches the top endpoint first.

Equivalently, the splice graph is the **same 4-cycle on the same four residue-4 families** in both cases; only the cyclic ordering of the two odd families swaps.

So the color-0 split is not a different mechanism.  It is the same residue-4 splice graph with two different odd-family orderings.

This part is not new compared to the previous note, but it now fits much better with the primary-geometry obstruction above.

---

## 5. Stronger deletion experiment inside the actual Case II rule (evidence, not yet paper-proof)

There is a stronger statement that looks true for the *current* Definition 4, but I do **not** yet count it as a finished proof theorem.

### Modified construction
Take the actual Case II layer-0 rule and delete only the added affine family
\[
\{(1,j,m-1-j):2\le j\le m-2\}\cup\{(2,0,m-2),(2,m-1,m-1)\},
\]
leaving the other Case II special points untouched.
Call the resulting induced lane maps `\widetilde T_1, \widetilde T_0`.

Direct computation from the modified definition gives the exact formulas
\[
\widetilde T_1(x)=
\begin{cases}
2,&x=0,\\
3,&x=1,\\
4,&x=2,\\
x+3,&3\le x\le m-4,\\
1,&x=m-3,\\
0,&x=m-2,\\
3,&x=m-1,
\end{cases}
\]
and
\[
\widetilde T_0(x)=
\begin{cases}
m-2,&x=0,\\
4,&x=1,2,\\
x+2,&3\le x\le m-6,\\
m-1,&x=m-5,m-4,\\
2,&x=m-3,\\
1,&x=m-2,\\
0,&x=m-1.
\end{cases}
\]
These formulas were verified by exact computation from the modified definition for every even
\[
10\le m\le 100,
\qquad
m\equiv 4 \pmod 6.
\]

The immediate consequence is
\[
\widetilde T_1(1)=\widetilde T_1(m-1)=3,
\qquad
\widetilde T_0(1)=\widetilde T_0(2)=4,
\]
so neither induced lane map is injective.

This is stronger than the theorem above: it says that if one removes the added affine family **without rebalancing the other Case II boundary points**, the construction breaks even before the single-cycle question.

At the moment I treat this as exact computational evidence rather than a finalized paper-proof, because I have not yet written the modified first-return derivation cleanly on paper.

---

## 6. What this means for the rewrite direction

I think the next draft can now be reorganized around the following theorem-shaped story.

### Stage A. Primary affine geometry
Use the Case I layer-0 defect arrangement as the base even object and prove:

- color 2 is always Hamiltonian;
- color 0 is always Hamiltonian;
- color 1 fails exactly for `m ≡ 4 (mod 6)` because the three residue-3 strands close on themselves.

This is the cleanest structural explanation of the parity repair that I have so far.

### Stage B. Affine critical-lane / itinerary lemma
Use the lemma from Section 1 to explain why the extra Case II affine family produces the arithmetic families automatically.
That is the right replacement for long orbit-by-orbit tracing.

### Stage C. Finite splice proposition
Once the interior families are in hand, the remaining proof should be a finite splice statement on the family-blocks.
The current splice proposition is already close to this; it just needs to be connected more explicitly to the primary-obstruction story.

---

## 7. What remains unfinished

1. I still do **not** have the fully general monodromy theorem for arbitrary finite affine defect arrangements.
   The critical-lane lemma above is the right abstraction, but I have not yet pushed it to full paper-ready generality.

2. I do **not** yet have a fully written paper-proof of the stronger deletion formulas for
   `\widetilde T_1, \widetilde T_0`.
   I only have exact symbolic/computational confirmation from the modified definition.

3. I do **not** yet have a uniqueness theorem saying Route E is the only minimal repair.
   What I do have now is a much sharper theorem-level statement of **where** the primary geometry fails and **why** the extra family has to target color 1.

---

## Bottom line

The most important new theorem-level progress is:

> the original low-complexity affine defect arrangement already solves colors 0 and 2 for all even `m`, and the only structural obstruction is color 1 at `m ≡ 4 (mod 6)`, where the induced lane map closes three residue-3 strands on themselves.

That is a genuine proof advance, not just exposition.
