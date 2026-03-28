# NEXT STEPS (2026-03-28)

지금 시점에서 가장 자연스러운 다음 작업은 더 이상 local cleanup이 아닙니다.
focus는 explicit reduced machine의 global cycle closure입니다.

## 우선순위 1: seam graph language 결정

현재 generic-late good branch `g_t`는

- rigid nondefect pieces
- explicit defect three-block piece
- constant ambient translation

으로 완전히 local-explicit합니다.

다음 proof step은 이것을

- finite seam graph / gluing operator
- 혹은 equivalent finite-state return graph

로 쓰는 것입니다.

이 선택이 맞으면 final cycle theorem은 arithmetic congruence보다
작은 combinatorial graph theorem으로 내려갑니다.

## 우선순위 2: split branch hand-closure 여부 판단

global odometer는 no-go이므로, split branch는

- seam graph theorem으로 같이 닫을지,
- 아니면 residue-family hand proof로 닫을지

를 비교해야 합니다.

현재 evidence상 split good branch는 single-cycle보다 multi-cycle이 훨씬 흔합니다.
그래서 목표는 “single-cycle criterion”보다
“cycle partition law” 쪽이 더 자연스러울 수 있습니다.

## 우선순위 3: unsplit classes beyond `15r+3 / 15r+9`

현재 explicit reduced base-machine theorem은 `m ≡ 3,9 (mod 15)` classes에서 가장 정리되어 있습니다.
이 범위를 넘어 동일한 seam language가 유지되는지 확인해야 합니다.

## 우선순위 4: manuscript patch는 마지막에

지금은 manuscript를 중간 상태로 부분 patch하는 것보다,
reduced arithmetic final theorem의 언어를 먼저 안정시키는 편이 낫습니다.

따라서 manuscript patch는 다음 두 조건 중 하나가 만족된 뒤에 하는 것이 좋습니다.

1. seam graph theorem statement가 정리됨
2. final cycle law가 residue-wise로 손으로 닫힘

## 즉시 참조할 문서

- `CURRENT_STATUS.md`
- `MAIN_FLOW.md`
- `KNOWN_CORRECTIONS_AND_SUPERSESSIONS.md`
- `../01_notes/d5_generic_late_hidden_plus5_clock_and_seam_surgery_draft_2026-03-28.md`
