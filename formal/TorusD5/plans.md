# D5 Lean formalization plan for Codex (2026-04-05)

## 목표

이번 계획의 목적은 두 가지다.

1. 현재 구조 뼈대를 Lean 프로젝트로 굳힌다.
2. 현재 `promoted theorem / checked packet / frontier`를 분리하고,
   Lean proof로 올리는 과정에서 빠지는 조각을 체계적으로 찾는다.

## 범위와 전제

- 기준 문서는 `RoundY`, `RouteY-Existence`, common `m = 15r + 9` bundle이다.
- 이번 계획은 **실행 계획**이다. 수학 자체를 새로 증명했다고 간주하지 않는다.
- 실제 repository 명칭과 import 경로는 약간 달라질 수 있다. 이 문서의 모듈명은 round 1 skeleton을 기준으로 한다.
- Lean 증명에서 문서 상태와 proof 상태를 혼동하지 않는다.

## 상태 taxonomy

각 항목은 아래 여섯 상태 중 하나를 가진다.

- `definitional`: 먼저 정확한 Lean 정의가 필요한 객체
- `promotedTheorem`: 현재 문서 기준 theorem-level로 취급하며, Lean proof로 직접 올릴 대상
- `workingTheorem`: theorem statement는 있으나 아직 upstream 정리/추출/보조정리에 의존
- `checkedCertificate`: exact/checked/support 수준으로 문서화되었으나 theorem 승격 전 단계
- `finiteAppendix`: stable theorem과 분리해야 하는 low-seed / outlier / finite patch
- `frontier`: 아직 genuinely open인 목표

## proof mode taxonomy

각 항목은 아래 네 방식 중 하나를 택한다.

- `direct`: 수기 증명을 그대로 Lean proof로 이식
- `statement-first`: 우선 exact statement만 고정하고 proof는 후속 milestone으로 넘김
- `certificate-first`: finite data + checker correctness theorem으로 승격
- `frontier-only`: 정의와 목표 statement만 두고 open gap로 남김

## 절대 고정할 경계

1. `R_re`와 `R_q`는 다른 return surface다. 하나의 정의로 합치지 않는다.
2. `checkedPacket`을 theorem namespace에 넣지 않는다.
3. stable theorem과 `39,69,129` 및 `9` 같은 seed/outlier appendix를 분리한다.
4. `axiom` 또는 `constant` placeholder가 남아 있으면 그 사실을 ledger와 log에 명시한다.
5. source statement가 불명확하면 theorem 이름만 만들지 말고 정확한 ambiguity를 적는다.

## 마일스톤

### M0. 저장소 부트스트랩 + 상태 체계 고정

**목표**
- round 1 skeleton을 Codex가 실제로 다룰 수 있는 Lean repository 구조로 옮긴다.
- 상태 taxonomy / proof mode taxonomy / 로그 체계를 고정한다.

**주요 파일**
- `D5.lean`
- `D5/Core/Objects.lean`
- `D5/Core/Interfaces.lean`
- `docs/plans.md` 또는 repository root의 `plans.md`
- `documentation.md`
- `lean_worklist.csv`

**산출물**
- 컴파일 가능한 최소 프로젝트 구조
- 상태 분류가 붙은 worklist
- Codex 운영 규칙이 적힌 `implement.md`

**acceptance criteria**
- 기본 import graph가 깨지지 않는다.
- 상태 label과 proof mode label이 문서/ledger/코드 주석에서 동일한 철자를 쓴다.
- `R_re`, `R_q`, stable theorem vs seed appendix 분리 원칙이 문서에 반영된다.

**validation commands**
- `lake build`
- `grep -R "Rre\|Rq" D5`
- `grep -R "axiom\|constant" D5 | sort`

---

### M1. Core definitions freeze

**목표**
- Lean 전체의 공용 객체를 정확히 정의한다.

**주요 파일**
- `D5/Core/Objects.lean`
- `D5/Core/Interfaces.lean`

**정의 대상**
- `State5`
- `sigma`
- `SigmaZero`
- `Visible4`
- `hiddenB`
- `Hm`
- `Bm`
- common residue-family labels
- `R_re`
- `R_q`
- `beta`, `betaTilde`, `Xi`, `Fm`, `Pm`의 interface shape

**빠진 조각을 찾는 포인트**
- `R_re`, `R_q`의 정확한 domain/codomain이 문서상 완전히 확정되는가?
- `betaTilde`가 visible line 위의 map인지 quotient surface 위의 map인지 구별이 필요한가?
- `Hm`, `Bm` 정의가 source notes의 표기와 정확히 일치하는가?

**acceptance criteria**
- 핵심 객체는 `def`/`structure` 수준으로 존재한다.
- `R_re`와 `R_q`는 서로 다른 이름과 타입으로 들어간다.
- `Core` 모듈의 placeholder는 모두 주석으로 source/gap가 연결된다.

**validation commands**
- `lake build D5.Core.Objects D5.Core.Interfaces`
- `grep -R "TODO\|GAP" D5/Core`

---

