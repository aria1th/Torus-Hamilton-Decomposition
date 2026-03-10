# Codex / GPT 5.4 Executor Guide

이 문서는 Codex 또는 GPT 5.4 Executor에게 레포지토리 구조와 작업 규칙을 안내합니다.

## 너의 주된 역할

**증명을 작성하는 것이 아니다. (보통은)** 너의 핵심 역할은:
1. **탐색** — brute-force search, SAT/CP-SAT, exhaustive enumeration
2. **검증** — 주어진 construction이 실제로 Hamilton decomposition인지 확인
3. **데이터 생성** — return map tables, cycle structure, counterexample search
4. **패키징** — 모든 결과를 재현 가능한 `.tar.gz` 아티팩트로 묶기

증명의 방향 설정과 수학적 논증은 Explorer (GPT 5.4 Pro)가 한다. 너는 계산과 검증을 담당한다.

# Memory / CPU / GPU usage

메모리는 96GB까지 사용 가능하다. 
CPU는 12thread까지 사용 가능하다.
GPU는 1개 사용 가능하다. (가능하면, 그냥 CPU로 해보자.)
---

## 레포지토리 구조

```
Torus-Hamilton-Decomposition/
│
├── tex/                          # d=3 원고 히스토리
│   └── d3torus_..._editorial_revision.tex   (v1 원본)
│
├── Round2/                       # d=3 개정 + referee 라운드
│   ├── proof-stages/             # Gemini/GPT 증명 재구성 초안들
│   ├── stage1/ ~ stage4/         # referee report + 수정본 (v2, v3)
│   ├── stage5/                   # v6 + REVISION_NOTES_v6.md
│   └── stage6/                   # v7 (최신) + v6 referee reports + opus 리뷰
│
├── RoundX/                       # d=4 일반화 (전부 여기)
│   ├── codex_job_request{,_2,_3}.md   # Codex 작업 명세서 1~3
│   ├── d4_line_union_general_theorem_proof_v3.{md,tex,pdf}  # 최종 d=4 증명
│   ├── d4_line_union_proof_patch_notes_v3.md  # v3 패치 노트
│   ├── d4_approach_summary_for_d5.md  # d=5 접근법 참조 문서
│   ├── routex_*.md               # AI 리뷰들 (gpt5.4pro, gemini31dt, opus46)
│   └── user_input_and_gpt54pro_response.md  # d≥5 방향 논의
│
├── scripts/                      # 탐색/검증 스크립트 (d=4 중심)
│   ├── torus_nd_validate.py              # 범용 d-torus 검증기
│   ├── torus_nd_line_union_validate.py    # d=4 line-union gauge 전용 검증기
│   ├── torus_nd_line_union_search.py      # line-union 후보 탐색
│   ├── torus_nd_hyperplane_fusion_search.py  # hyperplane fusion 탐색 (실패 기록)
│   ├── torus_nd_second_return_analysis.py # second-return odometer 분석
│   ├── torus_nd_layer2_gauge_analysis.py  # layer-2 gauge classification
│   ├── torus_nd_exact_search.py          # brute-force exact search
│   └── ...                               # 기타 탐색 스크립트
│
├── anc/                          # 논문 부록용 검증 스크립트 (d=3)
│   ├── route_e_even.py           # Route E 메인 검증기
│   ├── verify_m4_witness.py      # m=4 finite witness 검증
│   └── run_even_artifact_suite.py # 전체 even-case 검증 스위트
│
├── artifacts/4d_generalization/  # Codex 계산 결과물 (~40개 JSON/tar.gz)
│
├── reviews/                      # Round 1 AI 리뷰 + 제안
│   ├── review_a.md, review_b.md  # 초기 referee reports
│   ├── suggestion_c.md, suggestion_d.md  # 구조 제안
│   └── clarify-ai-plan.md        # AI 도구 사용 고지
│
├── traces/                       # 탐색 단계 기록
├── candidates/                   # 후보 construction 기록
├── 4d_generalization/            # 초기 4D 메모
│
├── RESEARCH_PROGRESSION.md       # 일주일간 연구 전개 Phase 0→5
├── README.md                     # 레포 README
│
└── tmp/                          # 임시 작업 공간 (정리 후 적절한 곳으로 이동)
    └── suggested_workflow.md     # AI-assisted research workflow SOP
```

---

## 핵심 파일 위치

### 읽어야 할 파일 (context)

| 목적 | 파일 |
|---|---|
| **d=3 최신 원고** | `Round2/stage6/d3torus_..._v7.tex` |
| **d=4 최종 증명** | `RoundX/d4_line_union_general_theorem_proof_v3.md` |
| **d=4 패치 노트** | `RoundX/d4_line_union_proof_patch_notes_v3.md` |
| **d=5 접근법 요약** | `RoundX/d4_approach_summary_for_d5.md` |
| **d=4 Codex job 패턴** | `RoundX/codex_job_request{,_2,_3}.md` |
| **연구 전체 흐름** | `RESEARCH_PROGRESSION.md` |
| **d=3 검증 스크립트** | `anc/route_e_even.py` |
| **d=4 검증 스크립트** | `scripts/torus_nd_line_union_validate.py` |
| **odd/even d 논의** | `RoundX/user_input_and_gpt54pro_response.md` |

### 작성할 곳

