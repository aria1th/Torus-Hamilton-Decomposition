# P-NP 인터페이스 공리계 작업 메모 (Markdown working memo)

## 0. 현재 버전의 목표

이 메모의 목표는 **SAT 자기환원 과정에서 무엇이 '재사용 가능한 의미론적 상태'인지**를 공리화하고,
그 공리계가 OBDD / structured d-DNNF / SDD / AOMDD를 각각 특수화로 회수하는지 점검하는 것이다.

중요한 교정 하나:
이전 버전에서는 local 상태를 "잔여 함수의 개수" 쪽으로 보려 했다.
하지만 structured d-DNNF 단계에서는 이보다 한 단계 위인 **컷 관계(cut relation)** 를 기본 객체로 보는 편이 더 정확하다.

즉, 이제 local 불변량은
- 단일 residual function 하나가 아니라,
- **context × inside-assignment** 위의 Boolean relation을
얼마나 작은 인터페이스로 정확하게 표현할 수 있는가
로 정의한다.

이 변화의 장점은 다음 셋이다.
1. OBDD의 row/residual 관점과 structured d-DNNF의 deterministic cut decomposition을 같은 언어로 기술할 수 있다.
2. pathwidth/treewidth 같은 구문 폭 이론보다 의미론적이다.
3. 정준성(canonicity)과 분해력(decomposability)을 분리해서 다룰 수 있다.

---

## 1. 데이터: support-context 시스템

변수 집합을 `X`라 하고, Boolean function을

\[
f: \{0,1\}^X \to \{0,1\}
\]

라 하자.

### 정의 1 (support-context 시스템)
하나의 support-context 시스템은

\[
(\mathfrak R, \mathrm{Ctx})
\]

로 이루어지며,

- `\mathfrak R \subseteq 2^X` 는 solver가 상태를 둘 수 있는 support들의 가족이다.
- 각 `R \in \mathfrak R`에 대해 `\mathrm{Ctx}(R)`는 domain이 `X \setminus R`인 admissible partial assignment들의 집합이다.

직관:
- OBDD: `R`는 suffix variable set, `Ctx(R)`는 prefix assignment.
- structured d-DNNF / SDD: `R`는 vtree 노드의 변수 집합, `Ctx(R)`는 shell restriction.
- AOMDD: `R`는 pseudo tree/context에 의해 정해지는 남은 변수 집합, `Ctx(R)`는 그 바깥 context.

---

## 2. 핵심 객체: 컷 관계(cut relation)

### 정의 2 (cut relation)
`R \in \mathfrak R`, `\alpha \in \mathrm{Ctx}(R)`, `\beta \in \{0,1\}^R`에 대해

\[
M^f_R(\alpha,\beta) := f(\alpha \cup \beta)
\]

를 정의한다.

여기서 `M^f_R`는

\[
\mathrm{Ctx}(R) \times \{0,1\}^R \to \{0,1\}
\]

인 Boolean relation이다.

이 relation이 바로 **support `R`를 가로지르는 정확한 의미론적 인터페이스**다.

### 왜 이 정의가 중요한가
- OBDD에서는 `M^f_R`의 서로 다른 row가 서로 다른 residual/state를 준다.
- structured d-DNNF에서는 `M^f_R`를 deterministic rectangles 또는 deterministic cut-decomposition으로 표현하는 문제가 된다.
- SDD에서는 여기에 compressed partition / canonical compression이 추가된다.

즉, row-count / decomposition-width / compressed partition size가 모두
**같은 객체 `M^f_R`의 다른 표현 비용**으로 보인다.

---

## 3. 인터페이스 언어

### 정의 3 (interface language)
각 `R \in \mathfrak R`에 대해, `\mathcal I(R)`를 `M^f_R` 같은 relation의 정확한 표현 객체들의 집합이라 하자.
각 객체 `I \in \mathcal I(R)`에는

- 의미론 `\llbracket I \rrbracket_R`,
- 비용 함수 `\ell_R(I) \in \mathbb N`

가 붙는다.

즉,

