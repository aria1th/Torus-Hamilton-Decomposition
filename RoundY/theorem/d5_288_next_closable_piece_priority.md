# D5 288 Next Closable Piece Priority

This note records the current answer to the question:

> if one now chooses exactly one next useful mathematical fragment to close,
> what should it be?

The choice recorded here is intentionally narrow. It is not a claim that the
full final theorem is now immediate. It is a priority decision about which next
fragment is both:

- mathematically central, and
- most likely to improve the real frontier rather than only its presentation.

## 1. Options considered

At the current branch state, the most plausible next targets are:

1. a new D3-facing theorem or cleanup fragment;
2. the D5 promoted-collar **base-section reduction / no-go theorem**;
3. the D5 separate **`B`-active / gate theorem**;
4. a D5 pure color-`1` **next-repair theorem on the base permutation**;
5. a broader resonant master theorem that tries to package all remaining
   resonant behavior at once.

## 2. Decision

**Priority choice:** target the D5 pure color-`1` **promoted-collar
base-section reduction / no-go theorem** first.

## 3. Why this is the best next target

### A. It is the mathematically live bottleneck

The current canonical packet already says that the remaining resonant program is
split into two branches:

- the pure color-`1` branch, now localized to the width-`1` / width-`3` /
  promoted-collar / double-top / base-section structure;
- the separate `B`-active / gate branch.

Inside the pure color-`1` branch, the current documents already isolate the
exact obstruction:

- width-`1` by itself is obstructed;
- width-`3` by itself is obstructed;
- the promoted-collar correction has now been locally audited completely;
- the current promoted-collar branch further reduces to an exact induced map on
  `H_m = {c=0, d=0}`;
- in checked resonant moduli, that induced map is not a single cycle and its
  cycle decomposition is already visible on the base subset `B_m = {e=0}`.

So this is not an arbitrary next experiment. It is the smallest unresolved
mathematical object that sits directly on the main resonant proof path and is
already strongly supported by exact checked data.

### B. It is upstream of the final resonant closure

If the base-section reduction / no-go theorem closes, then the pure color-`1`
branch is no longer being treated heuristically at the promoted-collar level.
It becomes a sharply reduced packet with one explicit base permutation
obstruction. The next positive theorem target then becomes correspondingly
smaller.

That is a much better frontier than the current one:

- one branch reduced to an exact one-dimensional obstruction,
- one branch still open,

rather than

- both branches still live in broad local language.

So this target produces the cleanest possible narrowing of the actual theorem
frontier.

### C. It is more canonical than the gate branch

The `B`-active / gate branch is real, but it is more special-case and more
branch-specific. The pure color-`1` branch is more canonical:

- it is visible in both the `51`-type and `69`-type reductions;
- it already has canonical width-`1` and width-`3` models;
- it already has theorem-level negative obstruction statements;
- it already has the promoted-collar local audit;
- and it now has an exact checked reduction to `H_m`, then to the base subset
  `B_m`.

That makes the base-section reduction / no-go theorem a better next theorem
target than the gate branch, because it is the place where the current branch
has already compressed the dynamics furthest.

### D. It is more valuable than a new D3 fragment right now

The D3 side is mathematically much more settled.

There are still useful D3 tasks:

- arXiv-facing cleanup,
- strategy exposition,
- possible finite-defect / return-ladder abstraction notes,
- formal cleanup.

But those would mostly improve presentation or portability, not the active
mathematical frontier.

By contrast, a D5 promoted-collar base-section reduction / no-go theorem would
change the actual frontier. So it is the better next fragment if the goal is to
close one more meaningful piece of open mathematics.

## 4. What this target should mean concretely

The goal should not be phrased vaguely as

- “make the resonant color-`1` branch work.”

It should be phrased sharply as:

> prove that the current promoted-collar pure color-`1` package reduces to an
> exact induced map on `H_m = {c=0, d=0}`, and that on the checked resonant
> branch this package is already governed by a smaller base permutation
> obstruction on `B_m = {e=0}` rather than by an unresolved bulk phenomenon.

That is now the exact missing structural counterpart to the existing local
obstruction theorems.

## 5. Acceptance target

The right acceptance target for this next piece is:

1. state the exact induced map `F_m : H_m -> H_m` at theorem level for the
   promoted-collar package;
2. prove the section-reduction statement from the full promoted-collar branch
   to `H_m`;
3. prove a theorem-level no-go conclusion, or at minimum an exact reduction to
   the base permutation `P_m : B_m -> B_m`;
4. use that result to rephrase the next positive repair target as a theorem
   about changing `P_m`, rather than as a vague direct breaker search.

If this succeeds, the pure color-`1` resonant branch is no longer a broad
double-top search problem. It becomes a sharply reduced base-permutation
problem.

## 6. Deferred targets

The following remain important but are not the first target:

- the separate `B`-active / gate theorem;
- the next positive repair theorem on the reduced base permutation;
- broader resonant packaging that mixes both branches too early;
- new D3 theorem fragments that do not move the D5 frontier.

## 7. Updated reading after 289/291

The mathematical priority recorded here is still correct as a theorem-order
statement: the promoted-collar base-section reduction / no-go object is the
right first structural target inside the pure color-`1` branch.

But after
[d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
and the compute-campaign conclusion
[d5_291_residual_compute_campaign_conclusion.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md),
the operational next step is now narrower:

- treat the current promoted-collar packet as a control/no-go family;
- and test new pure color-`1` candidates by whether they actually change the
  induced base permutation `P_m`.

So the present note should now be read as the theorem-priority predecessor to
that more operational campaign split, not as an invitation to keep polishing
the same local-burst family indefinitely.
