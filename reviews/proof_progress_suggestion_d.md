# Proof progress toward the `suggestion_d` rework

## Executive summary

I do **not** have a finished all-colors finite-defect monodromy theorem yet.

I **do** have a cleaner proof layer that sits strictly above the current orbit-by-orbit appendix casework:

1. a reusable **height-order lemma** for first-return maps of the form
   \[
   F(u,t)=\begin{cases}(u,t+1),&\text{off the defect set},\\
   (u+\Delta_\alpha,t+\tau_\alpha),&\text{on defect component }E_\alpha,
   \end{cases}
   \]
   saying that once the ordered defect itinerary is constant on a family of start lanes, the induced first-return map and return time become affine/constant on that whole family;
2. a clean geometric derivation of the **interior itineraries** for Route E colors 1 and 0 from explicit affine height functions;
3. a conceptual explanation of the **mod-6 split** for color 1 and the **mod-12 split** for color 0 in terms of how the extra Case II defect family changes the splice pattern of the same bulk arithmetic runs.

What is still missing for a completely finished abstraction is an automatic theorem that produces the arithmetic-family partition directly from an arbitrary affine defect arrangement. Right now I can prove it for the Route E geometries themselves, but not yet in one fully general theorem.

---

## 1. A local height-order lemma

Let
\[
L=\{(u,0):u\in\mathbb Z_m\}
\]
be the transversal and let the generic branch be
\[
G(u,t)=(u,t+1).
\]
Assume the defect components are finitely many sets on which the map has fixed increments
\[
D_\alpha(u,t)=(u+\Delta_\alpha,t+\tau_\alpha).
\]

### Lemma (height-order reduction)
Fix a family of start lanes \(A\subseteq \mathbb Z_m\). Suppose that for every \(u\in A\), the orbit from \((u,0)\) before first return to \(L\) has the same defect itinerary
\[
\alpha_1,\alpha_2,\dots,\alpha_r,
\]
in the same order, and that the heights at which those defects are encountered are affine functions of \(u\) on \(A\).
Then on \(A\):

1. the induced first-return map is affine,
   \[
   T(u)=u+\sum_{j=1}^r \Delta_{\alpha_j} \pmod m;
   \]
2. the return time \(\rho(u)\) is affine/constant on \(A\);
3. the only remaining global information is how the endpoint lanes of these families splice together.

### Proof
This is just the current defect-itinerary lemma plus the observation that on a family where the itinerary is fixed, the total lane change is the fixed sum of the defect lane-shifts and the generic run lengths are affine in the defect heights.

So the real issue is not computing \(T\) once an itinerary is known; it is proving that the itinerary is constant on large arithmetic families.

---

## 2. Color 1: the geometry already gives the interior formulas

Work in the bulk coordinates
\[
(u,t)=(i-k,k),\qquad G(u,t)=(u,t+1).
\]
The defect lines are:

- \(A: u+t=0\), with lane-shift \(+1\);
- \(B: u+2t=m-1\), with lane-shift \(+2\);
- in Case II only, \(C: u+t=1\), also with lane-shift \(+1\).

For a lane \(u=x\), the corresponding height functions are:
\[
a(x)=m-x\quad (A\text{-height}),
\]
\[
c(x)=m+1-x\equiv 1-x \pmod m\quad (C\text{-height, Case II only}),
\]
and, when \(x\) is odd,
\[
b_-(x)=\frac{m-1-x}{2},\qquad b_+(x)=b_-(x)+\frac m2
\]
for the two \(B\)-heights.

### Proposition C1-I (Case I interior lanes)
Assume \(m\equiv 0,2\pmod 6\).
For every interior lane \(x\notin\{0,m-3,m-2,m-1\}\):

- if \(x\) is even, the itinerary is
  \[
  A\ \to\ B,
  \]
  hence \(T_1(x)=x+3\);
- if \(x\) is odd, the itinerary is
  \[
  B\ \to\ A,
  \]
  hence \(T_1(x)=x+3\).

