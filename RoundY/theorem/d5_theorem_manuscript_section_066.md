# D5 theorem/manuscript section 066: the active branch as a one-corner odometer

This note turns the current theorem route into a manuscript-ready section.
It follows the concentrated handoff 065 exactly in spirit:

- the theorem object stays minimal,
- the constructive source-residue route is separated into a later remark,
- the phase-corner theorem is the conceptual center,
- and the branchwise reset formulas are corollaries, not primary theorems.

Throughout, fix an odd modulus `m >= 5` and the best seed
`left = [2,2,1]`, `right = [1,4,4]`.
We work on the active nonterminal branch of the unresolved best-seed channel
`R1 -> H_L1`.

## 1. The theorem object and auxiliary coordinates

The theorem object is

- `B = (s,u,v,layer,family)`,
- `tau`,
- `epsilon4`.

The auxiliary current coordinates are
\[
(q,w,u,\lambda),\qquad s=w+u \pmod m,
\]
and the auxiliary proof phase is
\[
\kappa := q+s+v+\lambda \pmod m.
\]
We also write
\[
c := \mathbf 1_{\{q=m-1\}}.
\]

The coordinates `rho`, `alpha`, `delta`, and `beta` are deliberately *not*
part of the theorem statement. They belong to the constructive route and may be
used only in remarks or auxiliary proofs.

## 2. Structural input from the earlier branch

The following ingredients are imported from the earlier structural analysis.
In a manuscript, they should already have been proved before the present
section.

### Proposition 2.1 (explicit trigger family)
The target hole family for the unresolved channel is
\[
H_{L1} = \{(q,w,u,\lambda)=(m-1,m-1,u,2): u\neq 2\}.
\]

### Proposition 2.2 (universal first-exit targets)
Let the active branch start from the alternate-`2` entry out of `R1`.
Then the first exit to `H_{L1}` occurs at exactly one of the two states
\[
T_{\mathrm{reg}}=(m-1,m-2,1),
\qquad
T_{\mathrm{exc}}=(m-2,m-1,1),
\]
with the regular source families exiting at `T_reg` and the exceptional source
family exiting at `T_exc`.

The proof from the earlier section uses the phase-`1` source-residue invariant
\[
q \equiv u-\rho+1 \pmod m,
\qquad \rho=u_{\mathrm{source}}+1,
\]
and the explicit trigger family in Proposition 2.1.

### Proposition 2.3 (pre-exit B-region invariance)
Every active nonterminal current state is `B`-labelled.
Equivalently, the active nonterminal branch stays entirely inside the
unmodified `B`-region of the mixed witness.

This follows by the bootstrap contradiction proved earlier: every modified
current class lies at or beyond the cross-section index of first exit, whereas
all nonterminal active states lie strictly before first exit.

## 3. Current-state scheduler on the active branch

The central theorem of the section is that once the branch is known to stay in
`B`, the active dynamics are simply the mixed witness scheduler written in the
current phase coordinate `kappa`.

### Theorem 3.1 (phase-corner theorem)
On the active nonterminal branch, let
\[
\kappa=q+s+v+\lambda \pmod m,
\qquad
c=\mathbf 1_{\{q=m-1\}}.
\]
Then the following hold.

1. **Clock law.**
   \[
   \kappa' = \kappa+1 \pmod m.
   \]

2. **Current-event scheduler.**
   The current grouped event `epsilon4` is determined by `kappa`, the carry bit
   `c`, and the single corner condition `s=2`:
   \[
   \kappa=0 \Rightarrow \epsilon_4=\mathrm{wrap},
   \]
   \[
   \kappa=1 \Rightarrow \epsilon_4=\mathrm{carry\_jump},
   \]
   \[
   \kappa=2 \Rightarrow
   \begin{cases}
   \epsilon_4=\mathrm{other}_{1000},& c=1,\\
   \epsilon_4=\mathrm{flat},& c=0,
   \end{cases}
   \]
   \[
   \kappa=3 \Rightarrow
   \begin{cases}
   \epsilon_4=\mathrm{other}_{0010},& (c=0 \text{ and } s=2) \text{ or } (c=1 \text{ and } s\neq 2),\\
   \epsilon_4=\mathrm{flat},& \text{otherwise},
   \end{cases}
   \]
   and for every
   \[
   4\le \kappa\le m-1,
   \]
   one has
   \[
   \epsilon_4=\mathrm{flat}.
   \]

