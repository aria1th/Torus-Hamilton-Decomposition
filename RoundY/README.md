# RoundY — d=5 Hamilton Decomposition

Hamilton decomposition of the directed `5`-torus

`D_5(m) = Cay((Z_m)^5, {e_0, e_1, e_2, e_3, e_4})`.

**Status:** `[O]` open.  
**Current frontier:** after artifact `046`, grouped-state-descending admissible families are pruned, the structural theorem branch has a clean checked normal form, the first carry-only admissible catalogs are dead, and the carry sheet is now identified exactly as a future grouped-transition event. On `m=5,7,9,11`, the minimal exact future grouped-delta horizon is `m-3`, the minimal exact future grouped-state horizon is `m-2`, and the exact future window compresses to `B` plus `initial flat-run length + first nonflat dn`. It is now: **seek an admissible coding of that exact future-transition event, not a generic broader gauge.**

This README is the current top-level map. It replaces the older Session-20-only
snapshot and is organized around the actual D5 branch progression through the
recent artifacts.

## One-paragraph status

The D5 program has already crossed the earlier barriers. Clean frame is not the
main issue anymore. Latin feasibility is not the main issue anymore. Mixed
cycle-plus-monodromy dynamics already exist. The project then pivoted from
blind local-rule widening to return-map extraction, then from return-map
extraction to reduced perturbation design, and then from reduced perturbation
design to local realization. The current best reduced target is known, the
smallest naive local realization families are heavily pruned, and the sharp
frontier is now a **tiny lifted-sheet admissibility obstruction** on the best
endpoint seed: the lifted phase is already visible on raw `(q,w,layer)`, the
raw control logic is already exact, the carry-slice trigger lift is known, and
the remaining structural object is now explicit: grouped base plus carry sheet
plus binary anticipation cover, with the first carry-only admissible catalogs
now ruled out and the carry bit exposed as a future-transition event.

## Barrier evolution

The real story of RoundY is the bottleneck moving inward:

1. `clean frame absent`
2. `Latin infeasibility`
3. `dynamic collapse`
4. `unknown mixed return mechanism`
5. `unknown reduced 2D/3D target`
6. `unknown local realization of that target`
7. `unresolved local phase exposure`
8. `raw static phase gates pruned`
9. `lifted corridor state visible on raw current coordinates`
10. `coordinate exposure / admissibility`
11. `carry-slice trigger lift identified`
12. `first carry-only admissible catalogs pruned`
13. `carry sheet identified as first exact future-transition event`
14. `current frontier: admissible coding of that future event`

In short:

`clean frame -> Latin -> return dynamics -> reduced normal form -> local realization -> orbit phase -> lifted-coordinate admissibility -> tiny finite-sheet cover -> carry-only admissibility no-go -> future-transition carry sheet`

## High-level progress map

### Phase A. Early discovery and theorem scaffolding

Sessions `1–10` established the prehistory:

- an `m=5` Hamilton witness existed,
- Boolean zero-pattern models were too weak,
- the color-by-color return-map analysis produced the first reusable theorem
  tools,
- the original witness line was useful diagnostically but not the final route,
- the project pivoted to a cyclic-equivariant master permutation field.

Main outcome:

- the problem was rewritten as a quotient-state / anchor-table construction
  problem.

### Phase B. Master field and dynamic-collapse diagnosis

Sessions `11–20` and exact artifacts `001–016` moved the project from broad
search to sharp mechanism analysis:

- clean frame was built into the construction,
- orbit-anchor reconstruction reduced the search space structurally,
- free-anchor search solved outgoing Latin in the live quotient families,
- but pilot-feasible fields collapsed dynamically,
- the collapse law was extracted exactly,
- one-bit and tail-phase refinements were scanned and pruned.

Main outcome:

- the bottleneck moved from Latin to return dynamics.

For the full compressed pre-`017` record, use
[`RoundY/d5_progress_master_summary.md`](./d5_progress_master_summary.md).

## Exact frontier after the old README

This is the part the old `README.md` did not capture.

### `017–019`: return-map extraction and explicit mixed model

These artifacts turned the mixed witness from “a surviving table” into a real
return-map object.

- `017`:
  grouped return for the canonical mixed witness stabilizes to a clean base
  model.
- `018`:
  the grouped dynamics collapse to a skew-odometer-style normal form.
- `019`:
  the exact obstruction is identified:
  each fixed `u` fiber is already perfect, and the remaining obstruction is
  grouped `u`-invariance.

Main outcome:

- the mixed witness is structurally understood,
- and the problem becomes “what extra mechanism creates the missing second
  grouped coordinate?”

### `020–025`: reduced perturbation target

These artifacts found the right reduced target before any honest local
realization search could succeed.

- `020–022`:
  tiny carry-swap and affine paired-carry families were pruned.
