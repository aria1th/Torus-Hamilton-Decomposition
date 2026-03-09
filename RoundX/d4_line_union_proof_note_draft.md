# d=4 line-union gauge proof draft

## Fixed witness

Let
\[
V=(\mathbb Z/m\mathbb Z)^4,\qquad D_4(m)=\operatorname{Cay}(V,\{e_0,e_1,e_2,e_3\}),\qquad m\ge 3.
\]

For a vertex \(x=(x_0,x_1,x_2,x_3)\), set
\[
S(x)=x_0+x_1+x_2+x_3,\qquad q(x)=x_0+x_2.
\]
Write
\[
P_0=\{x\in V:S(x)=0\}.
\]
Parameterize \(P_0\) by
\[
\phi(a,b,q)=(a,b,q-a,-q-b).
\]

We use the following line-union gauge rule.

- if \(S(x)=0\):
  - use \((3,2,1,0)\) when \(q(x)=0\),
  - use \((1,0,3,2)\) otherwise;
- if \(S(x)=1\): use \((0,1,2,3)\);
- if \(S(x)=2\) and \(q(x)=0\): start from \((0,1,2,3)\), then
  - swap slots \(1\leftrightarrow 3\) when \(x_0=0\),
  - swap slots \(0\leftrightarrow 2\) when \(x_3=0\);
- if \(S(x)\ge 3\): use \((0,1,2,3)\).

Equivalently, on
\[
H=\{S=2,\ q=0\}
\]
this witness is canonical except on
\[
\{x_0=0\}\cup\{x_3=0\},
\]
so the layer-2 defect is the union of two lines in \(H\).

For each color \(c\in\{0,1,2,3\}\), let \(f_c\) be the color-\(c\) map on \(V\).

## Goal

Show that, for this fixed witness, each \(f_c\) is a single Hamilton cycle on \(V\). Since every direction tuple used by the witness is a permutation of \((0,1,2,3)\), this gives a Hamilton decomposition of \(D_4(m)\).

---

## Lemma 1 (permutation property)
Every direction tuple used by the witness is a permutation of \((0,1,2,3)\).

### Proof
The witness only uses the six tuples
\[
(3,2,1,0),\ (1,0,3,2),\ (0,1,2,3),\ (0,3,2,1),\ (2,1,0,3),\ (2,3,0,1),
\]
and each is visibly a permutation. ∎

---

## Lemma 2 (first return to \(P_0\))
For every color \(c\), the first return map to \(P_0\) is
\[
R_c=f_c^m\big|_{P_0}.
\]

### Proof
Every step of any color map increases exactly one coordinate by \(1\), hence increases the layer \(S(x)\) by \(1\) modulo \(m\). Starting from \(P_0\), after exactly \(m\) steps one returns to layer \(0\), and before that one is on layers \(1,2,\dots,m-1\). ∎

---

## Lemma 3 (explicit first-return formulas)
Let \(x=\phi(a,b,q)\in P_0\). Then the line-union first-return maps are
\[
R_0(a,b,q)=
\begin{cases}
(a-1,b,q-1), & q=0,\\
(a-2,b+1,q-1), & q=m-1\text{ and }b=1,\\
(a-1,b+1,q-1), & \text{otherwise,}
\end{cases}
\]
\[
R_1(a,b,q)=
\begin{cases}
(a,b-1,q+1), & q=0,\\
(a+1,b-2,q+1), & q=m-1\text{ and }a=m-1,\\
(a+1,b-1,q+1), & \text{otherwise,}
\end{cases}
\]
\[
R_2(a,b,q)=
\begin{cases}
(a,b+1,q-1), & q=0,\\
(a+1,b,q-1), & q=m-1\text{ and }b=2,\\
(a,b,q-1), & \text{otherwise,}
\end{cases}
\]
\[
R_3(a,b,q)=
\begin{cases}
(a+1,b,q+1), & q=0,\\
(a,b+1,q+1), & q=m-1\text{ and }a=0,\\
(a,b,q+1), & \text{otherwise.}
\end{cases}
\]

