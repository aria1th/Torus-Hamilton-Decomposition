# Codex Job Report: RouteX 0

이 문서는 `message_for_codex_gpt5.4.md`의 실행 규칙에 맞춰, d=5 탐색을 위한 **executor-ready job spec** 으로 다시 정리한 것이다.

핵심은 이것이다:

- **전체 d=5 정리를 증명하라는 것이 아니다.**
- 현재 Codex의 일은 **odd `(m)` pilot case** 를 계산적으로 밀어 보고,
  low-layer witness가 실제로 3-carry normal form을 만들 수 있는지 찾는 것이다.
- 성공하든 실패하든, 반드시 `scripts/`, `artifacts/`, `.tar.gz` 패키지까지 남겨야 한다.

---

## 0. 먼저 읽을 것

### 필수 context

1. `message_for_codex_gpt5.4.md`
2. `RoundX/d4_line_union_general_theorem_proof_v3.md`
3. `RoundX/d4_approach_summary_for_d5.md`
4. `RoundX/codex_job_request.md`
5. `RoundX/codex_job_request_2.md`
6. `RoundX/codex_job_request_3.md`
7. `RESEARCH_PROGRESSION.md`

### 참고할 existing scripts

- `scripts/torus_nd_validate.py`
- `scripts/torus_nd_line_union_validate.py`
- `scripts/torus_nd_line_union_search.py`
- `scripts/torus_nd_second_return_analysis.py`
- `scripts/torus_nd_hyperplane_fusion_search.py`

---

## 1. Problem

증명하고 싶은 최종 정리는:

\[
D_5(m)=\operatorname{Cay}\bigl((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\}\bigr)
\]
가 모든 `(m\ge 3)` 에 대해 5개의 arc-disjoint directed Hamilton cycles로 분해되는가?

즉 각 vertex `x` 에 permutation `\delta(x)\in S_5` 를 주어

\[
f_c(x)=x+e_{\delta_c(x)}\qquad(c=0,1,2,3,4)
\]

가 모두 길이 `m^5` 의 single cycle이 되게 해야 한다.

현재 이 전체 정리 자체는 **[O]** 이다.

---

## 2. Current target

Codex가 지금 당장 닫아야 하는 것은 **전체 d=5가 아니라 odd `(m)` pilot case** 이다.

### Primary task

**[H → C/P]**  
single `5`-cycle bulk를 고정한 뒤, low-layer witness를 찾아서

`V -> P_0 -> Q -> 3D odometer`

구조를 실제 계산으로 확인하는 것.

즉 각 color `c`에 대해 first return

\[
R_c=f_c^m|_{P_0}
\]

가 affine coordinates `(u,v,w,q)` 에서

- bulk shift,
- `q=0`에서 lowest carry,
- `q=m-1`에서 middle carry,
- `q=m-1` and `v=w=0` 에서 top carry

를 갖는 **3-carry normal form** 또는 affine-conjugate로 떨어지는 candidate를 찾는 것이 핵심이다.

### Secondary task

even `(m)` 은 아직 construction이 없고, 현재 단계에서는 **obstruction을 더 분명히 하는 것** 까지만 기대한다.

---

## 3. What is already known

아래 태그는 반드시 유지:

- `[P]` rigorously established
- `[C]` computationally supported only
- `[H]` heuristic / strong design principle
- `[F]` ruled out in current family
- `[O]` open

### 3.1 Structural facts

- **[P] even `(m)` sign-product barrier**  
  odd `d`에서는 canonical coloring에서 시작하는 Kempe-only route가 짝수 `m`에서 막힌다.  
  따라서 d=5 even case는 canonical/Kempe path로 끝나지 않을 가능성이 높다.

- **[P] bulk cycle-block invariant lemma**  
  layer-0 bulk permutation `p` 의 cycle decomposition이 여러 block으로 나뉘면,
  pure bulk first-return displacement는 block-sum invariants를 남긴다.  
  따라서 d=5 odd pilot의 bulk는 사실상 **single 5-cycle** 이어야 한다.

- **[P] 3D odometer lemma**  
  \[
  O_3(u,v,w)=\bigl(u+\mathbf 1_{v=w=0},\ v+\mathbf 1_{w=0},\ w+1\bigr)
  \]
  는 `(\mathbb Z_m)^3` 위 단일 `m^3`-cycle이다.

- **[P] normal-form lifting lemma**  
  어떤 color `c`에 대해 `R_c`가 3-carry normal form으로 정리되면,
  second return `T_c` 는 `O_3` 와 affine-conjugate가 되고,
  따라서 `Q` 위 단일 cycle -> `P_0` 위 단일 cycle -> 전체 `V` 위 단일 cycle 로 lift된다.

### 3.2 Best current design principle

- **[H] odd `(m)`의 가장 유력한 bulk는 single 5-cycle**
  \[
  \sigma(c)=c+1\pmod 5
  \]
  이다.

- **[P] charge**
  \[
  q(x)=x_1+2x_2+3x_3+4x_4 \pmod m
  \]
  를 쓰면 bulk displacement가 color별로 clean하게 정리된다.

- **[H] rotational symmetry**
  simultaneous index shift `(i \mapsto i+1)` 에 대해 covariant한 ansatz를 강제하면
  탐색 공간이 크게 줄어든다.

### 3.3 What already failed

- **[F] `(2+2+1)` bulk families**  
  fixed color가 남거나 cycle block이 여러 개 남는 구조는 bulk invariant를 깨지 못해 Hamiltonicity가 막힌다.

