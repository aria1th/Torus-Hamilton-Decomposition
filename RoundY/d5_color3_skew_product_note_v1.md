# d=5 note: triangular skew-product criterion and color-3 extraction

## Problem
Extract the color-3 argument from the fixed 26-move witness in a theorem-ready form:
**first-return reduction + clean-frame lemma + triangular skew-product Hamiltonicity criterion + color-3 instantiation**.

For colors 0/1/4, do not chase full formulas first. Record only the failure profile:
1. clean-frame existence,
2. cycle decomposition of \(U_c\),
3. orbitwise monodromy.

Then choose the next branch.

---

## 1. First-return reduction

Let
\[
S(x)=x_0+x_1+x_2+x_3+x_4 \pmod m,
\qquad
P_0=\{x\in (\mathbb Z_m)^5 : S(x)=0\}.
\]
For each color \(c\), the color-\(c\) map \(f_c\) increments exactly one coordinate by \(+1\), hence
\[
S(f_c(x))=S(x)+1 \pmod m.
\]
Therefore \(f_c\) meets \(P_0\) once every \(m\) steps, and the first return
\[
R_c = f_c^m\big|_{P_0}
\]
is a permutation of \(P_0\cong (\mathbb Z_m)^4\).

**Lemma 1.**  
\(f_c\) is a Hamilton cycle on \((\mathbb Z_m)^5\) if and only if \(R_c\) is a single cycle on \(P_0\).

**Proof.**  
Every \(f_c\)-orbit visits the \(m\) layer classes \(S=0,1,\dots,m-1\) cyclically, so each \(R_c\)-orbit is exactly the intersection of an \(f_c\)-orbit with \(P_0\). Lifting and restricting are inverse operations. ∎

---

## 2. Clean frames

Write \(P_0\cong (\mathbb Z_m)^4\). A **clean frame** for \(R_c\) means an affine coordinate system
\[
A:P_0\to (\mathbb Z_m)^3\times \mathbb Z_m,\qquad A(x)=(b,z),
\]
such that
\[
A R_c A^{-1}(b,z)=(B_c(b),\, z+\beta_c(b)).
\]
So the last coordinate is a pure cocycle over a 3-dimensional base.

This notion has a coordinate-free test.

**Lemma 2 (clean-frame detection).**  
A clean frame exists for \(R_c\) if and only if there is a nonzero order-\(m\) vector
\[
k\in (\mathbb Z_m)^4
\]
such that
\[
R_c(x+k)=R_c(x)+k \qquad \text{for all } x\in P_0.
\]

**Proof.**

- If a clean frame exists, let \(k=A^{-1}(0,0,0,1)\). Then
  \[
  A R_c(x+k)=A R_c(x)+ (0,0,0,1),
  \]
  which is exactly \(R_c(x+k)=R_c(x)+k\).

- Conversely, assume \(R_c(x+k)=R_c(x)+k\) for some nonzero order-\(m\) vector \(k\). Choose a complement \(W\) to \(\langle k\rangle\), write each point uniquely as \(x=w+zk\) with \(w\in W\), \(z\in \mathbb Z_m\). Then
  \[
  R_c(w+zk)=R_c(w)+zk,
  \]
  so the quotient by \(\langle k\rangle\) is well defined and \(R_c\) has the form
  \[
  (b,z)\mapsto (B_c(b), z+\beta_c(b)).
  \]
∎

This lemma is the right diagnostic: if no such \(k\) exists, then the current witness does not even reach the triangular-skew-product stage.

---

## 3. Triangular skew-product Hamiltonicity criterion

Assume \(R\) has clean coordinates
\[
R(a,s,z)=\bigl(B_0(a,s),\ s+1,\ z+\beta(a,s)\bigr),
\]
where \(a\in A=(\mathbb Z_m)^2\), \(s\in \mathbb Z_m\), \(z\in \mathbb Z_m\).  
So \(s\) is a strict clock.

Let
\[
B(a,s)=\bigl(B_0(a,s), s+1\bigr),
\qquad
U=B^m\big|_{\{s=0\}}.
\]
Then \(U\) is a permutation of \(A\).

