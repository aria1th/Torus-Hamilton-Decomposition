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

---

## 17. 교정: structured d-DNNF에도 universal shell library는 있다

이전 버전에서는 structured d-DNNF에서 universal shell library 단계가
자동인지가 불분명하다고 적었는데, 이건 지나치게 비관적인 서술이었다.

문헌을 조합하면, **canonicality는 없어도 universal shell library 하한 자체는 얻어진다.**
핵심은 `같은 shell restriction마다 얻는 mutually disjoint family`와
`각 node의 unique decomposition node`를 합치면 충분하다는 점이다.

### 근거
- smooth structured d-DNNF에서는 모든 `∨`-node에도 decomposition node가 자연스럽게 확장된다.
- shell restriction `p`에 대해, `d-DNNF(D_p,v)` 안의 pruned subcircuits가 계산하는 함수들은 mutually disjoint다.
- 그들의 disjunction는 정확히 shell-restricted function `f_{A,p}`다.
- shell restriction은 `vars(v)` 바깥만 고정하므로, decomposition node가 `v`인 subcircuit은 본질적으로 변하지 않는다.

따라서 `v`에 charge된 원래 node들이 계산하는 함수들만 모아도,
모든 shell restriction에 대한 disjoint cover를 동시에 제공하는 universal library가 된다.

### 정의 17.1 (structured d-DNNF universal shell library cost)
`T`를 vtree, `f`를 Boolean function, `v`를 `T`의 node라고 하자.
`B = vars(v)`, `A = X \ B`로 두자.

`\lambda^{sd}_{T}(f,v)`를 다음 최소값으로 둔다.

\[
\lambda^{sd}_{T}(f,v)
=
\min |U|
\]

여기서 `U`는 `B` 위 Boolean function들의 유한 집합이고,
모든 shell restriction `p : A \to \{0,1\}`에 대해 어떤 부분집합 `U_p \subseteq U`가 존재해서

\[
f_{A,p} = \bigvee_{g\in U_p} g,
\qquad
(g\wedge h \equiv \bot \text{ for } g\neq h\in U_p)
\]

를 만족해야 한다.

### 정리 17.2 (structured d-DNNF shell-library theorem)
`D`를 smooth structured d-DNNF respecting `T`라 하고,
`f = \llbracket D \rrbracket`라 하자.
또 `N_D(v)`를 decomposition node가 `v`인 node의 수라 하자.

그러면 모든 vtree node `v`에 대해

\[
\lambda^{sd}_{T}(f,v) \le N_D(v).
\]

### 증명 스케치
`U_D(v)`를 `D` 안에서 decomposition node가 `v`인 node들이 계산하는 함수들의 집합으로 둔다.
그러면 `|U_D(v)| \le N_D(v)`.

이제 shell restriction `p`를 하나 고정하자. Bollig--Farenholtz의 Proposition 2에 따르면
`d-DNNF(D_p,v)`에 있는 pruned subcircuits들이 계산하는 함수들은 mutually disjoint이고,
Proposition 3에 따르면 그들의 disjunction는 정확히 `f_{A,p}`다.
또 shell restriction은 `vars(v)` 바깥만 고정하므로,
이 pruned subcircuits의 roots는 원래 `D` 안에서 decomposition node가 `v`였던 nodes로 볼 수 있다.
따라서 그들이 계산하는 함수들은 `U_D(v)`의 부분집합을 이룬다.

즉 각 `p`마다 어떤 `U_{D,p}(v) \subseteq U_D(v)`가 존재해서

\[
f_{A,p} = \bigvee_{g\in U_{D,p}(v)} g
\]

이며 이 family는 mutually disjoint다.
따라서 `U_D(v)`는 universal shell library이고,

\[
\lambda^{sd}_{T}(f,v) \le |U_D(v)| \le N_D(v).
\]

### 해설
이 정리는 SDD에서 필요했던 canonical compression 없이도 성립한다.
즉, **additive lower bound를 얻는 데 canonicality는 필수는 아니다.**
필요한 것은 더 약한 두 성질이다.

1. 각 node가 unique decomposition node를 가진다.
2. 각 shell restriction마다 그 support에서 얻는 local family가 disjoint cover를 이룬다.

