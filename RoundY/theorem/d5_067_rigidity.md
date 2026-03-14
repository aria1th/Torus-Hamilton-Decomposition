The handoff’s reformulation is exactly right: the old negative route should become a **rigidity theorem** saying that once the exact reduction object is fixed, any exact realization already contains the canonical clock on its accessible exact part. The key point is that injectivity on the accessible section/chain is enough to transport **every** theorem-side coordinate, not only carry. 

## 1. The right abstract setup

Let (X_m) be the exact reduced object on the active branch. For the moment, keep both possibilities open:

* **chain version:** (X_m=C_m={x_0,\dots,x_{m-1}}) with successor (T(x_i)=x_{i+1}) for (i<m-1);
* **cycle version:** (X_m=\Sigma_m={x_0,\dots,x_{m-1}}) with (T(x_q)=x_{q+1 \bmod m}).

Assume (X_m) comes with:

* the theorem-side visible object (B_X:X_m\to \mathcal B),
* the carry label (c_X:X_m)\to{0,1}),
* the canonical clock (\beta_X:X_m\to A_m) from the theorem package, where (A_m={0,\dots,m-1}) in the chain case or (A_m=\mathbb Z/m\mathbb Z) in the cycle case.

An **exact realization** of this reduced object is data
[
(Y,F,V,H,\pi)
]
such that

[
F\circ \pi=\pi\circ T,\qquad
V\circ \pi=B_X,\qquad
H\circ \pi=c_X.
]

Here:

* (Y) is the realization state space,
* (F:Y\to Y) is its deterministic update,
* (V:Y\to\mathcal B) is the visible theorem object readout,
* (H:Y\to{0,1}) is the carry readout,
* (\pi:X_m\to Y) identifies the accessible exact part.

The accessible exact part is
[
Y_*:=\pi(X_m)\subseteq Y.
]

The whole rigidity question is:

> when is (\pi) forced to be injective, so that every theorem-side coordinate on (X_m) transports uniquely to (Y_*)?

## 2. The clean rigidity criterion

The essential condition is not “finite quotient” and not “bounded horizon.” It is:

> distinct states of (X_m) must have distinct future carry words.

This is what makes exact compression impossible.

Define the future carry word of (x\in X_m):

* in the cycle case,
  [
  w(x):=\big(c_X(x),c_X(Tx),\dots,c_X(T^{m-1}x)\big)\in{0,1}^m;
  ]
* in the chain case,
  [
  w(x_i):=\big(c_X(x_i),c_X(x_{i+1}),\dots,c_X(x_{m-1})\big).
  ]

### Lemma 1

If the map (x\mapsto w(x)) is injective on (X_m), then every exact realization ((Y,F,V,H,\pi)) is injective on (X_m).

### Proof