\[
\llbracket I \rrbracket_R : \mathrm{Ctx}(R) \times \{0,1\}^R \to \{0,1\}.
\]

### 정의 4 (local interface cost)

\[
\delta_{\mathfrak C}(f,R)
:=
\min\{\ell_R(I) : I \in \mathcal I(R),\ \llbracket I \rrbracket_R = M^f_R\}.
\]

이 `\delta_{\mathfrak C}(f,R)`를 support `R`에서의 **local interface cost**라고 부른다.

핵심 포인트:
- 이 수치만 잘 정의되어도, "그 support에서 최소 몇 개의 의미론적 원자가 필요한가"를 측정할 수 있다.
- structured d-DNNF 단계에서는 이것이 최소 deterministic decomposition 크기로 내려앉고,
- OBDD 단계에서는 row/residual 기반 width로 내려앉는다.

---

## 4. 기본 공리 4개

아래 네 개는 공통분모 쪽 공리다. 이들은 OBDD / structured d-DNNF / SDD / AOMDD를 모두 수용하는 방향으로 의도했다.

### B1. Support-context typing
모든 interface 객체는 어떤 support `R`에 속해야 하고, 그 의미론은 정확히

\[
\mathrm{Ctx}(R) \times \{0,1\}^R
\]

위 relation이어야 한다.

의미:
local 상태는 항상 "어느 컷을 기준으로 한 정보인가"를 잃어버리면 안 된다.

### B2. Exactness
solver가 `R`에서 쓰는 interface는 반드시 정확해야 한다.
즉 approximate summary가 아니라,

\[
\llbracket I \rrbracket_R = M^f_R
\]

형태의 exact representation이어야 한다.

의미:
이 프로그램은 heuristic SAT가 아니라, exact SAT / exact compilation을 겨냥한다.

### B3. Conditioning closure
`x \in R`, `b \in \{0,1\}`일 때, support가 `R \setminus \{x\}`로 내려가는 restriction 연산이 내부적으로 구현되어야 한다.

의미론은

\[
M^f_{R\setminus\{x\}}(\alpha \cup \{x=b\},\beta) = M^f_R(\alpha, \beta \cup \{x=b\})
\]

와 일치해야 한다.

직관:
branching/self-reduction의 핵심은 conditioning이므로, 이 연산은 기본 공리여야 한다.

### B4. Decomposition closure (약한 형태)
support가 `R = R_1 \sqcup R_2`로 독립 분해될 때,
해당 분해를 반영하는 합성 연산이 interface 언어에 허용되어야 한다.

여기서 **약한 형태**라고 한 이유는,
- 합성이 존재한다는 것만 기본 공리로 두고,
- 그 비용이 additive인지, polytime인지 등은 모델별 특성으로 남겨둔다.

이렇게 약하게 잡아야 OBDD를 탈락시키지 않으면서도 structured d-DNNF/SDD/AOMDD를 포괄할 수 있다.

---

## 5. 선택 공리 2개

이 둘은 강한 모델을 설명하기 위한 선택 공리다.

### O1. Canonical compression
semantic equivalence class마다 유일한 compressed normal form이 존재한다.

즉, 정규화 사상 `\nu_R`가 있어서 같은 의미를 갖는 객체는 같은 정규형으로 압축된다.

이 공리는:
- OBDD: 강하게 성립
- SDD: compressed form에서 성립
- AOMDD: 주어진 pseudo tree 아래에서 성립
- structured d-DNNF: 일반적으로는 기본 공리로 두기 어렵다

### O2. Flux lifting
local에서 태어나는 genuinely new interface mass의 총합이 solver 전체 크기를 하한한다.

이것은 현재 **정리라기보다 연구 목표**다.
OBDD에서는 거의 정확식으로 보이고,
structured d-DNNF 이상에서는 아직 일반 정리로 확보되지 않았다.

---

## 6. faithful solver

이제 solver 자체를 공리계 상대적으로 정의한다.

### 정의 5 (`\mathfrak C`-faithful solver)
`\mathfrak C = (\mathfrak R,\mathrm{Ctx},\mathcal I,\Gamma,\ell)`에 대해,
solver `S`가 `\mathfrak C`-faithful하다는 것은 다음을 뜻한다.

