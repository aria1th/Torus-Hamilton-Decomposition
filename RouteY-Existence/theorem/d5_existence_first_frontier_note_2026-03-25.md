# d=5 존재성 중심(frontier) 연구노트 (2026-03-25)

## 0. 범위와 읽은 자료

이번 패스의 목표는 두 개의 tar 번들을 먼저 읽고,

- 현재 `d=5` 증명 spine 이 어디까지 닫혔는지 재구성하고,
- 남은 공명(resonant) 구간을 **정확한 패턴 분류**가 아니라
  **존재성(existence)** 중심으로 다시 읽는 것,
- 그리고 그 관점에서 실제로 조금 더 전선을 밀어보는 것

이었다.

이번 노트는 특히 다음 계열의 파일들을 중심으로 읽었다.

- 메인 proof status / spine:
  - `README.md`, `PACKAGE_SUMMARY.md`
  - `00_manuscript_and_spine/residual_assembly_theorem_status_2026-03-24.md`
  - `00_manuscript_and_spine/residual_assembly_master_flow_2026-03-25.md`
  - `00_manuscript_and_spine/d5_main_method_update_redefined_2026-03-25.tex`
- 비공명 종결:
  - `01_nonresonant_color1/*`
  - `02_nonresonant_color0_color2/*`
- 공명 전선의 구조화:
  - `03_resonant_overview_and_strategy/*`
  - `04_resonant_section_theorems_and_reductions/*`
- 이전 d=5 bundle의 evidence:
  - `resonant_casebook_summary.txt`
  - `row3_word_classification.txt`
  - `generalization_branch_report.txt`
  - `modulus_followup_63_69_75.txt`
  - `resonant_followup_progress.txt`, `resonant_deeper_progress.txt`

또한 이번 세션에서는 제공된 exact replay 코드 구조를 따라가며,
작은 수의 추가 exact 계산을 직접 수행했다.

중요한 구분:

- 아래의 **이미 bundle 안에 theorem-order 로 올라온 내용**과
- **이번 세션에서 exact finite replay 로 확인한 내용**을

명확히 구분한다. 후자는 아직 정리된 theorem 이 아니다.

---

## 1. 현재 d=5 증명 spine: 무엇이 이미 닫혔는가

현재 bundle 을 그대로 읽으면, `d=5`의 전체 구조는 이미 다음처럼 압축되어 있다.

### 1.1. 앞단(front-end)과 backbone 은 이미 닫힘

- selector/front-end 쪽은 theorem-order 로 정리되어 있다.
- color 4 branch 는 닫혀 있다.
- color 3 branch 도 닫혀 있다.

따라서 graph-side burden 은 더 이상 “5색 전체를 한 번에 찾는 문제”가 아니다.
실제로 남는 것은 **frozen color-3/color-4 backbone 주위에서 residual colors 0,1,2 를 닫는 문제**다.

### 1.2. 작은 홀수 moduli 는 이미 explicit package 로 닫힘

메인 manuscript 에서는

- `m=5,7,9`

에 대해 explicit residual package 가 이미 제시되어 있고,
full torus exact replay 로 5개 color map 이 모두 Hamilton 임이 기록되어 있다.

### 1.3. 비공명(nonresonant) 가지는 theorem-order 로 닫힘

현재 핵심 family 는

```text
P_m = {(1,2,1,3), (1,2,1,4), (0,1,(m-1)/2,4)}.
```

이 family 에 대해 bundle 은 이미 다음을 load-bearing 수준으로 올리고 있다.

- color 1:
  - `3 ∤ m` 이면 Hamilton,
  - `3 | m` 이면 exact 5-cycle decomposition 으로 non-Hamilton.
- color 0:
  - exact strip first-return law 로 닫힘.
- color 2:
  - exact lower law 로 닫힘.

즉

- 작은 홀수 `m=5,7,9`, 그리고
- 모든 odd `m ≥ 11` with `3 ∤ m`

에서는 residual assembly 가 이미 닫혀 있다.

