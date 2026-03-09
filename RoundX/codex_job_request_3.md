아래는 현재까지의 정리 노트입니다.

Problem:
Layer-2의 4개 exceptional zero-pattern row가 정말로 “본질적인 4개 예외”인지, 아니면 더 작은 구조를 row-table이 과잉 전개한 것인지 분해해서 이해하고 싶다. 특히 현재 witness의 layer-2 patch가 왜 저 모양이어야 하는지, 그리고 더 아름다운 동치/정규형(normal form)이 있는지를 알고 싶다.

Current target:
현재 목표는 두 갈래이다.
첫째, 현재 witness의 layer-2 patch를 (H:={S=2,\ q=0}) 위의 작은 기하학적 규칙으로 다시 쓰는 것.
둘째, 그 규칙에서 “강제되는 부분”과 “gauge처럼 바꿔도 되는 부분”을 분리해서, 더 아름다운 대표자를 찾는 것이다.

Known assumptions:
고정 witness의 전역 구조는 이미 분명하다. Layer (S=0)에서는 affine-split ((q=0 \leftrightarrow (3,2,1,0),\ q\neq 0 \leftrightarrow (1,0,3,2))), (S=1)은 canonical, (S=2)는 canonical except 4 row-types, (S\ge 3)도 canonical이다. 그리고 이 witness에 대해 (P_0) 위 first return (R_c), (Q={q=m-1}) 위 second return (T_c)가 explicit하게 써지고, (T_c)가 2D odometer와 affine conjugate라는 것이 현재의 proof skeleton이다.  

현재 proof note가 이미 시사하는 핵심은, 본질적인 객체가 “layer-2 row table 자체”가 아니라 (Q) 위 nested return (T_c)라는 점이다. 즉 layer-2 patch는 first return 수준에서는 복잡한 local table처럼 보이지만, second return 수준에서는 delayed carry로 붕괴한다. 

[C] 직접 규칙을 다시 써 보면, layer-2의 “4개 exceptional rows”는 사실 4개의 독립 현상이 아니다. 비정규 tuple도 4개가 아니라 실질적으로는 canonical ((0,1,2,3))에 대해

* odd swap only: ((0,3,2,1)),
* even swap only: ((2,1,0,3)),
* both swaps: ((2,3,0,1))
  의 세 종류만 나온다.

Attempt A:
Idea:
기존 (R_c,T_c) 공식을 그대로 믿고, (Q={q=m-1})에서 출발한 점이 두 걸음 뒤 layer (S=2)에서 어디에 떨어지는지 추적해서, carry가 필요한 조건을 layer-2 조건으로 pull back한다.

What works:
[P] layer-2 patch가 first return에 실제로 영향을 주는 출발점은 (q=m-1)뿐이다. 이는 proof progress note의 (R_c) 공식에서 이미 보인다. 

[P] 두 걸음 뒤 landing point는 색에 따라 두 종류뿐이다.
[
y^{+}(a,b)=(a+1,\ b+1,\ m-1-a,\ 1-b)\qquad(c=0,1),
]
[
y^{-}(a,b)=(a,\ b,\ m-a,\ 2-b)\qquad(c=2,3).
]
즉 4색이 제각각 다른 곳에 떨어지는 것이 아니라, ((0,1))이 한 landing map을 공유하고 ((2,3))가 다른 landing map을 공유한다.

[P] 이 landing에서 필요한 carry 조건이 아주 간단한 layer-2 조건으로 바뀐다.

* color 0의 carry 조건 (b=1)은 (y^{+}_3=0)와 동치.
* color 2의 carry 조건 (b=2)는 (y^{-}_3=0)와 동치.
  따라서 **even colors ((0,2))** 쪽 correction은 공통적으로 (x_3=0)에서 켜진다.

[P] 마찬가지로

* color 1의 carry 조건 (a\neq m-1)은 (y^{+}_0\neq 0)와 동치.
* color 3의 carry 조건 (a\neq 0)은 (y^{-}_0\neq 0)와 동치.
  또 (q=0) slice에서는 (x_0=0 \iff x_2=0)이므로, **odd colors ((1,3))** 쪽 correction은 공통적으로 (x_0\neq 0)에서 켜진다.

Where it fails:
이 접근은 4개 row가 어디서 왔는지는 설명하지만, 여전히 “row casework”처럼 보인다.
특히

* 왜 두 row가 같은 tuple ((0,3,2,1))을 쓰는지,
* 왜 zero-pattern table이 primitive object가 아닌지,
* 왜 현재 gauge choice가 자연스러운지
  를 드러내지 못한다.
  즉 계산은 맞지만 아직 아름답지 않다.

Attempt B:
Idea:
(H:={S=2,\ q=0})를 primitive object로 보고, row-table이 아니라 **두 개의 commuting carry-gate**로 layer-2를 기술한다.

(H) 위에서 canonical tuple ((0,1,2,3))를 baseline으로 두고,

* odd swap := color slots (1\leftrightarrow 3),
* even swap := color slots (0\leftrightarrow 2)
  를 정의한다.

