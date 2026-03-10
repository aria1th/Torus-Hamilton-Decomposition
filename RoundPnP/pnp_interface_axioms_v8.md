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

## 17. 수렴 가설 vs 맴돎 가설

### 질문
`weak shell-stability + support-typed canonicity`를 요구하는 순간,
언어가 사실상 SDD류 rigidity로 빠르게 수렴하는가?
아니면 그 사이에서 오래 맴도는 중간 계열들이 존재하는가?

### 현재 판단
둘 다 있다. 다만 **가정의 강도에 따라 두 단계로 갈린다.**

#### (A) 약한 안정성만 요구하면: 맴돎 가능성이 크다
- 일반 structured d-DNNF는 이미 SDD보다 더 succinct할 수 있다.
- AOMDD는 pseudo tree 아래 canonical하다.
- OBDD를 conjunctive decomposition으로 확장한 canonical family들도 존재한다.

즉, canonicity 그 자체나 decomposition 그 자체만으로는 SDD로 수렴하지 않는다.
이 경우에는 support discipline이 여러 방식으로 실현될 수 있어서
중간 계열이 꽤 두껍게 존재할 가능성이 높다.

#### (B) 안정성 + 정준성 + partition rigidity까지 요구하면: 빠른 수렴이 더 그럴듯하다
특히 다음이 함께 요구되면 SDD류로의 수렴이 강하게 의심된다.

1. shell restriction 후 새로 보이는 local atom이 원래 support를 바꾸지 않는다.
2. 같은 support에서 같은 의미는 반드시 merge된다.
3. local interface가 context마다 새로 만들어지는 것이 아니라, 하나의 canonical library / partition family로 재사용된다.
4. 공통 support/vtree 아래 Boolean combination이 잘 동작한다.

이 네 줄은 거의 SDD가 가진 핵심 패턴과 겹친다.
따라서 이 정도까지 요구하면, 문법은 달라도
lower-bound 메커니즘과 canonical interface calculus는 사실상 SDD형으로 수렴할 가능성이 높다.

### 작업 가설
- **Orbiting zone**: canonicity는 있으나 support rigidity 또는 partition rigidity가 약한 언어들.
- **Convergence zone**: shell-stability + support-typed canonicity + canonical partition library를 모두 갖는 언어들.

### 다음 목표
이 작업 가설을 정리 형태로 적는다:

> 충분히 강한 support-rigidity와 canonicity를 만족하는 structured subclass는
> SDD형 exact lifting을 허용한다.

그리고 반대로,

> 이들 중 하나라도 빠지면 structured d-DNNF류의 collapse counterexample 또는
> non-liftable orbiting behavior가 생긴다.

이 두 정리를 맞대어 두는 것이 다음 단계다.

---

## 16. rigidity에 대한 현재 판단: 빠른 수렴인가, 중간지대인가

현재까지의 그림을 가장 압축하면 다음 네 층으로 나눌 수 있다.

### L0. 일반 structured d-DNNF
- context-collapse가 실제로 일어난다.
- 따라서 fixed-support node count로 local cut cost를 바로 읽는 naive lifting은 거짓이다.

### L1. weak shell-stability만 가정한 층
- 어떤 shell restriction에서도 `v`-원자로 보이는 노드는 원래부터 `v`-support여야 한다.
- 이 층에서는 shell-active mass와 fixed-support mass가 일치하므로,
  `N_D(v) >= mu_T^{max}(f,v)` 같은 첫 번째 lifting이 복구된다.
- 하지만 아직 같은 support에서 같은 함수를 계산하는 노드가 자동으로 merge된다는 보장은 없다.

### L2. shell-stability + support-typed canonicity
- 같은 support `v`에서 같은 함수를 계산하는 두 노드는 하나로 합쳐진다.
- 이 층에 오면 fixed-support node 집합이 사실상 canonical shell library처럼 행동한다.
- 따라서 local invariant를 support별 birth mass로 내리는 표현정리가 자연스럽게 성립할 가능성이 크다.

### L3. compressed partition canonicity / strong canonical decomposition
- SDD류에서 나타나는 층이다.
- 고정된 vtree node에 대해 compressed partition이 유일하며,
  전체 구조가 canonical decomposition object로 읽힌다.
- right-linear vtree에서는 OBDD를 회수한다.

### 현재 추측
- **L0 -> L1**: 자연스러운 부분클래스가 있을 가능성을 아직 배제할 수 없다.
  즉, collapse만 금지한다고 해서 곧바로 SDD가 되는 것은 아닐 수 있다.
- **L1 -> L2**: 여기에도 중간지대가 있을 수 있다. shell-stability는 support rigidity이지만,
  canonicity는 merge rigidity이기 때문이다. 전자는 local support의 안정성이고,
  후자는 같은 support 내부에서의 global quotienting이다.
- **L2 -> L3**: 이 구간은 상대적으로 짧을 가능성이 크다. 이유는 local library를 global node count로
  정확히 읽으려면, support-typed canonicity만으로도 이미 상당한 정규성이 생기고,
  실제로 알려진 canonical 계열(OBDD, SDD, AOMDD, 그리고 SDD류의 canonical 변형들)은
  모두 이 근방에 모여 있기 때문이다.

요약하면:
- **고전적 SDD 그 자체로 필연 수렴한다**고 보지는 않는다.
- 그러나 **exact additive lifting을 가능하게 하는 regime**은 꽤 빠르게
  `SDD/AOMDD/SDD-variant` 류의 support-rigid canonical 체제로 수렴할 가능성이 높다.
- 따라서 “수렴하지 않고 오래 맴도는” 현상이 있다면, 그것은 대개 L1~L2 사이,
  즉 shell-stability는 있으나 full canonical compression은 아직 없는 중간지대일 가능성이 크다.

### 이 판단을 뒷받침하는 정성적 근거
- OBDD는 고정 순서에서 canonical하다.
- SDD는 compressed/trimmed 형태에서 고정 vtree에 대해 canonical하다.
- AOMDD는 고정 pseudo tree에 대해 canonical하다.
- VS-SDD 같은 SDD 변형도 canonical하면서 SDD보다 더 succinct할 수 있다.

따라서 “rigidity basin”은 꽤 넓어 보인다. 다만 그 basin의 중심이 꼭 고전적 SDD 한 점일 필요는 없다.
오히려 `support-rigid + canonical library`라는 추상 체제가 중심이고,
SDD는 그 대표적인 실현이라고 보는 편이 더 정확하다.

---

## X. "SDD류 rigidity로 빠르게 수렴하는가?"에 대한 현재 판단

핵심은 `structured d-DNNF -> SDD`를 한 번에 묻기보다,
다음 두 축을 분리하는 것이다.

1. **support rigidity**
   - shell restriction 뒤에 보이는 local atom이 원래부터 그 support에 속했는가?
   - 즉 weak shell-stability 류 조건.

2. **semantic uniqueness / canonical compression**
   - 같은 support에서 같은 의미를 계산하면 반드시 같은 정규형으로 합쳐지는가?

현재 판단은 다음과 같다.

### X.1. 약한 조건만으로는 빠른 수렴이 필연적이지 않다

일반 structured d-DNNF는 fixed vtree에 대해서도 SDD보다 지수적으로 더 succinct할 수 있다.
따라서 support 관련 조건을 조금 강화한다고 해서 곧바로 SDD와 같은 크기/형태로 수렴한다고 보기는 어렵다.

또한 SDD의 주변에는 canonical하면서도 표준 SDD와는 다른 변형들이 이미 존재한다.
예를 들어 ZSDD와 VS-SDD는 canonical form을 유지하면서도 표준 SDD와는 다른 trimming / equivalence를 사용한다.
이는 "rigidity"가 하나의 유일한 syntax로만 귀결되지는 않을 수 있음을 시사한다.

따라서 weak shell-stability만으로는

\[
\text{support collapse 금지} \;
\centernot\Rightarrow\; \text{곧바로 SDD}
\]

라고 보는 편이 안전하다.

### X.2. 그러나 조건을 조금만 더 얹으면 SDD-유사 영역으로는 빨리 밀려간다

다음 셋을 동시에 요구하면 상황이 달라진다.

1. weak shell-stability (context에 따라 support가 무너지지 않음)
2. support-typed canonicity (같은 support + 같은 의미는 반드시 merge)
3. 같은 vtree 위에서의 dual closure 성향 (특히 negation / complement를 함께 다룰 수 있음)

이 조합은 SDD류와 아주 가까워진다.
실제로 SDD는 fixed vtree에서 compressed form이 canonical이고,
구조화된 d-DNNF와 달리 Boolean 연산 쪽의 다루기 쉬운 성질을 많이 회복한다.
또한 Bollig--Farenholtz의 결과는,
`f`와 `¬f`가 같은 vtree를 respect하는 polynomial-size structured d-DNNF를 가지면,
`f`는 auxiliary variables를 넣은 vtree에 대해 polynomial-size SDD를 가진다는 방향을 준다.

이건 엄밀한 동치 정리는 아니지만,
"support rigidity + same-vtree duality"를 요구하면
structured d-DNNF의 자유도가 빠르게 줄어든다는 강한 증거다.

### X.3. 그래서 현재 베팅

- **literal한 의미의 "표준 SDD로 필연 수렴"**: 아직 아니다.
  중간 지대가 남을 가능성이 크다.

- **의미론적 의미의 "SDD-유사 rigidity 영역으로 수렴"**: 가능성이 높다.
  특히 canonicity와 complement 쪽 조건까지 얹으면 빠르게 그쪽으로 밀릴 것 같다.

즉 내 현재 예상은

\[
\text{bare structured d-DNNF} 
\;
\supsetneq
\;
\text{(hovering intermediates)}
\;
\supsetneq
\;
\text{SDD-like rigid zone}
\]

이며,
weak shell-stability 하나만으로는 오른쪽 끝까지 가지 않지만,
canonicity와 dual closure가 더해지면 오른쪽으로 급격히 좁아질 가능성이 높다.

### X.4. 다음 단계의 정확한 질문

따라서 앞으로의 질문은

1. **weak shell-stability만 만족하지만 SDD는 아닌 자연스러운 부분클래스가 실제로 있는가?**
2. **weak shell-stability + support-typed canonicity + same-vtree complement closure**가
   정말로 SDD-류 representation theorem으로 이어지는가?

로 정리된다.

