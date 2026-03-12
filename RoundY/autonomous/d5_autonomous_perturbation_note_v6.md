Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the reduced target is known
but several local realization families have now been pruned.

Current target:
Understand whether the `s44` endpoint-oriented idea has any genuinely live local
branch left, and if so, what the next smallest mechanism should be.

Known assumptions:
- `025` gives the reduced target:
  omit-base plus omitted-edge cocycle defect.
- `026/027` show the vertex-conditioned current-state `B/P/M` ansatz is blocked
  on both stationary rewrites.
- `028` extracts the right missing local signature:
  endpoint orientation on the active adjacent edge.
- `029` shows the smallest static two-layer endpoint-controller family is
  already exhausted: only the baseline word survives Latin.

Attempt A:
  Idea:
  Search for short nonbaseline endpoint words before insisting on a full static
  field realization.
  What works:
  `030` finds a real path-level candidate set on `m=5,7,9`:
  - `6` desired left words
  - `6` desired right words
  - `18` opposite-sign pairs
  - `14` pairs distinct at both layer 2 and layer 3
  So the richer branch is not empty at the path level.
  Where it fails:
  `030` is only a catalog. It does not address Latin or static consistency.

Attempt B:
  Idea:
  Promote the `030` words into the smallest static three-layer local family.
  What works:
  The family is still tiny and exact:
  - representative branch `(w0,s0)=(0,0)`
  - `18` endpoint-word pairs
  - `4` cocycle-defect choices
  - `72` total candidates per modulus
  Where it fails:
  `031` is completely negative on `m=5,7,9`:
  - `12` layer-2 conflicts
  - `16` layer-3 conflicts
  - `0` Latin survivors
  - `0` clean / strict / target survivors
  So path-level viable words do not yet lift to a static field family.

Candidate lemmas:
- [C] `028` identifies the correct local signature: endpoint orientation.
- [C] `029` prunes the smallest static two-layer endpoint-controller family.
- [C] `030` shows there are nonbaseline short endpoint words with the correct
  reduced `\pm 1` effect and changed intermediate state class.
- [C] `031` shows those path-level words still fail as the smallest static
  three-layer family; none is Latin on `m=5,7,9`.
- [H] The next live branch must do more than choose a fixed short endpoint word:
  it must also solve the Latin failure.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- Search the smallest mechanism that turns a `030`-type word pair into a Latin
  field.
- The next honest candidates are:
  - a two-step memory carrier,
  - a minimal neighboring Latin-repair mechanism around a `030` pair,
  - or a slightly longer local word family explicitly designed to repair the
    `031` indegree failure.
- Keep the `025` grouped orbit signature as the acceptance test.

Next branching options:
1. Main branch:
   use `030` as a seed and search the smallest Latin-repair / memory mechanism
   around one representative endpoint-word pair.
2. Secondary branch:
   extend the word length slightly, but only together with an explicit Latin
   repair criterion.
3. Only then:
   revisit translated copies or anti-diagonal analogues.

Claim status labels:
  [P] `019`, `025`
  [C] `026`, `027`, `028`, `029`, `030`, `031`
  [H] the next live branch must solve the Latin failure, not just endpoint
      separation
  [O] full D5 decomposition