### 1.4. 따라서 d=5의 진짜 남은 global gap 은 하나뿐

현재 manuscript 가 honest 하게 남겨둔 유일한 global gap 은

> **odd resonant moduli `m ≥ 15`, `3 | m` 에서의 uniform residual assembly**

이다.

이것이 bundle 이 말하는 `Frontier bg:five-color-assembly`의 현 상태다.

---

## 2. 공명(resonant) 전선은 지금 어떻게 읽어야 하는가

bundle 의 가장 중요한 변화는 “공명 쪽도 더 이상 막연한 search 가 아니다”는 점이다.
이미 다음 두 갈래로 구조화되어 있다.

### 2.1. 순수 color-1 frontier

현재 공명 쪽의 한 큰 줄기는 pure color-1 frontier 이다.
이 줄기에서 이미 bundle 은 다음 exact 구조를 확보했다.

- width-1 section return formula
- width-1 top-row obstruction
- width-3 exact collar correction
- width-3 double-top obstruction
- same-row `A` on collar row 가 top / double-top obstruction 을 깨는 exact local transducer
- promoted-collar package 에 대한 finite active-burst theorem
- 그리고 그 다음 단계 reduction:
  - base section `H_m = {c=0, d=0}`
  - base subset `B_m = {c=0, d=0, e=0} \cong Z/mZ`
  - induced permutation `P_m : B_m -> B_m`

즉 이 줄기에서는 “local transducer 를 어떻게 만들 것인가?”라는 질문 자체가 상당 부분 끝났고,
남은 문제는 크게 보면

> **1차원 base permutation `P_m` 를 한 주기로 만드는가?**

쪽으로 압축되어 있다.

### 2.2. B-active / gate branch

다른 큰 줄기는

- `45`-type wall-localized color-0 branch,
- `75`-type hybrid branch

이다.

여기서는 defect 가 wall / gate graph 로 압축되고,
특히 `m=45`에서는 `H_4` 위의 finite gate graph 와 SCC 분해가 이미 exact 하게 드러나 있다.

즉 이 줄기에서 남는 문제는 크게 보면

> **어떤 새 support row / word 가 gate destination 을 바꾸어 SCC 를 합치는가?**

라는 finite graph 문제다.

---

## 3. 왜 “정확한 family 분류”보다 “존재성”이 더 자연스러운 목표인가

지금까지의 compression 을 보면, 최종 공명 문제를 굳이

- 정확한 closed form family,
- 정확한 row-by-row atlas,
- 모든 residue class 에 대한 완전한 패턴 분류

로 끝낼 필요가 없을 가능성이 크다.

현재 정말 필요한 것은 그보다 약하다.

### 3.1. pure color-1 branch 에서 필요한 것

promoted-collar 류 package 들에 대해 local obstruction 은 이미 거의 다 벗겨졌다.
남은 것은

1. local active burst 가 항상 finite 임을 보이고,
2. orbit 가 결국 base section / base subset 으로 내려가고,
3. 거기서의 induced permutation 이 single cycle 임을 보이는 것

이다.

여기서는 **정확히 어떤 family 가 유일한가** 보다,

> **허용된 몇 개의 support move 들 중 적어도 하나가 cycle 들을 합친다**

를 보이면 충분하다.

### 3.2. gate branch 에서 필요한 것

`m=45`-type 쪽도 마찬가지다.
여기서 필요한 것은

- exact all-pattern classification 이 아니라,
- SCC 를 합치는 gate-destination change 가 적어도 하나 존재함을 보이는 것

이다.

즉 공명 전체를 existence-only 로 다시 쓰면, 목표는

> “하나의 miracle family 를 찾는다”

가 아니라

> “압축된 finite-state / finite-graph obstruction 에 대해, 허용된 local move 들이 cycle-merging 혹은 SCC-merging 을 일으키는 support 를 **적어도 하나** 가진다”

가 된다.

이것이 현재 자료를 가장 잘 살리는 재정식화라고 본다.