---

## 18. structured d-DNNF에 대한 additive global bound

위 정리의 즉시 따름으로,

\[
\sum_{v\in V(T)} \lambda^{sd}_{T}(f,v)
\le
\sum_{v\in V(T)} N_D(v)
\le |D|.
\]

따라서

\[
|D| \ge \sum_{v\in V(T)} \lambda^{sd}_{T}(f,v).
\]

### 해설
이건 OBDD의 exact birth formula처럼 equality는 아니다.
하지만 우리가 실제로 lower bound에 필요한 형태,

\[
\text{global size} \ge \sum \text{local interface cost}
\]

는 structured d-DNNF에서도 확보된다.

즉, 이전 버전에서 남겨 두었던 핵심 빈칸 중 하나는 이제 메워졌다.
비어 있는 것은 이제 `universal shell library cost` 자체를 explicit family에서 어떻게 크게 보이느냐이다.

---

## 19. 무엇이 필연이고 무엇이 증명 편의였는가

### 필연에 가까운 부분
support-local한 합산형 하한을 얻으려면,
local invariant는 단일 shell의 일회성 decomposition cost가 아니라
**모든 shell restriction을 동시에 처리하는 reusable library cost**여야 한다.
OBDD에서는 residual quotient,
structured d-DNNF와 SDD에서는 universal shell library가 이 역할을 한다.

### 단지 이전 증명에 필요했던 부분
canonicality는 additive inequality 자체에는 필수가 아니다.
그건 equality나 exact charge decomposition을 예쁘게 만들기 위한 강한 충분조건에 가깝다.

### 아직 남은 진짜 문제
- `\lambda^{sd}_{T}(f,v)`를 communication/rectangle/information 관점에서
  어떻게 직접 하한할 것인가?
- `\lambda^{sd}_{T}`와 structured d-DNNF의 기존 local invariant
  (minimal deterministic `X`-decomposition cost) 사이에 일반 비교정리가 있는가?
- canonicality가 없는 탓에 equality가 깨지는 정도를 정량화할 수 있는가?

---

## 17. 교정: structured d-DNNF에도 universal shell library lifting은 성립한다

위 16절의 마지막 문장은 너무 비관적이었다.
Bollig–Buttkus–Lalou–Razaq는 Beame–Liew의 pruned-vtree 기법을
structured d-DNNF로 일반화하며, 고정 shell restriction `p`와 vtree 노드 `v`에 대해
`d-DNNF(D_p,v)` 안의 함수들이 pairwise disjoint이고,
그 disjunction이 정확히 shell-restricted subfunction `f_{A,p}`를 준다고 적는다.
즉, `f_{A,p}`는 항상 `v`에서 관측되는 local pieces의 disjoint union으로 복원된다.

이를 바탕으로 다음 정의를 둔다.

### 정의 17.1 (structured d-DNNF용 universal shell library cost)
`T`를 vtree, `v`를 그 노드, `B = Vars(v)`, `A = shell(v)`라 하자.
Boolean 함수 `f`에 대해

\[
\lambda_T^{\mathrm{st}}(f,v)
=
\min |U|
\]

를 다음 조건을 만족하는 `B` 위 함수 집합 `U`의 최소 크기로 둔다:
각 shell restriction `p` w.r.t. `v`에 대해 어떤 부분집합 `U_p \subseteq U`가 존재하여

\[
f_{A,p} = \bigvee_{g\in U_p} g,
\qquad
g\wedge h \equiv \bot \ \ (g\neq h\in U_p).
\]

즉 `U`는 모든 shell restriction을 동시에 덮는 disjoint local atom library다.

### 정리 17.2 (structured d-DNNF universal shell library theorem)
`D`를 vtree `T`를 respect하는 structured d-DNNF라 하고 `f = \llbracket D\rrbracket`라 하자.
각 노드 `v`에 대해 `N_D(v)`를 decomposition node가 `v`인 circuit node의 수라고 하자.
그러면

\[
\lambda_T^{\mathrm{st}}(f,v) \le N_D(v)
\]

가 성립한다.