#### Proof
If \(x\) is even, then \(B\) is absent on lane \(x\), so the first defect is \(A\) at height \(a(x)=m-x\). After the \(+1\) stall, the orbit is on odd lane \(x+1\) at the same clock value.
The lower \(B\)-height on that lane is
\[
b_-(x+1)=\frac{m-x-2}{2}<a(x),
\]
so it is already behind. The upper \(B\)-height is
\[
b_+(x+1)=m-\frac x2-1>a(x),
\]
so this is the next defect. After that \(+2\) stall the orbit is on lane \(x+3\). On lane \(x+3\), both
\[
a(x+3)=m-x-3,
\qquad
b_+(x+3)=m-\frac x2-2
\]
are strictly below the current clock, so there are no further defects before return. Hence the itinerary is \(A\to B\) and the net lane change is \(+3\).

If \(x\) is odd, then the first defect is the lower \(B\)-hit
\[
b_-(x)=\frac{m-1-x}{2}<a(x)=m-x.
\]
After that \(+2\) stall the orbit is on lane \(x+2\). On that lane the next \(A\)-height is
\[
a(x+2)=m-x-2,
\]
while the upper \(B\)-height is
\[
b_+(x+2)=m-\frac{x+3}{2}.
\]
Now
\[
a(x+2)-b_+(x+2)= -\frac{x+1}{2}<0,
\]
so \(A\) comes next. After the \(+1\) stall the orbit lies on even lane \(x+3\), where \(B\) is absent and \(A\) is already behind. So the itinerary is \(B\to A\), again giving net shift \(+3\).

This recovers the generic part of the current Case I formula without tracing individual orbits.

### Proposition C1-II (Case II interior lanes)
Assume \(m\equiv 4\pmod 6\).
For every interior lane \(x\notin\{0,1,2,m-3,m-2,m-1\}\):

- if \(x\) is even, the itinerary is
  \[
  A\ \to\ C,
  \]
  hence \(T_1(x)=x+2\);
- if \(x\) is odd, the itinerary is
  \[
  B\ \to\ A\ \to\ C\ \to\ B,
  \]
  hence \(T_1(x)=x+6\).

#### Proof
If \(x\) is even, then the first defect is \(A\) at height \(a(x)=m-x\). After applying \(A\), the orbit is on lane \(x+1\) at the same clock value. But on lane \(x+1\), the \(C\)-height is
\[
c(x+1)=m-x=a(x),
\]
so the orbit lands **exactly** on \(C\) and the next step is an immediate second defect. After this \(C\)-stall the orbit is on lane \(x+2\), and both \(A\) and \(C\) are behind while \(B\) is absent. Hence the itinerary is \(A\to C\), with net shift \(+2\).

If \(x\) is odd, the first defect is again the lower \(B\)-hit \(b_-(x)\). After the \(+2\) shift the orbit is on lane \(x+2\). There,
\[
a(x+2)=m-x-2 < c(x+2)=m-x-1,
\]
and also
\[
a(x+2)< b_+(x+2)=m-\frac{x+3}{2},
\]
so the next defect is \(A\). After applying \(A\), the orbit is on lane \(x+3\) at height \(a(x+2)\), and on that lane
\[
c(x+3)=m-x-2=a(x+2),
\]
so again there is an immediate \(C\)-defect. After \(C\) the orbit lies on lane \(x+4\). On that lane, \(A\) and \(C\) are behind, while the upper \(B\)-height
\[
b_+(x+4)=m-\frac{x+5}{2}
\]
is still ahead. So the next defect is this upper \(B\)-hit, giving the fourth and last stall and total lane change \(+6\).

This recovers the generic part of the Case II formula directly from the defect geometry.

### Consequence for the splice graph in color 1
The interior rules already explain the family structure.