이 둘 중 1번이 나오면 "맴도는 중간지대"가 실재한다는 뜻이고,
2번이 증명되면 "어느 선을 넘으면 급격히 수렴한다"는 문턱 현상이 드러난다.

### X.5. 현재 판단의 더 날카로운 버전

내 현재 판단은 두 갈래다.

- **support rigidity만 요구하면**: 중간지대가 남을 가능성이 크다.
  이유는 weak shell-stability가 collapse를 막아도,
  같은 support에서 같은 의미를 계산하는 subcircuit들의 전역 병합을 강제하지는 않기 때문이다.
  즉 exact lifting의 첫 문턱은 넘지만, canonical library까지는 아직 멀 수 있다.

- **support rigidity + support-typed canonicity + dual/complement 쪽 안정성까지 요구하면**:
  SDD-유사 영역으로 빠르게 수렴할 가능성이 높다.
  실제로 SDD는 compressed/trimmed 조건 아래 fixed vtree에서 canonical하고,
  structured d-DNNF 쪽에서는 함수와 그 보수가 같은 vtree에서 작은 structured d-DNNF를 가지면
  auxiliary variables를 둔 modified vtree에서 polynomial-size SDD로 옮길 수 있다는 정리가 있다.
  따라서 dual-side 요구는 structured d-DNNF의 자유도를 매우 강하게 줄인다.

즉,

\[
\text{shell-stability alone} \not\Rightarrow \text{fast collapse to SDD},
\]

반면 직감상

\[
\text{shell-stability + canonicity + dual robustness}
\Longrightarrow
\text{rapid convergence to an SDD-like zone}.
\]

여기서 "SDD-like"는 literal한 문법적 동일성을 뜻하기보다,
- support가 고정되고,
- local partition library가 canonical해지며,
- complement/Boolean operation 쪽에서 크게 새 비용이 생기지 않는
영역을 뜻한다.

## 15. `사실상 SDD류로 수렴` 가설에 대한 현재 판단

### 15.1. 핵심 구분

`빠르게 수렴하느냐`는 질문은 무엇을 이미 가정했는지에 따라 전혀 다르게 보인다.

- **약한 가정만**: weak shell-stability 정도만 넣은 클래스.
- **강한 가정**: weak shell-stability + support-typed canonicity + (동일 support / 동일 vtree에서의) negation 또는 유사 closure.

내 현재 판단은:

- 약한 가정만으로는 **수렴하지 않고 맴도는 중간지대**가 남을 가능성이 크다.
- 강한 가정까지 넣으면 **꽤 빠르게 SDD/AOMDD류의 rigid canonical family로 끌려갈 가능성**이 높다.

### 15.2. 왜 약한 가정만으로는 맴돌 가능성이 큰가

weak shell-stability는 단지

- context에 따라 더 큰 support의 노드가 더 작은 support로 collapse되는 현상

을 금지할 뿐이다.

하지만 이것만으로는 다음이 전혀 통제되지 않는다.

1. 같은 support에서 같은 함수를 계산하는 두 노드가 merge되는가?
2. local decomposition이 unique / compressed한가?
3. negation, disjunction, forgetting을 같은 support 체계 안에서 처리할 수 있는가?

즉 weak shell-stability는 **support typing**만 제어하고,
**canonical compression**과 **Boolean closure**는 거의 건드리지 않는다.
그래서 이 수준에서는 structured d-DNNF와 SDD 사이에 실제 intermediate classes가 꽤 남을 여지가 있다.

### 15.3. 왜 `일반 structured d-DNNF -> SDD`의 즉시 수렴은 틀렸다고 보는가

문헌상 structured d-DNNF는 SDD를 포함하지만 더 일반적이며, 2024년에는 실제로 structured d-DNNF가 SDD보다 더 succinct할 수 있다는 정량적 분리가 증명되었다. 구체적으로 size `s`의 structured d-DNNF를 갖지만 어떤 SDD로도 `s^{\tilde\Omega(\log s)}`보다 작게 표현할 수 없는 함수들이 존재한다. 같은 논문은 structured d-DNNF가 negation, disjunction, existential quantification에 대해 닫혀 있지 않음을 보인다. 따라서 **structured d-DNNF 전체는 SDD 쪽으로 자동 수렴하지 않는다**. [Vinall-Smeeth et al. 2024]

### 15.4. 그런데 왜 `강한 가정`을 넣으면 빨라질 것 같나

반대로, 2021년 결과는 함수 `f`와 `¬f`가 **같은 vtree를 respect하는** polynomial-size structured d-DNNF를 둘 다 가지면, `f`는 auxiliary variables를 추가한 vtree 아래 polynomial-size SDD를 갖는다고 보여준다. 즉, same-vtree negation compatibility까지 주어지면 structured d-DNNF와 SDD 사이의 간극이 급격히 줄어든다.

이 결과는 중요한 힌트를 준다.

- support가 안정적이고,
- 같은 support에서 의미가 canonical하게 압축되며,
- complement 쪽과도 같은 support 체계에서 잘 맞물리면,

그때는 local interface가 사실상 sentential partition 쪽으로 정렬되기 쉽다.

즉 **exact lifting을 가능하게 하는 강한 공리 묶음은 SDD류 rigidity를 거의 강제할 가능성**이 있다.

다만 여기서도 결과는 `같은 vtree에서 문자 그대로 SDD가 된다`가 아니라,
`vtree 수정 + auxiliary variables`를 허용한 뒤 polynomial simulation이 가능하다는 형태다.
따라서 `빠르게 수렴`은 맞더라도, 그 수렴은 `정확히 SDD 그 자체`가 아니라
`SDD-equivalent canonical zone`으로의 수렴일 가능성이 더 크다.

### 15.5. SDD만이 유일한 attractor인가

내 생각엔 **그렇지는 않다**.

AOMDD는 pseudo tree가 주어지면 canonical/minimal representation을 가지며,
주어진 partition 위 decomposition의 유일성까지 갖는다.
따라서 `rigidity의 종착점`은 하나가 아니라 적어도

- vtree 기반의 SDD류
- pseudo-tree 기반의 AOMDD류

처럼 둘 이상일 가능성이 높다.

즉 `structured d-DNNF -> SDD`로의 일직선 수렴보다,
`support discipline이 강해질수록 몇 개의 rigid canonical attractor 중 하나로 끌려간다`
는 그림이 더 자연스럽다.

### 15.6. 현재 베팅

내 현재 베팅은 다음과 같다.

1. **weak shell-stability만으로는** 중간지대가 꽤 넓게 남는다. 즉 `맴돈다` 쪽.
2. **weak shell-stability + support-typed canonicity**까지 넣으면, exact lifting 쪽으로 갈 가능성이 급격히 커진다.
3. 여기에 **same-support negation compatibility** 또는 그에 준하는 closure까지 넣으면, SDD/AOMDD류 rigid family로 **상당히 빠르게 수렴**할 가능성이 크다.
4. 하지만 그 종착점은 꼭 `문자 그대로 SDD` 하나일 필요는 없다. `support discipline에 맞는 canonical family`일 가능성이 높다.

### 15.7. 연구 프로그램으로 바꾸면

그래서 가장 건강한 다음 추측은 다음 두 개다.

- **Conjecture W (wandering zone):** weak shell-stability만 만족하지만 support-typed canonicity는 없는 natural structured d-DNNF subclasses가 존재하며, 이들은 SDD보다 실질적으로 더 넓다.
- **Conjecture C (canonical convergence):** weak shell-stability + support-typed canonicity + same-support complement stability를 만족하는 모든 natural support-faithful classes는 polynomially simulated by an SDD/AOMDD-type canonical representation.

이 둘 중 어느 쪽이 먼저 깨지느냐가, `빠르게 수렴` 대 `중간지대 지속`을 가르는 핵심이다.

### 연구 추측: Rigidity Threshold Conjecture

고정된 support 시스템 위의 exact compilation 언어/solver 클래스 `C`가 다음을 모두 만족한다고 하자.
1. shell restriction에 대해 닫혀 있다.
2. weak shell-stability를 만족한다.
3. support-typed canonicity를 만족한다.
4. fixed-support charge에 의한 additive lifting이 성립한다.

그러면 `C`는 적어도 의미론적으로는 `support-rigid canonical library language`로 환원되며,
고전적 SDD일 필요는 없더라도 SDD/AOMDD/SDD-variant 류의 rigidity basin 안에 들어간다고 추측한다.

반대로 2가 빠지면 naive fixed-support lifting은 일반적으로 거짓이고,
3이 빠지면 local library cost를 fixed-support node count로 정확히 읽기 어렵고,
4가 빠지면 전역 하한을 깔끔한 support별 합으로 정리할 수 없다.

현재 판단:
- `L1 -> L2` 사이에는 중간지대가 있을 가능성이 있다.
- 그러나 `L2 + additive lifting`까지 요구하면, 고전적 SDD 자체는 아니더라도
  support-rigid canonical 체제로 꽤 빠르게 수렴할 가능성이 높다.

---

## 18. Conjecture W / Conjecture C: 맴돎 구간과 수렴 구간

이제 질문은 다음처럼 잘린다.

- 어떤 약한 조건까지는 structured d-DNNF류가 SDD류의 정준 강성(rigidity)으로 **수렴하지 않고 맴도는가**?
- 어떤 강한 조건부터는 사실상 **정준 인터페이스 라이브러리**가 강제되어, SDD/AOMDD형 exact lifting으로 빠르게 끌려가는가?

이를 위해 두 가설을 명시한다.

### 정의 18.1 (weakly stable support discipline)
고정된 support 체계 `(\mathfrak R, \preceq)`를 respect하는 exact solver/representation class `\mathcal K`가
**weakly stable**하다는 것은, 각 `R \in \mathfrak R`와 admissible context `\rho \in \mathrm{Ctx}(R)`에 대해,
`R`-원자로 관측되는 local object가 원래 larger support에서 붕괴해 내려온 것이 아니라
이미 `R`-typed object로 읽힐 수 있다는 것을 뜻한다.

즉, shell-active mass와 fixed-support mass를 구분하는 붕괴 현상이 금지된다.

### 정의 18.2 (support-typed canonicity)
`\mathcal K`가 **support-typed canonical**하다는 것은,
같은 support `R`에서 같은 Boolean meaning을 계산하는 두 객체가 항상 같은 정규형으로 합쳐진다는 뜻이다.

이는
- OBDD의 fixed-order canonical quotient,
- compressed/trimmed SDD의 fixed-vtree canonicity,
- AOMDD의 fixed pseudo-tree canonicity
와 같은 성질의 추상화다.

