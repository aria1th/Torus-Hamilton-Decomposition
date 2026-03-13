# D5 Positive Theorem Chain 054

This note rewrites the current D5 branch as a **positive theorem chain first**.
The negative/lower-bound direction is kept, but moved after the main chain so the
manuscript story stays centered on the minimal theorem-side object
\((B,\tau,\epsilon_4)\).

The active branch is always the checked best-seed branch for
\(R1 \to H_{L1}\).

## 0. The theorem-side object

Let
\[
B=(s,u,v,\lambda,f),
\]
where

- \(s,u,v\) are the grouped coordinates,
- \(\lambda\) is the layer,
- \(f\in\{\mathrm{regular},\mathrm{exceptional}\}\) is the family tag.

Let
\[
c=\mathbf 1_{\{q=m-1\}},
\qquad
d=\mathbf 1_{\{U^+\ge m-3\}},
\]
where \(U^+\) denotes the next-carry \(u\)-value on the checked active branch.

Let \(dn(x)\) be the grouped-delta event at the current state, with flat symbol
\[
\mathrm{flat}=(0,0,0,1),
\]
and let \(\epsilon_4(x)\) be the 4-class grouped-delta event label
(flat / wrap / carry\_jump / other).

Define \(\tau(x)\) to be the initial flat-prefix length of the future grouped-delta
sequence:
\[
\tau(x)=\max\{t\ge 0 : dn(F^j x)=\mathrm{flat}\text{ for }0\le j<t\}.
\]

This is the minimal theorem-side hidden datum.

## 1. The positive theorem chain

### Theorem A (checked finite-cover normal form; 044)
On the checked active branch for \(m=5,7,9,11\), the dynamics factor through the
finite-sheet normal form
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with the following properties.

1. The carry sheet \(c=\mathbf 1_{\{q=m-1\}}\) is the exact trigger lift.
2. The residual binary sheet can be chosen as
   \[
   d=\mathbf 1_{\{U^+\ge m-3\}}.
   \]
3. Carry states are singleton over \(B+c\).
4. The residual ambiguity is supported only on regular noncarry states.
5. The active transition law closes deterministically on \(B+c+d\).

**Status.** Checked on \(m=5,7,9,11\) from `044`.

---

### Theorem B (carry as anticipation datum; 046 + 052 support)
On the checked active branch, the carry sheet \(c\) is not a current grouped-state
observable, but it is an exact one-sided future grouped-transition datum.

More precisely, let \(\eta\) be the first nonflat grouped-delta event following the
initial flat run. Then on the checked range
\[
(B,\tau,\eta)
\]
exactly determines \(c\).

Equivalently, the first exact future horizons satisfy
\[
H_{dn}=m-3,
\qquad
H_B=m-2,
\]
where \(H_{dn}\) is the minimal exact future grouped-delta horizon and \(H_B\) is
the minimal exact future grouped-state horizon.

**Status.** Checked on \(m=5,7,9,11\) in `046`; the same horizon pattern is
checked through \(m=19\) in `052`.

---

### Theorem C (boundary sharpening; 047 + 052 support)
On the checked active branch, all ambiguity in \((B,\tau)\) is concentrated at the
boundary \(\tau=0\).

More precisely:

1. Away from the boundary, \((B,\tau)\) already determines \(c\).
2. At the boundary \(\tau=0\), the residual event class is genuinely 3-way:
   \[
   \{\mathrm{wrap},\ \mathrm{carry\_jump},\ \mathrm{other}\}.
   \]
3. The quotient
   \[
   (B,\tau,\epsilon_4)
   \]
   is exact for \(c\) on the checked range.

A stronger checked-range truncation pattern also holds:
\[
(B,\min(\tau,m-3),\epsilon_4)
\]
is exact on the tested moduli, but this should be treated as **checked-range
evidence**, not yet as the final canonical form.

**Status.** Checked on \(m=5,7,9,11\) in `047`; the same pattern is checked
through \(m=19\) in `052`.

---

### Theorem D (countdown carrier and boundary reset law; 048 + 050 + 053 support)
The hidden anticipation datum \(\tau\) is already a concrete countdown carrier.

On the checked active nonterminal branch:
\[
\tau(Fx)=\tau(x)-1 \qquad \text{whenever } \tau(x)>0.
\]
All nontrivial dynamics are confined to the boundary \(\tau=0\), where the reset
law is exact in the form
\[
\tau'(x)=
\begin{cases}
0, & \epsilon_4(x)=\mathrm{wrap},\\
R_{\mathrm{cj}}(s,v,\lambda), & \epsilon_4(x)=\mathrm{carry\_jump},\\
R_{\mathrm{oth}}(s,u,\lambda), & \epsilon_4(x)=\mathrm{other}.
\end{cases}
\]
Moreover, on the tested range \(m=5,7,9,11,13,15,17,19\), the reset-value sets are
exactly
\[
\operatorname{Im}(R_{\mathrm{cj}})=\{0,1,m-2\},
\qquad
\operatorname{Im}(R_{\mathrm{oth}})=\{0,m-4,m-3\}.
\]

