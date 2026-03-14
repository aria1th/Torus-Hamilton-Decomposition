# D5 Unified Bridge Handoff 071

This note is the current concentrated handoff for the `069–071` state.

It replaces ad hoc summaries of theorem package, exact reduction, realization,
rigidity, and compute support with one sharper statement of what is already
settled and what is still open.

## 1. What is no longer the main mystery

The D5 branch is no longer blocked on:

- finding a mixed witness
- finding a reduced target
- finding a tiny extra separator bit
- discovering the theorem object
- discovering the per-chain exact rule

Those parts are already compressed enough.

The theorem package is close to stable in shape:

- structural reduction
- phase-corner theorem
- countdown/reset as corollaries

The first exact reduction object is also much clearer than before:

- on each regular fixed slice, the first exact object is a marked length-`m`
  chain
- on that chain, the intended class already sees the full affine chain
  coordinate

So the project is no longer searching for the local rule. It is trying to
identify the exact global bridge that turns those per-chain facts into one
global exact quotient.

## 2. The first exact object

The safe first exact object is chain-first, not cycle-first.

For each regular slice, the exact rule is:

- marked length-`m` chain
- unique carry endpoint
- deterministic successor along the chain

This can be read in two equivalent gauges:

- `q`-gauge:
  `q -> q+1` with endpoint at `q = m-1`
- affine `s`-gauge:
  `s -> s+1` with chain-dependent marked endpoint

So the first exact object is not yet a periodized clock. It is a marked chain.

## 3. What the intended class already sees

On each fixed marked chain, the intended admissible class is already seeing the
full `m`-state deterministic chain coordinate.

The key point is:

- the best exact deterministic quotient per chain is not smaller than the full
  chain
- in the checked range, the admissible catalog features already identify that
  full coordinate
- the endpoint bit alone is cheaper, but it is not deterministic enough

So the issue is not lack of an `m`-state counter on each chain. That part is
already present.

## 4. The actual missing link

The real missing link is the **exact bridge across chains**.

Equivalently:

- can the chain-dependent offset be normalized away?
- can the per-chain exact quotients glue into one global exact reduction
  object?
- does the intended quotient become exact enough for current `epsilon4` on the
  union-of-chains object?

This is the D5-specific bottleneck now.

Another way to say the same thing:

- per-chain exactness is largely settled
- global exact promotion is not

## 5. Symmetry versus asymmetry

This bridge problem can be read as a symmetry question.

There are two possibilities:

### Rotatable / normalizable picture

There is a global gauge in which the chain offset is removable, the chains
become one common marked object up to rotation, and the canonical clock
descends globally.

### Essential asymmetry picture

The chain offset is intrinsic. Then the carry structure is only per-chain
rotatable, not globally rotatable, and no exact bridge of the intended kind
exists.

This is now one of the cleanest ways to state the open fork.

## 6. Canonical clock viewpoint

The constructive and rigidity sides are no longer competing stories.

They are both about the same canonical clock.

- theorem gauge: phase-corner machine
- constructive gauge: `beta`
- exact reduction view: marked chain with a unique short-corner structure

If the bridge exists, then the canonical clock should descend.
If the bridge does not exist, then the obstruction should come from the failure
to globalize the per-chain marked-chain picture.

So the open problem is not “invent a controller.” It is:

> determine whether the canonical clock globalizes from the per-chain exact
> objects to the intended global exact quotient.

## 7. Best current theorem-level formulation

The clean theorem fork is:

### Bridge-existence theorem

There exists an exact deterministic quotient on the accessible union of marked
chains whose restriction to each chain is the marked-chain quotient, and on
which current `epsilon4` is exact enough that corner-time descent yields the
canonical clock.

### Bridge-obstruction theorem

No such quotient exists in the intended local/admissible class. The chain
offset is essential, so the per-chain exact quotients do not globalize.

That is the right current target.

## 8. What compute should and should not do

Compute is no longer being asked to search the old broad space.

It should only support the bridge question:

- validate the exact marked-chain rule further
- validate the induced quotient on the union of chains
- test candidate normalizations of the chain offset
- stress-test exactness for current `epsilon4`
- clarify whether the correct exact global object is a chain family, a
  promoted cycle, or something intermediate

What compute should not do:

- generic search
- generic controller widening
- reopening old tiny-transducer families

## 9. Practical division of labor

The natural split is now:

- theorem package researcher:
  keep the theorem package clean and stable, but do not treat it as the main
  open branch
- bridge researcher:
  prove or disprove existence of the exact global bridge
- symmetry researcher:
  determine whether the chain offset is removable or essential
- realization / compute-support researcher:
  validate exactness of the quotient and corner-time descent on the candidate
  global object

## 10. Bottom line

The D5 case is now narrow enough to summarize in one sentence:

> the per-chain exact marked-chain rule is mostly understood, and the real
> remaining issue is whether those exact chain quotients glue to one exact
> global quotient on which the canonical clock descends, or whether the carry
> is essentially asymmetric across chains.
