# D5 beta-controller and section-reduction stress test

This note records a targeted compute audit of the `beta` controller identities and the
section-reduction picture, using only the bundled `064` artifacts plus the `065`
concentrated handoff as the mathematical target.

## Scope actually checked

### A. Exact per-row `beta` audit on frozen active-row data

Used file:

- `artifacts/d5_future_transition_carry_coding_047/data/frozen_B_c_tau_epsilon_dataset_047.json`

Checked moduli:

- `m = 5, 7, 9, 11`

Definition used on each active row:

- `beta = -q - s - v - layer mod m`

Targets checked against current key `(B,beta)`:

- current `q`
- current `c`
- current `epsilon4`
- current `tau`
- next `tau`
- next `B`

Also checked direct formulas:

- `q = -beta - s - v - layer mod m`
- `c = 1_{beta + s + v + layer = 1}`
- `kappa = -beta mod m`
- `epsilon4` from the phase-corner 4-class rule in `(kappa,c,s)`
- `tau = 0` on nonflat states, and on flat states `tau = 1` at `(beta,s)=(m-2,2)` and `tau = beta` otherwise

### B. Section-reduction audit on the raw branch-local odometer rule

Used raw active-corridor rule:

- `(q,w,theta=0) -> (q+1,w,1)`
- `(q,w,theta=1) -> (q,w,2)`
- `(q,w,theta=2) -> (q,w+1,3)` if `q=m-1`, else `(q,w,3)`
- `(q,w,theta=t) -> (q,w,t+1)` for `3 <= t <= m-1`

Start state:

- `(m-1,1,2)`

Stop at regular first-exit target:

- `(m-1,m-2,1)`

Checked moduli:

- `m = 5, 7, 9, 11, 13, 15, 17, 19, 25, 27, 29`

## Results

### 1. `beta` controller identities on frozen rows (`m=5,7,9,11`)

For every checked modulus:

- universal birth holds: every trace begins with `beta = m-2`
- unit drift holds: `beta' = beta - 1 mod m` on every recorded transition
- zero collisions on current key `(B,beta)` for:
  - `q`
  - `c`
  - `epsilon4`
  - `tau`
  - `next_tau`
  - `next_B`
- zero failures for the direct formulas listed above

Counts:

| m | row count | transition count | traces | birth failures | drift failures | `(B,beta)->next_B` collisions |
|---|----------:|-----------------:|-------:|---------------:|---------------:|-------------------------------:|
| 5 | 220 | 216 | 4 | 0 | 0 | 0 |
| 7 | 1218 | 1212 | 6 | 0 | 0 | 0 |
| 9 | 3960 | 3952 | 8 | 0 | 0 | 0 |
| 11 | 9790 | 9780 | 10 | 0 | 0 | 0 |

So on the bundled per-row data, the compressed controller picture is stronger than just
`q/c/tau`: current `(B,beta)` already determines current `epsilon4`, current `tau`, next
`tau`, and next `B` with zero collisions.

### 2. Section reduction: what the data naturally gives

The clean object visible in the raw branch-local model is a **constant-`theta` first-return
chain**, not yet a literal `m`-cycle on full states.

Fix the first-return section `theta = 2` (equivalently the `beta = m-2` slice if
`beta = -theta`). Its first-return map is:

- `(q,w) -> (q+1 mod m, w + 1_{q=m-1})`

So on the regular corridor, for each fixed

- `w = 2, 3, ..., m-3`

there is a full length-`m` block

- `(0,w,2), (1,w,2), ..., (m-1,w,2)`

with return dynamics:

- `(q,w,2) -> (q+1,w,2)` for `q = 0, ..., m-2`

and carry label

- `c = 1_{q=m-1}`

on that block.

This is an exact `m`-state **chain** with a unique carry-marked end state.
The bundled data supports this more directly than a literal cyclic `m`-section.

Block counts found before regular exit:

