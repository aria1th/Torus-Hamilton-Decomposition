좋습니다. Gemini의 “국소 수술” 해석은 방향상 맞습니다. 다만 제가 지금 실제로 밀어본 restricted computation까지 합치면 병목은 더 선명합니다:

**d=4에서 어려운 것은 ‘한 색의 불변 원통을 깨는 것’ 자체가 아니라, 그 수술을 네 색이 동시에 수행하면서도 각 저층 정점에서 방향 4개가 permutation이 되게 만드는 것**입니다.

아래는 그 관점으로 다시 정리한 연구 노트입니다.

---

## Claim status labels

* **[P]** 현재 note에서 직접 읽히거나, 거기서 바로 따라 나오는 짧은 유도
* **[C]** 제가 방금 제한된 범위에서 직접 계산/시뮬레이션한 것
* **[H]** 현재 가장 유력한 가설/설계 방향
* **[F]** 실제로 밀어봤는데 깨진 시도 또는 반례
* **[O]** 아직 열린 상태

---

## Problem

**[O]**
(D_4(m)=\mathrm{Cay}((\mathbb Z_m)^4,{e_0,e_1,e_2,e_3})) 가 모든 (m\ge 3) 에 대해 **4개의 arc-disjoint directed Hamilton cycle**로 분해되는가?

---

## Current target

**[H]**
지금 당장의 목표는 전체 정리를 바로 증명하는 것이 아니라, 현재 affine-split 후보의 실패를 만드는 **(m)개의 invariant cylinder**를 실제로 하나로 병합하는 메커니즘을 찾는 것입니다.
더 정확히는:

1. (P_0) 위의 1차 return map만 보는 수준을 넘어서,
2. (P_0) 안의 또 다른 codim-1 section에 대한 **2차 return map**을 잡고,
3. 그 coarse monodromy가 단순 translation이 아니라 **2차원 carry / odometer / finite splice** 형태가 되게 만드는 것.

이건 현재 note가 말하는 “one-affine-form cylinder model을 넘어서 affine hyperplane arrangements, multi-variable congruence, multi-homology splice가 필요하다”는 진단과 정확히 맞닿아 있습니다.

---

## Known assumptions

**[P]**
현재 4D note는 layer function (S=x_0+x_1+x_2+x_3) 와 section (P_0={S=0}) 를 잡고, 색별 (m)-step return map (R_c) 로 문제를 환원합니다. 또한 (R_c) 가 bijective이면 원래 색상 map (f_c) 의 cycle 구조가 그대로 lift되며 길이는 (m)배가 됩니다.

**[P]**
현재 affine-split 후보의 explicit return map은 ((a,b,q))-좌표에서 주어지고, 한 full (q)-turn 뒤에는
[
R_0^m(a,b,q)=(a,b-1,q),\quad
R_1^m(a,b,q)=(a-1,b,q),
]
[
R_2^m(a,b,q)=(a,b+1,q),\quad
R_3^m(a,b,q)=(a+1,b,q)
]
가 됩니다. 그래서 각 색은 (P_0) 위에서 길이 (m^2) 인 cycle (m)개로 분해되고, (V) 위에서는 길이 (m^3) 인 cycle (m)개가 됩니다.

**[P]**
실패는 우연이 아니라 rigid합니다. 현재 후보는
[
\lambda_0=a-q=-x_2,\quad
\lambda_1=b+q=-x_3,\quad
\lambda_2=a=x_0,\quad
\lambda_3=b=x_1
]
를 각각 보존하여 (P_0) 를 (m)개의 invariant cylinder로 쪼갭니다. note는 따라서 성공적인 repair가 색 (0,1,2,3) 에 대해 각각 예외적으로 (e_2,e_3,e_0,e_1) 를 써야 한다고 말합니다.

**[H]**
따라서 현재의 핵심 질문은 “불변 원통을 깰 수 있는가?”가 아니라,
**“원통을 깨는 carry를 어떤 section 위에 올릴 것인가, 그리고 그 carry를 네 색이 동시에 양립하게 만들 수 있는가?”** 입니다.

---

## Attempt A

### Idea

**[H]**
Gemini가 짚은 방향처럼, 가장 먼저 떠오르는 건 **(q=0) 근방의 아주 얇은 splice** 입니다.
가장 단순하게는 color 0에서, (q=0) 인 일부 affine line 위에서만 baseline의 (e_3) 를 (e_2) 로 바꾸는 방식입니다.

