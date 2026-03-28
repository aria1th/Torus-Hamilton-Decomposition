# d=5 존재성 관점 심화 노트: base-splicer / capture / cleanup 분해 (2026-03-25)

## 0. 이번 패스의 목표와 범위

이번 패스의 목표는 이전 노트의 `existence-first` 관점을 더 밀어붙이는 것이었다.
특히 공명 `3|m` 전선에서,

- 정확한 성공 패턴을 분류하려 하기보다,
- **무엇을 존재성 정리의 핵심 변수로 삼아야 하는지**를 더 잘 분해하고,
- 그 분해를 지지하는 새 exact 계산을 조금 더 확보하는 것

이 목표였다.

이번 노트에서 새로 한 일은 두 가지다.

1. 이미 알려진 exact success package 들에 대해, color-1 유도 단면
   
   - `H_m = {Sigma=0, c=0, d=0}`,
   - `B_m = {Sigma=0, c=0, d=0, e=0}`
   
   위의 induced map 을 다시 계산해 보았다.
2. promoted-collar control family 위에 **한 줄짜리 `A_{t,3}` splicer** 를 올린 selected probe 들을 exact replay 로 계산해 보았다.

중요한 점은, 아래의 새 결과들은

- bundle 안에 이미 theorem-order 로 정리된 진술과,
- 이번 패스에서 내가 exact replay 로 직접 확인한 selected probe

를 분명히 구분해서 적는다는 것이다.

---

## 1. 이번 패스에서 더 선명해진 구조: 남은 문제는 하나가 아니라 셋이다

이전 노트에서는 pure color-1 전선이 local transducer 문제를 넘어
`H_m` / `B_m` 위의 induced map 문제로 압축된다는 점을 강조했다.
이번 패스에서는 거기서 한 단계 더 나간 분해가 보였다.

현재 공명 `d=5` 존재성 문제는 실제로는 다음 세 층으로 갈라진다.

### 1.1. upper-to-base capture

모든 color-1 orbit 가 정말로 lower strip / base section
`H_m = {c=0,d=0}`
에 들어오는가?

이것이 실패하면, `H_m` 위 induced map 이 아무리 좋아도 global Hamiltonicity 는 나오지 않는다.

### 1.2. base splicing on `H_m` / `B_m`

`H_m`에 들어온 뒤 induced return 이 single cycle 이 되는가?
더 작게는 `B_m` 위 next-return permutation 이 cycle 들을 하나로 합치는가?

현재 pure color-1 전선에서 가장 압축된 obstruction 은 여기 있다.

### 1.3. collateral cleanup

color 1 을 닫은 뒤 color 0,2 가 남는가?
남는다면 color-1-invisible channel 로 그것을 정리할 수 있는가?

즉 existence-only 목표는

> “처음부터 all-color exact family 를 닫힌 식으로 분류한다”

가 아니라,

> “capture / base-splice / collateral-cleanup 의 세 단계를 각각 finite-state existence 문제로 분리한다”

가 되어야 한다.

이번 exact probe 들은 바로 이 3-way split 을 강하게 지지한다.

---

## 2. 정의: 이번 패스에서 본 control family 와 reduced sections

### 2.1. promoted-plus control family

이번 probe 는 아래 promoted-collar control 에서 시작했다.

```text
P_m^+
= {
    A_{1,4}, C_{r,4}, A_{1,3}, C_{3,3},
    C_{r-1,3}, A_{r,3}, C_{r+1,3}, A_{r+1,3}
  },
r=(m-1)/2.
```

이것은 width-3 canonical collar 에 same-row `A` 를 한쪽 collar row `r+1`에만 더한 family 이다.

그 위에 one-line splicer 를 하나 더 붙인 family 를

```text
P_m^+(t) := P_m^+ ∪ {A_{t,3}}
```

로 적겠다.

### 2.2. reduced sections

color 1의 `m`-block return

```text
R = h_1^m |_{Sigma=0}
```

에 대해,

- `H_m = {c=0,d=0}` 위 induced map `F_m : H_m -> H_m`,
- `B_m = {c=0,d=0,e=0}` 위 next-return permutation `P_m : B_m -> B_m`

을 본다.

여기서

- `H_m` single cycle = cycle type `[m^2]`,
- `B_m` single cycle = cycle type `[m]`

를 의미한다.

---

## 3. 새 exact 결과 A: 이미 알려진 exact success packages 는 모두 `H_m` / `B_m` 에서 단일 cycle 이다

casebook 에 이미 기록된 exact success packages

- `m=21`,
- `m=27`,
- `m=33`,
- `m=39`

에 대해 induced maps 를 다시 계산했다.

