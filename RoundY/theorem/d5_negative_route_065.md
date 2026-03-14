I used the unified handoff only and did not open the tarfile. The handoff already frames the negative route as: prove the intended local class collapses to a bounded quotient, then rule that quotient out by a cyclic-section argument. I think that can be sharpened into a stronger and more useful theorem package. 

## What I think the negative branch should prove

The clean statement is not just “bounded horizon fails.” It is:

> On the active cyclic section, the carry observable is generating.
> Therefore any exact local scheme over a bounded finite cover must carry at least (\Omega(m)) states.

That gives both:

* the desired impossibility for bounded quotients, and
* a quantitative lower bound showing why an (m)-valued carrier like (\alpha) is the right positive target.

## 1. Strengthen Proposition B to an injectivity theorem

Let
[
\Sigma_m={x_q : q\in \mathbb Z/m\mathbb Z},
\qquad
R_m(x_q)=x_{q+1},
\qquad
c(x_q)=\mathbf 1_{{q=m-1}}.
]

### Proposition 1

Suppose
[
\pi_m:\Sigma_m\to Q,
\qquad
\widehat R_m:Q\to Q,
\qquad
\chi:Q\to{0,1}
]
satisfy
[
\pi_m\circ R_m=\widehat R_m\circ \pi_m,
\qquad
c=\chi\circ \pi_m.
]
Then (\pi_m) is injective. In particular,
[
|Q|\ge m.
]

### Proof

For each (q), define the carry signature
[
\mathbf c_q
===========

\big(c(x_q),c(R_mx_q),\dots,c(R_m^{m-1}x_q)\big).
]
Because (R_m) is the (m)-cycle and (c) is (1) at exactly one residue, (\mathbf c_q) is the one-hot vector whose unique (1) occurs at position (m-1-q). Hence the (\mathbf c_q) are all distinct.

Now if (\pi_m(x_i)=\pi_m(x_j)), then by semiconjugacy
[
\pi_m(R_m^t x_i)=\pi_m(R_m^t x_j)\qquad\text{for all }t\ge 0.
]
Applying (\chi),
[
c(R_m^t x_i)=c(R_m^t x_j)\qquad\text{for all }t,
]
so (\mathbf c_i=\mathbf c_j), hence (i=j). Therefore (\pi_m) is injective, and (|Q|\ge m). ∎

This is stronger than the earlier lower-bound wording: any exact factor is not merely large, it is actually forced to separate every residue.

A useful slogan is:

> **The carry observable is generating on the cyclic section.**

## 2. The right reduction lemma for the negative branch

The real missing D5 step is not Proposition 1. It is the reduction from the intended local/admissible class to a bounded finite cover. Here is the version I would target.

### Definition

A **finite-cover local carrier scheme** on (\Sigma_m) consists of:

* a finite cover
  [
  \psi_m:\Sigma_m\to \Xi_m
  ]
  with deterministic successor
  [
  N_m:\Xi_m\to\Xi_m
  ]
  such that
  [
  \psi_m(R_mx)=N_m(\psi_m(x));
  ]

* a carrier coordinate
  [
  \sigma_m:\Sigma_m\to S_m;
  ]

* local update and readout maps
  [
  U_m:\Xi_m\times S_m\to S_m,
  \qquad
  H_m:\Xi_m\times S_m\to{0,1},
  ]
  such that on the section
  [
  \sigma_m(R_mx)=U_m(\psi_m(x),\sigma_m(x)),
  \qquad
  c(x)=H_m(\psi_m(x),\sigma_m(x)).
  ]

This matches the kind of “bounded local carrier over bounded grouped data” that the handoff says the negative branch should isolate. 

### Theorem 2

For any such scheme,
[
|\Xi_m|,|S_m|\ge m.
]

In particular, if (|\Xi_m|\le K) uniformly in (m), then
[
|S_m|\ge \frac{m}{K}.
]
So no family with uniformly bounded carrier size can recover carry on all odd (m).

### Proof

Define
[
\pi_m(x)=(\psi_m(x),\sigma_m(x))\in \Xi_m\times S_m.
]
Then
[
\pi_m(R_mx)
===========

\big(N_m(\psi_m(x)),,U_m(\psi_m(x),\sigma_m(x))\big),
]
so (\pi_m) semiconjugates (R_m) to the induced map
[
\widehat R_m(\xi,s)=(N_m(\xi),U_m(\xi,s)).
]
Also
[
c(x)=H_m(\psi_m(x),\sigma_m(x))=\chi(\pi_m(x))
]
with (\chi(\xi,s)=H_m(\xi,s)).

Thus Proposition 1 applies to (\pi_m), so (\pi_m) is injective. Hence
[
m=|\Sigma_m|
\le |\Xi_m\times S_m|
=|\Xi_m|,|S_m|.
]
∎

## 3. Why this is better than the old bounded-horizon no-go

The old witness argument only killed static bounded lookahead.
Theorem 2 kills any exact bounded carrier scheme built over a bounded finite cover.

So the conclusion is stronger:

* not only can you not read carry from a short local window;
* you cannot compute carry with any bounded auxiliary state unless the underlying cover size also grows with (m).

This is exactly the kind of theorem that supports the handoff’s split between the positive (\alpha/\beta) route and the negative bounded-quotient route. An (m)-valued transported carrier is not just one possible construction; up to constants, something of that size is forced. 

## 4. What remains D5-specific

From the unified handoff alone, I do **not** have these two inputs proved:

1. **Cyclic section extraction.**
   You still need the actual D5 section
   [
   \Sigma_m={x_0,\dots,x_{m-1}}
   ]
   with first-return
   [
   R_m(x_q)=x_{q+1}
   ]
   and carry
   [
   c(x_q)=\mathbf 1_{{q=m-1}}.
   ]

2. **Bounded finite-cover reduction.**
   You need a precise theorem saying the intended local/admissible class factors through some finite cover (\Xi_m) of uniformly bounded size (K). This is the real frontier.

Once those are in place, Theorem 2 finishes the negative branch immediately.

## 5. What I would write next in the manuscript

I would package the negative branch as:

* **Lemma N1:** carry is generating on the cyclic section.
* **Lemma N2:** any bounded local carrier over a (K)-state dynamical cover gives a quotient of size at most (K|S_m|).
* **Theorem N3:** therefore (K|S_m|\ge m).
* **Corollary N4:** no bounded carrier family works uniformly in odd (m).

That is the cleanest form I see from the handoff.

Scope: I used only `d5_064_unified_handoff.md`; I did not inspect the tar bundle. Unverified from this document alone: the actual D5 cyclic section and the exact bounded-cover reduction for the intended admissible class.