#### 증명 스케치
`U_v`를 `D` 안에서 decomposition node가 `v`인 모든 node가 계산하는 함수들의 **distinct** 집합으로 둔다.
그러면 `|U_v| \le N_D(v)`.
이제 임의의 shell restriction `p`를 고정하자.
pruned circuit `D_p`는 `D`의 subgraph이고,
`d\text{-}DNNF(D_p,v)` 안의 각 pruned subcircuit root는 원래 `D` 안의 어떤 `v`-node다.
따라서 그들이 계산하는 함수들은 모두 `U_v`에 속한다.
한편 Proposition 2와 3에 의해 이 함수들은 pairwise disjoint이고,
그 disjunction은 정확히 `f_{A,p}`다.
그러므로 `U_v`의 부분집합 하나가 `f_{A,p}`를 disjoint union으로 표현한다.
`p`는 임의였으므로 `U_v`는 universal shell library이고,
따라서

\[
\lambda_T^{\mathrm{st}}(f,v) \le |U_v| \le N_D(v).
\]
∎

### 따름정리 17.3 (structured d-DNNF의 global lower bound)
모든 structured d-DNNF `D`에 대해

\[
|D| \ge \sum_{v\in \mathrm{Int}(T)} \lambda_T^{\mathrm{st}}(f,v).
\]

#### 증명
정리 17.2를 각 `v`에 대해 더하면

\[
\sum_v \lambda_T^{\mathrm{st}}(f,v) \le \sum_v N_D(v).
\]

각 node는 하나의 decomposition node만 가지므로 `\sum_v N_D(v) \le |D|`. ∎

### 해설
이 정리는 꽤 중요하다.
우리가 SDD에서만 가능하다고 보았던

\[
\text{global size} \ge \sum \text{local library cost}
\]

형태는 사실 structured d-DNNF에서도 성립한다.
따라서 structured d-DNNF와 SDD의 차이는
**shell-library lifting의 유무**가 아니라,
그 라이브러리가 정준적으로 압축되는지,
그리고 Boolean 연산/negation/exists 아래 얼마나 잘 보존되는지 쪽으로 옮겨간다.

---

## 18. 새 구도: 어디까지가 필연이고 어디서 갈리는가

이제 모델들의 관계를 이렇게 다시 적는 편이 맞다.

### OBDD
- local atom = residual row 하나
- canonicality = 매우 강함
- global formula = birth/flux의 exact count

### structured d-DNNF
- local atom = shell restriction마다 등장하는 disjoint local piece
- canonicality = 약하거나 없음
- 그래도 universal shell library cost는 global size에 합산형 lower bound를 준다
- 다만 exact flux / Möbius형 복원은 아직 보이지 않는다

### SDD
- structured d-DNNF의 shell-library 그림 위에
  compressed partition의 canonicality가 추가된다
- 그래서 같은 support에서 같은 local meaning이면 같은 object로 collapse된다
- 이는 stronger exactness와 stronger algorithmic closure의 근원이다

### 현재 남은 진짜 질문
structured d-DNNF와 SDD를 가르는 핵심은

> local library가 존재하느냐

가 아니라

> local library가 canonical compressed partition으로 강제되느냐,
> 그리고 그 정준성이 negation / disjunction / existential quantification 같은 연산과 어떻게 맞물리느냐

쪽이다.

이는 2024년 결과에서 structured d-DNNF가 negation, disjunction, existential quantification에 대해
닫혀 있지 않다는 사실과도 잘 맞는다.

---

## 16. structured d-DNNF: 지금 증명되는 최선과, 정확히 멈추는 줄

이번 단계의 핵심은 다음 구분이다.

- SDD에서는 shell restriction 뒤에 `b`에서 보이는 local atoms를 **원래부터 `b`를 respect하던 canonical subobjects**로 읽을 수 있었다.
- structured d-DNNF에서는 이 줄이 자동으로 성립하지 않는다.

그 이유는 Definition 12의 `R(D_p,v)`가

> "원래 D에서 decomposition node가 `v`였던 노드"

가 아니라,

> "**pruned vtree** `T_A`에서 decomposition node가 `v`가 된 노드"

를 고르기 때문이다.

즉, 어떤 원래 노드가 더 큰 support에 있었더라도, shell 변수들이 고정된 뒤에 support가 줄어 `v`로 **붕괴(collapse)** 할 수 있다.
이 현상이 OBDD/SDD 식 exact lifting을 바로 막는다.