- In Case I, the generic map is \(+3\), so the lane set breaks into the three residue-\(3\) families, and the finitely many boundary lanes \(0,m-3,m-2,m-1\) splice them into one cycle.
- In Case II, the even lanes form one \(+2\) family, while the odd lanes split into two \(+6\) families. The boundary lanes then splice these three family-blocks into one directed 3-cycle.

So for color 1 the appendix orbit traces can be replaced by a comparison-of-heights proof plus a short boundary check.

---

## 3. Color 0: the same method also compresses the interior casework

Work directly in the bulk frame
\[
(x,y)=(i+2k,k),\qquad G(x,y)=(x,y+1).
\]
Now \(y\) is literally a clock and \(x\) is the lane coordinate.

The relevant defect families are:

- \(B\): the base line \(y=0\), with shift \((x,y)\mapsto(x+1,y+1)\);
- \(A\): the line \(x=y+1\), with shift \((x,y)\mapsto(x+1,y+2)\);
- in Case II only, \(R\): the line \(x=1+2y\), with shift \((x,y)\mapsto(x+2,y+2)\).

There are also finitely many isolated boundary corrections \(P,Q,S\) (and the point \((m-2,0)\) carrying a special \(R\)-move), but the long-range dynamics come only from \(A,B,R\).

For an odd lane \(u\), the two \(R\)-heights are exactly
\[
r_-(u)=\frac{u-1}{2},\qquad r_+(u)=\frac{u-1}{2}+\frac m2.
\]

### Proposition C0-I (Case I interior lanes)
Assume \(m\equiv 0,2\pmod 6\).
For every interior lane \(1\le x\le m-5\), the itinerary is
\[
B\ \to\ A,
\]
so \(T_0(x)=x+2\).

#### Proof
From \((x,0)\), the first defect is always \(B\), sending the orbit to \((x+1,1)\). On lane \(x+1\), the first defect ahead is the unique \(A\)-point \((x+1,x)\), reached after \(x-1\) generic steps. After applying \(A\), the orbit is at \((x+2,x+2)\). On lane \(x+2\), the only possible \(A\)-point is \((x+2,x+1)\), already behind the current clock, and \(B\) occurs only on \(y=0\) (plus two isolated boundary points on other lanes, which are not ahead on lane \(x+2\)). Hence there are no further defects before first return, so the itinerary is \(B\to A\) and the net lane shift is \(+2\).

### Proposition C0-II (Case II interior lanes)
Assume \(m\equiv 4\pmod 6\).
For every interior lane \(x\notin\{0,1,2,m-6,m-5,m-4,m-3,m-2,m-1\}\):

- if \(x\) is odd, the itinerary is
  \[
  B\ \to\ A\ \to\ R,
  \]
  hence \(T_0(x)=x+4\);
- if \(x\) is even, the itinerary is
  \[
  B\ \to\ R\ \to\ A,
  \]
  hence \(T_0(x)=x+4\).

#### Proof
If \(x\) is odd, the first step is \(B\):
\[
(x,0)\xrightarrow{B}(x+1,1).
\]
The lane \(x+1\) is even, so there is no \(R\)-defect there. The next defect is therefore the \(A\)-point \((x+1,x)\). After applying \(A\) the orbit is at \((x+2,x+2)\), now on an odd lane. The lower \(R\)-height on lane \(x+2\) is
\[
r_-(x+2)=\frac{x+1}{2}<x+2,
\]
so it is behind, while the upper one
\[
r_+(x+2)=\frac{x+1}{2}+\frac m2
\]
is ahead for \(x\le m-7\). After this \(R\)-jump the orbit lands on lane \(x+4\), where \(A\) is already behind and there is no further \(R\)-hit before return. Thus the itinerary is \(B\to A\to R\), giving net shift \(+4\).

