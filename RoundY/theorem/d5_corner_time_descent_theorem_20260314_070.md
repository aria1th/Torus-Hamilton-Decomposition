# D5 corner-time descent theorem

## Setup

Let `X` be the accessible exact reduction object (marked cycle, or marked chain together
with the natural regular continuation) with deterministic successor `F`. Let

- `epsilon4 : X -> E`
- `kappa : X -> Z/mZ`
- `beta := -kappa`

be the theorem-side event and clock data.

Assume the phase-corner theorem on `X`:

1. `kappa(Fx) = kappa(x) + 1 mod m`;
2. the current event `epsilon4(x)` is determined by the small phase-corner scheduler;
3. the unique short corner is the state with two-step event signature
   `(flat, other_0010)`.

Let `pi : X -> Q` be a deterministic quotient with induced successor `G` on `Q`, so
`pi ∘ F = G ∘ pi`.

Assume only current-event exactness:

- there exists `epsbar : Q -> E` with `epsilon4 = epsbar ∘ pi`.

## Lemma 1 (future event words descend automatically)

For every `L >= 1`, the length-`L` future event word

`(epsilon4(x), epsilon4(Fx), ..., epsilon4(F^{L-1}x))`

is a function of `pi(x)`.

### Proof

By determinism,

`pi(F^j x) = G^j pi(x)`

for every `j >= 0`. Since `epsilon4 = epsbar ∘ pi`, we get

`epsilon4(F^j x) = epsbar(G^j pi(x))`.

So the whole future event word is

`(epsbar(q), epsbar(Gq), ..., epsbar(G^{L-1}q))`, where `q = pi(x)`.

## Corollary 2 (short-corner detector descends)

Define on `X`

`C_X(x) = 1  iff  (epsilon4(x), epsilon4(Fx)) = (flat, other_0010)`.

Then `C_X` factors through `Q`. Equivalently,

`C_Q(q) = 1  iff  (epsbar(q), epsbar(Gq)) = (flat, other_0010)`

is well defined and satisfies `C_X = C_Q ∘ pi`.

In particular, any deterministic quotient exact for current `epsilon4` already sees the
short corner. No additional “two-step exactness” hypothesis is needed.

## Theorem 3 (corner-time descent)

Assume every accessible state of `Q` has a unique future short corner within the next `m`
steps. This is automatic on a one-marked `m`-cycle; on the chain version it holds on each
full regular block, or after passing to the natural cyclic completion.

Define

`T(q) := min { r in {0,...,m-1} : C_Q(G^r q) = 1 }`.

Then:

1. `T` is well defined on its domain;
2. `T(Gq) = T(q) - 1 mod m`;
3. `T` is the descended corner-time clock;
4. the canonical beta clock is recovered by the fixed normalization

   `beta_Q(q) := T(q) - 2 mod m`.

### Proof

The function `T` is well defined because the future corner in the next `m` steps is unique.
If `T(q) = r`, then the next corner from `Gq` occurs after `r-1` more steps when `r > 0`,
and after `m-1` steps when `r = 0`. Hence

`T(Gq) = T(q) - 1 mod m`.

Now pull back to `X`. By the phase-corner theorem, the short corner occurs at phase
`kappa = 2`, and `kappa` advances by `+1` each step. Therefore the time to the next short
corner on `X` is

`T_X(x) = 2 - kappa(x) mod m`.

Since `beta = -kappa`, we get

`T_X = beta + 2 mod m`,

hence

`beta = T_X - 2 mod m`.

Because `T` descends and is unique after normalization, the descended clock

`beta_Q := T - 2 mod m`

satisfies `beta_Q ∘ pi = beta`.

## Consequence for the D5 realization route

The realization target can be compressed further.

It is enough to prove:

1. the intended quotient is deterministic on the exact marked object;
2. current `epsilon4` is exact on that quotient;
3. the quotient domain carries one future short corner per period/block.

After that, the short-corner detector descends automatically, and the canonical clock is
forced by

`beta = T_corner - 2 mod m`.

So the remaining D5-specific burden is not “invent beta” and not even separately
“descend the corner detector.” It is:

> prove the intended quotient is exact enough for current `epsilon4` on the correct exact
> reduction object, and that the regular accessible block contains the next short corner.
