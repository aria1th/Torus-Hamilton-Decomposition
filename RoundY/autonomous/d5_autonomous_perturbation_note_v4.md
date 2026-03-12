Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, now that the full reduced normal
form target is known but the first direct local emulation attempt has failed.

Current target:
Understand whether the `s43` fixed-`w` local realization ansatz is genuinely
viable, and if not, identify the exact obstruction so the next local branch is
better targeted.

Known assumptions:
- `025` gives the first full reduced normal form candidate:
  omit-base plus pointwise omitted-edge cocycle defect.
- `s43` rewrites the diagonal branch as a fixed adjacent transposition on a
  `w`-pair and proposes the tiny current-state `B/P/M` local family.

Attempt A:
  Idea:
  Exhaust the tiny current-state `B/P/M` family exactly on `m=5,7,9`.
  What works:
  The family is tiny and exact, so this is the right first local test.
  Baseline `mixed_008` still validates cleanly on the same evaluator.
  Where it fails:
  The searched diagonal fixed-`w` family is completely negative:
  no candidate is Latin on all colors for `m=5,7,9`.

Attempt B:
  Idea:
  Check whether the anti-diagonal stationary rewrite avoids that obstruction,
  and explain the outcome structurally rather than treating it as a failed
  parameter sweep.
  What works:
  It does not avoid the obstruction.
  There is an exact layer-2 collision on both stationary rewrites:
  diagonal fixed-`w` and anti-diagonal fixed-`t`.
  In each case, the intended `P` target and the adjacent `M` target collapse to
  the same layer-2 current state, so they cannot be separated by a deterministic
  current-state layer-2 rule.
  Where it fails:
  This does not yet provide the replacement local mechanism.

Candidate lemmas:
- [C] The fixed-`w` and fixed-`t` current-state `B/P/M` families are both
  pruned on `m=5,7,9`.
- [C] The reason is the same exact layer-2 state collision on both branches.
- [H] The next local branch must leave the current-state `B/P/M` ansatz
  entirely.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Design the smallest memory mechanism that can distinguish the colliding
  layer-2 states.
- Keep the `025` grouped orbit signature as the acceptance test.
- Do not reopen broad current-state selector sweeps around the same palette.

Next branching options:
1. Main branch:
   smallest history-sensitive local mechanism for the `025` target.
2. Secondary branch:
   anti-diagonal reduced target only if the diagonal branch stays blocked.
3. Only after those:
   widen the local state space again.

Claim status labels:
  [P] `019`
  [C] `021`, `022`, `024`, `025`, `026`
  [H] next local branch must leave the current-state `B/P/M` ansatz
  [O] full D5 decomposition