For a \(U\)-orbit \(O\subset A\), let \(\widetilde O\) be the lifted \(B\)-orbit in \(A\times \mathbb Z_m\). Define its **orbitwise monodromy**
\[
M(O)=\sum_{y\in \widetilde O}\beta(y)\pmod m.
\]

**Theorem 3 (triangular skew-product Hamiltonicity criterion).**

1. The \(B\)-orbits are exactly the \(m\)-fold lifts of the \(U\)-orbits.
2. If \(|\widetilde O|=L\), then over \(\widetilde O\) the full skew product \(R\) splits into
   \[
   \gcd(m,M(O))
   \]
   cycles, each of length
   \[
   \frac{Lm}{\gcd(m,M(O))}.
   \]
3. Hence \(R\) is a single cycle if and only if:
   - \(U\) is a single cycle, and
   - on that unique \(U\)-orbit, \(M(O)\) is a unit in \(\mathbb Z_m\).

**Proof.**

Because \(s\mapsto s+1\), every \(B\)-orbit meets the section \(\{s=0\}\) exactly once every \(m\) steps, so \(B\)-orbits are precisely the lifts of \(U\)-orbits. This proves (1).

Fix one lifted orbit \(\widetilde O\) of size \(L\). Number it cyclically as \(y_0,\dots,y_{L-1}\), so \(B(y_i)=y_{i+1}\). On \(\widetilde O\times \mathbb Z_m\),
\[
R(y_i,z)=\bigl(y_{i+1},\, z+\beta(y_i)\bigr).
\]
After \(L\) steps,
\[
R^L(y_0,z)=\bigl(y_0,\, z+M(O)\bigr).
\]
Thus the induced fiber map is translation by \(M(O)\) on \(\mathbb Z_m\), which has \(\gcd(m,M(O))\) cycles. Lifting back gives (2). Statement (3) is immediate. ∎

This is the reusable criterion that the color-3 argument should be quoted through.

---

## 4. Color 3 instantiation

For color \(3\), use relative coordinates on \(P_0\):
\[
(q,w,v,u)=(x_4,x_0,x_1,x_2),
\qquad
x_3=-(q+w+v+u).
\]

For the fixed 26-move witness, the first return has the exact form
\[
R_3(q,w,v,u)=\bigl(B_3(q,w,u),\ v+\beta_3(q,w,u)\bigr),
\]
where
\[
B_3(q,w,u)=
\left(
q+\mathbf 1_{(w,u)=(1,0)},
\;
w+1,
\;
u+\gamma_3(q,w)
\right),
\]
and
\[
\gamma_3(q,w)=1
\iff
\bigl(w=0 \text{ and } q\in\{0,4\}\bigr)
\;\lor\;
\bigl(w=2 \text{ and } q\neq 4\bigr)
\;\lor\;
\bigl(w=4 \text{ and } q=3\bigr).
\]

So:
- \(v\) is a clean cocycle coordinate,
- \(w\) is a strict clock,
- the section return
  \[
  U_3 = B_3^m\big|_{w=0}
  \]
  acts on \((q,u)\in (\mathbb Z_m)^2\).

A convenient row description is:

- row \(q=0\): \(u\mapsto u+2\), except \(u=m-1\) jumps to \((1,1)\),
- row \(q=1\): \(u\mapsto u+1\), except \(u=0\) jumps to \((2,1)\),
- row \(q=2\): \(u\mapsto u+1\), except \(u=0\) jumps to \((3,2)\),
- row \(q=3\): \(u\mapsto u+2\), except \(u=0\) jumps to \((4,0)\),
- row \(q=4\): \(u\mapsto u+1\), except \(u=m-1\) jumps to \((5\bmod m,1)\),
- rows \(q=5,\dots,m-1\): \(u\mapsto u+1\), except \(u=0\) jumps to \((q+1\bmod m,1)\).