1. 각 state `q`는 support `R(q) \in \mathfrak R`를 갖는다.
2. 각 state `q`는 interface `I(q) \in \mathcal I(R(q))`를 갖는다.
3. root state는 전체 함수 `f`에 대응한다.
4. branch step은 B3의 conditioning과 일치해야 한다.
5. decomposition step은 B4의 허용 합성과 일치해야 한다.
6. merge는 semantic soundness를 위배하지 않아야 한다.
   즉 선택 공리 O1이 있다면 같은 compressed normal form끼리만 merge한다.

설명:
이 정의는 "solver의 영리함"을 전부 인터페이스 언어 안으로 끌어내린다.
따라서 하한 문제는
- solver의 구현 세부가 아니라,
- 그 solver가 허용하는 interface 언어의 한계
로 바뀐다.

---

## 7. 안전한 핵심 명제와 아직 열린 명제

아래에서 **핵심 정의/틀**과 **비자명한 연구 목표**를 분리한다.

### 안전한 핵심 A: local 불변량은 잘 정의된다
각 support `R`에 대해 `\delta_{\mathfrak C}(f,R)`는 exact cut relation `M^f_R`의 최소 표현 비용이다.
이건 정의 수준에서 안전하다.

### 안전한 핵심 B: OBDD / structured d-DNNF / SDD / AOMDD는 서로 다른 특수화다
이건 모델 회수(calibration) 문제다.

- OBDD: `\mathfrak R`는 선형 suffix supports, local cost는 row/residual 기반 width, canonical compression 강함.
- structured d-DNNF: `\mathfrak R`는 vtree supports, local cost는 deterministic cut decomposition 크기, canonical compression은 기본 공리가 아님.
- SDD: structured d-DNNF의 vtree 세계에서 compressed partition과 canonical compression을 추가한 형태.
- AOMDD: pseudo tree / context 기반, canonicality와 semantic treewidth의 동기가 강함.

### 연구 목표 C: representation meta-theorem
**목표 형태**

> 임의의 `\mathfrak C`-faithful solver `S`와 support `R`에 대해,
> `S`가 `R`에서 유지해야 하는 live interface mass는 `\delta_{\mathfrak C}(f,R)`를 하계로 갖는다.

이 명제는 rigid/canonical한 모델에서는 거의 tautological하지만,
일반적인 interface 언어에서는 정확한 정식화가 더 필요하다.

### 연구 목표 D: flux lifting theorem
**목표 형태**

> local birth mass들의 총합이 solver 전체 DAG 크기를 하한한다.

이건 OBDD에서는 사실상 맞는 그림이지만,
structured d-DNNF 이상에서는 아직 프로그램 수준이다.

---

## 8. 왜 이 공리계가 기존 틀을 넘어서는가

### (i) 폭 이론보다 의미론적이다
pathwidth/treewidth는 강력하지만, 기본적으로 구문/그래프 쪽 구조를 본다.
반면 이 공리계는 애초에 `M^f_R`라는 cut relation의 exact 표현 비용을 local invariant로 삼는다.
따라서 semantic treewidth가 시사하는 "동일 함수의 다른 표현이 전혀 다른 컴파일 난이도를 낳는다"는 현상을 직접 수용한다.

### (ii) 최종 언어보다 과정(process)에 가깝다
knowledge compilation map은 결과 언어의 succinctness와 polytime 질의/변환을 비교한다.
반면 여기서는 solver가 자기환원 도중 어떤 local state를 저장하고, 어떤 context에서 그 state를 재사용하며, 어디서 branch/decomposition/merge를 수행하는지를 기본 데이터로 둔다.

### (iii) 정준성과 분해력을 분리한다
structured d-DNNF와 SDD는 같은 vtree 세계를 공유하지만,
전자는 local decomposition 폭이 핵심이고,
후자는 그 위에 canonical compression이 더해진다.
이 차이를 기본 공리 4개 + 선택 공리 2개 구조가 자연스럽게 설명한다.

---

## 9. 모델별 빠른 회수표

