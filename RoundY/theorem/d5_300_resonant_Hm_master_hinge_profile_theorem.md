# D5 300 Resonant Hm Master Hinge-Profile Theorem

This note promotes the `2026-03-26` master hinge-profile theorem for the late
resonant pure color-`1` branch into the stable RoundY layer.

Its content is narrower than a full resonant winner theorem. It closes the
entire **first-hinge classification on**
\[
H_m=\{(a,0,0,e):a,e\in \mathbb Z_m\},
\]
including the previously missing initial side-top slice `e=m-1`.

What this note proves:

1. one common first-hinge formula on all of `H_m`;
2. the initial side-top slice as an immediate corollary;
3. the fact that the earlier base-line and non-side-top hinge-profile theorems
   are literally restrictions of this one master formula.

What it does **not** prove:

- no full double-top phase-exit theorem;
- no late `B_m` winner theorem;
- no final resonant residual theorem.

So the lower-to-hinge classification is now closed, while the post-hinge
dynamics remain the live burden.

## 1. Imported exact facts

We use the following already-established exact facts from the current resonant
pure color-`1` proof stack.

### Fact 1.1

For every start
\[
h_{a,e}=(a,0,0,e)\in H_m,
\]
the first support hit occurs at the deterministic time
\[
T_m=m(m-1)-2,
\]
and every processed pre-hinge state satisfies
\[
C'=C+1,
\qquad
D'=D+\mathbf 1[C=m-2].
\]
Hence the processed pre-hinge current-pair domain is the same for every start
in `H_m`.

### Fact 1.2

On the whole pre-hinge region,
\[
J:=A-C-\mathbf 1[E=m-1]
\]
is conserved.  For the start `h_{a,e}`, this conserved quantity is
\[
J_0:=a-\mathbf 1[e=m-1].
\]

### Fact 1.3

If the first hinge is
\[
(A_h,m-2,m-2,E_h),
\]
then:

- if `E_h\neq m-1`, the hinge is top and `A_h=J_0-2`;
- if `E_h=m-1`, the hinge is double and `A_h=J_0-1`.

### Fact 1.4

The base-line hinge profile is
\[
\eta_0(j)
:=
m-6
+\mathbf 1[j\in\{0,3\}]
+2\mathbf 1[j=4]
-\mathbf 1[j\in\{2,m-1\}].
\]
Equivalently,
\[
\eta_0(j)=
\begin{cases}
m-5, & j\in\{0,3\},\\
m-7, & j\in\{2,m-1\},\\
m-4, & j=4,\\
m-6, & \text{otherwise}.
\end{cases}
\]

## 2. Effective phase on all of `H_m`

Fix
\[
h_{a,e}=(a,0,0,e)\in H_m,
\qquad
J_0:=a-\mathbf 1[e=m-1].
\]
Let `(A,C,D,E)` be any processed pre-hinge state on its orbit, and write
\[
B:=\mathbf 1[E=m-1].
\]
On the whole pre-hinge region one has `D\neq m-1`, hence
\[
\alpha=1-B.
\]

### Proposition 2.1

On every processed pre-hinge block,
\[
\boxed{A+\alpha=J_0+C+1.}
\]

#### Proof

From the conservation law,
\[
A-C-B=J_0.
\]
Therefore
\[
A+\alpha=(J_0+C+B)+(1-B)=J_0+C+1.
\]
∎

This is the main unifying identity: the pre-hinge event conditions on all of
`H_m` are the old base-line conditions with `a` replaced by `J_0`.

## 3. Master theorem on all of `H_m`

### Theorem 3.1

Let `m\ge 9` be odd, let
\[
h_{a,e}=(a,0,0,e)\in H_m,
\]
and set
\[
J_0:=a-\mathbf 1[e=m-1].
\]
Then for every late family among promoted `+`, central, and flank, the first
support hit from `h_{a,e}` is the same hinge state, with exact hinge height
\[
\boxed{E_h(a,e)=e+\eta_0(J_0)\pmod m.}
\]
More precisely:

