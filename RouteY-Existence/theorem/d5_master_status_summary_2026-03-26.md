# d=5 공명 존재성/증명 프로그램 중간 총정리 (2026-03-26)

## 0. 이번 정리의 목적

이 문서는 지금까지의 여러 연구노트를 한 번에 다시 묶어,

- 무엇이 **정말로 닫힌 부분**인지,
- 무엇이 **exact-check 로 강하게 지지되지만 아직 손증명이 필요한 부분**인지,
- 무엇이 **아직 진짜 open bottleneck**인지,
- 그리고 이 모든 것이 왜 `d=5`, 더 나아가 `d=prime` 존재성 프로그램에 합당한 접근인지,

를 분리해서 적는 상태표다.

핵심 메시지는 간단하다.

> 현재 프로그램은 “정확한 전체 패턴 분류”가 아니라,
> **finite symbolic machine + splice/visibility** 구조 위에서
> 적절한 witness 가 하나 존재함을 보이는 방향으로 압축되었다.

---

## 1. 처음 목표에서 지금 목표로: 문제의 재정식화

초기 목표는 `d=5` 분해의 정확한 global pattern 을 찾는 쪽에 가까웠다.
하지만 두 tar 번들과 후속 exact replay 를 통해 현재 목표는 다음처럼 바뀌었다.

### 1.1 존재성 중심 목표
공명 구간 `3|m` 에서 필요한 것은 전체 패턴 분류가 아니라,

- pure color-1 section 에 대해 Hamiltonian return 이 존재함을 보이는 것,
- 그 뒤 color 0/2 를 staged repair 로 처리할 수 있음을 보이는 것,
- 더 나아가 이 architecture 가 `d=prime` 에도 일반화됨을 보이는 것,

이다.

### 1.2 pure color-1 의 진짜 구조
현재 pure color-1 문제는 사실상 다음 세 변수로 분해된다.

1. `Omega_m` leak: top-wall pocket 이 실제로 빠져나오는가?
2. `B_m` splice: base permutation `B_m` 가 single-cycle 인가?
3. `H_m -> B_m` visibility: upper section 에서 생기는 cycle 들이 결국 base 를 실제로 보는가?

그리고 지금까지의 exact data 는 다음 heuristic 을 강하게 지지한다.

> splice 와 leak 가 둘 다 맞고, visibility 가 깨지지 않으면,
> pure color-1 section exactness 가 나온다.

---

## 2. 지금까지 확보한 큰 구조

## 2.1 local/global 분해
promoted-plus one-line family

```text
P_m^+(t) = P_m^+ ∪ {A_{t,3}}
```

에 대해, dynamics 전체가 bulk 전체에 흩어져 있지 않고 다음 조각으로 압축되었다.

```text
universal bulk cocycle
+ hinge conveyor
+ single corner burst
+ top-row transducer
+ base splice/visibility
```

즉 현재는 full `m^4` state space 를 직접 보지 않고,
상수 개의 symbolic layers 와 finite active bands 만 보면 된다.

## 2.2 support localization
`P_m^+(t)` 의 `t`-dependence 는 bulk 전체가 아니라 top/hinge active locus 에만 남는다.
그래서 lower bulk 는 essentially universal cocycle 로 떨어진다.
이 reduction 은 `d=prime` 일반화 템플릿의 첫 축이다.

## 2.3 `Omega_m` pocket 의 분리
남은 pure color-1 defect 는 막연한 residual 이 아니라 정확한 pocket

```text
Omega_m = {d=e=m-1,
           c ≠ 1 mod 3,
           a ≠ 2c mod 3}
```

으로 압축된다.
splice 는 되는데 leak 이 안 되면, defect 가 정확히 이 pocket 에서만 남는다는 쪽이 반복 확인되었다.

---

## 3. 지금 “증명 수준”까지 올라간 부분

아래는 exact-check 를 넘어, 적어도 theorem-order skeleton 또는 손증명 패킷으로 올라간 부분들이다.

## 3.1 top-row `t != 0` symbolic transducer law
`S_m^- = {d=m-1, e≤m-2, c≠m-2}` 위에서는 `t!=0` 에 대해
one-block map 이 special sigma-layer audit 으로 닫힌다.
핵심은 color 1 choice 가 바뀔 수 있는 sigma-layer 가

```text
{0,1,2,3,r-1,r,r+1,t}
```

에만 국한된다는 점이다.
이로부터 class-by-class top-row transducer law 가 나온다.

이 부분은 사실상 proof-order 로 올라갔다.
근거 노트:
- `d5_toprow_t_nonzero_transducer_proof_packet_2026-03-26.md`

## 3.2 top-row single-anomaly acyclicity lemma
transducer 가

```text
(w,c) -> (w+s, c+u-1[w=w_*])
```