예를 들어
[
E_r={(a,b,q)\in P_0:\ q=0,\ a+b=r}
]
위에서만 color 0의 방향을 (e_2) 로 바꾸고, 나머지는 기존 affine-split baseline을 유지해 보는 것입니다.

### What works

**[P]**
이 시도가 왜 자연스러운지는 note의 Remark 8에서 바로 나옵니다. color 0은 현재 (x_2) 를 전혀 바꾸지 않기 때문에, 결국 (e_2) 를 예외적으로 도입해야만 (\lambda_0) 불변량을 깰 수 있습니다.

**[P]**
더 강하게, 이건 “충돌 연쇄”가 실제로 어떻게 생기는지 algebraically 바로 보입니다.
현재 note의 color 0 공식은
[
R_0(a,b,q)=
\begin{cases}
(a-1,b,q-1), & q=0,\
(a-1,b+1,q-1), & q\neq 0
\end{cases}
]
입니다.

이제 (y=(a,b,0)) 에서만 (e_3\to e_2) 로 바꾸면
[
R_0'(y)=(a-1,b,0).
]
그런데 baseline을 유지한 점
[
x=(a,b-1,1)
]
도 여전히
[
R_0(x)=(a-1,b,0)
]
로 갑니다. 즉 **즉시 2-to-1 collision** 이 납니다. 동시에 원래 (y) 가 보내던
[
(a-1,b,m-1)
]
은 비게 됩니다.
그래서 (q=0) 에서의 단일 수정은 곧바로 **(q=1)과 (q=m-1) 쪽 보정 사슬**을 강제합니다.

**[C]**
실제로 line patch (E_0={q=0,\ a+b=0}) 를 color 0에 넣어 제한 계산을 해보면, 동역학 자체는 꽤 “맞는 방향”으로 움직입니다.

* (m=5): 가장 긴 cycle 길이 (105)
* (m=6): 가장 긴 cycle 길이 (186)
* (m=7): 가장 긴 cycle 길이 (301)

즉 기존의 (m)개 cylinder 구조를 실제로 많이 병합합니다.

### Where it fails

**[F]**
하지만 이 patch는 **bijective가 아닙니다**.

* (m=5,6,7) 에서 각각 정확히 **(m)개의 collision** 과 **(m)개의 missing image** 가 생겼습니다.
* preimage multiplicity는 전부 2였고, “한 줄을 건드리면 바로 한 줄의 충돌과 한 줄의 구멍이 생기는” 패턴이었습니다.

즉, **작은 (q=0)-only splice는 cylinder merging 자체는 시작하지만, permutation 성질을 보존하지 못합니다.**

### Interim conclusion

**[H]**
Gemini의 “chain of dependencies”는 맞습니다.
다만 지금 보이는 건 더 구체적입니다:

> **(q=0) 에서만 하는 작은 수술은 너무 작다.
> 최소한 인접 (q)-layer들까지 따라가는 라우팅 체인, 혹은 아예 다른 coarse section에서의 carry 설계가 필요하다.**

---

## Attempt B

### Idea

**[H]**
Attempt A가 너무 작았다면, 반대로 **codim-1 hyperplane 전체를 carry patch로 쓰는 것**은 어떨까를 봤습니다.

놀랍게도, 한 색씩 따로 보면 아주 깨끗한 패턴이 나옵니다.

* color 0: (x_0=s) 위에서 예외적으로 (e_2)
* color 1: (x_1=s) 위에서 예외적으로 (e_3)
* color 2: (x_2=s) 위에서 예외적으로 (e_0)
* color 3: (x_3=s) 위에서 예외적으로 (e_1)

즉, **각 color (c) 가 자신의 coordinate hyperplane (x_c=s) 를 지날 때 “필요한 예외 방향” (e_{c+2}) 를 쓴다**는 매우 대칭적인 규칙입니다.

### What works

**[P]**
color 0은 거의 바로 증명됩니다. (a=x_0) 라 쓰고, (a=0) 위에서만 예외 방향 (e_2) 를 쓰면 color 0의 return map은
[
R_0^\star(a,b,q)=
\begin{cases}
(a-1,b,q), & a=0,\
(a-1,b,q-1), & a\neq 0,\ q=0,\
(a-1,b+1,q-1), & a\neq 0,\ q\neq 0.
\end{cases}
]
가 됩니다.

이제 section
[
A_0={a=0}
]
를 보면, (a) 는 매 step마다 (-1) 되므로 모든 orbit는 정확히 (m) step마다 (A_0) 로 돌아옵니다.
그 (m)-step return (M) 은 ((b,q)) 위에서
[
M(b,q)=
\begin{cases}
(b-2,\ q+1), & q\neq m-1,\
(b-1,\ 0), & q=m-1.
\end{cases}
]
가 됩니다.

