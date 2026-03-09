# Further proof progress toward the `suggestion_d` rework (round 3)

## Executive summary

This round follows the two latest feedback notes very closely:

- keep the abstraction **Route-E-specific and bounded**, rather than chasing a universal affine-defect theorem;
- replace the large deletion experiment by a **small noninjectivity theorem with explicit colliding lanes**.

That produces one new paper-relevant theorem-level gain.

> For the actual Case II Route E rule, if one deletes **only** the added Case II affine family from the layer-0 assignment (together with its two endpoints) and leaves all other Case II special points untouched, then the induced lane maps cease to be injective:
> \[
> \widetilde T_1(1)=\widetilde T_1(m-1)=3,
> \qquad
> \widetilde T_0(1)=\widetilde T_0(2)=4.
> \]
> In particular, the added Case II family is not merely a convenient embellishment; within the present scaffold it carries genuine repair work that boundary corrections alone do not perform.

This is the right scale of necessity statement.  It does **not** claim uniqueness of Route E, and it does **not** require a full modified closed form for the deleted variant.

Combined with the previous two progress notes, the current proof picture is now:

1. **Primary geometry and obstruction.**  The Case I low-layer geometry extends naturally to all even `m`; colors 0 and 2 already work there, while color 1 fails exactly at `m ≡ 4 (mod 6)` by closing into three residue-3 strands.
2. **Comparison machinery.**  The actual Case II extra family changes the affine defect-height ordering, giving the previously derived interior rules `+2 / +6` for color 1 and `+4` for color 0.
3. **Necessity at the correct scale.**  If one tries to keep the Case II boundary corrections but removes the added interior family itself, the induced lane maps are already noninjective on two explicit pairs of lanes.

That is a much cleaner advisor-style story than the original “Case II happens to work” narrative.

---

## 1. The primary-geometry obstruction theorem (from round 2)

I keep the main theorem from the previous note, since it remains the structural starting point.

### Definition (primary Route E geometry)
For every even `m >= 6`, define the **primary Route E geometry** by keeping layers `S >= 1` exactly as in the current Route E definition, and on layer `S = 0` using the **Case I** families for all even `m`:
\[
X_{102},\ X_{021},\ X_{210},
\]
with the default triple `120` elsewhere.

So this is the original low-complexity geometry, with no added Case II affine family.

### Theorem A (primary geometry works for colors 0 and 2, and fails first in color 1)
Let `m = 6q+4 >= 10`.
For the primary geometry:

1. color `2` is unchanged from the current manuscript and remains Hamiltonian;
2. color `0` still has the old Case I induced lane map and remains Hamiltonian;
3. color `1` still has the old Case I induced lane map
   \[
   T_1^{\mathrm{pri}}(x)=
   \begin{cases}
   2,&x=0,\\
   x+3,&1\le x\le m-4,\\
   1,&x=m-3,\\
   0,&x=m-2,\\
   3,&x=m-1,
   \end{cases}
   \]
   and this map splits into the three closed cycles
   \[
   (0,2,5,8,\dots,m-2),
   \]
   \[
   (1,4,7,10,\dots,m-3),
   \]
   \[
   (3,6,9,12,\dots,m-1).
   \]

Hence the first genuine obstruction in the primary geometry occurs in **color 1 at `m ≡ 4 (mod 6)`**.

### Proof sketch
This is exactly the round-2 theorem.
The color-2 part is unchanged because the added Case II family never alters the color-2 letter.
For color 0 and color 1, the Case I return-map derivations use only the primary defect families and boundary points, so the same formulas remain valid under the primary geometry for all even `m`.
The cycle decomposition for `T_1^{pri}` is immediate from the formula above: the generic successor rule is `x -> x+3`, and the three terminal values map back to the first point of the same residue-3 block.

This explains **why** the Case II story exists: the base geometry already solves colors 0 and 2, and the only missing piece is to break the residue-3 closure of color 1.

---

## 2. A paper-sized necessity statement: deleting the added Case II family breaks injectivity

The latest feedback strongly suggested that I do **not** need a full deleted-variant closed form in the paper.
A pair of explicit collisions is enough.

That is what I prove here.

