# D5 bridge theorem 075 — the boundary odometer bridge

## Scope actually used

I used the theorem-side structural chain package through the phase-corner theorem,
together with the `075` bridge request and handoff. In particular, the proof
below uses only:

- the `062` return-map / first-exit structure on the section `Theta = 2`;
- the `069` phase-corner scheduler;
- the `070` chain-first reduction;
- the `071` marked-chain normalization.

I also reran one small support pass on the saved frozen `047` data, but only
for the final checked-support section.

What is **proved** here:

1. the accessible union of full regular carry-to-wrap chains has a canonical
   **boundary label**
   \[
   \delta = q + m\sigma \in \mathbb Z / m^2 \mathbb Z,
   \]
   attached to each full chain;
2. this gives a canonical **partial exact global quotient**
   \((\beta,\delta)\) on that union;
3. current `epsilon4` factors **exactly** through \((\beta,\delta)\) with an
   explicit readout derived from the phase-corner scheduler;
4. if one asks for a **total splice-closed** bridge, then the only possible
   nonempty boundary subset is the **full** odometer \(\mathbb Z/m^2\mathbb Z\);
5. on that symbolic full bridge, the boundary right-congruence is trivial, so
   no smaller deterministic exact bridge exists.

What still depends on checked support:

- whether a given accessible regular union actually realizes a total splice-closed
  component rather than only a partial interval of the odometer;
- full accessibility of every boundary state for every odd `m`.

So the bridge theorem itself is now solved at the exact-quotient level. The
remaining uncertainty is only about **realized accessibility**, not about the
shape of the bridge object.

---

## 1. Structural setup

Work on the regular active branch, and write the theorem-side phase as `Theta`.
Set
\[
\beta := -\Theta \pmod m.
\]
By the phase-corner theorem, along every full regular carry-to-wrap block the
values of `beta` are exactly
\[
m-1,\ m-2,\ \dots,\ 1,\ 0
\]
in order, with

- `beta = m-1` at `carry_jump`,
- `beta = 0` at `wrap`.

So every full regular block is a length-`m` marked chain in the already-settled
coarse coordinate `beta`.

Now use the `Theta = 2` section
\[
\Sigma_2 := \{\Theta = 2\}.
\]
The `062/070` structural package gives the return map on `Sigma_2`
\[
T(q,w) = (q+1,\ w + \mathbf 1_{\{q=m-1\}}).
\tag{1.1}
\]
Equivalently, if
\[
\rho := u_{\mathrm{source}}+1,
\qquad
\sigma := w+\rho-1 \equiv source_u + w \pmod m,
\]
then the same return map is
\[
T(q,\sigma) = (q+1,\ \sigma + \mathbf 1_{\{q=m-1\}})
\pmod m.
\tag{1.2}
\]
This is already the base-`m` odometer law on the two digits `(q,sigma)`.

### Definition 1.1 (boundary label of a full chain)

Let `C` be a full regular carry-to-wrap chain. It has a unique state
`y_C \in C` with `Theta = 2`, equivalently `beta = m-2`.
Let
\[
(q(C), w(C))
\]
be the lifted coordinates of `y_C`, and set
\[
\sigma(C) := w(C) + \rho(C) - 1 \equiv source_u(C) + w(C) \pmod m.
\]
The **boundary label** of `C` is
\[
\delta(C) := q(C) + m\sigma(C) \pmod{m^2}.
\tag{1.3}
\]

This is canonical: each full chain contains exactly one `Theta = 2` state.

### Lemma 1.2 (boundary successor)

If `C -> C^+` is a splice from one full regular chain to the next full regular
chain, then
\[
\delta(C^+) = \delta(C) + 1 \pmod{m^2}.
\tag{1.4}
\]

#### Proof