| 상황 | 위치 | 이름 규칙 |
|---|---|---|
| 새 탐색/검증 스크립트 | `scripts/` | `torus_nd_<주제>.py` |
| 탐색 결과 (JSON 등) | `artifacts/<task_id>/` | 하위 디렉터리 생성 |
| 요약 보고서 | `artifacts/<task_id>/summary.md` | 항상 포함 |
| d=5 관련 모든 것 | `tmp/` → 나중에 `RoundY/`로 이동 | `d5_<주제>.{md,py}` |

### 아티팩트 패키징 규칙

작업이 끝나면, 결과물 전체를 **하나의 `.tar.gz`로 묶는다.**

```bash
# 예: d5-baseline-search 작업의 패키징
tar -czf artifacts/d5_baseline_search.tar.gz \
  scripts/torus_nd_d5_baseline.py \
  artifacts/d5_baseline_search/
```

`.tar.gz` 안에 반드시 포함할 것:

```
<task_id>.tar.gz
├── scripts/          # 실행한 코드 전부
├── data/             # 생성된 JSON, CSV, cycle lists
├── logs/             # stdout/stderr 로그
├── summary.md        # 아래 형식의 요약 보고서
└── README.md         # 재현 방법 (1줄 명령어)
```

### summary.md 형식

```markdown
# Task: <task_id>

## 질문
<이 작업이 답하려는 연구 질문>

## 결과
- 탐색 범위: m = ?, d = ?
- 소요 시간: ?
- 발견: <있으면 구체적으로, 없으면 "해당 범위에서 없음">

## 발견된 패턴 / 반례
<구체적 데이터>

## 실패한 경우
- 어디까지 탐색했는지
- 어떤 패턴이 배제되었는지
- 다음에 줄일 수 있는 탐색 범위

## 재현
python scripts/<script>.py
```

---

## 작업 규칙

### 반드시 지켜야 할 것

1. **증명을 (어지간하면) 쓰지 않는다** — 계산으로 확인하고 데이터를 남긴다
2. **모든 주장에 상태 태그**: `[C]` computationally supported, `[F]` failed, `[O]` open
3. **실패해도 빈손으로 끝나지 않기** — negative result도 기록한다
4. **결과물은 반드시 `.tar.gz`로 묶기** — 위의 패키징 규칙 참조
5. **재현 가능성** — `python scripts/<script>.py` 한 줄로 재실행 가능
6. **랜덤 시드, 탐색 범위, 파라미터**를 코드 상단에 명시

(인사이트를 얻었다면, 적는 것 정도는 readme에 해서 넘기면 나쁘지는 않음.)
---

## 현재 열린 연구 질문

### d=5 관련 (다음 target)

1. **Canonical baseline에서 어떤 색이 먼저 깨지는가?**
   - d=3에서는 color 2, d=4에서는 모두 동일
   - d=5에서 확인 필요: `torus_nd_validate.py`로 m=3,5,7 odd 케이스 먼저

2. **Sign-product invariant가 d=5에서도 parity barrier를 만드는가?**
   - d=3 (odd d): even m에서 barrier 있음
   - d=4 (even d): barrier 없음
   - d=5 (odd d): barrier 재등장 예상 — 확인 필요

3. **Single-color hyperplane carry가 d=5에서 작동하는가?**
   - d=4에서는 작동했지만 4색 호환 불가 → line-union gauge 필요
   - d=5에서는? 5색 호환 탐색 필요

4. **Nested return map 구조**
   - d=3: V → P₀ (1단계)
   - d=4: V → P₀ → Q (2단계)
   - d=5: V → P₀ → Q → Q' (3단계 예상?)

### d=3 원고 관련

5. **v7 LaTeX 컴파일 + 최종 PDF 생성**
   - 파일: `Round2/stage6/d3torus_..._v7.tex`
   - 필요: pdflatex 2회 이상

---

## Codex job 패턴 (d=4에서 검증된 순서)

```
Job 1: baseline 실패 분석
  입력: canonical construction
  출력: 어떤 색이 깨지는지, cylinder 구조, 불변량
  패키징: d4_baseline_analysis.tar.gz

Job 2: single-color fix 시도
  입력: Job 1의 실패 양상
  출력: 한 색만 고쳤을 때의 cycle structure table
  패키징: d4_single_color_fix.tar.gz

Job 3: compatibility 탐색 (SAT/CP-SAT)
  입력: Job 2의 incompatibility 패턴
  출력: small m에서 multi-color 호환 후보 family
  패키징: d4_compatibility_search.tar.gz

Job 4: gate classification
  입력: Job 3의 후보
  출력: reduced family enumeration, explicit witness
  패키징: d4_gate_classification.tar.gz

Job 5: return map 분석
  입력: Job 4의 witness
  출력: return map table, cycle lengths, odometer conjugacy data
  패키징: d4_return_map_analysis.tar.gz
```

각 Job의 `.tar.gz`에는 코드, 데이터, 로그, summary.md가 반드시 포함된다.

---

## 규칙 요약

1. **너의 역할은 계산과 검증이다.** 증명은 쓰지 않는다.
2. **읽기**: 관련 파일을 먼저 읽고 context를 파악한 후 작업
3. **쓰기**: `scripts/`에 코드, `artifacts/<task_id>/`에 데이터
4. **태그**: 모든 결과에 `[C]/[F]/[O]`
5. **패키징**: 모든 작업은 `.tar.gz`로 묶어서 `artifacts/`에 저장
6. **실패**: 실패도 자산 — negative result를 summary.md에 기록
7. **재현**: `python scripts/<script>.py` 한 줄로 재실행 가능