### Definition (deleted-extra-family variant)
Assume `m = 6q+4 >= 10` and start from the **actual** Case II Route E rule.
Define the deleted-extra-family variant by changing only the added Case II family
\[
Y_{210}^{\mathrm{add}}
:=
\{(1,j,m-1-j):2\le j\le m-2\}
\cup
\{(2,0,m-2),(2,m-1,m-1)\}
\]
back to the default triple `120`, and keeping all other Case II assignments unchanged.

Let `\widetilde R_c` and `\widetilde T_c` denote the corresponding return maps on `P_0` and the induced lane maps on the same transversals as in the current paper.

So this is exactly the “keep the Case II boundary corrections, but remove the added bulk affine family itself” experiment.

### Proposition B1 (color 1 becomes noninjective)
For every `m = 6q+4 >= 10`,
\[
\widetilde T_1(1)=\widetilde T_1(m-1)=3.
\]
Hence `\widetilde T_1` is not injective.

#### Proof
Work in the current color-1 bulk coordinates
\[
(u,t)=(i-k,k),
\qquad
G(u,t)=(u,t+1).
\]
Under the deleted-extra-family variant, the interior defect line `u+t=1` is removed, but all other Case II boundary corrections remain.

**Lane `1`.**
The start point `(u,t)=(1,0)` is the retained isolated point `(i,k)=(1,0)` on `P_0`.
At this point the color-1 branch is still the `+2` stall, so one step gives
\[
(1,0)\longmapsto(3,0).
\]
This is already a first return to the transversal `t=0`, hence
\[
\widetilde T_1(1)=3.
\]

**Lane `m-1`.**
Start from `(u,t)=(m-1,0)`.
Because the top endpoint of the old `u+2t=m-1` family is no longer a defect here, the first step is generic:
\[
(m-1,0)\xrightarrow{G}(m-1,1).
\]
Now `(m-1,1)` lies on the primary defect line `u+t=0`, so the next step is the `+1` stall:
\[
(m-1,1)\longmapsto(0,1).
\]
Since the interior line `u+t=1` has been deleted, the orbit now climbs generically on lane `0` all the way up to the retained boundary point `(0,m-1)`:
\[
(0,1)\xrightarrow{G^{m-2}}(0,m-1).
\]
At `(0,m-1)` the retained isolated boundary correction gives a `+2` stall,
\[
(0,m-1)\longmapsto(2,m-1),
\]
and at `(2,m-1)` the retained point corresponding to `(i,k)=(1,m-1)` gives a final `+1` stall,
\[
(2,m-1)\longmapsto(3,m-1).
\]
One generic step returns to the transversal:
\[
(3,m-1)\xrightarrow{G}(3,0).
\]
Therefore
\[
\widetilde T_1(m-1)=3.
\]
So `\widetilde T_1` is not injective.

---

### Proposition B2 (color 0 also becomes noninjective)
For every `m = 6q+4 >= 10`,
\[
\widetilde T_0(1)=\widetilde T_0(2)=4.
\]
Hence `\widetilde T_0` is not injective.

#### Proof
Work in the current color-0 bulk coordinates
\[
(u,t)=(i+2k,k),
\qquad
G(u,t)=(u,t+1).
\]
In these coordinates the primary defect set is supported on `t=0` and `u=t+1`; the actual Case II rule adds the interior family `u=1+2t`.
In the deleted-extra-family variant that interior family is removed, but the retained boundary points are left unchanged.

**Lane `1`.**
The start point `(u,t)=(1,0)` is a retained isolated boundary point, and it still carries the `(+2,+2)` jump.  So
\[
(1,0)\longmapsto(3,2).
\]
Now `(3,2)` lies on the primary defect line `u=t+1`, giving the usual `(+1,+2)` jump:
\[
(3,2)\longmapsto(4,4).
\]
From `(4,4)` there are no further defects ahead before first return: the line `u=t+1` has already been passed on lane `4`, the deleted interior family `u=1+2t` is absent, and `t=0` occurs only at return.  Hence the orbit climbs generically back to `(4,0)`, so
\[
\widetilde T_0(1)=4.
\]

