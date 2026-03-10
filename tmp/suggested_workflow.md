# AI-Assisted Research Workflow for Mathematical Proofs

*Battle-tested on: Hamilton Decompositions of Directed d-Tori, March 2–9, 2026*
*Results: d=3 theorem (v1→v7 in one week), d=4 theorem (5 hours), d=5 roadmap begun*

---

## 0. 핵심 철학

1회차 산출물은 "정답"이 아니라 **연구 자산**이다.

매 단계에서 남겨야 하는 것:
1. 어디까지 전진했는가
2. 어디서 왜 막혔는가
3. 무엇을 코드/탐색/계산으로 넘겨야 하는가
4. 다음 분기 중 사람이 무엇을 선택해야 하는가

**실패는 손실이 아니다.** d=4 증명에서, hyperplane-fusion 시도가 실패한 것이 line-union gauge 발견의 직접적 원인이었다.

---

## 1. 역할 기반 설계

모델명이 아니라 **역할**을 고정하면 모델이 바뀌어도 절차가 유지된다.

| 역할 | 하는 일 | 현재 배정 (2026-03) |
|---|---|---|
| **Explorer** | 문제를 밀고 나가며 연구 노트 생산 | GPT 5.4 Pro |
| **Executor** | 코드 실행, 대규모 탐색, 반례 탐색 | Codex 5.3 (GPT 5.4) |
| **Critic** | 논리적 빈틈, 대안 경로, 구조적 조언 | GPT 5.4 Pro / Gemini 3.1 DT |
| **Synthesizer** | 여러 결과를 묶고 분기 정리 | GPT 5.4 Thinking |
| **Referee** | 독립 심사 보고서 (×3, 서로 blind) | GPT 5.4 Pro |
| **Referee Validator** | 심사 보고서의 meta-review | GPT 5.2 Pro (×2) |
| **Editor** | 가독성, 문체, 어순, 구조 정리 | Opus 4.6 |
| **Advisor** | 수학적 아름다움, 자연스러움, 장기 가치 | Gemini 3.1 DT / GPT 5.4 Pro |

### 실전에서 배운 것

- **Explorer와 Critic은 같은 모델이어도 별개 세션으로** — 자기 산출물을 비판하게 하면 방어적이 된다
- **Critic들의 강점이 다르다** — GPT 5.4 Pro는 구조적 결함 (Prop 5–6 lifting gap), Gemini 3.1 DT는 표면적 완결성 (정의역 누락, 변수명 충돌)
- **Editor는 수학 생성을 기대하지 않는다** — defense 정리, referee report 비교, 문장 흐름에 집중
- **Advisor 보고서는 referee와 분리한다** — referee는 "맞는가", advisor는 "좋은 수학인가"

---

## 2. 연구 생성 루프 (Research Loop)

```
┌─────────────────────────────────────────────────────┐
│  0. 문제 브리프 작성                                    │
│  1. Explorer로 1차 탐색 → 연구 노트                     │
│  2. Executor로 코드 검증 / 대규모 탐색                   │
│  3. Critic들로 독립 비평                                │
│  4. Synthesizer로 종합 → 사람이 분기 선택               │
│  5. 선택된 방향으로 다시 1단계 → 반복                    │
│                                                       │
│  탈출 조건: 정리 진술 안정 + 증명 골격 확보 + 반례 없음   │
└─────────────────────────────────────────────────────┘
```

### 0단계. 문제 브리프

포함 항목:
- 문제 진술 + 성공 기준
- 현재 알고 있는 가정과 제한
- 금지할 비약 (예: "computational evidence만으로 proved라 쓰지 않는다")
- 코드/탐색 개입 가능성

> **실전 예**: d=4 브리프는 "D₄(m)의 Hamilton decomposition for all m≥3. 단일-색 hyperplane carry는 이미 작동함을 확인. 핵심 병목: 4-색 호환"이었다.

### 1단계. Explorer 탐색

출력은 답변이 아니라 **연구 노트**. 모든 주장에 상태 태그:

| 태그 | 의미 | 예시 |
|---|---|---|
| **[P]** | proved | "R_c의 first-return formula [P]" |
| **[C]** | computationally supported | "m=3…10에서 단일 순환 확인 [C]" |
| **[H]** | heuristic | "even d는 uniform proof 가능할 듯 [H]" |
| **[F]** | failed attempt | "hyperplane fusion — 4색 호환 불가 [F]" |
| **[O]** | open / unresolved | "Prop 5 counting argument 빈틈 [O]" |

> **실전 교훈**: d=4에서 [F] 태그가 붙은 "hyperplane fusion 실패"가 가장 가치 있는 산출물이었다 — 실패 양상이 line-union gauge의 설계 조건을 직접 알려줬다.

### 2단계. Executor 위임

코드 실행이 필요하면 **명세서**로 떼어낸다.

