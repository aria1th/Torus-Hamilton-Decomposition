Problem:
After `043`, determine whether the theorem branch can be sharpened from
“carry sheet plus residual `2`-sheet” to a concrete finite-cover normal form,
and isolate the exact status of the local branch.

Current target:
Work the `044` branch on the fixed best-seed active union and extract:
- a checked normal form
  `B <- B+c <- B+c+d`,
- a canonical intrinsic choice of binary residual sheet `d`,
- and the exact statement that the next local target is still only the carry
  sheet `c`.

Known assumptions:
- `042` isolates the carry bit
  `c = 1_{q=m-1}`
  as the smallest verified trigger lift.
- `043` shows the minimal deterministic cover over `B+c` is binary and
  supported only on regular noncarry states.
- `043` also shows time to next carry and first-carry data already
  coordinatize that residual cover nonlocally.

Attempt A:
  Idea:
  Search for a cleaner intrinsic binary coordinatization of the residual sheet.
  What works:
  On `m = 5,7,9,11`, the residual sheet can be chosen as
  `d = 1_{next carry u >= m-3}`.
  This is binary, exact over `B+c`, and makes the lifted transition law
  deterministic.
  Where it fails:
  This is structural, not yet an admissible local observable.

Attempt B:
  Idea:
  Turn the `043` cover into a manuscript-level theorem statement.
  What works:
  The checked active branch now has a clean normal form:
  `B = (s,u,v,layer,family)`,
  `c = 1_{q=m-1}`,
  `d = 1_{next carry u >= m-3}`.
  Exceptional fire descends to `B`, regular fire descends to `B+c`, and active
  evolution closes on `B+c+d`.
  The support of `d` is regular noncarry only, and carry states are singleton
  over `B+c`.
  Where it fails:
  The admissible realization of `c` remains open, so the main local branch is
  still unresolved.

Candidate lemmas:
- [C] Exceptional fire is a function of `B`.
- [C] Regular fire is a function of `B+c`.
- [C] The minimal deterministic cover over `B+c` is binary.
- [C] `d = 1_{next carry u >= m-3}` refines the cover exactly.
- [C] Carry states are singleton over `B+c`.
- [C] The support of `d` lies entirely on regular noncarry states.
- [H] D5 should be stated as grouped base + carry sheet + binary anticipation
  cover.
- [O] Admissible realization of the carry sheet.

Needed computations/search:
- package the `044` normal form
- record the canonical binary anticipation bit
- keep the local branch restricted to carry realization

Next branching options:
1. Main local branch:
   admissible realization of `c = 1_{q=m-1}`
2. Parallel theorem branch:
   formalize / prove the binary anticipation normal form
3. Only later:
   attempt admissible realization of `d` if the global proof still needs it

Claim status labels:
  [P] `025`
  [C] `042`, `043`, `044`
  [H] D5 is grouped base + carry sheet + binary anticipation cover
  [F] broad search for the full residual sheet before carrying `c`
  [O] admissible carry realization
  [O] full D5 decomposition