**Lane `2`.**
Start from `(u,t)=(2,0)`.
This lies on the ordinary base defect line `t=0`, so the first step is the usual `(+1,+1)` move:
\[
(2,0)\longmapsto(3,1).
\]
Then one generic step gives
\[
(3,1)\xrightarrow{G}(3,2),
\]
and from there the same `u=t+1` defect as above sends the orbit to `(4,4)`.
Again there are no further defects before return, so the orbit climbs generically to `(4,0)`.
Thus
\[
\widetilde T_0(2)=4.
\]
Therefore `\widetilde T_0` is not injective.

---

### Corollary B3 (boundary corrections alone do not carry the Case II repair)
Within the present Route E scaffold, the added Case II affine family is doing genuine bulk repair work.
If one removes that family but leaves the remaining Case II boundary corrections in place, the induced lane maps for colors 1 and 0 are already noninjective.

This is the right scale of necessity claim:

- it does **not** assert uniqueness of Route E;
- it does **not** claim that no other repair could exist;
- it does show that the actual added family is not a cosmetic appendage and cannot be replaced by the retained boundary corrections alone.

That seems exactly aligned with the strongest feedback.

---

## 3. How this fits the earlier geometric comparison proofs

The current structural picture is now quite tight.

### Stage A: base geometry and obstruction
The primary geometry theorem shows that the natural low-complexity geometry already solves colors 0 and 2, and that the first failure is the residue-3 closure of color 1 when `m ≡ 4 (mod 6)`.

### Stage B: comparison geometry
The previous proof note (`proof_progress_suggestion_d.md`) already gave the defect-height comparison proofs for the actual Case II interior rules:

- color 1, Case II: even lanes have itinerary `A -> C` and shift `+2`, odd lanes have itinerary `B -> A -> C -> B` and shift `+6`;
- color 0, Case II: odd lanes have itinerary `B -> A -> R`, even lanes have itinerary `B -> R -> A`, both giving shift `+4`.

So the interior arithmetic families and the mod-splits now come from affine height comparisons rather than from repeated orbit tracing.

### Stage C: splice and payoff
The splice-graph proposition from the current integrated manuscript already packages the final finite closure step.
The new noninjectivity propositions above show that the added Case II family is not just helping the splice proposition cosmetically; it is essential to getting a valid induced lane permutation in the first place.

This gives the clean proof story I was hoping for:

> primary geometry -> precise obstruction -> forced bulk repair -> finite splice.

---

## 4. What is now genuinely theorem-level, and what is still only evidence

### Fully proved at theorem scale
I now regard the following as theorem-level progress, not just heuristic improvement.

1. **Primary-geometry obstruction theorem.**
   The Case I low-layer geometry extends naturally to all even `m`; it already works for colors 0 and 2; and color 1 fails exactly at `m ≡ 4 (mod 6)` by splitting into three residue-3 cycles.

2. **Deleted-extra-family noninjectivity theorem.**
   In the actual Case II scaffold, removing only the added affine family and keeping the remaining Case II corrections makes `\widetilde T_1` and `\widetilde T_0` noninjective, with explicit witnesses.

Those two results are both paper-sized and conceptually strong.

### Still not fully abstracted
I still do **not** have a universal monodromy theorem for arbitrary finite affine defect arrangements.
I also do **not** have a uniqueness theorem for Route E.
The current progress does not need either one.

### Still only supporting evidence
The full deleted-variant closed forms from the round-2 computations remain **supporting evidence**, not proof ingredients.
After the new noninjectivity propositions, I do not think the paper needs those closed forms at center stage.
They can stay as computational backup.

---

## 5. What I think the next rewrite should now aim for

The proof architecture is now stable enough that I do **not** think the next mathematical step should be a broader theorem.
The next step should be a manuscript rewrite around the following three nodes.

1. **Primary Geometry Obstruction.**
   Introduce the primary geometry as the natural baseline and prove that only color 1 at `m ≡ 4 (mod 6)` fails.

2. **Critical-Lane / Height-Comparison Lemma.**
   Use the bounded Route-E-specific comparison lemma from the earlier note to derive the actual Case II interior arithmetic rules.

3. **Finite splice proposition.**
   Keep the existing splice-graph closure for the final bounded family-block permutation.

The deleted-extra-family proposition can then sit as a short remark or appendix proposition showing why the repair is genuinely doing bulk work.
That seems to answer both recent feedback notes in the most economical way.
