Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch, now that the reduced target is
explicit but the first local realization strategies have been pruned.

Current target:
Determine whether the `s44` edge-conditioned controller is locally realizable
in the smallest static family around `mixed_008`, and if not, identify the next
honest mechanism to try.

Known assumptions:
- `025` gives the first full reduced target:
  omit-base plus omitted-edge cocycle defect.
- `026/027` show that the current-state `B/P/M` realization is blocked on both
  stationary rewrites because the intended `P` and `M` roles collide at the
  same layer-2 current state.
- `028` extracts the missing controller type exactly:
  endpoint orientation on the active adjacent edge.

Attempt A:
  Idea:
  Package `028` as the exact edge-signature extraction implied by `s44`.
  What works:
  The collision files do identify the smallest separating signature:
  - diagonal branch: predecessor `w` relative to `{w0-1,w0}`
  - anti-diagonal branch: predecessor `t=w+2u` relative to `{t0,t0+1}`
  This yields the abstract `off/L/R` transducer demanded by `s44`.
  Where it fails:
  `028` is only an extraction step. It does not yet show that the transducer is
  realizable as a small static local family around `mixed_008`.

Attempt B:
  Idea:
  Search the smallest static two-layer endpoint-controller family on the
  representative diagonal branch.
  What works:
  The family is exact and still tiny:
  - fix `(w0,s0)=(0,0)`
  - choose independent layer-1 directions on the two endpoints
  - choose independent layer-2 directions on the resulting target sets
  - add the four omitted-edge cocycle-defect choices
  Across `2500` candidates on each of `m=5,7,9`:
  - `240` are immediate layer-2 conflicts
  - only `4` are Latin on all colors
  - those same `4` are clean and strict
  - `0` reach the `025` grouped-orbit target
  The crucial refinement is:
  - all `4` Latin survivors are the baseline word `(4,4;2,2)` with the four
    cocycle-defect choices
  - there are `0` nonbaseline Latin survivors
  - there are `0` endpoint-asymmetric Latin survivors
  Where it fails:
  The edge signature is real, but the smallest static two-layer realization is
  blocked before the grouped-orbit stage. The family collapses back to baseline.

Candidate lemmas:
- [C] `028` identifies the correct missing controller type: endpoint
  orientation on the active adjacent edge.
- [C] `029` shows that the smallest static two-layer endpoint-controller family
  is exhausted on `m=5,7,9`.
- [C] More sharply, the only Latin / clean / strict survivors in `029` are the
  baseline low-layer word with optional cocycle defect.
- [H] The next live local branch must add a genuine extra local state carrier
  beyond static two-layer endpoint control.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Search the smallest richer mechanism that can produce a nonbaseline
  endpoint-asymmetric Latin survivor.
- The next honest options are:
  - a three-layer local word search,
  - a two-step memory carrier,
  - or another equally small mechanism that changes the intermediate
    current-state class instead of reusing the baseline one.
- Keep the `025` grouped-orbit signature as the acceptance test.

Next branching options:
1. Main branch:
   smallest three-layer or two-step state-carrier mechanism around the diagonal
   branch.
2. Secondary branch:
   enumerate short endpoint words around `mixed_008` and keep only those that
   change the intermediate current-state class while preserving Latin.
3. Only then:
   revisit translated copies or anti-diagonal variants of the same richer
   mechanism.

Claim status labels:
  [P] `019`, `025`
  [C] `026`, `027`, `028`, `029`
  [H] next local branch must add a genuine extra local state carrier
  [O] full D5 decomposition
