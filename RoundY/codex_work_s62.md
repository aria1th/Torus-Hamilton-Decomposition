Problem:
Clarify the autonomous `047A` branch: determine whether the checked hidden
datum `tau` from `047` has a clean internal dynamics on the frozen active
best-seed branch, or whether it still behaves like an opaque future window.

Current target:
Work directly from the frozen `047` dataset and decide whether the next-`tau`
map admits a compact exact description on `m=5,7,9,11`.

Known assumptions:
- `044` gives the checked finite-cover normal form `B <- B+c <- B+c+d`.
- `045` kills the first carry-only admissible catalogs.
- `046` identifies `c` as the first exact future nonflat-event sheet.
- `047` sharpens the checked target to `B + min(tau,8) + epsilon4`.
- All `B+tau` ambiguity is already confined to `tau=0`.

Attempt A:
  Idea:
  Test whether positive `tau` values already evolve by a deterministic
  countdown law on the frozen active branch.
  What works:
  - On every checked modulus `m=5,7,9,11`, every nonterminal row with
    `tau > 0` satisfies `tau_next = tau - 1` exactly.
  - So the nontrivial part of the dynamics is pushed entirely to the boundary
    `tau = 0`.
  Where it fails:
  - Positive countdown alone does not describe the boundary reset.

Attempt B:
  Idea:
  Search for the smallest exact current-state quotients governing the
  `tau = 0` reset law.
  What works:
  - `wrap` resets to `0`.
  - `carry_jump` resets exactly on `(s,v,layer)`, and no smaller current
    quotient works.
  - `other` resets exactly on `(s,u,layer)` or `(s,u,v)`, and no smaller
    current quotient works.
  - Globally on the boundary, `next_tau` is exact on
    `(epsilon4,s,u,v,layer)`, and no smaller `B`-subset with `epsilon4`
    survives.
  Where it fails:
  - This still does not prove admissibility/local exposure of the needed
    observables.

Candidate lemmas:
- [C] On the checked active nonterminal branch, `tau > 0` implies
  `tau_next = tau - 1`.
- [C] On the boundary `tau = 0`, `next_tau` is exact on
  `(epsilon4,s,u,v,layer)`.
- [C] `carry_jump` boundary reset is already exact on `(s,v,layer)`.
- [C] `other` boundary reset is already exact on `(s,u,layer)`.
- [H] The live local target is a countdown carrier plus a tiny reset law, not
  a generic future sheet.
- [O] Admissible/local realization of that countdown carrier.

Needed computations/search:
- package `048`
- update the RoundY frontier docs
- treat future local branches as countdown-carrier coding, not generic
  future-window coding

Next branching options:
1. theorem branch:
   package `044–048` as one finite-cover / no-go / anticipation / countdown
   chain
2. local branch:
   search admissible codings aimed explicitly at the countdown carrier and its
   reset law
3. no-go branch:
   prove that the current admissible mechanism class cannot expose the needed
   countdown/reset observables

Claim status labels:
  [C] `044`, `045`, `046`, `047`, `048`
  [H] the live local target is a countdown carrier with tiny reset law
  [O] admissible/local coding of that carrier
  [O] full D5 decomposition
