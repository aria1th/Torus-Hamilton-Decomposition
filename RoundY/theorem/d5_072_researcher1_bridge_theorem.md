# Researcher 1 note: exact bridge existence on the union of marked chains

## Claim

At the level of the exact quotient itself, the bridge **does exist**.

More precisely, let the accessible regular chain family be the marked length-`m`
chains

- `C_a = {x_{a,0},...,x_{a,m-1}}`
- successor `T(x_{a,q}) = x_{a,q+1}` for `0 <= q < m-1`
- carry mark `c(x_{a,q}) = 1_{q=m-1}`
- splice law `T(x_{a,m-1}) = x_{a^+,0}` whenever the next accessible full chain
  `C_{a^+}` exists.

(For the final terminal chain in a finite splice, `T` is simply left undefined at
its last state; this matches the finite-chain diagnostics used in the bundle,
which only require deterministic successor on states that actually have a next
state.)

Then there is a canonical exact quotient

- `pi : U -> Q_m`, where `U = \bigcup_a C_a`
- `Q_m = {0,1,...,m-1}`
- `pi(x_{a,q}) = d(x_{a,q}) := m-1-q`

with partial successor on `Q_m`

- `d -> d-1` for `d > 0`
- `0 -> m-1` whenever the splice to the next full chain exists

and carry readout

- `c_Q(d) = 1_{d=0}`.

On each individual chain `C_a`, this is exactly the canonical marked-chain
quotient.

So the per-chain exact marked-chain quotients **do** globalize to one exact
partial deterministic quotient on the accessible union of chains.

## Why this is the right normalization

The bundle’s local quotient note identifies the per-chain exact quotient in the
affine gauge

- `s = q + sigma_a mod m`

with chain-dependent endpoint at

- `s = sigma_a - 1`.

On that chain,

- `d = m-1-q = sigma_a - 1 - s mod m`.

Thus the varying offset `sigma_a` is a gauge artifact of the affine `s`
coordinate. Once each chain is normalized by its unique marked endpoint, all
chains carry the same intrinsic coordinate `d`, and the splice law is exactly
`0 -> m-1`.

## Proof

### 1. Well-definedness on each chain

On each `C_a`, the unique marked state is `x_{a,m-1}`. Therefore every state
has a canonical distance-to-endpoint

- `d(x_{a,q}) = m-1-q`.

This uses only the marked-chain structure, not any extra observable family.

### 2. Compatibility with successor

If `q < m-1`, then

- `T(x_{a,q}) = x_{a,q+1}`
- hence `d(Tx_{a,q}) = m-1-(q+1) = d(x_{a,q}) - 1`.

If `q = m-1` and the next full chain exists, then by the splice law

- `T(x_{a,m-1}) = x_{a^+,0}`
- so `d(Tx_{a,m-1}) = m-1`.

Therefore `d` is a quotient map to the common marked odometer `Q_m`.

### 3. Exactness for the mark

By construction,

- `c(x_{a,q}) = 1` iff `q = m-1`
- iff `d(x_{a,q}) = 0`.

So carry/endpoint marking descends exactly.

### 4. Restriction to each chain

Fix `a`. The restriction `pi|_{C_a}` identifies `C_a` with the standard marked
length-`m` chain in distance-to-endpoint gauge. Hence the global quotient really
is obtained by gluing the per-chain quotients.

### 5. Minimality at the quotient level

Because the restriction to any single chain is the marked-chain quotient, any
global quotient with that restriction has at least `m` states. The quotient
`Q_m` has exactly `m` states. Hence it is minimal among global quotients whose
restriction to each chain is the exact marked-chain quotient.

## What this does and does not settle

This settles the **bridge-existence question at the exact quotient level**:
there is no abstract obstruction to gluing the per-chain exact marked-chain
quotients.

What it does **not** yet settle is the stronger realization question:
whether this `m`-state bridge is already exact for the finer current event
`epsilon4` and therefore sufficient for corner-time descent.

The checked March 14 note suggests that the corresponding global normalized
position quotient (written there in the one-step `beta` gauge) is deterministic
and chain-exact, but still merges the two early post-carry decorations at the
positions corresponding to `beta = m-2` and `beta = m-3`. So the remaining gap
is not bridge existence itself; it is extra event exactness on top of this
bridge.

## Bottom line

- **Positive theorem:** the per-chain exact marked-chain quotients glue.
- **Canonical bridge:** distance to the marked endpoint (equivalently, the
  normalized `q`-coordinate; in the one-step gauge, the same role is played by
  the `beta` position chain).
- **No contradiction:** the changing affine offset `sigma_a` obstructs the raw
  `s`-gauge, not the exact quotient itself.
- **Remaining frontier:** whether this global `m`-state bridge already carries
  enough extra exactness for `epsilon4` / corner-time descent.