3. **One-corner law.**
   Among flat states, the only short reset occurs at the corner
   \[
   (\kappa,s)=(2,2).
   \]

Equivalently, the active best-seed branch is an odometer with one corner.

#### Proof
By Proposition 2.3, every active nonterminal current state is `B`-labelled, so
its outgoing direction is exactly the unmodified mixed witness direction.

For color `0`, the mixed witness uses the following current anchor table.

- At layer bucket `0`, use anchor `1`.
- At layer bucket `1`, use anchor `4`.
- At layer bucket `2`, use the old-bit orientation `0/2`, where the old bit is
  exactly `c=1_{q=m-1}`.
- At layer bucket `3`, use the predecessor switch governed by
  `pred_sig1_wu2`.
- At layer buckets `4,\dots,m-1`, use anchor `0`.

Because
\[
\kappa=q+s+v+\lambda=q+w+u+v+\lambda=\sum_{i=0}^4 x_i \pmod m,
\]
this layer bucket is exactly the current value of `kappa`.
Every anchor increases the coordinate sum by one, hence
\[
\kappa'=\kappa+1 \pmod m.
\]
This proves the clock law.

Now translate the witness anchors into grouped events.

- Anchor `1` increments `q`, hence gives `wrap`.
- Anchor `4` increments `u`, hence gives `carry_jump`.
- At `kappa=2`, the old-bit rule chooses anchor `2` exactly when `c=1`, and
  otherwise anchor `0`. Thus one gets `other_1000` when `c=1`, and `flat`
  otherwise.
- At `kappa=3`, the predecessor flag `pred_sig1_wu2` is equivalent to `s=2` on
  the active branch, so the witness chooses anchor `3` exactly in the two cases
  `(c=0 and s=2)` or `(c=1 and s\neq 2)`, and anchor `0` otherwise. This gives
  the stated `other_0010` versus `flat` dichotomy.
- For `kappa\ge 4`, the witness uses anchor `0`, hence the event is always
  flat.

This proves the scheduler.

Finally, among flat states the only departure from the pure cyclic odometer
countdown occurs when the scheduler reaches `kappa=3` and the predecessor test
fires with `c=0`, which is exactly the corner `s=2` seen one step earlier at
`(kappa,s)=(2,2)`. Thus the only short reset on the flat branch occurs at that
single corner. ∎

## 4. Countdown and reset corollaries

The theorem above should now be used to derive all reset laws, rather than
stating them independently.

### Corollary 4.1 (countdown law)
Define `tau` on the active branch by

- `tau = 0` on nonflat states,
- on flat states,
  \[
  \tau=
  \begin{cases}
  1,& (\kappa,s)=(2,2),\\
  m-\kappa,& \text{otherwise}.
  \end{cases}
  \]

Then
\[
\tau' = \tau-1 \qquad (\tau>0).
\]

#### Proof
If the current state is nonflat, then by definition `tau=0`.
Assume the state is flat. By Theorem 3.1, the event remains flat at every
subsequent phase until the scheduler next reaches a nonflat bucket, except at
one exceptional short corner. If `(kappa,s)=(2,2)`, then the very next event is
`other_0010`, so `tau=1`. Otherwise the next nonflat phase occurs after exactly
`m-kappa` steps. Hence the stated formula, and the decrement law follows
immediately. ∎

### Corollary 4.2 (CJ reset formula)
On a carry-jump state,
\[
R_{\mathrm{cj}}=
\begin{cases}
0,& s+v+\lambda\equiv 2 \pmod m,\\
1,& s=1 \text{ and } s+v+\lambda\not\equiv 2 \pmod m,\\
m-2,& \text{otherwise}.
\end{cases}
\]