---

## 4. existence-first 로 다시 쓴 d=5 proof program

이미 닫힌 부분과 남은 부분을 합치면, d=5 전체는 다음 형태로 읽을 수 있다.

### 4.1. 이미 끝난 부분

- small odd residual packages: 완료
- nonresonant residual theorem: 완료
- 따라서 odd `m` 중 `m=5,7,9` 또는 `3 ∤ m` 인 모든 경우: 완료

### 4.2. 남은 resonant part 의 존재성 중심 목표

odd `m ≥ 15`, `3 | m` 에 대해, 다음 중 하나를 보이면 충분하다.

#### (E1) pure color-1 branch

어떤 저차원 family `F_{m,η}` (예: sigma-core + 소수의 collar/generic rows) 와 parameter `η` 가 존재하여

1. local active episode 가 항상 finite,
2. induced base map 이 single cycle,
3. donor colors 의 collateral damage 가 staged repair 로 복구됨

을 보인다.

#### (E2) B-active / gate branch

어떤 family `G_{m,η}` 와 parameter `η` 가 존재하여

1. defect 가 wall / gate graph 로 finite reduction 되고,
2. induced gate graph 가 strongly connected,
3. 다른 residual colors 는 Hamilton 을 유지하거나 staged repair 로 복구됨

을 보인다.

이 두 가지 중 moduli 의 branch 에 맞는 하나를 주면 된다.

핵심은 여기서 **η의 정확한 폐형식(closed form) formula 가 없어도 된다는 점**이다.
`η`가 존재한다는 것만 보이면 전체 d=5 decomposition theorem 은 완료된다.

---

## 5. 이번 세션에서 직접 확인한 exact 계산: existence-first 관점의 새 증거

아래 계산들은 bundle 의 theorem 이 아니다. 다만 제공된 exact replay 구조를 따라 실제로 재계산한 것이다.

### 5.1. promoted-collar induced base permutation `P_m` 재구성

promoted-collar color-1 package 의 exact local formula (`promoted_step`)를 사용해서
base permutation `P_m : B_m -> B_m` 를 재구성하면, cycle lengths 는 다음과 같이 bundle 의 note 와 일치한다.

- `m=21`: `11, 5, 5`
- `m=27`: `13, 12, 2`
- `m=33`: `17, 11, 5`
- `m=39`: `10, 9, 9, 8, 3`
- `m=51`: `12, 10, 9, 6, 4, 3, 3, 2, 2`

이것은 pure color-1 branch 가 실제로 **1차원 permutation obstruction**으로 내려왔다는 reading 을 강화한다.

### 5.2. 새 exact success at `m=21`: symmetric double-promoted collar

canonical width-3 package

```text
Nhat_21(1) = {
  (1,2,1,4), (0,1,10,4),
  (1,2,1,3), (0,1,3,3),
  (0,1,9,3), (1,2,10,3), (0,1,11,3)
}
```

에 collar-side same-row `A` 를 양쪽 모두 추가한

```text
S_21^sym = Nhat_21(1) ∪ {(1,2,9,3), (1,2,11,3)}
```

를 exact replay 하면

```text
orbit lengths = [21^5, 21^5, 21^5] = [4084101, 4084101, 4084101].
```

즉 `m=21`에서는 promoted-collar logic 에서 직접 나온 **symmetric double-collar A-thickening**이 실제 all-color Hamilton package 로 닫힌다.

rowwise net permutation 으로 쓰면, 이는 대략

- row `9`: `C` then `A` = `rho`
- row `10`: `A`
- row `11`: `C` then `A` = `rho`

라는 형태다.

나는 extraction 후 text grep 으로 이 exact support pattern 자체는 bundle 안에서 보지 못했다. 다만 row-word equivalence 까지 전부 정규화해서 비교한 것은 아니므로, “형식적으로 완전히 새로운 package”라고 단정하지는 않는다.

### 5.3. 새 exact success at `m=27`: collar-thickening 에서 나온 7-op family

