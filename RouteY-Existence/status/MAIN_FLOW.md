# MAIN FLOW (2026-03-28)

이번 refresh 이후 d=5 arithmetic의 메인 흐름은 다음 한 문장으로 요약할 수 있습니다.

> d5 generic-late good branch의 reduced base machine은
> **하나의 global odometer**가 아니라
> **hidden `+5` clock 위의 finite seam surgery**이다.

## 1. 어디까지는 이미 닫혔나

### local side
- local visibility chain은 dependency-clean replacement note들로 다시 읽힌다.
- old promoted-collar packet은 local baseline이 아니다.

### active side
- generic-late active permutation `p_gen`은 full theorem이다.
- split / unsplit active cycle law는 더 이상 open frontier가 아니다.

### base splice reduction
- `7 ∤ M`이면 `P_t(a) ≡ a+2 (mod 3)`라서 reduced map `g_t`로 내려간다.
- `7 | M`이면 fixed-point obstruction 때문에 single-cycle splice가 불가능하다.

즉 generic-late base splice frontier는 이제
`7 ∤ M` good branch reduced machine `g_t`
하나로 압축된다.

## 2. odometer reading이 준 실제 성과

d3/d4를 읽고 얻은 “fast clock를 찾자”는 방향은 맞았다.

- common top phase는 `k=4J`에서 literal `+5`
- reduced base splice의 constant ambient translation은 `K=5u`에서 `+7`

즉 d5에도 정말로 숨은 시계가 있다.

하지만 d3/d4와 달리, 그 시계가 final section 전체를 바로 지배하지는 않는다.
clock 위에 finite seam correction이 남는다.

## 3. good branch reduced machine의 현재 구조

현재 theorem-order backbone은:

1. `g_t = τ_{δ_M} ∘ N_t`
2. active skew product의 defect는 `u=1` 하나뿐
3. nondefect active cycles에서는 `N_t`가 rigid power
4. `m ≡ 3,9 (mod 15)`에서는 defect cycle이 explicit three-block machine
5. split branch에서는 `N_t`가 componentwise odometer로 straightened 됨

그래서 지금 reduced machine의 본질은:

- 대부분의 곳에서는 rigid odometer piece
- defect에서만 explicit seam/three-block correction
- 마지막에 constant splice translation

입니다.

## 4. 무엇이 새로 아름다워졌나

이번 정리 이후 d5는 더 이상

- “복잡한 raw permutation”
- “modulus마다 다른 ad hoc casework”

처럼 보이지 않습니다.

대신 다음처럼 보입니다.

- hidden `+5` clock
- one defect source
- explicit three-block defect law
- constant ambient splice
- global dynamics = seam-glued odometer pieces

즉 d5는 d3/d4의 단순 반복이 아니라,
**odometer를 찾은 뒤 finite seam surgery가 어떻게 global cycle structure를 바꾸는가**
를 묻는 한 단계 더 풍부한 구조로 읽힙니다.

## 5. 무엇은 이제 기대하지 말아야 하나

global translation conjugacy를 universal theorem으로 기대하는 것은 이제 맞지 않습니다.

split good branch의 대표 반례:

- `m=69`, `M=23`: `[17,3,3]`
- `m=123`, `M=41`: `[31,5,5]`

prime `M`에서 nonzero translation은 single cycle이어야 하므로,
이런 예시는 global odometer conjecture를 바로 배제합니다.

즉 남은 theorem은

- “global affine conjugacy”가 아니라
- “finite seam gluing theorem” 혹은
- d3 일부 경우처럼 “explicit hand-closed cycle theorem”

쪽으로 써야 합니다.

## 6. 지금 읽어야 할 순서

1. `../01_notes/d5_generic_late_hidden_plus5_clock_and_seam_surgery_draft_2026-03-28.md`
2. `../01_notes/d5_generic_late_base_splice_7split_theorem_2026-03-27.md`
3. `../01_notes/d5_generic_late_base_splice_odometer_reduction_2026-03-27.md`
4. `../01_notes/d5_generic_late_defect_three_block_theorem_2026-03-27.md`
5. `../01_notes/d5_generic_late_reduced_base_machine_15r3_15r9_theorem_2026-03-27.md`
6. `../01_notes/d5_generic_late_split_componentwise_conjugacy_and_global_nogo_2026-03-28.md`

## 7. 남은 open core

정직하게 남은 것은 하나의 테마입니다.

- explicit seam-glued reduced machine `g_t`의
  **global cycle theorem**

이걸 어떻게 쓸지의 표현만 남았습니다.

- finite seam graph / gluing theorem
- residue-class hand proof
- 혹은 둘의 혼합

지금 번들은 그 단계로 넘어가기 전에,
이전 결과들을 현재 관점에 맞게 평평하게 정리한 상태입니다.