#### Proof
A carry-jump state has `kappa=1` by Theorem 3.1. Therefore
\[
q\equiv 1-s-v-\lambda \pmod m.
\]
The zero-reset fiber is exactly `q=m-1`, equivalently `s+v+lambda ≡ 2 (mod m)`.
If `q\neq m-1`, then the successor is flat at phase `kappa=2`. The only short
flat reset occurs at the corner `(kappa,s)=(2,2)`, which here is equivalent to
`s=1` before the jump. Thus the reset is `1` when `s=1`, and `m-2` otherwise. ∎

### Corollary 4.3 (OTH reset formulas)
For the two `other` branches one has
\[
(1,0,0,0)\mapsto
\begin{cases}
m-3,& s=1,\\
0,& s\neq 1,
\end{cases}
\qquad
(0,0,1,0)\mapsto m-4.
\]

#### Proof
The event `other_1000` occurs at `kappa=2` and necessarily has `c=1` by Theorem
3.1. Its successor lies at `kappa=3`. If `s=1`, then the successor is flat and
its next nonflat event occurs after `m-3` steps; otherwise the successor is
already on the boundary reset and the value is `0`.

The event `other_0010` occurs at `kappa=3`. Its successor lies at `kappa=4`,
which is always flat by Theorem 3.1, so the next nonflat event occurs after
exactly `m-4` steps. ∎

### Corollary 4.4 (finite-cover compatibility)
The phase-corner machine is compatible with the finite-cover chain
\[
B \leftarrow B+c \leftarrow B+c+d,
\]
where
\[
c=\mathbf 1_{\{q=m-1\}},
\qquad
d=\mathbf 1_{\{\text{next carry }u\ge m-3\}}.
\]

#### Proof
The carry sheet `c` is exactly the extra current datum appearing in the phase
scheduler. The residual binary sheet `d` records the anticipation side of the
next carry along the regular noncarry branch. Since the scheduler determines
all nonflat events and the countdown law determines the flat stretches, the
finite-cover description and the phase-corner description encode the same
active machine. ∎

## 5. How the structural proof spine feeds the theorem

For the manuscript, the logical flow should be written in the following order.

1. **Exact trigger family.** Prove Proposition 2.1.
2. **Universal first-exit targets.** Use the phase-`1` source-residue invariant
   to prove Proposition 2.2.
3. **Pre-exit B-region invariance.** Use the bootstrap contradiction to prove
   Proposition 2.3.
4. **Phase-corner theorem.** Apply the mixed witness rule on current `B`-states
   to prove Theorem 3.1.
5. **Reset corollaries.** Derive countdown and reset laws from the theorem.

This avoids the older branch-by-branch organization in which `CJ` and `OTH`
looked like separate mysteries.

## 6. Placement of the constructive and negative routes

The constructive source-residue route should come *after* the theorem section,
as a remark or later section.

### Remark 6.1 (constructive cyclic controller)
On the constructive route one may introduce
\[
\rho=u_{\mathrm{source}}+1,
\qquad
\alpha=\rho-u,
\qquad
\beta=\alpha-(s+v+\lambda)-J,
\]
where `J = 1_{epsilon4 = carry_jump}`. On the checked range, `beta` has unit
drift and determines `q`, `c`, `tau`, and `next_tau` from `(B,beta)`.
This is a stronger constructive refinement, not a change in the theorem object.

The negative bounded-quotient route should likewise be stated later, as an
independent obstruction theorem for any intended admissible/local realization
class.

## 7. Honest status to preserve in the manuscript

The theorem route is now close to closed in shape, but two kinds of honesty are
still important in the draft.

1. The main theorem object should remain `(B,tau,epsilon4)`.
   Auxiliary clocks such as `rho`, `alpha`, `delta`, `beta`, and `kappa`
   should be explicitly declared auxiliary.

2. The manuscript should distinguish between:
   - the theorem-side structural result: the active branch is a one-corner
     odometer;
   - the constructive open question: can the cyclic clock be realized locally;
   - the negative open question: can one prove that the intended local class
     cannot realize it except through an `m`-state carrier.

That separation is now one of the project’s main conceptual achievements.