For odd \(m\), the jumps stitch these rows into a single \(m^2\)-cycle because \(+2\) is a unit mod \(m\). The orbitwise monodromy on that unique \(U_3\)-orbit is
\[
M_3=\sum \beta_3 \equiv -1 \pmod m.
\]
Hence \(M_3\) is a unit.

**Theorem 4 (color 3).**  
For every odd \(m\ge 5\), the fixed 26-move witness makes color \(3\) Hamilton:
\[
R_3 \text{ is a single } m^4\text{-cycle on }P_0,
\qquad
f_3 \text{ is a Hamilton cycle on }(\mathbb Z_m)^5.
\]

**Proof.**  
Apply Theorem 3 to the clean frame above. \(U_3\) is a single cycle for odd \(m\), and the unique orbit has monodromy \(-1\), hence unit. Therefore \(R_3\) is a single cycle. Lemma 1 lifts this to \(f_3\). ∎

---

## 5. Failure profile for colors 0, 1, 4

The right question is not yet “what is the full formula?”, but rather:
1. does a clean frame exist?
2. if yes, what does \(U_c\) do?
3. if \(U_c\) is one cycle, is monodromy the only obstruction?

We tested the clean-frame condition from Lemma 2 exhaustively for
\[
m=5,7,9,11.
\]

### Diagnostic table

- **Color 0**
  - \(m=5\): no clean frame
  - \(m=7\): no clean frame
  - \(m=9\): no clean frame
  - \(m=11\): no clean frame

- **Color 1**
  - \(m=5\): no clean frame
  - \(m=7\): no clean frame
  - \(m=9\): no clean frame
  - \(m=11\): no clean frame

- **Color 4**
  - \(m=5\): no clean frame
  - \(m=7\): no clean frame
  - \(m=9\): no clean frame
  - \(m=11\): no clean frame

Therefore, for the current witness:

- \(U_0,U_1,U_4\) are **not defined** as clean section maps.
- Orbitwise monodromy is **not the right diagnostic yet** for colors \(0,1,4\).
- The obstruction appears **before** the monodromy stage: the map does not admit a triangular factorization at all.

Ancillary cycle data for the full first return \(R_c\):

- color 0:
  - \(m=7\): 5 cycles
  - \(m=9\): 5 cycles
  - \(m=11\): 5 cycles

- color 1:
  - \(m=7\): 433 cycles
  - \(m=9\): 2055 cycles
  - \(m=11\): 6003 cycles
  - moreover, independently, color 1 has an explicit large fixed set for every \(m\ge 6\)

- color 4:
  - \(m=7\): 3 cycles
  - \(m=9\): 7 cycles
  - \(m=11\): 5 cycles

So the current 26-move witness is **not** in the regime
“base \(U_c\) is good, monodromy needs repair”.
It is already failing one level earlier.

---

## 6. Branch decision

The decision tree is now:

- **monodromy only bad**  \(\Rightarrow\) local surgery
- **base \(U_c\) fractures**  \(\Rightarrow\) witness redesign
- **clean frame absent**  \(\Rightarrow\) new cyclic template

For colors \(0,1,4\), the fixed witness lands in the third case.

### Decision
1. **Freeze color 3 now** in theorem form via:
   - first-return reduction,
   - clean-frame lemma,
   - triangular skew-product criterion,
   - explicit color-3 instantiation.

2. **Do not spend the main effort repairing the 26-move witness** for colors \(0,1,4\).  
   The missing piece is not merely bad monodromy.

3. **Move to a new cyclic family / new template** whose low-layer rules are built so that every color has a clean frame by construction, ideally in the relative coordinates
   \[
   q_c=x_{c+1},\quad w_c=x_{c+2},\quad v_c=x_{c+3},\quad u_c=x_{c+4}.
   \]

That is the correct next branch.

---

## Status labels
- [P] first-return reduction
- [P] clean-frame detection lemma
- [P] triangular skew-product Hamiltonicity criterion
- [P] color-3 odd-\(m\) instantiation
- [C] no clean frame for colors 0/1/4 in the tested moduli \(m=5,7,9,11\)
- [P] color 1 fixed-set obstruction for \(m\ge 6\)
- [O] new cyclic family for colors 0/1/4