| m | full constant-w blocks of length m | first full w | last full w |
|---|-----------------------------------:|-------------:|------------:|
| 5 | 1 | 2 | 2 |
| 7 | 3 | 2 | 4 |
| 9 | 5 | 2 | 6 |
| 11 | 7 | 2 | 8 |
| 13 | 9 | 2 | 10 |
| 15 | 11 | 2 | 12 |
| 17 | 13 | 2 | 14 |
| 19 | 15 | 2 | 16 |
| 25 | 21 | 2 | 22 |
| 27 | 23 | 2 | 24 |
| 29 | 25 | 2 | 26 |

So the regular corridor contains many explicit length-`m` carry chains before exit. The
negative lower-bound proof should therefore be safe to formulate on a chain if the literal
cycle statement turns out to be awkward.

## Immediate mathematical takeaway

The compute evidence now strongly favors the following wording.

### Positive side

The right controller audit is:

- `beta` is born at `m-2`
- `beta' = beta - 1 mod m`
- current `(B,beta)` exactly determines `q, c, epsilon4, tau, next_tau`, and even `next_B`

### Negative side

The raw branch already exposes a length-`m` carry chain on the regular corridor. So the
section lower-bound theorem can be stated either:

- on a literal cyclic `m`-section, if one is later extracted cleanly, or
- more conservatively, on an `m`-chain with unique carry endpoint, since the same
  injectivity argument works by shifting any pair to the carry endpoint.

## What is still missing from the bundle for a full larger-range audit

The bundle does **not** include raw per-row frozen datasets for `m=13,15,17,19`, only the
`063a` summary that the source-residue formulas are exact there.

So I could not directly rerun the same `(B,beta)` exactness audit for those moduli from the
bundled files alone.

## Precise compute request if a follow-up run is desired

Do **not** reopen generic search. Run only the following targeted tasks.

### Request A: extend the exact `beta` audit

Produce frozen active-row datasets for

- `m = 13, 15, 17, 19`
- optionally also `m = 21, 23`

with at least these columns on every active nonterminal row:

- `m`
- `source_u`
- `family`
- `trace_step`
- `state_index`
- `B = (s,u,v,layer,family)`
- `q, w, u, v, layer`
- `c`
- `dn` or split event class `epsilon5`
- `tau`
- next-row link or enough ordering to recover `next_B` and `next_tau`

Then check, with zero tolerated failures:

1. **Birth**: every trace starts with `beta = -q-s-v-layer = m-2 mod m`.
2. **Drift**: every transition satisfies `beta' = beta - 1 mod m`.
3. **Current exactness**: `(B,beta)` has zero collisions for `q, c, epsilon, tau`.
4. **Next exactness**: `(B,beta)` has zero collisions for `next_tau` and `next_B`.
5. **Formula exactness**:
   - `q = -beta - s - v - layer mod m`
   - `c = 1_{beta + s + v + layer = 1}`
   - `epsilon` from the phase-corner rule
   - `tau` from the flat/corner rule.
6. If any failure occurs, save the **first exact witness row pair** for each failed item.

### Request B: section / lower-bound reduction

Using the raw branch-local corridor model on the regular family, for each odd

- `m = 13,15,17,19,25,27,29`
- optionally also `31,33,35`

extract the `theta=2` first-return section and verify:

1. first-return map is exactly `(q,w) -> (q+1 mod m, w + 1_{q=m-1})`;
2. for every `w = 2, ..., m-3`, the block
   - `(0,w,2), ..., (m-1,w,2)`
   is present before first exit;
3. on each such block, carry is exactly `1` at `q=m-1` and `0` elsewhere.

Report:

- number of full blocks found,
- first and last valid `w`,
- first counterexample if any.

### Request C: literal cycle vs chain

Try to extract a genuine cyclic `m`-section on the active branch. If none appears naturally,
record that the correct exact compute statement is the **chain** version above, not the cycle
version.

Pass criterion:

- either an explicit cyclic `m`-section is produced with zero failures, or
- the chain version is confirmed and documented as the stable negative reduction.

