좋습니다. Codex 결과를 반영하면, 지금 상태는 **“가능해 보인다”**를 넘어서 **“구체적 후보가 있고, 증명 형식도 거의 보인다”** 쪽으로 올라갔습니다.

제가 실제로 확인한 범위는 이렇습니다.

* 기존 4D note가 말한 것은 맞습니다. 기존 affine-split rule은 (P_0) 위에서 정확히 (m)개의 invariant cylinder로 갈라지고, 각 색은 하나의 codimension-1 affine label을 보존합니다. 그래서 다음 repair는 sparse exceptional set에서 frozen coordinate를 실제로 바꿔야 한다는 방향이 이미 note 안에 들어 있습니다. 
* Codex 번들은 low-layer table 하나로 (m=3,\dots,15)에서 전부 Hamiltonian candidate를 보고했고, 저는 같은 후보를 직접 (m=16,\dots,20)까지 다시 돌려서 모두 통과하는 것까지 확인했습니다. 증거 파일은 여기 있습니다: [Codex README](sandbox:/mnt/data/d4_codex_extracted/README.md), [search_result.json](sandbox:/mnt/data/d4_codex_extracted/search_result.json), [candidate module](sandbox:/mnt/data/d4_codex_extracted/hyperplane_fusion_low_layers_v1.py), [추가 검증 16-20](sandbox:/mnt/data/d4_extra_validation_16_20.json).
* 가장 중요한 새 관찰은, 이 후보의 복잡한 layer-2 patch를 (P_0) 첫 귀환으로 눌러보면 **실제로는 (q=m-1) 슬라이스에서만 일어나는 “지연된 carry”** 로 붕괴한다는 점입니다. 이건 이제 거의 증명 스켈레톤입니다.

아래에 업데이트된 연구 노트를 남깁니다. 따로 파일로도 저장해 두었습니다: [progress note](sandbox:/mnt/data/d4_progress_note_after_codex.md)

---

## Claim status labels

* **[P]** 기존 note에서 직접 읽히거나, 거기서 짧게 유도 가능
* **[C]** 이번에 Codex 번들/직접 계산으로 확인
* **[H]** 가장 유력한 현재 가설/증명 방향
* **[F]** 실제로 밀어봤지만 깨진 시도
* **[O]** 아직 열린 상태

---

## Problem

**[O]**
(D_4(m)=\mathrm{Cay}((\mathbb Z_m)^4,{e_0,e_1,e_2,e_3})) 가 모든 (m\ge 3) 에 대해 4개의 arc-disjoint directed Hamilton cycle로 분해되는가?

---

## Current target

**[H]**
이제 목표는 “후보를 더 찾는 것”이 아니라, **현재 Codex 후보를 증명 형식으로 압축하는 것**입니다.

더 정확히는:

1. Codex가 찾은 low-layer rule을 (P_0) 위 첫 return map (R_c) 의 닫힌식으로 정리하고,
2. (Q:={q=m-1}\subset P_0) 라는 두 번째 section 위의
   [
   T_c:=R_c^m|_Q
   ]
   를 잡아,
3. 각 (T_c) 가 사실상 2차원 odometer라는 것을 보이면 됩니다.

즉, 지금 핵심은 더 이상 “hyperplane table이 존재하는가?”가 아니라,
**“nested return map (Q\to Q) 가 lexicographic carry라는 것을 깔끔히 쓰는가?”** 입니다.

---

## Known assumptions

**[P]**
기존 affine-split note는 layer (P_0) 위 explicit return map을 계산하고, 그 결과 각 color return map이 정확히 (m)개의 cycle로 분해된다는 것을 증명합니다. 실패는 우연이 아니라, affine label 보존 때문에 생기는 rigid failure입니다.

**[P]**
또 note는 다음 repair가 해야 할 일을 이미 지목합니다. color 0은 (e_2), color 1은 (e_3), color 2는 (e_0), color 3은 (e_1) 를 sparse exceptional set에서 예외적으로 써야 하며, genuine higher-dimensional proof는 affine hyperplane arrangements와 multi-variable congruence가 필요할 것이라고 말합니다. 