### 정의 16.1 (shell-active node set)
`D`를 vtree `T`를 respect하는 structured d-DNNF라 하자.
노드 `v \in T`와 `A = shell(v)`를 고정한다.

원래 회로 `D`의 노드 `u`가 `v`에 대해 **shell-active** 라는 것은,
어떤 shell restriction `p` w.r.t. `v`가 존재하여,
pruned circuit `D_p`에서 `u`가 `R^+(D_p,v)`에 속하는 것을 말한다.

이들의 집합을

\[
\mathcal U_D(v)
:=
\{u\in V(D): \exists p \text{ shell restriction w.r.t. } v \text{ s.t. } u\in R^+(D_p,v)\}
\]

로 두고,

\[
\sigma_D(v):=|\mathcal U_D(v)|
\]

를 `v`에서의 **shell-active mass**라고 부른다.

### 정의 16.2 (shellwise local decomposition cost)
`f`를 `D`가 계산하는 함수라 하자.
`p`가 `v`에 대한 shell restriction이면, `f_{A,p}`를 그 restriction 아래의 subfunction이라 한다.

그리고

\[
\mu_T(f,v,p)
:=
\text{minimal deterministic }\mathrm{vars}(v)\text{-decomposition size of } f_{A,p}
\]

로 두고,

\[
\mu_T^{\max}(f,v):=\max_p \mu_T(f,v,p)
\]

를 정의한다. 여기서 최대는 `v`에 대한 모든 shell restriction `p`에 대해 취한다.

이 양은 "각 shell context를 따로 봤을 때 필요한 local 컷 비용"의 최댓값이다.

### 정리 16.3 (structured d-DNNF shell-active lower bound)
`D`가 vtree `T`를 respect하는 structured d-DNNF이고 `f=\llbracket D\rrbracket`라 하자.
그러면 모든 vtree 노드 `v`에 대해

\[
\sigma_D(v) \ge \mu_T^{\max}(f,v).
\]

#### 증명
shell restriction `p`를 하나 고정하자.
Bollig et al.의 Proposition 2와 Proposition 3에 의해,
`d`-DNNF`(D_p,v)`에 들어 있는 pruned structured d-DNNF들이 계산하는 함수들은 서로소이고,
그 disjunction은 정확히 `f_{A,p}`이다.
따라서 이들의 루트 집합 `R^+(D_p,v)`는 `f_{A,p}`의 deterministic `vars(v)`-decomposition 하나를 유도한다.
그러므로

\[
|R^+(D_p,v)| \ge \mu_T(f,v,p).
\]

그런데 `R^+(D_p,v) \subseteq \mathcal U_D(v)`이므로

\[
\sigma_D(v)=|\mathcal U_D(v)| \ge |R^+(D_p,v)| \ge \mu_T(f,v,p).
\]

이 부등식이 모든 shell restriction `p`에 대해 성립하므로,
최댓값을 취하면

\[
\sigma_D(v) \ge \mu_T^{\max}(f,v).
\]

∎

### 해설
이 정리는 canonicity 없이도 성립한다.
즉 structured d-DNNF에 대해서도

> local deterministic decomposition 비용
> \(\Rightarrow\)
> 그 support에서 어떤 식으로든 드러나야 하는 활성 node 질량

이라는 연결고리는 살아 있다.

하지만 이 질량은 `N_D(v)`—즉 "원래부터 `v`를 decomposition node로 갖는 노드 수"—와는 다르다.
`
\sigma_D(v)`는 **context에 따라 `v`로 붕괴해 나타날 수 있는 노드들의 전체 합집합**이기 때문이다.

### 정의 16.4 (shell-stability)
structured d-DNNF `D`가 노드 `v`에서 shell-stable 하다는 것은

\[
\mathcal U_D(v) \subseteq V_v(D)
\]

가 성립하는 것이다. 여기서 `V_v(D)`는 원래 decomposition node가 `v`인 노드들의 집합이다.

더 강하게,

\[
\mathcal U_D(v)=V_v(D)
\]

이면 strong shell-stable이라 하자.

### 따름 16.5 (conditional library theorem)
만약 `D`가 모든 `v`에서 shell-stable 하다면,

