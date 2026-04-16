# D5 Leanization Round 1 (2026-04-05)

## 이번 패스에서 실제로 한 일

이번 패스는 두 목표를 동시에 겨냥했다.

1. **Lean 구조 뼈대 준비**  
   정본 `RoundY`, 병행 `RouteY-Existence`, 그리고 4월 1 / 4 / 5 common-support 문서를 다시 훑어
   Lean 모듈 경계를 잡고 시작용 skeleton을 만들었다.

2. **현재 theorem의 상태 구분과 gap 적출**  
   각 패키지를 `promoted theorem / closed working block / checked exact / explicit local packet / open frontier`
   로 나누고, Lean으로 올릴 때 비어 있는 조각이 무엇인지 적었다.

이 패스에서 **재실행하지 않은 것**은 명확하다.

- Python check script 재실행
- TeX 전체 라인 대조
- 3월 역사 문서 전범위 재독
- Lean compile 검증

따라서 아래 결과는 **문서 읽기와 구조 분석에 근거한 leanization 설계 1차본**이다.

---

## 이번 패스의 핵심 판단

### 1. 바로 Lean으로 옮길 수 있는 축

가장 먼저 파일/정의/정리를 잡아도 되는 것은 아래 네 덩어리다.

1. `State5 / Sigma=0 / Visible4 / H_m / B_m` 같은 **핵심 객체 정의**
2. `RoundY`의 **이미 닫힌 theorem-level 패키지 인터페이스**
3. `d5_300`의 **`H_m` master hinge theorem**
4. common `m=15r+9`의 **stable packet exact classification**

이 네 개는 서로 잘 맞물린다.  
특히 `d5_300`과 common stable packet은 지금 시점에서도 “문서 상태가 충분히 선명한 정리”라서,
Lean에서 뼈대만이 아니라 실제 statement extraction까지 바로 들어갈 수 있다.

### 2. 먼저 정의를 갈라야 하는 곳

April 1 spine note가 경고하는 `R_re`와 `R_q`는 Lean에서 반드시 **별도 정의**여야 한다.

문서가 이미 말하듯, low branch에서는 이 둘이 같은 진술이 아니고,
여기를 흐리면 뒤의 low-branch/theorem-floor/common-branch 문장들이 잘못 동일시된다.
그래서 skeleton에서는 이 경계를 `Core/Interfaces.lean`으로 먼저 분리했다.

### 3. checked를 theorem처럼 axiomatize하면 안 되는 곳

다음은 현재 문서 상태상 **정리로 올리면 안 되고 certificate-first**로 다뤄야 한다.

- `d5_289`의 checked no-go cycle data
- `d5_297/298/299` late atlas / routing / first promotions
- common all-family channel quotient compression
- denominator-`16`의 `r ≡ 2,10 (mod 16)` interior finite table
- denominator-`8`의 `r=8s` checked portal packet
- denominator-`8`의 `r=8s+4` interior transport table 중 아직 남은 master-tape transport 부분

즉 Lean에서는 이 층을 “already proved theorem” namespace에 넣지 말고,
`Certificate`, `Table`, `CheckedWindow`, `FinitePacket` 류로 분리해 두는 편이 안전하다.

---

## 모듈 뼈대

이번 패스에서 만든 skeleton은 다음 구조다.

- `D5/Core/Objects.lean`  
  좌표계, `Sigma=0`, `Visible4`, `H_m`, `B_m`, common residue family 분기

- `D5/Core/Interfaces.lean`  
  `R_re`, `R_q`, `beta`, `betaTilde` 같은 인터페이스 이름과
  “두 return surface는 같지 않다”는 경계

- `D5/Canonical/*`  
  `RoundY`에서 theorem-level 또는 working-level로 닫힌 축

- `D5/Common/M15r9/*`  
  common theorem floor / stable packet / denominator-`16` / denominator-`8` / compression

- `D5/RouteYExistence/GenericLate.lean`  
  seam-surgery 병행 lane

이 구조의 의도는 한 가지다.

> **정의 계층**, **promoted theorem 계층**, **checked certificate 계층**, **open frontier 계층**을 파일 경계에서부터 분리한다.

이렇게 하지 않으면 이후 Lean proof import 단계에서
“이건 theorem인지, check report인지, 아직 frontier note인지”가 자꾸 섞인다.

---

## 지금 당장 proof import 우선순위

### A. 바로 statement extraction에 들어가도 되는 것

1. `RoundY` accepted odd-`m` backbone  
2. `RoundY` front-end `T0--T4`
3. `d5_286` finite `chi`-active episodes
4. `d5_300` `H_m` master hinge profile
5. `d5_common_beta_m_15r9_all_residue_families_full_stable_packet_and_exact_classification_2026-04-04`

이 다섯 개는 skeleton에서 **axiom/placeholder 이름을 이미 잡아 둘 가치가 있다.**