```
Task ID:   d4-gauge-search-01
Question:  m=5에서 4-색 호환 direction assignment 존재하는가?
Purpose:   line-union gauge 후보 탐색
Search space: P₀ 위 direction tuple 전수조사 (|P₀|=125)
Success:   단일 m⁴-cycle 산출 + 4색 모두 Hamilton
Failure:   전수조사 완료 후 후보 없음 → 어떤 패턴이 배제되었는지 기록
Artifacts: code, candidate_list.json, failure_report.md
```

**핵심 규칙**: 실패해도 "빈손"으로 끝나면 안 된다.
- 어디까지 탐색했는지
- 어떤 패턴이 없었는지
- 탐색 범위를 어떻게 줄일지

> **실전 예**: Codex job 1(hyperplane fusion)의 실패 보고서가 job 2(second-return odometer)의 설계를 직접 결정했다. Job 3(layer-2 gauge classification)의 결과가 최종 증명의 witness가 되었다.

### 3단계. 독립 비평

Critic마다 초점을 다르게 준다:

| Critic | 물어볼 것 |
|---|---|
| GPT 5.4 Pro | "논리 체인이 닫히는가? Prop X의 counting이 실제로 충분한가?" |
| Gemini 3.1 DT | "정의역이 실제로 exhaustive인가? 변수명 충돌은 없는가?" |

**범위 제한이 중요**: "전체를 풀어라"가 아니라 "이 막힘이 본질적인가?"

> **실전 교훈**: d=4 v2 증명을 두 모델에 보냈을 때, GPT 5.4 Pro는 Prop 5–6의 lifting gap(구조적)을 잡았고, Gemini 3.1 DT는 S=2 q≠0 정의 누락(표면적)을 잡았다. 둘 다 합쳐야 완전한 리뷰.

### 4단계. 종합 + 사람 선택

Synthesizer 출력:
- 제안된 방향 + 근거 + 위험
- 바로 시도 / 보류 / 폐기
- **사람이 선택해야 할 분기**

**선택은 반드시 사람이 한다.** 모델은 정돈하지만 방향은 잡지 않는다.

> **실전 예**: d=4에서 "hyperplane fusion vs line-union gauge vs SAT brute force" 삼지선다가 나왔을 때, 사람이 line-union을 선택한 것이 5시간 완성의 열쇠였다.

### 5단계. 반복

선택된 방향으로 1→2→3→4를 반복. 매 라운드에서:
- 새로 얻은 것
- 여전히 비는 것
- 새 코드 과제

탈출 조건:
- 정리 진술이 안정됨
- 증명 골격이 보임
- 치명적 반례가 없음
- 계산 뒷받침이 재현 가능함

---

## 3. 논문 개선 루프 (Paper Loop)

연구 루프가 닫힌 후, **별도 루프**로 진입한다. 두 루프를 섞지 않는다.

```
┌─────────────────────────────────────────────────────┐
│  A. 초안 → Explorer가 작성                            │
│  B. Referee ×3 (blind) → 독립 심사                    │
│  C. Referee Validator ×2 → meta-review               │
│  D. Editor → 취합 + 가독성 + defense 정리              │
│  E. 사람 개정 → 다시 B                                │
│                                                       │
│  탈출 조건: Referee 수렴 (공통 요청 ≤ 표기/미학)        │
└─────────────────────────────────────────────────────┘
```

### A. 초안 게이트

논문으로 넘어가기 전 최소 요건:
- 메인 정리의 정확한 진술
- 필요 정의 + 기호표
- 핵심 보조정리 목록
- proof skeleton
- 계산 결과의 재현 가능 기록
- 취약점 목록

**연구 노트 ≠ 논문**. 노트는 탐색의 역사, 논문은 독자를 위한 압축.

### B. Referee 단계

세 Referee는 **서로의 보고서를 보지 않고** 작성한다.

```
1. Summary of the main claim
2. Perceived significance
3. Correctness concerns — 구체적 정리/줄번호
4. Gaps / hidden assumptions
5. Exposition quality
6. Suggested revisions
7. Fatal issues (있을 경우)
8. Minor issues
9. Recommendation + score
```

"aggressively critical"이어도 **근거 기반**: "어느 정리의 어느 연결이 왜 약한가."

> **실전 점수 추이**: Stage 1 (near-accept) → Stage 2 (6/10) → Stage 3 (7.5/10) → Stage 4 (8/10) → Stage 5–6 (accept after minor). Stage 2에서 낮아진 건 증명을 근본적으로 재구성했기 때문 — **예상된 하락**.

### C. Referee Validator

논문이 아니라 **referee report를 심사**한다:
- 과장된 비판이 있는가?
- 문제 제기가 실제로 치명적인가?
- 엉뚱한 비판이 섞였는가?