\[
N_D(v) \ge \mu_T^{\max}(f,v)
\]

가 모든 `v`에 대해 성립한다.

만약 여기에 support-typed canonicity까지 더해져,
같은 `v`에서 같은 Boolean function을 계산하는 노드가 유일하다면,
`v`에서의 universal shell library cost를 node 수로 직접 하계하는 SDD형 정리로 더 밀 수 있다.

### 지금 정확히 어디서 멈추는가
따라서 structured d-DNNF에서 OBDD/SDD식 전역합 정리가 안 나오는 이유는 둘로 분해된다.

1. **shell-instability**: pruning 뒤 `v`에서 보이는 원자가 원래부터 `v`에 있던 것이 아닐 수 있다.
2. **non-canonicity**: 같은 support `v`에서 같은 함수를 계산해도 노드가 하나로 압축되지 않을 수 있다.

이 둘 중 첫 번째가 더 근본적이다.
canonicity가 없어도 정리 16.3은 살아 있지만,
shell-stability가 없으면 local cost를 `v`-charged node 수로 읽을 방법이 없다.

### 의미
이제 남은 핵심 질문은 아주 정확하다.

> structured d-DNNF의 어떤 자연스러운 부분클래스에서 shell-stability가 성립하는가?

- 성립한다면, 그 부분클래스에 대해서는 SDD형 exact/near-exact lifting으로 갈 수 있다.
- 성립하지 않는 명시적 예가 나오면, structured d-DNNF와 SDD 사이의 진짜 간극은 바로 "context-collapse"에 있다는 뜻이 된다.

현재까지의 판단으로는,
OBDD는 체인형 support 때문에 shell-stability가 사실상 자명하고,
SDD는 canonical partition 구조 때문에 shell-stability + canonicity가 함께 성립하는 쪽으로 보인다.
반면 general structured d-DNNF는 Definition 12 자체가 context-collapse를 허용하므로,
추가 제약 없이 shell-stability를 기대하기는 어렵다.

## 17. complement-assisted lifting: structured d-DNNF에서 지금 당장 얻을 수 있는 우회 정리

직접 exact lifting은 막혀 있지만, `f`와 `\neg f`를 **같은 normalized vtree**에 대한 structured d-DNNF로 함께 잡을 수 있다면,
SDD로 우회하는 실제 정리를 얻을 수 있다.

핵심 입력은 Bollig–Buttkus의 변환 정리다.
그들은 `f`와 `\neg f`가 같은 normalized vtree `T`에 대한 structured d-DNNF `D, \overline D`를 가지면,
auxiliary variables를 넣어 수정한 vtree `T'` 위에서 `f`를 계산하는 SDD `S`를

\[
|S| = O\big((|D|+|\overline D|)^2\big)
\]

크기로 만들 수 있음을 보였다.

우리는 이미 SDD에 대해,
각 internal vtree node `b`에서의 universal shell library cost `\lambda_{T'}(f,b)`가
해당 노드에서의 canonical decomposition node 수를 하계하고,
따라서