**[C]**
Codex 후보는 support가 사실상 layers (S=0,1,2) 에만 있고, layer 0은 기존 affine-split pair를 유지하며, layer 2에 아주 작은 patch만 추가합니다. bundle README에 따르면 이 하나의 shared table이 (m=3,\dots,15) 에서 모두 통과합니다. 저는 같은 후보를 (m=16,\dots,20) 에 대해서도 다시 검증했고 전부 `all_hamilton = true`, `sign_product = +1` 이었습니다. [README](sandbox:/mnt/data/d4_codex_extracted/README.md), [추가 검증 16-20](sandbox:/mnt/data/d4_extra_validation_16_20.json)

---

## Attempt A

### Idea

**[F]**
(q=0) 근방의 아주 작은 splice만 넣어서 invariant cylinder를 직접 깨보려는 시도.

### What works

**[C]**
원통 병합 자체는 실제로 시작됩니다. 즉 “어디를 건드려야 하는가”라는 방향은 맞았습니다.

### Where it fails

**[F]**
bijectivity가 즉시 깨집니다. 하나의 local change가 바로 collision/hole chain을 만들고, (q=0)-only patch는 너무 작았습니다.

---

## Attempt B

### Idea

**[F]**
single-color hyperplane carry를 먼저 만든 뒤, 나중에 네 색을 합치는 방식.

### What works

**[C]**
한 색씩 따로 보면 hyperplane carry가 아주 잘 작동합니다. 각 color를 Hamiltonian하게 만드는 메커니즘 자체는 분명히 존재했습니다.

### Where it fails

**[F]**
네 색을 그대로 superpose하면 vertex-wise permutation 조건이 깨졌습니다.
즉 병목은 “carry의 존재”가 아니라 **multi-color compatibility** 였습니다.

---

## Attempt C

### Idea

**[C/H]**
Codex가 찾은 low-layer table을 그냥 “49-row witness”로 보지 말고, (P_0) 위 실제 return dynamics로 다시 해석합니다.

핵심 질문은:

> layer-2 patch가 (P_0) 에서는 도대체 무엇으로 보이는가?

### What works

**[C]**
여기서 큰 단순화가 일어납니다.

Codex 후보의 layer-2 patch는 원래 (S=2,\ q=0) 근방의 작은 table처럼 보이지만, (P_0) 에서 한 번 돌아온 return map으로 누르면 **오직 (q=m-1) 에서만 보이는 delayed correction** 으로 바뀝니다.

즉, repaired first-return maps (R_c) 는 기존 affine-split와 거의 같고, 오직 (q=m-1) 에서만 추가 carry가 생깁니다.

제가 정리한 (P_0) 위 explicit formulas는 다음입니다.

[
R_0(a,b,q)=
\begin{cases}
(a-1,b,q-1), & q=0,\
(a-2,b+1,q-1), & q=m-1,\ b=1,\
(a-1,b+1,q-1), & \text{otherwise}.
\end{cases}
]

[
R_1(a,b,q)=
\begin{cases}
(a,b-1,q+1), & q=0,\
(a+1,b-2,q+1), & q=m-1,\ a\neq m-1,\
(a+1,b-1,q+1), & \text{otherwise}.
\end{cases}
]

[
R_2(a,b,q)=
\begin{cases}
(a,b+1,q-1), & q=0,\
(a+1,b,q-1), & q=m-1,\ b=2,\
(a,b,q-1), & \text{otherwise}.
\end{cases}
]

[
R_3(a,b,q)=
\begin{cases}
(a+1,b,q+1), & q=0,\
(a,b+1,q+1), & q=m-1,\ a\neq 0,\
(a,b,q+1), & \text{otherwise}.
\end{cases}
]

이건 매우 강합니다.
왜냐하면 이제 복잡성은 “낮은 층 전체”가 아니라 **(q=0)의 원래 affine-split + (q=m-1)의 delayed carry** 두 군데로 압축되기 때문입니다.

