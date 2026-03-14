# D5 Minimal Handoff For 069 Readers

This note is for researchers who already know the `069` picture.

It does **not** restate the full theorem package. It only records what `070`
 clarified and why the focus has shifted.

## What changed from 069 to 070

`069` already cleaned up the global split:

- theorem package: near-stable
- exact reduction: first live focus
- realization: second live focus

`070` sharpens the two live focuses.

### 1. Exact reduction is chain-first

The right first exact object is not a cycle. It is a **marked length-`m`
chain** on the regular corridor.

Why:

- the phase-corner theorem already gives a deterministic `m`-window for free;
- it does **not** give the return identification needed to close that window
  into a cycle;
- so a cycle should be treated as a later **promotion / periodization**
  statement, not the first exact object on actual states.

This means the correct D5 order is:

1. extract the marked chain;
2. study the quotient induced by the intended class on that chain;
3. only later ask whether the quotient closes to a cycle.

### 2. Realization is now corner-time descent

The realization route is now cleaner than in `069`.

If the intended quotient on the exact marked object is:

- deterministic, and
- exact for current `epsilon4`,

then the short corner is already visible from the two-step event signature

- `(flat, other_0010)`.

So the canonical clock is not something to invent or transport by hand. It is
just:

- **time to the next short corner**

with the normalization

- `beta = T_corner - 2 mod m`.

So the realization problem has reduced to:

> prove exact deterministic `epsilon4` quotient on the right exact object.

That is the main conceptual gain of `070`.

## What compute now says

The `069/070` compute side supports this exact-reduction-first picture.

### Marked chain

On the checked frozen range, the existing admissible catalog already gives
exact deterministic quotients of size exactly `m` on the marked length-`m`
slice chains.

So the intended class already sees the first exact object at the right scale.

### Spliced source-chain

On the longer spliced source-chains, the same catalog does **not** compress
below the full chain length.

So the longer object should not be treated as the first reduction target.

### Full branch

On the full active branch, the first small catalogs still do **not** yet give
an exact deterministic current-event quotient.

So the remaining compute/theorem target is very specific:

> identify the exact deterministic `epsilon4` quotient on the marked chain.

## Current focus

The right all-in focus is now:

### Exact reduction

- determine the exact marked chain cleanly;
- determine the quotient induced by the intended class on that chain;
- determine whether that quotient is exact for `epsilon4`.

### Realization

- once that quotient is exact for `epsilon4`, descend the short-corner
  detector;
- then define the canonical clock by corner-time.

## What is no longer the focus

- not a new witness search
- not a new controller design search
- not broad admissible-family widening
- not forcing a cycle before the marked chain is understood

## One-line summary

`070` says: **for D5, the right first exact object is a marked length-`m`
chain, and the realization problem has reduced to exact deterministic
`epsilon4` quotient plus corner-time descent on that chain.**