### 정의 18.3 (canonical library property)
`\mathcal K`가 **canonical library property**를 가진다는 것은,
각 support `R`에 대해 모든 admissible context들이 만들어내는 local behaviors가
하나의 유한한 canonical atom library `\mathcal L_R`의 부분집합들의 disjoint union으로 표현될 수 있고,
그 library 크기가 support `R`에서의 local interface cost와 동치(또는 상수배 동치)라는 뜻이다.

즉 local invariant는
- context 하나마다 다시 계산되는 비용이 아니라,
- support `R` 전체에서 재사용되는 정준 원자 저장소의 크기
로 읽힌다.

### Conjecture W (Orbiting Zone)
weak stability만으로는, 또는 weak stability와 support-typed canonicity만으로도,
표현 계열이 필연적으로 SDD형 rigidity로 수렴하지는 않는다.

정확히는, 자연스러운 representation classes의 연속체 `\mathcal K_1, \mathcal K_2, \dots`가 존재해서

1. 각 `\mathcal K_i`는 weakly stable이며,
2. 일부는 support-typed canonicity까지 가지지만,
3. canonical library property 또는 Boolean-combination tractability는 일관되게 갖지 않으며,
4. 따라서 structured d-DNNF와 SDD 사이의 중간지대에서 오래 맴도는(non-convergent) behavior를 보인다.

직관:
- support collapse를 금지하는 것만으로는 local atom들이 하나의 canonical partition family로 정렬될 이유가 없다.
- 같은 support에서의 merge를 강제해도, context 전체를 하나의 재사용 라이브러리로 압축하는 것은 별개의 요구다.
- 따라서 weak shell-stability 수준의 강화만으로는 rigidity basin에 곧바로 빨려 들어가지 않을 수 있다.

### Conjecture C (Convergence Zone)
반대로, 어떤 exact representation class `\mathcal K`가 다음 네 줄을 만족하면,
`\mathcal K`는 SDD/AOMDD형 exact lifting을 허용하는 canonical zone으로 빠르게 수렴한다.

1. weak stability,
2. support-typed canonicity,
3. canonical library property,
4. same-support discipline 아래에서 complement/Boolean combinations와의 정합성.

결론적으로,
각 support `R`의 local interface cost는 그 support에 charge된 canonical objects의 수와 동치(또는 상수배 동치)이고,
따라서 exact/near-exact flux lifting

\[
\sum_{R \in \mathfrak R} \delta(f,R) \lesssim \mathrm{size}(S)
\]

이 성립한다.

### 현재 해석
- Conjecture W는 structured d-DNNF가 SDD보다 더 succinct할 수 있고,
  동시에 SDD처럼 정준 조합 규칙을 자동으로 갖지는 않는다는 사실과 잘 맞는다.
- Conjecture C는 OBDD/SDD/AOMDD처럼 support와 canonicity가 함께 rigid한 계열들이
  실제로 exact lifting에 가깝게 행동한다는 관찰을 추상화한 것이다.

### 증명 로드맵
Conjecture W를 보이려면:
- weak stability는 유지하되 canonical library property가 깨지는 자연스러운 부분클래스를 찾거나,
- support-typed canonicity는 유지하지만 context 전체를 하나의 library로 압축하지 못하는 예를 만든다.

Conjecture C를 보이려면:
- 각 support `R`에서 local context family가 canonical atom library `\mathcal L_R`로 factorization된다는
  representation theorem을 먼저 세우고,
- 그 다음 charge calculus를 통해
  `|V(S)| = \sum_R B(R)` 및 `\delta(f,R) \le O(B(R))`
  를 결합하면 된다.

### 작업상 중요한 구분
- **필연적인 부분**: exact additive lifting이 성립한다면, 그 내부에는 charge calculus가 있어야 한다.
- **수렴을 강제하는 부분**: support-typed canonicity와 canonical library property 같은 강한 정규성.
- **맴도는 중간지대의 원인**: support rigidity는 일부 확보되었지만, library rigidity 또는 complement 정합성이 부족한 경우.

---

## 16. W/C 추측의 정식화: 맴도는 구간과 수렴 구간

이번 버전에서는 `Conjecture W`와 `Conjecture C`를 더 공리적인 언어로 적는다.
핵심은 structured d-DNNF 전체를 한 번에 다루기보다,
`어떤 추가 공리 묶음이 들어오면 정확히 무엇이 복구되는가`를 층으로 나누는 것이다.

### 16.1. 세 개의 핵심 속성

고정된 support 시스템 `(\mathfrak R, \mathrm{Ctx})`를 respect하는 exact compilation/solver 클래스 `\mathcal K`를 생각하자.

#### (WS) Weak shell-stability
모든 support `R \in \mathfrak R`, 모든 admissible context `p \in \mathrm{Ctx}(R)`에 대해,
context를 가한 뒤 `R`에서 보이는 local atom은 원래 회로/표현에서도 이미 `R`-support를 가진 객체여야 한다.

직관:
context 때문에 더 큰 support의 객체가 `R`로 붕괴하여 나타나는 collapse를 금지한다.

#### (SC) Support-typed canonicity
같은 support `R`에서 같은 의미를 계산하는 두 local object는 동일한 canonical object로 압축된다.

직관:
같은 support 안의 의미론적 중복이 남지 않도록 한다.

#### (NC) Negation coherence
같은 support discipline(예: 같은 vtree 또는 같은 pseudo tree) 아래에서 `f`와 `\neg f`가 모두 small representation을 가지면,
그 두 representation은 같은 support system 안에서 상호 변환 가능하거나,
적어도 같은 support system을 따르는 stronger canonical language로 polynomial simulation 된다.

직관:
`yes-side`와 `no-side`가 같은 좌표계 위에서 맞물리게 만든다.

### 16.2. 층별로 복구되는 것

이 세 속성은 각각 다른 역할을 한다.

- `WS`만 있으면: naive fixed-support lifting이 다시 가능해질 여지가 생긴다.
- `WS + SC`가 있으면: local library cost를 fixed-support node mass와 직접 비교할 수 있다.
- `WS + SC + NC`가 있으면: complement 쪽까지 같은 support calculus 안에 들어와서, canonical library language로의 수렴이 강하게 시사된다.

즉,

```text
WS          : collapse 금지
WS + SC     : support 내부 canonical library 형성
WS + SC + NC: yes/no 양쪽이 같은 support calculus 안에서 정렬
```

### 16.3. Conjecture W (wandering zone)

**Conjecture W.**
자연스러운 exact structured classes `\mathcal K`가 존재해서,

1. `\mathcal K`는 `WS`를 만족한다.
2. `\mathcal K`는 `SC`를 만족하지 않는다.
3. `\mathcal K`는 고정된 support discipline 아래 SDD/AOMDD류 canonical language로 polynomially collapse하지 않는다.

직관적으로는,
`WS`는 collapse만 막고,
같은 support에서의 semantic merging이나 partition compression의 유일성은 전혀 강제하지 않으므로,
structured d-DNNF와 SDD/AOMDD 사이에 실제 intermediate zone이 남는다는 추측이다.

### 16.4. Conjecture C (canonical convergence)

**Conjecture C.**
자연스러운 exact support-faithful classes `\mathcal K`가 다음을 모두 만족하면,

1. `WS`
2. `SC`
3. `NC`
4. support-wise additive lifting (또는 그에 준하는 exact flux theorem)

`\mathcal K`는 polynomially simulated by a canonical library language 이다.
여기서 canonical library language는 문자 그대로 SDD일 필요는 없고,
주어진 support discipline에 맞는 `SDD/AOMDD/그 변형`일 수 있다.

즉 이 추측은
`structured exact language + 충분한 rigidity`
가 결국 canonical attractor 쪽으로 수렴한다는 주장이다.

### 16.5. 약한 형태의 귀결

Conjecture C의 강한 결론(문자 그대로 SDD/AOMDD)을 당장 주장하기보다,
먼저 다음 약한 형태가 더 현실적이다.

**Weak C.**
`WS + SC + NC`를 만족하는 클래스는
support-wise local library calculus를 갖는 canonical representation으로 polynomial simulation 된다.

이 표현은 일부 auxiliary variables, support refinement, 혹은 representation change를 허용할 수 있다.
즉 `SDD 그 자체`가 아니라 `SDD-equivalent canonical zone` 정도를 먼저 노리는 쪽이 안전하다.

### 16.6. 왜 이 둘이 자연스러운가

- structured d-DNNF 전체에서는 collapse가 실제로 일어나므로 `WS`가 자동은 아니다.
- structured d-DNNF는 SDD보다 더 succinct할 수 있고, negation/disjunction/∃-projection에 대해 닫혀 있지 않다.
  따라서 `WS`가 조금 보강된 정도만으로는 SDD 쪽으로 즉시 수렴한다고 보기 어렵다.
- 반대로 `f`와 `¬f`가 같은 vtree 아래 small structured d-DNNF를 가지면,
  auxiliary variables가 들어간 modified vtree 아래 small SDD로 옮길 수 있다는 결과는
  `NC`가 들어오면 수렴이 빨라질 것이라는 강한 힌트다.
- AOMDD는 pseudo tree 아래 canonical/minimal representation을 주므로,
  수렴의 종착점이 꼭 SDD 하나만은 아닐 수 있다.

### 16.7. 연구 전략

이제 가장 자연스러운 연구 순서는 다음 둘 중 하나다.

#### 경로 A: W를 밀기
`WS`는 만족하지만 `SC`는 실패하는 자연 클래스 예를 찾아,
실제로 intermediate zone이 넓게 존재함을 보인다.

#### 경로 B: C를 밀기
`WS + SC + NC`가 주어지면 canonical attractor로 가는 representation theorem을 증명한다.

현재 감각으로는,
- `W`는 counterexample/부분클래스 구성의 방향이고,
- `C`는 meta-theorem/표현정리의 방향이다.

둘 다 중요하지만, `C`가 성립하려면 어떤 버전의 `NC`가 정확히 필요하고 충분한지가 핵심 난점이다.

### 16.8. 현재 베팅의 공리적 재정리

- `WS`만으로는 **맴도는 구간**이 남는다.
- `WS + SC`는 exact lifting 쪽으로 많이 가까워지지만, 여전히 complement와 global closure가 느슨할 수 있다.
- `WS + SC + NC`에 additive lifting까지 들어오면,
  **빠르게 canonical attractor로 수렴**할 가능성이 크다.