- **[C] 좁은 sanity family random search 실패**  
  layer `0,1,2`에 너무 제한된 transposition-gate만 허용한 family에서는
  `m=3,5` 에서 full witness를 찾지 못했다.  
  이건 impossibility proof가 아니라, **현재 family가 너무 좁다** 는 뜻이다.

---

## 4. Actionable Codex task

## Task ID

`D5-ODD-CYCLIC-BULK-001`

## Research question

odd `(m)` 에 대해, single `5`-cycle bulk와 rotational symmetry를 고정한 restricted low-layer family 안에서

1. 실제 Hamiltonian candidate witness가 존재하는가?
2. 그 witness의 `R_c` 가 3-carry normal form 또는 affine-conjugate로 정리되는가?
3. `T_c=R_c^m|_Q` 가 3D odometer와 affine-conjugate라는 데이터를 추출할 수 있는가?

## Purpose

d=5 odd pilot case의 계산 파이프라인을 닫는 것:

`low-layer witness -> R_c -> T_c -> O_3 -> lift`

---

## 5. Search space

### Fixed ingredients

- dimension `d=5`
- start with odd `m in {3,5,7}`
- vertex set `(\mathbb Z_m)^5`
- layer function
  \[
  S=x_0+x_1+x_2+x_3+x_4
  \]
- charge
  \[
  q=x_1+2x_2+3x_3+4x_4 \pmod m
  \]
- default layer-0 bulk permutation
  \[
  \sigma(c)=c+1\pmod 5
  \]
- layers `S>=4` should be canonical unless there is a very strong reason otherwise

### Preferred symmetry restriction

- simultaneous coordinate/color rotation invariance
- same local rule family for all colors, transported by rotation

### Allowed low-layer ingredients

- `\sigma` and `\sigma^{-1}`
- transpositions / adjacent swaps
- short-cycle local modifications
- affine zero-tests / hyperplane tests
- delayed gates on `S=1,2,3`

### First script target

If only one new search script is made first, prefer:

- `scripts/torus_nd_d5_odd_cyclic_bulk_search.py`

If validation logic is large, split:

- `scripts/torus_nd_d5_odd_cyclic_bulk_search.py`
- `scripts/torus_nd_d5_odd_cyclic_bulk_validate.py`

---

## 6. Required methods

Allowed and encouraged:

- exhaustive enumeration under symmetry reduction
- SAT / CP-SAT / MILP
- brute-force cycle checks for small `m`
- symbolic first-return extraction
- affine-conjugacy detection to the 3D odometer
- heuristic search with **fixed random seeds** and full logs

Not enough by itself:

- “candidate seems good on a few random starts”
- proof prose without stored computation

---

## 7. Success criteria

The job counts as a success if **one** of the following happens:

1. **[C] positive pilot result**  
   A candidate family works for `m=3,5,7`, with explicit `R_c` and `T_c` data showing affine conjugacy to `O_3`.

2. **[C/F] strong negative result on a clean restricted family**  
   A natural restricted family is exhaustively ruled out, with logs and cycle data.

3. **[C] proof-supporting reduction**  
   Even without a full witness, the script extracts a stable reduced normal form showing exactly which carries are missing.

The following is **not** enough:

- “searched some random samples, none found” with no artifact structure

---

## 8. Failure criteria

The job is a failure if it ends with only one of these:

- vague intuition with no saved data
- no exact description of searched family
- no fixed seeds / no reproducibility
- no `.tar.gz` package
- no negative-result summary when search fails

---

## 9. Where to write

### Code

- place new scripts in `scripts/`

### Artifact directory

For this task, prefer:

- `artifacts/d5_odd_cyclic_bulk_001/`

Inside it, always include:

- `summary.md`
- raw JSON / CSV data
- logs
- README with one-line reproduction command

### Final package

- `artifacts/d5_odd_cyclic_bulk_001.tar.gz`

---

## 10. Required artifact contents

The `.tar.gz` must contain:

- executed script(s)
- machine-readable candidate tables / witnesses
- cycle statistics
- return-map data
- logs
- `summary.md`
- `README.md`

If search fails, still include:

- best candidates found
- exact explored family
- ruled-out subfamilies
- seeds and solver versions

---

## 11. Required `summary.md` contents

At minimum:

```markdown
# Task: D5-ODD-CYCLIC-BULK-001

## 질문
odd d=5 cyclic-bulk family에서 3-carry normal form witness가 존재하는가?

## 결과
- 탐색 범위: m = ...
- 소요 시간: ...
- 상태: [C] / [F] / [O]

## 발견
- witness 있으면 explicit rule
- 없으면 ruled-out family

## return-map 데이터
- R_c 요약
- T_c 요약
- odometer conjugacy 여부

## negative results
- 실패한 family / best score / max cycle lengths

## 재현
python scripts/torus_nd_d5_odd_cyclic_bulk_search.py
```

---

## 12. Suggested execution order

1. **small exact pilot**
   - `m=3`
   - very restricted rotational family
   - exact full cycle validation

2. **same family on `m=5,7`**
   - keep same symmetry assumptions
   - compare whether the same structural pattern survives

3. **extract `R_c`**
   - once a promising candidate appears, stop broad random search
   - switch to return-map extraction

4. **check affine conjugacy to `O_3`**
   - if this fails, save the near-miss

5. **package negative or positive result**
   - no empty-handed finish

---

## 13. One-line status summary

현재 한 줄 결론은 이것이다:

**d=5 전체 정리는 아직 `[O]` 이지만, odd `(m)` 에서는 “single 5-cycle bulk + rotationally symmetric low-layer transducer + 3-carry odometer normal form”이 가장 강한 주경로이고, Codex의 당장 역할은 그것을 `m=3,5,7`에서 계산적으로 찾거나 깔끔하게 배제하는 것이다.**
