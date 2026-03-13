# D5 proof progress 052: countdown carrier, boundary reset law, and lower bounds

## Scope

This note keeps the theorem-side object fixed at
\[
(B,\tau,\epsilon_4),
\qquad B=(s,u,v,\lambda,f),
\]
and treats the source-residue coordinate
\[
\rho=u_{\mathrm{source}}+1\pmod m
\]
only as a stronger checked constructive refinement.

The aim is to sharpen the proof program after `044--050` without changing the
main theorem object.

Checked ranges used below:
- `044--048` main theorem-chain facts: checked on
  \[
  m\in\{5,7,9,11\};
  \]
- `049/050` proof-support refinements (source-residue route, reset-law
  persistence, witness persistence): checked on
  \[
  m\in\{5,7,9,11,13,15,17,19\}.
  \]

Status labels:
- **[C]** checked on the active best-seed branch on the stated odd moduli
- **[F]** formal consequence of definitions
- **[H]** theorem-shaped target for all odd `m\ge 5`
- **[O]** open

---

## 1. The theorem chain should now read `044 -> 046 -> 047 -> 048/050`

The most stable manuscript ordering is:

### Theorem A (finite-cover normal form) [C -> H]
On the active best-seed branch, the checked structure factors as
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with
\[
B=(s,u,v,\lambda,f),
\qquad
c=\mathbf 1_{\{q=m-1\}},
\qquad
d=\mathbf 1_{\{U^+\ge m-3\}}.
\]
Moreover:
1. exceptional trigger descends to `B`;
2. regular trigger descends to `B+c` but not to `B`;
3. deterministic active evolution closes on `B+c+d`.

This is the correct D5 structural object: grouped skew-odometer base, one
trigger-level carry sheet, one residual binary anticipation sheet.

### Theorem B (carry as anticipation datum) [C -> H]
The carry sheet `c` is not a current grouped-state observable. It is an exact
one-sided future grouped-transition datum.

A canonical future-side signature is
\[
(B,\tau,\eta),
\]
where `\tau` is the initial flat-run length for the future grouped-delta
sequence and `\eta` is the first nonflat grouped-delta event.

Checked minimal exact horizons:
- future grouped-delta horizon: `m-3`;
- future grouped-state horizon: `m-2`.

This is the conceptual theorem of the current D5 branch.