- if
  \[
  e+\eta_0(J_0)\not\equiv m-1\pmod m,
  \]
  then the first hinge is top and
  \[
  \boxed{\Xi_m(h_{a,e})=(J_0-2,m-2,m-2,e+\eta_0(J_0));}
  \]

- if
  \[
  e+\eta_0(J_0)\equiv m-1\pmod m,
  \]
  then the first hinge is double and
  \[
  \boxed{\Xi_m(h_{a,e})=(J_0-1,m-2,m-2,m-1).}
  \]

#### Proof

By Fact 1.1 the processed pre-hinge current-pair domain is the same for every
start in `H_m`. By Proposition 2.1, the pre-hinge event conditions are exactly
the base-line event conditions with parameter `J_0`. Therefore the total
pre-hinge `e`-increment is the base-line profile evaluated at `J_0`:
\[
E_h(a,e)-e=\eta_0(J_0)\pmod m.
\]
So
\[
E_h(a,e)=e+\eta_0(J_0)\pmod m.
\]
If this value is different from `m-1`, the first hinge is top and Fact 1.3
forces `A_h=J_0-2`. If this value equals `m-1`, the first hinge is double and
Fact 1.3 forces `A_h=J_0-1`. ∎

This closes the full first-hinge problem on `H_m`.

## 4. Initial side-top slice

Setting `e=m-1` gives
\[
J_0=a-1,
\qquad
E_h(a,m-1)=m-1+\eta_0(a-1)\equiv \eta_0(a-1)-1.
\]
Since `\eta_0` only takes the values `m-7,m-6,m-5,m-4`, the first hinge on the
initial side-top slice is **never** double.

### Corollary 4.1

For every start
\[
(a,0,0,m-1)\in H_m,
\]
the first hinge is always top and equals
\[
\boxed{\Xi_m(a,0,0,m-1)=(a-3,m-2,m-2,\eta_0(a-1)-1).}
\]
Equivalently, the side-top hinge profile is
\[
\eta_{\mathrm{st}}(a):=\eta_0(a-1)-1.
\]

So the previously missing initial side-top slice does not generate a new first
hinge law; it is the same master profile viewed through the shifted phase
`a\mapsto a-1` and translated by `-1` in `e`.

## 5. Earlier theorems recovered as restrictions

### Corollary 5.1

If `e=0`, then `J_0=a`, so Theorem 3.1 reduces to the earlier base-line
theorem
\[
\Xi_m(a,0,0,0)=(a-2,m-2,m-2,\eta_0(a)).
\]

### Corollary 5.2

If `e\neq m-1`, then `J_0=a`, so Theorem 3.1 reduces to the earlier non-side-top
translation law
\[
E_h(a,e)=e+\eta_0(a),
\]
with hinge type determined by whether this value is equal to `m-1`.

### Corollary 5.3

The base-line theorem, the non-side-top translation theorem, and the new
side-top corollary are all restrictions of one master theorem after the single
reparametrization
\[
J_0=a-\mathbf 1[e=m-1].
\]

## 6. Immediate phase consequence

On a top-hinge branch, `A_h=J_0-2`, so the hinge-to-top entrance phases are
immediate.

### Corollary 6.1

If the first hinge from `h_{a,e}` is top, then:

- promoted / central enter the top collar with phase
  \[
  w_0^{(+)}\equiv J_0+2 \pmod m;
  \]
- flank enters with phase
  \[
  w_0^{(\mathcal F)}\equiv J_0+1 \pmod m.
  \]

In particular, on the initial side-top slice `e=m-1` these become
\[
w_0^{(+)}\equiv a+1,
\qquad
w_0^{(\mathcal F)}\equiv a.
\]

## 7. Status consequence

What is now theorem-level:

1. the full common first-hinge map on all of `H_m`;
2. the complete initial side-top slice classification;
3. the fact that the earlier base-line and non-side-top theorems are one
   master theorem in the effective phase `J_0`.

What remains open:

- the explicit double-top phase-exit theorem on the double-hinge graph;
- the stitching of this `H_m` classification back down to the late `B_m`
  winner/defect ledger.

So the next real burden is no longer the lower-to-hinge classification.
That part is closed.