- 다만 그 attractor는 SDD 하나가 아니라,
  support discipline에 따라 SDD/AOMDD/기타 canonical library language일 수 있다.

---

## 18. Conjecture W / Conjecture C

이제 `structured d-DNNF -> SDD류 rigidity`를 한 번에 묻지 않고,
`orbiting zone`과 `convergence zone`을 나누는 두 개의 작업 가설로 정리한다.

### Conjecture W (Orbiting Zone)
자연스러운 structured d-DNNF 부분클래스 `\mathcal W`가 존재해서 다음을 만족한다.

1. `\mathcal W`의 모든 회로는 **weak shell-stability**를 만족한다.
2. `\mathcal W`는 SDD보다 엄격히 넓거나, 적어도 SDD와 다르게 행동한다.
3. `\mathcal W`에서는 support별 local cut lower bound가
   
   \[
   N_D(v) \ge \mu_T^{\max}(f,v)
   \]
   
   꼴로는 복구되지만,
   
   \[
   |D| \stackrel{?}{\ge} \sum_v \lambda_T(f,v)
   \]
   
   같은 **exact additive lifting**은 일반적으로 성립하지 않는다.
4. 즉 `\mathcal W`는 fixed-support local control은 주지만,
   canonical shell library까지는 강제하지 않는 **중간지대**를 이룬다.

직관:
weak shell-stability는 context-collapse만 금지할 뿐,
같은 support에서 같은 의미를 계산하는 노드의 전역 병합이나
compressed partition의 유일성까지는 전혀 강제하지 않는다.
따라서 이 수준에서는 support rigidity는 있으나 merge rigidity는 부족해서
오래 `맴도는` 자연스러운 클래스가 존재할 가능성이 높다.

### Conjecture C (Canonical Convergence Zone)
structured d-DNNF 부분클래스 `\mathcal C`가 다음 네 조건을 만족한다고 하자.

1. **weak shell-stability**
2. **support-typed canonicity**
3. **support-local negation coherence**:
   같은 support 체계 아래 `f`와 `\neg f`의 local interface가 함께 작은 크기로 표현된다.
4. **canonical partition-library closure**:
   각 support `R`에서 local behaviors를 표현하는 compressed library가 유일하고,
   shell restriction에 대해 library의 부분집합 선택으로 내려간다.

그러면 `\mathcal C`는 사실상 SDD/AOMDD형 exact lifting regime로 수렴한다.
구체적으로는, 어떤 refined support system 위에서

\[
|D| \ge \sum_{R} \Lambda_{\mathcal C}(f,R)
\]

꼴의 exact 또는 near-exact flux lifting이 가능하고,
추가적인 정규성 하에서는 `\mathcal C`의 회로를 canonical SDD/AOMDD류 언어로
다항 또는 준다항 overhead 내에 시뮬레이션할 수 있을 것으로 예상한다.

직관:
약한 안정성만으로는 collapse만 막을 뿐이지만,
여기에 same-support negation coherence와 canonical partition library까지 더하면
local atom들이 거의 `support별 canonical basis`처럼 행동하게 된다.
이 지점부터는 구조가 급격히 rigid해져서
SDD/AOMDD류의 charge calculus와 큰 차이가 없어질 가능성이 높다.

### 왜 W와 C를 동시에 두는가
- `W`는 `왜 중간지대가 자연스러운가`를 설명한다.
- `C`는 `어떤 추가 공리부터는 왜 rigid family로 빨려 들어가는가`를 설명한다.

둘 중 하나만 두면 그림이 왜곡된다.
- `W`만 두면: 결국 아무 강한 정리도 기대할 수 없는 것처럼 보인다.
- `C`만 두면: structured d-DNNF의 진짜 유연성을 과소평가하게 된다.

### 검증 경로

#### W를 향한 경로
1. structured d-DNNF vs SDD separation witness를 다시 본다.
2. 그 witness가 weak shell-stability를 만족하도록 정규화될 수 있는지 본다.
3. 가능하면 `orbiting` 자연 클래스의 존재가 강해진다.
4. 반대로 모든 such normalization이 quasipoly 이상 blow-up을 유발하면 `C`가 강화된다.

#### C를 향한 경로
1. shell-stability + canonicity로부터 support별 canonical library를 구축한다.
2. negation coherence를 써서 library가 partition-complete하다는 것을 보인다.
3. 각 support의 canonical library를 decision node 또는 AND/OR meta-node로 조립한다.
4. charge calculus와 결합해 exact/near-exact flux lifting을 얻는다.

### 현재 베팅
- `W`는 존재할 가능성이 높다. 즉, `맴도는 구간`은 남아 있을 것 같다.
- 하지만 exact additive lifting까지 요구하는 순간에는 `C` 쪽으로 빠르게 이동할 가능성이 높다.
- 그래서 `structured d-DNNF 전체`에서 한 방에 정리를 기대하기보다,
  `W`와 `C` 사이의 경계 공리를 찾는 것이 더 현실적인 연구 방향이다.

## 16. Conjecture W / Conjecture C / Threshold Principle

### 16.1. 왜 이제 `문턱` 언어로 바꾸어야 하는가

지금까지 얻은 사실을 종합하면, structured d-DNNF 전반에 대해 naive fixed-support lifting은 거짓이다.
작은 counterexample에서 이미 context-collapse가 실제로 발생한다.
반면 SDD와 AOMDD처럼 canonical/minimal한 언어에서는 support-typed charging과 additivity가 자연스럽게 성립한다.

따라서 이제 질문은 단순히

- structured d-DNNF가 SDD로 가느냐

가 아니라,

- **어떤 공리 조합을 넘는 순간 support-rigid canonical basin으로 들어가는가**

로 바뀐다.

이를 위해 아래의 두 추측과 하나의 문턱 원리를 둔다.

---

### 16.2. Conjecture W (wandering zone)

**Conjecture W.**
다음 성질을 만족하는 자연스러운 exact structured d-DNNF 부분클래스 `C_W`가 존재한다.

1. shell restriction에 대해 닫혀 있다.
2. weak shell-stability를 만족한다.
3. 그러나 support-typed canonicity는 만족하지 않는다.
4. 따라서 fixed-support exact lifting은 일반적으로 성립하지 않거나, 성립하더라도 canonical library cost와 직접 일치하지 않는다.
5. 이 클래스는 polynomially simulated by standard SDD일 필요가 없다.

직관:
weak shell-stability는 support collapse만 막을 뿐,
같은 support에서 같은 함수를 계산하는 subcircuits의 global merge를 강제하지 않는다.
그러므로 이 수준에서는 local decomposition 라이브러리가 여전히 비정준적일 수 있고,
그 결과 structured d-DNNF와 SDD 사이에 실질적인 intermediate region이 남는다.

이 추측이 참이라면,

\[
\text{weak shell-stability} \not\Rightarrow \text{fast convergence to canonical SDD-like form}.
\]

---

### 16.3. Conjecture C (canonical convergence)

**Conjecture C.**
고정된 support 시스템 위의 exact compilation 언어/solver 클래스 `C`가 다음을 만족한다고 하자.

1. shell restriction closure,
2. weak shell-stability,
3. support-typed canonicity,
4. support-preserving complement stability
   (적어도 `f`와 `¬f`가 같은 support discipline 안에서 다뤄진다),
5. support-charged additive lifting
   (fixed-support birth mass의 합이 전체 크기를 통제한다).

그러면 `C`는 polynomially simulated by a support-rigid canonical language,
구체적으로는 vtree 기반이면 SDD-type,
pseudo-tree 기반이면 AOMDD-type 표현으로 환원된다고 추측한다.

더 약하게는,
`C`의 local interface calculus는 canonical library language로 정규화되며,
전체 복잡도는 그 canonical library mass로 제어된다.

직관:
- 2는 support collapse를 금지하고,
- 3은 같은 support에서 같은 의미를 하나로 강제하며,
- 4는 yes-side / no-side가 같은 discipline 안에서 정합적으로 움직이게 하고,
- 5는 local 비용을 전역 크기로 올린다.

이 네 줄이 함께 들어오면,
비정준적 structured d-DNNF의 자유도 대부분이 사라지고,
남는 것은 support-rigid canonical library뿐일 가능성이 높다.

---

### 16.4. Threshold Principle (비공식)

위 두 추측을 하나로 묶으면 다음 문턱 그림이 나온다.

\[
\text{bare structured d-DNNF}
\;
\supsetneq
\;
\text{wandering zone}
\;
\supsetneq
\;
\text{canonical threshold}
\;
\subseteq
\;
\text{SDD/AOMDD-like rigid basin}.
\]

여기서

- wandering zone의 왼쪽 경계는 **weak shell-stability**,
- canonical threshold의 핵심은 **support-typed canonicity + complement stability + additive lifting**

라고 본다.

즉,

\[
\text{stability alone} \Rightarrow \text{still wandering possible},
\]

하지만

\[
\text{stability + canonicity + dual stability + lifting}
\Rightarrow
\text{rapid drift into a rigid canonical basin}.
\]

---

### 16.5. 왜 `rapid`라고 보나

그 이유는 다음 두 갈래다.

1. **same-vtree duality의 강도**
   structured d-DNNF 문헌에는 `f`와 `¬f`가 같은 vtree를 respect하는 작은 structured d-DNNF를 모두 가지면,
   `f`가 polynomial-size SDD 쪽으로 이동할 수 있다는 결과가 있다.
   이는 complement compatibility가 structured d-DNNF의 자유도를 크게 줄인다는 직접적 증거다.

2. **canonical support charging의 강도**
   OBDD, SDD, AOMDD에서는 같은 support에서 같은 의미를 계산하면 merge가 사실상 강제된다.
   이 성질이 들어오면 local library cost와 fixed-support node mass가 거의 일치하게 되고,
   이후에는 additivity가 global size를 제어한다.

즉 `rapid`의 의미는

- syntax가 곧바로 표준 SDD가 된다는 뜻이 아니라,
- **남는 자유도가 canonical support library의 재표현 정도로만 축소된다**

는 뜻이다.

---

### 16.6. 왜 `wandering`도 현실적인가

반대로 weak shell-stability까지만으로는 다음이 전혀 강제되지 않는다.

1. 같은 support에서의 유일한 정규형
2. compressed partition의 유일성
3. complement와의 같은-support 정합성
4. local library mass의 support-wise additive lifting

