
# Promoted-collar breaker: complete local audit and finite active-burst theorem (2026-03-25)

## Setting

Let
\[
\widehat{\mathfrak N}_m(1)
=
\{A_{1,4},\,C_{r,4},\,A_{1,3},\,C_{3,3},\,C_{r-1,3},\,A_{r,3},\,C_{r+1,3}\},
\qquad r=(m-1)/2,
\]
be the canonical width-3 pure color-1 frontier, with odd resonant modulus \(m\ge 15\).
Fix one collar side
\[
u\in\{r-1,r+1\},
\]
and define the promoted-collar package
\[
\widehat{\mathfrak N}_m^{(u)}
:=
\widehat{\mathfrak N}_m(1)\cup\{A_{u,3}\}.
\]

Write
\[
R^{(u)}_{1,m}=h_1^m\big|_{\Sigma=0}
\]
for the color-1 section return of \(\widehat{\mathfrak N}_m^{(u)}\), and
\[
R^{\mathrm{wd1}}_{1,m},\qquad R^{\mathrm{wd3}}_{1,m}
\]
for the exact width-1 and canonical width-3 section returns already derived earlier.

On \(\Sigma=0\), write
\[
(a,b,c,d,e)=(x_0,x_1,x_2,x_3,x_4),
\qquad
b\equiv -a-c-d-e\pmod m.
\]
Recall the indicator
\[
\beta=\mathbf 1[c=m-2],
\qquad
\chi=\mathbf 1[d+\beta\equiv m-1].
\]
The earlier exact theorem proved
\[
R^{(u)}_{1,m}=R^{\mathrm{wd3}}_{1,m}+\chi(e_2-e_0),
\qquad
R^{\mathrm{wd3}}_{1,m}=R^{\mathrm{wd1}}_{1,m}+2\chi(e_0-e_1).
\]

The present note isolates the **entire** \(\chi\)-support and proves that every maximal \(\chi\)-active episode is finite. This closes the local section-level audit: no hidden persistent collar locus remains.

---

## 1. Exact support of the promoted correction

Since
\[
\chi=\mathbf 1[d+\mathbf 1[c=m-2]\equiv m-1],
\]
one has immediately
\[
\chi=1
\iff
\bigl(d=m-1,\ c\neq m-2\bigr)
\ \text{or}\
\bigl(d=c=m-2\bigr).
\]

So the promoted-collar correction is supported **exactly** on the disjoint union
\[
\mathcal A_m
=
\underbrace{\{d=m-1,\ c\neq m-2\}}_{\text{top / double-top interiors}}
\;\sqcup\;
\underbrace{\{d=c=m-2\}}_{\text{hinge line}}.
\]

Outside \(\mathcal A_m\), one has
\[
R^{(u)}_{1,m}=R^{\mathrm{wd3}}_{1,m}=R^{\mathrm{wd1}}_{1,m}.
\]

So there are only three genuinely new local regimes to analyze:

1. top-collar interior \(d=m-1,\ e\neq m-1,\ c\neq m-2\);
2. double-top interior \(d=e=m-1,\ c\neq m-2\);
3. hinge line \(d=c=m-2\).

The first two were already solved by exact transducer theorems. The only missing local regime is the hinge line.

---

## 2. Exact hinge-line formulas

### Proposition 2.1 (top hinge, \(e\neq m-1\))

Assume
\[
c=d=m-2,\qquad e\neq m-1.
\]
Then
\[
R^{(u)}_{1,m}(a,b,m-2,m-2,e)
=
\begin{cases}
(5,\ *,\ 1,\ m-1,\ e), & a=2,\\[1mm]
(a+2,\ *,\ 2,\ m-1,\ e), & a\neq 2,
\end{cases}
\]
where \(*\) is determined by \(\Sigma=0\).

In particular, every top-hinge state enters the top-collar interior after one block, and the entering \(c\)-value is either \(1\) or \(2\).

#### Proof

On this locus
\[
\beta=1,\qquad \chi=1,\qquad d\neq m-1,\qquad e\neq m-1,
\]
so
\[
\varepsilon=0,\qquad \alpha=1,\qquad \gamma=0,\qquad \delta=0.
\]
Also
\[
\phi=\mathbf 1[-a-(m-2)-(m-2)+1-1\equiv 2]
=\mathbf 1[a\equiv 2].
\]
Hence the promoted exact block map gives
\[
\Delta_0=\alpha+\phi\chi+\chi = 2+\phi,
\qquad
\Delta_2=1+\chi(3-\phi)=4-\phi,
\qquad
\Delta_3=\beta=1,
\qquad
\Delta_4=0.
\]
Therefore
\[
a'=
\begin{cases}
a+3=5,& a=2,\\
a+2,& a\neq 2,
\end{cases}
\qquad
c'=
\begin{cases}
m-2+3=1,& a=2,\\
m-2+4=2,& a\neq 2,
\end{cases}
\]
and \(d'=m-1,\ e'=e\). ∎

