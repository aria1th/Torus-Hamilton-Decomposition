# D5 Decorated Exact Bridge Handoff 073

This note records the post-`072` synchronization for the D5 bridge branch.
It is a status / handoff note, not a new proof package.

Its job is to say what `072` actually settled, what it contradicted, and what
should now count as the live exact-bridge target.

## Scope actually used

This note only uses the existing saved material:

- `RoundY/theorem/d5_071_unified_bridge_handoff.md`
- `RoundY/theorem/d5_corner_time_descent_theorem_20260314_070.md`
- `artifacts/d5_exact_reduction_support_068b/README.md`
- `artifacts/d5_bridge_compute_support_072/README.md`
- `artifacts/d5_bridge_compute_support_072/data/analysis_summary.json`
- `artifacts/d5_bridge_compute_support_072/data/offset_normalization_checks.json`
- `artifacts/d5_bridge_compute_support_072/data/state_chain_union_quotients.json`
- `artifacts/d5_bridge_compute_support_072/data/chain_type_formula_validation.json`

I did **not** reopen broad search, rerun old controller scans, or regenerate a
new large-modulus exhaustive dataset for this note.

## 1. What `072` changes

`071` treated the live fork as:

- either the per-chain marked-chain quotients globalize to one exact bridge,
- or the carry offset is essentially asymmetric and blocks that bridge.

`072` sharpens this fork.

### 1.1 The coarse bridge should now be treated as settled

At the carry / distance-to-endpoint level, the per-chain picture does glue.
More precisely:

- on the regular carry_jump slice union, the affine normalization
  `q = s - source_u - w (mod m)` is exact for the carry mark and deterministic
  on successor;
- the other nearby normalizations tested in `072`
  (`s`, `s-source_u`, `s-w`) fail;
- the larger-modulus `068B` data already keep the marked length-`m` chain and
  canonical `beta` transport exact on regenerated full rows through
  `m = 13,15,17,19,21`, with branch-local support through
  `m = 31,33,35,37,39,41`.

So the branch should no longer talk as if the whole bridge question were still
about whether *any* meaningful globalization exists. A meaningful coarse bridge
already exists on the checked support.

### 1.2 The realization theorem is now conditional rather than mysterious

The `070` corner-time note already reduced the realization burden to a very
small exactness hypothesis:

- if a deterministic quotient on the exact marked object is exact for current
  `epsilon4`,
- then the two-step signature `(flat, other_0010)` detects the short corner,
- and the canonical clock descends automatically by corner-time.

So the live realization question is no longer “how do we invent the clock?”
It is only:

> what is the smallest deterministic global quotient that is exact for current
> `epsilon4`?

### 1.3 The bare `m`-state bridge is too coarse

`072` gives a concrete contradiction to the bare normalized `m`-state beta
bridge.

On the checked frozen exhaustive range `m = 5,7,9,11`:

- the bare quotient `beta` is deterministic on successor;
- but it is **not** exact for current `epsilon4`;
- and it is **not** exact for the short-corner detector.

The first collisions occur at the early post-carry sites. So offset
normalization alone does not produce the exact current-event bridge.

### 1.4 A small decorated bridge is supported

Among the targeted natural quotients checked in `072`:

- `beta`
- `beta+a`
- `beta+b`
- `beta+q`
- `beta+sigma`
- `beta+q+sigma`
- `beta+a+b`

all the one-decoration candidates fail, the bare bridge fails, and the first
small exact survivor is:

- `beta+a+b`, equivalently the decorated state `(beta,a,b)`.

This quotient is exact for current `epsilon4`, deterministic on successor, and
exact for the short-corner detector on the checked frozen range.
This is compute support, not yet a proof of global minimality beyond the
checked candidate family.

So from this point forward, the honest shared target is the **decorated exact
bridge**, not the bare bridge.

## 2. The exact reduction object actually supported now

The checked frozen data support the following sharpened object on the union of
regular carry_jump-to-wrap chains.

### Supported state

Use the decorated beta-chain state

`(m, beta, a, b)`

with `4m` states per modulus on the checked range.

Here:

- `beta` is the canonical chain coordinate;
- `a` and `b` are the two early post-carry decoration bits.

### Supported successor rule

On nonterminal states,

`(m, beta, a, b) -> (m, beta-1, a, b)`.

So the decorations are stationary along each chain; the dynamics remain the
same one-step beta countdown.

