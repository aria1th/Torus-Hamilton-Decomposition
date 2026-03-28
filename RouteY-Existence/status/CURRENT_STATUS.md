# CURRENT STATUS (2026-03-28, refreshed after the odometer / seam-surgery pass)

## 1. Local proof chain

local packet은 여전히 March 27 dependency-clean replacement note들로 읽는 것이 맞습니다.

- `d5_promoted_control_dependency_free_reproof_2026-03-27.md`
- `d5_hinge_corner_dependency_free_proof_2026-03-27.md`
- `d5_bulk_side_top_dependency_free_closure_2026-03-27.md`
- `d5_c0_compact_return_dependency_free_reproof_2026-03-27.md`
- `d5_actual_entry_visibility_dependency_free_upgrade_2026-03-27.md`

즉 old March 25 promoted-collar packet은 더 이상 별도 local dependency가 아닙니다.

다만 honest baseline은 그대로 남아 있습니다.

- width-1 exact section-return theorem
- nonzero top-row transducer packet
- `t=0` top-row / global compact packet
- universal `U->H` bridge theorem

그리고 lower-strip scope correction도 그대로 유효합니다.

```text
R_t = R_* = R_wd1 on all of A_m^c
```

라는 광역 문구는 현재 기준으로는 틀립니다.
현재 packet이 정확히 보이는 범위는

```text
0 <= d <= m-3
```

의 lower-strip localization입니다.

## 2. Safe regime visibility

작업 가정은

```text
m = 3M >= 27,   5 ∤ m.
```

이 safe regime에서 visibility는 다음 네 클래스에 대해 닫혀 있습니다.

- `t=r-1`
- `t=r`
- `t=1`
- generic late 전체

이 상태는 이번 v3에서도 변함이 없습니다.

## 3. Generic-late active arithmetic

generic-late active permutation `p_gen`은 theorem-order로 닫혀 있습니다.

- `M ≢ 2 (mod 3)`이면 single `M`-cycle
- `M ≡ 2 (mod 3)`이면 `Q=(M-2)/3`에 대해 cycle type이 `Q, Q+1, Q+1`

따라서 old generic-late mod-`5` active frontier는 사라졌습니다.

## 4. Base splice: current real frontier

현재 pure color-1 핵심은 visibility가 아니라 base splice입니다.

### 4.1 Good / bad split at `7`

generic late base return `P_t`는 `7`에서 구조적으로 갈립니다.

- **good branch `7 ∤ M`**
  - `P_t(a) ≡ a+2 (mod 3)`
  - 그래서 splice 문제는 reduced base map
    ```text
    g_t : Z_M -> Z_M
    ```
    의 cycle theorem으로 내려갑니다.

- **bad branch `7 | M`**
  - explicit fixed-point obstruction이 있습니다.
  - generic-late single-cycle base splice는 구조적으로 불가능합니다.

즉 현재 arithmetic target은

```text
7 ∤ M good branch의 reduced base machine g_t
```

입니다.

## 5. What the odometer pass changed

이번 v3에서 가장 중요한 해석 변화는 다음입니다.

### 5.1 The fast clock is real

parallel note와 odometer reduction을 합치면, common top branch의 fast clock는
정말로 `+5` odometer입니다.

- `k=4J`에서는 common phase가 literal하게 `+5`
- `K=5u`에서는 reduced base splice의 ambient translation이 `+7`

즉 “clock를 찾는다”는 d3/d4식 방향은 맞았습니다.

### 5.2 The final object is not one global odometer

하지만 split good branch scan에서 global translation conjugacy 기대는 깨졌습니다.

대표 반례:

- `m=69`, `M=23` prime: cycle type `[17,3,3]`
- `m=123`, `M=41` prime: cycle type `[31,5,5]`

prime cyclic group 위의 nonzero translation이라면 이런 분해는 나올 수 없습니다.
따라서 d5의 final reduced machine을 **하나의 global odometer**로 보는 전략은
현재 기준으로는 맞지 않습니다.

### 5.3 The right picture is odometer + seam surgery

good branch generic late에서는 이제 다음이 증명된 backbone입니다.

- `g_t = τ_{δ_M} ∘ N_t`
- active skew product의 defect는 `u=1` 하나뿐
- nondefect active cycle에서는 `N_t`가 rigid power
- `m ≡ 3,9 (mod 15)`에서는 defect cycle이 explicit three-block machine
- split branch에서는 `N_t`가 componentwise odometer로 straightened 됨

그래서 현재 main slogan은

> hidden `+5` clock + finite seam surgery

입니다.

## 6. What is already explicit

다음 범위에서는 reduced base machine이 이미 **explicit finite permutation**입니다.

```text
m = 3M >= 33,
5 ∤ m,
7 ∤ M,
t generic late,
m ≡ 3 or 9 (mod 15).
```

이 범위에서는:

- factorization note:
  `d5_generic_late_base_splice_odometer_reduction_2026-03-27.md`
- defect theorem:
  `d5_generic_late_defect_three_block_theorem_2026-03-27.md`
- combined theorem:
  `d5_generic_late_reduced_base_machine_15r3_15r9_theorem_2026-03-27.md`

을 합치면 local arithmetic은 다 드러나 있습니다.

검증 범위도 현재 bundle 안에 남아 있습니다.

- odometer reduction check:
  `total_moduli = 32`, `factor_failures = 0`, `nondef_failures = 0`, `defect_failures = 0`
- defect three-block theorem check:
  `27 <= m <= 1501`, `84` moduli, `16453` defect-cycle states, `all_pass: True`
- explicit reduced base-machine check:
  `33` moduli, `3407` reduced states, `N_failures = 0`, `g_failures = 0`

## 7. Honest open core

현재 남은 진짜 open core는 다음입니다.

1. reduced base machine `g_t`의 **final cycle theorem**
2. 이 final theorem을 translation conjugacy가 아니라
   **finite seam graph / gluing theorem**으로 쓸지 여부
3. `5 | m` branch
4. manuscript patch와 final all-color assembly

즉 지금은 local cleanup 단계가 아니라, explicit seam-glued finite permutation의
global cycle structure를 마감하는 단계입니다.

## 8. Documentation caveat

한 가지 기록상 caveat가 있습니다.

- split first-special-hit result는 현재 bundle 안에서 standalone precursor note로
  분리되어 있지 않습니다.
- 현재 남아 있는 형태는
  `d5_generic_late_split_componentwise_conjugacy_and_global_nogo_2026-03-28.md`
  의 imported-input packaging과 accompanying check report입니다.

이건 **문서 정리상의 caveat**이지, 이번 번들에서 새로 발견된 수학적 반례는 아닙니다.
