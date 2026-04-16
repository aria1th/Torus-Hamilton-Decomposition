# D5 Lean formalization documentation log

## 현재 기준

- 날짜: 2026-04-05
- 현재 단계: **실행 전 계획 고정**
- 기준 입력: round 1 skeleton / round 1 report / current status ledger

## 이번 계획에서 이미 고정한 결정

1. `R_re`와 `R_q`는 Lean에서 서로 다른 object로 시작한다.
2. common stable theorem과 low-seed appendix는 파일 단위로 분리한다.
3. checked packet은 certificate layer로 보낸다.
4. 첫 proof-import 우선순위는 `Core -> d5_300 -> common stable packet`이다.
5. denom-16, denom-8 portal sector는 동일한 proof mode로 묶지 않는다.

## milestone 상태판

| Milestone | 상태 | 메모 |
|---|---|---|
| M0 | planned | 저장소 부트스트랩 + taxonomy 고정 |
| M1 | planned | core definitions freeze |
| M2 | planned | canonical theorem statement extraction |
| M3 | planned | `d5_300` `H_m` master hinge proof import |
| M4 | planned | common theorem floor + stable packet |
| M5 | planned | certificate layer 구축 |
| M6 | planned | denom-16 / denom-8 portal split |
| M7 | planned | post-hinge / stitching / RouteY frontier |
| M8 | planned | 최종 wiring + audit |

## 현재까지 알려진 핵심 gap

### A. definition gap

- `R_re`, `R_q`의 정확한 Lean domain/codomain
- stable residual core predicate
- portal alphabet / ordered portal word object
- `J_0`, `eta_0`의 Lean 표현 방식

### B. statement extraction gap

- accepted odd-`m` backbone의 exact theorem signature
- `T0--T4`의 exact statement bundle
- graph-side theorem 중 certificate-backed 항목의 경계
- RouteY lane theorem signature 정리

### C. certificate gap

- `d5_289` checked no-go cycle data
- `d5_297/298/299` late atlas/routing/promotions
- common quotient compression checker shape
- denom-16 shared-lexicon interior table representation
- denom-8 `r = 8s` checked packet data representation

### D. genuine frontier gap

- post-hinge double-top exit theorem
- `H_m -> B_m` stitching
- `B`-active / gate branch
- RouteY seam-glued reduced machine final global cycle theorem

## source-of-truth 파일 목록

이 번들의 상위 입력은 아래 두 파일이다.

- `upstream_round1_report.md`
- `upstream_status_ledger.csv`

Codex 작업 중 새로운 판단이 생기면, 위 입력을 덮어쓰지 말고 이 로그에 추가한다.

## 업데이트 템플릿

### [DATE / SESSION]

**milestone**:

**edited files**:

**new definitions/statements**:

**status changes**:

**new gaps/blockers**:

**validation commands**:

**result**:

**next step**:

### [2026-04-05 / tracker-import-sync]

**milestone**:
tracking/bootstrap sync before local M0 path reconciliation

**edited files**:
`formal/TorusD5/FullCoordinates.lean`,
`formal/TorusD5/memory.md`,
`formal/TorusD5/d5-plan.md`,
imported working docs in `formal/TorusD5/`,
selected common notes in `formal/TorusD5/common_ref/`

**new definitions/statements**:
no new theorem-side objects yet; only tracking docs and imported source notes

**status changes**:
the current conservative `TorusD5` base-model library is verified green locally;
the imported `lean_worklist.csv` remains upstream-shaped and still needs a local
path/namespace reconciliation step in M0

**new gaps/blockers**:
main blocker is the mismatch between the imported future `D5/...` tree and the
already buildable local `TorusD5/...` namespace

**validation commands**:
`cd formal && source "$HOME/.elan/env" && lake build TorusD5`

**result**:
success; build completed and the prior `FullCoordinates.lean` linter warning was
removed during the sync

**next step**:
M0 local path reconciliation, then M1 theorem-side core object freeze

### [2026-04-05 / symbolic-scaffold-pass]

**milestone**:
M0 complete, plus partial M1/M3/M4/M5/M7 symbolic scaffold

**edited files**:
`formal/TorusD5.lean`,
`formal/TorusD5/Core/Objects.lean`,
`formal/TorusD5/Core/Interfaces.lean`,
`formal/TorusD5/Canonical/Residual/HmCore.lean`,
`formal/TorusD5/Common/M15r9/TheoremFloor.lean`,
`formal/TorusD5/Common/M15r9/StablePacket.lean`,
`formal/TorusD5/Common/M15r9/SeedCases.lean`,
`formal/TorusD5/Certificates.lean`,
`formal/TorusD5/Gaps.lean`,
`formal/TorusD5/memory.md`,
`formal/TorusD5/d5-plan.md`

**new definitions/statements**:
- theorem-side visible-state / `SigmaZero` / `H_m` / `B_m` objects
- separate `R_re` / `R_q` interface shells
- `beta`, `betaTilde`, `Xi`, `F_m`, `P_m` interface shapes
- symbolic `d5_300` effective phase / hinge-profile target object
- common `m = 15r + 9` theorem-floor predicate and stable-packet time formulas
- Type A / Type B packet shells and formalized `x = 1` boundary difference
- low-seed / outlier appendix split
- certificate and frontier registries

**status changes**:
the local module-layout blocker is resolved in favor of nested `TorusD5/...`
modules; `TorusD5` now builds with the new theorem-side symbolic scaffold

**new gaps/blockers**:
- raw `IsCommonModulus m := ∃ r, m = 15r + 9` does not imply oddness; the odd
  common branch needs an additional parity restriction on `r` or a stronger
  predicate
- `R_re` / `R_q` still have abstract carriers because the exact domain/codomain
  theorem boundary is not frozen enough
- `HmCore` currently packages the master hinge theorem boundary symbolically; it
  does not yet import the full dynamic proof

**validation commands**:
- `cd formal && source "$HOME/.elan/env" && lake build TorusD5.Core.Objects TorusD5.Core.Interfaces`
- `cd formal && source "$HOME/.elan/env" && lake build TorusD5.Canonical.Residual.HmCore`
- `cd formal && source "$HOME/.elan/env" && lake build TorusD5.Common.M15r9.TheoremFloor TorusD5.Common.M15r9.StablePacket TorusD5.Common.M15r9.SeedCases`
- `cd formal && source "$HOME/.elan/env" && lake build TorusD5`

**result**:
all commands succeeded; the D5 library remains green with the new scaffold in
place

**next step**:
start exact statement extraction for the first closed theorem packet, preferably
the accepted odd-`m` backbone or the explicit `d5_300` hinge theorem statement
layer

### [2026-04-05 / proof-priority-reassessment]

**milestone**:
priority reassessment note after the first compileable theorem-side scaffold

**edited files**:
`formal/TorusD5/proof_priority_reassessment_2026-04-05.md`,
`formal/TorusD5/memory.md`,
`formal/TorusD5/d5-plan.md`

**new definitions/statements**:
no new Lean definitions; added a proof-order note separating main frontier lane
from secondary verification lanes

**status changes**:
the recommended main Lean lane is now explicitly:
`286/300 -> post-hinge/stitching interface -> certificate packaging`,
with accepted odd-`m` backbone and common stable packet kept as secondary but
important verification lanes

**new gaps/blockers**:
none new at code level; this note mainly reclassifies proof priority

**validation commands**:
none; markdown-only update

**result**:
priority note recorded and linked from the local D5 handoff docs

**next step**:
follow the new note by extracting exact theorem statements for `d5_286` and
`d5_300` before spending the main proof budget on the common lane
