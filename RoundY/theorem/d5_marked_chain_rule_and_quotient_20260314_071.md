# D5 marked-chain rule and intended quotient (working note)

## Setup

Using the frozen `047` active-branch rows from the `064` bundle, restrict to
regular states and extract every length-`m` slice

- starting at a regular `carry_jump` state,
- following actual one-step successors,
- ending at the corresponding `wrap` state.

These are the natural state-level marked chains relevant to `epsilon4` and the
short-corner detector.

Define
\[
\beta := -(q+s+v+\lambda) \pmod m.
\]
On every extracted chain, the observed values are exactly
\[
\beta = m-1, m-2, \dots, 1, 0
\]
in order, so the successor rule is simply
\[
\beta' = \beta - 1.
\]

## Observed exact chain types on the frozen checked range

For `m=5,7,9,11`, every extracted regular chain had one of exactly four event
patterns:

- `(0,0)`: `carry_jump, flat, flat, ..., flat, wrap`
- `(0,1)`: `carry_jump, flat, other_0010, flat, ..., flat, wrap`
- `(1,0)`: `carry_jump, other_1000, flat, ..., flat, wrap`
- `(1,1)`: `carry_jump, other_1000, other_0010, flat, ..., flat, wrap`

where the pair `(a,b) in {0,1}^2` records whether the states at
`beta = m-2` and `beta = m-3` are `other_1000` and `other_0010`, respectively.

Counts on the frozen checked range:

- `m=5`: `(0,0):19`, `(0,1):5`, `(1,0):1`, `(1,1):2`
- `m=7`: `(0,0):103`, `(0,1):17`, `(1,0):3`, `(1,1):12`
- `m=9`: `(0,0):299`, `(0,1):37`, `(1,0):5`, `(1,1):30`
- `m=11`: `(0,0):655`, `(0,1):65`, `(1,0):7`, `(1,1):56`

So the compact exact rule on the state-level marked chain is a decorated
beta-chain:

- states are `(beta,a,b)` with `beta in {m-1,...,0}` and `(a,b) in {0,1}^2`
  fixed for the whole chain,
- successor is `beta -> beta-1`,
- labels are
  - `carry_jump` at `beta=m-1`,
  - `other_1000` at `beta=m-2` iff `a=1`, else `flat`,
  - `other_0010` at `beta=m-3` iff `b=1`, else `flat`,
  - `flat` for `1 <= beta <= m-4`,
  - `wrap` at `beta=0`.

## Quotient most plausibly seen by the intended local/admissible class

The smallest natural quotient of this exact decorated rule is obtained by
forgetting `(a,b)` and remembering only `beta`.

That quotient has exactly `m` states and deterministic successor
\[
\beta \mapsto \beta - 1.
\]

On the frozen checked range, this quotient is exact for transition position but
**not** exact for current `epsilon4`:

- `beta = m-1`: always `carry_jump`
- `beta = 0`: always `wrap`
- `1 <= beta <= m-4`: always `flat`
- `beta = m-2`: merged class `flat / other_1000`
- `beta = m-3`: merged class `flat / other_0010`

So the realization gap is extremely narrow. The intended quotient already looks
like the canonical beta position chain, but it still forgets exactly the two
early-post-carry decorations that determine the short corner.

This is precisely the obstruction to descending the corner-time clock: the
quotient already has the right `m`-state drift, but it is not yet exact enough
for `epsilon4` at `beta = m-2, m-3`.