꼴로 떨어질 때, active/inactive coset 분리를 써서 여러 class 의 top acyclicity 를 손으로 증명했다.
이로부터 다음이 proof-order 로 올라갔다.

- `t=1`: top-acyclic
- `t=r`: 실제 entry regime 에서 top-acyclic
- `t=r-1`: `5∤m` 이면 top-acyclic, `5|m` 이면 trapped cycle
- generic late: 실제 entry regime 에서 `5∤m` 이면 top-acyclic, `5|m` 이면 trapped cycle

즉 `5|m` / `5∤m` arithmetic split 이 단순 계산 현상이 아니라 구조적 경계임이 드러났다.

근거 노트:
- `d5_single_anomaly_transducer_proof_packet_2026-03-26.md`

## 3.3 `t=0` top-row early cascade law
`t=0` 은 원래 예외처럼 보였지만, 실제로는 가장 짧게 설명되는 class 였다.
`A_{0,3}` 는 sigma `0` 에서 즉시 작동하고, top row 의 모든 state 를 한 block 뒤

```text
d' ∈ {0,1}
```

로 떨어뜨린다.
즉 top row 에는 한 block 후 아무 state 도 남지 않는다.

이 law 는 explicit compact formula 로 정리되었고, proof packet 으로 올렸다.

근거 노트:
- `d5_t0_toprow_early_cascade_proof_packet_2026-03-26.md`

## 3.4 `t=0` global compact law
더 중요한 후속 정리는 다음이다.

```text
R_0 = E   on {d=m-1},
R_0 = R_* on {d<m-1}.
```

즉 `t=0` 의 extra row 는 한 section block 의 맨 처음 sigma `0` 에서만 보이고,
그때 시작점이 top row 가 아니면 block 전체에서 extra row 가 다시 작동하지 않는다.
따라서 `t=0` 은

```text
explicit top reset + control continuation
```

으로 완전히 분해된다.
이로써 `t=0` local gap 은 사실상 사라졌다.

근거 노트:
- `d5_t0_global_compact_law_completion_note_2026-03-26.md`
- `d5_t0_compact_completion_by_control_excursion_note_2026-03-26.md`

---

## 4. exact-check 로 매우 강하게 지지되지만, 아직 손증명이 덜 적힌 부분

여기가 지금 가장 조심해서 구분해야 할 부분이다.

## 4.1 universal bulk cocycle
lower bulk 의 section return 이 `t` 와 무관한 universal cocycle 로 떨어진다는 점은
강한 exact-check 로 뒷받침된다.
하지만 현재 상태는 아직 “검증 완료 + 손증명 skeleton 필요” 쪽에 가깝다.

## 4.2 hinge conveyor (`d=m-2` row)
`d=m-2` row 의 대부분이 universal conveyor 로 움직이고,
corner 로만 정보가 집약된다는 것도 exact-check 가 매우 강하다.
그러나 이 part 는 아직 top-row 쪽만큼 proof-order 로 정리되지는 않았다.

## 4.3 corner burst law
corner `K_m={c=d=m-2}` 에서 `t` 가 6 class 로만 갈리고,
거의 affine branch + single anomaly graph 하나로 압축된다는 사실도 강하게 지지된다.
다만 이 역시 아직 손증명 정리본이 필요하다.

## 4.4 double-top / `Omega_m` symbolic law
`Omega_m` five-class atlas 는 지금 프로그램에서 가장 중요한 local symbolic law 중 하나다.

- instant exit
- quarter-retention
- half-retention
- invariant wall

의 다섯 class 가 residue 계산으로 깔끔하게 나오고,
exact data 와 잘 맞는다.
하지만 이 part 는 현재 “proof attempt + exhaustive / representative checks” 상태다.
완전한 손증명 패킷은 아직 아니다.

근거 노트:
- `d5_symbolic_doubletop_atlas_proof_attempt_2026-03-26.md`
- `d5_hinge_corner_symbolic_reduction_note_2026-03-26.md`
- `d5_global_glue_symbolic_reduction_and_prime_d_template_2026-03-26.md`

---

## 5. existence/frontier 쪽에서 이미 확보한 것

## 5.1 exact success / staged witness 들
exact replay 를 통해, one-line splicer 들이 실제로 작동하는 사례를 다수 확보했다.
특히 pure color-1 section program 에서 중요한 selected witnesses 는 다음과 같다.

- `(m,t) = (21,9)`
- `(27,1)`
- `(33,4)`
- `(33,14)`
- `(39,1)`
- `(51,4)`
- `(51,28)`

이 계열은 적어도 current section-level program 에서

- `H_m` single-cycle,
- `B_m` single-cycle,
- `Omega` leak,
- section exactness

