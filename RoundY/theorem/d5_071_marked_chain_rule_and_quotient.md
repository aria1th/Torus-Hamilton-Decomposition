# D5 marked chain: exact rule and induced quotient

This note works only on the chain-first reduction question.

## Scope actually used

- theorem-side chain-first setup from `070`
- minimal `070` handoff statement that the existing admissible catalog already
  gives exact deterministic quotients of size exactly `m` on the marked
  length-`m` slice chains
- direct inspection of the bundled frozen active-row dataset `047` on the
  checked moduli `m=5,7,9,11`

I did **not** inspect a raw standalone “admissible catalog” artifact in this
note. So the identification of the quotient seen by the intended class is made
from the theorem plus the reported exact size-`m` quotient fact, not from a
reverse-engineering of the catalog internals.

## 1. The correct first marked-chain object

Fix odd `m>=5`, the regular family, and one full returned block

```text
C_w = {x_{w,q}: q=0,1,...,m-1},   w=2,...,m-3
```

from the `Theta=2` / `beta=m-2` first-return slice.

Write `i=q`. The exact first-return successor on the block is

```text
x_i -> x_{i+1}     for 0<=i<=m-2.
```

The endpoint `x_{m-1}` is carry-marked and then hands off to the next block.
So the first exact object is the marked chain

```text
L_m = ({0,1,...,m-1}, sigma, c)
```

with

```text
sigma(i)=i+1    for 0<=i<=m-2,
c(i)=1_{i=m-1}.
```

This is the exact reduction object on actual states.

## 2. What the bundled frozen data says on that chain

Restrict the `047` frozen rows to:

- regular family,
- `beta = -q-s-v-layer = m-2`,
- full blocks `2 <= w <= m-3`.

On the checked range `m=5,7,9,11`, every such row satisfies:

1. `label = B`;
2. `epsilon4 = flat` off the endpoint, and `epsilon4 = other` at the endpoint;
3. `tau = 0` at the endpoint;
4. `tau = 1` exactly when `s=2` and `c=0`;
5. otherwise `tau = m-2`.

So the exact current rule on the marked chain is:

```text
interior states:  label B, event flat,
endpoint state:   label B, event other, carry=1,
countdown pulse:  tau=1 exactly at the unique interior state with s=2.
```

Equivalently,

```text
epsilon4(i) = flat        for i<m-1,
epsilon4(m-1) = other_1000   (after the later split),
```

and

```text
tau(i) = 1      if i<m-1 and s(i)=2,
tau(i) = m-2    if i<m-1 and s(i)!=2,
tau(m-1)=0.
```

So the first exact rule is **not** yet the periodized beta-cycle with its full
corner scheduler. It is a unary marked chain with one distinguished interior
pulse.

## 3. The pulse is block-dependent in q-coordinate

On the checked frozen range, the `tau=1` site on the full block satisfies

```text
q + w + source_u == 1 mod m,
```

with the carry endpoint excluded.

Using the slice identity `u = q + source_u + 1`, this is equivalent to

```text
w + u == 2 mod m.
```

And on the same slice, this pulse is exactly the same as

```text
s = 2,  c=0.
```

So the short pulse is intrinsic in the theorem-side state, but it is *not* a
fixed site of the bare q-indexed chain across different blocks. This is why the
correct first exact object is the marked chain itself, while the fully stationary
short-corner picture belongs to a later periodized/canonical-clock object.

## 4. The canonical exact quotient of the marked chain

For the bare marked chain `L_m`, the future carry word from state `i` is

```text
0^(m-1-i) 1.
```

These words are pairwise distinct, so the Myhill–Nerode / right-congruence
quotient for exact carry on the chain is exactly

```text
d(i) = m-1-i,
```

with state set `{0,1,...,m-1}` and transition

```text
d -> d-1     for d>0.
```

So the minimal deterministic exact-carry quotient of the marked chain is not a
smaller compressed object. It is an isomorphic copy of the full length-`m`
chain itself.

This is just the “distance to carry endpoint” counter.

## 5. What quotient the intended local/admissible class is actually seeing

Now combine two facts:

1. any deterministic quotient that remains exact for current carry on the marked
   chain is injective, hence has at least `m` states;
2. the `070` handoff reports that the existing admissible catalog already gives
   exact deterministic quotients of size exactly `m` on the marked length-`m`
   slice chains.

Therefore the quotient seen by the intended class on the marked chain must be,
up to relabeling, exactly the canonical distance-to-carry quotient above.

So the intended class is actually seeing:

```text
Q_m  ~=  {0,1,...,m-1}
```

with update

```text
d -> d-1,
```

and carry readout

```text
c = 1_{d=0}.
```

In other words: **on the first exact marked object, the intended class is not
compressing below the full `m`-state counter.**

## 6. What this means for the beta/corner picture

This resolves a subtle mismatch.

- The raw first exact object is the marked q-chain / distance-to-carry chain.
- The moving `tau=1` pulse is a decoration of that chain, visible as `s=2` on
  the theorem-side slice, but not fixed in the bare q-coordinate across blocks.
- The fully stationary short-corner / beta-clock object belongs to the later
  periodized quotient, not to the first chain theorem itself.

So the clean order really is:

1. extract the marked chain `L_m`;
2. identify the induced quotient of the intended class on `L_m`;
3. conclude that this quotient is already the full `m`-state distance-to-carry
   counter;
4. only then promote to the periodized corner/clock object.

## 7. Bottom line

The correct first exact rule on the marked chain is:

```text
unary successor chain + unique carry endpoint,
with a theorem-side interior pulse tau=1 exactly at s=2.
```

The quotient actually seen by the intended local/admissible class, assuming the
reported exact size-`m` chain quotients, is:

```text
the full distance-to-carry quotient,
which is isomorphic to the marked chain itself.
```

So the intended class is already carrying an `m`-valued counter on the first
exact reduction object. The remaining issue is not further compression of the
chain; it is the promotion from this chain counter to the stationary
periodized/corner clock.
