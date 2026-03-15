# Research Highlights — Torus Hamilton Decomposition

*2026-03-02 ~ 2026-03-15*

---

## 현재 프로그램 상태: d=3, d=4는 닫혔고, d=5는 odd/even으로 분기됨

이번 라운드에서 전체 low-dimensional program은 세 층으로 정리되었다.

- `d=3`: 수학적으로 완결. 현재 원고는 odd/even 모두 포함한 완성 manuscript 상태
- `d=4`: return-map / odometer 언어로 완전 증명 완료, Lean formalization까지 진행 완료
- `d=5`, odd `m`: accepted theorem package 안에서 닫힘.
  현재 cleaned manuscript-order theorem suite까지 정리되었고, 남은 것은
  selective reproof / inlining 정리
- `d=5`, even `m`: 아직 open.
  하지만 broad witness search가 아니라 **finite-splice / critical-row repair**
  branch로 재정의됨

즉, 프로젝트의 전체 건강도는 꽤 좋아졌다.
이제 사실상 열린 건 `d=5` even branch와 이후 일반화 문제다.

## Leanification checkpoint: d=4 완료, d=3 even package 완료, odometer rewrite는 color-0 Case II frontier

이번 라운드의 formal progress도 의미가 크다.

- `d=4`: Lean formalization complete
- `d=3 even`: Route E package complete
- `d=3 odometer rewrite`: `Color2Full`, `Color1FullCaseI`,
  `Color1FullCaseII`, `Color0FullCaseI` complete
- 현재 Lean frontier는 `Color0FullCaseII`의 남은 upper special lanes와
  `hreturn` / `hfirst`
- `d=5 Lean`: full proof branch가 아니라 extracted-model / spec support branch

즉 formal program도 exploratory 상태를 지나,
명확한 checkpoint를 하나 확보한 셈이다.

## 가장 놀라운 결과: m=5 witness → 전체 odd m color 3 theorem

m=5 하나에서 찾은 26-move Kempe sequence가 **아무런 수정 없이** odd m ≥ 5 전체에서 color 3을 Hamilton으로 만든다.

- finite witness → infinite family가 의식적 일반화 없이 일어남
- 26-move의 Kempe support가 pinned constants `0,1,2,3,4`를 사용하는데, 이것들이 **m에 의존하지 않는 affine 조건**이었음
- 증명 구조: f₃ (m⁵) ← R₃ (m⁴) ← B (m³) ← U (m²) ← row dynamics
- "좋은 witness는 좋은 이유가 있다"의 실례

## 가장 어려웠던 부분: d=3 even case Route E 설계

sign-product barrier가 Kempe 경로 자체를 차단 → 비-Kempe low-layer construction을 처음부터 설계.

- defect family (X₁₀₂, X₀₂₁, X₂₁₀) + Case II repair + m mod 6 분기 + finite splice
- v1 → v7, referee 6라운드
- **설계보다 정확성 확인의 case analysis 깊이**가 진짜 병목

## 가장 과소평가되었지만 결정적인: Boolean model UNSAT (d=5)

"Boolean zero-pattern으로 충분하다"는 자연스러운 가정이 **m=5에서 이미 모순**.

- rotational covariance + odometer target → layer 1 출력이 π(c)-c ∈ {0,2}로 강제
- S₅에서 이를 만족하는 건 identity뿐 → carry 불가능
- **한 줄짜리 obstruction이 전체 접근법을 폐기시킴** → affine-pinned model로 전환

## 현재 가장 중요한 성과: d=5 odd-m closure와 cleaned theorem suite

`d=5`의 최근 진전은 “탐색이 더 필요하다”가 아니라
**정확한 theorem chain이 닫히고, 그것이 manuscript-order theorem suite로
재패키징되었다**는 데 있다.

- `017–019`: mixed witness의 return-map이 실제 reduced dynamical object라는 점을 추출
- `044`: active branch가
  `B <- B+c <- B+c+d`
  로 factor된다는 finite-cover normal form 획득
- `046–048`: carry sheet가 one-sided anticipation datum이고, 숨은 datum이
  `tau`라는 countdown carrier라는 점을 추출
- `049–055`: proof-support compute가 reset law와 branch formulas를 더 큰 odd `m`
  까지 밀어 줌