### M2. Canonical theorem statement extraction

**목표**
- 이미 닫힌 canonical 블록의 exact Lean statement를 문서에서 뽑아낸다.

**주요 파일**
- `D5/Canonical/Backbone.lean`
- `D5/Canonical/FrontEnd.lean`
- `D5/Canonical/GraphSide.lean`
- `D5/Canonical/Residual/PromotedCollar.lean`

**우선 대상**
- odd-`m` backbone
- `T0--T4`
- graph-side closed branches
- nonresonant `P_m` classification
- `d5_286` promoted collar active-burst theorem

**빠진 조각을 찾는 포인트**
- theorem statement가 archive 안에서 한 파일로 뽑히는지, status note를 종합해야 하는지
- certificate-backed theorem으로 두어야 하는 항목이 무엇인지
- quantifier, modulus side-condition, parity condition이 정확히 무엇인지

**acceptance criteria**
- 각 target theorem에 대해 Lean signature가 생긴다.
- 각 theorem 주석에 source doc와 현재 status가 명시된다.
- theorem과 certificate-backed theorem이 구분된다.

**validation commands**
- `lake build D5.Canonical.Backbone D5.Canonical.FrontEnd D5.Canonical.GraphSide D5.Canonical.Residual.PromotedCollar`
- `grep -R "sourceDoc\|status:" D5/Canonical`

---

### M3. `d5_300` Hm master hinge proof import

**목표**
- `H_m` first-hinge master theorem을 첫 실증명 타깃으로 올린다.

**주요 파일**
- `D5/Canonical/Residual/HmCore.lean`
- 필요 시 `D5/Canonical/Residual/HmLemmas.lean` 신설

**우선 정리 대상**
- `H_m = {(a,0,0,e)}`의 first hinge profile
- `J_0`와 `eta_0` 분류식
- lower-to-hinge chain과 hinge statement의 연결

**빠진 조각을 찾는 포인트**
- `Xi`, `Fm`의 exact meaning
- `J_0`, `eta_0`를 Lean에서 함수로 둘지 relation으로 둘지
- proof import에 필요한 lower lemmas가 `286`/`289`/`300` 중 어디에서 오는지

**acceptance criteria**
- `HmCore`의 핵심 정리가 `axiom`이 아닌 theorem/proof로 들어간다.
- proof에서 필요한 보조정리와 아직 부족한 부분이 documentation에 분리 기록된다.
- post-hinge / double-top 부분은 따로 frontier로 남긴다.

**validation commands**
- `lake build D5.Canonical.Residual.HmCore`
- `grep -R "HmCore" documentation.md`

---

### M4. Common theorem floor + stable packet exact classification

**목표**
- common `m = 15r + 9` lane의 theorem floor와 stable packet exact classification을 정리한다.

**주요 파일**
- `D5/Common/M15r9/TheoremFloor.lean`
- `D5/Common/M15r9/StablePacket.lean`
- `D5/Common/M15r9/SeedCases.lean` (신설 권장)

**우선 정리 대상**
- `R_re` / `R_q` separation
- zero-drift domain / packet-excised source forest / exact seed set statements
- high-side quotient return / low-side collar closure statements
- all-residue full stable packet and exact classification
- Type A / Type B partition

**빠진 조각을 찾는 포인트**
- stable residual core의 정확한 Lean predicate
- shared first-rung packet을 list/fintype/finite set 중 무엇으로 둘지
- `39,69,129` 및 `9`를 theorem 본문에서 어떻게 분리할지

**acceptance criteria**
- theorem floor의 핵심 statement가 모두 Lean 서명으로 정리된다.
- stable packet theorem과 low-seed appendix가 다른 파일로 분리된다.
- `R_re`와 `R_q`가 common 모듈 어디에서도 동일시되지 않는다.

**validation commands**
- `lake build D5.Common.M15r9.TheoremFloor D5.Common.M15r9.StablePacket D5.Common.M15r9.SeedCases`
- `grep -R "Rre.*Rq\|Rq.*Rre" D5/Common/M15r9`

---

### M5. checked packet certificate layer 구축

**목표**
- checked/exact/support 패킷을 theorem 계층과 분리한 certificate layer를 만든다.

**주요 파일**
- `D5/Certificates/README.lean` 또는 `D5/Certificates.lean`
- `D5/Canonical/Residual/Certificates.lean` (신설 권장)
- `D5/Common/M15r9/Compression.lean`
- 필요 시 `D5/Common/M15r9/Certificates/*.lean`

**certificate로 분리할 대상**
- `d5_289`
- `d5_297/298/299`
- common channel quotient compression
- denominator-16 shared-lexicon interior table
- denominator-8 checked portal packet

**빠진 조각을 찾는 포인트**
- finite data를 Lean에 어떻게 입력할지
- checker correctness theorem의 shape
- certificate-backed theorem과 raw checked data의 경계를 어디에 둘지

**acceptance criteria**
- checked packet이 theorem namespace에서 빠진다.
- certificate 구조체/record와 source doc link가 생긴다.
- 어떤 항목이 direct proof가 아니라 certificate-first인지 worklist에 표시된다.

