# D5 Lean Plan

## Completed Baseline

- [x] Read `tmp/lean_bundle` and selected the reusable D5 Lean planning docs.
- [x] Imported the Codex working docs into `formal/TorusD5/`.
- [x] Imported the two immediate common-reference notes into
  `formal/TorusD5/common_ref/`.
- [x] Verified the current local target with
  `cd formal && source "$HOME/.elan/env" && lake build TorusD5`.
- [x] Kept the existing conservative `TorusD5` base-model library green.
- [x] Cleared the current `FullCoordinates.lean` linter warning during sync.
- [x] Chose the local module policy: keep the `TorusD5` root and add nested
  theorem-side modules under it.
- [x] Added a first compileable theorem/certificate/frontier scaffold for D5.

## Current Lean Progress

- [x] Extracted D5 base coordinates and maps (`Basic.lean`)
- [x] Slice/full-coordinate embedding and recovery (`FullCoordinates.lean`)
- [x] Shifted carry / first-return presentation (`FirstReturn.lean`)
- [x] Grouped-base iterate and period package (`GroupedReturn.lean`)
- [x] Symbolic grouped cocycle layer (`Cocycle.lean`)
- [x] Spec predicates and extensional equality lemmas (`Specs.lean`)
- [x] Exact deterministic quotient abstraction (`ExactQuotient.lean`)
- [x] Theorem-side D5 object/interface shell (`Core/Objects.lean`, `Core/Interfaces.lean`)
- [x] Symbolic `H_m` / `B_m` and `d5_300` hinge-profile shell (`Canonical/Residual/HmCore.lean`)
- [x] Common theorem-floor and stable-packet symbolic shell (`Common/M15r9/*.lean`)
- [x] Checked certificate / frontier registries (`Certificates.lean`, `Gaps.lean`)
- [ ] Canonical theorem statement extraction for the closed RoundY packages
- [ ] `d5_300` `H_m` master hinge proof import
- [ ] Common `m = 15r + 9` theorem floor and stable-packet theorem import
- [ ] Checked packet certificate layer
- [ ] Denom-16 / denom-8 portal split
- [ ] Post-hinge / RouteY frontier registry
- [ ] Final D5 wiring and audit

## Ordered Next Steps

1. [ ] M0. Reconcile local paths before any theorem-side coding
   - Local policy chosen: use nested `TorusD5/...` modules rather than a new
     parallel `D5/...` tree.
   - Remaining cleanup: reflect that mapping more explicitly in the worklist if
     the upstream CSV is kept as a live local tracker.
   - Keep `lake build TorusD5` green while refining that mapping.

2. [ ] M1. Freeze theorem-side core objects
   - Introduce exact local definitions/interfaces for
     `State5`, `SigmaZero`, `Visible4`, `hiddenB`, `Hm`, `Bm`,
     residue-family labels, `R_re`, `R_q`, `beta`, `betaTilde`, `Xi`, `Fm`,
     and `Pm`.
   - Preserve distinct names and types for `R_re` and `R_q`.
   - Any unavoidable placeholder must carry `status`, `sourceDoc`, and `gap`.
   - Current state: compileable symbolic object/interface shells exist, but the
     concrete theorem-side event-map and quotient domains are not frozen yet.

3. [ ] M2. Extract canonical closed-package theorem signatures
   - Odd-`m` backbone
   - `T0--T4`
   - graph-side closed branches
   - `d5_286` promoted collar local dynamics
   - Separate theorem statements from certificate-backed statements.

4. [ ] M3. Import `d5_300` as the first real proof target
   - Build the `H_m` first-hinge statement around exact Lean objects.
   - Track missing lower-to-hinge lemmas explicitly instead of hiding them.

5. [ ] M4. Formalize the common `m = 15r + 9` stable lane
   - Use `common_ref/...FULL_STABLE...md` as the main exact-classification note.
   - Keep low seeds `39,69,129` and outlier `9` outside the stable theorem file.
   - Do not collapse `R_re` and `R_q` anywhere in this lane.
   - Current state: times, Type A / Type B shells, the `x=1` boundary
     difference, and seed appendix separation are compileable; the actual
     stable residual-core theorem is not yet imported as a proof.

6. [ ] M5. Build the certificate layer
   - Route checked-only material such as `d5_289`, `d5_297/298/299`,
     quotient compression, and table-driven portal packets into certificate
     namespaces.
   - Do not promote checked packets to theorem namespace early.

7. [ ] M6. Split the portal sector cleanly
   - Keep denominator-`16` and denominator-`8` work separate.
   - Promote only the handwritten/exact pieces with stable statements.
   - Leave remaining table-driven transport/compression parts as certificates or
     open gaps.

8. [ ] M7. Keep the frontier honest
   - Post-hinge double-top exit
   - `H_m -> B_m` stitching
   - `B`-active / gate branch
   - RouteY seam-glued global cycle theorem

9. [ ] M8. Final wiring
   - Full import audit
   - Placeholder audit
   - Full build

## Session Rule

- Always read `plans.md`, `implement.md`, `documentation.md`, and
  `lean_worklist.csv` before resuming work.
- For proof-order emphasis, also read
  `proof_priority_reassessment_2026-04-05.md`.
- Work one milestone at a time.
- Update `documentation.md` at the end of each milestone.