### Proof
Start from
\[
x=\phi(a,b,q)=(a,b,q-a,-q-b).
\]
We analyze the first two steps and then observe that all later layers are canonical.

### Color 0
If \(q=0\), then layer 0 uses direction \(e_3\), and layer 1 uses the canonical direction \(e_0\). Thus after two steps we are at
\[
(a+1,b,-a,1-b),
\]
whose new \(q\)-value is \(1\), so the layer-2 patch does not fire. The remaining \(m-2\) steps are all along \(e_0\). Therefore the total displacement is
\[
e_3+(m-1)e_0\equiv e_3-e_0,
\]
which gives
\[
R_0(a,b,0)=(a-1,b,-1).
\]

Now assume \(q\neq 0\). Then layer 0 uses \(e_1\), and layer 1 uses \(e_0\), so after two steps we are at
\[
(a+1,b+1,q-a,-q-b).
\]
Its new \(q\)-value is \(q+1\), so the layer-2 patch can fire only when \(q=m-1\). In that case the layer-2 point is
\[
(a+1,b+1,m-1-a,1-b).
\]
Here the even gate condition is
\[
x_3=0\iff b=1.
\]
The odd gate does not affect color 0, whereas the even gate changes color 0 from \(e_0\) to \(e_2\). Hence color 0 is modified exactly when \(b=1\). Therefore:
- if \(q=m-1\) and \(b=1\), the total displacement is
  \[
  e_1+e_2+(m-2)e_0\equiv e_1+e_2-2e_0,
  \]
  giving
  \[
  R_0(a,b,q)=(a-2,b+1,q-1);
  \]
- otherwise, the total displacement is
  \[
  e_1+(m-1)e_0\equiv e_1-e_0,
  \]
  giving
  \[
  R_0(a,b,q)=(a-1,b+1,q-1).
  \]

### Color 1
If \(q=0\), then layer 0 uses \(e_2\), and layer 1 uses the canonical direction \(e_1\). After two steps we are at
\[
(a,b+1,1-a,-b),
\]
whose new \(q\)-value is \(1\), so no layer-2 patch fires. The total displacement is
\[
e_2+(m-1)e_1\equiv e_2-e_1,
\]
which gives
\[
R_1(a,b,0)=(a,b-1,1).
\]

Now assume \(q\neq 0\). Then layer 0 uses \(e_0\), and layer 1 uses \(e_1\), so after two steps we are again at
\[
(a+1,b+1,q-a,-q-b).
\]
Thus the layer-2 patch can only fire when \(q=m-1\), in which case the layer-2 point is
\[
(a+1,b+1,m-1-a,1-b).
\]
The odd gate condition is
\[
x_0=0\iff a=m-1.
\]
The even gate does not affect color 1, whereas the odd gate changes color 1 from \(e_1\) to \(e_3\). Hence color 1 is modified exactly when \(a=m-1\). Therefore:
- if \(q=m-1\) and \(a=m-1\), the total displacement is
  \[
  e_0+e_3+(m-2)e_1\equiv e_0+e_3-2e_1,
  \]
  giving
  \[
  R_1(a,b,q)=(a+1,b-2,q+1);
  \]
- otherwise, the total displacement is
  \[
  e_0+(m-1)e_1\equiv e_0-e_1,
  \]
  giving
  \[
  R_1(a,b,q)=(a+1,b-1,q+1).
  \]

### Color 2
If \(q=0\), then layer 0 uses \(e_1\), and layer 1 uses the canonical direction \(e_2\). After two steps we are at
\[
(a,b+1,1-a,-b),
\]
whose new \(q\)-value is \(1\), so no layer-2 patch fires. The total displacement is
\[
e_1+(m-1)e_2\equiv e_1-e_2,
\]
which gives
\[
R_2(a,b,0)=(a,b+1,-1).
\]

