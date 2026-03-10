# d=4 generic theorem proof via the line-union gauge

## Theorem
For every integer \(m\ge 3\), the directed torus
\[
D_4(m)=\operatorname{Cay}\bigl((\mathbb Z/m\mathbb Z)^4,\{e_0,e_1,e_2,e_3\}\bigr)
\]
admits a Hamilton decomposition.

More concretely, if we define the direction tuple \(\delta(x)=(d_0(x),d_1(x),d_2(x),d_3(x))\) by the line-union rule below and set
\[
f_c(x)=x+e_{d_c(x)}\qquad(c=0,1,2,3),
\]
then each color map \(f_c\) is a single cycle of length \(m^4\).

## Witness
Let
\[
S(x)=x_0+x_1+x_2+x_3,\qquad q(x)=x_0+x_2
\]
(modulo \(m\)). Throughout, we identify residues with their standard representatives in \(\{0,1,\dots,m-1\}\), so phrases such as \(S(x)\ge 3\) and \(q(x)=m-1\) are understood in that sense. The witness is:

- if \(S(x)=0\):
  - use \((3,2,1,0)\) when \(q(x)=0\),
  - use \((1,0,3,2)\) when \(q(x)\ne 0\);
- if \(S(x)=1\): use the canonical tuple \((0,1,2,3)\);
- if \(S(x)=2\) and \(q(x)=0\): start from \((0,1,2,3)\), then
  - swap slots \(1\leftrightarrow 3\) when \(x_0=0\),
  - swap slots \(0\leftrightarrow 2\) when \(x_3=0\).
  If both conditions hold, apply both swaps; they commute because they are disjoint.
- otherwise: use the canonical tuple \((0,1,2,3)\).

Thus on
\[
H=\{S=2,\ q=0\}
\]
the defect support is exactly
\[
\{x_0=0\}\cup\{x_3=0\},
\]
a union of two lines.

The only tuples ever used are
\[
(3,2,1,0),\ (1,0,3,2),\ (0,1,2,3),\ (0,3,2,1),\ (2,1,0,3),\ (2,3,0,1),
\]
all permutations of \((0,1,2,3)\). Therefore the four color classes partition the outgoing arcs of the digraph.

---

## 1. First return to the layer section
Let
\[
P_0=\{x\in (\mathbb Z/m\mathbb Z)^4:S(x)=0\}.
\]
Parameterize \(P_0\) by
\[
\phi(a,b,q)=(a,b,q-a,-q-b).
\]
Then \(q=x_0+x_2\) in these coordinates.

Every color step increases \(S\) by \(1\). Hence the first return of \(f_c\) to \(P_0\) is
\[
R_c=f_c^m\big|_{P_0}.
\]

### Proposition 1 (explicit first-return formulas)
For \(x=\phi(a,b,q)\in P_0\),
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
Fix \(x=\phi(a,b,q)=(a,b,q-a,-q-b)\).

If \(q=0\), the layer-0 tuple is \((3,2,1,0)\). After one step we are in layer \(1\), and the layer-1 tuple is canonical. After the second step we are in layer \(2\), but the new \(q\)-value is \(1\), so the layer-2 patch does not fire. Thus the remaining \(m-2\) steps are canonical. This immediately gives the four \(q=0\) branches:
\[
e_3+(m-1)e_0\equiv e_3-e_0,
\qquad
e_2+(m-1)e_1\equiv e_2-e_1,
\qquad
e_1+(m-1)e_2\equiv e_1-e_2,
\qquad
e_0+(m-1)e_3\equiv e_0-e_3.
\]

Now assume \(q\ne 0\). Then the layer-0 tuple is \((1,0,3,2)\).

- For colors \(0,1\), after two steps the layer-2 landing point is
  \[
  y^+(a,b,q)=(a+1,b+1,q-a,-q-b),
  \]
  so its new \(q\)-value is \(q+1\). Therefore the layer-2 splice can fire only when \(q=m-1\), in which case
  \[
  y^+(a,b,m-1)=(a+1,b+1,m-1-a,1-b).
  \]
  Here the even gate condition is \(y^+_3=0\iff 1-b=0\iff b=1\), and the odd gate condition is \(y^+_0=0\iff a+1=0\iff a=m-1\).
  The even gate affects color \(0\) by changing \(e_0\) to \(e_2\), while the odd gate affects color \(1\) by changing \(e_1\) to \(e_3\).
  This yields exactly the displayed exceptional branches for \(R_0\) and \(R_1\).

- For colors \(2,3\), after two steps the layer-2 landing point is
  \[
  y^-(a,b,q)=(a,b,q-a+1,-q-b+1),
  \]
  whose new \(q\)-value is again \(q+1\). Hence only \(q=m-1\) can trigger the layer-2 splice, and then
  \[
  y^-(a,b,m-1)=(a,b,m-a,2-b).
  \]
  Here the even gate condition is \(y^-_3=0\iff 2-b=0\iff b=2\), and the odd gate condition is \(y^-_0=0\iff a=0\).
  The even gate affects color \(2\) by changing \(e_2\) to \(e_0\), while the odd gate affects color \(3\) by changing \(e_3\) to \(e_1\).
  This yields exactly the displayed exceptional branches for \(R_2\) and \(R_3\).