결과:

| modulus | exact success package 존재 | `H_m` cycle type | `B_m` cycle type |
|---|---:|---:|---:|
| `21` | yes | `[441]` | `[21]` |
| `27` | yes | `[729]` | `[27]` |
| `33` | yes | `[1089]` | `[33]` |
| `39` | yes | `[1521]` | `[39]` |

즉 최소한 checked exact success 들에서는

> global color-1 success가 나올 때 `H_m` / `B_m` induced map 도 이미 단일 cycle

이라는 패턴이 관찰된다.

이것은 “pure color-1 존재성 문제의 핵심이 base permutation splicing 이다”라는 해석을 강하게 지지한다.

다만 아래 §5에서 보듯이, 역은 아직 거짓일 수 있다. 즉 `H_m` / `B_m` 가 single cycle 이라고 해서 자동으로 global color-1 Hamiltonicity 가 나오지는 않는다.

---

## 4. 새 exact 결과 B: one-line `A_{t,3}` splicer 만으로도 `H_m` / `B_m` obstruction 이 자주 무너진다

이제 promoted-plus control `P_m^+` 위에 selected `A_{t,3}` 한 줄을 더 올려 보았다.

### 4.1. control data

bundle 에 이미 기록된 promoted-collar control 의 reduced cycle types 는 다음과 같다.

| modulus | control `F_m` on `H_m` | control `P_m` on `B_m` |
|---|---:|---:|
| `21` | `[220,126,95]` | `[11,5,5]` |
| `27` | `[343,342,44]` | `[13,12,2]` |
| `33` | `[538,423,128]` | `[17,11,5]` |
| `39` | `[412,356,333,309,111]` | `[10,9,9,8,3]` |

즉 control family 는 명백히 multi-cycle 이다.

### 4.2. selected splicer probes

아래는 이번 패스에서 exact 로 계산한 selected splicer probe 들이다.

| modulus | probe family | `H_m` cycle type | `B_m` cycle type | full orbit lengths `[l0,l1,l2]` | 해석 |
|---|---|---:|---:|---:|---|
| `21` | `P_21^+ + A_{9,3}` | `[441]` | `[21]` | `[21^5,21^5,21^5]` | one-line splicer 만으로 exact all-color success |
| `21` | `P_21^+ + A_{11,3}` | `[441]` | `[21]` | `[4084101,4079985,4084101]` | base-splice 는 됐지만 color-1 global capture 가 아직 완전히 안 닫힘 |
| `27` | `P_27^+ + A_{1,3}` | `[729]` | `[27]` | `[3869424,27^5,27^5]` | color 1,2 는 닫히고 color 0만 남음 |
| `33` | `P_33^+ + A_{4,3}` | `[1089]` | `[33]` | `[31754283,33^5,33^5]` | color 1,2 는 닫히고 color 0만 남음 |
| `33` | `P_33^+ + A_{14,3}` | `[1089]` | `[33]` | `[31754283,33^5,33^5]` | 위와 같은 성질의 symmetric witness |
| `39` | `P_39^+ + A_{1,3}` | `[1521]` | `[39]` | `[33321990,39^5,39^5]` | color 1,2 는 닫히고 color 0만 남음 |
| `39` | `P_39^+ + A_{3,3}` | `[1521]` | `[39]` | `[33321990,90197835,39^5]` | base-splice 는 됐지만 color-1 capture defect 와 color-0 defect 가 함께 남음 |

몇 가지 load-bearing observation:

1. **control family 는 multi-cycle 인데, one-line `A_{t,3}` 만으로 `H_m` / `B_m` 가 single cycle 로 바뀌는 경우가 실제로 존재한다.**
2. 그 변화는 단지 reduced section 에만 있는 가짜 변화가 아니다. 실제로 `m=21,27,33,39`에서 color 1 orbit length 가 크게 개선되고, 여러 probe 에서는 exact full length `m^5` 에 도달한다.
3. 다만 **`H_m` / `B_m` single cycle 이 global color-1 success의 충분조건은 아니다.**
   - `m=21`, `P_21^+ + A_{11,3}`는 `H_m` / `B_m` 가 모두 single cycle 이지만 color 1 orbit length는 `4079985 < 21^5` 이다.
   - deficiency는 `4116`으로 작지만 0은 아니다.
4. 반대로 `m=27,33,39`의 best one-line splicer 들은 **color 1,2 를 닫고 color 0만 남기는 staged near-success** 를 준다.

즉 `base-splice`와 `global capture`, 그리고 `collateral cleanup` 이 서로 다른 obstruction 이라는 점이 exact data 로 분리된다.

---