### Proposition C (boundary sharpening) [C -> H]
All ambiguity of `B+\tau` lies at the boundary `\tau=0`. At that boundary, the
current grouped-delta event class is genuinely three-way:
\[
\{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]
So the theorem-side quotient is canonically
\[
(B,\tau,\epsilon_4),
\qquad
\epsilon_4\in\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]
The checked-range truncations such as `min(\tau,8)` are evidence, not the final
canonical form.

### Theorem D (countdown carrier with boundary reset law) [F + C -> H]
Define
\[
\tau(x)=\max\{t\ge 0: dn_j(x)=\delta_{\mathrm{flat}} \text{ for } 0\le j<t\},
\qquad
\delta_{\mathrm{flat}}=(0,0,0,1).
\]
Then away from the boundary,
\[
\tau(Fx)=\tau(x)-1 \qquad (\tau(x)>0).
\]
Thus all nontrivial dynamics of `\tau` are confined to `\tau=0`.

On the tested range
\[
m\in\{5,7,9,11,13,15,17,19\},
\]
the boundary reset law is exact on the small current quotients:
- `wrap -> 0`;
- `carry_jump` exact on `(s,v,\lambda)`;
- `other` exact on `(s,u,\lambda)`.

More sharply, the tested reset-value images are **equalities**, not just
containments:
\[
\mathrm{Im}(R_{\mathrm{cj}})=\{0,1,m-2\},
\qquad
\mathrm{Im}(R_{\mathrm{oth}})=\{0,m-4,m-3\}.
\]

So the hidden future datum is not an opaque window. It is a countdown carrier
with a tiny boundary reset micro-law.

### Corollary E (reduction of the local problem) [F + C]
Once `c` is known to factor through `(B,\tau,\epsilon_4)`, and `\tau` is known
to satisfy countdown away from the boundary, any local/admissible realization of
`c` reduces to one of two proof problems:
1. code the current value of `\tau`, or
2. code the boundary reset map at `\tau=0` and transport the resulting
   countdown carrier.

This is the cleanest restatement of the live proof fork.

---

## 2. What is now formal, and what remains genuinely D5-specific

### Lemma 2.1 (countdown off the boundary) [F]
If `\tau(x)>0`, then
\[
\tau(Fx)=\tau(x)-1.
\]

#### Proof
By definition, `\tau(x)` is the length of the initial flat prefix of the future
`dn` sequence at `x`. If `\tau(x)>0`, then `dn_0(x)=\delta_{\mathrm{flat}}`, and
shifting the future sequence forward decreases the flat-prefix length by one.
∎

So the real D5 content is no longer the decrement law. The remaining theorem
content is concentrated at the boundary:
- the `\tau=0` reset law closes on small current quotients;
- those quotients remain exact on the tested odd range through `m=19`;
- the reset images are restricted to the explicit three-point sets above.

That is the proof-side simplification produced by `048/050`.

---

## 3. Boundary exactness and minimality

### Proposition F (boundary exactness on minimal theorem-side coordinates) [C]
On the tested range, the full next-`\tau` map is exact on
\[
(\tau,\epsilon_4,s,u,v,\lambda).
\]
At the boundary `\tau=0`, no smaller current `B`-subset together with
`\epsilon_4` is exact for the full reset map. Equivalently, the checked minimal
exact current quotient for boundary next-`\tau` is size four:
\[
\{s,u,v,\lambda\}.
\]

### Proposition G (branchwise boundary minimality) [C]
On the tested range:
- on the `carry_jump` branch, next-`\tau` is exact on `(s,v,\lambda)`;
- on the `other` branch, next-`\tau` is exact on `(s,u,\lambda)`;
- `wrap` resets identically to `0`.

These branchwise quotients are already minimal on the tested range for the
corresponding boundary pieces.

This is the smallest honest current-state reset description known on the
minimal theorem-side object.

---

## 4. The first real lower-bound statement

### Proposition H (persistent witness family) [C]
For every tested odd modulus
\[
m\in\{5,7,9,11,13,15,17,19\},
\]
the active branch contains the pair
\[
x^-_m=(m-2,2,1,2,0),
\qquad
x^+_m=(m-1,2,1,2,0),
\]
with common grouped base
\[
B_*=(3,1,2,0,\mathrm{regular}),
\]
common current event label
\[
\epsilon_4=\mathrm{flat},
\]
but opposite carry labels:
\[
c(x^-_m)=0,
\qquad
c(x^+_m)=1.
\]
The same pair has
\[
\tau(x^-_m)=m-3,
\qquad
\tau(x^+_m)=m-4,
\]
and common future flat/nonflat prefix length `m-5`.

Consequently, for every tested modulus `m`, any coding that sees only current
`B`, current `\epsilon_4`, and the next `h<m-4` future flat/nonflat bits fails
on that modulus.

### Corollary I (conditional no fixed bounded horizon) [H]
If the witness family of Proposition H persists for all odd `m\ge 5`, then no
fixed bounded future horizon can code the carry sheet uniformly in odd `m`.

This is the first theorem-shaped no-go direction stronger than the raw catalog
negative from `045`.

---

## 5. Where the stronger source-residue refinement fits

The checked constructive refinement is real:
\[
\rho=u_{\mathrm{source}}+1\pmod m.
\]
On the tested range through `m=19`:
- `\tau` is exact on `(s,u,v,\lambda,\rho)`;
- `\tau'` is exact on `(s,u,\lambda,\rho,\epsilon_4)`;
- `c` is exact on `(u,\rho,\epsilon_4)`;
- checked raw bridge:
  \[
  q\equiv u-\rho + \mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
  \]

But this should remain a **constructive remark**, not a theorem-object change.
For tested `m\ge 7`, `\rho` is not recoverable from `(B,\tau,\epsilon_4)`, so
it is not an equivalent reparametrization of the minimal cover.

The clean split therefore remains:
- **proof**: stay on `(B,\tau,\epsilon_4)`;
- **constructive compute**: exploit `(B,\rho)` if it helps.

---

## 6. The next proof targets

### Target T1 (uniform boundary reset theorem) [H]
Prove, for every odd `m\ge 5` on the active best-seed branch, that
\[
R(\epsilon_4,s,u,v,\lambda)=
\begin{cases}
0, & \epsilon_4=\mathrm{wrap},\\
R_{\mathrm{cj}}(s,v,\lambda), & \epsilon_4=\mathrm{carry\_jump},\\
R_{\mathrm{oth}}(s,u,\lambda), & \epsilon_4=\mathrm{other},
\end{cases}
\]
with exact image sets
\[
\mathrm{Im}(R_{\mathrm{cj}})=\{0,1,m-2\},
\qquad
\mathrm{Im}(R_{\mathrm{oth}})=\{0,m-4,m-3\}.
\]

This is the cleanest uniform theorem now in reach.

### Target T2 (uniform anticipation/carrier theorem) [H]
Prove that on every odd `m\ge 5` on the same branch:
1. `c` is a one-sided anticipation datum on the grouped base;
2. `\tau` is its exact countdown carrier;
3. all boundary ambiguity is encoded by `\epsilon_4` and the reset law above.

This is the manuscript-level D5 analogue of the d3/d4 odometer statements.

### Target T3 (reduction-lemma no-go) [O]
Prove that the intended admissible/local mechanism class collapses to bounded
transition/reset data of depth `h`. Once such a reduction lemma exists,
Proposition H gives the contradiction for all sufficiently large odd `m`.

At this point the missing proof ingredient is not more witness families. It is
that reduction lemma.

---

## 7. Best manuscript framing now

The stable D5 proof narrative is:

1. finite-cover normal form
   \[
   B \leftarrow B+c \leftarrow B+c+d;
   \]
2. carry is not current grouped data but a future-side anticipation datum;
3. that anticipation datum is a countdown carrier with a tiny boundary reset
   law;
4. therefore the unresolved issue is now precise:
   - either prove an admissible/local coding theorem for the countdown carrier,
   - or prove that the intended local class cannot code it.

That is the right d5 generalization language:
- `d=3`: odometer return map;
- `d=4`: affine / second-return odometer;
- `d=5`: grouped skew-odometer base plus one-sided anticipation carrier and a
  tiny finite cover.

---

## 8. Immediate proof tasks

### P1
Promote Theorems B/D and Proposition C into manuscript propositions with the
explicit status split:
- `046` = conceptual theorem;
- `047` = boundary sharpening;
- `048/050` = countdown/reset theorem with exact tested reset-value sets.

### P2
Insert Proposition H early in the proof narrative as the first serious no-go
statement. It is sharper and more explanatory than the raw catalog negative
from `045`.

### P3
Search for symbolic formulas for `R_{\mathrm{cj}}` and `R_{\mathrm{oth}}`, but keep
those formulas **out of the theorem statement** until they are proved. The
current theorem-level object only needs exact dependence and exact image sets.

### P4
Only after P1--P3, attempt the reduction lemma for the intended admissible/local
class.