Now assume \(q\neq 0\). Then layer 0 uses \(e_3\), and layer 1 uses \(e_2\), so after two steps we are at
\[
(a,b,q-a+1,-q-b+1).
\]
Its new \(q\)-value is \(q+1\), so the layer-2 patch can fire only when \(q=m-1\). In that case the layer-2 point is
\[
(a,b,m-a,2-b).
\]
The even gate condition is
\[
x_3=0\iff b=2.
\]
The odd gate does not affect color 2, whereas the even gate changes color 2 from \(e_2\) to \(e_0\). Hence color 2 is modified exactly when \(b=2\). Therefore:
- if \(q=m-1\) and \(b=2\), the total displacement is
  \[
  e_3+e_0+(m-2)e_2\equiv e_3+e_0-2e_2,
  \]
  giving
  \[
  R_2(a,b,q)=(a+1,b,q-1);
  \]
- otherwise, the total displacement is
  \[
  e_3+(m-1)e_2\equiv e_3-e_2,
  \]
  giving
  \[
  R_2(a,b,q)=(a,b,q-1).
  \]

### Color 3
If \(q=0\), then layer 0 uses \(e_0\), and layer 1 uses the canonical direction \(e_3\). After two steps we are at
\[
(a+1,b,-a,1-b),
\]
whose new \(q\)-value is \(1\), so no layer-2 patch fires. The total displacement is
\[
e_0+(m-1)e_3\equiv e_0-e_3,
\]
which gives
\[
R_3(a,b,0)=(a+1,b,1).
\]

Now assume \(q\neq 0\). Then layer 0 uses \(e_2\), and layer 1 uses \(e_3\), so after two steps we are again at
\[
(a,b,q-a+1,-q-b+1).
\]
Thus the layer-2 patch can fire only when \(q=m-1\), in which case the layer-2 point is
\[
(a,b,m-a,2-b).
\]
The odd gate condition is
\[
x_0=0\iff a=0.
\]
The even gate does not affect color 3, whereas the odd gate changes color 3 from \(e_3\) to \(e_1\). Hence color 3 is modified exactly when \(a=0\). Therefore:
- if \(q=m-1\) and \(a=0\), the total displacement is
  \[
  e_2+e_1+(m-2)e_3\equiv e_2+e_1-2e_3,
  \]
  giving
  \[
  R_3(a,b,q)=(a,b+1,q+1);
  \]
- otherwise, the total displacement is
  \[
  e_2+(m-1)e_3\equiv e_2-e_3,
  \]
  giving
  \[
  R_3(a,b,q)=(a,b,q+1).
  \]

This proves all four formulas. ∎

---

## Lemma 4 (second return to \(Q\))
Let
\[
Q=\{(a,b,q)\in P_0:q=m-1\}.
\]
Define
\[
T_c=R_c^m\big|_Q.
\]
Then
\[
T_0(a,b)=(a-1_{b=1},b-1),
\]
\[
T_1(a,b)=(a-1,b-1_{a=m-1}),
\]
\[
T_2(a,b)=(a+1_{b=2},b+1),
\]
\[
T_3(a,b)=(a+1,b+1_{a=0}).
\]

### Proof
For colors 0 and 2, the q-coordinate decreases by 1 under every application of \(R_c\). Thus starting from \(Q\), one sees exactly one \(q=m-1\) branch, then \(m-2\) ordinary branches, and finally one \(q=0\) branch.

For \(T_0\), the increment in \((a,b)\) is
- \((-2,+1)\) when \(q=m-1\) and \(b=1\),
- \((-1,+1)\) on all other nonzero \(q\)-levels,
- \((-1,0)\) when \(q=0\).
Therefore
- if \(b=1\), the total change is
  \[
  (-2,+1)+(m-2)(-1,+1)+(-1,0)=(-(m+1),m-1)\equiv(-1,-1),
  \]
