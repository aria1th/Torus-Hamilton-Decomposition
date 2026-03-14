# D5 compute validation 075

## Dynamic boundary odometer survives the current stress tests

## Scope actually used

This pass stayed inside the narrowed `075` compute role.

What I actually used:

- direct recomputation on the frozen `047` regular-family dataset for
  `m = 5,7,9,11`;
- the regenerated `068B` marked-chain summaries for `m = 13,15,17,19,21`;
- a symbolic stress test of the candidate bridge on every odd modulus
  `m = 5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41`.

What I did **not** do:

- no broad controller search;
- no reopening the old small-family catalog scans;
- no dangerous fresh full-row regeneration past the saved bundle.

So the output here has three layers:

1. **direct row validation** on saved frozen rows;
2. **accessible-subset / splice-law extension** from saved full-row summaries;
3. **symbolic exactness / minimality stress tests** on the dynamic bridge model.

The direct-current-event validation is therefore strongest on `m = 5,7,9,11`.
Beyond that, what I can extend from the bundle is the splice law, the boundary
state space, and the no-smaller-factor evidence inside the supported symbolic
model.

## Data sources

Primary files actually used:

- `artifacts/d5_future_transition_carry_coding_047/data/frozen_B_c_tau_epsilon_dataset_047.json`
- `artifacts/d5_exact_reduction_support_068b/data/marked_chain_validation.json`
- `artifacts/d5_exact_reduction_support_068b/data/beta_exactness_extension.json`

I also generated a small local artifact bundle with the script and JSON outputs
for this pass.

## Candidate quotients tested

On the direct frozen rows and on the full symbolic bridge, I tested the focused
family

- `(beta)`
- `(beta,a,b)`
- `(beta,q)`
- `(beta,sigma)`
- `(beta,q,b)`
- `(beta,r)` with `r = q + sigma mod m`
- `(beta,q,sigma)`
- `(beta,delta)` with `delta = q + m sigma`
- `(beta,q,r)`

The last three are all exact reparameterizations of the same dynamic bridge.
`(beta,q,r)` is not smaller than `(beta,q,sigma)` because `(q,r)` is bijective
with `(q,sigma)`.

---

## 1. Direct frozen-row validation on `m = 5,7,9,11`

The direct recomputation matches the `074` picture and sharpens it slightly by
including the equivalent `delta` and `r=q+sigma` parameterizations.

### Surviving exact deterministic candidates

On the saved regular full-chain union:

- `(beta,q,sigma)` is exact for current `epsilon4`, deterministic, and exact for
  short-corner;
- `(beta,delta)` is exactly equivalent and also survives;
- `(beta,q,r)` is exactly equivalent and also survives.

Observed quotient sizes on the saved rows are:

- `m=5`: `115 = 5 * 23`
- `m=7`: `343 = 7^3`
- `m=9`: `729 = 9^3`
- `m=11`: `1331 = 11^3`

So the only non-full case on the saved rows is `m=5`, where the boundary sample
is not yet closed.

### Failing smaller candidates

The direct row verdict is unchanged in kind:

- `(beta)` is deterministic but too coarse;
- `(beta,a,b)` is exact for current event and short-corner, but not
  deterministic across the splice;
- `(beta,q)` is deterministic but too coarse;
- `(beta,sigma)` fails both exactness and determinism;
- `(beta,q,b)` is exact for current event and short-corner, but still not
  deterministic;
- `(beta,r)` also fails both exactness and determinism.

### First concrete failure witnesses

These are the first relevant witnesses from the direct frozen rows.

1. **Bare `beta` fails current-event exactness.**  
   At `m=5`, key `beta=3` contains both
   - `flat`, for example `(beta,q,sigma)=(3,0,3)`,
   - `other`, for example `(beta,q,sigma)=(3,4,3)`.

2. **Static `(beta,a,b)` fails determinism.**  
   At `m=5`, key `(beta,a,b)=(0,0,0)` wraps to all four next decorated carry
   states
   - `(4,0,0)`,
   - `(4,0,1)`,
   - `(4,1,0)`,
   - `(4,1,1)`.

3. **`(beta,q)` is still too coarse.**  
   At `m=5`, key `(beta,q)=(2,0)` mixes
   - `flat` at `sigma=3`,
   - `other` at `sigma=1`.