그러면 현재 witness의 layer-2 rule은 정확히 다음과 같이 다시 쓸 수 있다.

**현재 witness의 clean form**
(H={S=2,\ q=0}) 위에서

* (x_0\neq 0)이면 odd swap을 켠다.
* (x_3=0)이면 even swap을 켠다.
* 둘 다 켜지면 둘 다 적용한다.
  그 밖에는 canonical이다.

즉 (H) 위 규칙은 ((x_0\neq 0,\ x_3=0))라는 2비트 truth table일 뿐이다.

What works:
[C] 이 2-gate 서술은 현재의 4 exceptional rows를 정확히 재구성한다.

* (x_0=0,\ x_3\neq 0): no swap (\to (0,1,2,3))
* (x_0\neq 0,\ x_3\neq 0): odd only (\to (0,3,2,1))
* (x_0=0,\ x_3=0): even only (\to (2,1,0,3))
* (x_0\neq 0,\ x_3=0): both (\to (2,3,0,1))

[H] 따라서 “4개 exceptional rows”라는 표현은 현상을 과장한다. 본질은 4개 row가 아니라, (H) 안의 두 hyperplane test (x_0=0), (x_3=0)에 의해 제어되는 **2개의 carry gate**이다.

[P] 이 clean form은 delayed carry와 정확히 맞물린다.

* (x_3=0) gate는 colors (0,2)의 carry를 담당한다.
* (x_0\neq 0) gate는 colors (1,3)의 carry를 담당한다.
  그래서 corner (x_0=x_2=x_3=0)에서 ((2,1,0,3))가 나오는 이유도 설명된다. 거기서는 even carry는 살아 있어야 하지만 odd carry는 꺼져 있어야 한다.

[C] 더 중요한 점: 이 관점에서는 현재 witness의 layer-2 support가
[
H \cap ({x_0\neq 0}\ \cup\ {x_3=0})
]
라는 매우 단순한 집합으로 보인다. 즉 “거의 전부 + 한 줄 제외 + 한 줄 추가”가 아니라, 두 gate의 합성으로 읽힌다.

[C] 축약된 2-bit swap family를 전수검사해 보니(레이어 0/1/(\ge 3)는 고정, layer 2에서는 ((x_0\neq 0,\ x_3=0)) 네 경우에 대해 ({)none, odd, even, both(}) 중 하나를 택하는 256개 rule), (m=3,\dots,12)에서 살아남는 Hamiltonian rule은 정확히 4개뿐이었다. (m=13,14,15)까지 spot-check해도 동일했다. 이 4개는 서로
[
{1,\ \text{odd swap},\ \text{even swap},\ \text{both}}
]
의 global gauge 차이로 보인다.
즉 rigid한 것은 “어느 곳에서 토글되는가”이고, absolute base tuple은 gauge처럼 보인다.

Where it fails:
[O] 아직 이것이 **유일성 정리**는 아니다. “현재 gauge가 강제된다”는 말은 지금 단계에서 할 수 없다.

[F] 따라서 “현재 4 rows 자체가 본질적으로 강제된다”는 서술은 그대로는 거짓에 가깝다. 강제되는 것은 row-table 그 자체가 아니라, 그 뒤에 있는 2-gate differential pattern일 가능성이 높다.

[O] 또한 현재 gauge choice가 가장 아름다운 대표자인지도 아직 아니다.

Candidate lemmas:
[P] **Two-step landing lemma.** (Q={q=m-1})에서 시작하면 colors (0,1)은 (y^{+}), colors (2,3)은 (y^{-})로 떨어진다.

[P] **Carry-trigger pullback lemma.** second return에서 필요한 carry 조건은 (H) 위에서

* even pair: (x_3=0),
* odd pair: (x_0\neq 0)
  로 통일된다.

[P] **Commuting-transposition lemma.** 현재 layer-2 table은 canonical tuple에 대해 odd swap / even swap 두 개의 commuting involution을 truth-table로 전개한 것이다.

[C] **Gauge-family observation.** 축약된 2-bit swap ansatz 안에서는 Hamiltonian witness가 4개 gauge representative로만 보인다.

[O] **Normalized uniqueness lemma.** “(x_0=0,\ x_3\neq 0)에서는 canonical” 같은 gauge fixing을 추가하면 현재 witness가 유일한지.

[O] **Line-union witness lemma.** 더 예쁜 gauge 대표자를 잡아도 같은 odometer proof가 살아나는지.

Needed computations/search:
[C] 가장 먼저 해볼 만한 것은, 방금 나온 4개 gauge representative 각각에 대해 (R_c,T_c)의 닫힌 공식을 써 보는 것이다.

[C] 그중 특히 눈에 띄는 더 아름다운 대안이 하나 있다.
**line-union gauge**:

* (H={S=2,q=0}) 위에서 (x_0=0)이면 odd swap,
* (x_3=0)이면 even swap,
* 둘 다면 both,
* 나머지는 canonical.