- if \(b\neq 1\), the total change is
  \[
  (-1,+1)+(m-2)(-1,+1)+(-1,0)=(-m,m-1)\equiv(0,-1).
  \]
This gives
\[
T_0(a,b)=(a-1_{b=1},b-1).
\]

For \(T_2\), the increment in \((a,b)\) is
- \((+1,0)\) when \(q=m-1\) and \(b=2\),
- \((0,0)\) on all other nonzero \(q\)-levels,
- \((0,+1)\) when \(q=0\).
Hence
- if \(b=2\), the total change is \((+1,+1)\),
- otherwise, the total change is \((0,+1)\).
Thus
\[
T_2(a,b)=(a+1_{b=2},b+1).
\]

For colors 1 and 3, the q-coordinate increases by 1 under every application of \(R_c\). Thus starting from \(Q\), one sees the \(q=m-1\) branch first, then the \(q=0\) branch, and then \(m-2\) ordinary branches.

For \(T_1\), the increment in \((a,b)\) is
- \((+1,-2)\) when \(q=m-1\) and \(a=m-1\),
- \((+1,-1)\) on all other nonzero \(q\)-levels,
- \((0,-1)\) when \(q=0\).
Therefore
- if \(a=m-1\), the total change is
  \[
  (+1,-2)+(0,-1)+(m-2)(+1,-1)=(m-1,-m-1)\equiv(-1,-1),
  \]
- otherwise, the total change is
  \[
  (+1,-1)+(0,-1)+(m-2)(+1,-1)=(m-1,-m)\equiv(-1,0).
  \]
Hence
\[
T_1(a,b)=(a-1,b-1_{a=m-1}).
\]

For \(T_3\), the increment in \((a,b)\) is
- \((0,+1)\) when \(q=m-1\) and \(a=0\),
- \((0,0)\) on all other nonzero \(q\)-levels,
- \((+1,0)\) when \(q=0\).
Thus
- if \(a=0\), the total change is \((+1,+1)\),
- otherwise, the total change is \((+1,0)\).
Therefore
\[
T_3(a,b)=(a+1,b+1_{a=0}).
\]
This proves the stated formulas. ∎

---

## Lemma 5 (odometer conjugacies)
Let
\[
O(u,v)=(u+1,v+1_{u=0})
\]
on \((\mathbb Z/m\mathbb Z)^2\). Then each \(T_c\) is affinely conjugate to \(O\):
\[
\psi_0(a,b)=(1-b,-a),
\]
\[
\psi_1(a,b)=(-a-1,-b),
\]
\[
\psi_2(a,b)=(b-2,a),
\]
\[
\psi_3(a,b)=(a,b),
\]
and
\[
\psi_c\circ T_c = O\circ \psi_c
\qquad (c=0,1,2,3).
\]

### Proof
Direct substitution. For example,
\[
\psi_3(T_3(a,b))=(a+1,b+1_{a=0})=O(a,b)=O(\psi_3(a,b)).
\]
Similarly,
\[
\psi_0(T_0(a,b))=(2-b,-a+1_{b=1})=O(1-b,-a),
\]
\[
\psi_1(T_1(a,b))=(-a,-b+1_{a=m-1})=O(-a-1,-b),
\]
\[
\psi_2(T_2(a,b))=(b-1,a+1_{b=2})=O(b-2,a).
\]
Thus each \(T_c\) is conjugate to \(O\). ∎

---

## Lemma 6 (the odometer is one cycle)
The map \(O(u,v)=(u+1,v+1_{u=0})\) is a single cycle of length \(m^2\) on \((\mathbb Z/m\mathbb Z)^2\).

