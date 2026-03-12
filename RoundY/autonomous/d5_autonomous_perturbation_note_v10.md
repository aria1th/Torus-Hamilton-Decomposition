Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
through the mixed-witness return-map branch after the unresolved best-seed
channel has already been extracted as a reduced corridor-phase model.

Current target:
Decide whether the first static phase-exposure layer is already enough on the
best endpoint seed:
- left `[2,2,1]`
- right `[1,4,4]`

More concretely:
- can a raw current-coordinate projection of `(q,w,v,u,s,layer)` isolate the
  first `H_L1` exit along every best-seed corridor?
- and if so, do the resulting static `B`-state phase gates have any chance of
  realizing the target?

Known assumptions:
- `025` remains the correct reduced grouped target.
- `032` fixes the best endpoint seed.
- `033` quotients the defect graph and kills the natural tiny-transducer branch
  on the current local alphabet.
- `034` proves the unresolved `R1 -> H_L1` channel is an exact corridor-phase
  problem on `(s, layer)`.

Attempt A:
  Idea:
  Search the smallest raw current-coordinate projection that isolates the first
  `H_L1` exit on every best-seed corridor.
  What works:
  `035` gives a clean boundary.
  Across `m = 5,7,9,11`:
  - no `1`-coordinate projection works
  - no `2`-coordinate projection works
  - exactly `8` `3`-coordinate projections work:
    `(q,w,u)`, `(q,w,s)`, `(q,w,layer)`, `(q,u,s)`, `(q,s,layer)`,
    `(w,u,layer)`, `(w,s,layer)`, `(u,s,layer)`
  So the first static phase-exposure layer is already forced to at least
  `3` raw coordinates.
  Where it fails:
  This only isolates first exit positions along the extracted corridor. It does
  not say the resulting static gate family is viable.

Attempt B:
  Idea:
  Use each separating `3`-coordinate projection to define the first static
  `B`-state phase-gate families and test them exactly.
  What works:
  The family is still small and exact:
  - `8` projections
  - `3` gate modes: `reg_only`, `exc_only`, `both`
  - `4` cocycle-defect choices: `none`, `left`, `right`, `both`
  so `96` exact candidates in total.
  The verdict is sharp:
  - `latin_count = 0`
  - `clean_count = 0`
  - `strict_count = 0`
  - `target_count = 0`
  Every candidate dies at incoming Latin already on the pilot range.
  Where it fails:
  The branch does not produce a positive local realization. It instead proves
  that the first naive static coordinate-gate layer is already pruned.

Candidate lemmas:
- [C] No `1`-coordinate projection of `(q,w,v,u,s,layer)` isolates the first
  `H_L1` exit on every best-seed corridor.
- [C] No `2`-coordinate projection does either.
- [C] Exactly `8` `3`-coordinate projections isolate that first exit on
  `m = 5,7,9,11`.
- [C] Every static `B`-state phase gate built from those projections fails
  incoming Latin on the pilot range.
- [H] The next live branch is not static raw current-coordinate gating.
- [H] The next live branch needs a dynamic/coupled phase carrier or a richer
  observable.
- [O] Full D5 decomposition remains open.

Needed computations/search:
- stop widening raw static coordinate-gated `B`-state repairs on the best seed
- search for the smallest dynamic/coupled phase carrier
- or search for a richer observable that is not just a static projection of the
  current cell coordinates

Next branching options:
1. Main branch:
   a dynamic or coupled local carrier that actually transports corridor phase.
2. Secondary branch:
   a richer local observable than raw current-coordinate projections, still
   tested first on the best seed.
3. Only then:
   reopen local synthesis on the enriched phase-aware alphabet.

Claim status labels:
  [P] `019`, `025`
  [C] `032`, `033`, `034`, `035`
  [H] the first naive static phase-exposure layer is pruned
  [F] raw static coordinate-gated `B`-state repairs
  [O] full D5 decomposition
