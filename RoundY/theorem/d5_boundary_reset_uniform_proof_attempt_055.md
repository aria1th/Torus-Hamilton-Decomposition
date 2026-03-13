# D5 proof attempt 055: uniform odd-\(m\) boundary reset theorem

## Goal

Try to promote the checked boundary reset law from `048/050/053` into a uniform odd-\(m\) theorem on the active best-seed branch for
\[
R1\to H_{L1}.
\]

The theorem-side object remains
\[
B=(s,u,v,\lambda,f),\qquad \tau,\qquad \epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]

This note keeps the positive chain centered on `046`:

1. finite-cover normal form `044`
2. carry as anticipation datum `046`
3. boundary sharpening `047`
4. countdown/reset law `048/050`

The stronger source-residue coordinate
\[
\rho=u_{\mathrm{source}}+1\pmod m
\]
is used only as an **auxiliary proof device**.

---

## 1. What is already formal

Let
\[
\tau(x)=\max\{t\ge 0: dn(F^j x)=\delta_{\mathrm{flat}}\text{ for }0\le j<t\},
\qquad
\delta_{\mathrm{flat}}=(0,0,0,1).
\]

Then:

### Lemma 1.1 (countdown away from the boundary)
If \(\tau(x)>0\), then
\[
\tau(Fx)=\tau(x)-1.
\]

### Proof
This is immediate from the definition of \(\tau\) as the initial flat-prefix length of the future grouped-delta sequence. Shifting the future sequence forward shortens that prefix by one whenever the prefix is nonempty. ∎

So the only genuinely D5-specific content is the boundary reset law at \(\tau=0\).

---

## 2. The boundary classes