`m=27`, `r=13`에서 다음 7-op package 를 exact replay 했다.

```text
S_27^new = {
  (1,2,1,4),
  (0,1,13,4),
  (1,2,1,3),
  (0,1,3,3),
  (1,2,12,3),
  (1,2,13,3),
  (0,2,14,3)
}.
```

결과는

```text
orbit lengths = [27^5, 27^5, 27^5] = [14348907, 14348907, 14348907].
```

즉 `m=27`에서도 pure color-1 promoted-collar 쪽의 staged idea 에서 바로 나온 저차원 family 가 실제 success 로 닫힌다.

이 package 는 bundle casebook 의 `m=27` 성공 package 와 support pattern 이 다르다.
따라서 적어도 “같은 exact listed package 를 다시 발견한 것”은 아닌 것으로 보인다.

### 5.4. staged repair 패턴은 `m=27,33,39`에서도 계속 보인다

다음 family 를 보자.

```text
D_m^+ := width3 + A_{r-1,3} + A_{r+1,3} + C_{r+1,3}.
```

이번 세션 exact replay 에서 확인한 값은 다음과 같다.

- `m=27`:
  - `orbit lengths = [3268971, 27^5, 27^5]`
- `m=33`:
  - `orbit lengths = [28124415, 33^5, 33^5]`
- `m=39`:
  - `orbit lengths = [9534837, 39^5, 39^5]`

즉 이 family 는 최소한 checked range 에서 반복적으로

> **colors 1,2 를 먼저 닫고, 남는 defect 를 pure color-0 으로 isolate 한다**

는 동일한 staged pattern 을 보인다.

그리고 `m=27`에서는 여기에 `B_{r-1,3}`를 추가하면 실제로 all-color Hamilton 이 된다.
즉

```text
D_27^+ + B_{12,3}
```

가 위의 `S_27^new`와 같은 success 로 닫힌다.

`m=33`에서는 같은 방식이 아직 마지막까지 닫히지 않지만, defect transfer 는 분명히 보인다. 예를 들어

```text
D_33^+ + B_{3,3}
```

는

```text
orbit lengths = [33^5, 33^5, 14285502]
```

를 주어, unresolved defect 를 color 0 에서 color 2 로 옮긴다.

이것은 존재성 중심 관점에서 매우 중요한 신호다.
정확한 atlas 를 모른다고 해도, local channel 들이

- defect 를 한 색에서 다른 색으로 옮기고,
- base permutation / gate structure 를 단계적으로 바꾼다

는 것이 exact data 로 보이기 때문이다.

---

## 6. 이번 세션 계산이 시사하는 것

이번 계산들로부터 내가 얻은 가장 중요한 메시지는 다음이다.

### 6.1. pure color-1 branch 의 핵심 목표는 “transducer 찾기”가 아니라 “cycle merging”이다

double-top breaker 자체는 이미 거의 local level 에서 해부되어 있다.
실제로 더 중요한 것은 그 뒤에 생기는 induced permutation 이 몇 개의 cycle 로 갈라지는지,
그리고 추가 support row 가 그 cycle 들을 어떻게 합치는지이다.

즉 existence-only program 에서는

- transducer 의 exact formula 완전분류

보다

- parameter 하나가 base permutation 의 cycle decomposition 을 어떻게 바꾸는지,
- 그리고 적어도 하나의 parameter 가 single cycle 을 만든다는 것

이 핵심이다.

### 6.2. `C`-visible move 로 colors 1,2 를 닫고, `B`-visible move 로 color 0 를 정리하는 staged 그림이 실제로 보인다

이번 계산에서

- `m=27,33,39`에서 `D_m^+` family 가 colors 1,2 를 먼저 닫고,
- 그 뒤에 남은 것이 pure color-0 defect 로 보이며,
- `m=27`에서는 실제로 `B` channel 하나가 마무리를 해 준다.

이것은 bundle 안의 visibility calculus 와 정확히 맞물린다.

