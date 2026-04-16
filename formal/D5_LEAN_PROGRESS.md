# D5 Lean Progress

Status note for the `d=5` Lean preparation branch.

Current scope:

- formalize only the safe base-model layer extracted from
  `artifacts/d5_return_map_model_017/`
- avoid committing to any unreviewed closed form for the grouped cocycle
- prepare the exact theorem boundaries that later witness proofs should target

Companion tracking docs:

- `TorusD5/memory.md`
- `TorusD5/d5-plan.md`
- `TorusD5/result_report_2026-04-05.md`

## Done

- Added a standalone `TorusD5` Lean library entry in `formal/lakefile.toml`.
- Added umbrella import file:
  - `formal/TorusD5.lean`
- Added base extracted-model module:
  - `formal/TorusD5/Basic.lean`
  - section coordinates `(q,w,u)`
  - grouped coordinates `(w,u)`
  - abstract skew coordinates `(w,u,t)`
  - extracted first-return base map
  - extracted grouped-return base map
  - abstract grouped skew-product
- Added slice/full-coordinate module:
  - `formal/TorusD5/FullCoordinates.lean`
  - bundle-backed `S=0` slice embedding `(-q-w-v-u, q, w, v, u)`
  - coordinate recovery from a point on the `S=0` slice
  - clean-frame forgetful projections to `(q,w,u)` and `(w,u)`
- Added first-return preparation module:
  - `formal/TorusD5/FirstReturn.lean`
  - shifted coordinate `qHat = q + 1`
  - shifted carry presentation
  - proof that the raw carry slice `q = -2` matches the shifted slice
    `qHat = -1`
- Added grouped-return base module:
  - `formal/TorusD5/GroupedReturn.lean`
  - iterate formula for `(w,u) ↦ (w+1,u)`
  - exact period-`m` theorem
  - no-smaller-positive-iterate theorem on each fixed-`u` fiber
  - projection lemma for abstract grouped skew-products
- Added abstract cocycle module:
  - `formal/TorusD5/Cocycle.lean`
  - recursive cocycle accumulation along the grouped base orbit
  - exact iterate formula for the abstract grouped skew-product
  - period-`m` skew-product formula reducing to orbit cocycle sums
- Added spec layer:
  - `formal/TorusD5/Specs.lean`
  - abstract predicates for the extracted first-return law
  - abstract predicates for the grouped-return base law
  - abstract predicates for grouped skew-product projection
  - extensional lemmas reducing those specs to exact map equality
- Added abstract quotient/rigidity layer:
  - `formal/TorusD5/ExactQuotient.lean`
  - exact deterministic quotient interface for an event map
  - future-word factorization through the quotient
  - rigidity theorem:
    if future words separate states, any exact deterministic quotient is injective
  - unique coordinate descent to the quotient image
- Added theorem-side symbolic scaffold:
  - `formal/TorusD5/Core/Objects.lean`
  - `formal/TorusD5/Core/Interfaces.lean`
  - `formal/TorusD5/Canonical/Residual/HmCore.lean`
  - `formal/TorusD5/Common/M15r9/TheoremFloor.lean`
  - `formal/TorusD5/Common/M15r9/StablePacket.lean`
  - `formal/TorusD5/Common/M15r9/SeedCases.lean`
  - `formal/TorusD5/Certificates.lean`
  - `formal/TorusD5/Gaps.lean`
  - theorem/certificate/frontier separation now exists in code, not only in docs
- Added witness-target note:
  - `formal/TorusD5/THEOREM_TARGETS.md`
- Added D5 Lean frontier documentation:
  - `formal/README-D5.md`
- Updated the main Lean README to point to the D5 note.
- Verified:
  - `cd formal && source "$HOME/.elan/env" && lake build TorusD5`

## In progress

- Keep the cocycle symbolic until the mathematician has reviewed the `017`
  bundle and the next branch is fixed.
- Keep the witness side out of Lean until the exact section/coordinate
  parameterization target is fixed cleanly enough to avoid rework.
- Shift the next Lean target from “more extracted model lemmas” to the
  theorem-side bridge package:
  exact deterministic quotient for the current event map,
  grouped-base retention,
  and comparison/factor statements toward `(beta,delta)`.
- Keep `R_re` / `R_q` abstract until the exact theorem-side carrier boundary is
  frozen cleanly enough to avoid a false identification.
- Tighten the common-branch predicate before importing odd-common theorems:
  plain `m = 15r + 9` is too weak to encode oddness by itself.

## Next safe targets

1. Add the theorem-side D5 bridge interface:
   exact deterministic quotient for the current event map,
   grouped-base retention,
   and abstract factor/comparison data.
2. Add the D5-specific current-event bridge layer only after freezing the
   exact event-map target (`epsilon4` / its formal Lean avatar).
3. Start the witness side only after fixing the exact section/coordinate
   definitions that the witness proof must hit.
4. Use `FullCoordinates.lean` to state the future section parameterization
   theorem explicitly, but still stop short of encoding the full witness rule.

## Not started

- Full Lean definition of the `mixed_008` witness rule.
- Proof that the full witness induces the extracted first-return map.
- Proof that the full witness induces the grouped-return base map.
- The theorem-side componentwise/global bridge package around
  exact deterministic quotients and grouped-base retention.
- Any cocycle closed form, cohomology normalization, or one-defect normal form.
- Any formalization of the cycle-only / monodromy-only / anti-compressive
  controls.

## Mathematical caution

Nothing critical has changed mathematically in this Lean-prep branch.

So far all friction has been proof-engineering only:

- `ZMod` normalization for the shifted carry slice
- iterate bookkeeping for the grouped base

The project is still intentionally avoiding any claim stronger than the
bundle-backed `017` base-model layer.