### Proof
In one step, \(u\) always increases by 1. Hence in exactly \(m\) steps, \(u\) returns to its starting value. During those \(m\) steps, the value \(u=0\) occurs exactly once, so
\[
O^m(u,v)=(u,v+1).
\]
Therefore
\[
O^{m^2}(u,v)=(u,v).
\]
Conversely, if \(O^t(u,v)=(u,v)\), write \(t=qm+r\) with \(0\le r<m\). Since the first coordinate changes by \(r\) modulo \(m\), we must have \(r=0\). Then \(t=qm\), and applying the identity \(O^m(u,v)=(u,v+1)\) repeatedly gives
\[
O^t(u,v)=(u,v+q),
\]
so \(q\equiv 0\pmod m\). Hence \(t\) is a multiple of \(m^2\). Thus every orbit has length exactly \(m^2\), and since the state space has size \(m^2\), there is only one orbit. ∎

---

## Lemma 7 (lifting from \(Q\) to \(P_0\))
If \(T_c\) is a single \(m^2\)-cycle on \(Q\), then \(R_c\) is a single \(m^3\)-cycle on \(P_0\).

### Proof
Under every \(R_c\), the q-coordinate changes by \(+1\) or \(-1\), depending only on the color. Therefore each \(R_c\)-orbit in \(P_0\) meets \(Q\) exactly once every \(m\) steps. Equivalently, every point of \(P_0\) can be written uniquely as
\[
R_c^j(x),\qquad x\in Q,
\quad 0\le j<m.
\]
If \(T_c\) is one cycle on \(Q\), choose \(x_0\in Q\). Then the full \(R_c\)-orbit of \(x_0\) contains all points
\[
R_c^j(T_c^t(x_0)),
\qquad 0\le j<m,
\quad 0\le t<m^2,
\]
which are pairwise distinct because their q-values determine \(j\) uniquely modulo \(m\). Hence the \(R_c\)-orbit has size \(m\cdot m^2=m^3\), which is exactly \(|P_0|\). ∎

---

## Lemma 8 (lifting from \(P_0\) to the whole torus)
If \(R_c\) is a single \(m^3\)-cycle on \(P_0\), then \(f_c\) is a single \(m^4\)-cycle on \(V\).

### Proof
Exactly as in Lemma 2, each application of \(f_c\) increases the layer \(S\) by 1, so every \(f_c\)-orbit meets \(P_0\) exactly once every \(m\) steps. Therefore each point of \(V\) is uniquely of the form
\[
f_c^j(x),\qquad x\in P_0,
\quad 0\le j<m.
\]
If \(R_c\) is a single cycle on \(P_0\), then the \(f_c\)-orbit of one point in \(P_0\) contains all such points, hence all \(m\cdot m^3=m^4\) vertices of \(V\). ∎

---

## Theorem (line-union gauge is Hamiltonian for all \(m\ge 3\))
For every \(m\ge 3\), the fixed line-union gauge witness gives a Hamilton decomposition of \(D_4(m)\).

### Proof
By Lemma 1, each vertex assigns a permutation of the four outgoing directions, so the four color classes partition the outgoing arcs.

Fix a color \(c\). By Lemma 5, \(T_c\) is conjugate to the odometer \(O\). By Lemma 6, \(O\) is a single cycle on \((\mathbb Z/m\mathbb Z)^2\), so \(T_c\) is a single cycle on \(Q\). By Lemma 7, \(R_c\) is therefore a single cycle on \(P_0\). By Lemma 8, \(f_c\) is a single Hamilton cycle on \(V\).

Since this holds for every color \(c=0,1,2,3\), the witness yields four arc-disjoint Hamilton cycles covering all outgoing arcs. Hence it is a Hamilton decomposition of \(D_4(m)\). ∎

---

## Conceptual takeaway
The layer-2 mechanism is better viewed as an affine gate law on
\[
H=\{S=2,q=0\}
\]
than as a raw row-table. In the reduced 2-bit family, the computational evidence says that the Hamiltonian truth tables are exactly the affine family
\[
s(u,v)=g+(u,v),\qquad g\in (\mathbb Z/2\mathbb Z)^2,
\]
and the line-union gauge is the unique representative in that orbit with minimal layer-2 support.
