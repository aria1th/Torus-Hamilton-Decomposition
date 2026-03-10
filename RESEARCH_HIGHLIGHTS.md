# Research Highlights — Torus Hamilton Decomposition

*2026-03-02 ~ 2026-03-09, one week*

---

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