## 5. 이번 패스에서 얻은 가장 중요한 개념적 결론

### 5.1. `B_m` single-cycle 은 핵심이지만, 단독으로는 아직 부족하다

이전 노트에서는 pure color-1 전선의 핵심을 `B_m` 위의 base permutation 으로 읽자고 제안했다.
이번 패스는 그 해석을 더 sharpen 했다.

정확히는,

- `B_m` / `H_m` single-cycle 은 정말 load-bearing invariant 이고,
- known success 들은 모두 이것을 만족하지만,
- 그것만으로는 아직 global success 를 보장하지 않는다.

따라서 pure color-1 존재성 정리는 아래처럼 읽는 것이 맞다.

> **(capture theorem)** 모든 orbit 가 base section `H_m` 으로 들어온다.
>
> **(base-splice theorem)** induced map on `H_m` (또는 충분한 경우 `B_m`) 가 single cycle 이다.

즉 `base permutation` 은 마지막 장애물의 핵심이지만, 그 전 단계인 `upper-to-base capture` 를 별도 theorem 으로 분리해야 한다.

### 5.2. color-1 splicing 과 color-0 cleanup 도 분리된다

`m=27,33,39` probe 에서 보듯,

- one-line `A_{t,3}` splicer 가 `H_m` / `B_m` 를 single cycle 로 만들고,
- color 1과 color 2를 exact Hamilton 으로 닫은 뒤,
- color 0만 남기는 경우

가 실제로 나타난다.

따라서 all-color existence 를 위해서는 마지막으로

> **(cleanup theorem)** color-1-invisible 혹은 stage-compatible channel 로 남은 color 0 defect 를 지운다

를 분리해야 한다.

이 관점에서는 정확한 성공 package 분류보다 다음 정리 구조가 훨씬 더 자연스럽다.

---

## 6. d=5에 대한 existence theorem skeleton (새 버전)

이제 `d=5` 공명 구간에 대한 존재성 목표를 아래처럼 적는 것이 맞다고 본다.

### Theorem skeleton A: target-color capture + splicing

모든 odd resonant `m >= 15`, `3|m` 에 대해, 적절한 bounded-support color-1-visible family `S_m` 가 존재하여

1. color-1 orbit 들이 모두 finite upper defect 를 지나 base section `H_m` 으로 들어오고,
2. induced return `F_m : H_m -> H_m` 가 single cycle 이다.

이 정리는 exact pattern classification 을 요구하지 않는다.
필요한 것은 “어떤 bounded atlas 안에서 적어도 하나의 splicer 가 존재한다”는 것뿐이다.

### Theorem skeleton B: collateral cleanup

위 `S_m` 를 보존하는 color-1-invisible 또는 stage-compatible repair `C_m` 가 존재하여,

- color 0 defect 를 지우고,
- 필요한 경우 color 2 collateral 도 함께 정리하며,
- color 1 Hamiltonicity 는 깨지지 않는다.

### Combined existence statement

그러면 `S_m ∪ C_m` 가 residual colors `0,1,2` 를 모두 Hamilton 으로 만들고,
closed backbone colors `3,4` 와 합쳐 `d=5` residual assembly existence 가 성립한다.

이 formulation 의 장점은,

- exact universal pattern 을 요구하지 않고,
- local transducer, base permutation, cleanup channel 을 각각 finite-state existence 로 떼어낼 수 있다는 점이다.

---

## 7. 이번 exact probe 가 이 theorem skeleton 을 어떻게 지지하는가

이번 probe 들은 위 정리 구조를 거의 직접적으로 뒷받침한다.

### 7.1. Stage A = splicer existence 는 실제로 보인다

selected one-line probe 만으로도

- `m=21,27,33,39`에서 `H_m` / `B_m` single-cycle witness 가 실제로 발견되었다.

즉 “next repair 는 induced base permutation 을 실제로 바꿔야 한다”는 compute memo 의 방향은 단순 heuristic 이 아니라 실제 exact witness 를 갖는다.

### 7.2. Stage A 는 다시 capture와 splice로 쪼개진다

`m=21`, `P_21^+ + A_{11,3}`가 보여주듯,

- `H_m` / `B_m` single-cycle,
- colors 0,2 full,
- color 1만 very small defect

라는 상황이 가능하다.

따라서 pure color-1 theorem 안에서도

- base-splice,
- global capture

를 분리해서 증명하는 것이 자연스럽다.

### 7.3. Stage B = cleanup 도 실제로 분리된다

`m=27,33,39`의 best probe 들은

- color 1,2 full,
- color 0 only defect

형태다.

즉 color-1 splicing 이후 남는 마지막 문제는 color 0 cleanup 으로 isolated 된다.