| 모델 | support | local interface의 핵심 | O1 canonical compression | O2 flux lifting |
|---|---|---|---|---|
| OBDD | 선형 suffix | row/residual quotient | 예 | 거의 정확식 수준 |
| structured d-DNNF | vtree node | minimal deterministic cut decomposition | 일반적으로 아님 | 아직 미정 |
| SDD | vtree node | compressed partition | 예 | 미정 |
| AOMDD | pseudo tree / context | AND/OR context-merged interfaces | 예(주어진 pseudo tree) | 미정 |

---

## 10. 다음 단계

다음에는 아래 둘 중 하나로 가면 된다.

### 경로 A: 첫 메타정리의 약한 버전
다음을 엄밀히 적는다.

> solver가 `\mathfrak C`-faithful하면, 각 support `R`에 대해 solver의 live states는 `M^f_R`의 exact interface representation을 유도한다.

이 버전은 표현 정리 쪽이다.

### 경로 B: OBDD → structured d-DNNF → SDD 순의 검산 강화
- OBDD에서는 `\delta`와 실제 노드 수/flux가 어떻게 정확히 맞물리는지 쓴다.
- structured d-DNNF에서는 `\delta`가 minimal deterministic decomposition 크기로 내려앉는지 쓴다.
- SDD에서는 O1이 왜 실제로 정준성을 회복하는지 붙인다.

내 판단으로는, 지금 가장 자연스러운 다음 한 걸음은 **경로 A**다.
즉, faithful solver가 local cut relation을 정확히 유도한다는 약한 메타정리를 먼저 짧게 써두는 편이 좋다.

---

## 11. 상태 표시

- 정의/틀: 비교적 단단함
- 모델 회수: 상당히 유망함
- flux lifting: 아직 핵심 미해결
- yes-side / no-side 통합: 뒤 단계

즉 현재 프로그램의 안전한 핵심은

> "컷 관계의 최소 exact 표현 비용을 local 불변량으로 삼는다"

이고,
가장 큰 열린 문제는

> "이 local 비용이 전체 solver 크기로 어떻게 증폭되는가"

이다.

---

## 12. 약한 메타정리 초안

### 목표 정리 A (representation-soundness, 약한 형태)
`f`를 Boolean function, `\mathfrak C`를 interface calculus, `S`를 `\mathfrak C`-faithful exact solver라고 하자.
그렇다면 `S`가 실제로 방문하는 각 support `R`에 대해,
`S`의 `R`-상태들의 live family는 cut relation `M^f_R`의 exact representation을 유도한다.

직관적으로는,
- root에서 출발한 정확한 solver라면,
- 어느 support `R`에 도달한 뒤 남은 모든 행동은
- 결국 `M^f_R`가 정하는 의미론을 보존해야 하므로,
- live states를 충분히 많이 합쳐서 보면 `M^f_R`의 exact interface description 하나를 읽어낼 수 있어야 한다.

이 정리가 성립하면 바로

\[
\text{local live interface mass at }R \ge \delta_{\mathfrak C}(f,R)
\]

라는 하한이 따라온다.

### 어디까지 안전한가
이 명제는 다음 모델들에선 매우 자연스럽다.
- OBDD: state 자체가 residual quotient와 거의 일치한다.
- SDD / AOMDD: canonical compression이 있으므로 live family를 정규형으로 모으기 쉽다.

반면 structured d-DNNF 일반형에서는
- state 하나가 local interface 원자 하나에 대응하는지,
- 아니면 여러 state의 묶음이 하나의 cut decomposition을 이루는지
를 먼저 정리해야 한다.

즉, 이 정리는 **rigid/canonical한 모델에서는 거의 정리 수준**,
**structured d-DNNF 일반형에서는 아직 정식화 작업이 필요한 목표 정리**다.

### 목표 정리 B (flux lifting)
각 support `R`에서 새로 태어나는 genuinely new normal forms의 비용을 `birth(R)`라 하자.
그러면 이상적인 최종 형태는

\[
\operatorname{size}(S) \ge \Omega\Big(\sum_{R\in\mathfrak R} birth(R)\Big)
\]