By construction, the `Theta = 2` states of successive full chains are related by
exactly one application of the return map `T`. Formula `(1.2)` says that the
base-`m` digits update by
\[
(q,\sigma) \mapsto (q+1,\ \sigma + \mathbf 1_{\{q=m-1\}}),
\]
which is precisely
\[
q + m\sigma \mapsto q + 1 + m\Bigl(\sigma + \mathbf 1_{\{q=m-1\}}\Bigr)
\equiv \delta + 1 \pmod{m^2}.
\]
So `delta` increments by one at each full-chain splice. ∎

---

## 2. The exact bridge on the union of full regular chains

Let
\[
U^{\mathrm{full}}_{\mathrm{reg}}
\]
be the union of all full regular carry-to-wrap chains in the accessible regular
object.
For `x \in U^{full}_{reg}`, let `C(x)` be the unique full chain containing `x`.
Define
\[
\pi(x) := \bigl(\beta(x),\ \delta(C(x))\bigr).
\tag{2.1}
\]

### Theorem 2.1 (canonical boundary-odometer bridge)

The map `pi` is a canonical **partial deterministic quotient** on
\(U^{full}_{reg}\) with successor law
\[
(\beta,\delta) \mapsto (\beta-1,\delta)
\qquad (\beta>0),
\tag{2.2}
\]
and, whenever the current full chain is followed by another full regular chain,
\[
(0,\delta) \mapsto (m-1,\delta+1).
\tag{2.3}
\]
So the per-chain exact quotients glue to one global bridge whose extra state is
exactly the boundary odometer `delta`.

#### Proof

Inside a fixed full chain, `delta(C(x))` is constant by definition, while the
phase-corner theorem gives `beta -> beta-1`. That proves `(2.2)`.

At `beta = 0`, the state is the `wrap` endpoint of the current full chain. If
that endpoint is followed by another full regular chain `C^+`, then the next
state has `beta = m-1`, and by Lemma `1.2` its chain label is
`delta(C^+) = delta(C)+1`. That proves `(2.3)`.

If no next full regular chain exists, then the quotient successor is simply left
undefined at `(0,delta)`. Hence the bridge is canonical as a **partial** exact
quotient on the actual union of full chains. ∎

### Remark 2.2

This is the exact bridge theorem at the quotient level.
The old coarse `beta` bridge is the projection
\[
(\beta,\delta) \mapsto \beta.
\]
The old static decorated object `(beta,a,b)` is not the bridge state; it is only
a readout of the bridge state, as made explicit below.

---

## 3. Exact factorization of current `epsilon4`

Write the base-`m` digits of `delta` as
\[
\delta \leftrightarrow (q,\sigma),
\qquad
q,\sigma \in \{0,\dots,m-1\}.
\]
Define the two boundary readout bits
\[
a(\delta) := \mathbf 1_{\{q=m-1\}},
\tag{3.1}
\]
\[
b(\delta) := \mathbf 1_{\{q+\sigma\equiv 1\pmod m\}}
\ \vee\
\bigl(\mathbf 1_{\{q=m-1\}} \wedge \mathbf 1_{\{\sigma\neq 1\}}\bigr).
\tag{3.2}
\]
These are exactly the old `073/074` decoration bits, now read from `delta`.

### Lemma 3.1 (the two special post-carry events)

For a full chain with boundary digits `(q,sigma)`, the current event on that
chain is:

- at `beta = m-2`: `other_1000` iff `q = m-1`;
- at `beta = m-3`: `other_0010` iff
  \[
  q+\sigma \equiv 1 \pmod m
  \quad\text{or}\quad
  (q=m-1\ \&\ \sigma\neq 1).
  \]

#### Proof

Let `y_C` be the unique `Theta = 2` state of the chain, so `beta(y_C)=m-2` and
its boundary digits are exactly `(q,sigma)`.

On `Theta = 2`, the structural theorem gives
\[
u = q + \rho,
\qquad \rho = u_{\mathrm{source}}+1.
\tag{3.3}
\]
Hence at `y_C`
\[
s = w+u = w + q + \rho = q + (w+\rho-1) + 1 = q + \sigma + 1.
\tag{3.4}
\]
Also the carry bit is
\[
c = \mathbf 1_{\{q=m-1\}}.
\tag{3.5}
\]

