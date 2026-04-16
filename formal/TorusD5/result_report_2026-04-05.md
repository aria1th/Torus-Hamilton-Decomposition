# D5 Lean Result Report (2026-04-05)

## Scope

This pass aimed at the two active Lean goals:

1. move already-closed proof content into compileable Lean-facing objects for
   verification work;
2. convert live frontier support into symbolic / certificate / gap layers so
   missing pieces become explicit instead of staying implicit in notes.

## What Was Added

### Verified compileable scaffold

- `Core/Objects.lean`
  - theorem-side visible-state coordinates `(a,c,d,e)`
  - `SigmaZero`, `hiddenB`, `H_m`, `B_m`
  - common residue-family and stable-geometry enumerations
- `Core/Interfaces.lean`
  - distinct interface shells for `R_re` and `R_q`
  - interface shapes for `beta`, `betaTilde`, `Xi`, `F_m`, `P_m`
  - exact quotient realization shell
- `Canonical/Residual/HmCore.lean`
  - symbolic `d5_300` objects:
    `J_0`, `η_0`, predicted first-hinge height, predicted `Xi`
  - compileable hinge-profile interface
- `Common/M15r9/TheoremFloor.lean`
  - common-lane predicate `IsCommonModulus`
  - theorem-floor package shell
  - arithmetic facts needed to separate the odd branch correctly
- `Common/M15r9/StablePacket.lean`
  - the seven first-rung time formulas
  - Type A / Type B packet predicates
  - formal proof that the geometric difference between Type A and Type B is the
    boundary leaf `x = 1`
- `Common/M15r9/SeedCases.lean`
  - low-seed and outlier appendix separation
- `Certificates.lean`
  - checked-certificate shell
  - promoted-collar checked no-go ledger packaging
- `Gaps.lean`
  - explicit frontier registry

### Tracking updates

- `memory.md` now records the local module policy and the new audit finding.
- `d5-plan.md` now reflects the completed local path reconciliation and the new
  compileable symbolic scaffold.
- `documentation.md` contains a session log for this pass.

## What Is Now Actually Verified In Lean

- The existing conservative `017` extracted-model layer still builds.
- The theorem-side `H_m` / `B_m` objects now exist as Lean definitions.
- `R_re` and `R_q` are formally separated at the type/interface level.
- The common stable-packet time palette for `m = 15r + 9` is checked by Lean.
- The Type A / Type B packet split is encoded, and the “only real difference is
  whether `x = 1` survives” claim is now formalized as compileable lemmas.
- The seed appendix is separated from the stable lane in code, not just in
  prose.

## Important New Finding

- The naive predicate
  `IsCommonModulus m := ∃ r, m = 15r + 9`
  is too weak for the odd common branch.
- Lean exposed the issue immediately:
  this predicate alone does **not** imply that `m` is odd.
- So future common-lane theorem statements must carry either:
  - a parity condition on `r`, or
  - a stronger odd-common predicate.

This is a real proof-boundary clarification, not a cosmetic note.

## What Remains Symbolic

- `R_re` / `R_q` carriers are still abstract.
- `HmCore` packages the `d5_300` hinge theorem target, but not the full dynamic
  proof import.
- The common stable-packet file encodes the exact classification boundary and
  arithmetic shell, but not yet the full stable residual-core theorem proof.
- Checked material remains in certificate form; it has not been falsely
  promoted.

## Validation

Executed successfully:

```bash
cd formal
source "$HOME/.elan/env"
lake build TorusD5
```

## Recommended Next Step

The next best proof-bearing target is:

1. freeze the first exact theorem statement extraction for a genuinely closed
   packet;
2. then import either:
   - the accepted odd-`m` backbone statement layer, or
   - the full `d5_300` master hinge theorem statement layer
     on top of the new `HmCore` objects.