실제로 structured d-DNNF는 SDD보다 더 succinct할 수 있고,
standard SDD로는 따라가기 어려운 함수들이 존재한다.
또한 structured d-DNNF는 negation, disjunction, existential quantification에 일반적으로 닫혀 있지 않다.
이는 weak stability만으로는 rigidity basin에 자동 진입하지 않음을 뒷받침한다.

---

### 16.7. 현재 연구 과제로 번역

이제 질문은 네 개로 정리된다.

1. weak shell-stability를 만족하지만 support-typed canonicity는 없는 자연스러운 클래스가 실제로 존재하는가?
2. 그런 클래스가 standard SDD보다 genuinely 더 넓은가?
3. support-typed canonicity를 넣는 순간 local library가 실제로 정준화되는가?
4. 여기에 same-support complement stability와 additive lifting을 더하면 SDD/AOMDD-type simulation이 따라오는가?

현재 판단은:

- 1과 2는 **예일 가능성**이 꽤 높다.
- 3은 **모형에 따라 다르지만 꽤 강하게 예** 쪽이다.
- 4는 아직 미증명이나, 지금까지 본 증거는 **예 방향**으로 기운다.

---

### 16.8. 가장 공격적인 형태의 추측

다음이 현재 메모의 가장 공격적인 버전이다.

**Rigidity Threshold Conjecture.**
고정 support 시스템 위의 exact compilation 클래스 `C`가

- shell restriction closure,
- weak shell-stability,
- support-typed canonicity,
- same-support complement stability,
- support-charged additive lifting

을 만족하면,
`C`의 모든 표현은 polynomial blow-up 이내에서 어떤 canonical support library language로 시뮬레이션된다.
vtree setting에서는 SDD류,
pseudo-tree setting에서는 AOMDD류가 그 대표 후보다.

반대로 support-typed canonicity 또는 complement stability가 빠지면,
`C`는 여전히 wandering zone에 머물 수 있다.

---

### 16.9. 다음 단계

다음으로 가장 자연스러운 일은 두 가지다.

1. **Conjecture W 후보 찾기**:
   weak shell-stability는 만족하지만 canonicality는 없는 자연 structured d-DNNF subclass를 설계/식별한다.

2. **Conjecture C의 첫 보조정리 만들기**:
   support-typed canonicity + same-support complement stability에서
   local shell library가 canonical sentential partition으로 정렬된다는 lemma를 세운다.

이 둘이 각각 잡히면,
`맴도는 구간`과 `수렴 구간`의 경계가 실제 정리 수준으로 내려온다.

---

## 18. Orbiting zone / Convergence zone: 공리적 경계선

이제까지의 논의를 가장 압축하면,
문제는 structured d-DNNF 전체가 아니라
**support-rigid exact solver들이 어느 순간부터 canonical library calculus로 수렴하는가**이다.

이를 위해 다음 네 속성을 분리한다.

### 정의 18.1 (monotone chargeability)
solver `S`의 각 internal node `u`에 대해 support `\chi(u) \in \mathfrak R`를 붙일 수 있고,

1. 각 node는 정확히 하나의 support에만 청구된다.
2. edge `u \to v`가 있으면 `\chi(v) \prec \chi(u)` 이다.

라고 하자.

이때 support별 birth mass는

\[
B_S(R):=|\chi^{-1}(R)|
\]

로 정의된다.

### 정의 18.2 (weak shell-stability)
support `R`와 admissible context `\alpha \in \mathrm{Ctx}(R)`에 대해,
`\alpha` 아래에서 local atom으로 보이는 모든 객체는
원래부터 `R`에 청구된 node여야 한다.

즉, context에 의해 더 큰 support의 node가 `R`로 붕괴해서 나타나는 일이 없어야 한다.

structured d-DNNF 일반형에서는 이 성질이 깨지는 작은 반례가 이미 있다.

### 정의 18.3 (support-typed canonicity)
같은 support `R`에 청구된 두 node `u,v`가 같은 함수를 계산하면

\[
\llbracket u \rrbracket = \llbracket v \rrbracket
\quad\Longrightarrow\quad
u(u)=\nu(v)
\]

가 되어야 한다.

즉, semantic quotient가 support 내부에서 완전히 구현된다.

### 정의 18.4 (canonical library realization)
각 support `R`에 대해, solver 안의 `R`-charged canonical node들의 함수집합을

\[
\mathcal L_S(R)
\]

라 하자.

이 집합이 모든 admissible context `\alpha \in \mathrm{Ctx}(R)`에 대해
`f^R_\alpha`를 exact하게 재구성하는 **universal library**이면,
solver는 support `R`에서 canonical library realization을 가진다고 하자.

즉 각 `\alpha`마다 `\mathcal L_S(R)`의 어떤 부분집합이 존재해서,
적절한 deterministic/disjoint composition 규칙 아래
정확히 `f^R_\alpha`를 복원해야 한다.

---

## 19. 추상 exact lifting 정리 (수렴 구간)

이제 local 불변량을 단순 cut 비용이 아니라
support `R`에서의 **minimal universal library cost**로 잡는다.

### 정의 19.1 (minimal universal library cost)

\[
\lambda_{\mathfrak C}(f,R)
:=
\min\{|U| : U \text{ is an exact universal library for }(f,R)\}.
\]

여기서 universal library란,
모든 admissible context에 대해 그 context 아래 residual/local function을
`U`의 부분집합들로 정확히 재구성할 수 있는 라이브러리를 뜻한다.

### 정리 19.2 (Abstract Exact Lifting Theorem)
다음을 만족하는 `\mathfrak C`-faithful exact solver class를 생각하자.

1. monotone chargeability,
2. weak shell-stability,
3. support-typed canonicity,
4. canonical library realization.

그러면 임의의 solver `S`와 함수 `f`에 대해

\[
\sum_{R\in\mathfrak R} \lambda_{\mathfrak C}(f,R)
\le
\sum_{R\in\mathfrak R} B_S(R)
=
|V(S)|.
\]

즉 local universal library costs의 합이 solver 전체 internal size를 하한한다.

### 증명 스케치
support `R`를 고정하자.
weak shell-stability 때문에 `R`에서 context별로 보이는 local atom들은
모두 원래부터 `R`에 청구된 node에서 나온다.
canonical library realization에 의해,
`R`-charged canonical node들의 함수집합 `\mathcal L_S(R)`는
실제로 `(f,R)`의 exact universal library가 된다.
따라서

\[
\lambda_{\mathfrak C}(f,R) \le |\mathcal L_S(R)|.
\]

support-typed canonicity 때문에 `\mathcal L_S(R)`의 크기는
중복을 제거한 `R`-charged node 수와 같고,
이는 정확히 `B_S(R)`이다.
즉

\[
\lambda_{\mathfrak C}(f,R) \le B_S(R).
\]

마지막으로 monotone chargeability로 support별 birth masses가 node 집합을 분할하므로

\[
\sum_R \lambda_{\mathfrak C}(f,R)
\le
\sum_R B_S(R)
=
|V(S)|.
\]

∎

### 해설
이 정리는 OBDD의 `residual flux = node count`,
SDD의 `shell library <= charged node mass`를 하나의 골격으로 통합한다.
즉 **exact additive lifting**이 가능한 영역은
결국 `local exactness + support rigidity + semantic quotient + universal library`가
모두 갖춰진 구간이다.

---

## 20. Orbiting Conjecture (Conjecture W)

### 비형식 직관
weak shell-stability만으로는 support collapse는 막지만,
같은 support 내부에서 local atom들이 context마다 다른 방식으로 재조합될 수 있다.
이 경우 하나의 canonical library가 잡히지 않으므로,
solver는 structured d-DNNF와 SDD 사이에서 **맴도는** 중간지대를 가질 수 있다.

### 추측 W
자연스러운 structured d-DNNF 부분클래스 `\mathcal W`가 존재해서,

1. monotone chargeability를 만족하고,
2. weak shell-stability를 만족하지만,
3. support-typed canonicity 또는 canonical library realization 중 적어도 하나는 실패하며,
4. 같은 support discipline 아래 SDD형 exact lifting으로는 일반적으로 환원되지 않는다.

즉 `\mathcal W` 안에는 fixed-support lifting은 부분적으로 가능하지만,
complete exact lifting은 되지 않는 **orbiting zone**이 존재한다.

### 의미
이 추측이 맞으면,
structured d-DNNF와 SDD 사이의 차이는 단순한 문법 차이가 아니라
`context-stable support`와 `canonical reusable library` 사이의 진짜 간극이 된다.

---

## 21. Convergence Conjecture (Conjecture C)

### 비형식 직관
반대로 support rigidity에 더해 semantic quotient와 library rigidity까지 붙으면,
언어는 오래 맴돌지 못하고 빠르게 canonical-library 체제로 수렴할 가능성이 높다.
이때 종착점은 꼭 표준 SDD 한 점일 필요는 없지만,
적어도 `SDD / AOMDD / SDD-variant` 류의 rigid basin 안으로 들어갈 가능성이 크다.

### 추측 C
어떤 exact solver class가 다음을 모두 만족하면,

1. monotone chargeability,
2. weak shell-stability,
3. support-typed canonicity,
4. canonical library realization,
5. 같은 support discipline 아래 complement/Boolean composition에 대한 충분한 정합성,

그 클래스는 적어도 다항 또는 준다항 왜곡 안에서
canonical library calculus로 시뮬레이션된다.

즉,
강한 의미의 exact lifting이 가능해지는 순간
언어는 support-rigid canonical basin으로 **빠르게 수렴**한다.

### 주의
이 추측의 결론은 꼭

\[
\text{"모든 것이 정확히 SDD다"}
\]

일 필요는 없다.
더 적절한 해석은,

\[
\text{"canonical library calculus로 환원 가능하다"}
\]

이다.
즉 대표 실현은 SDD/AOMDD류일 수 있지만,
문법적으로는 다른 변형이 존재할 여지는 남겨 둔다.

---

## 22. 현재의 경계선: 무엇이 이미 증명되었나

현재까지 이 메모 수준에서 확보된 것은 다음과 같다.

1. **OBDD**에서는 local residual quotient와 global flux가 정확식으로 맞물린다.
2. **SDD**에서는 local invariant를 one-shot cut cost가 아니라 universal shell library cost로 바꾸면,
   support-typed canonicity를 통해 additive lifting이 성립한다.