At `beta = m-2`, the phase-corner scheduler says
`other_1000` occurs iff `c=1`. By `(3.5)`, this is exactly `q=m-1`.

Now move one step forward to `F(y_C)`, the `beta = m-3` state.

- If `q < m-1`, then the phase-`2` step does **not** increment `w`, so `c=0`
  and `s` stays equal to `q+sigma+1`.
  The scheduler at `beta=m-3` says `other_0010` iff `c=0` and `s=2`, i.e.
  iff
  \[
  q+\sigma+1 \equiv 2 \pmod m,
  \]
  equivalently `q+sigma \equiv 1`.

- If `q = m-1`, then the phase-`2` step increments `w` once, so `c=1` and
  \[
  s = (q+\sigma+1)+1 \equiv \sigma+1 \pmod m.
  \]
  The scheduler says `other_0010` iff `c=1` and `s \neq 2`, i.e. iff
  `sigma+1 \neq 2`, equivalently `sigma \neq 1`.

Combining the two cases gives the formula. ∎

### Theorem 3.2 (exact `epsilon4` readout)

Current `epsilon4` factors exactly through `(beta,delta)` by the rule
\[
\bar\epsilon_4(\beta,\delta)=
\begin{cases}
\mathrm{carry\_jump}, & \beta=m-1,\\[1mm]
\mathrm{wrap}, & \beta=0,\\[1mm]
\mathrm{other}_{1000}, & \beta=m-2 \text{ and } a(\delta)=1,\\[1mm]
\mathrm{other}_{0010}, & \beta=m-3 \text{ and } b(\delta)=1,\\[1mm]
\mathrm{flat}, & \text{otherwise.}
\end{cases}
\tag{3.6}
\]

#### Proof

`carry_jump` and `wrap` are already the distinguished positions `beta=m-1` and
`beta=0` from the phase-corner theorem.
The two early post-carry positions are exactly Lemma `3.1`.
All remaining positions are flat by the same scheduler. ∎

### Corollary 3.3

The old static decoration `(beta,a,b)` is a quotient of the true bridge state:
\[
(\beta,\delta) \mapsto (\beta,a(\delta),b(\delta)).
\]
It remains a correct current-event readout, but it is **not** the splice state.

---

## 4. How the accessible subset `A` enters

The right way to package `A` is now clear.

### Definition 4.1

For any chosen union `U` of full regular chains, let
\[
B(U) := \{\delta(C): C \subseteq U \text{ is a full regular chain}\}
\subseteq \mathbb Z/m^2\mathbb Z.
\tag{4.1}
\]
Then the bridge of Theorem `2.1` lands in
\[
Q_{B(U)} := \{0,1,\dots,m-1\} \times B(U).
\]

This bridge is always **partial** on the actual union of full chains.
The only possible failure of totality is at `beta=0`, when the next state after
`wrap` is not the start of another full regular chain in the chosen union.

### Proposition 4.2 (totalization criterion)

If `U` is splice-closed at the full-chain level — meaning every full chain in
`U` is followed at `wrap` by another full chain of `U` — then `A:=B(U)` is
forward-invariant under
\[
\delta \mapsto \delta+1,
\tag{4.2}
\]
and the bridge on
\[
Q_A = \{0,\dots,m-1\}\times A
\]
is a **total** deterministic exact quotient.

Conversely, any total bridge of this boundary-odometer form arises from such a
splice-closed full-chain union.

#### Proof

Forward invariance is exactly Lemma `1.2`: whenever the next full chain exists
inside `U`, its boundary label is `delta+1`. That makes the quotient successor
`(0,delta) -> (m-1,delta+1)` total on `Q_A`. The converse is immediate from the
meaning of totality at `beta=0`. ∎

