Problem:
After `046`, determine whether the exact future-transition carry target
compresses further on the checked active branch, and identify the first exact
transition-sheet coding of
`c = 1_{q=m-1}`.

Current target:
Work the `047` branch on the fixed active best-seed union and decide whether
the real hidden datum is:
- full future window data,
- `tau =` initial flat-run length,
- `tau` plus a tiny boundary correction,
- or a larger future binary/event sheet.

Known assumptions:
- `044` gives the checked structural normal form
  `B <- B+c <- B+c+d`.
- `045` kills the first current-state / short-transition carry catalogs.
- `046` proves that `c` is already the first exact future-transition event,
  with exact signature
  `B + flat-run length + first nonflat dn`.
- Follow-on analysis shows:
  all `B+tau` ambiguity is at `tau=0`,
  and `B+tau+epsilon` is exact on `m=5,7,9,11`.

Attempt A:
  Idea:
  Prune smaller exact quotients of `(tau, epsilon)`.
  What works:
  - the `tau=0` boundary label is genuinely `3`-class minimal:
    `wrap`, `carry_jump`, `other`
  - `B + min(tau,8) + epsilon4` is exact on `m=5,7,9,11`
  - no smaller truncation or threshold-bit quotient survives before `8`
  - the unique minimal exact contiguous interval quotient on
    `tau in {0,...,9}` is
    `{0,1}|{2}|{3}|{4}|{5}|{6}|{7}|{8,9}`
  What fails:
  - no coarser tested quotient removes the need to track the interior positive
    `tau` values on the checked range

Attempt B:
  Idea:
  Search the first exact transition-sheet codings rather than another
  current-gauge catalog.
  What works:
  - current `B` plus current `epsilon4` plus the next `7` future binary
    flat/nonflat indicators after the current step is exact
  - full current-to-future `4`-class event windows become exact at horizon `8`
  - pure future binary flat/nonflat windows become exact only at horizon `10`
  What fails:
  - pure future binary windows are too coarse unless they are longer
  - the boundary class is not disposable in the first exact compact coding

Candidate lemmas:
- [C] The boundary event class at `tau=0` is genuinely `3`-class minimal on
  `m=5,7,9,11`.
- [C] The first exact checked-range quotient is
  `B + min(tau,8) + epsilon4`.
- [C] The first exact checked-range transition-sheet coding is
  current `B` plus current `epsilon4` plus the next `7` future binary
  flat/nonflat indicators after the current step.
- [H] The real hidden datum is `tau`, with `epsilon` as a secondary boundary
  correction.
- [O] Admissible/local realization of that `tau` coding.
- [O] Symbolic proof of the checked `8/7/10` horizon facts in the exact
  transition-sheet catalogs.

Needed computations/search:
- package `047`
- update the frontier docs
- next local branch:
  search admissible codings of `tau`, not larger future sheets
- parallel proof branch:
  package `044/045/046/047` as one checked theorem chain

Next branching options:
1. Main local branch:
   search admissible codings of `tau`, using the `047` exact target as the
   new boundary
2. Parallel proof branch:
   turn `044/045/046/047` into one normal-form / no-go / exact-coding package
3. Only later:
   ask whether the checked-range `tau` cap at `8` reflects a true uniform law
   or only the current tested range

Claim status labels:
  [P] `025`
  [C] `042`, `043`, `044`, `045`, `046`, `047`
  [H] the live hidden datum is `tau` with a tiny boundary correction
  [F] treating the carry target as a generic broader future sheet
  [O] admissible/local coding of `tau`
  [O] full D5 decomposition
