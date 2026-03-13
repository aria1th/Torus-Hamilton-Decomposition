# D5 proof generalization after 049/050

## Scope

This note keeps the theorem side centered on the minimal object
\[
(B,\tau,\epsilon_4),
\qquad
B=(s,u,v,\lambda,f),
\]
and treats the source-residue coordinate
\[
\rho=u_{\mathrm{source}}+1 \pmod m
\]
only as a stronger constructive refinement.

The goal is to sharpen the **proof program** for odd-modulus D5 on the active
best-seed branch, not to change the theorem object.

The checked evidence splits into two ranges:
- the main theorem-chain objects from `044--048` are checked on
  \[
m=5,7,9,11,
  \]
- the `050` proof-support extensions (reset law and witness persistence) are checked on
  \[
m=5,7,9,11,13,15,17,19.
  \]

Status labels:
- **[C]** checked on the active best-seed branch on the tested odd moduli
- **[H]** theorem-shaped conjecture / proof target for all odd `m`
- **[O]** open

---

## 1. Minimal theorem-side object

Keep the manuscript on the future-side carrier:
\[
(B,\tau,\epsilon_4),
\]
where
- `B=(s,u,v,layer,family)` is the grouped base,
- `\tau` is the initial flat-run length for the grouped-delta event
  \(dn=(0,0,0,1)\),
- `\epsilon_4` is the current grouped-delta event class
  \(\{\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}\).

This is the right theorem object because:
- `044` already gives the finite-cover normal form,
- `046` identifies the carry mechanism as an anticipation datum,
- `047` shows the only ambiguity of `B+tau` sits at `tau=0`,
- `048` turns the anticipation datum into a countdown carrier with a tiny reset law,
- `050` shows the reset law and the lower-bound witness family persist through `m=19`.

The stronger refinement
\[
(B,\rho)
\]
should stay outside the main theorem chain. It is useful for compute and may
still become a constructive proof route, but it is **not** an equivalent
reparametrization of the minimal cover: for tested `m>=7`, `rho` is not
recoverable from \((B,\tau,\epsilon_4)\). [C]

---

## 2. Canonical theorem chain

### Theorem A (finite-cover normal form) [C -> H]
On the active best-seed branch, the checked structure factors as
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
with
\[
c=\mathbf 1_{\{q=m-1\}},
\qquad
d=\mathbf 1_{\{U^+\ge m-3\}}.
\]
Moreover:
1. exceptional trigger descends to `B`;
2. regular trigger descends to `B+c` but not to `B`;
3. deterministic active evolution closes on `B+c+d`.

This is the right D5 structural statement: a grouped skew-odometer base with
one trigger-level carry sheet and one residual binary anticipation sheet.
The finite-cover part itself is currently checked on \(m=5,7,9,11\).

### Theorem B (carry as anticipation datum) [C -> H]
The carry sheet `c` is not a current grouped-state observable. It is an exact
one-sided future grouped-transition datum.

The canonical future-side signature is
\[
(B,\tau,\eta),
\]
where `tau` is the initial flat-run length and `eta` is the first nonflat
future grouped-delta event.

Checked minimal exact horizons:
- future grouped-delta horizon: `m-3`,
- future grouped-state horizon: `m-2`.

This is the conceptual theorem from the current chain. The carry mechanism is
already a future-side event on the grouped base. The anticipation statement itself
is currently checked on \(m=5,7,9,11\).

### Theorem C (boundary sharpening) [C -> H]
All ambiguity of `B+tau` lies at `tau=0`.
At the boundary, the current event class is genuinely three-way:
\[
\{\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\}.
\]
Thus the canonical theorem-side quotient is
\[
(B,\tau,\epsilon_4),
\]
not the checked-range truncation `min(tau,8)`.