꼴이다.

현재 판단:
- OBDD: 매우 유망, 거의 정확식에 가깝다.
- structured d-DNNF / SDD / AOMDD: 아직 새 연구 단계.

### 다음 실제 작업
다음에는 Goal A를 먼저 OBDD에 대해 완전히 증명 가능한 형태로 쓰고,
그 뒤 structured d-DNNF로 올릴 때 무엇이 깨지는지 적는다.
이 순서가 가장 안전하다.


---

## 13. 교정: SDD용 local 불변량은 "단일 컷 분해비용"이 아니라 universal shell library cost여야 한다

이전 Goal B에서는 `v`-컷의 minimal compressed partition cost를 local invariant로 두려 했다.
하지만 이 양은 **루트 함수 하나**의 `v`-컷 표현비용이지,
실제 SDD가 `v`에서 캐시하는 **shell restriction 전체에 대한 재사용 라이브러리**의 크기와는 어긋난다.

OBDD에서는 prefix 뒤 residual 하나가 곧 state 하나라서
`row quotient = local state mass`가 맞았다.
그러나 SDD에서는 하나의 shell residual이 `v` 아래의 여러 subfunction들의 **서로소 합(disjoint union)** 으로 표현된다.
따라서 SDD에 맞는 local invariant는 다음과 같아야 한다.

### 정의 13.1 (universal shell library cost)
고정된 vtree `T`의 노드 `b`를 잡고

- `B = Vars(b)`
- `A = X \setminus B = Shell(b)`

라 하자.

함수 `f : {0,1}^X -> {0,1}`에 대해,
`b`에서의 **universal shell library**란 `B` 위 Boolean 함수들의 유한 집합 `U`로서,
모든 shell restriction `rho : A -> {0,1}`에 대해 어떤 부분집합 `U_rho \subseteq U`가 존재하여

1. `U_rho`의 함수들은 서로소이고,
2. 그들의 disjunction이 정확히 `f|rho`를 준다.

즉,

\[
 f|\rho = \bigvee_{g\in U_\rho} g,
 \qquad
 g\wedge h \equiv \bot \text{ for } g\neq h \in U_\rho.
\]

이때 비용 `|U|`의 최소값을

\[
\lambda_T(f,b)
\]

라 쓰고, 이를 `b`에서의 universal shell library cost라고 부른다.

### 직관
- OBDD에서는 `U_rho`가 항상 원소 1개인 특수한 경우다.
- SDD에서는 `U_rho`가 여러 원소를 가질 수 있다.
- structured d-DNNF의 minimal deterministic decomposition은 `rho` 하나를 고정했을 때의 local 비용이고,
  `\lambda_T(f,b)`는 **모든 shell restriction을 동시에 커버하는 라이브러리 비용**이다.

즉, exact flux를 위해 필요한 불변량은
"한 컷에서의 최소 분해비용"보다
"해당 support에서 재사용 가능한 원자 라이브러리의 최소 크기"에 더 가깝다.

---

## 14. SDD representation theorem (증명 가능한 버전)

### 정리 14.1 (SDD library representation theorem)
`T`를 vtree라 하고,
`\alpha`를 `T`를 respect하는 compressed and trimmed SDD라고 하자.
`f = \llbracket \alpha \rrbracket`라 하고,
내부 노드 `b`를 하나 고정하자.

`N_\alpha(b)`를 `\alpha` 안에서 `b`를 respect하는 decomposition node의 개수라 하자.
그러면

\[
\lambda_T(f,b) \le N_\alpha(b).
\]

즉, `b`에서 필요한 universal shell library cost는,
실제 SDD가 `b`에 charge한 canonical subfunction 수를 넘을 수 없다.

#### 증명 스케치
`U_b`를 `\alpha` 안의 decomposition node들 중 `b`를 respect하는 것들이 계산하는 Boolean 함수들의 집합으로 둔다.

