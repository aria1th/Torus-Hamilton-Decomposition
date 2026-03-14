I can sharpen the clock route quite a bit.

The clean upgrade is this:

> **At the exact reduction level, clock descent is forced as soon as the intended quotient is an exact deterministic quotient for the current event (\epsilon_4) on the marked cycle.**

The reason is not mysterious carrier transport. It is that the phase-corner package already makes the short corner the **unique** state with two-step event signature
[
(\epsilon_4,\epsilon_4\circ T)=(\mathrm{flat},\mathrm{other}_{0010}),
]
and the canonical clock is just “time to the next occurrence of that corner,” in the gauge (\beta=-\kappa). The current D5 packaging already treats the phase-corner theorem as the main theorem, (\beta=-\kappa) as the canonical clock, and clock descent/realization as the live frontier, with chain-vs-cycle still the remaining reduction nuance.

## Formal theorem package

Let (X_m) be the exact active reduction object, with deterministic successor (T). For the cleanest theorem, take (X_m) to be a cyclic section of length (m); I will state the chain version afterward. The theorem-side package says the active branch is an odometer with one corner, with phase
[
\kappa=q+s+v+\mathrm{layer}\pmod m,
\qquad
\beta=-\kappa\pmod m,
]
and the special flat corner at ((\kappa,s)=(2,2)). It also packages the active event machine so that flat leaves to `wrap` only at (\kappa=m-1), to `other_{0010}` only at the corner ((\kappa,s)=(2,2)), and otherwise stays flat.

### Definition 1: exact event quotient

An **exact event quotient** of (X_m) is data
[
\pi:X_m\to Y_m,\qquad F:Y_m\to Y_m,\qquad E:Y_m\to\mathcal E
]
such that
[
F\circ \pi=\pi\circ T,
\qquad
E\circ \pi=\epsilon_4.
]

This is the right exactness notion for the clock route, because the theorem object includes (\epsilon_4), and the clock route is now explicitly about realizing the canonical (\beta) with exact readout of (\epsilon_4) and the other theorem-side observables.

### Lemma 2: short-corner detector

Let (x_\star\in X_m) be the theorem-side short corner, so
[
(\kappa(x_\star),s(x_\star))=(2,2).
]
Then (x_\star) is the unique state of (X_m) satisfying
[
(\epsilon_4(x),\epsilon_4(Tx))=(\mathrm{flat},\mathrm{other}_{0010}).
]

**Reason.** The packaged phase-corner scheduler says exactly:
[
\mathrm{flat}\to \mathrm{other}_{0010}
\iff
(\kappa,s)=(2,2),
]
while flat goes to wrap only at (\kappa=m-1), and otherwise flat goes to flat.

### Corollary 3: the intended quotient necessarily sees the short corner

In any exact event quotient ((\pi,F,E)), the image
[
y_\star:=\pi(x_\star)
]
is uniquely characterized on the accessible part of (Y_m) by
[
(E(y),E(Fy))=(\mathrm{flat},\mathrm{other}*{0010}).
]
Moreover, the fiber over (y*\star) is a singleton:
[
\pi^{-1}(y_\star)={x_\star}.
]

**Proof.** If (y=\pi(x)), then
[
(E(y),E(Fy))
============

(\epsilon_4(x),\epsilon_4(Tx)).
]
By Lemma 2, the pair ((\mathrm{flat},\mathrm{other}*{0010})) occurs only at (x*\star). So any (x) above such a (y) must equal (x_\star). ∎

This is the part that answers the “why should the quotient see the unique short corner?” question. It is inevitable as soon as the quotient is exact for (\epsilon_4): the short corner is not special because of a guessed carrier; it is already the unique two-step event marker in the theorem-side scheduler.

### Definition 4: corner-time on the quotient

Assume now that (X_m) is a cycle of length (m). Define the corner indicator on (Y_m) by
[
C(y)=1
\iff
(E(y),E(Fy))=(\mathrm{flat},\mathrm{other}*{0010}).
]
On the accessible cycle, define
[
t*\star(y):=\min{,0\le t<m:\ C(F^t y)=1,}.
]

Because there is exactly one short corner per cycle, (t_\star(y)) is well-defined and unique. The theorem-side corner has
[
\beta(x_\star)=-\kappa(x_\star)\equiv -2\equiv m-2 \pmod m.
]

### Theorem 5: explicit clock descent from the corner marker

