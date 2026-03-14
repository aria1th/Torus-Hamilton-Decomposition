# D5 realization of the canonical beta clock via lifted phase

## Verdict

I can prove a meaningful **positive-route realization statement**, but it is a
realization on the **exact lifted active corridor**, not yet a realization in
the intended local/admissible mechanism class.

The key point is:

> the canonical `beta` clock is already present on the lifted corridor as the
> negative raw phase.

So the remaining constructive problem is no longer

> “does a beta clock exist at all?”

but rather

> “can that already-existing lifted clock be descended / exposed in the intended
> local/admissible class?”

---

## 1. Context from the current handoffs

The concentrated handoff `066` says the clock route is now the realization of
one canonical cyclic clock `beta`, equivalent to the theorem-side phase
`kappa` by

\[
\beta = -\kappa \pmod m,
\]

with target properties:

- universal birth,
- unit drift `beta' = beta - 1 mod m`,
- exact current readout of `q,c,epsilon4,tau,next_tau` from `(B,beta)`.

The earlier handoff `065` sharpens this further by recording the checked
constructive readouts

\[
q \equiv -\beta - s - v - \lambda \pmod m,
\qquad
c = 1_{\{\beta+s+v+\lambda=1\}},
\]

and by treating the realization problem as “realize `beta` directly, or realize
`alpha` and straighten it to `beta`.”

---

## 2. Exact lifted realization theorem

### Theorem (lifted-phase realization of canonical beta)

Assume the strengthened structural chain used in the current route, namely the
candidate active branch on raw lifted current coordinates
\((q,w,u,\Theta)\) with step rule

\[
\widehat F(q,w,u,0)=(q+1,w,u,1),
\]
\[
\widehat F(q,w,u,1)=(q,w,u+1,2),
\]
\[
\widehat F(q,w,u,2)=\bigl(q,\,w+\mathbf 1_{\{q=m-1\}},\,u,\,3\bigr),
\]
\[
\widehat F(q,w,u,\Theta)=(q,w,u,\Theta+1)
\qquad(3\le \Theta\le m-1),
\]
with `Theta` read mod `m`, and assume moreover the structural promotion step
that identifies this lifted phase with the theorem-side scheduler:

\[
\Theta = q+s+v+\lambda = \kappa
\]

on the active nonterminal branch.

Define

\[
\beta_{\mathrm{lift}} := -\Theta \pmod m.
\]

Then on the active nonterminal branch:

1. `beta_lift` has universal birth value
   \[
   \beta_{\mathrm{lift}}(E)=m-2
   \]
   at the post-entry active state `E=(q,w,Theta)=(m-1,1,2)`;
2. `beta_lift` has unit drift
   \[
   \beta_{\mathrm{lift}}' = \beta_{\mathrm{lift}} - 1 \pmod m;
   \]
3. `beta_lift` is exactly the canonical `beta` clock,
   \[
   \beta_{\mathrm{lift}} = -\kappa = \beta \pmod m.
   \]

### Proof

By the lifted candidate rule, every step increases `Theta` by exactly `1 mod m`.
This is immediate from the displayed formulas: each branch sends the phase label
`0 -> 1 -> 2 -> 3 -> ... -> m-1 -> 0`, with no exception.
Hence

\[
\Theta' = \Theta + 1 \pmod m,
\]
so for
\(\beta_{\mathrm{lift}}=-\Theta\)
we get

\[
\beta_{\mathrm{lift}}' = -\Theta' = -(\Theta+1)
= \beta_{\mathrm{lift}} - 1 \pmod m.
\]

At post-entry, the lifted state is `E=(m-1,1,2)`, so `Theta(E)=2` and therefore

\[
\beta_{\mathrm{lift}}(E) = -2 \equiv m-2 \pmod m.
\]

Finally, under the structural identification
\(\Theta=\kappa=q+s+v+\lambda\)
on the active branch, we have

\[
\beta_{\mathrm{lift}} = -\Theta = -\kappa = \beta \pmod m.
\]

So the lifted-phase variable is exactly the canonical `beta` clock. ∎

---

## 3. Consequences

### 3.1 The clock itself is no longer the mystery

At the exact lifted level, the canonical cyclic controller already exists.
There is nothing left to design there:

\[
\boxed{\beta = -\Theta}
\]

is the realization.

So the open positive-route problem is not the abstract existence of `beta`, but
its **descent**.

### 3.2 Readout becomes automatic once `Theta` is available

Since `065` gives the beta-readout formulas

\[
q \equiv -\beta-s-v-\lambda \pmod m,
\qquad
c=1_{\{\beta+s+v+\lambda=1\}},
\]

substituting `beta=-Theta` yields

\[
q \equiv \Theta-s-v-\lambda \pmod m,
qquad
c = 1_{\{s+v+\lambda-\Theta\equiv 1\}}.
\]

And because `beta=-kappa`, the current event scheduler and the countdown law are
exactly the phase-corner scheduler written in the negative gauge.

Thus, on the lifted exact corridor, the whole controller is realized as soon as
`Theta` is part of the state description.

### 3.3 The remaining positive-route problem is a descent/exposure theorem

The honest remaining task is now:

> prove that the lifted phase `Theta` (equivalently `beta=-Theta`) is exposed or
> transportable in the intended local/admissible class.

This is much sharper than the earlier phrasing “realize beta.”
The beta clock is already present on the exact lifted object; what is unresolved
is whether the intended local class can support that same `m`-valued phase.

---

## 4. Best next theorem target

The strongest clean next positive theorem is therefore:

### Descent theorem for the lifted phase

There exists a local/admissible carrier variable `Gamma` on the active branch
such that

\[
\Gamma = \Theta \pmod m
\]

on the accessible exact lifted section.

Equivalently, defining

\[
\beta := -\Gamma,
\]

one gets a local/admissible realization of the canonical beta clock.

This theorem is exactly what remains after the lifted realization above.

---

## 5. Honest status

What is proved here:

- **conditional exact realization on the lifted corridor:** yes;
- **universal birth and unit drift there:** yes;
- **identification with the canonical theorem-side beta:** yes;
- **local/admissible realization in the intended class:** still open.

So the positive-route frontier has sharpened to:

> `beta` is already realized on the exact lifted model as `-Theta`; now prove
> that this phase descends to the intended local/admissible mechanism class.