- `023`:
  the first clean 2D reduced perturbation appeared:
  a moving adjacent transposition along a diagonal or anti-diagonal, with base
  orbit sizes `[m, m(m-1)]`.
- `024`:
  omitting one row of that moving transposition collapses the grouped base to a
  single orbit of size `m^2`.
- `025`:
  adding the right edge-tied cocycle defect collapses the full grouped state to
  a single orbit of size `m^3`.

Main outcome:

- the correct reduced target is now explicit:
  `omit-base + edge-tied point cocycle defect`.

This is the first point where the D5 branch had a concrete theorem-shaped
target rather than a vague “better mixed witness”.

### `026–031`: first local realization branch pruned

Once `025` existed, the next question became local realization.

These artifacts ruled out the first natural local ansatze:

- `026/027`:
  current-state `B/P/M` stationary realizations fail because of exact layer-2
  collisions.
- `028`:
  endpoint orientation is identified as the right missing local signature.
- `029`:
  the smallest static two-layer endpoint-controller family is pruned.
- `030`:
  short endpoint words exist at the path level.
- `031`:
  the smallest static three-layer promotion of those words is also pruned.

Main outcome:

- endpoint orientation is necessary,
- but fixed static endpoint words are still not enough.

### `032–046`: best endpoint seed, defect quotient, corridor phase, static gate no-go, phase clarification, carrier target, birth-local split, exact raw birth formulas, realization boundary, first admissibility no-go, carry-slice / finite-cover extraction, first carry-only no-go, deep future-transition carry sheet

This is the current live branch.

- `032`:
  the best endpoint seed is isolated:
  left `[2,2,1]`, right `[1,4,4]`.
  Its Latin defect is exact and balanced:
  `250, 490, 810 = 10 m^2` on `m=5,7,9`.
  One-gate, one-bit, and smallest two-class static repairs all fail.
- `033`:
  that defect is quotiented exactly.
  Per color it reduces to four overfull families against four hole families,
  with only one unresolved channel left:
  `R1 -> H_L1`.
  On the extracted local alphabet, the natural shortest repair corridor is
  unary `BBB`, which kills `2`-state and `3`-state transducers immediately.
- `034`:
  the unresolved corridor is extracted as an explicit reduced phase model on
  `(s, layer)`.
  The short and long delay families differ by exactly one full large-orbit lap
  `m(m-1)`.
- `035`:
  the first static phase-exposure layer is already dead:
  no `1`- or `2`-coordinate projection isolates the first exit, exactly `8`
  `3`-coordinate projections do, and every resulting raw static `B`-state gate
  family fails Latin on the pilot range.
- `036`:
  the saved `034` `(s, layer)` rule is clarified as a first-pass projected
  phase lap, not the full long-run deterministic factor.
  The actual traced long corridor admits an exact lifted model on
  `(q, a, layer)`, where `a = s - rho` and `rho = u_source + 1`.
- `037`:
  the lifted state is already visible on raw current coordinates.
  Along every traced corridor state up to first exit,
  `a = q + w - 1_{layer=1}`.
  The raw triple `(q,w,layer)` is an exact `m^3` odometer, and the first exits
  become two universal raw targets:
  regular `(m-1,m-2,1)` and exceptional `(m-2,m-1,1)`.
- `038`:
  in the simple one-step predecessor/successor neighborhood-bit family, the
  exceptional source slice is already local at birth, but the source marker and
  entry marker are not isolated up to projection size `5`.
  So the live issue is the marker itself, not the family bit.
- `039`:
  the best-seed source and entry slices are already exact on raw current
  coordinates:
  source `layer=1, q=m-1, w=0, u!=0`,
  entry `layer=2, q=m-1, w=1, u!=0`,
  with exceptional tag `u=3` at birth in both.
  Current raw `u` then drifts through all residues along representative regular
  and exceptional corridor traces, so the family tag must be transported.
- `040`:
  the first richer families still derived from the same simple `038` row also
  fail:
  full-row source-edge pairs do not isolate birth, and lag-1 / lag-2 full-row
  temporal pairs do not stabilize the exceptional trigger.
  But the raw current coordinate family already closes the reduced control
  logic on the checked active union:
  birth is exact, current `(q,w,u,layer)` separates source families, and
  active-conditioned current `(q,w,layer)` fires with zero prehits.
- `041`:
  the first `025`-style grouped-state-descending admissible families still
  fail exactly.
  On the checked active union, `w` already descends as `s-u mod m`, but the
  regular and exceptional fire predicates are not functions of the current
  grouped state `(s,u,v)`, even after conditioning on family.
  Canonical omit-base base gauges and edge-tied point cocycles do not change
  those collision counts because they still descend to that same grouped state.
