# P-NP 인터페이스 프로그램: SDD 비교 정리의 정리형

## 0. 목적

이 문서는 다음 질문을 좁혀 닫는다.

> 고정 vtree `T` 아래 canonical SDD library 비용과,
> exact cut relation `M_b^f`에서 나오는 **순수 semantic 비용** 사이에
> 어떤 비교 정리가 실제로 증명되는가?

핵심 결론은 다음이다.

- `canonical minimal library`는 순수 의미론에서 generally 성립하지 않는다.
- 그러나 **minimal universal disjoint library size**는 순수 의미론에서 잘 정의된다.
- 그리고 canonical compressed/trimmed SDD library는 그 semantic 최솟값의 **실현 가능한 상계**가 된다.
- 따라서 SDD 크기는 이 semantic 최솟값들의 합보다 항상 크다.

즉, `exact operator theorem`과 `pure semantic floor`를 연결하는 **안전한 comparison lemma**가 있다.

---

## 1. cut relation과 shell row family

함수

\[
f : \{0,1\}^X \to \{0,1\}
\]

와 vtree `T`를 고정하자.
내부 노드 `b`를 잡고

- `B := Vars(b)`
- `A := X \setminus B` (여기서는 shell context 쪽)

로 둔다.

각 shell restriction

\[
\rho : A \to \{0,1\}
\]

에 대해 `B`-row를

\[
S_\rho := \{\phi \in \{0,1\}^B : f(\rho,\phi)=1\}
\]

로 둔다.

이 family

\[
\mathcal R_T(f,b) := \{S_\rho : \rho \text{ is a shell restriction wrt } b\}
\]

이 support `b`에서의 **semantic cut family**다.

이 row family는 exact cut relation

\[
M_b^f(\rho,\phi)=f(\rho,\phi)
\]

의 Bob-side row family와 같다.

---

## 2. 순수 semantic 비용: minimal universal disjoint library size

`B` 위의 부분집합 family

\[
U \subseteq 2^{\{0,1\}^B}
\]

가 `\mathcal R_T(f,b)`의 **universal disjoint library**라는 것은,
각 shell restriction `\rho`에 대해 어떤 부분가족 `U_\rho \subseteq U`가 존재해서

\[
S_\rho = \bigcup U_\rho
\]

이고, `U_\rho`의 원소들이 pairwise disjoint인 것을 뜻한다.

그 최소 크기를

\[
\lambda_T^{\sqcup}(f,b)
:=
\min\{|U| : U \text{ is a universal disjoint library for } \mathcal R_T(f,b)\}
\]

로 둔다.

### 관찰 2.1

`\lambda_T^{\sqcup}(f,b)`는 항상 well-defined다.

**이유.** row family 자체 `\mathcal R_T(f,b)`를 그대로 `U`로 택하면 된다.
각 row는 자기 자신 하나의 singleton subfamily로 표현된다.

### 관찰 2.2

`\lambda_T^{\sqcup}(f,b)`는 **순수 semantic quantity**다.
representation class, compression rule, canonicity를 전혀 쓰지 않는다.

### 관찰 2.3

이 quantity는 atomization보다 약하다.
즉 common refinement의 atom 수보다 작을 수 있다.
그래서 이 값은 “semantic floor”에 더 가깝다.

---

## 3. canonical SDD library

이제 `\alpha_T(f)`를 `f`의 고정 vtree `T`에 대한 compressed and trimmed SDD라고 하자.

내부 노드 `b`에 대해,

\[
\mathcal L_T^{\mathrm{SDD}}(f,b)
\]

를 `b`를 respect하는 decomposition sub-SDD들이 계산하는 **서로 다른 Boolean 함수들**의 집합으로 둔다.

이 library는 class-selected canonical object다.
즉,

- 고정 vtree `T`에서 compressed/trimmed canonicity로 잘 정의되고,
- shell restriction 아래에서도 support-`b` residual을 disjoint subfamily union으로 exact하게 덮는다.

이전 정리에서 이미 확보한 사실은 다음이다.

### SDD-Op

고정 `T,f,b`에 대해