Assume (\pi(x)=\pi(x')). Then for every forward time for which both sides are defined,
[
\pi(T^n x)=F^n(\pi(x))=F^n(\pi(x'))=\pi(T^n x').
]
Applying (H),
[
c_X(T^n x)=H(F^n\pi(x))=H(F^n\pi(x'))=c_X(T^n x').
]
So (w(x)=w(x')). By injectivity of (x\mapsto w(x)), we get (x=x'). ∎

This already gives the exact mechanism: **determinism + exact carry readout force faithful embedding whenever carry words separate states.**

## 3. One-marked chain/cycle gives separation automatically

Now specialize to the D5-style marked reduction object.

### Chain case

Assume
[
c_X(x_i)=\mathbf 1_{{i=m-1}}.
]
Then
[
w(x_i)=0^{,m-1-i}1,
]
so the words are pairwise distinct.

### Cycle case

Assume
[
c_X(x_q)=\mathbf 1_{{q=q_*}}.
]
Then (w(x_q)) is the length-(m) one-hot word with the unique (1) in position determined by (q), so again the words are pairwise distinct.

Therefore:

### Theorem 2

For a one-marked chain or one-marked cycle, every exact realization is injective on the accessible exact part:
[
\pi:X_m\to Y_*
]
is a bijection onto (Y_*=\pi(X_m)).

So (Y_*) is not a compressed shadow. It is a faithful copy of the reduced object itself.

This is stronger than the old bounded-quotient statement because it does **not** assume (Y) is finite.

## 4. Transport theorem: every theorem-side coordinate survives intact

Once injectivity is known, every theorem-side coordinate on (X_m) becomes an actual realization-side coordinate on (Y_*).

### Corollary 3

For any function
[
g:X_m\to A,
]
there is a unique function
[
\widetilde g:Y_*\to A
]
such that
[
\widetilde g\circ \pi=g.
]

It is given by
[
\widetilde g(y)=g(\pi^{-1}(y)).
]

This is the real rigidity mechanism. The realization does not merely need “some large memory.” It already contains a faithful copy of the theorem-side state, hence every theorem-side coordinate.

## 5. Clock rigidity

Now apply Corollary 3 to the canonical theorem-side clock (g=\beta_X).

### Theorem 4

For any exact realization of the reduced object, there is a unique realization-side clock
[
\widetilde\beta:Y_*\to A_m
]
such that
[
\widetilde\beta\circ \pi=\beta_X.
]

So any exact realization must carry **that same clock** on its accessible exact part.

This is the sharp statement you wanted.

It is not merely that an exact realization must have at least (m) accessible states. It must carry the actual theorem-side clock, transported through the unique accessible conjugacy.

## 6. The clock law transports automatically

Suppose the theorem package proves a clock law on (X_m), for example
[
\beta_X(Tx)=\Psi(B_X(x),\beta_X(x)).
]
Then on the realization side,
[
\widetilde\beta(Fy)=\Psi(V(y),\widetilde\beta(y))
\qquad (y\in Y_*).
]

### Proof

Write (y=\pi(x)). Then
[
\widetilde\beta(Fy)
===================

# \widetilde\beta(F\pi(x))

# \widetilde\beta(\pi(Tx))

# \beta_X(Tx)

# \Psi(B_X(x),\beta_X(x))

\Psi(V(y),\widetilde\beta(y)).
]
∎

So if the theorem package gives the cycle law
[
\beta_X'=\beta_X-1 \pmod m,
]
then the realization-side clock satisfies the same law on (Y_*). If the first exact object is only a marked chain, then the transported chain clock satisfies the same chain countdown law there; once the return is closed, it becomes the cyclic law. This matches the handoff’s chain-vs-cycle nuance. 

## 7. Why this proves “same clock,” not just “some clock”

There is a subtle but important distinction:

* “some clock” would mean merely an (m)-valued phase variable exists;
* “that same clock” means the exact realization carries the theorem-side (\beta_X), not just a different phase variable.

Theorem 4 gives the stronger statement, because (\widetilde\beta) is defined by transport:
[
\widetilde\beta=\beta_X\circ \pi^{-1}.
]

So once the theorem package fixes the gauge of (\beta_X) — for example via (\beta=-\kappa) on the active branch — the realization-side clock is fixed in exactly that gauge on (Y_*).

## 8. All theorem-side readouts transfer too

This is the big payoff for D5.

If the theorem package proves that on (X_m),
[
q,\ c,\ \epsilon_4,\ \tau,\ \text{next}_\tau
]
are exact functions of ((B_X,\beta_X)), then on the realization side the same formulas hold with ((V,\widetilde\beta)):

[
q=Q(V,\widetilde\beta),\quad
c=C(V,\widetilde\beta),\quad
\epsilon_4=E(V,\widetilde\beta),\quad
\tau=T(V,\widetilde\beta),\quad
\text{next}*\tau=N(V,\widetilde\beta)
]
on (Y**).

So the rigidity theorem says:

> any exact realization already contains the theorem-side controller on its accessible exact part.

That is exactly the interpretation the handoff is pushing toward. 

## 9. Immediate lower-bound corollary

If the realization is represented as
[
Y=\Xi\times S
]
with a visible cover (\Xi) and a hidden carrier (S), then injectivity of (\pi) immediately implies
[
|Y_*|\ge m.
]
Hence if the accessible cover size is bounded by
[
|\Xi_*|\le K,
]
then
[
|S_*|\ge \left\lceil \frac{m}{K}\right\rceil.
]

So the old bounded-quotient route drops out as a corollary of clock rigidity.

## 10. What remains to instantiate this in D5

Conditionally, the rigidity theorem is done. The remaining D5-specific work is:

1. extract the exact reduced object (X_m) on the active branch;
2. prove it is at least a one-marked chain, and ideally a one-marked cycle;
3. identify the theorem-side canonical (\beta_X) on that object.

Once those are in place, the rigidity route is no longer a search problem. The proof is just:

* one-marked chain/cycle (\Rightarrow) separating carry words,
* separating carry words (\Rightarrow) injective exact realization,
* injective exact realization (\Rightarrow) transport of (\beta_X).

Scope: this gives a conditional rigidity theorem package, not yet the D5-specific extraction of the exact chain/section itself.