### Proposition 2.2 (double hinge, \(e=m-1\))

Assume
\[
c=d=m-2,\qquad e=m-1.
\]
Then
\[
R^{(u)}_{1,m}(a,b,m-2,m-2,m-1)
=
\begin{cases}
(5,\ *,\ 1,\ m-1,\ m-1), & a=3,\\[1mm]
(a+1,\ *,\ 2,\ m-1,\ m-1), & a\neq 3,
\end{cases}
\]
where \(*\) is determined by \(\Sigma=0\).

In particular, every double-hinge state enters the double-top interior after one block, and the entering \(c\)-value is again either \(1\) or \(2\).

#### Proof

Now
\[
\beta=1,\qquad \chi=1,\qquad e=m-1,
\]
so
\[
\varepsilon=1,\qquad \alpha=0,\qquad \gamma=0,\qquad \delta=0.
\]
Also
\[
\phi=\mathbf 1[-a-(m-2)-(m-2)+1+1-1\equiv 2]
=\mathbf 1[a\equiv 3].
\]
Therefore
\[
\Delta_0=\alpha+\phi\chi+\chi = 1+\phi,
\qquad
\Delta_2=4-\phi,
\qquad
\Delta_3=1,
\qquad
\Delta_4=0.
\]
Hence
\[
a'=
\begin{cases}
a+2=5,& a=3,\\
a+1,& a\neq 3,
\end{cases}
\qquad
c'=
\begin{cases}
1,& a=3,\\
2,& a\neq 3,
\end{cases}
\qquad
d'=e'=m-1.
\]
So the image lies in the double-top interior. ∎

---

## 3. Top and double interiors are already forced to exit

The previous transducer theorems already showed:

### Theorem 3.1 (top-collar forcing)
On the top-collar interior
\[
d=m-1,\qquad e\neq m-1,\qquad c\neq m-2,
\]
the promoted-collar section return is
\[
w'=w+5,\qquad c'=c+4-\mathbf 1[w=1],
\qquad w:=a+c.
\]
Hence every uninterrupted top-collar episode is finite.

### Theorem 3.2 (double-top forcing)
On the double-top interior
\[
d=e=m-1,\qquad c\neq m-2,
\]
the promoted-collar section return is
\[
w'=w+6,\qquad c'=c+4-\mathbf 1[w=0],
\qquad w:=a+c.
\]
Hence every uninterrupted double-top episode is finite.

---

## 4. Consequence: finite active-burst theorem

Combine Propositions 2.1–2.2 with Theorems 3.1–3.2.

### Theorem 4.1 (finite \(\chi\)-active episodes)

For every odd resonant modulus \(m\ge 15\), every maximal orbit segment of
\(R^{(u)}_{1,m}\) contained in the active locus
\[
\mathcal A_m=\{d=m-1,\ c\neq m-2\}\sqcup\{d=c=m-2\}
\]
is finite.

More precisely:

- if the segment starts on the hinge line \(d=c=m-2\), then after one block it enters either the top-collar interior or the double-top interior, with \(c\in\{1,2\}\);
- once in the top-collar interior, it exits after finitely many further blocks;
- once in the double-top interior, it exits after finitely many further blocks.

So no orbit can remain forever inside the support of the promoted-collar correction.

#### Proof

Immediate from Propositions 2.1–2.2 and Theorems 3.1–3.2. ∎

---

## 5. What this upgrades, and what it still does not prove

This completes the local section-return audit for the promoted-collar breaker:

- there is **no omitted \(\chi\)-active locus** beyond the already analyzed top and double interiors plus the newly analyzed hinge line;
- the hinge line is only an entrance line, not a new persistent resonance;
- every local collar burst is finite.

So the promoted-collar package is now best understood as
\[
\boxed{
\text{solved width-1 bulk} \;+\; \text{finite promoted-collar bursts}.
}
\]

What remains open is **global**, not local:

1. prove that the induced lower return is a single cycle after these finite bursts are inserted into the bulk dynamics;
2. prove compatibility with the donor color (color 2) in a final residual-assembly package;
3. finish the separate \(B\)-active / gate branch.

Thus the present theorem does **not** yet close the resonant residual theorem, but it does remove one possible source of hidden local omissions.
