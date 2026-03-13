# D5 proof program after 049

## Guiding principle

The manuscript should stay centered on the **minimal theorem-side object**
\[
(B,\tau,\epsilon_4),
\qquad
B=(s,u,v,\lambda,f),
\]
not on the stronger checked constructive refinement
\[
(B,\rho),\qquad \rho=u_{\mathrm{source}}+1 \pmod m.
\]

The right conceptual order is:

1. finite-cover normal form (`044`),
2. carry as anticipation datum (`046`),
3. boundary sharpening (`047`),
4. countdown carrier law (`048`),
5. then either:
   - a positive admissible/local coding theorem for `tau`, or
   - a no-go theorem for the intended local mechanism class.

The stronger `rho` refinement should appear only as a remark / auxiliary constructive route.

---

## I. Main theorem-shaped target for D5

### Theorem T0 (D5 active anticipation normal form; theorem target)
For the best-seed unresolved channel
\[
R1 \to H_{L1}
\]
on odd moduli `m`, the active branch factors through a grouped skew-odometer base with a finite anticipation cover:
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
where
\[
B=(s,u,v,\lambda,f),
\qquad
c=\mathbf 1_{\{q=m-1\}},
\qquad
d=\mathbf 1_{\{U^+\ge m-3\}}.
\]
Moreover:

1. exceptional trigger descends to `B`;
2. regular trigger descends to `B+c`;
3. deterministic active evolution closes on `B+c+d`;
4. the carry sheet `c` is not a current grouped-state observable, but a one-sided anticipation datum.

### Manuscript message
D5 is not a hidden transducer problem anymore. It is a grouped skew-odometer base plus a tiny anticipation cover.

---

## II. Conceptual core theorem

### Theorem T1 (carry as anticipation datum; conceptual theorem)
On the active branch, the carry sheet `c` is exactly determined by the first nonflat future grouped-transition event.
Equivalently, there exists a future-side coordinate pair
\[
(\tau,\eta)
\]
with
- `tau` = initial flat-run length for `dn=(0,0,0,1)`,
- `eta` = first nonflat grouped-delta event,

such that `c` is a function of
\[
(B,\tau,\eta).
\]
On the checked data, the minimal exact grouped-delta horizon is `m-3` and the minimal exact grouped-state horizon is `m-2`.

### Proof strategy
- Start from the grouped active branch and its exact future grouped-delta sequence.
- Show that the first nonflat event is the first place the grouped base distinguishes carry from noncarry.
- Use the explicit witness family from `s63` to show that smaller bounded horizons fail.

### What this theorem should *not* say
Do **not** make `min(\tau,8)` the conceptual theorem. That is checked-range evidence only. The canonical object is the anticipation datum `(\tau,\eta)`.

---

## III. Boundary sharpening and internal dynamics

### Theorem T2 (boundary sharpening)
All ambiguity in `B+tau` lies at the boundary `tau=0`.
At `tau=0`, the current event class is genuinely three-way:
\[
\{\mathrm{wrap},\ \mathrm{carry\_jump},\ \mathrm{other}\}.
\]
Thus the hidden future datum reduces to `tau` plus a tiny boundary correction `epsilon4`.

### Theorem T3 (countdown carrier law)
On the active nonterminal branch, `tau` is an exact countdown carrier:
\[
\tau' = \tau-1 \qquad (\tau>0).
\]
All nontrivial dynamics occur at `tau=0`, where the reset map is exact and piecewise current-state:
- `wrap -> 0`,
- `carry_jump` resets on `(s,v,\lambda)`,
- `other` resets on `(s,u,\lambda)`.

Equivalently, the next-`tau` map is exact on
\[
(\tau,\epsilon_4,s,u,v,\lambda),
\]
and no smaller `B`-subset with `epsilon4` is exact on the boundary.

### Manuscript message
The hidden future sheet is not an opaque window. It is a countdown carrier with a tiny reset law.

---

## IV. First serious no-go direction

### Proposition N0 (first carry-only no-go)
The first admissible current-edge / short-transition / low-cardinality gauge catalogs do not realize `c`.
This includes observables factoring through
\[
B,\qquad B\to B_{\mathrm{next}},\qquad B\to B_{\mathrm{next}}\to B_{\mathrm{next2}}.
\]

This is a useful obstruction, but it is still only a catalog no-go, not yet a theorem for a local mechanism class.

