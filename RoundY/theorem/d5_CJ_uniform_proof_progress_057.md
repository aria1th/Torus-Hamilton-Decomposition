# D5 CJ Uniform Proof Progress 057

This note keeps the theorem object fixed at
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\},
\]
and pushes the carry\_jump branch proof one step further.

The main new point is that the carry\_jump reset law can be reduced to a
single **flat-corner countdown lemma** on the constructive side, without
promoting the source residue \(\rho\) to a theorem coordinate.

---

## 1. Target CJ statement

On the checked active branch, the carry\_jump reset law is
\[
R_{\mathrm{cj}}(s,v,\lambda)=
\begin{cases}
0,& s+v+\lambda\equiv 2 \pmod m,\\[1mm]
1,& s=1 \text{ and } s+v+\lambda\not\equiv 2 \pmod m,\\[1mm]
m-2,& \text{otherwise.}
\end{cases}
\tag{CJ}
\]
Equivalently, on the carry\_jump boundary,
\[
q\equiv 1-s-v-\lambda \pmod m.
\tag{CJ-q}
\]

The zero-reset fiber is already conceptually explained:
\[
s+v+\lambda\equiv 2 \iff q=m-1 \iff c=1 \iff R_{\mathrm{cj}}=0.
\]
So the only real CJ content is the noncarry part
\[
q\neq m-1 \Longrightarrow
R_{\mathrm{cj}}=
\begin{cases}
1,& s=1,\\
m-2,& s\neq 1.
\end{cases}
\tag{CJ*}
\]

---

## 2. Auxiliary constructive residue

As in `049`, let
\[
\rho = u_{\mathrm{source}}+1 \in \mathbb Z_m.
\]
Define the auxiliary residue
\[
\delta := \rho-(s+u+v+\lambda) \in \mathbb Z_m.
\tag{delta}
\]
This is **not** a new theorem coordinate.  It is an auxiliary proof device,
used only to simplify the CJ branch.

Two checked identities are important.

### 2.1 Carry\_jump elimination identity

On the carry\_jump boundary,
\[
q\equiv u-\rho+1 \pmod m
\]
and therefore, combining with `(CJ-q)`,
\[
\rho\equiv s+u+v+\lambda \pmod m.
\tag{CJ-rho}
\]
So on a carry\_jump state, \(\delta=0\).

### 2.2 Flat-step residue rule

On a flat state, \(dn=(0,0,0,1)\), so \(s,u,v\) are fixed and \(\lambda\) increases by
\(1\). Hence under one flat step,
\[
\delta \mapsto \delta-1.
\tag{delta-flat}
\]

---

## 3. Successor of a noncarry carry\_jump state

Let \(x\) be a boundary state with
\[
\tau(x)=0,\qquad \epsilon_4(x)=\mathrm{carry\_jump},\qquad c(x)=0.
\]
Let \(y=F(x)\) be its successor.

Since carry\_jump has
\[
dn=(1,1,0,0),
\]
we have
\[
s(y)=s(x)+1,\qquad u(y)=u(x)+1,\qquad v(y)=v(x),\qquad \lambda(y)=\lambda(x).
\tag{CJ-succ}
\]
Moreover \(q\) is unchanged across a carry\_jump step, because
\[
q(x)=u(x)-\rho+1,
\qquad
q(y)=u(y)-\rho,
\]
and `(CJ-succ)` gives \(u(y)=u(x)+1\).

Using `(CJ-rho)` and `(CJ-succ)`, the successor residue is
\[
\delta(y)=\rho-(s(y)+u(y)+v(y)+\lambda(y))
=\rho-(s(x)+u(x)+v(x)+\lambda(x)+2)
\equiv -2 \equiv m-2.
\tag{CJ-delta}
\]
So every noncarry carry\_jump state lands in a flat state with
\[
\delta=m-2.
\]
This is the key reduction.

---

## 4. Checked flat-corner lemma

The frozen `047` checked data imply the following exact one-step law on the
flat branch for \(m=5,7,9,11\):

> **Flat-corner lemma (checked).**  Let \(y\) be a flat state and write
> \(\delta(y)=\rho-(s+u+v+\lambda)\).
> Then:
> 1. if \(\delta=1\), the next event is `wrap`;
> 2. if \(2\le \delta\le m-3\), the next event is `flat`;
> 3. if \(\delta=m-2\), the next event is
>    \[
>    \begin{cases}
>    \mathrm{other},& s=2,\\
>    \mathrm{flat},& s\neq 2.
>    \end{cases}
>    \tag{Flat-corner}
>    \]

Equivalently, on the checked flat branch,
\[
\tau(y)=
\begin{cases}
1,& (s(y),\delta(y))=(2,m-2),\\
\delta(y),& \text{otherwise.}
\end{cases}
\tag{Flat-tau}
\]
The proof is immediate from `(delta-flat)` by induction on \(\delta\), once the
one-step event classification `(Flat-corner)` is known.

This is **not yet proved uniformly in odd \(m\)** in this note.  It is the
single remaining auxiliary lemma needed to finish CJ.

---

## 5. CJ from the flat-corner lemma

Assume `(Flat-corner)`.

Take a noncarry carry\_jump state \(x\).  By `(CJ-delta)`, its successor \(y=F(x)\)
is flat with \(\delta(y)=m-2\).  Also, by `(CJ-succ)`,
\[
s(y)=s(x)+1.
\]
Applying `(Flat-tau)` to \(y\), we obtain
\[
\tau(y)=
\begin{cases}
1,& s(y)=2,\\
m-2,& s(y)\neq 2,
\end{cases}
\]
that is,
\[
R_{\mathrm{cj}}(x)=
\begin{cases}
1,& s(x)=1,\\
m-2,& s(x)\neq 1.
\end{cases}
\]
This is exactly the noncarry dichotomy `(CJ*)`.

Together with the already-settled zero-reset fiber, this yields the full
carry\_jump formula `(CJ)`.

So the uniform CJ theorem is now reduced to a very small auxiliary statement:

> prove the flat-corner one-step law `(Flat-corner)` uniformly in odd \(m\).

---

## 6. Why this is real proof progress

Before this reduction, CJ still looked like a direct boundary theorem.
After introducing the auxiliary residue \(\delta\), the CJ branch becomes:

1. carry\_jump boundary gives \(\delta=0\);
2. one CJ step sends every noncarry state to a flat state with \(\delta=m-2\);
3. CJ reset is therefore determined entirely by the flat-corner law at
   \(\delta=m-2\).

This is much sharper than the earlier formulation.

The remaining proof burden is now **not** “understand the whole future window”
or even “understand all of OTH.”  It is only:

- prove the flat one-step transition rule at \(\delta=m-2\),
- equivalently, prove `(Flat-corner)`.

That is the right next proof target.

---

## 7. Honest status

What is proved or formally reduced:

- the theorem object remains \((B,\tau,\epsilon_4)\);
- zero-reset on the CJ branch is explained by the carry slice;
- noncarry CJ is reduced to the successor flat state with \(\delta=m-2\);
- assuming the flat-corner lemma, the full CJ formula follows.

What still remains open for a uniform odd-\(m\) proof:

- prove the flat-corner lemma `(Flat-corner)` uniformly;
- then separately prove the OTH branch.

So the CJ branch is now very close: its only remaining content is the
flat-corner one-step law.