### Theorem D (countdown carrier law) [partly formal, partly C -> H]
Let
\[
\tau(x)=\max\{t\ge 0 : dn_j(x)=\delta_{\mathrm{flat}}\text{ for }0\le j<t\},
\qquad
\delta_{\mathrm{flat}}=(0,0,0,1).
\]
Then the countdown update away from the boundary is formal:
\[
\tau(Fx)=\tau(x)-1 \qquad \text{whenever } \tau(x)>0.
\]
So all nontrivial dynamics of `tau` are confined to the boundary `tau=0`.

On the extended tested range \(m=5,7,9,11,13,15,17,19\), the boundary reset law is exact on the same small
quotients:
- `wrap -> 0`,
- `carry_jump` exact on `(s,v,layer)`,
- `other` exact on `(s,u,layer)`.

Observed reset-value sets on the tested range:
\[
R_{\mathrm{carry\_jump}}\subseteq \{0,1,m-2\},
\qquad
R_{\mathrm{other}}\subseteq \{0,m-4,m-3\}.
\]
This is the real internal-dynamics theorem. The hidden future datum is not an
opaque window: it is a countdown carrier with a small reset micro-law.

### Corollary E (reduction to reset-law coding) [formal + C]
Once `c` is known to factor through \((B,\tau,\epsilon_4)\), and once `tau`
is known to satisfy the countdown law away from the boundary, any local /
admissible realization of the carry mechanism reduces to one of two proof
problems:
1. code the current value of `tau`, or
2. code the boundary reset map at `tau=0` and transport the resulting
   countdown carrier.

This is the cleanest statement of the current proof fork.

---

## 3. What is now genuinely formal

One part of `048` no longer needs to be treated as an experimental theorem.
It is built into the definition of the flat-run carrier.

### Lemma 3.1 (countdown off the boundary) [formal]
If `tau(x)>0`, then `dn_0(x)=delta_flat`, hence
\[
\tau(Fx)=\tau(x)-1.
\]

#### Proof
By definition, `tau(x)` is the length of the initial flat prefix of the future
`dn`-sequence at `x`. If `tau(x)>0`, the first event is flat and the remaining
flat prefix after one step has length exactly one less. ∎

So the computational content of `048/050` is **not** the decrement law itself.
The real content is:
- the boundary reset map closes on small current quotients, and
- those quotients remain exact through the extended tested range.

That makes the next proof target much narrower.

---

## 4. Lower-bound direction

### Proposition F (bounded-horizon witness family) [C -> H]
For each tested odd modulus `m`, the active branch contains the pair
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
The same pair has anticipation values
\[
\tau(x^-_m)=m-3,
\qquad
\tau(x^+_m)=m-4,
\]
and common future flat/nonflat prefix length `m-5`.

Consequently, any coding that sees only current `B`, current `epsilon4`, and
the next `h<m-4` future flat/nonflat bits fails on modulus `m`.

### Corollary G (no uniform fixed bounded horizon, conditional on persistence) [H]
If the witness family of Proposition F persists for all odd `m>=5`, then no
fixed bounded future horizon can code the carry sheet uniformly in odd `m`.

This is the first serious no-go direction for any theorem that tries to keep
`c` inside a bounded grouped-transition window independent of `m`.

---

## 5. Where 049 fits without changing the theorem object

