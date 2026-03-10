# d=4 증명 접근법 요약 — d=5를 위한 참조 문서

## 핵심 구조: 3단계 환원

```
D₄(m) 전체 (m⁴ vertices)
  ↓  f_c^m (layer return)
P₀ = {S=0} (m³ vertices, 3D)
  ↓  R_c^m (q-return)
Q = {S=0, q=m-1} (m² vertices, 2D)
  ↓  affine conjugacy
O(u,v) = (u+1, v+1_{u=0})  ← 표준 odometer, 단일 m²-cycle
```

**원리**: 매 단계에서 1차원씩 줄여서, 최종적으로 2D odometer의 단일순환성으로 환원.

---

## Witness 설계 ("무엇을 건드렸나")

| Layer | 규칙 | 역할 |
|---|---|---|
| S ≥ 3 | canonical (0,1,2,3) | 아무것도 안 함 |
| S = 1 | canonical (0,1,2,3) | 아무것도 안 함 |
| S = 0, q ≠ 0 | (1,0,3,2) | 색 쌍 {0↔1}, {2↔3} swap |
| S = 0, q = 0 | (3,2,1,0) | 완전 역순 |
| S = 2, q = 0 | canonical + 2개 swap | 핵심 gate ← **여기가 전부** |

Layer 2의 gate 규칙:
- x₀ = 0이면 slots 1↔3 swap (color 1 → e₃, color 3 → e₁)
- x₃ = 0이면 slots 0↔2 swap (color 0 → e₂, color 2 → e₀)
- 두 swap은 disjoint → commute

**설계 원리**: 각 color c에 대해 "coordinate x_c를 바꾸지 않는" 불변량이 있으므로, 그 불변량을 깨는 예외 방향 e_{c+2}를 주입해야 함. Gate의 역할은 정확히 이것.

---

## 왜 이게 작동하는가 (증명 골격)

### Step 1: First return R_c

모든 color step이 S를 +1 → m번 돌아야 P₀ 복귀.
중간에 layer 2를 지나면서 gate가 **딱 한 번** 발화할 수 있음 (q=m-1일 때만).

→ R_c는 3-branch piecewise affine:
- q=0 branch (layer-0 defect)
- q=m-1 + gate condition (layer-2 defect)  
- otherwise (bulk: 단순 translation)

### Step 2: Second return T_c

R_c가 q를 매번 ±1 변화 → m번 적용하면 Q로 복귀.
m번의 R_c 중 defect branch는 딱 2번 (q=0, q=m-1 각 1번).

→ T_c(a,b) = (a ± 1_{조건}, b ± 1)  형태, 조건은 **단 하나의 affine line** 위에서만 달라짐.

### Step 3: Odometer conjugacy

T_c가 "거의 translation + 1개 line에서만 carry" → 표준 odometer O(u,v) = (u+1, v+1_{u=0})에 affinely conjugate.

O가 단일 m²-cycle임은 3줄 증명:
- O^m(u,v) = (u, v+1)
- O^{m²} = id
- 최소주기 = m² (q-좌표 복귀 + v-좌표 복귀)

### Step 4: Lifting (v3에서 수정됨)

Q → P₀: "R_c^t(x)=x이면 t는 m의 배수 (q-복귀), 그러면 T_c^{t/m}(x)=x이므로 t/m은 m²의 배수 → t = m³k"
P₀ → V: 동일 패턴으로 t = m⁴k

---

## d=5 적용 시 예상되는 변화

| d=4 | d=5 (예상) |
|---|---|
| P₀ = 3D (m³) | P₀ = 4D (m⁴) |
| Q = 2D (m²) | Q = 3D (m³) |
| T_c = 2D odometer | T_c = 3D map → **Q' = 2D로 한 번 더 환원 필요** |
| 2-level return | **3-level return** |
| 2개 swap으로 4색 분배 | 5색, (2+2)+1 분배? |
| Parity obstruction 없음 | d=5는 odd d → **even m에서 obstruction 가능** |

### 탐색 순서 제안

1. Affine-split baseline 설정 → 불변량 확인 (어떤 좌표가 보존되는지)
2. Single-color hyperplane carry 실험 (d=4의 Attempt B와 동일)
3. 5-color compatibility 탐색 (SAT/CP-SAT)
4. Nested return map 추출 (P₀ → Q → Q' → odometer?)
5. Even m에서 obstruction 유무 확인

---

## Codex job 설계 패턴 (d=4에서 실제로 한 것)

```
Job 1: "이 baseline이 왜 실패하는지?" → 불변량/cylinder 구조 확인
Job 2: "single-color fix는?" → hyperplane carry → works but incompatible
Job 3: "finite compatibility table?" → SAT search on small m
Job 4: "gate classification?" → reduced family enumeration
Job 5: "found candidate → proof?" → return map → odometer → done
```