All four formulas follow. ∎

---

## 2. Second return to the \(q=m-1\) slice
Let
\[
Q=\{(a,b,q)\in P_0:q=m-1\}.
\]
Since each application of \(R_c\) changes \(q\) by \(+1\) or \(-1\), every \(R_c\)-orbit meets \(Q\) once every \(m\) iterates. Define the second return
\[
T_c=R_c^m\big|_Q.
\]

### Proposition 2 (explicit second-return formulas)
On \(Q\cong (\mathbb Z/m\mathbb Z)^2\),
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
For colors \(0\) and \(2\), the \(q\)-coordinate decreases by \(1\) under each application of \(R_c\). Thus starting from \(Q\), one sees:
- the \(q=m-1\) branch once,
- then \(m-2\) ordinary nonzero branches,
- then the \(q=0\) branch once.

For color \(0\), the \((a,b)\)-increments are
\[
(-2,+1)\text{ if }b=1,\qquad (-1,+1)\text{ otherwise on }q=m-1,
\]
\[
(-1,+1)\text{ on the }m-2\text{ middle steps},
\qquad
(-1,0)\text{ on the final }q=0\text{ step}.
\]
Therefore
\[
(-2,+1)+(m-2)(-1,+1)+(-1,0)=(-(m+1),m-1)\equiv(-1,-1)
\]
when \(b=1\), and
\[
(-1,+1)+(m-2)(-1,+1)+(-1,0)=(-m,m-1)\equiv(0,-1)
\]
when \(b\ne 1\). Hence
\[
T_0(a,b)=(a-1_{b=1},b-1).
\]

For color \(2\), the increments are
\[
(+1,0)\text{ if }b=2,\qquad (0,0)\text{ otherwise on }q=m-1,
\]
\[
(0,0)\text{ on the middle steps},
\qquad
(0,+1)\text{ on the final }q=0\text{ step}.
\]
So
\[
T_2(a,b)=(a+1_{b=2},b+1).
\]

For colors \(1\) and \(3\), the \(q\)-coordinate increases by \(1\) under each application of \(R_c\). Thus starting from \(Q\), one sees:
- the \(q=m-1\) branch once,
- then the \(q=0\) branch once,
- then \(m-2\) ordinary branches.

For color \(1\), the increments are
\[
(+1,-2)\text{ if }a=m-1,\qquad (+1,-1)\text{ otherwise on }q=m-1,
\]
\[
(0,-1)\text{ on the }q=0\text{ step},
\qquad
(+1,-1)\text{ on each middle step}.
\]
Thus
\[
(+1,-2)+(0,-1)+(m-2)(+1,-1)=(m-1,-m-1)\equiv(-1,-1)
\]
when \(a=m-1\), and
\[
(+1,-1)+(0,-1)+(m-2)(+1,-1)=(m-1,-m)\equiv(-1,0)
\]
otherwise. Hence
\[
T_1(a,b)=(a-1,b-1_{a=m-1}).
\]

For color \(3\), the increments are
\[
(0,+1)\text{ if }a=0,\qquad (0,0)\text{ otherwise on }q=m-1,
\]
\[
(+1,0)\text{ on the }q=0\text{ step},
\qquad
(0,0)\text{ on the middle steps}.
\]
Therefore
\[
T_3(a,b)=(a+1,b+1_{a=0}).
\]
∎

---

## 3. Odometer conjugacy
Let
\[
O(u,v)=(u+1,v+1_{u=0})
\]
on \((\mathbb Z/m\mathbb Z)^2\).

### Proposition 3
Each \(T_c\) is affinely conjugate to \(O\). One may take
\[
\psi_0(a,b)=(1-b,-a),
\qquad
\psi_1(a,b)=(-a-1,-b),
\qquad
\psi_2(a,b)=(b-2,a),
\qquad
\psi_3(a,b)=(a,b).
\]
Then
\[
\psi_c\circ T_c = O\circ \psi_c
\qquad(c=0,1,2,3).
\]

### Proof
This is direct substitution.

For example,
\[
\psi_3(T_3(a,b))=(a+1,b+1_{a=0})=O(a,b)=O(\psi_3(a,b)).
\]
Likewise,
\[
\psi_0(T_0(a,b))=(2-b,-a+1_{b=1})=O(1-b,-a),
\]
because \(u=1-b\) satisfies \(u=0\iff b=1\).
Similarly,
\[
\psi_1(T_1(a,b))=(-a,-b+1_{a=m-1})=O(-a-1,-b),
\]
because \(u=-a-1\) satisfies \(u=0\iff a=m-1\), and
\[
\psi_2(T_2(a,b))=(b-1,a+1_{b=2})=O(b-2,a).
\]
Thus every \(T_c\) is conjugate to \(O\). ∎

### Proposition 4
The odometer \(O\) is a single cycle of length \(m^2\).