따라서 (q) 는 빠른 시계처럼 한 칸씩 돌고, (q) 가 한 바퀴 돈 뒤에는
[
M^m(b,q)=(b+1,q)
]
가 됩니다.
즉 (M) 은 정확히 **2차원 odometer** 이고, 하나의 (m^2)-cycle입니다. 그러면 (R_0^\star) 는 하나의 (m^3)-cycle입니다.

이건 매우 중요합니다.
**한 색에 대해서는 d=4에서도 carry mechanism이 이미 아주 단순한 hyperplane patch로 구현됩니다.**

**[C]**
같은 유형의 hyperplane patch를 다른 색에 대해 계산해 보면, 아래 규칙이 (m=3,\dots,10) 모든 테스트에서 각각 단일 (m^3)-cycle을 만들었습니다.

* color 0: (x_0=s) 에서 (e_2)
* color 1: (x_1=s) 에서 (e_3)
* color 2: (x_2=s) 에서 (e_0)
* color 3: (x_3=s) 에서 (e_1)

즉 **“한 색을 Hamiltonian하게 만드는 것” 자체는 이미 매우 구조적으로 보입니다.**

### Where it fails

**[F]**
문제는 이 네 개를 **그대로 합치면 안 된다**는 점입니다.

가장 naive하게 (s=0) 으로 맞춰 동시에 superpose하면, layer 0의 방향 quadruple이 permutation이 아니게 됩니다. 제한 계산에서 bad vertex 수는

* (m=3): 16
* (m=4): 36
* (m=5): 64
* (m=6): 100

이었습니다. 즉 관찰상 (4(m-1)^2) 꼴입니다.

의미는 명확합니다.

> **single-color carry는 해결되었고, multi-color compatibility가 진짜 병목이다.**

이건 Gemini가 말한 “아핀 초평면 배열 + 다변수 합동 제약”과 정확히 맞습니다. 다만 저는 그걸 더 날카롭게 말하고 싶습니다:

> **d=4의 다음 정리는 새 global dynamics를 발명하는 문제가 아니라,
> 이미 보이는 네 개의 single-color odometer hyperplane을 어떻게 동시에 엮을지에 대한 finite compatibility theorem 문제에 가깝다.**

---

## Candidate lemmas

1. **Local collision propagation lemma** — **[P]**
   color 0에서 (q=0) 점 하나를 (e_3\to e_2) 로 바꾸면 즉시 하나의 collision과 하나의 hole가 생긴다.
   따라서 (q=0)-only patch는 본질적으로 불가능하고, 적어도 인접 (q)-layer까지 라우팅 체인을 가져야 한다.

2. **Single-color hyperplane odometer lemma** — **[P]** for color 0, **[C]** for the other three
   각 color (c) 에 대해 hyperplane (x_c=s) 위에서만 예외 방향 (e_{c+2}) 를 쓰면, 그 color의 return dynamics는 codim-1 section 위에서 2차원 odometer가 되어 단일 cycle이 된다.

3. **Finite compatibility lemma** — **[H]**
   위 네 single-color hyperplane carry를 동시에 넣기 위해서는, hyperplane 교차 패턴들 위에 대해 **유한 개의 예외 permutation table** 이 존재해야 한다.
   d=4 일반증명의 핵심은 아마 이 유한 compatibility lemma일 가능성이 크다.

4. **Two-scale return-map lemma** — **[H]**
   d=4에서는 (P_0) 위 1차 return만으로는 부족하고, (P_0) 안의 codim-1 section에 대한 2차 return이 실제 Hamiltonicity를 드러내는 natural object일 가능성이 높다.

5. **Route-E-type proof skeleton for d=4** — **[H]**
   증명 형식은 아마
   **primary geometry → precise compatibility obstruction → boundary-only / intersection-only no-go → actual repaired local table → finite splice**
   순서가 될 것이다.

---

## Needed computations/search

1. **[C]**
   hyperplane 교차 타입별 finite table search

   * features: (x_0=s_0,\ x_1=s_1,\ x_2=s_2,\ x_3=s_3,\ q=0) 여부
   * 목표: 각 pattern마다 어떤 permutation을 줄지 탐색

2. **[C]**
   위 finite table이 실제로 각 color map을 permutation으로 만드는지 검사

3. **[C]**
   candidate rule에 대해 2차 return map을 자동 추출하고, odometer/finite-splice closed form이 나오는지 확인