\[
\sum_{b\in \mathrm{Int}(T')} \lambda_{T'}(f,b) \le |S|
\]

를 얻었다.

이 둘을 합치면 바로 다음이 나온다.

### 정리 17.1 (complement-assisted shell lifting)
`T`를 normalized vtree라 하고,
`D, \overline D`를 각각 `f`와 `\neg f`를 계산하는 structured d-DNNF라 하자.
둘 다 `T`를 respect한다고 하자.

그러면 auxiliary variables를 포함한 어떤 modified vtree `T'`가 존재하여,

\[
|D|+|\overline D|
\ge
\Omega\!\left(
\sqrt{\sum_{b\in \mathrm{Int}(T')} \lambda_{T'}(f,b)}
\right).
\]

#### 증명
Bollig–Buttkus의 정리에 의해,
`f`를 계산하는 SDD `S`가 modified vtree `T'` 위에 존재하고

\[
|S| = O\big((|D|+|\overline D|)^2\big)
\]

이다.

한편 SDD에 대한 앞 절의 정리로부터

\[
\sum_{b\in \mathrm{Int}(T')} \lambda_{T'}(f,b)
\le |S|.
\]

따라서

\[
\sum_{b\in \mathrm{Int}(T')} \lambda_{T'}(f,b)
= O\big((|D|+|\overline D|)^2\big).
\]

양변에 제곱근을 취하면 원하는 식이 나온다. ∎

### 해설
이 정리는 약하지만 실제로 쓸 수 있다.
핵심은 다음과 같다.

- structured d-DNNF 단일 회로 `D`로부터는 아직 `\sum_v \lambda_T(f,v) \lesssim |D|`를 못 얻는다.
- 하지만 **보수 회로 `\overline D`까지 함께 있으면**, partition을 완성하는 데 필요한 complement 쪽 원자들이 공급되어
  SDD로의 우회 변환이 가능해진다.
- 그 결과 선형 하한은 아니더라도 **제곱근형 하한**은 얻어진다.

즉, 현재 수준에서 structured d-DNNF에 대해 확보된 것은

\[
\text{single-circuit exact lifting}
\quad\text{가 아니라}\quad
\text{dual-circuit indirect lifting}
\]

이다.

### 왜 이게 중요하나
이 정리는 우리가 찾는 "무엇이 필연이고, 무엇이 현재 증명법에 필요하냐"를 아주 선명하게 갈라준다.

- **필연적 뼈대**: shell restriction 아래 local partition이 생긴다.
- **현재 증명법에 필요한 강화**: 그 partition이 `p`와 무관한 하나의 라이브러리로 모여야 한다.
- **우회 수단**: `\neg f` 회로를 함께 넣어 SDD의 partition property를 강제로 복구한다.

즉, `\neg f` 회로는 단순한 편의가 아니라,
structured d-DNNF에서 빠져 있는 **global partition completion device** 역할을 한다.

## 18. 이제 남은 핵심 명제는 한 줄로 줄어든다

structured d-DNNF 쪽에서 직접 exact/near-exact lifting을 얻고 싶다면,
실제로 필요한 건 다음 명제 하나다.

### 추측 18.1 (uniform shell library conjecture)
모든 structured d-DNNF `D`와 모든 vtree node `v`에 대해,
어떤 함수 집합 `L_D(v)`가 존재해서

1. `|L_D(v)| \le \mathrm{poly}(N_D(v))`,
2. 모든 shell restriction `p` w.r.t. `v`에 대해,
   `f_{A,p}`는 `L_D(v)`의 부분집합에 의한 mutually-disjoint disjunction으로 표현된다.

만약 이 추측이 참이면,

\[
\lambda_T(f,v) \le |L_D(v)| \le \mathrm{poly}(N_D(v))
\]

가 되고,
모든 `v`에 대해 합하면 structured d-DNNF용 near-exact lifting이 얻어진다.

### 왜 이 추측이 정확한가
정리 16.3은 각 `p`마다 필요한 원자 수가 shell-active mass로 드러난다는 걸 보였다.
즉 **per-shell partition**은 이미 있다.
문제는 이 partition들이 `p`마다 제각각 다른 곳에서 튀어나올 수 있다는 점이다.

따라서 남은 핵심은 더 이상 "분해가 가능한가"가 아니라,

> 여러 shell context에서 등장하는 local 원자들을
> 하나의 `p`-독립적 라이브러리로 압축할 수 있는가?

이다.

OBDD에서는 답이 예다.
SDD에서도 답이 예다.
structured d-DNNF 일반형에서는 바로 이 지점이 아직 비어 있다.

## 19. 현재 시점의 매우 압축된 결론

1. **OBDD**: exact flux theorem까지 닫힌다.
2. **SDD**: universal shell library cost를 통해 additive lower bound가 닫힌다.
3. **structured d-DNNF**: per-shell local partition은 증명되지만,
   그것을 single library로 모으는 uniform shell library 단계가 비어 있다.
4. **하지만** `f`와 `\neg f`의 structured d-DNNF가 함께 있으면,
   SDD 우회로를 통해 제곱근형의 indirect lifting은 증명된다.

따라서 지금의 가장 정직한 요약은:

> structured d-DNNF에서 막힌 곳은 determinism 자체가 아니라,
> **context마다 생기는 local atoms의 global library화**다.

이다.