### B. theorem이 아니라 certificate-first로 분리해야 하는 것

1. `d5_289` checked cycle decompositions
2. `d5_297/298/299`
3. common channel quotient compression
4. denominator-`16` shared-lexicon interior table (`501` universal interior source types)
5. denominator-`8` checked portal packets

### C. 현재 genuinely open이라 TODO로 남겨야 하는 것

1. post-hinge double-top exit theorem
2. `H_m -> B_m` stitching
3. `B`-active / gate branch integration
4. RouteY seam-glued reduced machine global cycle theorem
5. common global quotient promotion / seam-gluing compression

---

## Lean으로 변환할 때 드러난 빠진 조각

이번 패스에서 가장 중요한 것은 “문서에 수학은 있지만 Lean object가 아직 없다”는 빈칸들이다.

### 1. exported theorem statement의 부재
`RoundY`의 여러 닫힌 패키지는 상태 문서에서 “closed”라고 선언되어 있지만,
Lean import에 필요한 정확한 statement는 별도 추출이 필요하다.
대표적으로:

- accepted odd-`m` backbone
- `T0--T4`
- `G1/G2`
- color-`3` Route-E branch

즉 현재 문서는 theorem map와 status note는 좋지만,
Lean에 그대로 옮길 “정리 본문 시그니처”는 아직 자동으로 얻어지지 않는다.

### 2. common theorem floor namespace의 부재
common lane는 문서가 여러 묶음으로 나뉘어 있어서, Lean 입장에서는 먼저 다음 이름들을 표준화해야 한다.

- `R_re`
- `R_q`
- `beta_m`
- `betaTilde`
- zero-drift packet families
- source lines / seed sets / collar maps

이 namespace 정규화 없이 portal packet을 올리면,
같은 기호가 파일마다 다른 표면을 가리키는 문제가 생긴다.

### 3. checked finite tables를 proof로 바꾸는 표준 방식의 부재
common branch의 진짜 병목은 이제 새 residue family 발견이 아니라
**explicit local packet을 어떤 방식으로 Lean proof로 승격할지**다.

선택지는 둘이다.

- **certificate-first**  
  CSV / table / report를 Lean 데이터로 넣고, 검증 정리를 증명한다.

- **compression-first**  
  four master tapes, seam laws, shared lexicon 같은 압축 정리부터 사람 손으로 짧게 증명한 뒤, 표를 없앤다.

문서 상태를 보면 denominator-`8` `r=8s+4`는 이미
`222 = 87 + 124 + 11`, 네 개 master tape, `11` seam law까지 줄어들어 있어서
compression-first로 갈 가치가 꽤 높다.

### 4. low seed / degenerate seed 부록 처리
stable common theorem은 stable range에서 매우 잘 정리돼 있지만,
`m=39,69,129` 같은 low seed와 `m=9` outlier 처리는 여전히 appendix 성격이다.
이 부분은 main theorem 파일에 섞지 말고,
Lean에서도 `SeedCases.lean` 또는 `FiniteAppendix` 류로 분리하는 편이 낫다.

---

## 추천되는 다음 실제 작업 순서

### 1단계
`Core/Objects.lean`와 `Core/Interfaces.lean`를 실 definition 파일로 만든다.

특히 다음을 먼저 고정한다.

- `State5`
- `SigmaZero`
- `Visible4`
- `H_m`
- `B_m`
- `R_re`
- `R_q`

### 2단계
`d5_300` statement extraction을 먼저 끝낸다.

이 정리는:

- 현재 문서가 명시적이고,
- lower-to-hinge chain의 분기점을 잡아 주며,
- 이후 post-hinge gap을 깨끗하게 분리해 준다.

### 3단계
common `m=15r+9` stable packet exact classification을 formal theorem으로 옮긴다.

이 정리는 현재 common branch에서 가장 “formalization-friendly”하다.
portal machine보다 먼저 잡는 것이 자연스럽다.

### 4단계
checked packet은 `Certificate` namespace로 옮긴다.

특히:

- `d5_289`
- late atlas/routing/promotion
- common quotient compression
- denominator-`16` interior tables
- denominator-`8` portal tables

은 theorem namespace와 분리해야 이후 혼선이 없다.

---

## 이번 패스 산출물

이 패키지에는 다음이 들어 있다.

1. `STATUS_LEDGER_2026-04-05.csv`  
   패키지별 status / Lean mode / missing piece 표

2. `STATUS_LEDGER_2026-04-05.md`  
   같은 내용을 사람이 읽기 쉽게 옮긴 표

3. `D5/*.lean` skeleton  
   시작용 모듈 뼈대

이 산출물의 역할은 완성 proof가 아니라,
**지금 어떤 파일을 만들고 어떤 것은 theorem으로, 어떤 것은 certificate로, 어떤 것은 TODO로 놔야 하는지**
를 고정하는 것이다.