즉 적어도 pure color-1 branch 에서는 다음 식의 theorem 을 노려볼 수 있다.

> 먼저 color-1-visible family 로 colors 1,2 를 닫는다.
> 그 다음 color-1-invisible `B` channel 로 color 0 base permutation / gate structure 를 single cycle 로 만든다.

### 6.3. 공명 쪽 최종 theorem 은 “정확한 global family 분류”보다 “저차원 family 안에서 good parameter 가 존재한다”로 끝날 가능성이 크다

현재 exact data 는 특정 support rows 전체를 완전분류할 필요 없이,
상당히 낮은 자유도 family 안에서 이미 성능 좋은 candidates 가 반복된다는 것을 보여준다.

따라서 최종 theorem 의 형태는 아마

- `η(m)` 의 exact closed form 을 주는 theorem

이 아니라

- 어떤 finite menu 의 family 안에 들어가는 parameter `η` 가 적어도 하나 존재하여,
  induced permutation / gate graph 를 single cycle / SCC 하나로 만든다

가 더 자연스러워 보인다.

---

## 7. d=5에 대한 existence-first conjectural roadmap

현재 자료를 바탕으로 하면, d=5 에 대한 가장 경제적인 남은 목표는 다음 두 정리로 정리된다.

### 7.1. Pure color-1 existence theorem (conjectural target)

어떤 finite low-parameter family `F_{m,η}` 가 존재하여, 모든 odd resonant `m ≥ 15`에 대해 적당한 `η`에 대해

1. local active burst 가 finite,
2. every orbit descends to a base section,
3. induced base permutation 이 single cycle,
4. 다른 두 residual colors 는 Hamilton 을 유지하거나 한 단계 staged repair 로 복구

를 만족한다.

여기서 핵심은 `η`의 exact formula 가 아니라 **존재**다.

### 7.2. B-active / gate existence theorem (conjectural target)

wall / gate branch 에 대해서도 어떤 family `G_{m,η}` 와 적당한 `η`가 존재하여

1. defect 가 finite gate graph 로 압축되고,
2. 그 graph 가 strongly connected,
3. collateral residual defect 는 staged repair 로 복구

를 만족함을 보이면 된다.

이 둘을 branchwise 로 결합하면, small odd + nonresonant closure 와 합쳐서 d=5 전체가 끝난다.

---

## 8. prime d 로의 일반화: 무엇이 옮겨가고, 무엇은 아직 안 옮겨가는가

사용자 요청의 두 번째 축은 “`d=5`를 넘어서 `d = prime` 에서도 존재성만 보여볼 수 있는가?”였다.

여기서는 조심해야 한다.
이번 두 bundle 은 실질적으로 `d=5`에 대한 자료다. 따라서 `d>5`에 대해 실제 theorem 을 주장할 수는 없다.
다만 **proof architecture** 차원에서는 옮겨갈 가능성이 있는 부분이 분명하다.

### 8.1. prime d 에도 거의 확실히 옮겨가는 구조

#### (i) fixed-color quotient

고정된 target color `c`를 추적할 때, local row permutation `pi`는 오직 `pi^{-1}(c)`를 통해서만 보인다는 아이디어는 `d=5` 특유가 아니다.
이 논리는 일반 `S_d`에서도 그대로 살아남는다.

즉 고정된 color 하나를 보면, row-word search 는 원칙적으로

- `|S_d|`개의 경우

가 아니라

- `d`개의 source class

로 내려간다.

이것은 existence proof 에 매우 중요하다. “모든 row-word 를 분류”할 필요가 없기 때문이다.

#### (ii) visibility calculus

transposition `(ab)`는 색 `a,b`에만 보이고 나머지 색에는 invisible 하다는 사실도 일반적이다.
따라서 “이미 닫힌 색을 건드리지 않으면서 남은 색만 repair 하는 staged channel design”은 prime `d`에서도 살아남을 가능성이 높다.

#### (iii) finite-state induced map / gate reduction