If \(x\) is even, the first step is again \(B\), landing on odd lane \(x+1\). Now the next \(R\)-height is the lower one,
\[
r_-(x+1)=\frac x2,
\]
which lies ahead of the current clock value \(1\). So the next defect is \(R\), sending the orbit to lane \(x+3\). On that odd lane, the lower \(R\)-height is already behind, while the \(A\)-height \(x+2\) occurs before the upper \(R\)-height as long as \(x\le m-8\). Thus the next defect is \(A\), after which the orbit reaches lane \(x+4\) and no further defect is ahead. Hence the itinerary is \(B\to R\to A\), again giving net shift \(+4\).

This is the conceptual core of the Case II formula.

### Consequence for the splice graph in color 0
This explains the mod-12 split almost exactly as hoped in `suggestion_d`.

- In Case I, the generic interior rule is \(+2\), so the lane set splits into two long arithmetic runs (odd and even), and the boundary corrections splice them through a two-point block \((0,m-2)\) and a one-point tail \((m-1)\).
- In Case II, the generic interior rule is \(+4\), so the natural bulk families are the four residue-\(4\) classes.
  The only difference between \(m\equiv 10\pmod{12}\) and \(m\equiv 4\pmod{12}\) is **which odd residue-4 family contains the endpoint near the top of the range**. Equivalently, the same 4-block splice graph appears in both cases, but the cyclic order of the two odd residue classes swaps.

So for color 0 the mod-12 split is not a different mechanism; it is a different cyclic ordering of the same residue-4 splice graph.

---

## 4. What this gives immediately for a rework

A realistic next version of the paper could replace most of the long appendix orbit traces by the following proof pattern.

### Step 1: defect-itinerary lemma
Keep the current finite-defect and defect-itinerary lemmas.

### Step 2: height-order propositions
Add short propositions for colors 1 and 0 saying:

- here are the defect height functions;
- on each interior arithmetic family, the ordered defect itinerary is constant;
- therefore the induced lane map is affine on that family.

For Route E, the interior families are:

- color 1, Case I: odd vs. even interior lanes;
- color 1, Case II: odd vs. even interior lanes, with two odd \(+6\) families emerging at the splice stage;
- color 0, Case I: one interior family with generic \(+2\);
- color 0, Case II: odd vs. even interior lanes, giving generic \(+4\).

### Step 3: finite splice proposition
Then keep only a short finite splice proposition that handles the bounded set of boundary lanes and says which arithmetic family-block comes next.

At that point the paper would say, in substance:

> bulk motion gives the long arithmetic families;
> affine defect lines determine their itineraries by height comparisons;
> isolated boundary corrections only splice finitely many family-blocks;
> the splice permutation is a single cycle.

That is much closer to the advisor vision.

---

## 5. What is still open

### 5.1 Not yet proved abstractly
I do **not** yet have a fully general theorem of the form

> any finite union of affine defect lines over a primitive bulk translation automatically yields an arithmetic-family partition with constant itinerary.

The current proofs above still use the very special Route E line arrangements and their explicit height functions.

### 5.2 Necessity of the extra Case II family
I also do **not** yet have a clean theorem saying that the extra Case II defect family is mathematically forced.

I do have supporting evidence from modified calculations:

- if one removes the extra Case II family from the color-1 Route E rule but leaves the rest of the construction unchanged, the induced lane map \(T_1\) is no longer a single cycle in the tested cases \(m=10,16,22\); it splits into two cycles;
- doing the analogous modification for color 0 in the same tested cases gives a map with four cycles.

That is good evidence for a “missing bridge” phenomenon, but at the moment it is still evidence, not a theorem.

---

## 6. Best candidate theorem to chase next

The next serious target should be a theorem of this form:

### Candidate theorem (Route E monodromy theorem)
For each Route E color map in adapted bulk coordinates, there is a finite partition of the transversal into arithmetic families such that:

1. on each family the ordered defect itinerary is constant;
2. the induced first-return map is affine on that family;
3. the cycle structure is determined by a finite splice permutation on the family labels, depending only on the defect arrangement and the lane-shifts.

This is already proved above for the current Route E geometries **up to the finite boundary splice step**. Finishing that theorem in a paper-ready form looks realistic.