Define
[
\beta_Y(y):=m-2+t_\star(y)\pmod m.
]
Then (\beta_Y) is the unique descended clock on the accessible quotient, and
[
\beta_Y\circ \pi=\beta,
\qquad
\beta_Y(Fy)=\beta_Y(y)-1\pmod m.
]

**Proof sketch.** On the theorem-side cycle, (\beta) decreases by (1) each step and equals (m-2) at the short corner. So for any (x), the unique time to the next corner is exactly the unique (t\in{0,\dots,m-1}) such that
[
\beta(x)-t\equiv m-2\pmod m,
]
that is,
[
\beta(x)\equiv m-2+t_\star(\pi(x))\pmod m.
]
This gives (\beta_Y\circ \pi=\beta). The drift identity follows because moving one step forward decreases the time-to-next-corner by (1) modulo (m). ∎

So at the cycle level, the clock descent problem is actually solved by the event scheduler: once the quotient is exact for (\epsilon_4), the canonical clock is recovered by “distance to the next short corner.” No extra phase fiber argument is needed.

### Corollary 6: canonical realization collapses to a graph

Let
[
\mathcal R_m
============

{(y,b)\in Y_m\times \mathbb Z/m\mathbb Z:\exists x\in X_m,\ \pi(x)=y,\ \beta(x)=b}.
]
Then, under Theorem 5,
[
\mathcal R_m={(y,\beta_Y(y)):y\in Y_m^{*}}.
]

So the canonical realization exists automatically, and on the exact event quotient it collapses to the graph of the descended clock.

---

## Why this is better than the previous fiber-singleton answer

The previous answer said: descent is equivalent to singleton phase fibers, and one singleton anchor would suffice.

This version is stronger because it identifies the anchor **intrinsically**:

* the short corner is already visible from the two-step event word;
* that visibility is forced by exactness of (\epsilon_4);
* the descended clock is an explicit function of corner-time.

So the key new point is:

> **The quotient should see the short corner because the short corner is the only state whose current event is flat and whose next event is `other_{0010}`.**

That is why it is inevitable, not merely plausible.

---

## Chain version and promotion

The notes still treat cycle-vs-chain as the main exact-reduction nuance, with the chain statement possibly safer first and the cycle statement a later strengthening.

So the clean promotion path is:

### Chain theorem

If the validated exact reduction is only a marked chain
[
x_0\to x_1\to\cdots\to x_{m-1},
]
and the short corner lies in that chain, then on the forward-reachable segment
[
X_m^{\preceq x_\star}:={x:\text{some }T^t x=x_\star}
]
the same detector
[
(E(y),E(Fy))=(\mathrm{flat},\mathrm{other}*{0010})
]
identifies the corner image uniquely, and the same formula
[
\beta_Y(y)=m-2+t*\star(y)
]
recovers the clock on that forward-reachable segment.

### Promotion step

If that chain is later promoted to a return cycle, the same detector extends globally, and Theorem 5 gives the full modulo-(m) descended clock on the whole accessible quotient.

So the safest proof strategy is:

1. prove short-corner visibility on the chain,
2. prove the return promotion to a cycle,
3. conclude full clock descent.

That matches the current packaging very well.

---

## What I think is actually proved in shape now

Conditionally, I think the clock route can be packaged as:

**Clock Realization Theorem.**
For any exact quotient of the validated marked cycle that is exact for (\epsilon_4), the canonical lifted clock (\beta=-\kappa) descends uniquely to the quotient and is given explicitly by time to the next short corner.

**Short-Corner Visibility Lemma.**
The intended quotient necessarily sees the unique short corner state, because it is the unique state with event signature ((\mathrm{flat},\mathrm{other}_{0010})).

**Promotion Corollary.**
If only the marked chain is first validated, the same argument already gives the clock on the pre-corner corridor; once the return is promoted, the full cyclic clock follows immediately.

---

## What is still missing

I do not think the package alone proves the intended local/admissible object is already an exact deterministic quotient for (\epsilon_4) on the validated chain/cycle. That is still the reduction/validation step the notes leave to the live frontier and compute support.

So the remaining proof-critical tasks are:

1. validate the exact reduction object cleanly as chain or cycle;
2. prove the intended quotient is deterministic and exact at least for (\epsilon_4) there.

If those two are done, the clock descent/realization is no longer open in substance: the short-corner detector gives it.