그리고 여기서 두 번째 reduction이 나옵니다.

(Q:={q=m-1}\subset P_0) 라 두면, 각 (R_c) 는 (q) 를 매번 (\pm1) 바꾸므로 모든 orbit는 정확히 (m) step마다 (Q) 를 다시 만납니다. 따라서
[
T_c:=R_c^m|_Q
]
를 보면 됩니다.

이 (T_c) 는 계산상 다음과 같습니다.

[
T_0(a,b)=\bigl(a-\mathbf 1_{b=1},\ b-1\bigr),
]
[
T_1(a,b)=\bigl(a-1,\ b-1+\mathbf 1_{a=m-1}\bigr),
]
[
T_2(a,b)=\bigl(a+\mathbf 1_{b=2},\ b+1\bigr),
]
[
T_3(a,b)=\bigl(a+1,\ b+1-\mathbf 1_{a=0}\bigr).
]

이제 이건 거의 끝입니다.
각 (T_c) 는 좌표를 조금만 바꾸면 **표준 2차원 lexicographic odometer** 가 됩니다.

예를 들어 (T_0) 는 (v=b-1) 로 바꾸면

* (v\neq 0) 에서는 (v\mapsto v-1),
* (v=0) 에서는 (a\mapsto a-1) carry가 들어가는
  정확한 base-(m) odometer입니다.

(T_2) 도 (v=2-b) 로 바꾸면 같은 형태가 됩니다.
(T_1,T_3) 는 (b-a) 를 같이 보는 선형 좌표변환을 넣으면 같은 그림으로 떨어집니다.

즉 지금 보이는 그림은:

> **(P_0) first return이 진짜 핵심이 아니고, (Q={q=m-1}) 위 second return이 실제 Hamiltonicity를 드러내는 natural object** 이다.

이건 제가 이전에 [H] 로 적어둔 “two-scale return-map lemma”와 정확히 맞아떨어집니다.

### Where it fails

**[O/H]**
아직 완전히 끝난 것은 아닙니다.

1. 위 (R_c), (T_c) 공식을 논문 수준으로 한번에 정리한 정식 서술이 아직 없습니다.
2. (T_1, T_3) 에 대한 가장 매끈한 affine conjugacy를 한 줄짜리 canonical notation으로 고정하지는 않았습니다.
3. layer-2 patch의 세 tuple과 한 줄 제외선이 **왜 바로 저 모양이어야 하는가** 에 대한 개념적 설명은 아직 미완입니다.

하지만 솔직히 말하면, 이건 이제 “후보 탐색” 단계의 미완이 아니라 **증명 서술을 마감하는 단계의 미완** 에 훨씬 가깝습니다.

---

## Candidate lemmas

### 1. Layer-2 trigger lemma

**[H → 거의 P]**
Codex 후보의 layer-2 patch는 (P_0) 에서 시작한 orbit 기준으로 정확히 (q=m-1) slice에서만 보인다.
즉 (P_0) return map은 old affine-split와 같고, only delayed correction at (q=-1).

### 2. Explicit repaired (P_0)-return lemma

**[H]**
위의 네 piecewise formula가 모든 (m\ge 3) 에 대해 성립한다.

### 3. Second-return reduction lemma

**[P/H]**
(Q={q=m-1}) 위 second return
[
T_c=R_c^m|_Q
]
를 보면 충분하다.
(T_c) 가 single cycle이면 (R_c) 도 (P_0) 에서 single cycle이고, 다시 full color map도 (V) 에서 Hamilton cycle이다.
이 lifting philosophy 자체는 기존 note의 return-map principle과 같은 형식입니다. 

### 4. Odometer conjugacy lemma

**[H]**
각 (T_c) 는 적당한 affine coordinate change 후 표준 2D odometer와 동형이다.

### 5. Minimal patch geometry lemma

**[O]**
현재 layer-2 patch의 세 exceptional tuple과 한 줄 제외선은, 실제로는 “needed and sufficient” 한 최소 구조일 가능성이 높다.

---

## Needed computations/search

