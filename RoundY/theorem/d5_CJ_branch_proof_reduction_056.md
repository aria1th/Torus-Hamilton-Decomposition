# D5 CJ-First Boundary Reset Proof Reduction 056

This note keeps the theorem object fixed at
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\},
\]
and pushes the proof of the uniform odd-\(m\) boundary reset theorem through the
carry\_jump branch first.

The guiding chain remains:

1. `044`: finite-cover normal form
   \[
   B \leftarrow B+c \leftarrow B+c+d,
   \qquad
   c=\mathbf 1_{\{q=m-1\}},
   \qquad
   d=\mathbf 1_{\{U^+\ge m-3\}}.
   \]
2. `046`: the carry sheet \(c\) is a one-sided anticipation datum.
3. `047`: all \((B,\tau)\)-ambiguity lies at \(\tau=0\), with genuine boundary class
   \(\{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}\).
4. `048/050/052/053/055`: on the tested range through \(m=23\), \(\tau\) is an exact
   countdown carrier, and the boundary reset law stays exact on the same theorem-side
   quotients.

The theorem-side question is therefore:

> Can the boundary reset map
> \[
> R(\epsilon_4,s,u,v,\lambda)=\tau(Fx)\qquad(\tau(x)=0)
> \]
> be proved uniformly for odd \(m\)?

The current reduction says yes, provided two branch lemmas are proved:

- **CJ**: the carry\_jump reset law;
- **OTH**: the other-branch subtype/reset law.

`wrap -> 0` is already formal.

---

## 1. Formal part already proved

By definition of \(\tau\) as the initial flat-prefix length of the future grouped-delta
sequence,
\[
\tau(Fx)=\tau(x)-1\qquad(\tau(x)>0).
\]
So the only nontrivial part of the reset theorem is the boundary \(\tau=0\).

---

## 2. Carry\_jump branch: theorem statement

On the tested range \(m=5,7,9,11,13,15,17,19,21,23\), the carry\_jump boundary reset is
exactly
\[
R_{\mathrm{cj}}(s,v,\lambda)=
\begin{cases}
0,& s+v+\lambda\equiv 2 \pmod m,\\[1mm]
1,& s=1 \text{ and } s+v+\lambda\not\equiv 2 \pmod m,\\[1mm]
m-2,& \text{otherwise.}
\end{cases}
\tag{CJ-form}
\]
Equivalently, on the carry\_jump boundary,
\[
q\equiv 1-s-v-\lambda \pmod m.
\tag{CJ-q}
\]

The checked image set is exactly
\[
\mathrm{Im}(R_{\mathrm{cj}})=\{0,1,m-2\}
\]
through \(m=23\).

---

## 3. First proof lemma on CJ: eliminate the constructive residue \(\rho\)

The stronger compute-side refinement says that on the active branch
\[
q\equiv u-\rho+\mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m,
\qquad \rho=u_{\mathrm{source}}+1.
\tag{rho-q}
\]
On the carry\_jump boundary this becomes
\[
q\equiv u-\rho+1 \pmod m.
\tag{CJ-rho-q}
\]
Combining this with the checked current-state carry\_jump identity `(CJ-q)` gives the
auxiliary boundary relation
\[
\rho\equiv s+u+v+\lambda \pmod m.
\tag{CJ-rho}
\]
So the theorem-side carry\_jump law can be read as the elimination of the constructive
source residue \(\rho\) from the compute-side formula.

This is an important proof-side simplification:

- `rho` remains only an auxiliary witness coordinate;
- the theorem object is still \((B,\tau,\epsilon_4)\).

---

## 4. What is already explained on the CJ branch

The zero-reset fiber is now conceptually clear.

From `(CJ-q)`,
\[
s+v+\lambda\equiv 2 \pmod m
\iff
q\equiv m-1.
\]
But \(q=m-1\) is exactly the carry slice \(c=1\). On the tested range, this is precisely
the subfiber on which the carry\_jump boundary resets to
\[
R_{\mathrm{cj}}=0.
\]
So the first branch of `(CJ-form)` is already reduced to the carry-sheet identity.

Thus the remaining CJ content is the noncarry dichotomy:

> **CJ noncarry dichotomy.**  On the carry\_jump boundary with \(q\neq m-1\),
> \[
> R_{\mathrm{cj}}=
> \begin{cases}
> 1,& s=1,\\
> m-2,& s\neq 1.
> \end{cases}
> \tag{CJ*}
> \]

This is the real proof target on the carry\_jump branch.

---

## 5. Why proving CJ first is the right move

The support through \(m=23\) shows that CJ is much sharper than OTH.

### 5.1 What is now theorem-like on CJ

- the boundary class is fixed: \(\epsilon_4=\mathrm{carry\_jump}\);
- the raw coordinate is eliminated by `(CJ-q)`;
- the zero-reset fiber is exactly the carry slice;
- the only remaining split is the short/long noncarry reset `(CJ*)`.

### 5.2 What remains looser on OTH

OTH still needs:

- the proof that only the two grouped-delta subtypes
  \[
  (0,0,1,0),\qquad (1,0,0,0)
  \]
  occur on the tested boundary;
- the exact reset law on those two subtypes;
- the discriminator description via
  \[
  r=\lambda+3((s-u)-1).
  \]

So CJ is presently the more theorem-ready branch.

---

## 6. Clean proof fork after this reduction

There are now two distinct proof tasks.

### Positive route
Prove `(CJ*)` and the OTH subtype/reset law uniformly for odd \(m\), which yields the
uniform boundary reset theorem.

### Negative route
If a local/admissible coding theorem is still sought, prove that the intended local class
collapses to bounded transition/reset data and then apply the witness family from `047/050`.

These routes are independent.  The boundary reset theorem itself no longer depends on
proving a local coding theorem.

---

## 7. Current honest status

What is essentially settled on the theorem side:

- `046` is the conceptual theorem: the carry sheet is an anticipation datum;
- `047` is only the boundary sharpening;
- `048` identifies the hidden datum as an exact countdown carrier;
- `053/055` give symbolic polish for the carry\_jump zero-reset fiber and extend the
  checked support through \(m=23\).

What remains to prove uniformly:

1. `CJ*` (the short/long noncarry dichotomy on the carry\_jump boundary),
2. the OTH subtype/reset theorem.

So the proof burden is now much smaller than “understand the future window.”
It is exactly:

\[
\textbf{prove two boundary branch lemmas, starting with CJ.}
\]