- `055`: uniform odd-`m` proof target을
  `wrap`, `CJ`, `OTH`
  세 boundary branch lemma로 압축
- `058–062`: 그 branch lemma들마저
  `Theta = q+s+v+layer`
  위의 tiny phase machine과
  `B`-region bootstrap theorem으로 다시 압축
- `068`: 이 structural theorem package가 사실상 near-stable shape임을 정리
- `071`: fixed regular slice마다 exact object가 이미 marked length-`m` chain임을 분리
- `076`: safest theorem object는 abstract bridge `(beta,rho)`이고,
  concrete odometer `(beta,q,sigma)` / `(beta,delta)`는 strongest checked model임을 정리
- `077–083`: globalization bottleneck을 tail-length / exceptional interface /
  final gluing theorem으로 차례로 압축하고 odd `m` closure 도달
- `087`: odd-`m` D5는 accepted package 안에서 닫혔음을 dependency audit으로 확인
- `092`: structural first-exit theorem, chart-to-raw composition,
  final globalization proof를 하나의 cleaned independent-style suite로 정리
- `093`: 아직 accepted-support form으로 남아 있는 정리들의 재증명 우선순위를
  `076`, `079`, `062` patch-avoidance clause로 압축

따라서 지금의 odd-`m` D5 질문은 더 이상

> globalization이 되느냐?

가 아니라

> 어떤 정리를 다시 inlining/reproof 하면 fully independent package로
> 부를 수 있는가?

이다.

이것은 초기 d=5 단계들의 “blind local search”와는 질적으로 전혀 다른 상태다.

## 새 open branch: d=5 even-m은 finite-splice / critical-row repair 문제

odd-`m` closure 이후 even-`m`은 별도 수학 문제로 정리되었다.

- parity barrier가 `Kempe-from-canonical` 경로를 차단
- odd final gluing proof는 형식적으로 parity-blind라서,
  같은 upstream package만 재건되면 carry-over 가능
- 따라서 새 목표는 fresh bridge theorem이 아니라
  **critical-row finite-splice theorem**

즉 even `m`의 좋은 질문은:

> bulk odometer를 보존하면서 regular source-window splice `u -> u-3`를
> 증명하고, source `3`을 유일한 exceptional splice defect로 고립시킬 수 있는가?

이다.

이건 `d=3` even Route E의 D5 analogue로 보는 것이 맞다.

## 다음 우선순위: d=7,9,... 에서 theorem-guided screening method 검증

현재 우선순위는 even branch를 곧바로 brute-force로 여는 것이 아니라,

- `d=5` odd solution을 screening template로 정리하고
- `d = 7, 9, ...`의 관리 가능한 작은 범위에서
  theorem-guided search/screen method가 실제로 작동하는지
  pilot validation 하는 것

이다.

즉 지금 필요한 것은 새로운 광범위 탐색이 아니라
**탐색법 자체의 이식성 검증**이다.

## AI 역할 분화

| 역할 | 담당 |
|---|---|
| 방향 설정, 분기 판단 | 사람 |
| 증명 설계, obstruction 발견 | GPT 5.4 Pro |
| 대규모 search, 검증 스크립트 | Codex |
| 논문 편집, referee 대응, cross-validation | Opus 4.6 |

## 결과 타임라인

| 날짜 | 결과 |
|---|---|
| 3/2 | d=3 odd case 완성 |
| 3/4 | d=3 even case Route E 초안 |
| 3/7 | d=3 v1 원고 완성 |
| 3/8 | d=3 v3~v6 referee 대응 |
| 3/9 AM | d=3 v7 (최종), d=4 증명 완성 |
| 3/9 PM | d=5 m=5 witness 발견, color 3 partial theorem 증명 |
| 3/10–3/12 | d=5 return-map extraction → finite-cover / countdown-carrier normal form |
| 3/13 | d=5 positive theorem chain 정리, phase-machine / bootstrap proof branch로 압축 |
| 3/14 | d=5 bridge theorem cleanup: abstract bridge `(beta,rho)` vs componentwise concrete `(beta,delta)`, globalization question 분리 |
| 3/14 late | exceptional-row gluing theorem까지 닫히며 odd-`m` accepted package closure |
| 3/15 | `092` cleaned theorem suite, `093` reproof-target audit, even-`m` critical-row branch 정리 |