### Supported `epsilon4` rule

The checked `072` exact rule is:

- `epsilon4 = carry_jump` at `beta = m-1`;
- `epsilon4 = wrap` at `beta = 0`;
- `epsilon4 = other_1000` at `beta = m-2` iff `a = 1`, else `flat`;
- `epsilon4 = other_0010` at `beta = m-3` iff `b = 1`, else `flat`;
- otherwise `epsilon4 = flat`.

So the only failure of the bare bridge is concentrated in the two early
post-carry positions.

### Supported short-corner detector

On the same checked range,

`short_corner = 1 iff (beta,a,b) = (m-2,0,1)`.

This is exactly the input needed by the corner-time realization route.

## 3. What the decoration bits are

The bits are not arbitrary labels on the checked frozen range.
They are exactly determined by the normalized slice data.

Let

- `q = s - source_u - w (mod m)`;
- `sigma = source_u + w (mod m)`.

Then `072` validates the formulas

- `a = 1` iff `q = m-1`;
- `b = 1` iff `(q + sigma = 1 mod m)` or `(q = m-1 and sigma != 1)`.

So the supported small bridge can also be read as a quotient of the normalized
slice-chain data. This matters for the symmetry question:

- the offset is removable at the coarse level,
- but exact `epsilon4` still remembers two post-carry decorations after that
  normalization.

## 4. What is now settled versus still open

### Settled on current support

The following should now be treated as settled at the present compute / theorem
support level.

- The per-chain marked-chain rule is not the live mystery.
- The coarse cross-chain bridge at carry / distance-to-endpoint level is not
  the live mystery.
- The realization route is no longer conceptually open-ended:
  deterministic exactness for current `epsilon4` is the key hypothesis, and
  corner-time then forces the short-corner detector and the canonical clock.
- The bare `m`-state beta bridge is not the right exact object for current
  `epsilon4`.

### Still open

The live bridge question has changed shape.
It is now:

> is `(beta,a,b)` the true smallest exact bridge for current `epsilon4`, or
> can the two decoration bits be compressed, symmetrized, or characterized more
> canonically?

That is a much narrower problem than the old “does any bridge exist?” fork.

## 5. Consequence for the four-way split

The `071` four-researcher split should now be read in decorated form.

### Researcher 1: bridge existence

The bridge-existence question is no longer about a bare beta quotient.
It is about the existence / characterization of the exact **decorated** global
bridge.

### Researcher 2: symmetry versus asymmetry

The symmetry question is no longer “can beta alone be globalized?”
That answer is already no for exact `epsilon4`.
The new symmetry question is whether the two decorations are intrinsic, or
whether they can be packaged more canonically after normalization.

### Researcher 3: realization / clock descent

The realization theorem should now be interpreted relative to the decorated
bridge.
Once a deterministic quotient exact for current `epsilon4` is fixed, the
short-corner detector and `beta` descend automatically by corner-time.

### Researcher 4: compute support

The compute burden is now very specific:

- extend the decorated `(beta,a,b)` exactness checks beyond the frozen
  `m = 5,7,9,11` range;
- test whether the two decoration bits admit a more invariant formula on larger
  moduli;
- test whether any still-smaller decorated quotient survives exactness;
- avoid reopening broad controller search.

## 6. The immediate shared target

The project target should therefore be stated as follows.

### Decorated exact bridge target

Find the smallest deterministic global quotient on the accessible regular union
of chains that

- restricts to the marked-chain / beta picture on each chain,
- is exact for current `epsilon4`, and
- therefore supports short-corner descent and canonical clock descent by
  corner-time.

On current checked support, the best exact candidate is the decorated quotient
`(beta,a,b)`.

So the live question is not:

- whether a bridge exists at all,
- nor whether beta alone globalizes,

but rather:

- whether the decorated bridge is final,
- and if not, what smaller exact decorated object replaces it.

## 7. Bottom line

`072` narrows the D5 bridge frontier in one decisive way.

The coarse bridge should now be treated as essentially settled, the bare
`m`-state bridge should now be treated as contradicted for current `epsilon4`,
and the supported exact target on the checked range is a small decorated bridge
of the form `(beta,a,b)`.

So the shared target from here onward should be the **decorated exact bridge**,
with symmetry/asymmetry and realization questions interpreted relative to that
refined object.