**validation commands**
- `lake build D5.Common.M15r9.Compression`
- `grep -R "checkedCertificate" D5 documentation.md`
- `grep -R "axiom" D5/Common D5/Canonical/Residual | sort`

---

### M6. Portal sector split: denom-16 / denom-8

**목표**
- portal 쪽을 theorem/certificate/frontier로 다시 쪼갠다.

**주요 파일**
- `D5/Common/M15r9/Portal/Denom16.lean`
- `D5/Common/M15r9/Portal/Denom8.lean`

**세부 과제**
- denom-16 `r = 16u + 6, 14`: promoted local theorem lane
- denom-16 `r = 16u + 2, 10`: shared lexicon + finite interior table lane
- denom-8 `r = 8s`: checked portal packet lane
- denom-8 `r = 8s + 4`: four master tapes + 11 seam laws + 17 exit laws lane

**빠진 조각을 찾는 포인트**
- `501` universal interior source types를 finite data로 둘지 compression lemma로 둘지
- `r = 8s + 4`의 네 master tape transport theorem을 직접 증명할 수 있는지
- portal alphabet / ordered portal word의 정확한 object 설계

**acceptance criteria**
- 네 sector가 같은 status로 뭉개지지 않는다.
- `r = 8s + 4`의 남은 진짜 gap이 master tape transport 하나라는 점이 코드/문서에 반영된다.
- denom-16 `2/10`과 denom-8 `8s`는 theorem이 아니라 certificate 또는 explicit-packet lane으로 표시된다.

**validation commands**
- `lake build D5.Common.M15r9.Portal.Denom16 D5.Common.M15r9.Portal.Denom8`
- `grep -R "MasterTape\|portal" D5/Common/M15r9/Portal`

---

### M7. Post-hinge / stitching / parallel lane 정리

**목표**
- 실제로 아직 open인 것들을 frontier obligations로 정리한다.

**주요 파일**
- `D5/Canonical/Residual/PostHinge.lean`
- `D5/RouteYExistence/GenericLate.lean`
- `D5/Gaps.lean`

**우선 대상**
- post-hinge double-top exit theorem
- `H_m -> B_m` stitching
- `B`-active / gate branch
- RouteY seam-glued reduced machine global cycle theorem

**빠진 조각을 찾는 포인트**
- 현재 genuinely open인 것과 merely unformalized인 것을 구별하는 기준
- RouteY lane에서 canonical main proof에 필요한 산술 core가 무엇인지

**acceptance criteria**
- open frontier는 theorem처럼 선언되지 않는다.
- 각 frontier 항목마다 dependency와 blocker가 붙는다.
- `Gaps.lean` 또는 대응 문서에서 전체 남은 조각이 한 곳에 모인다.

**validation commands**
- `lake build D5.RouteYExistence.GenericLate D5.Canonical.Residual.PostHinge D5.Gaps`
- `grep -R "frontier" documentation.md D5/Gaps.lean`

---

### M8. 최종 wiring + audit

**목표**
- 현재까지 formalized / certificated / frontier를 한 프로젝트로 묶고 audit한다.

**주요 파일**
- `D5.lean`
- `D5/MainTheorem.lean`
- `documentation.md`
- `lean_worklist.csv`

**acceptance criteria**
- 모든 모듈이 status와 proof mode를 가진다.
- source doc가 빠진 theorem이 없다.
- temporary placeholder 목록이 documentation과 grep 결과에서 일치한다.
- 전체 build가 돈다.

**validation commands**
- `lake build`
- `grep -R "axiom\|constant" D5 | sort`
- `grep -R "TODO\|GAP" D5 documentation.md | sort`

## 권장 실행 순서

기본 순서는 `M0 -> M1 -> M2 -> M3 -> M4 -> M5 -> M6 -> M7 -> M8`이다.

다만 `M1`이 끝난 뒤에는 다음 두 갈래를 병렬로 진행할 수 있다.

- Lane A: `M2 -> M3` (canonical closed theorem lane)
- Lane B: `M4 -> M5 -> M6` (common theorem + certificate lane)

`M7`과 `M8`은 앞선 두 lane의 결과를 모은 뒤 진행한다.

## 승격 규칙 (promotion gate)

어떤 항목도 아래 다섯 조건 없이 `promotedTheorem`으로 승격하지 않는다.

1. exact Lean statement가 있다.
2. source doc가 코드 주석과 documentation에 적혀 있다.
3. proof mode가 `direct` 또는 `certificate-first`로 고정되어 있다.
4. validation command가 있다.
5. low-seed / outlier / frontier가 theorem 본문 밖으로 분리돼 있다.

## milestone 종료 시 반드시 남길 기록

매 milestone 종료 시 `documentation.md`에 아래를 남긴다.

- 오늘 끝낸 파일
- 새로 확정된 정의/정리 statement
- 아직 불명확한 기호/조건
- 새로 드러난 gap
- 사용한 validation command와 결과
- 다음 milestone에 넘기는 blocker
