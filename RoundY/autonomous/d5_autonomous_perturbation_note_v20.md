Problem:
After `044`, decide whether the carry sheet
`c = 1_{q=m-1}`
already appears in the first admissible lifted families, or whether the next
local branch must move beyond current edge / `1`-step / `2`-step /
low-cardinality anchored-gauge data.

Current target:
Work the `045` branch on the fixed best-seed active union and search the first
carry-only admissible catalogs exactly.

Known assumptions:
- `042` identifies `c = 1_{q=m-1}` as the smallest verified trigger lift.
- `044` gives the checked structural normal form
  `B <- B+c <- B+c+d`
  with
  `d = 1_{next carry u >= m-3}`.
- The live local target is still only `c`, not `d`.

Attempt A:
  Idea:
  Exhaust the first carry-only admissible catalogs:
  current-edge / label / delta core data,
  low-cardinality anchored gauge-transition data,
  and targeted point-defect data.
  What works:
  Exact cached parallel search on `m = 5,7,9,11` finished in about `108s`
  with `32` workers.
  Total candidates tested:
  `119 + 68405 + 1470 = 69994`.
  What fails:
  There are `0` exact carry realizations in those catalogs.

Attempt B:
  Idea:
  Read the sharpest negative rather than just the zero count.
  What works:
  The best surviving negatives are `next_dn`, then `dn + next_dn`.
  They are exact on `m=5`, and on `m=7,9,11` they miss only regular carry
  states, always on label `B`.
  What fails:
  Adding the first low-cardinality `025`-style anchored-gauge bits does not
  improve that boundary.

Candidate lemmas:
- [C] No exact carry family appears in the first current-edge / `1`-step /
  `2`-step / low-cardinality anchored-gauge catalogs on the checked active
  union.
- [C] Full `B`, `B -> B_next`, and `B -> B_next -> B_next2` grouped transition
  classes still fail to realize `c`.
- [C] The best first negatives are `next_dn` and `dn + next_dn`.
- [H] The next missing admissibility datum is a broader lifted gauge or a
  deeper-than-`2`-step transition sheet.
- [O] Exact admissible realization of `c`.

Needed computations/search:
- package `045`
- update the frontier docs
- next local branch:
  broader lifted gauge or deeper-than-`2`-step transition sheet
- parallel theorem branch:
  formalize `044` and the `045` first-catalog no-go

Next branching options:
1. Main local branch:
   broader lifted gauge for `c`
2. Main local branch:
   deeper-than-`2`-step transition sheet for `c`
3. Parallel theorem branch:
   formalize `044` and the `045` no-go cleanly

Claim status labels:
  [P] `025`
  [C] `042`, `043`, `044`, `045`
  [H] the next carry datum lies beyond the first admissible catalogs
  [F] reopening the same first carry-only catalogs
  [O] admissible carry realization
  [O] full D5 decomposition
