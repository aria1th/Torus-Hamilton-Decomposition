# D5 Phase-Machine Hypothesis Handoff 057a

This note is a mathematician-facing handoff for the current `d=5` proof
frontier.

It is meant to answer one question:

> what is the smallest plausible conceptual jump that could turn the current
> checked `d=5` boundary-reset picture into a uniform odd-`m` theorem?

The current best answer is:

> a small phase machine on the active best-seed branch, with the
> carry-jump (`CJ`) branch already reducible to one auxiliary flat-corner
> lemma.

This note keeps theorem statements on the minimal theorem-side object and uses
extra coordinates only as auxiliary proof devices.

## 1. Current theorem object

The theorem-side object remains

`(B, tau, epsilon4)`

with

- `B = (s, u, v, layer, family)`
- `tau` = initial flat-run length for future grouped-delta
  `dn = (0,0,0,1)`
- `epsilon4 in {flat, wrap, carry_jump, other}`

The important discipline is:

- theorem side stays on `(B, tau, epsilon4)`
- stronger coordinates such as `rho` or `delta` may be used in proof, but are
  not promoted to theorem coordinates

This is consistent with:

- [d5_carry_and_finite_cover_044/README.md](../../artifacts/d5_carry_and_finite_cover_044/README.md)
- [d5_tau_countdown_carrier_048/README.md](../../artifacts/d5_tau_countdown_carrier_048/README.md)
- [d5_proof_direction_compute_support_052.md](./d5_proof_direction_compute_support_052.md)

## 2. What is already structurally known

The current positive theorem chain is:

1. `044`: finite-cover normal form `B <- B+c <- B+c+d`
2. `046`: carry sheet `c` is an anticipation datum
3. `047`: all ambiguity of `(B, tau)` lies at `tau = 0`
4. `048`: `tau` is a true countdown carrier
5. `050`, `052`, `055`, `057a`: proof-support checks persist on larger odd
   moduli

So the full `d=5` proof burden is no longer "decode a future window". It is:

- prove the boundary reset theorem at `tau = 0`

and that boundary theorem is already reduced to three branches:

- `wrap`
- `CJ`
- `OTH`

The `wrap` branch is essentially trivial. The current live proof work is:

- prove `CJ` first
- then prove `OTH`

See:

- [d5_boundary_reset_uniform_proof_attempt_055.md](./d5_boundary_reset_uniform_proof_attempt_055.md)
- [d5_CJ_branch_proof_reduction_056.md](./d5_CJ_branch_proof_reduction_056.md)
- [d5_CJ_uniform_proof_progress_057.md](./d5_CJ_uniform_proof_progress_057.md)

## 3. Why `CJ` is the right first branch

On the checked range through `m = 23`, the `CJ` reset law is:

- reset `0` if `s+v+layer == 2 mod m`
- reset `1` if `s = 1` and not zero-reset
- reset `m-2` otherwise

Equivalently, on the `CJ` boundary:

- `q == 1 - s - v - layer mod m`

The zero-reset fiber is already conceptually explained:

- `s+v+layer == 2 mod m`
- iff `q = m-1`
- iff we are on the carry slice
- hence reset is `0`

So the only real mathematical content in `CJ` is the noncarry dichotomy:

- if `q != m-1` and `s = 1`, reset is `1`
- if `q != m-1` and `s != 1`, reset is `m-2`

That is much sharper than the old "understand the future window" version.

## 4. Auxiliary proof coordinate for `CJ`

The strongest current proof device is the constructive residue

- `rho = source_u + 1 mod m`

from:

- [d5_source_residue_refinement_049/README.md](../../artifacts/d5_source_residue_refinement_049/README.md)

Define the auxiliary quantity

- `delta = rho - (s+u+v+layer) mod m`

Important:

- `delta` is not being proposed as a theorem coordinate
- it is only a proof device for the `CJ` branch

The current `057` reduction shows:

1. on the `CJ` boundary, `delta = 0`
2. on a noncarry `CJ` state, one `CJ` step sends you to a flat successor with
   `delta = m-2`
3. therefore the `CJ` reset law follows if one can prove the flat-corner law
   for flat states with `delta = m-2`

That is the key reduction in:

- [d5_CJ_uniform_proof_progress_057.md](./d5_CJ_uniform_proof_progress_057.md)

and is compute-supported through `m = 23` by:

- [d5_CJ_flat_corner_support_057a/README.md](../../artifacts/d5_CJ_flat_corner_support_057a/README.md)

## 5. Flat-corner lemma

The flat-corner law is the current smallest positive target.

For flat states, the checked one-step law is:

- `delta = 1 -> next epsilon4 = wrap`
- `2 <= delta <= m-3 -> next epsilon4 = flat`
- `delta = m-2 -> next epsilon4 = other` iff `s = 2`, else `flat`

From this, the checked flat countdown law follows:

- `tau = delta`
- except at the corner `(s, delta) = (2, m-2)`, where `tau = 1`

Then `CJ` becomes immediate:

- every noncarry `CJ` state lands in a flat state with `delta = m-2`
- if current `s = 1`, then successor has `s = 2`, so reset is `1`
- otherwise successor has `s != 2`, so reset is `m-2`

This extension now checks exactly on

- `m = 13,15,17,19,21,23`

with packaged support in:

- [analysis_summary.json](../../artifacts/d5_CJ_flat_corner_support_057a/data/analysis_summary.json)
- [flat_corner_extension_checks_057a.json](../../artifacts/d5_CJ_flat_corner_support_057a/data/flat_corner_extension_checks_057a.json)
- [flat_tau_formula_extension_057a.json](../../artifacts/d5_CJ_flat_corner_support_057a/data/flat_tau_formula_extension_057a.json)
- [CJ_delta_reduction_extension_057a.json](../../artifacts/d5_CJ_flat_corner_support_057a/data/CJ_delta_reduction_extension_057a.json)

So the current best positive route for `CJ` is:

> prove the flat-corner one-step law uniformly in odd `m`.

## 6. Phase-machine hypothesis

Here is the actual "jump hypothesis" now worth testing.

### Hypothesis

On the active best-seed branch, the boundary/reset mechanism is governed by a
small phase machine. The visible phase is not the whole theorem object, but a
derived scalar that organizes the event classes and the flat evolution.

The current best candidate is:

- `kappa = q + s + v + layer mod m`

### Working observations

These are currently internal checked observations from local validation on
`m = 5,7,9,11,13`. They are not yet packaged as a separate artifact, so they
should be treated as working support rather than part of the formal theorem
chain.

Observed pattern:

- `wrap` occurs at `kappa = 0`
- `carry_jump` occurs at `kappa = 1`
- `other` splits as:
  - subtype `(1,0,0,0)` at `kappa = 2`
  - subtype `(0,0,1,0)` at `kappa = 3`
- each flat step increments `kappa` by `+1`
- a noncarry `CJ` step lands in a flat state with `kappa = 2`

If this phase picture is uniform, then the boundary theorem may be hiding a
very small phase machine behind the current coordinates.

### Why this matters

The `delta` reduction explains `CJ` in a clean way, but `delta` is tied to the
auxiliary residue `rho`.

The `kappa` hypothesis points to something better:

- a theorem-side phase description using current visible variables
- a possible common explanation for both `CJ` and `OTH`

So the current best conceptual jump is:

> `CJ` is already a corollary of the flat-corner lemma in `delta`, and that
> lemma itself may be the visible part of a more intrinsic `kappa`-phase
> machine.

## 7. What another mathematician could productively try

Here are the highest-value proof tasks.

### Task A. Prove the flat-corner lemma directly

This is the most concrete current target.

Try to derive the flat one-step event law uniformly in odd `m`, using:

- the grouped-delta rules
- the raw coordinate identities already extracted
- the fact that `delta` decreases by `1` on flat steps

If successful, this should finish `CJ`.

### Task B. Prove the `kappa` phase machine

Try to prove some or all of:

- `wrap <-> kappa = 0`
- `CJ <-> kappa = 1`
- `OTH` subtype split by `kappa = 2,3`
- flat steps satisfy `kappa -> kappa+1`

If this works, it may unify the `CJ` and `OTH` analyses conceptually.

### Task C. Derive `CJ` from `kappa` instead of `delta`

If `kappa` is the right intrinsic phase, try to rederive the noncarry `CJ`
dichotomy from first hitting times of the next nonflat phase. This would be a
cleaner theorem story than using `rho`-based proof auxiliaries.

### Task D. Reassess `OTH` through the same phase picture

Current `OTH` still depends on subtype reduction and the checked discriminator
`r = layer + 3((s-u)-1)`.

The right question is:

> is `OTH` genuinely a second mechanism, or is it just another face of the
> same phase machine?

## 8. What not to do

At this stage, the following are probably weak directions:

- reopening broad search over tiny controllers
- searching for new theorem objects instead of working with `(B,tau,epsilon4)`
- promoting `rho` to the theorem statement
- treating checked formulas as theorem substitutes rather than proof clues

The current program is already narrow enough that the right next move is proof
compression, not search widening.

## 9. Honest status

What is theorem-shaped now:

- `d=5` has a stable theorem object
- the boundary theorem is reduced to branch lemmas
- `CJ` is reduced further to one auxiliary flat-corner lemma
- the flat-corner reduction is compute-supported through `m = 23`

What is not yet proved:

- the flat-corner lemma uniformly in odd `m`
- the `OTH` branch uniformly in odd `m`
- the phase-machine hypothesis itself

So the situation is:

> most of the problem compression has happened; the main remaining work is now
> one or two small conceptual lemmas, not another global search.
