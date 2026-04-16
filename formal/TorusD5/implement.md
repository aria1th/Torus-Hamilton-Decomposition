# Codex runbook for D5 Lean formalization

이 문서는 Codex가 D5 Lean 작업을 수행할 때 따라야 할 운영 규칙이다.

## 시작 순서

1. `plans.md`를 먼저 읽는다.
2. `documentation.md`에서 현재 milestone과 최근 결정 사항을 확인한다.
3. `lean_worklist.csv`에서 이번에 손댈 파일과 상태를 확인한다.
4. 이번 턴에서는 **하나의 milestone**만 수행한다.

## 핵심 운영 규칙

1. `plans.md`가 source of truth다.
2. 범위를 넓히지 않는다. 현재 milestone에 필요한 파일만 수정한다.
3. milestone 종료 전에는 반드시 validation command를 실행한다.
4. validation 실패가 나오면 먼저 수정한다.
5. 수정 후에는 `documentation.md`와 `lean_worklist.csv`를 함께 업데이트한다.

## 수학/상태 규칙

1. `R_re`와 `R_q`를 절대 같은 surface로 취급하지 않는다.
2. `checkedCertificate`는 `promotedTheorem`이 아니다.
3. stable theorem 본문에 low-seed appendix를 섞지 않는다.
4. frontier를 theorem처럼 이름 붙여도 되지만, proof 상태는 반드시 `frontier`로 남긴다.
5. status note에서 theorem statement를 추출할 때, quantifier와 side-condition을 추측하지 않는다.

## 코드 레벨 규칙

1. 새 정의는 가능한 한 `def`/`structure`/`inductive`로 둔다.
2. theorem module에 새 `axiom`을 추가하지 않는다.
3. 임시 placeholder가 정말 필요하면 아래 형식을 쓴다.
   - 주석에 `[PLACEHOLDER]`
   - 주석에 `status:`
   - 주석에 `sourceDoc:`
   - 주석에 `gap:`
   - `lean_worklist.csv`에 같은 항목을 추가
4. 하나의 placeholder가 실제 theorem인 척 import graph를 오염시키지 않게, 가능하면 interface/assumption 파일로 격리한다.

## theorem / certificate 구분 규칙

다음 조건을 만족해야만 theorem으로 승격할 수 있다.

- exact statement가 있다.
- source doc가 적혀 있다.
- proof가 있거나, certificate checker correctness theorem이 있다.
- validation command가 있다.

아래 중 하나라도 빠지면 theorem 승격을 금지한다.

- checked report만 존재
- finite table만 읽었고 checker가 아직 없음
- low seed / outlier / degenerate case 분리가 안 됨
- notation ambiguity가 남아 있음

## 로그 업데이트 규칙

milestone 종료 시 `documentation.md`에 반드시 적는다.

- 완료한 파일
- 추가/수정한 정의
- 추출한 theorem statement
- 남아 있는 placeholder
- 새로 드러난 gap
- 실행한 validation command와 결과

`lean_worklist.csv`에는 반드시 반영한다.

- status 변경
- proof mode 변경
- blocker 변경
- validation command 변경

## 멈춰야 하는 경우

다음 상황에서는 범위를 넓히지 말고 멈춘다.

1. source 문서만으로 exact statement를 복원할 수 없음
2. `R_re` / `R_q` 표면이 다시 섞일 위험이 있음
3. checked packet을 theorem처럼 올리고 있어 gap가 숨겨짐
4. 현재 milestone의 build가 깨졌는데 unrelated file까지 고쳐야 할 상황

이 경우 해야 할 일은 두 가지뿐이다.

- `documentation.md`에 blocker를 기록한다.
- `lean_worklist.csv`에서 해당 항목 상태를 `workingTheorem` 또는 `frontier`로 유지한다.

## 권장 작업 패턴

- 작은 diff
- build
- log update
- 다음 작은 diff

한 번에 큰 refactor를 시도하지 않는다.
