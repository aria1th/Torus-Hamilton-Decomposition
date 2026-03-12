Problem:
After `045`, decide whether the next carry object is still an unspecified
deeper lift, or whether the checked active branch already determines an exact
future-transition sheet for
`c = 1_{q=m-1}`.

Current target:
Work the `046` branch on the fixed best-seed active union and extract the
minimal exact future grouped-transition horizons and their best compression.

Known assumptions:
- `044` gives the checked structural normal form
  `B <- B+c <- B+c+d`.
- `045` kills the first carry-only admissible catalogs.
- The next live local target is still carry-only.

Attempt A:
  Idea:
  Search the minimal exact future grouped-delta and grouped-state horizons.
  What works:
  The minimal exact future `dn` horizons are
  `2,4,6,8` on `m=5,7,9,11`, hence `m-3`.
  The minimal exact future grouped-state horizons are
  `3,5,7,9`, hence `m-2`.
  What fails:
  Nothing on the checked range.

Attempt B:
  Idea:
  Compress the exact future window to a theorem-friendly signature.
  What works:
  Current `B` plus
  `initial flat-run length where dn=(0,0,0,1)` plus
  `first nonflat dn`
  is exact on `m=5,7,9,11`.
  Flat-run length alone is not exact.
  The `H-1` ambiguity is confined to regular carry `B`-states.
  What fails:
  No smaller exact compression is extracted yet.

Candidate lemmas:
- [C] The minimal exact future `dn` horizon is `m-3` on the checked moduli.
- [C] The minimal exact future grouped-state horizon is `m-2` on the checked
  moduli.
- [C] Current `B` plus `flat-run length + first nonflat dn` is exact.
- [H] The next local target is admissible coding of this future-transition
  event.
- [O] Symbolic proof of the `m-3` / `m-2` law.
- [O] Admissible surrogate for the exact future signature.

Needed computations/search:
- package `046`
- update the frontier docs
- next local branch:
  search admissible codings of
  `B + flat-run length + first nonflat dn`
- parallel proof branch:
  package `044/045/046` into one theorem chain

Next branching options:
1. Main local branch:
   admissible coding of the exact future-transition signature
2. Parallel proof branch:
   prove the `m-3` / `m-2` horizon laws
3. Only later:
   revisit whether an even smaller equivalent coding exists

Claim status labels:
  [P] `025`
  [C] `042`, `043`, `044`, `045`, `046`
  [H] the carry bit is the first exact future-transition event
  [F] treating the next carry object as an unspecified broader gauge
  [O] admissible coding of the future-transition signature
  [O] full D5 decomposition