- `042`:
  the carry-slice bit `c = 1_{q=m-1}` is the smallest verified trigger lift.
  Exceptional fire already descends to
  `B = (s,u,v,layer,family)`, and regular fire descends to `B` plus `c`.
  But `(B,c)` is still not a closed deterministic active dynamics.
  The structural lift is better read as a tiny finite cover over `B`, with
  fiber size at most `3` on the checked range.
- `043`:
  that tiny-cover picture sharpens.
  The minimal deterministic cover over `B+c` is `2`-sheet on `m=5,7,9,11`,
  supported entirely on the regular noncarry branch.
  The residual sheet is not the obvious bit `1_{q=m-2}` on `m=7,9,11`, and
  short future-carry windows also fail there.
  A theorem-friendly nonlocal coordinatization does exist via time to next
  carry.
- `044`:
  the theorem branch becomes explicit.
  The checked active branch factors as
  `B <- B+c <- B+c+d`
  with
  `d = 1_{next carry u >= m-3}`.
  Carry states are singleton over `B+c`, and `d` is needed only on regular
  noncarry states.
- `045`:
  the first carry-only admissible catalogs are exhausted exactly.
  Across `69,994` candidates on `m=5,7,9,11`, there are `0` exact carry
  realizations in:
  current-edge / label / delta cores up to size `5`,
  low-cardinality `025`-style gauge-transition families up to size `5`,
  and targeted point-defect families up to size `4`.
  Full `B -> B_next` and `B -> B_next -> B_next2` grouped transition classes
  also fail.
  The best surviving negatives are driven by `next_dn` and `dn + next_dn`,
  which are exact on `m=5` but miss only regular carry `B`-states on
  `m=7,9,11`.
- `046`:
  the carry bit is already an exact future-transition event on the checked
  active grouped base.
  The minimal exact future `dn` horizon is `m-3` on `m=5,7,9,11`, and the
  minimal exact future grouped-state horizon is `m-2`.
  The exact future window compresses to:
  current `B` plus
  `initial flat-run length where dn=(0,0,0,1)` plus
  `first nonflat dn`.
  Flat-run length alone is not exact, and the `H-1` ambiguity is confined to
  regular carry `B`-states.

Main outcome:

- the live obstruction is no longer “missing another separator bit”,
- and no longer “need a slightly larger transducer”.
- It is no longer generic coordinate exposure either.
- It is now a **tiny lifted-sheet admissibility problem**.
- The first naive static coordinate-gating branch on the old projected phase is
  already pruned.
- The old `(s, layer)` model is useful, but only as a first-pass projection.
- The lifted phase itself is no longer hidden.
- The exceptional family bit is already cheap at the source.
- The raw birth predicate itself is already explicit at the reduced level.
- The active family split and active-conditioned trigger are already explicit at
  the reduced raw-coordinate level too.
- The missing ingredient is not reduced control logic anymore.
- `w` already descends to grouped state.
- Exceptional fire already descends to `B = (s,u,v,layer,family)`.
- Regular fire descends to `B` plus the carry slice `1_{q=m-1}`.
- The structural lift is no longer vague:
  it is now grouped base plus carry sheet plus binary anticipation cover.
- The first carry-only admissible families are now pruned too.
- The carry sheet is no longer an amorphous deeper lift.
- It is already the first exact future grouped-transition event.
- The remaining live local branch is admissible coding of that future event.
- But the closed structural lift is still not just the carry bit.
- So the missing admissibility ingredient is the smallest finite lifted sheet
  over the grouped base beyond current edge / `1`-step / `2`-step /
  low-cardinality anchored-gauge data.

## Current picture

The strongest supported D5 picture so far is:

1. A canonical mixed witness exists and is structurally real.
2. Its grouped return already has a clean reduced model.
3. The correct reduced perturbation target is known.
4. The smallest natural local realization families have been pruned.
5. The unresolved best-seed local obstruction has a traced deterministic lift on
   `(q, a, layer)`.
6. That lifted state is already visible on raw `(q,w,layer)`.
7. The first raw static phase gate on the projected `(s, layer)` picture has
   already been pruned.
8. In the smallest birth-local neighborhood family, the exceptional source bit
   is already visible but the source marker is not.
9. In exact raw current coordinates, the source and entry birth classes are
   already explicit.
10. The first richer simple-row-derived source-edge and lagged families still
    fail, while raw current coordinates already realize the reduced control
    logic on the checked active union.
11. The first `025`-style grouped-state-descending admissible families also
    fail.
12. The carry slice is the smallest verified trigger lift, but the structural
    reduced object is a tiny finite cover over the grouped base, with fiber
    size at most `3` on the checked range.

So the current question is not:

- “does mixed dynamics exist?”
- “can we guess another one-bit repair?”
- “should we widen tiny transducer search again?”

It is:

**what is the smallest admissible lifted sheet over the grouped base that
exposes and closes the raw control logic already identified?**

## Current next branch

