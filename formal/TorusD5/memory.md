# D5 Lean Memory

## Current State

- Date: `2026-04-05`
- Verified green build:
  - `cd formal && source "$HOME/.elan/env" && lake build TorusD5`
- The current buildable Lean code in `formal/TorusD5/` is still the conservative
  extracted-model layer from the old `017` preparation branch, now extended by
  a theorem-side symbolic scaffold:
  - `Basic.lean`
  - `FullCoordinates.lean`
  - `FirstReturn.lean`
  - `GroupedReturn.lean`
  - `Cocycle.lean`
  - `Specs.lean`
  - `ExactQuotient.lean`
  - `Core/Objects.lean`
  - `Core/Interfaces.lean`
  - `Canonical/Residual/HmCore.lean`
  - `Common/M15r9/TheoremFloor.lean`
  - `Common/M15r9/StablePacket.lean`
  - `Common/M15r9/SeedCases.lean`
  - `Certificates.lean`
  - `Gaps.lean`
- This layer formalizes:
  - the extracted section/grouped-return coordinates,
  - the slice/full-coordinate interface,
  - the shifted first-return presentation,
  - the grouped-base period package,
  - the symbolic cocycle layer,
  - the abstract spec/equality interfaces,
  - the exact deterministic quotient abstraction,
  - theorem-side visible-state / `H_m` / `B_m` objects,
  - separate interface shells for `R_re` and `R_q`,
  - a symbolic `d5_300` hinge-profile target object,
  - common `m = 15r + 9` stable-packet times and Type A / Type B packet shells,
  - certificate/frontier registries.
- This layer does **not** yet formalize:
  - theorem-side D5 objects such as `R_re`, `R_q`, `Hm`, `Bm`,
  - canonical closed-package theorem statements,
  - `d5_300` hinge proofs,
  - common `m = 15r + 9` stable-packet theorems,
  - certificate layers for checked packets,
  - post-hinge/global frontier closure.

## Imported Working Docs

Imported from `tmp/lean_bundle/d5_codex_plan_bundle_2026-04-05.zip`:

- `plans.md`
- `implement.md`
- `documentation.md`
- `lean_worklist.csv`
- `upstream_round1_report.md`
- `upstream_status_ledger.csv`
- `codex_session_prompt.md`

Imported from `tmp/lean_bundle/d5_common_proof_progress_bundle_2026-04-05.tar`:

- `common_ref/CURRENT_FRONTIER_AND_START_HERE_2026-04-05_AFTER_COMMON_FULL_STABLE_RESIDUE_SECTOR_PORTAL_PACKET_COVERAGE.md`
- `common_ref/d5_common_beta_m_15r9_all_residue_families_full_stable_packet_and_exact_classification_2026-04-04.md`

Only those two common-branch notes were pulled in locally.
The rest of the `177`-file tar remains archival in `tmp/lean_bundle/` until
M5/M6 work actually needs more portal/compression packets on disk.

Priority note:

- `proof_priority_reassessment_2026-04-05.md`

## Important Local Mismatch

- The imported plan bundle assumes a future `D5/...` module tree.
- The current repository already has a buildable `TorusD5` namespace with flat
  files under `formal/TorusD5/`.
- Local module policy is now fixed:
  keep the existing `TorusD5` root, and add new theorem-side work underneath
  nested paths such as `TorusD5/Core/...`, `TorusD5/Common/...`,
  `TorusD5/Canonical/...`.
- Do **not** rewrite the existing `TorusD5` base-model files into a parallel
  `D5/...` root unless there is a compelling later reason.

## New Audit Finding

- The raw predicate `IsCommonModulus m := ∃ r, m = 15r + 9` does **not** imply
  that `m` is odd.
- So any future theorem claiming the odd common branch must carry an extra
  parity restriction on the parameter `r`, or use a stronger predicate than
  plain `15r+9`.
- This showed up during Leanization and is now a recorded proof-boundary fact,
  not just a documentation caveat.

## Hard Rules

- Never identify `R_re` and `R_q`.
- Keep checked material out of theorem namespace until there is either a real
  proof or a checker-correctness theorem.
- Keep stable theorems separate from low-seed / outlier appendix cases.
- If an exact theorem statement cannot be extracted, record the ambiguity
  rather than inventing a Lean theorem.

## Next Handoff Order

1. Read `plans.md`, `implement.md`, `documentation.md`, and `lean_worklist.csv`.
2. Decide the local module-layout policy for M0.
3. Only after that, proceed in the order
   `Core -> d5_300 -> common stable packet -> certificate layer -> portal split`.
