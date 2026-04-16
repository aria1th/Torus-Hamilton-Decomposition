# D5 Lean Proof Priority Reassessment (2026-04-05)

## 목적

이 문서는 현재 D5 증명 흐름의 최전선을 기준으로,

1. 기존 Lean 작업 우선순위를 얼마나 바꿔야 하는지,
2. 다음에 어떤 증명에 집중해야 하는지,

를 정리하는 Lean-side 우선순위 메모다.

이 문서는 `RoundY`의 canonical frontier 문서를 대체하지 않는다.
역할은 하나다:

> 현재 수학적 frontier가 이미 어디까지 닫혔는지를 반영해서,
> Lean proof/import 순서를 다시 잡는다.

기준 문서:

- `RoundY/current-frontier-and-approach.md`
- `RoundY/theorem/d5_301_resonant_pure_color1_proof_state_after_Hm_master_profile.md`
- `RoundY/theorem/d5_302_resonant_pure_color1_core_chain.md`
- `RoundY/theorem/d5_303_current_d5_proof_status_overview.md`
- `RoundY/theorem/d5_305_current_d5_status_with_routey_existence.md`
- `formal/TorusD5/result_report_2026-04-05.md`

## 한 줄 결론

우선순위 변경은 **필요하다**. 다만 전면 재작성 수준은 아니다.

기존의

`Core -> d5_300 -> common stable packet -> certificate -> portal`

순서는 “증명된 것을 Lean으로 옮긴다”는 관점에서는 나쁘지 않다.
하지만 현재 proof frontier를 반영하면, Lean의 **주력 proof budget**은
이제 common stable packet보다

- `d5_286` local dynamics,
- `d5_300` `H_m` master hinge,
- 그리고 그 다음의 **post-hinge double-top exit / `H_m -> B_m` stitching**

에 먼저 들어가야 한다.

즉, 변경 폭은 **중간 정도**다:

- `Core`와 theorem/certificate/frontier 분리 원칙은 유지한다.
- 그러나 proof import의 주축은 이제
  “closed background 대량 이식”보다
  “frontier 바로 위까지 닫힌 theorem stack의 formal stabilization”
  쪽으로 옮겨야 한다.

## 왜 우선순위를 바꿔야 하는가

현재 canonical status는 이미 다음을 말하고 있다.

1. accepted odd-`m` globalization background는 닫혀 있다.
2. front-end `T0--T4`도 닫혀 있다.
3. graph-side color-`4`, color-`3`도 닫혀 있다.
4. small odd / nonresonant residual packet도 닫힌 working block이다.
5. resonant pure color-`1` lower-to-hinge 분류도 이제 닫혀 있다.

특히 `301`, `302`, `303`의 현재 해석은 분명하다:

- live burden는 더 이상 lower-to-hinge가 아니다.
- live burden는 **post-hinge**다.

정확히는:

1. explicit double-top phase-exit theorem
2. `H_m -> B_m` stitching
3. late central/flank residual law의 theorem-level organization
4. separate `B`-active / gate branch integration

따라서 Lean이 “현재 열린 수학”에 최대한 가까운 검증 작업이 되려면,
닫힌 theorem을 옮기더라도 **frontier-adjacent closed theorem**부터
잡아야 한다.

## 우선순위 변경의 정도

### 바꾸지 말아야 하는 것

다음은 그대로 유지한다.

- `R_re`와 `R_q` 분리
- checked packet과 theorem packet 분리
- low-seed appendix와 stable theorem 분리
- exact statement가 없으면 theorem으로 승격하지 않는 원칙
- 기존 `TorusD5` base-model layer를 green으로 유지하는 원칙

즉 설계 원칙은 유지한다.

### 실제로 바꿔야 하는 것

기존 계획은 다음 두 축을 거의 같은 무게로 두고 있었다.

1. 현재 닫힌 theorem package의 Lean import
2. common `m = 15r + 9` lane의 theoremization

하지만 현재 frontier를 반영하면 이 둘은 같은 무게가 아니다.

지금은

- common stable packet theoremization은 **중요하지만 보조축**이고,
- resonant pure color-`1`의 `286 -> 300 -> post-hinge` 스택이
  **주축**이다.

그래서 작업 순서는 다음처럼 바뀌어야 한다.

## 새 권장 우선순위

### P0. 유지

`Core` freeze와 theorem/certificate/frontier 분리.

이건 이미 맞는 방향이다.
다만 이제 `Core`는 추상 준비 작업이 아니라
`286/300/post-hinge`를 받치기 위한 최소 경계 고정에 집중해야 한다.

### P1. 최우선: `d5_286` + `d5_300` theorem statement stabilization

다음 두 개가 현재 Lean의 첫 주력 증명 대상이다.

1. `d5_286` promoted-collar complete local dynamics
2. `d5_300` resonant `H_m` master hinge profile

이 둘을 먼저 잡아야 하는 이유:

- 둘 다 current frontier 바로 위의 닫힌 local theorem이다.
- 둘 다 post-hinge frontier의 입력이다.
- 둘 다 현재 만든 `HmCore` / theorem-side visible-state scaffold 위에
  자연스럽게 올라간다.

특히 `300`은 “좋은 닫힌 theorem”일 뿐 아니라,
현재 열린 문제를 한 단계 위로 밀어 올린 theorem이다.
Lean proof budget을 먼저 여기에 써야 한다.

### P2. 다음 집중: post-hinge theorem boundary의 formalization

아직 완전 증명은 아니더라도, 지금 당장 formal statement와 object는
만들어야 한다.

집중 대상:

