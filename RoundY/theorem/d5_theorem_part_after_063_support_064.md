# D5 Theorem Part After Extended 063 Constructive Support

This note updates the theorem branch after the user-level extension that the explicit `063` constructive formulas remain exact through
\[
m=13,15,17,19.
\]
The purpose is not to change the theorem object, but to sharpen the theorem-side manuscript route.

## 0. The theorem object stays minimal

The theorem object remains
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4.
\]

The coordinates
\[
\rho=u_{\mathrm{source}}+1,\qquad \alpha=\rho-u,\qquad \delta=\rho-(s+u+v+\lambda),\qquad \kappa=q+s+v+\lambda
\]
are auxiliary proof coordinates. They should not replace `(B,\tau,\epsilon_4)` in the main theorem statement.

This is exactly the theorem/constructive split recommended in the route-organization note: theorem side minimal, constructive side allowed to use the stronger transported source-residue object. 

## 1. What the theorem side should now claim

The best theorem-side slogan is unchanged:

> **On the active best-seed branch, D5 is an odometer with one corner.**

Conditional on the explicit `033` trigger family theorem for `H_{L1}`, the clean proof spine is still
\[
033 \to 062 \to 059,
\]
with the candidate-orbit / first-exit argument closing the structural branch and the mixed-witness rule yielding the current-state scheduler in the phase
\[
\kappa=q+s+v+\lambda \pmod m.
\]

So the theorem-side main result should be written as a phase-corner theorem, not as a collection of branchwise fitted formulas.

## 2. Main theorem target

### Theorem A (Phase--Corner Theorem, manuscript target)
Fix odd `m\ge 5` and the best seed. On the active nonterminal best-seed branch, let
\[
\kappa=q+s+v+\lambda \pmod m.
\]
Then:

1. **Clock law**
   \[
   \kappa' = \kappa+1 \pmod m.
   \]

2. **Current event scheduler**
   the current event `\epsilon_4` is determined by the table
   \[
   \kappa=0 \Rightarrow \mathrm{wrap},
   \qquad
   \kappa=1 \Rightarrow \mathrm{carry\_jump},
   \]
   \[
   \kappa=2 \Rightarrow
   \begin{cases}
   \mathrm{other}_{1000},& c=1,\\
   \mathrm{flat},& c=0,
   \end{cases}
   \]
   \[
   \kappa=3 \Rightarrow
   \begin{cases}
   \mathrm{other}_{0010},& (c=0\ \&\ s=2)\ \text{or}\ (c=1\ \&\ s\neq 2),\\
   \mathrm{flat},& \text{otherwise},
   \end{cases}
   \]
   and every phase `4,\dots,m-1` is flat.

3. **One-corner law**
   among flat states, the only short reset occurs at the corner
   \[
   (\kappa,s)=(2,2).
   \]

In particular, the active best-seed branch is an odometer with one corner.

## 3. Immediate corollaries to write after Theorem A

### Corollary B (Countdown law)
On the active nonterminal branch,
\[
\tau=0 \quad \text{on nonflat states},
\]
and on flat states,
\[
\tau=
\begin{cases}
1,& (\kappa,s)=(2,2),\\
m-\kappa,& \text{otherwise}.
\end{cases}
\]
Hence
\[
\tau' = \tau-1 \qquad (\tau>0).
\]

### Corollary C (CJ reset formula)
The carry-jump reset law is
\[
R_{\mathrm{cj}}=
\begin{cases}
0,& s+v+\lambda\equiv 2 \pmod m,\\
1,& s=1 \text{ and } s+v+\lambda\not\equiv 2 \pmod m,\\
m-2,& \text{otherwise.}
\end{cases}
\]

### Corollary D (OTH reset formulas)
The two `other` branches satisfy
\[
(1,0,0,0)\mapsto
\begin{cases}
m-3,& s=1,\\
0,& s\neq 1,
\end{cases}
\qquad
(0,0,1,0)\mapsto m-4.
\]

### Corollary E (Finite-cover compatibility)
The phase-corner machine is compatible with the structural finite-cover chain
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
where
\[
c=1_{\{q=m-1\}},
\qquad d=1_{\{\text{next carry }u\ge m-3\}}.
\]

So the finite-cover normal form and the countdown/reset theorems are not separate objects; they are two views of the same active machine.

## 4. Theorem-side proof route

The theorem-side manuscript should use the following order.

### Proposition 1. Explicit trigger family (import from `033`)
State the exact formula
\[
H_{L1}=\{(q,w,u,\lambda)=(m-1,m-1,u,2):u\neq 2\}.
\]

### Proposition 2. Universal first-exit targets
Using the phase-1 source-residue invariant
\[
q\equiv u-\rho+1 \pmod m,
\qquad \rho=u_{\mathrm{source}}+1,
\]
derive the only possible trigger states
\[
T_{\mathrm{reg}}=(m-1,m-2,1),
\qquad
T_{\mathrm{exc}}=(m-2,m-1,1).
\]

### Proposition 3. Pre-exit `B`-region invariance
Show that the actual active branch agrees with the candidate orbit up to first exit, hence every active nonterminal current state is `B`-labelled.

### Proposition 4. Mixed-witness scheduler on active nonterminal states
Because every active nonterminal current state is `B`-labelled, the mixed witness rule applies exactly there. This induces the current-state scheduler in `\kappa`.

### Theorem 5. Phase--Corner Theorem
Promote Proposition 4 to Theorem A.

### Corollaries 6--9
Deduce the countdown law, reset formulas, and finite-cover compatibility.

This is the theorem route. It is cleaner than proving `CJ` and `OTH` separately and then trying to interpret them afterward.

## 5. How to use the constructive support without changing the theorem object

The constructive route is now explicitly stable through `m=19`, but it should be used only as support.

The useful theorem-side remark is:

### Remark F (Auxiliary constructive clock)
On the constructive route, define
\[
\alpha=\rho-u,
\qquad
\delta=\rho-(s+u+v+\lambda)=\alpha-(s+v+\lambda).
\]
Then on flat states,
\[
\delta\equiv -\kappa \pmod m.
\]
So the constructive residue clock and the theorem-side phase clock are the same machine in two gauges.

This is the right way to use the extended `063` constructive exactness in the theorem manuscript:
- not as a replacement theorem coordinate,
- but as evidence that the phase-corner theorem is not accidental.

## 6. Honest remaining open point

The theorem side is now close to stable in shape.

The real remaining frontier is not “what should the theorem say?”
It is one of two external closure questions:

1. **positive constructive closure**:
   can one locally initialize and transport source residue (preferably `\alpha=\rho-u`)?
2. **negative closure**:
   can one prove that the intended admissible/local class collapses to a bounded quotient and therefore cannot transport that residue uniformly in `m`?

So the theorem manuscript should now proceed as though the theorem object is known:

> the active best-seed D5 branch is a phase-corner / one-corner odometer machine.

The unresolved issue is whether that machine can be locally realized in the intended admissible class.