The countdown part is formal from the definition of \(\tau\); the real theorem
content is the exact boundary reset quotient.

**Status.** The exact boundary quotients are checked on \(m=5,7,9,11\) in `048`
and persist through \(m=19\) in `050`.

---

### Corollary E (minimal positive carry coding)
On the checked active branch, the carry sheet is exactly coded by the minimal
future-side object
\[
(B,\tau,\epsilon_4).
\]
In particular, the open positive route is no longer “understand an opaque future
window”, but rather:

- code the countdown carrier \(\tau\) admissibly/locality-wise, or
- code only the boundary reset law at \(\tau=0\), since the interior law is just
  decrement.

## 2. Symbolic polish from 053

The optional reset-formula probe does **not** change the theorem object, but it
adds one clean symbolic fact on the tested range \(m=5,7,9,11,13,15,17,19\):

### Proposition E.1 (simple zero-reset fiber on the carry\_jump branch)
On the boundary branch \(\epsilon_4=\mathrm{carry\_jump}\), the zero-reset fiber is
cut out exactly by
\[
s+v+\lambda \equiv 2 \pmod m.
\]

No exact single affine law was found for the full reset map, and no exact
small-coefficient two-stage piecewise law was found in the tested catalog.
So this proposition should be read as **symbolic polish**, not as a complete
closed formula for \(R_{\mathrm{cj}}\) or \(R_{\mathrm{oth}}\).

## 3. Checked constructive refinement (remark only)

The checked data also support a stronger constructive coordinate
\[
\rho = u_{\mathrm{source}}+1 \pmod m.
\]
On the tested range through \(m=19\):

- \(\tau\) is exact on \((s,u,v,\lambda,\rho)\),
- \(\tau'\) is exact on \((s,u,\lambda,\rho,\epsilon_4)\),
- \(c\) is exact on \((u,\rho,\epsilon_4)\),
- and checked data satisfy
  \[
  q \equiv u-\rho + \mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
  \]

This is a useful **compute-side refinement**, but it is not equivalent to the
minimal theorem-side object \((B,\tau,\epsilon_4)\), because for \(m\ge 7\) the
value \(\rho\) is not recoverable from \((B,\tau,\epsilon_4)\).

So \(\rho\) should stay in the manuscript only as a remark or constructive aside,
not as a replacement theorem coordinate.

## 4. The first lower-bound proposition (kept after the positive chain)

### Proposition F (persistent bounded-horizon witness family; 047 + 050 + 052 support)
For each tested odd modulus \(m\in\{5,7,9,11,13,15,17,19\}\), the active branch
contains states
\[
x^-_m=(m-2,2,1,2,0),
\qquad
x^+_m=(m-1,2,1,2,0),
\]
with common grouped base
\[
B_*=(3,1,2,0,\mathrm{regular}),
\qquad
\epsilon_4=\mathrm{flat},
\]
but opposite carry labels
\[
c(x^-_m)=0,
\qquad
c(x^+_m)=1,
\]
and distinct countdown values
\[
\tau(x^-_m)=m-3,
\qquad
\tau(x^+_m)=m-4.
\]
Moreover, their future binary flat/nonflat signatures agree for the first
\(m-5\) steps. Hence any coding that factors only through
\[
(B,\epsilon_4,\beta_h)
\]
with \(h<m-4\) fails on modulus \(m\), where \(\beta_h\) is the next \(h\) future
flat/nonflat bits.

This is the first serious no-go direction for bounded future horizons. It should
appear **after** the positive theorem chain, because it constrains candidate local
codings without changing the theorem-side object.

## 5. What remains open on the proof side

The proof fork is now sharp.

### Positive route
Prove an admissible/local coding theorem for the countdown carrier \(\tau\), or at
least for the boundary reset law at \(\tau=0\).

### Negative route
Prove a reduction lemma showing that the intended admissible/local mechanism
class collapses to bounded grouped transition/reset data; then apply
Proposition F.

## 6. Recommended manuscript order

1. finite-cover normal form (Theorem A)
2. carry as anticipation datum (Theorem B)
3. boundary sharpening (Theorem C)
4. countdown/reset theorem (Theorem D)
5. optional symbolic remark from 053 (Proposition E.1)
6. constructive \(\rho\)-remark
7. bounded-horizon witness proposition (Proposition F)

That keeps the mathematics centered on the minimal theorem-side object
\((B,\tau,\epsilon_4)\), with the stronger source-residue picture used only as a
constructive side route.