### D. Editor 취합

- Referee report들의 공통점 / 차이점 표로 정리
- 수정 우선순위 제안
- 수정에 필요한 노력 추정
- 가독성 + 문체 개선
- **수학 생성은 하지 않음**

> **실전 예**: v6 후 두 referee의 공통 요청 4개 + 개별 요청 각 5개를 식별, 우선순위표 작성 → v7에서 공통 4개 + 핵심 개별 3개 반영 → 추가 수정 불필요 판정.

### E. 반복 개정

**Revision log를 반드시 유지한다.**

```
Issue ID:   S4-A-3
Raised by:  Referee A, Stage 4
Location:   Introduction, ¶3
Type:       literature positioning
Action:     Added Keating citation, rewrote Bogdanowicz/DarijaniMiraftabMorris positioning
Status:     fixed in v7
```

이 로그가 있으면:
- 같은 비판을 반복해서 듣지 않음
- 폐기한 방향을 다시 살리지 않음
- 무엇이 해결되었는지 놓치지 않음

탈출 조건: **Referee들이 수렴** — 남은 요청이 전부 표기, 미학, nice-to-have 수준.

---

## 4. 논문 구조 (수학/이론)

| 섹션 | 내용 |
|---|---|
| Title / Abstract | 결과, 범위, 방법, 의미 압축 |
| Introduction | 배경, 기존 맥락, 메인 결과, proof idea, 구조 안내 |
| Preliminaries | 정의, 표기표, 기존 사실 |
| Main Results | 정리 + corollary를 읽기 좋은 순서로 |
| Proof Roadmap | 전체 증명 전략을 먼저 보여줌 (**proof-dependency chain**) |
| Core Proof | 핵심 보조정리와 본증명 |
| Examples | worked example로 기계가 돌아가는 것을 보여줌 |
| Discussion | 범위, 한계, open problems — **톤 주의** |
| Appendix | 긴 계산, 코드, 재현성 (**증명의 일부 vs 독립 감사 구분** 명시) |

> **실전 교훈**: proof-dependency chain (v7 line 727)은 Stage 3 이후 모든 referee가 요청한 가장 반복적인 항목이었다. 처음부터 넣었으면 2라운드를 아꼈을 것.

---

## 5. Advisor 보고서

Referee와 **별도**. 정확성보다 미학을 묻는다:

```
1. 이 결과가 왜 아름다운가?
2. 진술이 자연스러운가, 인공적인가?
3. 더 본질적인 형태로 압축할 수 있는가?
4. proof idea가 theorem statement와 조화를 이루는가?
5. 더 강한 정리나 더 우아한 formulation이 가능한가?
6. 무엇이 이 논문을 기억에 남게 하는가?
```

> **실전 예**: GPT 5.4 Pro가 advisor로서 "d=3 odd case는 이미 숨겨진 odometer"임을 발견 — d=4와의 통일성을 드러내는 재작성으로 이어짐. 이건 referee 모드에서는 나올 수 없는 종류의 관찰.

---

## 6. 이 논문에서 배운 메타 교훈

### 실패를 자산으로

| 실패 | 무엇을 알려줬나 |
|---|---|
| Hyperplane fusion → 4색 비호환 | Gate의 설계 조건 (line-union) |
| Sign-product barrier | Odd/even 분기의 필연성 |
| Stage 2 점수 하락 (6/10) | 증명 재구성 후 exposition 미완 — 예상된 하락 |

### 교차 검증의 가치

같은 증명을 **다른 모델에 독립적으로** 보내면, 각자 다른 종류의 문제를 잡는다.
- 구조적 결함 (GPT 5.4 Pro) + 표면적 완결성 (Gemini 3.1 DT) = 완전한 리뷰
- 한쪽만으로는 충분하지 않다

### Referee 수렴 패턴

4회 이상 반복하면 남은 요청이 수렴한다:
- 1차: 큰 구조 문제 (exposition 방향, 증명 재구성)
- 2차: 중간 단위 문제 (로드맵, 사례 보강)
- 3차+: 표기, 문헌, 미학

### 사람의 역할

AI는 **방향을 제시하고 정돈**하지만, **어느 방향을 밀 것인지는 사람이 잡는다.**
이 논문에서 사람이 한 결정적 선택들:
- Suggestion D(splice-graph) 방향 채택
- line-union gauge 방향 선택
- d=3 odd case를 odometer로 재작성 결정
- 모든 최종 수학적 판단

---

## 7. 한 줄 요약

**탐색 노트 → 코드 위임 → 독립 비평 → 사람 선택 → 반복 → | 게이트 | → 초안 → blind referee ×3 → meta-review → editor 취합 → 개정 반복 → advisor 평가**

두 루프를 섞지 않는다. 연구 루프가 닫힌 후에만 논문 루프에 진입한다.