After `042`, the honest next branch is:

1. search for an admissible realization of the **carry-slice lift** if
   trigger-level control is enough, or
2. extract / realize the **tiny finite-sheet cover** over the grouped base if
   a closed odometer-style dynamics is the real target, or
3. only then open genuinely new observable families that are not lifts of the
   same simple `038` row.

What is not recommended now:

- broader one-bit scans,
- generic `2`-state / `3`-state transducer widening on the same alphabet,
- reopening static endpoint-word families without a phase-aware ingredient.

## Recommended companion files

Use these together:

- [`RoundY/d5_progress_master_summary.md`](./d5_progress_master_summary.md)
  for the compressed exact history through the earlier D5 pilot chain
- [`RoundY/current-frontier-and-approach.md`](./current-frontier-and-approach.md)
  for the current problem statement, workflow note, and theorem targets
- [`RoundY/instruction_for_codex.md`](./instruction_for_codex.md)
  for the short Codex-oriented reading order and thinking patterns
- [`DOCUMENT_FOR_EXTERNAL_REVIEW.md`](../DOCUMENT_FOR_EXTERNAL_REVIEW.md)
  for the branch decisions `D17` through `D33`
- [`RoundY/autonomous/d5_autonomous_perturbation_note_v17.md`](./autonomous/d5_autonomous_perturbation_note_v17.md)
  for the latest local-branch summary
- [`formal/README-D5.md`](../formal/README-D5.md)
  for the Lean / formalization side of the extracted D5 model

## Recent artifact chain

| Artifact | Main result |
|---|---|
| `017` | grouped return base model extracted |
| `018` | mixed skew-odometer normal form extracted |
| `019` | exact obstruction = grouped `u`-invariance |
| `023` | first clean 2D reduced perturbation: moving adjacent transposition |
| `024` | omit-one-row defect gives single grouped-base orbit |
| `025` | edge-tied point cocycle defect gives single full grouped orbit |
| `032` | best endpoint seed isolated; tiny static repairs pruned |
| `033` | defect graph quotiented; tiny transducers pruned |
| `034` | unresolved channel extracted as corridor-phase model |
| `035` | raw static phase gates pruned on the best seed |
| `036` | `(s,layer)` clarified as first-pass only; lifted corridor model extracted |
| `037` | lifted phase visible on raw `(q,w,layer)`; next target = localized carrier |
| `038` | exceptional source bit already birth-local; source/entry marker still not locally isolated |
| `039` | source/entry birth classes exact on raw coordinates; next reduced issue = tagged transport |
| `040` | simple richer lifts still fail; raw current coordinates already close reduced control logic |
| `041` | grouped-state-descending admissible families fail; next target = one lifted coordinate beyond `(s,u,v)` |
| `042` | carry slice is the smallest trigger lift; structural object = tiny finite cover over grouped base |
| `043` | minimal deterministic cover over `B+c` is `2`-sheet on `m=5,7,9,11`; residual sheet not any short future-carry window; time-to-next-carry coordinatizes it |
| `044` | **normal form confirmed**: `B <- B+c <- B+c+d` with `d = 1_{next carry u >= m-3}`; carry states singleton over `B+c`; `d` needed only on regular noncarry; carry realization: **open** |
| `045` | **first carry-only admissibility no-go**: `0` exact candidates across `69,994` first catalog families; `B`, `B->B_next`, and `B->B_next->B_next2` classes all fail; next missing datum = broader lifted gauge or deeper-than-`2`-step transition sheet |
| `046` | **future-transition carry sheet extracted**: minimal exact future `dn` horizon = `m-3`, minimal exact future grouped-state horizon = `m-2`; exact compression = `B + flat-run length + first nonflat dn`; next branch = admissible coding of that event |

## Claim labels

- `[P]` proved
- `[C]` computationally verified
- `[H]` heuristic / design principle
- `[F]` failed / ruled out
- `[O]` open

## Short takeaway

RoundY is no longer in the "search around and hope" stage.

It already knows:

- the mixed mechanism,
- the grouped normal form,
- the reduced target,
- the first local families that fail,
- and the **exact 3-layer normal form** of the remaining obstruction:
  `B <- B+c <- B+c+d` where
  `B = (s,u,v,layer,family)`,
  `c = 1_{q=m-1}`,
  `d = 1_{next carry u >= m-3}`.

The d=5 theorem narrative:

| d | Structure |
|---|---|
| 3 | odometer return map |
| 4 | affine / second-return odometer |
| 5 | grouped base + carry sheet + binary anticipation cover |

Next branches:

1. **046A (local):** search an admissible surrogate for `B + flat-run length + first nonflat dn` that still targets only `c = 1_{q=m-1}`.
2. **046B (proof):** formalize the `044` normal form, the `045` first-catalog no-go, and the `046` future-transition theorem cleanly.