4. **`(beta,q,b)` still fails determinism.**  
   At `m=5`, key `(beta,q,b)=(0,0,0)` wraps to both
   - `(4,1,0)`,
   - `(4,1,1)`.

So the direct saved rows still point to the same answer:

> the first surviving exact deterministic bridge is the dynamic one.

---

## 2. Splice law extension beyond the frozen `047` range

This is the first place where I can extend support beyond `m=11` **without**
regenerating new raw event tables.

The `068B` marked-chain summary validates, on regenerated full rows through
`m = 21`, that for every regular source:

- every expected `w`-slice is present, namely `w = 2,3,...,m-2`;
- on each fixed `w`, the carry-jump rows form the full marked `q`-chain
  `q = 0,1,...,m-1`;
- the endpoint of the `w`-slice splices to the next `w+1` slice.

Because
`sigma = source_u + w mod m`,
this is exactly the boundary-odometer update law on carry-jump chain states:

```text
(q, sigma) -> (q+1, sigma)         if q < m-1
(q, sigma) -> (0, sigma+1)         if q = m-1
```

equivalently

```text
delta -> delta + 1 mod m^2
```

with `delta = q + m sigma`.

So the splice law is now supported in two different ways:

- **directly on saved frozen rows** for `m = 5,7,9,11`;
- **from regenerated carry-jump chain summaries** for `m = 13,15,17,19,21`.

That is a real extension of support beyond the frozen range.

---

## 3. Accessible subset `A`

This is where the new compute pass is most useful.

### 3.1 Frozen saved sample

On the saved frozen rows:

- `m=7,9,11`: the observed boundary state set is already the full `m^2` grid;
- `m=5`: the observed boundary state set has size `23`, missing only
  `[(4,0), (4,2)]`.

But that `m=5` defect is not splice-invariant.
If one closes the observed set under the supported odometer successor, the
closure adds exactly those two missing states and becomes the full `5^2 = 25`
grid.

So the saved `m=5` gap is a **sample-closure issue**, not evidence for a
smaller invariant subset.

### 3.2 Regenerated full-row summary through `m=21`

The `068B` full-row summary implies more:

- the regular source set is exactly
  `Z/mZ \ {0,3}`;
- every regular source has every `w = 2,...,m-2`;
- every such slice has the full `q`-chain.

From those facts alone, the implied boundary state set is already the full grid
for every saved full-row modulus:

- `m=13`: `169 = 13^2` pairs;
- `m=15`: `225 = 15^2` pairs;
- `m=17`: `289 = 17^2` pairs;
- `m=19`: `361 = 19^2` pairs;
- `m=21`: `441 = 21^2` pairs.

There were no missing boundary pairs on any of those moduli in the implied grid
reconstruction.

### 3.3 Practical conclusion on `A`

The current compute picture is now:

- on the actual saved frozen rows, only `m=5` is incomplete, and its
  splice-closure is already full;
- on the regenerated full-row summary range `13..21`, the accessible boundary
  subset is already the full odometer grid `A = (Z/mZ)^2`.

So the live accessible-subset gap is much narrower than before.
The data now support the working picture that the regular-chain bridge uses the
**full** boundary odometer, not a mysterious strict subset, on every tested
full-row modulus beyond the tiny `m=5` saved-sample artifact.

---

## 4. Symbolic stress test on odd `m = 5..41`

I then stress-tested the dynamic bridge itself as a symbolic unary automaton on
the full odometer grid.

This does **not** replace direct D5 row validation, but it does answer two
important compute questions:

1. does the candidate-status pattern stay stable well past `m=11`?
2. is there any smaller deterministic exact factor visible inside the symbolic
   model?

### 4.1 Candidate-status pattern is stable on every tested odd modulus

For every odd
`m = 5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39,41`,
the symbolic verdict is the same:

- `(beta)`:
  - `epsilon4` exact? **no**
  - deterministic? **yes**
  - short-corner exact? **no**

- `(beta,a,b)`:
  - `epsilon4` exact? **yes**
  - deterministic? **no**
  - short-corner exact? **yes**

- `(beta,q)`:
  - `epsilon4` exact? **no**
  - deterministic? **yes**
  - short-corner exact? **no**