1. double-hinge graph의 exact object
2. explicit double-top phase-exit theorem statement
3. `H_m -> B_m` stitching theorem statement
4. late central/flank residual law가 의존하는 induced-map boundary

이 단계의 목적은 “미증명 theorem을 꾸며내는 것”이 아니다.
목적은 다음과 같다.

- live frontier를 Lean에서 정확히 기술한다.
- 빠진 보조정리가 어디인지 드러낸다.
- checked ledger (`297/298/299`)가 정확히 어느 theorem boundary 아래에
  있는지 분리한다.

즉 이 단계는 frontier formalization이다.

### P3. 그 다음: `d5_289`와 late ledger의 certificate 정리

`289`, `297`, `298`, `299`는 아직 theorem-level all-`m` closure가 아니다.
그래서 여기서 할 일은 theorem 승격이 아니라:

- certificate structure 정리
- checked ledger와 theorem boundary 연결
- `F_m`, `P_m`, late routing data의 provenance 고정

이다.

이건 지금 당장 필요하다.
왜냐하면 post-hinge / stitching theorem을 적으려면,
어디까지 theorem-level이고 어디부터 checked ledger인지
경계가 명확해야 하기 때문이다.

### P4. secondary verification lane: accepted odd-`m` backbone

accepted odd-`m` backbone은 중요하다.
하지만 현재 live frontier를 직접 밀어 주는 증명은 아니다.

그래서 Lean에서는:

- statement-first import는 빨리 해도 좋다.
- 하지만 proof budget의 첫 번째 사용처로 두지는 않는다.

권장 역할은:

- library stabilization,
- theorem-side language normalization,
- later comparison object (`beta`, quotient language) 정리

이다.

즉 “먼저 formalize하면 좋은 closed theorem”이지,
“frontier를 당장 가장 많이 줄이는 theorem”은 아니다.

### P5. secondary but independent lane: common `m = 15r + 9`

common stable packet도 마찬가지다.

현재 Lean 성과는 이미 의미 있다:

- 시간 팔레트가 formalized되었고,
- Type A / Type B 분기와 `x=1` 차이가 compileable하게 들어갔다.

하지만 canonical D5 frontier는 현재 common lane가 아니라
resonant post-hinge pure color-`1` 쪽이다.

그래서 common lane의 위치는:

- “지속적으로 전진 가능한 독립 verification lane”
- “frontier-adjacent main lane는 아님”

으로 보는 것이 맞다.

## 집중해야 할 증명 목록

### A. 가장 먼저 잡아야 할 것

1. `d5_300` exact theorem statement import
2. `d5_286` exact theorem statement import
3. `HmCore`에서 symbolic shell이 아니라 theorem statement와 proof landing
   point를 정확히 고정

### B. 그 다음 바로 이어야 할 것

1. explicit double-top phase-exit theorem statement
2. `H_m -> B_m` stitching theorem statement
3. induced `F_m : H_m -> H_m` / `P_m : B_m -> B_m` theorem boundary

### C. certificate-first로 묶어야 할 것

1. `d5_289` base-section reduction / checked no-go ledger
2. `d5_297` zero-state late atlas
3. `d5_298` mod-`30` routing note
4. `d5_299` first exact late promotions

### D. 당장 main focus로 두지 말아야 할 것

1. common portal denom-16 / denom-8 full theoremization
2. RouteY global cycle theorem
3. checked late atlas를 바로 all-`m` theorem으로 승격하려는 시도
4. accepted odd-`m` backbone의 깊은 proof import를
   frontier-adjacent 작업보다 앞세우는 것

## Lean 작업 순서 제안

실제 Lean 순서는 다음이 가장 낫다.

1. `Core` object/interface를 지금 수준에서 조금 더 정제한다.
2. `Canonical/Residual/PromotedCollar.lean`를 만들고 `286` statement를 넣는다.
3. `Canonical/Residual/HmCore.lean`를 statement-first에서 proof-import 단계로 올린다.
4. `Canonical/Residual/PostHinge.lean`를 만들고
   double-top exit / stitching theorem statements를 적는다.
5. `Certificates.lean` 아래에 `289/297/298/299` provenance와 payload를 묶는다.
6. 그 다음에야 common stable packet theorem import를 다시 주력으로 올린다.

## 현재 `d5-plan`과의 차이

기존 `d5-plan`은

- `M2 -> M3 -> M4`

를 거의 직선 순서로 읽게 되어 있다.

현재 frontier를 반영하면 이 부분은 다음처럼 읽는 것이 더 정확하다.

- `M2 (286/300 중심)` -> `M7 일부 (post-hinge interface formalization)` ->
  `M5 일부 (289/297/298/299 certificate packaging)` ->
  그 다음 `M4 common lane`

즉 milestone 번호를 완전히 바꾸자는 뜻은 아니다.
하지만 **proof budget의 실제 배분**은 바꿔야 한다.

## 최종 판단

현재 필요한 우선순위 변경은 다음 정도다.

- 작은 미세조정: 아니다.
- 전체 계획 폐기: 아니다.
- **frontier-adjacent theorem stack으로 주력을 옮기는 중간 규모 재정렬**: 맞다.

지금 Lean이 가장 크게 기여할 수 있는 지점은:

> 이미 닫힌 `286/300` local theorem을 안정적으로 formalize하고,
> 그 위에서 현재 진짜 frontier인 post-hinge / stitching 문제의
> exact theorem boundary를 드러내는 것

이다.

그 다음에야 common stable packet이나 older closed backbone의 deeper import가
“좋은 추가 검증 작업”이 된다.
