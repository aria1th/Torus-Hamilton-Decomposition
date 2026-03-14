The concentrated handoff says the negative route should be an **exact bounded-quotient theorem** built on the **cyclic-section principle**, not just another bounded-horizon no-go. It also says the positive route has compressed to a transported cyclic clock, ideally a `beta` with unit drift. The cleanest progress here is a rigidity theorem showing that on a one-marked cycle, any exact quotient already contains the full clock. 

## 1. The core theorem: exact quotients on the cyclic section are trivial

Let
[
\Sigma_m={x_0,\dots,x_{m-1}},
\qquad
R(x_q)=x_{q+1}\ \ (\bmod m),
]
and suppose the carry label is supported at one residue:
[
c(x_q)=\mathbf 1_{{q=q_*}}.
]

Take any finite-state exact quotient data
[
\pi:\Sigma_m\to Q,\qquad \widehat R:Q\to Q,\qquad \chi:Q\to{0,1},
]
such that
[
\pi\circ R=\widehat R\circ \pi,
\qquad
c=\chi\circ \pi.
]

### Theorem N1 (cyclic-section rigidity)

Under those assumptions, (\pi) is injective. Hence (\pi(\Sigma_m)) has exactly (m) points, (\widehat R) restricts to an (m)-cycle on (\pi(\Sigma_m)), and (\pi) is a conjugacy
[
(\Sigma_m,R)\cong (\pi(\Sigma_m),\widehat R).
]

### Proof

Define the first-hit time to carry on the quotient image:
[
h(y):=\min{n\ge 0:\chi(\widehat R^n y)=1}.
]
This is well-defined on (\pi(\Sigma_m)) because along one cycle there is exactly one carry state.

For (y=\pi(x_q)),
[
h(\pi(x_q))
===========

\text{the unique }n\in{0,\dots,m-1}\text{ such that }q+n\equiv q_*\pmod m.
]
So
[
h(\pi(x_q))\in{0,\dots,m-1}
]
takes distinct values for distinct (q). Therefore the states (\pi(x_q)) are all distinct, so (\pi) is injective.

Now
[
\widehat R(\pi(x_q))=\pi(Rx_q)=\pi(x_{q+1}),
]
so (\widehat R) cycles through those (m) distinct image states in order. Thus (\pi(\Sigma_m)) is itself an (m)-cycle, and (\pi) is a conjugacy onto that image. ∎

The punchline is stronger than “(|Q|\ge m)”: there is **no nontrivial exact quotient on the cyclic section**.

---

## 2. The lower bound you actually want for a local carrier

The negative route wants a reduction from the intended local/admissible class to a finite cover plus a carrier. Here is the right statement.

Assume on (\Sigma_m) you have a deterministic cover
[
\psi_m:\Sigma_m\to \Xi_m,
\qquad
N_m:\Xi_m\to\Xi_m,
\qquad
\psi_m\circ R=N_m\circ \psi_m,
]
and a carrier
[
\sigma_m:\Sigma_m\to S_m
]
with local update/readout maps
[
U_m:\Xi_m\times S_m\to S_m,
\qquad
H_m:\Xi_m\times S_m\to{0,1},
]
such that
[
\sigma_m(Rx)=U_m(\psi_m(x),\sigma_m(x)),
\qquad
c(x)=H_m(\psi_m(x),\sigma_m(x)).
]

Define the combined state
[
\Pi_m(x):=(\psi_m(x),\sigma_m(x)).
]

### Theorem N2 (finite-cover lower bound)

(\Pi_m) is injective on (\Sigma_m). Consequently,
[
m\le |\psi_m(\Sigma_m)|,|\sigma_m(\Sigma_m)|
\le |\psi_m(\Sigma_m)|,|S_m|.
]

In particular, if the cover visits at most (K) states on the cyclic section, then
[
|S_m|\ge \Big\lceil \frac{m}{K}\Big\rceil.
]

### Proof

The combined state semiconjugates the cycle:
[
\Pi_m(Rx)
=========

\big(N_m(\psi_m(x)),,U_m(\psi_m(x),\sigma_m(x))\big)
=: \widehat R_m(\Pi_m(x)).
]
Also
[
c(x)=H_m(\Pi_m(x)).
]
So Theorem N1 applies to (\Pi_m), giving injectivity.