과 잘 맞는다.

다만 여기서 주의할 점은,
이건 어디까지나 **pure color-1 / section program**의 success 패키지이지,
full all-color decomposition 전체를 한 번에 다 닫았다는 뜻은 아니다.

## 5.2 splice-only 와 leak-only 의 실패 법칙
반례도 구조를 분명하게 해 주었다.

- splice 는 되지만 leak 이 안 되면 defect 는 정확히 `Omega_m` 에서만 남는다.
- leak 는 되지만 splice 가 안 되면 exactness 는 나오지 않는다.
- 어떤 경우는 `H -> B` visibility 자체가 깨진다.

즉 “`Omega + B`면 끝”이 아니라,
정확히는

```text
Omega leak + B single-cycle + H->B visibility
```

가 본질이라는 점이 더 선명해졌다.

---

## 6. 현재 남아 있는 진짜 병목

지금 남은 문제는 예전처럼 state space 전체가 아니라, 꽤 좁다.

## 6.1 local symbolic law 쪽에서 남은 것
1. universal bulk cocycle 의 손증명
2. hinge conveyor / corner burst 의 손증명
3. double-top / `Omega_m` atlas 의 완전 손증명

이 세 가지는 모두 local symbolic reduction 의 완성에 해당한다.
즉 “새로운 패턴을 찾는 탐색”이 아니라 “이미 압축된 law 를 정리로 올리는 작업”이다.

## 6.2 global glue 쪽에서 남은 것
진짜 핵심 open bottleneck 은 여전히 다음 두 개다.

1. `H_m -> B_m` visibility theorem
2. resonant `m` 에서 `B_m` single-cycle witness 의 existence theorem

지금까지의 정리는 global glue 를 설명 가능한 finite machine 으로 줄여 주었지만,
최종 existence theorem 을 얻으려면 결국 여기서 승부를 봐야 한다.

---

## 7. 현재 접근법이 왜 합당한가

지금 프로그램의 합당성은 다음 이유로 강해졌다.

### 7.1 state space 를 실제로 압축했다
단순히 계산을 많이 돌린 것이 아니라,

- bulk 는 universal,
- hinge 는 conveyor,
- corner 는 single burst,
- top row 는 single-anomaly transducer,
- pure color-1 exactness 는 leak/splice/visibility,

라는 식으로 문제의 자유도를 실제로 낮췄다.

### 7.2 실패도 구조를 드러낸다
실패 사례가 무작위 residual 이 아니고,

- `Omega_m` trapped pocket,
- missing visibility,
- multi-cycle base map,

같은 작은 obstruction 으로 정리된다.
이건 existence theorem 으로 가는 데 매우 좋은 신호다.

### 7.3 `d=prime` 일반화 방향이 보인다
아직 `d=prime` 일반화는 정리 상태가 아니지만, architecture 는 상당히 선명하다.

```text
support localization
+ universal bulk
+ finite top atlas
+ base splice/visibility
```

이 네 층 구조는 `d=5` 전용 계산을 넘어서는 틀이다.
즉 지금 작업은 단순히 하나의 작은 케이스를 푸는 것이 아니라,
prime degree 전체에 쓰일 template 을 조립하는 과정으로 읽힌다.

---

## 8. 가장 자연스러운 다음 순서

지금 시점에서 다음 순서는 탐색보다 증명 쪽이 맞다.
우선순위는 다음처럼 보인다.

### 8.1 local symbolic law 완성
가장 먼저는 이미 압축된 local law 들을 theorem-order 로 끌어올린다.
특히

1. `Omega_m` double-top law
2. hinge conveyor
3. corner burst
4. universal bulk cocycle

를 차례로 손증명 쪽으로 정리하는 것이 깔끔하다.

### 8.2 global glue theorem
그 다음은

```text
Omega leak + B single-cycle + H->B visibility
=> pure color-1 section exactness
```

를 명확한 정리 문장으로 쓰는 것이다.
proof skeleton 은 이미 있고, 남은 것은 visibility 쪽이다.

### 8.3 existence theorem 으로 복귀
마지막으로 splice witness 존재성과 visibility 를 결합해,
공명 `3|m` 에 대한 pure color-1 existence theorem 을 노린다.
그리고 그 뒤 staged repair 를 통해 full decomposition 으로 복귀한다.

---

## 9. 한 줄 요약

지금까지의 가장 중요한 진전은 이것이다.

> `d=5` 공명 존재성 문제는 더 이상 “복잡한 전역 패턴 찾기”가 아니라,
> **작은 symbolic machine 몇 개의 손증명**과
> **base splice / visibility existence** 문제로 줄었다.

즉 local 쪽은 이미 상당히 압축되었고,
남은 진짜 난점은 global base architecture 쪽이다.