---

## 8. d = prime 일반화에 대한 실제로 쓸 만한 메시지

여기서부터는 theorem 이 아니라 **방법론적 template** 이다. 아직 증명은 아니다.

그래도 이번 `d=5` 데이터는 `d=prime` 존재성 목표를 다음 방향으로 읽게 만든다.

### 8.1. exact pattern classification 을 포기하고 quotient-visible atlas 로 간다

`d=5`에서는 fixed-color quotient / visibility law 덕분에

- target color에 보이는 row class,
- target color에 안 보이는 row class

를 분리할 수 있었다.

`d=prime`에서도 진짜 필요한 것은 explicit global family 분류가 아니라,

> target color를 splice할 visible class 하나와,
> collateral을 정리할 invisible class 몇 개가 bounded atlas 안에 존재한다

는 식의 정리일 가능성이 크다.

### 8.2. general prime-`d` proof program 은 세 단계여야 한다

`d=5`에서 본 분해를 일반 prime `d`에 옮기면, 가장 자연한 proof program 은 아래 구조다.

1. **local audit / finite-burst theorem**
   - upper active episodes 가 finite 이고,
   - dynamics 가 lower finite-band automaton 으로 내려간다.
2. **base-section capture + splicing theorem**
   - target color orbit 가 base section 으로 들어오고,
   - induced base map / gate graph 가 single component 가 된다.
3. **collateral cleanup theorem**
   - target-color-invisible channel 로 다른 colors 를 정리한다.

이 구조는 explicit family 분류보다 훨씬 약하고, 따라서 existence proof 와 더 잘 맞는다.

### 8.3. 무엇이 아직 미증명인가

`d=prime` 일반화에 대해서는 아직 아래가 전부 open 이다.

- `d=5`에서의 exact quotient-visible algebra 가 어떤 형태로 일반 prime `d`에 올라가는지,
- `H_m`, `B_m`의 올바른 high-`d` analogue 가 무엇인지,
- congruence data 가 `m mod 24` 같은 작은 주소계로 다시 압축되는지.

따라서 지금 말할 수 있는 것은 theorem 이 아니라 **proof architecture** 뿐이다.

하지만 존재성 목표에는 그 architecture 가 이미 충분히 유력하다.

---

## 9. 이번 패스에서 얻은 가장 실전적인 연구 지시문

다음에 전선을 더 민다면, 가장 생산적인 질문은 더 이상

> “어떤 exact family 가 all-color Hamilton 인가?”

가 아니다.

지금 가장 중요한 질문은 셋이다.

1. **capture question**
   - `H_m` / `B_m` single-cycle candidate 에서,
   - 어떤 upper residual set 이 아직 `H_m`으로 내려오지 않는가?
2. **splicer question**
   - bounded atlas 안에서 `H_m` / `B_m` cycle count를 실제로 1로 만드는 visible row는 무엇인가?
3. **cleanup question**
   - color 1을 건드리지 않고 color 0 only defect 를 제거하는 invisible / stage-compatible row는 무엇인가?

즉 다음 research program 은 “exact successful package atlas 확장”이 아니라,

> **capture / splice / cleanup의 세 finite-state existence 문제를 따로 닫는 것**

이어야 한다.

---

## 10. honest status

이번 패스에서 실제로 확인한 범위는 아래까지다.

- casebook exact success packages `m=21,27,33,39`의 `H_m` / `B_m` single-cycle property: 직접 exact 계산으로 확인.
- promoted-plus control `P_m^+`에 대한 selected one-line `A_{t,3}` probe:
  - `m=21`: `t=9,11`
  - `m=27`: `t=1,12,14`
  - `m=33`: `t=4,14,3`
  - `m=39`: `t=1,3,18,20`
  중 핵심 witness 들을 직접 exact 계산으로 확인.

아직 하지 않은 것 / 아직 미확인인 것:

- 위 row sets 에 대한 exhaustive all-`t` classification for all tested moduli,
- `m>=45` 이후에서의 동일 splicer phenomenon의 체계적 atlas,
- `m=27,33,39`의 color-0 only defect 를 실제로 없애는 cleanup witness,
- `d=prime` 일반화의 exact theorem.

따라서 이번 노트의 정직한 결론은 다음이다.

> 공명 `d=5` 존재성 문제는 이제
> **(capture) + (base splice) + (cleanup)**
> 의 세 finite-state existence 문제로 읽는 것이 맞고,
> 이번 exact probe 는 이 세 단계가 실제로 분리된다는 점과,
> one-line splicer 만으로도 middle stage 를 상당 부분 실제로 해결할 수 있다는 점을 보여준다.