1. **중복이 없다.**
   Darwiche의 Lemma 9와 Theorem 10에 의해,
   compressed and trimmed SDD는 nontrivial function마다 unique vtree node를 가지며,
   같은 vtree node를 respect하는 두 compressed and trimmed SDD가 동치이면 실제로 같은 SDD다.
   따라서 `|U_b| = N_\alpha(b)`이다.

2. **각 shell restriction 아래 필요한 함수들은 `U_b`의 부분집합으로 나온다.**
   Beame–Liew의 pruning 정리(Proposition 3.3)에 따라,
   shell restriction `rho`를 넣은 pruned SDD `\alpha|rho`는 `f|rho`를 계산하는 pruned SDD가 된다.
   또한 Theorem 3.5의 증명에 따르면,
   Bob의 입력 `phi`에 대해 `f|rho(phi)=1`인 것은
   `Sdds_{\alpha|rho}(b|A)` 안의 어떤 pruned SDD `eta|rho`가 `phi`를 accept하는 것과 동치다.
   따라서 `Sdds_{\alpha|rho}(b|A)`가 계산하는 함수들의 disjunction은 정확히 `f|rho`다.
   또 Proposition 3.4에 의해 이 함수들은 pairwise disjoint다.

3. **pruned 함수는 원래 라이브러리의 함수로 볼 수 있다.**
   shell restriction은 `B = Vars(b)` 바깥 변수들만 고정하므로,
   `Sdds_{\alpha|rho}(b|A)`의 각 pruned SDD는 원래 `\alpha` 안의 어떤 `b`-respecting SDD에 대응한다.
   Theorem 3.5의 증명은 이를 명시적으로 사용한다.
   따라서 각 `rho`에 대해 위 disjoint cover는 `U_b`의 부분집합 `U_rho`로 읽힌다.

이로써 `U_b`가 universal shell library가 되며,
`\lambda_T(f,b) \le |U_b| = N_\alpha(b)`가 된다. ∎

### 해설
이 정리는 우리가 원하던 `local invariant -> charged mass`를
SDD에 대해서는 정말로 확보한다.
다만 그 local invariant는 더 이상
"루트 함수의 한 번짜리 minimal partition cost"가 아니라,
**모든 shell restriction을 동시에 커버하는 canonical atom library의 최소 크기**여야 한다.

---

## 15. 즉시 따름정리: SDD의 global lower bound by summing local library costs

### 따름정리 15.1
위 가정 아래,

\[
\sum_{b\in \mathrm{Int}(T)} \lambda_T(f,b)
\le
\sum_{b\in \mathrm{Int}(T)} N_\alpha(b)
\le |\alpha|.
\]

특히,

\[
|\alpha| \ge \sum_{b\in \mathrm{Int}(T)} \lambda_T(f,b).
\]

### 해설
이건 OBDD의 exact birth formula만큼 정밀하지는 않다.
하지만 SDD에서는 적어도 우리가 원한 형태의

\[
\text{global size} \ge \sum \text{local interface cost}
\]

가 실제 정리로 닫힌다.

즉, SDD에서는 exact flux theorem이 `birth class`가 아니라
`universal shell library`를 통해 성립한다.

---

## 16. 새 그림: local invariant의 두 종류

이제 모델별 차이가 더 선명해진다.

### OBDD형
각 context 뒤 남는 residual 하나가 곧 state 하나다.
따라서 local invariant는 **quotient state count**다.

### SDD형
각 shell residual은 canonical atoms의 서로소 합으로 복원된다.
따라서 local invariant는 **universal shell library cost**다.

### structured d-DNNF형
문헌이 직접 주는 것은
각 shell restriction 또는 각 cut에 대한 **minimal deterministic decomposition cost**다.
하지만 이들이 모든 shell restriction을 동시에 커버하는 canonical library로 조립되는지는 아직 자동이 아니다.

따라서 structured d-DNNF에서 비어 있는 핵심은 정확히 이 질문이다.

> minimal deterministic decomposition costs를
> universal shell library cost로 끌어올릴 수 있는가?

이게 되면 structured d-DNNF에도 SDD형 exact lifting이 가까워지고,
안 되면 structured d-DNNF와 SDD 사이의 진짜 간극이 바로 여기라는 뜻이 된다.