- `(beta,sigma)`:
  - `epsilon4` exact? **no**
  - deterministic? **no**
  - short-corner exact? **no**

- `(beta,q,b)`:
  - `epsilon4` exact? **yes**
  - deterministic? **no**
  - short-corner exact? **yes**

- `(beta,r)` with `r=q+sigma`:
  - `epsilon4` exact? **no**
  - deterministic? **no**
  - short-corner exact? **no**

- `(beta,q,sigma)`, `(beta,delta)`, `(beta,q,r)`:
  - `epsilon4` exact? **yes**
  - deterministic? **yes**
  - short-corner exact? **yes**

So the dynamic bridge is not merely surviving at `5,7,9,11`.
Its symbolic status pattern is stable on every tested odd modulus up to `41`.

### 4.2 No smaller deterministic exact factor survives inside the symbolic model

Because the symbolic bridge is a single cycle on the full state set, Moore
minimality reduces to a primitive-period check of the output word.

I checked both levels:

1. the chain-level decorated word on the boundary odometer
   `(q,sigma) -> (a,b)`;
2. the full current-event word on the bridge
   `(beta,q,sigma) -> epsilon4`.

On every tested odd modulus `5..41`:

- the chain-level word has minimal period exactly `m^2`;
- the full current-event word has minimal period exactly `m^3`.

So on every tested odd modulus through `41`:

- the chain decoration already has all `m^2` Moore classes;
- the full bridge already has all `m^3` Moore classes.

That is stronger than saying that `(beta,q,sigma)` works.
It says:

> inside the supported symbolic dynamic bridge model, **no smaller deterministic
> exact quotient survives** on any tested odd modulus through `41`.

This is the cleanest current compute evidence for the minimality side.

---

## 5. Short-corner recurrence on the final bridge

A small but useful side computation:

- on the full symbolic bridge, the successor is one cycle of length `m^3`;
- the short-corner set has exactly `m-1` states on that cycle.

So the final bridge is **not** a one-short-corner-per-component object.
It is a recurrent short-corner object with `m-1` short corners on the single
full cycle.

That matches the `074` realization correction: recurrence, not uniqueness of a
corner state, is the right quotient-level hypothesis.

---

## 6. What is actually settled by this compute pass

What is now genuinely strengthened:

1. **Direct support for the dynamic bridge survives recheck** on saved frozen
   rows `m=5,7,9,11`.
2. **Splice-law support extends beyond the frozen range** to regenerated
   carry-jump summaries through `m=21`.
3. **Accessible subset `A` is now much clearer**:
   the saved `m=5` defect is a nonclosed sample artifact, and the regenerated
   full-row range `13..21` already supports the full odometer grid.
4. **No smaller deterministic exact factor is visible** inside the symbolic
   model on any tested odd modulus through `41`.

---

## 7. Exact remaining gap

The remaining compute gap is now very specific:

> I did **not** directly validate the current `epsilon4` readout and the
> short-corner readout on freshly regenerated raw split-event rows beyond
> `m=11`, because the bundle does not include those larger row tables.

So the strongest honest status is:

- **direct actual-row validation**
  - splice law: through `m=11`
  - current `epsilon4` exactness: through `m=11`
  - short-corner exactness: through `m=11`

- **summary / structural extension from saved full-row support**
  - accessible subset `A`: through `m=21`
  - boundary odometer splice law: through `m=21`

- **symbolic bridge-model validation**
  - candidate status pattern: through `m=41`
  - no smaller deterministic exact factor in the symbolic model: through `m=41`

That is the exact line between what I checked directly and what I only extended
symbolically.

---

## Bottom line

I did **not** find a counterexample to the dynamic bridge.

The compute answer is now:

> the dynamic boundary odometer `(beta,q,sigma)` / `(beta,delta)` still
> survives every targeted stress test I could run from the saved bundle.
> The direct row checks remain positive on `m=5,7,9,11`; the boundary splice
> law and the accessible full odometer grid are supported through `m=21`; and
> on the full symbolic model no smaller deterministic exact factor survives on
> any odd modulus tested through `m=41`.

So the compute frontier is no longer “find any bridge.”
It is now narrower:

> **obtain one larger direct raw split-event validation pass beyond `m=11`, or
> prove from structure that the already-supported odometer readout is the true
> exact global bridge.**