The stronger current-state refinement is real and useful:
\[
\rho=u_{\mathrm{source}}+1 \pmod m.
\]
Through the tested range:
- `tau` is exact on `(s,u,v,layer,rho)`,
- `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
- `c` is exact on `(u,rho,epsilon4)`,
- checked raw relation:
  \[
  q \equiv u-\rho + \mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
  \]

This should be used only as a **constructive remark** or auxiliary route.
It does not replace the minimal theorem-side cover because, on the tested range
for `m>=7`, `rho` is not recoverable from \((B,\tau,\epsilon_4)\). [C]

So the clean split remains:
- proof: stay on `(B,tau,epsilon4)`,
- constructive compute: exploit `(B,rho)` if it helps.

---

## 6. Uniform odd-m proof targets

The next theorem-shaped statements worth proving are:

### Target T1 (uniform anticipation theorem) [H]
For every odd `m>=5` on the best-seed active branch, the carry sheet `c` is an
exact one-sided anticipation datum on the grouped base, with minimal future
`dn` horizon `m-3` and minimal future grouped-state horizon `m-2`.

### Target T2 (uniform countdown/reset theorem) [H]
For every odd `m>=5` on the same branch, the future-side carrier `tau` obeys
\[
\tau' = \tau-1 \qquad (\tau>0),
\]
and the boundary reset law closes exactly as
\[
R(\epsilon_4,s,u,v,\lambda)=
\begin{cases}
0, & \epsilon_4=\mathrm{wrap},\\
R_{\mathrm{cj}}(s,v,\lambda), & \epsilon_4=\mathrm{carry\_jump},\\
R_{\mathrm{oth}}(s,u,\lambda), & \epsilon_4=\mathrm{other}.
\end{cases}
\]
Moreover,
\[
R_{\mathrm{cj}} \subseteq \{0,1,m-2\},
\qquad
R_{\mathrm{oth}} \subseteq \{0,m-4,m-3\}.
\]

### Target T3 (uniform bounded-horizon obstruction) [H]
No theorem for the intended local/admissible mechanism class can reduce the
carry sheet to a fixed bounded future grouped-transition horizon independent of
`m`.

This is the proof-side negative target that matches the current witness family.

---

## 7. Proof routes

## Route P: positive countdown-carrier theorem
A clean positive proof would proceed in this order.

1. Prove the grouped active branch admits only the four current event classes
   \(\mathrm{flat},\mathrm{wrap},\mathrm{carry\_jump},\mathrm{other}\).
2. Define `tau` as the initial flat-prefix length.
3. Use Lemma 3.1 to get countdown away from the boundary for free.
4. Prove the boundary reset exactness on the theorem-side quotients:
   - wrap on the empty key,
   - carry_jump on `(s,v,layer)`,
   - other on `(s,u,layer)`.
5. Deduce that `c` is mediated by a countdown/reset carrier over the grouped
   base.

This is the cleanest D5 analogue of the d3/d4 odometer story: not just a cover,
but a grouped skew-odometer base plus a one-sided anticipation carrier.

## Route N: bounded-horizon / intended-class no-go
A clean negative proof would need a reduction lemma:

> every observable in the intended admissible/local mechanism class factors
> through bounded grouped transition/reset data of depth `h`.

Once such a lemma exists, Proposition F gives the contradiction for all
sufficiently large odd `m`.

At this point the missing ingredient is **not** another witness family. It is
that reduction lemma.

---

## 8. Best manuscript framing now

The most stable D5 theorem narrative is:

1. finite-cover normal form `B <- B+c <- B+c+d`;
2. carry is not current grouped data but a future-side anticipation datum;
3. the anticipation datum is a countdown carrier with a tiny reset law;
4. therefore the unresolved issue is precisely:
   - either prove an admissible/local coding theorem for the countdown carrier,
   - or prove that the intended local class cannot code it.

This keeps the paper aligned with the earlier dimensions:
- `d=3`: odometer return map,
- `d=4`: affine / second-return odometer,
- `d=5`: grouped skew-odometer base plus anticipation carrier and tiny finite
  cover.

---

## 9. Immediate proof tasks

### Task P1
Turn Theorems B/C/D into manuscript propositions with the precise status split:
- `046` is the conceptual theorem,
- `047` is boundary sharpening,
- `048/050` is the countdown/reset theorem with extended support.

### Task P2
Write Proposition F as the first real lower-bound statement in the paper.
This is more informative than the catalog no-go from `045`.

### Task P3
Prove or symbolically derive the boundary reset maps.
This is now the shortest route to a uniform odd-`m` theorem.

### Task P4
Only after that, attempt the reduction lemma for the intended
admissible/local class.