At the boundary \(\tau=0\), the current grouped-delta event is nonflat and falls into exactly three classes:
\[
\epsilon_4\in\{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]

On the checked range, the exact reset law is:
\[
\tau'(x)=
\begin{cases}
0,& \epsilon_4=\mathrm{wrap},\\
R_{\mathrm{cj}}(s,v,\lambda),& \epsilon_4=\mathrm{carry\_jump},\\
R_{\mathrm{oth}}(s,u,\lambda),& \epsilon_4=\mathrm{other}.
\end{cases}
\]

Theorem `D` in the positive chain only needs these branchwise quotient statements. But the checked data now support a sharper symbolic picture.

---

## 3. Carry\_jump branch: explicit candidate formula

Write \(R_{\mathrm{cj}}\) for the boundary reset on the carry\_jump branch.

### Checked formula (exact on \(m=5,7,9,11\))
On the checked range,
\[
R_{\mathrm{cj}}(s,v,\lambda)=
\begin{cases}
0,& s+v+\lambda\equiv 2\pmod m,\\
1,& s=1 \text{ and } s+v+\lambda\not\equiv 2\pmod m,\\
m-2,& \text{otherwise}.
\end{cases}
\]

Equivalently, on the carry\_jump boundary one has the current-state raw formula
\[
q\equiv 1-s-v-\lambda\pmod m,
\]
which is exact on the checked range, so the zero-reset fiber is exactly the carry slice
\[
q=m-1
\iff s+v+\lambda\equiv 2\pmod m.
\]
This matches the `053` symbolic finding.

### Proof on the checked range
A direct validation on the frozen `047` dataset shows:

1. on the carry\_jump boundary,
   \[
   q=1-s-v-\lambda
   \quad (\text{exact on }m=5,7,9,11),
   \]
2. the reset values are exactly \(\{0,1,m-2\}\),
3. the partition above matches every checked carry\_jump boundary state.

So the formula is a verified candidate for the uniform theorem.

### What remains to prove uniformly
It is enough to prove the following branch lemma.

### Lemma CJ (uniform target)
On the carry\_jump boundary for every odd \(m\ge 5\):

1. \(q=1-s-v-\lambda\) on the active branch;
2. if \(q=m-1\), then the next grouped-delta event is immediately nonflat, so \(\tau'=0\);
3. if \(q\neq m-1\) and \(s=1\), then exactly one flat step occurs before the next nonflat event, so \(\tau'=1\);
4. if \(q\neq m-1\) and \(s\neq 1\), then the next nonflat event occurs after a full \(m-2\)-step flat block, so \(\tau'=m-2\).

Once Lemma CJ is proved, the carry\_jump part of the boundary reset theorem follows immediately.

---

## 4. Other branch: structural split and explicit checked formula

The `other` class is the only genuinely mixed branch. On the checked range it splits into two concrete grouped-delta subtypes:
\[
(0,0,1,0)\qquad\text{and}\qquad(1,0,0,0).
\]

A direct read of the frozen `047` data gives:

### Lemma 4.1 (checked subtype reset values)
On the `other` boundary:

1. if
   \[
   dn=(0,0,1,0),
   \]
   then
   \[
   \tau'=m-4;
   \]
2. if
   \[
   dn=(1,0,0,0),
   \]
   then
   \[
   \tau'=
   \begin{cases}
   m-3,& s=1,\\
   0,& s\neq 1.
   \end{cases}
   \]

So the whole `other` reset law reduces to one question:

> can the current-state subtype \((0,0,1,0)\) versus \((1,0,0,0)\) be identified uniformly from \((s,u,\lambda)\)?

The answer is **yes on the checked range**, and that is exactly what the theorem statement from `048/050` is recording abstractly.

### Checked-range discriminator
Let
\[
w=s-u\pmod m,
\qquad
r=\lambda+3(w-1)\pmod m.
\]
On the checked range, the following piecewise law is exact:
\[
R_{\mathrm{oth}}(s,u,\lambda)=
\begin{cases}
m-3,& r=0\text{ and }s=1,\\
0,& r=2,\\
0,& r=0,\ s\notin\{1,2\},\\
0,& r=0,\ s=2,\ u=1,\\
m-4,& \text{otherwise}.
\end{cases}
\]
This formula is **not** yet promoted as canonical manuscript language; it should be viewed as a proof-supporting explicit checked description of the current quotient theorem.

### What remains to prove uniformly
It is enough to prove the following branch lemma.

### Lemma OTH (uniform target)
On the `other` boundary for every odd \(m\ge 5\):

1. the subtype \(dn=(0,0,1,0)\) versus \(dn=(1,0,0,0)\) is a function of \((s,u,\lambda)\);
2. on the \((0,0,1,0)\) subtype one has \(\tau'=m-4\);
3. on the \((1,0,0,0)\) subtype one has
   \[
   \tau'=
   \begin{cases}
   m-3,& s=1,\\
   0,& s\neq 1.
   \end{cases}
   \]

Once Lemma OTH is proved, the `other` part of the boundary reset theorem follows.

---

## 5. Wrap branch

This one is already conceptually trivial.

### Lemma WRAP (uniform target)
On the wrap boundary,
\[
\tau'=0.
\]

### Reason
`047/048` show that wrap is immediately followed by a nonflat event and never begins a positive flat run. This is exact on the checked range and is the simplest part of the boundary theorem to prove from the grouped-delta transition rules.

---

## 6. Uniform boundary reset theorem: reduced proof target

Putting the previous pieces together gives the following reduced theorem.

### Theorem BR (uniform odd-\(m\) target)
For every odd \(m\ge 5\), on the active best-seed branch the countdown carrier \(\tau\) satisfies
\[
\tau(Fx)=\tau(x)-1\qquad (\tau(x)>0),
\]
and at the boundary \(\tau(x)=0\) one has the exact reset law
\[
\tau'(x)=
\begin{cases}
0,& \epsilon_4(x)=\mathrm{wrap},\\
R_{\mathrm{cj}}(s,v,\lambda),& \epsilon_4(x)=\mathrm{carry\_jump},\\
R_{\mathrm{oth}}(s,u,\lambda),& \epsilon_4(x)=\mathrm{other},
\end{cases}
\]
where the branchwise reset maps are given by the two auxiliary lemmas `CJ` and `OTH`.

### Proof sketch
- the decrement law is formal (Lemma 1.1);
- `wrap` is immediate;
- `carry_jump` reduces to Lemma `CJ`;
- `other` reduces to Lemma `OTH`.

So the full uniform theorem has been reduced to two explicit branchwise statements.

---

## 7. What is genuinely proved now, and what is still open

### Checked and settled
1. the theorem-side object remains \((B,\tau,\epsilon_4)\);
2. the positive chain `044 -> 046 -> 047 -> 048/050` is stable;
3. \(\tau\) is a true countdown carrier;
4. the boundary theorem is exact on the checked range through the quotients already stated in `048/050`;
5. on the checked range, the carry\_jump branch admits the explicit formula
   \[
   R_{\mathrm{cj}}(s,v,\lambda)=0/1/(m-2)
   \]
   as above;
6. on the checked range, the `other` branch splits into two concrete grouped-delta subtypes with reset values
   \[
   m-4\quad\text{or}\quad 0/(m-3),
   \]
   and this is exact on \((s,u,\lambda)\).

### Still open
A **uniform proof** of the boundary reset theorem still requires proving the two branch lemmas `CJ` and `OTH` for all odd \(m\).

That is the right next proof target.

---

## 8. Recommended manuscript stance

The manuscript should still say:

- `046` is the conceptual theorem;
- `047` is only the boundary sharpening;
- `048/050` identify the hidden anticipation datum as a countdown carrier with a tiny reset law.

The explicit formulas above should be presented as:
- carry\_jump explicit formula candidate (stronger than the theorem statement),
- checked explicit `other`-branch piecewise law (proof support),
- both subordinate to the minimal theorem-side quotient language.

That keeps the theorem object clean while making the proof target substantially sharper.