### Proof
In one step, \(u\) always increases by \(1\), so in exactly \(m\) steps it returns to its starting value. During those \(m\) steps the value \(u=0\) occurs exactly once, hence
\[
O^m(u,v)=(u,v+1).
\]
Therefore \(O^{m^2}=\mathrm{id}\).

Conversely, if \(O^t(u,v)=(u,v)\), write \(t=km+r\) with \(0\le r<m\). The first coordinate changes by \(r\), so necessarily \(r=0\). Thus \(t=km\), and applying \(O^m(u,v)=(u,v+1)\) repeatedly gives
\[
O^t(u,v)=(u,v+k).
\]
Hence \(k\equiv 0\pmod m\), so \(t\) is a multiple of \(m^2\). Thus every orbit has exact length \(m^2\), and since the state space has size \(m^2\), there is only one orbit. ∎

---

## 4. Lifting back to \(P_0\) and to the full torus

### Proposition 5 (from \(Q\) to \(P_0\))
If \(T_c\) is a single \(m^2\)-cycle on \(Q\), then \(R_c\) is a single \(m^3\)-cycle on \(P_0\).

### Proof
Choose \(x_0\in Q\). Let \(s_c\in\{+1,-1\}\) be the sign by which \(R_c\) changes \(q\); this sign depends only on the color. Along the forward orbit
\[
x_t:=R_c^t(x_0),
\]
one has
\[
q(x_t)=m-1+s_c t \pmod m.
\]
Hence \(x_t\in Q\) if and only if \(t\equiv 0\pmod m\). In particular,
\[
R_c^{m^3}(x_0)=T_c^{m^2}(x_0)=x_0,
\]
because \(T_c\) has period \(m^2\).

Conversely, suppose \(R_c^t(x_0)=x_0\). Write
\[
t=km+r,\qquad 0\le r<m.
\]
Since returning to \(Q\) forces \(t\equiv 0\pmod m\), we must have \(r=0\). Thus \(t=km\), and then
\[
R_c^{t}(x_0)=R_c^{km}(x_0)=T_c^k(x_0)=x_0.
\]
Because \(T_c\) is a single \(m^2\)-cycle on \(Q\), its period at \(x_0\) is exactly \(m^2\), so \(k\) is a multiple of \(m^2\). Therefore \(t\) is a multiple of \(m^3\).

We have shown that the orbit of \(x_0\) under \(R_c\) has exact length \(m^3\). Since \(|P_0|=m^3\), this orbit is all of \(P_0\). Hence \(R_c\) is a single cycle on \(P_0\). ∎

### Proposition 6 (from \(P_0\) to the full torus)
If \(R_c\) is a single \(m^3\)-cycle on \(P_0\), then \(f_c\) is a single \(m^4\)-cycle on \((\mathbb Z/m\mathbb Z)^4\).

### Proof
Choose \(x_0\in P_0\). Along the forward orbit
\[
y_t:=f_c^t(x_0),
\]
one has
\[
S(y_t)=t \pmod m,
\]
because each application of \(f_c\) increases \(S\) by \(1\). Hence \(y_t\in P_0\) if and only if \(t\equiv 0\pmod m\). In particular,
\[
f_c^{m^4}(x_0)=R_c^{m^3}(x_0)=x_0,
\]
because \(R_c\) has period \(m^3\) on \(P_0\).

Conversely, suppose \(f_c^t(x_0)=x_0\). Write
\[
t=km+r,\qquad 0\le r<m.
\]
Since returning to \(P_0\) forces \(t\equiv 0\pmod m\), we must have \(r=0\). Thus \(t=km\), and then
\[
f_c^t(x_0)=f_c^{km}(x_0)=R_c^k(x_0)=x_0.
\]
Because \(R_c\) is a single \(m^3\)-cycle on \(P_0\), its period at \(x_0\) is exactly \(m^3\), so \(k\) is a multiple of \(m^3\). Therefore \(t\) is a multiple of \(m^4\).

We have shown that the orbit of \(x_0\) under \(f_c\) has exact length \(m^4\). Since the full torus has size \(m^4\), this orbit is all vertices. Hence \(f_c\) is a single cycle on \((\mathbb Z/m\mathbb Z)^4\). ∎

---

## Conclusion
For each color \(c\):

1. Proposition 3 shows that \(T_c\) is conjugate to the standard odometer \(O\).
2. Proposition 4 shows that \(O\) is a single \(m^2\)-cycle.
3. Proposition 5 lifts this to a single \(m^3\)-cycle for \(R_c\) on \(P_0\).
4. Proposition 6 lifts this again to a single \(m^4\)-cycle for \(f_c\) on the whole torus.

Therefore every color map \(f_c\) is a Hamilton cycle. Since the direction tuple at each vertex is always a permutation of \((0,1,2,3)\), the four color classes are arc-disjoint and cover all outgoing arcs. Hence the witness gives a Hamilton decomposition of \(D_4(m)\) for every \(m\ge 3\).

---

## Remark
This proof is completely all-\(m\) once the line-union witness is fixed. The Codex gauge classification is useful for choosing a clean witness, but not needed for the Hamiltonicity proof itself.