3. **structured d-DNNF 일반형**에서는 naive fixed-support lifting이 작은 반례로 깨진다.
4. structured d-DNNF에서도 shell-active mass에 대한 하한은 얻을 수 있다.
5. 따라서 structured d-DNNF와 SDD의 차이는
   `local cut decomposition 존재`가 아니라
   `그 분해 원자들이 support-stable한 canonical library로 모이는가`에 있다.

즉 현재의 논리적 경계선은

\[
\text{structured d-DNNF}
\quad\Big|
\quad
\text{orbiting zone}
\quad\Big|
\quad
\text{canonical library zone (SDD/AOMDD류)}
\]

처럼 보는 것이 가장 자연스럽다.

---

## 23. 다음 작업

이제 남은 작업은 두 갈래다.

### 경로 W: orbiting zone을 실제 예로 두껍게 만들기
- weak shell-stability는 만족하지만 canonical library realization은 실패하는 자연 클래스 찾기
- structured d-DNNF와 SDD 사이의 실제 분리 family를 이 언어로 재해석하기

### 경로 C: convergence zone의 충분조건 정리화
- complement coherence와 Boolean-combination stability를 공리화하기
- 그 공리 아래 canonical library calculus로의 시뮬레이션 정리 시도하기

현재 판단으로는,
**반례는 이미 작게 확보되었으므로, 이제는 경로 C의 공리를 조금 더 날카롭게 적는 것이 생산적**이다.

## 16. Rigidity Ladder: 어디서 맴돌고, 어디서 수렴하나

이제까지의 결과를 `support-local 하한 -> fixed-support library -> global additive lifting -> canonical attractor`의 네 단계로 나눌 수 있다.

### 16.1. 기본 local 단계 (L0)

가정:
- shell restriction closure
- local partition property

그러면 각 support `R`에 대해 shell-active mass
`σ_D(R)`가 local cut cost의 최댓값 `μ_R^{max}(f)`를 하계한다.

즉
`σ_D(R) >= μ_R^{max}(f)`.

이 단계는 structured d-DNNF에서도 성립한다. 다만 이때의 양은 fixed-support node count가 아니라 shell-active mass다.

### 16.2. 안정화 단계 (L1)

추가 가정:
- weak shell-stability

즉, 어떤 shell restriction에서 `R`-원자로 보이는 노드는 원래부터 `R`-support 노드였다고 가정한다.

그러면 shell-active mass가 fixed-support function family로 내려온다.
구체적으로, `F_D(R)`를 `D` 안의 `R`-support 노드들이 계산하는 서로 다른 함수들의 집합이라 하면,
모든 shell restriction `p`에 대해 restricted function `f_p`는 `F_D(R)`의 어떤 부분집합의 서로소 합으로 표현된다.
따라서 universal shell library cost `λ(f,R)`에 대해

`λ(f,R) <= |F_D(R)|`.

이 단계까지는 아직 canonicity를 요구하지 않는다.

### 16.3. 정준화 단계 (L2)

추가 가정:
- support-typed canonicity

즉, 같은 support `R`에서 같은 함수를 계산하는 두 노드는 하나로 merge된다.

그러면 `|F_D(R)| = N_D(R)`이므로

`λ(f,R) <= N_D(R)`.

즉, local library cost가 실제 fixed-support node count를 하계하게 된다.
이게 SDD에서 성공하는 단계다.

### 16.4. 전역 lifting 단계 (L3)

추가 가정:
- exact chargeability / additive lifting

즉, 각 internal node를 정확히 하나의 essential support에 charge할 수 있고,
node set이 support별 fiber로 분해된다.

그러면
`|D| = Σ_R B_D(R)`
꼴의 exact flux decomposition이 생기고, 위의 `λ(f,R) <= N_D(R)`를 합치면

`Σ_R λ(f,R) <= |D|`

류의 global additive lower bound가 나온다.

### 16.5. 보강 단계 (L4)

추가 가정:
- same-support complement compatibility (또는 그에 준하는 Boolean stability)

즉, `f`와 `¬f`가 같은 support discipline 아래 다뤄질 수 있다.

이 단계부터는 단순한 lower bound를 넘어서, 클래스 자체가 canonical library language 쪽으로 수렴할 가능성이 생긴다.

---

## 17. 추상 정리: Library Theorem

support system `Σ` 위의 exact compilation class `C`가 L0와 L1을 만족한다고 하자.
또 `D in C`가 함수 `f`를 계산한다고 하자.

각 support `R`에 대해 `F_D(R)`를 `D` 안의 `R`-support 노드들이 계산하는 서로 다른 함수들의 집합으로 두면,
`F_D(R)`는 `f`의 support `R`에 대한 universal shell library가 된다.
따라서

`λ_Σ(f,R) <= |F_D(R)|`.

또한 `C`가 L2까지 만족하면

`λ_Σ(f,R) <= N_D(R)`.

### 증명 스케치

L0에 의해 모든 shell restriction `p`에 대해, restricted function `f_p`는 pruned object 안의 `R`-원자들의 pairwise disjoint cover로 표현된다.
L1에 의해 이 원자들은 원래 객체 `D` 안의 `R`-support 노드에서 왔다.
따라서 각 `p`마다 `F_D(R)`의 부분집합 `F_{D,p}(R)`가 존재하여 `f_p`를 서로소 합으로 표현한다.
즉 `F_D(R)`는 universal shell library다.
L2가 있으면 같은 `R`-support에서 같은 함수를 계산하는 노드가 merge되므로 `|F_D(R)| = N_D(R)`가 된다. ∎

이 정리는 SDD에서 이미 확보된 shell-library 하한을 추상화한 것이고,
structured d-DNNF 일반형에서는 L1이 깨져서 그대로 적용되지 않는다.

---

## 18. 두 개의 추측: Wandering vs Convergence

### Conjecture W (Wandering Zone)

자연스러운 support-faithful 클래스 `C_W`가 존재하여

1. L0와 L1은 만족하지만,
2. L2 또는 L4는 만족하지 않고,
3. 그 결과 `C_W`는 어떤 canonical library language로도 polynomially simulated되지 않는다.

즉 weak shell-stability만으로는 support-rigid attractor로 수렴하지 않으며,
`fixed-support library lower bound`는 성립해도 `canonical convergence`는 실패할 수 있다는 추측이다.

현재 structured d-DNNF 전체는 L1 자체가 깨지므로 `C_W`의 직접 예는 아니다.
다만 structured d-DNNF가 SDD보다 더 succinct할 수 있고 Boolean closure도 약하다는 사실은,
rigidity가 약해질수록 실제 intermediate zone이 생길 가능성을 강하게 시사한다.

### Conjecture C (Canonical Convergence)

자연스러운 support-faithful 클래스 `C_C`가 L0, L1, L2, L4를 만족하면,
`C_C`는 동일한 support discipline 또는 polynomially related support refinement 위의 canonical library language로 polynomial simulation된다.

즉,
- local partition property,
- weak shell-stability,
- support-typed canonicity,
- complement compatibility

이 네 줄이 함께 있으면, 클래스는 더 이상 `맴돌지` 못하고
SDD/AOMDD류의 rigidity basin으로 빨려 들어간다는 추측이다.

현재 근거:
- SDD는 L2까지 강하게 만족하고 canonical하다.
- AOMDD는 pseudo tree 아래 canonical/minimal representation을 갖는다.
- structured d-DNNF와 그 complement가 같은 vtree를 respect하는 polynomial-size 표현을 가지면, auxiliary variables와 vtree refinement를 허용했을 때 polynomial-size SDD로 갈 수 있다는 2021 결과는 L4가 실제로 수렴 압력을 준다는 강한 증거다.

---

## 19. 현재 작업 가설: Rigidity Threshold

내 현재 작업 가설은 다음과 같다.

- `L0`만으로는 shell-active lower bound까지만 가능하다.
- `L1`이 추가되면 fixed-support library lower bound가 가능해진다.
- `L2`가 추가되면 그 lower bound가 실제 node count로 내려온다.
- `L3`이 추가되면 exact/additive global lifting이 나온다.
- `L4`가 추가되면 클래스 전체가 canonical attractor 쪽으로 수렴할 가능성이 커진다.

즉, 진짜 threshold는 단일 공리가 아니라

`L1 + L2 + L4`

근방에 있을 가능성이 높다.

이 그림이 맞다면,
- `맴도는 구간`은 대략 `L1` 근방,
- `빠르게 수렴하는 구간`은 `L2 + L4` 근방

으로 나뉜다.

다음 목표는 두 가지다.
1. `Conjecture W`의 자연스러운 후보 클래스를 찾는다.
2. `Conjecture C`를 위해, L2+L4가 실제로 어떤 canonical language construction을 강제하는지 더 정밀한 representation theorem으로 바꾼다.

---

## 15. 맴도는 구간과 수렴 구간: Conjecture W / Conjecture C

지금까지의 검토를 통해, structured d-DNNF와 SDD 사이의 간극은 단순한 determinism의 차이가 아니라

1. **support drift / context-collapse를 막는가**,
2. **같은 support에서 같은 의미를 정준적으로 합치는가**,
3. **같은 support에서 complement/partition refinement를 복구할 수 있는가**

의 세 층으로 나뉜다는 그림이 보인다.

이를 정리하기 위해 아래 세 성질을 분리한다.

### 정의 15.1 (Weak shell-stability; WSS)
고정된 support 체계 위의 표현 언어가 WSS를 만족한다는 것은, 모든 표현 `D`, 모든 support `v`, 모든 `v`에 대한 shell restriction `p`에 대해

\[
u\in R^+(D_p,v) \Longrightarrow d\text{-node}_T(u)=v
\]

가 성립하는 것을 말한다.

즉, 어떤 context에서 `v`-원자로 보이는 노드는 원래부터 `v`-support여야 한다.

### 정의 15.2 (Support-typed canonicity; STC)
고정된 support `v`에서 같은 Boolean function을 계산하는 두 reduced object는 동일하다.

형식적으로, reduced form에서

