# Codex session prompt

아래 지시에 따라 D5 Lean formalization 작업을 진행하라.

1. 먼저 `plans.md`, `implement.md`, `documentation.md`, `lean_worklist.csv`를 읽어라.
2. `plans.md`를 source of truth로 삼아라.
3. 이번 세션에서는 **현재 milestone 하나만** 진행하라.
4. 범위를 넓히지 말고, 관련 파일만 수정하라.
5. `R_re`와 `R_q`를 절대 같은 surface로 취급하지 마라.
6. checked packet을 theorem으로 승격하지 마라. theorem 승격은 proof 또는 certificate checker correctness theorem이 있을 때만 허용된다.
7. stable theorem과 low-seed appendix를 분리하라.
8. source statement가 불명확하면 추측하지 말고 `documentation.md`와 `lean_worklist.csv`에 gap로 기록하라.
9. milestone 종료 전에 validation command를 실행하고, 실패가 있으면 먼저 고쳐라.
10. milestone 종료 후에는 반드시 `documentation.md`와 `lean_worklist.csv`를 갱신하라.

세션 시작 시 우선순위는 다음 순서를 따른다.

- M0 / M1이 안 끝났으면 그것부터 진행
- 그 다음 `M2 -> M3 -> M4`
- certificate layer는 `M5`
- portal split은 `M6`
- frontier 정리는 `M7`
- 최종 audit은 `M8`

재개 세션에서는 `documentation.md`의 마지막 업데이트 블록을 먼저 읽고 이어서 작업하라.