Since (\Pi_m(\Sigma_m)\subseteq \psi_m(\Sigma_m)\times \sigma_m(\Sigma_m)),
[
m=|\Sigma_m|
============

|\Pi_m(\Sigma_m)|
\le
|\psi_m(\Sigma_m)|,|\sigma_m(\Sigma_m)|
\le
|\psi_m(\Sigma_m)|,|S_m|.
]
∎

This is the exact bounded-quotient theorem the handoff is pointing toward. 

Two useful features:

* You only need to bound the number of cover states **visited on the section**, not necessarily the full global size of (\Xi_m).
* The conclusion is linear: if the visible cover is (O(1)) on the section, the hidden carrier must be (\Omega(m)).

---

## 3. The hidden-clock corollary

There is an even stronger conceptual consequence.

### Corollary N3 (every exact scheme contains a cyclic clock)

Under the assumptions of Theorem N1, define on (\pi(\Sigma_m))
[
\beta_\pi(\pi(x_q)):=q_*-q \pmod m.
]
Then
[
\beta_\pi(\widehat R y)=\beta_\pi(y)-1 \pmod m,
\qquad
\chi(y)=\mathbf 1_{{\beta_\pi(y)=0}}.
]

So any exact quotient already carries an (m)-valued clock with unit drift.

This is the clean bridge to the positive route: an exact local solution does not merely “recover carry somehow.” On the cyclic section it must secretly realize a clock conjugate to (\mathbb Z/m\mathbb Z) with drift (-1). That is exactly why the `beta` route in the handoff is structurally natural, not just convenient. 

---

## 4. What the D5 negative branch should now target

I think the negative branch should be written as the following theorem package.

### N1. Cyclic section exists

Extract a return section
[
\Sigma_m={x_0,\dots,x_{m-1}}
]
on the active branch with
[
R(x_q)=x_{q+1},
\qquad
c(x_q)=\mathbf 1_{{q=q_*}}.
]

### N2. Admissible local schemes reduce to a finite cover

Prove that any intended local/admissible exact scheme on that section factors through some deterministic cover
[
\psi_m:\Sigma_m\to\Xi_m
]
with a bounded number of visited cover states:
[
|\psi_m(\Sigma_m)|\le K
]
for a constant (K) independent of (m).

This is weaker than a full global bounded-cover theorem, and therefore easier. It is also already sufficient.

### N3. Apply Theorem N2

Then
[
|S_m|\ge \Big\lceil \frac{m}{K}\Big\rceil,
]
so no uniformly bounded carrier family can recover carry on all odd (m).

That gives the exact impossibility theorem the handoff wants. 

---

## 5. Why this is better than the old witness-pair route

The witness-pair route only says some bounded future codings fail.

This route says something much stronger:

* any exact local scheme induces an exact quotient on the cyclic section;
* any such exact quotient is rigid;
* therefore the scheme must carry the full cyclic phase, up to conjugacy.

So the negative conclusion is not merely “short local data are insufficient.” It is:

> on the cyclic section, exact carry recovery forces a genuine (m)-clock.

That is the sharp form of the bounded-quotient route.

---

## 6. The most useful formulation for the manuscript

I would package it like this.

**Lemma N.1 (cyclic-section rigidity).**
Any exact semiconjugate quotient of a one-marked (m)-cycle is injective, hence a conjugacy onto an (m)-cycle.

**Lemma N.2 (finite-cover lower bound).**
If an exact local scheme factors through a deterministic cover (\psi_m) and a carrier (S_m), then
[
m\le |\psi_m(\Sigma_m)|,|S_m|.
]

**Corollary N.3 (bounded-cover impossibility).**
If (|\psi_m(\Sigma_m)|\le K) uniformly in (m), then every exact carrier needs (|S_m|\ge m/K), so no uniformly bounded local scheme exists.

**Corollary N.4 (clock extraction).**
Any exact local scheme on the cyclic section contains an (m)-valued unit-drift clock.

That is, I think, the cleanest negative bounded-quotient / cyclic-section route now available.

I used only the concentrated handoff, not the tar bundle.