\[
d\text{-node}_T(u)=d\text{-node}_T(u')=v,
\quad \llbracket u\rrbracket = \llbracket u'\rrbracket
\Longrightarrow u=u'.
\]

### 정의 15.3 (Support-complement coherence; SCC)
고정된 support `v`에서 표현 가능한 함수 `g`가 있으면, 같은 support 체계에서 `\neg g`도 다항식 오버헤드로 표현 가능하다.

보다 강한 버전은, support `v`의 유한 라이브러리 `U`가 주어졌을 때, 그들이 생성하는 Boolean algebra의 atom partition을 다항식 오버헤드로 복구할 수 있다는 것이다. 이를 **local partition closure (LPC)** 라고 부른다.

---

## 16. 이미 증명된 약한 정리

### 정리 16.1 (WSS + STC가 주는 local exact lifting)
표현 언어가 WSS와 STC를 만족한다고 하자. 그때 support `v`에서의 universal shell library cost를 `\lambda_T(f,v)`라 하고, canonical reduced representation `D` 안의 `v`-support node 수를 `N_D(v)`라 하면

\[
\lambda_T(f,v) \le N_D(v).
\]

#### 증명 스케치
- WSS로 인해 shell restriction 뒤에 `v`에서 살아남는 원자들은 원래부터 `v`-support node들이다.
- STC로 인해 같은 `v`-support에서 같은 함수를 계산하는 중복 원자들은 하나로 압축된다.
- 따라서 `v`-support node들의 함수집합이 곧 모든 shell restriction을 동시에 덮는 universal shell library가 된다.
- library의 최소 크기는 그 library를 제공하는 node 수보다 클 수 없다.

이 정리는 OBDD와 SDD에서는 그대로 작동하고, structured d-DNNF 일반형에서는 WSS가 실패할 수 있으므로 자동으로는 쓸 수 없다.

---

## 17. Conjecture W (wandering regime)

### 비형식 버전
WSS만으로는 충분하지 않다. support collapse만 막아서는 SDD/AOMDD류 정준 영역으로 자동 수렴하지 않는다.

### 정식 버전
자연스러운 표현 언어 계열 `\mathcal K_W`가 존재해서 다음을 만족할 것이라 예상한다.

1. `\mathcal K_W`는 structured d-DNNF의 부분클래스이다.
2. `\mathcal K_W`는 WSS를 만족한다.
3. `\mathcal K_W`는 STC 또는 SCC/LPC 중 적어도 하나를 만족하지 않는다.
4. `\mathcal K_W`는 SDD에 대해 다항식 시뮬레이션으로 곧장 붕괴하지 않는다.

즉, WSS만으로는 **맴도는 중간 지대**가 남는다.

### 동기
- 일반 structured d-DNNF는 SDD보다 더 succinct할 수 있고, negation·disjunction·existential quantification에 대한 polytime closure가 없다.
- 하지만 이 separating example들이 WSS를 만족하는지는 아직 모른다.
- 따라서 `WSS => SDD collapse`를 기대하는 것은 지나치게 낙관적이고, 먼저 `WSS but not SCC`인 자연스러운 부분클래스를 찾는 것이 맞다.

---

## 18. Conjecture C (convergence regime)

### 비형식 버전
반대로 WSS 위에 STC와 SCC/LPC까지 얹으면, 표현 언어는 꽤 빠르게 SDD/AOMDD류 canonical zone으로 수렴할 가능성이 높다.

### 정식 버전
고정된 support 체계를 가지는 reduced exact language `\mathcal K_C`가 다음을 만족한다고 하자.

1. WSS
2. STC
3. SCC
4. 필요하면 LPC

그렇다면 `\mathcal K_C`는 support별 canonical library를 가지며, 그 library는 local partition으로 정제 가능하다. 따라서 적어도 다항식 오버헤드 안에서 SDD/AOMDD형 canonical representation으로 시뮬레이션될 것이라고 예상한다.

즉,

\[
\mathcal K_C \rightsquigarrow \text{canonical zone}
\]

라는 수렴 현상이 일어날 것으로 본다.

### 왜 빠르게 수렴한다고 보는가
- WSS는 support drift를 막아 support-local library를 고정한다.
- STC는 그 library를 유일화한다.
- SCC/LPC는 그 library를 complement/partition 쪽으로 닫아, decision-style atoms를 복구하게 한다.
- 이 세 단계를 지나면 남는 자유도는 크게 줄고, 사실상 SDD/AOMDD류의 canonical decomposition 규칙에 가까워진다.

---

## 19. 현재까지의 근거

### 근거 19.1 (구조적 근거)
- OBDD는 right-linear support 체계에서 WSS, STC, SCC/LPC를 매우 강하게 만족하는 극단이다.
- SDD는 vtree support 체계에서 STC와 canonical compression을 만족하는 극단이다.
- AOMDD는 pseudo-tree support 체계에서 canonical/minimal representation을 준다.
- structured d-DNNF 일반형은 local decomposition 하한은 강하지만, WSS와 STC가 기본 성질이 아니다.

### 근거 19.2 (문헌 근거)
- SDD는 compressed/trimmed form에서 주어진 vtree에 대해 canonical하다.
- structured d-DNNF는 SDD보다 더 succinct할 수 있고, polytime negation closure를 갖지 않는다.
- 반대로 `f`와 `\neg f`가 같은 vtree를 respect하는 polynomial-size structured d-DNNF를 모두 가지면, `f`는 auxiliary variables를 추가한 vtree 아래 polynomial-size SDD로 시뮬레이션된다.

이 세 사실은 “약한 조건이면 맴돌 수 있고, complement coherence가 붙으면 빠르게 canonical zone으로 끌린다”는 그림과 잘 맞는다.

---

## 20. 현재의 작업 가설

### 작업 가설 G1
WSS만으로는 collapse를 기대하지 않는다.

### 작업 가설 G2
WSS + STC만으로는 local exact lifting까지는 가도, canonical partition extraction까지는 자동으로 안 간다.

### 작업 가설 G3
WSS + STC + SCC/LPC는 사실상 canonical zone의 공리적 특징이다.

즉, 앞으로의 핵심은 다음 경계선을 찾는 것이다.

\[
\text{WSS only} \quad \text{vs.} \quad \text{WSS + STC + SCC/LPC}.
\]

왼쪽은 맴도는 영역, 오른쪽은 빠르게 수렴하는 영역으로 보는 것이 현재로선 가장 자연스럽다.

---

## 21. 다음 할 일

1. `WSS but not SCC`인 자연스러운 structured d-DNNF 부분클래스 후보를 찾는다.
2. `WSS + STC + SCC`에서 실제로 partition extraction이 되는지, 최소한 quasi-SDD까지는 가는지 본다.
3. right-linear / vtree / pseudo-tree를 각각 canonical zone의 서로 다른 극단으로 배치할 수 있는지 정리한다.


---

## 18. 정리된 다음 단계: Library 정리와 `Conjecture W / C`

### 18.1. support별 canonical library

지금까지의 경험을 추상화하면, local invariant는 단순히

\[
\delta(f,R)
\]

같은 최소 표현 비용으로만 보지 말고, support `R`에서 **모든 admissible context를 감당하는 canonical atom들의 라이브러리**로 보는 편이 더 정확하다.

### 정의 18.1 (support-R canonical library)
고정된 support 시스템 `\mathfrak R`와 함수 `f`에 대해, 각 `R\in\mathfrak R`에 대해 유한 집합

\[
\mathcal L_f(R)
\]

이 support `R`의 canonical library라고 하자. 그 원소들은 support `R`에 속한 canonical atom들이다.

원하는 성질은 다음이다.

1. **support-typed**: 각 원자 `g\in \mathcal L_f(R)`는 support `R`에 속한다.
2. **canonical**: 같은 support `R`에서 같은 의미를 갖는 두 원자는 동일하다.
3. **coverage**: 모든 admissible context `\alpha\in \mathrm{Ctx}(R)`에 대해, residual/cut behavior `f^R_\alpha`가 `\mathcal L_f(R)`의 어떤 부분집합의 서로소 합(disjoint union, deterministic disjunction)으로 표현된다.

즉 각 context마다 새로운 원자를 새로 만드는 것이 아니라, support `R`마다 하나의 **고정된 atom 라이브러리**가 있고, 각 context는 그 라이브러리의 부분집합만 고른다.

이 관점은
- OBDD에서는 residual quotient의 atom화,
- SDD에서는 shell restrictions 전체를 덮는 canonical partition library,
- AOMDD에서는 pseudo tree/context 아래의 canonical local subproblem library

로 읽을 수 있다.

### 18.2. 추상 Library Lifting 정리 (증명 가능)

### 정리 18.2 (Abstract Library Lifting)
클래스 `C`가 support 시스템 `\mathfrak R` 위에서 다음을 만족한다고 하자.

1. **weak shell-stability**: 어떤 admissible context에서도 support `R`에서 보이는 local atom은 원래부터 support `R`에 속한다.
2. **support-typed canonicity**: 같은 support `R`에서 같은 의미를 계산하는 두 local object는 동일하다.
3. **library completeness**: 각 `f,R`에 대해 canonical library `\mathcal L_f(R)`가 존재하고, 모든 admissible context residual은 `\mathcal L_f(R)`의 부분집합의 서로소 합으로 표현된다.

그렇다면, `f`의 임의의 `C`-representation `D`에 대해 support `R`에서의 fixed-support node 수 `N_D(R)`는

\[
N_D(R) \ge |\mathcal L_f(R)|
\]

를 만족한다. 따라서 support들에 대해 합을 취하면

\[
|D| \ge \sum_{R\in\mathfrak R} |\mathcal L_f(R)|
\]

형태의 additive lifting이 성립한다.

### 증명 스케치
각 context residual은 `\mathcal L_f(R)`의 원자들의 서로소 합으로 표현된다. weak shell-stability 때문에 이 원자들은 실제 representation 안에서 support `R`의 node들로 구현되어야 한다. support-typed canonicity 때문에 같은 원자를 두 번 세지 않는다. 따라서 support `R`에서 필요한 node 수는 library atom 수 이상이다. support별 합을 취하면 전체 하한이 나온다.

이 정리는 OBDD에서는 이미 `birth mass` 공식으로 닫혀 있고, SDD에서는 `universal shell library cost`에 대해 성립하는 형태를 회수한다. structured d-DNNF 일반형에서는 library completeness가 자동이 아니라는 점이 정확한 장애물이다.

### 18.3. 지금 무엇이 비어 있는가

위 정리에서 진짜 어려운 가정은 3번, 즉 **library completeness**다.

- OBDD: 거의 자동.
- SDD: compressed partition + canonicity로 실질적으로 확보.
- structured d-DNNF: shell restriction마다 local decomposition은 얻어지지만, 그것들이 모든 context를 덮는 **고정 support library**로 합쳐진다는 보장이 없다.

즉 지금 남은 문제는

> shell-wise deterministic decomposition  
> `\Longrightarrow` support-wise canonical library

를 언제 증명할 수 있는가이다.

### 18.4. `Conjecture W` — orbiting zone

### Conjecture W (Wandering / Orbiting Zone)
자연스러운 structured d-DNNF류 subclass `C_W`가 존재해서, 다음을 만족한다.

1. `C_W`는 basic exactness/conditioning/decomposition 공리를 만족한다.
2. `C_W`는 weak shell-stability를 만족한다.
3. 그러나 `C_W`는 support-typed canonicity 또는 library completeness를 만족하지 않는다.
4. 그 결과 `C_W`는 support-rigid canonical language (예: SDD/AOMDD형 언어)로 polynomial simulation되지 않는다.

직관:
- collapse는 금지되지만,
- support 안에서의 semantic quotienting과 canonical library 형성은 아직 일어나지 않으므로,
- exact lifting 직전에서 오래 맴도는 중간지대가 존재한다는 가설이다.

이 가설이 맞다면, `weak shell-stability`만으로는 rigidity basin으로의 빠른 수렴이 일어나지 않는다.

### 18.5. `Conjecture C` — canonical convergence

### Conjecture C (Canonical Convergence)
자연스러운 support-faithful exact class `C`가 다음을 만족한다고 하자.

1. weak shell-stability,
2. support-typed canonicity,
3. same-support complement stability,
4. support별 additive lifting.

그러면 `C`는 적어도 polynomial simulation의 의미에서,

\[
\text{SDD/AOMDD-type support-rigid canonical language}
\]

로 환원된다. 필요하다면 support refinement, auxiliary variables, 또는 동등한 canonical re-encoding을 허용한다.

즉, 이 수준까지 오면 더 이상 자유롭게 orbiting하지 못하고, 어떤 rigid canonical basin으로 **빠르게 수렴**한다는 가설이다.

### 18.6. 두 가설을 잇는 pivot lemma

내가 보기엔 실제 핵심은 `Conjecture C` 자체보다 아래 lemma다.

### Pivot Lemma (예상 형태)
weak shell-stability + support-typed canonicity + same-support complement stability가 있으면,
각 support `R`에서 admissible contexts 전체를 덮는 canonical library `\mathcal L_f(R)`가 존재한다.

즉,

\[
\text{complement stability}
\Longrightarrow
\text{partition refinement}
\Longrightarrow
\text{library completeness}
\]

가 되어야 한다.

이 lemma가 성립하면, 정리 18.2를 통해 `Conjecture C`는 거의 자동으로 뒤따른다.

### 18.7. 현재 베팅

현재 내 베팅은 다음과 같다.

- **약한 조건만으로는 orbiting이 남는다.**
- **complement stability까지 넣는 순간 빠르게 rigid basin으로 끌려간다.**
- 다만 그 basin은 고전적 SDD 한 점이 아니라, SDD / AOMDD / SDD-variant를 포함하는 더 넓은 canonical zone일 가능성이 높다.

### 18.8. 다음 실제 과제

이제 다음 라운드의 실제 작업은 두 갈래다.

1. `Conjecture W` 쪽: weak shell-stability는 있으나 canonical library가 없는 자연스러운 subclass 후보를 만든다.
2. `Conjecture C` 쪽: Pivot Lemma를 support별 보조정리들로 쪼개서, complement stability가 왜 partition refinement를 강제하는지 본다.

현재 우선순위는 2번이다. 이유는, 이쪽이 되면 exact lifting의 추상 이론이 거의 닫히기 때문이다.

## 17. `맴도는 구간`과 `빠른 수렴`을 더 날카롭게 나누는 초안

### 17.1. Conjecture W 쪽의 모형 후보: support-annotated structured d-DNNF

문헌의 기존 클래스가 아니더라도, 다음 thought-experiment 클래스는 왜
`weak shell-stability alone`이 부족한지 잘 보여준다.

**support-annotated structured d-DNNF (sa-st-d-DNNF)** 를 가정하자.

- 모든 ∧-gate와 relevant subcircuit에 `d-node_T(u)=v` 같은 support label을 명시적으로 붙인다.
- pruning/shell restriction은 노드를 제거할 수는 있어도, 살아남은 노드의 support label은 바꾸지 못한다.
- 즉 context에 따라 상위 support 노드가 하위 support로 collapse되는 것은 금지한다.
- 그러나 같은 support에서 같은 함수를 계산하는 두 노드는 merge하지 않아도 된다.
- compressed partition의 유일성이나 complement와의 same-support 정합성도 요구하지 않는다.

이 클래스는 by construction weak shell-stability를 만족한다.
하지만 support-typed canonicity가 없으므로,
local library cost와 fixed-support node mass는 일반적으로 일치하지 않을 수 있다.

따라서 이 thought-experiment는

\[
\text{weak shell-stability} \not\Rightarrow \text{canonical convergence}
\]

를 논리적으로 보여주는 시험장 역할을 한다.

이 클래스가 표준 문헌의 자연 class인지는 별도 문제지만,
적어도 **stability alone이 SDD류 rigidity를 논리적으로 강제하지는 않는다**는 점은 분명히 해 준다.

---

### 17.2. Conjecture C 쪽의 첫 보조정리 후보

Conjecture C를 실제 정리로 끌고 가려면, 다음 lemma가 핵심일 가능성이 높다.

**Canonical Alignment Lemma (후보).**
vtree 기반 exact language `C`가

1. weak shell-stability,
2. support-typed canonicity,
3. same-support complement stability

를 만족한다고 하자.
그러면 각 support node `v`와 함수 `f`에 대해,
`v`에서의 모든 shell restriction residual들을 동시에 덮는
유한한 canonical atom family

\[
\mathcal A_v(f)
\]

가 존재하여, 각 shell restriction `p`마다 어떤 부분집합 `\mathcal A_v(f,p) \subseteq \mathcal A_v(f)`가 있어서

\[
f\mid p \,=\, \bigvee_{a\in \mathcal A_v(f,p)} a
\]

이고, 위 합은 pairwise disjoint하다.
또한 `\mathcal A_v(f)`는 support `v`에서 유일하다.

직관적으로는:
- weak shell-stability가 atom의 support를 고정하고,
- canonicity가 같은 support의 같은 atom을 하나로 만들고,
- complement stability가 yes-side / no-side의 경계를 같은 support 안에서 정렬해
  atom family가 partition처럼 굳어지게 한다.

이 lemma가 성립하면

\[
\lambda_T(f,v)=|\mathcal A_v(f)|
\]

꼴의 exact library cost가 정의되고,
additive lifting과 결합해 전역 하한으로 바로 간다.

---

### 17.3. 그래서 `rapid`의 정확한 의미

내가 말한 `빠르게 수렴`은 다음 뜻이다.

- weak shell-stability만으로는 support collapse만 막는다.
- 여기에 support-typed canonicity를 추가하면, 같은 support 안에서 중복이 급격히 사라진다.
- 여기에 complement stability까지 추가하면, local atoms가 단순 cover가 아니라 partition으로 정렬되기 쉽다.
- 마지막으로 additive lifting이 있으면, 그 partition library가 전역 크기를 직접 통제한다.

즉 수렴은 단계적으로 일어나지만,
**canonicity와 dual stability가 들어오는 순간 남는 자유도는 `canonical atom library의 표현 방식` 정도로 급격히 줄어든다**.
이 의미에서 `rapid`라고 부르는 것이 적절하다.

---

### 17.4. 실제 다음 목표

이제 가장 자연스러운 증명 경로는 다음 둘 중 하나다.

1. sa-st-d-DNNF 같은 stability-only 모형에서
   canonicity 없이도 genuinely noncanonical intermediate behavior가 남는다는 것을 명시적으로 보인다.

2. Canonical Alignment Lemma를 SDD에서 재증명하고,
   그 증명에서 정말로 필요한 줄이
   - support-typed canonicity,
   - same-support complement stability,
   - weak shell-stability
   중 무엇인지 분해한다.

내 판단으로는 2번이 더 생산적이다.
왜냐하면 거기서 빠진 줄이 정확히 structured d-DNNF와 SDD 사이의 문턱을 드러낼 가능성이 크기 때문이다.

### 18.9. 중요한 교정: complement만으로는 아직 부족하다

`Conjecture C`를 조금 더 정확히 말하면, **complement stability만으로는 partition refinement가 자동으로 나오지 않는다.**

왜냐하면 두 support-`R` 원자 `p,q`가 있을 때, 이들을 공통 refinement로 쪼개려면 보통

\[
p\wedge q,
\qquad
p\wedge \neg q,
\qquad
\neg p\wedge q
\]

류의 same-support 조각들이 다시 support `R` 안에서 표현되어야 하기 때문이다.

따라서 실제 임계점은 아마 다음에 더 가깝다.

### Refined Conjecture C
weak shell-stability + support-typed canonicity + same-support complement stability + same-support refinement closure

가 있으면, canonical library가 sentential partition / context-minimal partition 쪽으로 정렬되며,
결국 SDD/AOMDD-type canonical zone으로 polynomially 시뮬레이션된다.

여기서 same-support refinement closure는 적어도 다음의 약한 형태다.

- support `R`의 두 canonical object `p,q`가 있을 때,
  그 공통 refinement를 주는 유한한 support-`R` family를 클래스 내부에서 polynomial cost로 만들 수 있다.

이 교정은 중요하다. structured d-DNNF가 negation, disjunction, existential quantification에 대해 닫혀 있지 않다는 최근 결과는,
`complement`나 `Boolean closure`를 기본 공리로 넣는 순간 클래스가 급격히 rigid해질 수 있음을 시사한다.

즉 현재 더 정확한 그림은:

- weak shell-stability만으로는 orbiting 가능,
- canonicity까지 넣어도 아직 orbiting 가능,
- **canonicity + complement + refinement closure**까지 넣으면 빠른 수렴이 훨씬 그럴듯.

이제 실제 핵심 lemma는 다음과 같다.

### Pivot Lemma (수정판)
weak shell-stability + support-typed canonicity + same-support refinement closure가 있으면,
각 support `R`에 대해 모든 admissible contexts를 덮는 canonical library `\mathcal L_f(R)`가 존재한다.

추가로 same-support complement stability까지 있으면 이 library는 deterministic partition 쪽으로 refinement되어,
SDD/AOMDD형 exact lifting으로 연결된다.