### Corollary 4.3 (there is no proper nonempty splice-invariant boundary subset)

Let
\[
A \subseteq \mathbb Z/m^2\mathbb Z
\]
be nonempty and forward-invariant under `delta -> delta+1`.
Then
\[
A = \mathbb Z/m^2\mathbb Z.
\tag{4.3}
\]

#### Proof

Starting from any `delta_0 \in A`, forward invariance puts every iterate
`delta_0+n` in `A`. But `+1` generates the whole cyclic group
`\mathbb Z/m^2\mathbb Z`, so the forward orbit of `delta_0` is all of
`\mathbb Z/m^2\mathbb Z`. Hence `A` is the whole group. ∎

### Consequence 4.4

This resolves the `A` issue sharply:

- on an arbitrary accessible regular union, the bridge is canonically a
  **partial** boundary odometer;
- on any **total splice-closed** nonempty component, the boundary set is not a
  mysterious smaller subset — it is automatically the **full** odometer
  `Z/m^2`;
- therefore the only remaining accessibility question is whether the actual
  regular union closes up to a total component, not which proper invariant
  subset might occur.

So the correct distinction is:

1. **symbolic bridge object:** always the full boundary odometer;
2. **actual realized regular union:** may give only a partial interval of that
   odometer unless total splice-closure is proved.

---

## 5. Minimality: no smaller exact bridge on the total object

The bridge theorem above proves existence. One can also prove the exact
minimality statement on the symbolic total bridge.

### Proposition 5.1 (boundary right-congruence is trivial)

On the symbolic boundary odometer `delta -> delta+1`, the future bit word
\[
\Lambda(\delta) := \bigl(a(\delta+n),\ b(\delta+n)\bigr)_{n\ge 0}
\tag{5.1}
\]
determines `delta` uniquely.

#### Proof

Write `delta \leftrightarrow (q,sigma)`.

First recover `q`.
The bit `a(delta+n)` equals `1` exactly when the low digit is `m-1`.
So the first index `r` with `a(delta+r)=1` is
\[
r = m-1-q.
\]
Hence `q = m-1-r`.

Now recover `sigma`.
At that same index `r`, the low digit is already `m-1`, so by `(3.2)`
\[
b(\delta+r)=1 \iff \sigma\neq 1.
\]
Thus if `b(delta+r)=0`, then immediately `sigma=1`.

Assume now `b(delta+r)=1`, so `sigma\neq 1`.
After one more step the low digit wraps and the high digit increments:
\[
\delta+r+1 \leftrightarrow (0,\sigma+1).
\]
For the next `m-1` steps the high digit stays `sigma+1` while the low digit runs
through `0,1,\dots,m-2`.
On that segment, `b=1` exactly when
\[
t + (\sigma+1) \equiv 1 \pmod m.
\]
There is a unique such `t \in \{0,\dots,m-2\}`:
\[
t=0 \text{ if } \sigma=0,
\qquad
t=m-\sigma \text{ if } \sigma\in\{2,\dots,m-1\}.
\]
So the first post-wrap index where `b=1` recovers `sigma` uniquely.
Hence `(q,sigma)`, and therefore `delta`, is uniquely determined by the future
bit word `Lambda(delta)`. ∎

### Corollary 5.2 (minimal exact bridge)

On any nonempty total splice-closed component, every deterministic quotient that
is exact for current `epsilon4` must keep all `m^2` boundary states and all `m`
clock positions. Hence the smallest exact total bridge has exactly
\[
m^3
\tag{5.2}
\]
states, namely the full `(beta,delta)` bridge.

#### Proof

By Proposition `5.1`, distinct boundary states have distinct future decorated
block words, so no exact deterministic quotient can merge them.
Also, for a full bridge state `(beta,delta)`, the future current-event word
determines `beta`: the first occurrence of `wrap` is exactly `beta` steps ahead.
So distinct clock positions cannot be merged either. Therefore every exact total
bridge has at least `m*m^2 = m^3` states, and the bridge already constructed has
exactly that many. ∎