### Proposition N1 (bounded-horizon witness family)
For each checked odd modulus `m`, there are states
\[
x^-_m=(m-2,2,1,2,0),
\qquad
x^+_m=(m-1,2,1,2,0),
\]
with common grouped base
\[
B_*=(3,1,2,0,\mathrm{regular}),
\]
common boundary label `epsilon4 = flat`, but opposite carry labels,
\[
c(x^-_m)=0,
\qquad
c(x^+_m)=1,
\]
and anticipation times
\[
\tau(x^-_m)=m-3,
\qquad
\tau(x^+_m)=m-4.
\]
Hence any coding that sees only current `B`, current `epsilon4`, and the next `h<m-4` future flat/nonflat bits fails on modulus `m`.

### Intended theorem use
This is the first genuine lower-bound witness family. It should be the bridge to a real impossibility theorem once a reduction lemma is available.

---

## V. The exact proof fork

The proof problem is now well-posed.

### Positive route P
Prove an admissible/local coding theorem for the countdown carrier `tau`.
A sharper version is enough:
- code the reset law at `tau=0`, and
- provide an internal carrier that decrements by one away from the boundary.

This is stronger than coding `c` directly, but conceptually cleaner.

### Negative route N
Prove a reduction lemma showing that the intended admissible/local mechanism class collapses to bounded grouped transition/reset data. Then apply Proposition N1.

The missing ingredient here is **not** another witness pair. The missing ingredient is the reduction lemma.

---

## VI. How `rho` should appear in the paper

### Remark R (checked constructive refinement)
On the checked data, define
\[
\rho = u_{\mathrm{source}}+1 \pmod m.
\]
Then:
- `tau` is exact on `(s,u,v,layer,rho)`;
- `c` is exact on `(u,rho,epsilon4)`;
- checked relation:
  \[
  q \equiv u-\rho + \mathbf 1_{\{\epsilon_4=\mathrm{carry\_jump}\}} \pmod m.
  \]

### How to use this remark
- Use it as a **constructive refinement** and a bridge back to the earlier transport picture.
- Do **not** identify it with the minimal theorem-side object.
- Explicitly state that for checked `m>=7`, `rho` is not recoverable from `(B,tau,epsilon4)`.

This keeps the theorem language minimal while leaving open a stronger constructive proof route.

---

## VII. Best manuscript structure now

1. **Finite-cover normal form** (`044` with `043` input)
2. **First carry-only no-go** (`045`) as motivation only
3. **Carry as anticipation datum** (`046`) — conceptual center
4. **Boundary sharpening** (`047`) — boundary-only refinement
5. **Countdown carrier law** (`048`) — internal dynamics theorem
6. **Bounded-horizon witness family** (`047`/`048` follow-on)
7. **Open theorem**: admissible/local coding of the countdown carrier or no-go for the intended local class
8. **Remark**: source-residue refinement `rho`

This is the cleanest D3/D4/D5 narrative:
- D3: odometer return map,
- D4: affine / second-return odometer,
- D5: grouped skew-odometer base plus anticipation carrier and tiny finite cover.

---

## VIII. Smallest proof tasks that would unblock the paper

### Proof task A
Write the explicit reduction from `046 + 047 + 048` to a single reset-map problem:
\[
\tau' =
\begin{cases}
\tau-1, & \tau>0,\\
R(\epsilon_4,s,u,v,\lambda), & \tau=0.
\end{cases}
\]
This should become a proposition in the paper.

### Proof task B
Package Proposition N1 as a lower-bound statement for bounded future horizons. This is already theorem-shaped.

### Proof task C
Attempt the reduction lemma for the intended admissible/local class:
show that any such mechanism factors through bounded grouped transition/reset data of depth `h`.
This is the shortest road to a real impossibility theorem.

### Proof task D
If the compute branch finds an admissible realization of `rho`, write it only as a constructive corollary:
`rho` realizes the countdown carrier, but the theorem statement remains in terms of `(B, tau, epsilon4)`.

---

## IX. What I would try to prove next

The next statement I would actively try to prove is:

### Proposition P/N (next proof target)
On the active best-seed branch, the carry sheet is mediated by an exact countdown/reset carrier `tau` over the grouped base. Therefore any intended local/admissible realization of the carry mechanism must either:
1. realize the countdown carrier (or its reset law), or
2. transport an equivalent stronger refinement such as `rho`.

This is the right place to hold the proof line while compute explores both branches.