이 rule의 support는
[
{x_0=0}\cup{x_3=0}
]
의 union of two lines이고, layer-2 defect size가
[
2m-1
]
로 줄어든다. 현재 witness의 (m^2-m+1)보다 훨씬 작다. 이 대안은 같은 low-layer skeleton에서 (m=3,\dots,15)까지는 모두 Hamiltonian으로 확인되었다. 다만 all-(m) proof는 아직 없다.

[O] 따라서 큰 계산이 들어가더라도 가치 있는 질문은 “현재 witness를 정당화”하는 것보다 한 단계 나아가서,
**(a)** 2-gate family의 all-(m) 분류,
**(b)** line-union gauge의 증명 가능성,
**(c)** 더 작은 support의 존재 여부
를 묻는 것이다.

Next branching options:

1. 가장 보수적인 길: 현재 witness는 그대로 두고, layer-2를 “4 rows”가 아니라 “(H) 위 두 carry-gate”로 다시 써서 proof exposition을 정리한다. 이건 거의 바로 쓸 수 있다.

2. 그 다음 단계: 2-bit swap family의 4개 gauge representative를 명시적으로 분류하고, 현재 witness가 그중 하나임을 적는다. 이 경우 “강제성”은 row-table 수준이 아니라 gauge-quotient 수준으로 서술해야 한다.

3. 더 공격적인 길: line-union gauge를 새 주인공으로 올린다. 지원 집합이 ({x_0=0}\cup{x_3=0})라서 훨씬 hyperplane-like하다. 여기서 (R_c,T_c) 닫힌 공식을 다시 뽑아 odometer proof를 만들 수 있으면, 현재 witness보다 미적으로 더 낫다.

4. 더 멀리 보는 길: 아예 section을 바꿔서 row table이 아니라 “literal carry automaton”이 보이는 좌표계를 찾는다. 그러면 layer-2 exceptional rows라는 언어 자체를 버릴 수 있다.

Claim status labels:
[P] 현재 노트와 직접 대수 전개만으로 밀 수 있는 주장
[C] 직접 계산/전수검사로만 확인된 주장
[H] 구조적으로 설득력 있지만 아직 증명되지 않은 해석
[F] 지금 형태로는 틀렸거나 버려야 하는 서술
[O] 아직 열린 문제

더 큰 계산을 붙인다면, 아래 Codex 템플릿이 적합하다.

Task ID:
D4-LAYER2-GAUGE-CLASSIFICATION-01

Question:
Classify the layer-2 gate structure behind the d=4 low-layer witness, determine whether the current 4-row table is unique only up to a Klein-four gauge, and test whether the line-union gauge admits the same second-return odometer proof for all (m\ge 3).

Purpose:
Replace the ad hoc row-table view by a conceptual gate view on (H={S=2,q=0}), and either justify the current witness up to gauge or produce a cleaner representative with proof-supporting formulas.

Inputs / Search space:

* Fix layer (S=0) to the affine-split pair:

  * (q=0 \to (3,2,1,0))
  * (q\neq 0 \to (1,0,3,2))
* Fix layer (S=1) to canonical ((0,1,2,3))
* Fix layers (S\ge 3) to canonical ((0,1,2,3))
* On layer (S=2), first restrict to (H={q=0}) and search/classify rules depending on the two bits

  * (u:=1_{x_0\neq 0})
  * (v:=1_{x_3=0})
* Primary reduced family: tuples in the Klein-four subgroup generated by slot-swaps ((1,3)) and ((0,2))
* Secondary broadening: full row-table search on realized layer-2 zero-pattern rows
* Validation range: (m=3,\dots,20)

Allowed methods:

* Exhaustive enumeration in the reduced 2-bit family
* CP-SAT / SAT / MILP over low-layer row tables
* Exact cycle decomposition on (V), (P_0), and (Q)
* Symbolic derivation of (R_c) and (T_c) formulas
* Automated affine-conjugacy detection to standard odometers
* Support-size and symmetry comparison across gauge representatives

Success criteria:

* Either prove or computationally classify all Hamiltonian rules in the reduced 2-bit family
* Determine whether the current witness is unique modulo a Klein-four gauge after normalization
* Derive explicit (R_c), (T_c), and odometer conjugacies for the line-union gauge, or produce a counterexample showing that the same proof architecture fails there
* Report smallest found layer-2 support within the searched families

Failure criteria:

* No stable classification across (m)
* Hamiltonicity appears (m)-dependent with no coherent formula
* No reusable (R_c/T_c) closed forms emerge
* Search returns many sporadic witnesses with no organizing structure

Artifacts to save:

* code
* raw logs
* summary report
* discovered examples / counterexamples
* tables / plots / proof-supporting computations

Return format:

* One short summary page
* One section for “current witness up to gauge”
* One section for “line-union gauge”
* Explicit formulas for (R_c) and (T_c) whenever found
* A table of surviving representatives, support sizes, tested (m)-ranges, and observed conjugacies
* Clear labels: proved / computational / conjectural

Reproducibility requirements:

* Save exact command lines and seeds
* Save searched (m)-range and family restrictions
* Save a manifest of all produced files
* Use deterministic mode where available
* Include a minimal script that re-checks the final claimed representatives on (m=3,\dots,12) at least