1. `\mathcal L_T^{\mathrm{SDD}}(f,b)`는 well-defined이고,
2. 각 shell restriction `\rho`에 대해
   
   \[
   S_\rho = \bigcup U_\rho
   \]
   
   인 어떤 `U_\rho \subseteq \mathcal L_T^{\mathrm{SDD}}(f,b)`가 존재하며,
   그 원소들은 pairwise disjoint이고,
3. support-`b` decomposition node 수 `N_{\alpha_T(f)}(b)`와 정확히 같은 크기를 갖는다:
   
   \[
   N_{\alpha_T(f)}(b)=\bigl|\mathcal L_T^{\mathrm{SDD}}(f,b)\bigr|.
   \]

---

## 4. 비교 정리: semantic floor <= canonical SDD library

이제 가장 안전한 comparison lemma가 바로 나온다.

### 정리 SDD-Cmp

모든 `f,T,b`에 대해

\[
\lambda_T^{\sqcup}(f,b)
\le
\bigl|\mathcal L_T^{\mathrm{SDD}}(f,b)\bigr|
=
N_{\alpha_T(f)}(b).
\]

#### 증명

`\mathcal L_T^{\mathrm{SDD}}(f,b)`는 SDD-Op에 의해 `\mathcal R_T(f,b)`의 universal disjoint library다.
따라서 `\lambda_T^{\sqcup}(f,b)`의 최소성으로

\[
\lambda_T^{\sqcup}(f,b)
\le
\bigl|\mathcal L_T^{\mathrm{SDD}}(f,b)\bigr|.
\]

또한 SDD-Op에서

\[
\bigl|\mathcal L_T^{\mathrm{SDD}}(f,b)\bigr|=N_{\alpha_T(f)}(b)
\]

이므로 결론이 따른다. ∎

---

## 5. 전역 따름정리

support charge가 vtree 내부 노드마다 유일하게 주어지므로,
정리 SDD-Cmp를 합산하면

### 따름정리 SDD-Floor

\[
|\alpha_T(f)|
\ge
\sum_{b\in \mathrm{Int}(T)} \lambda_T^{\sqcup}(f,b).
\]

이건 SDD의 canonical operator theorem과 exact cut relation의 **순수 semantic floor**를 잇는 정리다.

---

## 6. 왜 이게 현재 기준 가장 강한 안전한 비교문장인가

더 강한 문장

\[
\lambda_T^{\sqcup}(f,b)
=
\bigl|\mathcal L_T^{\mathrm{SDD}}(f,b)\bigr|
\]

이나

> “minimal universal disjoint library가 semantic data만으로 canonical하게 정해진다”

는 일반적으로 기대하면 안 된다.

이유는 두 가지다.

1. 순수 semantic 층에서는 minimizer가 여러 개일 수 있다.
2. 따라서 canonicality는 semantic optimization이 아니라, class-internal compression discipline에서 나온다.

즉 SDD가 주는 것은

- `minimum theorem`이 아니라
- `canonical feasible theorem`

이다.

그런데 lower bound에는 이것으로 충분하다.
왜냐하면 canonical library가 feasible하기만 하면 그 크기는 언제나 semantic minimum의 상계가 되고,
operator theorem이 그 canonical library 크기를 실제 node mass와 연결해 주기 때문이다.

---

## 7. 현재 위치

이제 SDD 쪽에는 다음 세 층이 분리되었다.

1. **semantic floor**
   - `\lambda_T^{\sqcup}(f,b)`
   - representation-independent

2. **canonical operator cost**
   - `|\mathcal L_T^{\mathrm{SDD}}(f,b)|`
   - class-selected, fixed-vtree canonical

3. **representation size**
   - `|\alpha_T(f)|`

그리고 지금 닫힌 비교는

\[
\text{semantic floor}
\le
\text{canonical operator cost}
\le
\text{representation size (summed over supports)}.
\]

이 사슬이다.

---

## 8. 남은 질문

1. `\lambda_T^{\sqcup}(f,b)`가 communication complexity나 다른 cut invariant와 어떻게 직접 연결되는가?
2. AOMDD에서도 같은 꼴의 `semantic floor <= canonical operator cost <= size`가 닫히는가?
3. structured d-DNNF의 자연스러운 subclass 중에서, SDD와 같은 operator-ready canonical floor theorem이 살아나는 것이 있는가?

이 세 질문이 다음 단계다.