d=5에서 가장 중요한 철학은

- full torus dynamics
- -> section return
- -> lower return
- -> finite-state transducer / induced permutation / gate graph

로 compression 하는 것이다.

이것은 exact formula 가 달라져도 existence-first 방향에서는 매우 유력한 일반 템플릿이다.

### 8.2. 아직 prime d 로 바로 옮길 수 없는 부분

아래 항목들은 이번 bundle 로는 전혀 일반화되지 않는다.

- `m mod 24` 법칙
- row-3 `rho/sigma` atlas
- residual colors 가 정확히 3개인 현상 자체
- d=5에서의 특수한 top-collar / double-top formulas

즉 `d=5`의 exact local formulas 를 prime `d`에 복사하는 접근은 맞지 않다.

### 8.3. prime d 에 대한 가장 그럴듯한 existence-first conjecture

현재로서는 다음 정도가 가장 자연스럽다.

> **Prime-d existence-first meta-conjecture.**
> prime `d`에 대해, 만약 front-end/backbone compression 이 모든 but boundedly-many residual colors 를 thin support 위의 finite-state problem 으로 내릴 수 있다면, 최종 Hamilton decomposition proof 는 exact explicit family classification 이 아니라 induced permutation / gate graph 의 cycle-merging existence theorem 으로 끝날 수 있다.

이것은 theorem 이 아니라 roadmap 이다.
하지만 d=5 bundle 이 실제로 보여주는 것은 정확히 이 방향이다.

---

## 9. 지금 바로 다음에 노릴 정리들

이번 패스 기준으로, 다음 타깃이 가장 설득력 있다.

### 9.1. d=5 pure color-1 branch

다음 타입의 정리를 노린다.

1. 한 작은 family 에 대해 local finite-burst / section descent 를 정리한다.
2. induced base permutation 이 parameter 에 따라 오직 국소적으로만 바뀜을 보인다.
3. parameter 가 변하면 cycle 들이 실제로 합쳐진다는 cycle-merging lemma 를 증명한다.
4. 따라서 good parameter 가 하나 존재함을 보인다.

### 9.2. d=5 B-active branch

1. gate graph 의 SCC 들을 local support change 가 어떻게 바꾸는지 exact 하게 쓴다.
2. admissible move 들이 적어도 하나의 inter-SCC edge 를 만든다는 것을 보인다.
3. finite induction 으로 SCC 하나까지 합친다.

### 9.3. prime d

1. fixed-color quotient 를 일반 `S_d` 문맥으로 formalize 한다.
2. backbone-first compression 이 residual colors 수를 boundedly-many 로 줄이는지 본다.
3. 줄어든 뒤에는 d=5와 같은 finite-state existence theorem 을 목표로 한다.

---

## 10. bottom line

이번 두 bundle 을 읽고 나면 d=5의 전체 상황은 다음처럼 정리된다.

- small odd 와 nonresonant 는 이미 닫혀 있다.
- 실제 남은 것은 resonant residual assembly 하나다.
- 그런데 그 문제도 이제는 full selector search 가 아니라
  - base permutation cycle-merging,
  - 혹은 gate graph SCC-merging
  의 문제로 압축되어 있다.

그리고 이번 세션의 exact 계산은 그 existence-first reading 을 더 밀어준다.

- `m=21`에서 promoted-collar 논리에서 직접 나온 새 exact success family 하나를 확인했다.
- `m=27`에서도 같은 철학에서 나온 새 exact success family 하나를 확인했다.
- `m=27,33,39`에서는 “먼저 colors 1,2를 닫고 마지막 color 0 defect 만 isolate 하는” staged family 가 반복적으로 나타난다.

따라서 지금 가장 유망한 frontier 는

> **정확한 패턴 전체를 분류하는 것**이 아니라,
> **압축된 finite-state obstruction 위에서 cycle / SCC 를 합치는 good support 가 적어도 하나 존재함을 보이는 것**

이라고 본다.