### Corollary 5.3 (precise obstruction to the old candidates)

The bare `beta` bridge is too coarse because it forgets both special post-carry
positions. The static decorated bridge `(beta,a,b)` is still too coarse because
many distinct `delta` share the same current decoration but have different
future splice behavior.

So the exact global obstruction is not “no bridge exists.” It is:

> **the bridge exists, but the full boundary odometer state is forced.**

---

## 6. Checked support from the frozen `047` data

I reran a small pass on the saved frozen regular rows only to confirm the
abstract formulas on the checked moduli `m=5,7,9,11`.

Summary:

| `m` | full regular chains | splice checks | splice failures | event-readout failures | observed boundary pairs |
|---|---:|---:|---:|---:|---:|
| 5  | 27  | 24  | 0 | 0 | 23 / 25 |
| 7  | 135 | 130 | 0 | 0 | 49 / 49 |
| 9  | 371 | 364 | 0 | 0 | 81 / 81 |
| 11 | 783 | 774 | 0 | 0 | 121 / 121 |

More concretely:

- the splice law `delta -> delta+1` had zero failures on every observed
  full-chain splice in the frozen data;
- the exact current-event readout `(3.6)` had zero failures on every observed
  state in those extracted full chains;
- for `m=7,9,11`, the union of observed full regular chains realizes the whole
  symbolic boundary set `Z/m^2`;
- for `m=5`, the frozen sample misses exactly the two pairs `(q,sigma)=(4,0)`
  and `(4,2)`.

This checked support is consistent with the theorem above.
In particular, Corollary `4.3` shows that the `m=5` deficit cannot represent a
proper nonempty splice-invariant symbolic subset. It can only mean either:

1. the frozen sample is incomplete, or
2. the saved full-chain union is not yet a total splice-closed component.

That is exactly the right remaining uncertainty.

---

## 7. What is proved, and what remains open

### Proved here

- The per-chain exact quotients do glue into one canonical global object.
- The correct exact global object is the **boundary odometer bridge**
  `(beta,delta)` with `delta = q + m sigma`.
- On the actual accessible union of full regular chains, this bridge is a
  canonical **partial exact quotient**.
- Current `epsilon4` factors exactly through `(beta,delta)` by the explicit rule
  `(3.6)`.
- Any nonempty **total splice-closed** bridge component must use the full
  boundary set `Z/m^2`.
- On that total symbolic bridge, the right-congruence is trivial, so the bridge
  is minimal and has `m^3` states.

### Still open after this note

- Whether the actual accessible regular union is total splice-closed for every
  odd `m`, or only partial on some components.
- Equivalently: whether every boundary state is actually realized in the true
  accessible regular union for every odd `m`.
- The realization/integration question downstream of this bridge theorem.

These are no longer bridge-existence problems. They are accessibility and
realization problems **relative to the solved bridge object**.

---

## Bottom line

Researcher 1 conclusion for the `075` bridge request:

> The bridge theorem is positive.
> The exact global bridge on the accessible union of full regular chains is the
> canonical boundary odometer
> \[(\beta,\delta),\qquad \delta = q + m\sigma \pmod{m^2}.\]
> Inside a chain, `beta` decreases and `delta` is fixed; at a full-chain splice,
> `delta -> delta+1`.
> Current `epsilon4` factors exactly through this bridge.
>
> If one asks for a nonempty **total** splice-closed exact bridge, then there is
> no smaller accessible subset `A`: necessarily `A = Z/m^2`, and the minimal
> exact total bridge has `m^3` states.

So the live frontier is no longer “does the bridge exist?” and no longer “which
proper invariant subset `A` should we pick?”
It is only:

> does the actual accessible regular union realize the full symbolic boundary
> odometer, or only a partial interval of it, and how does realization descend
> from that now-fixed bridge object?