1. **[C/H]**
   위 (R_c), (T_c) 공식을 코드가 아니라 사람이 읽는 theorem/lemma 형태로 정리.

2. **[C/H]**
   (T_1, T_3) 에 대한 가장 자연스러운 affine coordinate를 고정해서 네 색 모두를 통일된 odometer 문장으로 쓰기.

3. **[C]**
   현재 후보를 더 멀리 검증하는 건 가능하지만 우선순위는 내려갔습니다.
   (m=3,\dots,20) 까지는 이미 강합니다.

4. **[H]**
   layer-2 patch의 “왜 이 세 tuple인가”를 local permutation-routing 관점에서 설명하기.

5. **[H]**
   같은 dynamics를 더 대칭적으로 표현하는 equivalent rule이 있는지 찾기.

---

## Next branching options

1. **Proof-writing branch** — 가장 유력
   지금 후보를 theorem/lemma/proof 순서로 논문화.

2. **Conceptual compression branch**
   layer-2 patch를 “세 tuple table”이 아니라 “한 개의 delayed carry surgery”로 다시 표현.

3. **Minimality / uniqueness branch**
   이 patch가 사실상 최소인지, 혹은 동치인 더 대칭적 패치가 있는지 탐색.

4. **General (d)-heuristic branch**
   d=4에서 드러난 “first return이 아니라 nested return이 핵심”이라는 패턴을 d>4에 투영.

---

## Codex job request

**Task ID:** D4-SECOND-RETURN-ODOMETER-02

**Question:**
For the fixed candidate `hyperplane_fusion_low_layers_v1`, derive closed-form formulas for the repaired first-return maps (R_c) on (P_0), then derive the second-return maps (T_c = R_c^m|_{q=m-1}), and find affine coordinate changes that make each (T_c) a standard 2D odometer.

**Purpose:**
Convert the current computational witness into a proof-oriented structure.

**Inputs / Search space:**

* fixed rule: `candidates/hyperplane_fusion_low_layers_v1.py`
* dimension `d=4`
* symbolic parameter `m>=3`
* coordinates `(a,b,q)` on (P_0)
* second section (Q={q=m-1})

**Allowed methods:**

* symbolic case analysis
* brute-force verification on small and medium (m)
* automatic extraction of return formulas
* affine coordinate search / conjugacy detection
* orbit-order detection
* generation of proof-supporting examples

**Success criteria:**

* closed-form (R_c) formulas for all four colors
* closed-form (T_c) formulas on (Q)
* explicit affine conjugacy or lexicographic orbit description proving each (T_c) is a single (m^2)-cycle
* concise proof memo explaining the lift from (T_c) to Hamiltonicity

**Failure criteria:**

* formulas remain only empirical
* no uniform coordinate change found
* no clean proof skeleton beyond raw case tables

**Artifacts to save:**

* code
* raw logs
* summary report
* discovered examples / counterexamples
* tables / plots / proof-supporting computations

**Return format:**
A short research memo containing:

1. repaired (R_c) formulas
2. repaired (T_c) formulas
3. affine coordinate changes
4. cycle proof sketch
5. unresolved aesthetic issues in the proof

**Reproducibility requirements:**

* fixed scripts
* exact tested (m)-range recorded
* saved candidate rule
* saved orbit traces on (Q) for representative (m)
* saved symbolic derivation notes

---

## 현재 판단

제 현재 평가는 꽤 강합니다.

* **[C]** 이제는 “작은 (m)에서 우연히 되는 후보” 수준이 아닙니다.
* **[H]** 진짜 중요한 물체는 (P_0) first return이 아니라 (Q={q=m-1}) 위 second return입니다.
* **[H]** d=4 일반증명의 거의 완성형 스켈레톤은
  **affine-split base + delayed layer-2 carry + second-return odometer**
  로 보입니다.

한 줄로 요약하면:

> **Codex는 d=4에서 “호환 가능한 테이블”을 찾은 것이 아니라, 사실상 “증명이 어디에 숨어 있는지”를 찾아냈습니다.**