4. **[C]**
   (m=3,4,5,6) 에서 exhaustive / SAT / CP-SAT로 restricted family를 완전 탐색하고, 공통 패턴이 보이면 symbolic formula로 승격

5. **[C]**
   Attempt A 류의 q-chain repair도 보조적으로 확인

   * “작은 splice + 인접 q-layer chain”이 실제 finite closure를 갖는지
   * 혹은 hyperplane approach가 훨씬 우월한지 비교

---

## Next branching options

1. **Hyperplane-fusion branch** — **가장 유력 [H]**
   네 single-color hyperplane carry를 출발점으로 잡고, 교차부의 finite compatibility patch를 찾는다.

2. **SAT/CP finite-table branch** — **매우 유력 [H]**
   위 branch를 사람 손으로 하지 말고, low-layer/local-pattern family를 완전 탐색해 작은 (m) 에서 해를 먼저 뽑는다.

3. **q-chain routing branch** — **보조적 [H]**
   Attempt A의 collision/hole를 따라가며 finite chain closure를 설계한다.
   다만 지금 느낌으로는 이쪽은 너무 국소적이라 최종 구조가 지저분해질 가능성이 크다.

4. **Alternative section branch** — **중간 우선순위 [H]**
   (P_0) 말고, (P_0) 안의 더 자연스러운 codim-1 section을 먼저 잡아 거기서 monodromy를 설계하는 방법.

---

## Codex job request

**Task ID:** D4-HYPERPLANE-FUSION-01

**Question:**
Does there exist a low-complexity low-layer direction assignment for (D_4(m)), built from the hyperplane triggers
[
x_0=s_0,\quad x_1=s_1,\quad x_2=s_2,\quad x_3=s_3
]
(and optionally (q=x_0+x_2=0), plus possibly layers (S\in{0,1,2})),
such that:

1. at every vertex the four directions form a permutation of ({0,1,2,3}), and
2. for each color, the induced return map is a single cycle for small (m), ideally revealing a uniform odometer / finite-splice formula?

**Purpose:**
Turn the current qualitative picture into a finite compatibility problem.
Either find a common hyperplane-fusion rule, or show that this restricted family is impossible.

**Inputs / Search space:**

* Base ambient digraph: (D_4(m)) for (m=3,4,5,6) first
* Start from the affine-split baseline outside the low layers
* Pattern features may include:

  * (x_0=s_0)
  * (x_1=s_1)
  * (x_2=s_2)
  * (x_3=s_3)
  * (q=0)
  * optional low-layer index (S\in{0,1,2})
* A candidate rule assigns one permutation in (S_4) to each realized local pattern type
* Symmetry reduction strongly encouraged

**Allowed methods:**

* exhaustive search over pattern tables
* SAT / CP-SAT / MILP encodings
* symmetry reduction / orbit compression
* brute-force cycle verification on small (m)
* symbolic extraction of first-return / second-return formulas
* counterexample generation

**Success criteria:**

* Find at least one candidate family that works for (m=3,4,5,6), and
* produce a concise closed-form description of its induced monodromy, or
* prove that no rule exists in this restricted family

**Failure criteria:**

* No candidate found in the restricted family
* Search is too large without symmetry reduction
* Found candidates only work sporadically with no stable formula

**Artifacts to save:**

* code
* raw logs
* summary report
* discovered examples / counterexamples
* tables / plots / proof-supporting computations

**Return format:**
A short research memo with:

1. searched family definition
2. symmetry reductions used
3. successful candidates or impossibility result
4. exact cycle statistics by (m)
5. extracted return-map formulas if any
6. recommended next family if this one fails

**Reproducibility requirements:**

* fixed random seeds
* exact searched (m)-range recorded
* scripts runnable from a clean environment
* candidate pattern tables saved in a canonical JSON format
* cycle decompositions or return-map summaries saved for each successful case

---

## My current view

**[H]**
Gemini의 큰 방향은 맞지만, 지금 단계에서 저는 초점을 이렇게 바꾸겠습니다.

* **너무 작은 (q=0)-only patch**는 거의 확실히 부족합니다.
* 반대로 **single-color hyperplane carry**는 이미 작동합니다.
* 따라서 d=4 일반증명의 다음 문턱은
  **“carry를 만드는 것”이 아니라 “네 개의 carry를 동시에 호환시키는 finite local theorem”**
  으로 보입니다.

즉, 지금 가장 유력한 그림은
**hyperplane odometer + intersection compatibility patch + finite splice**
입니다.
