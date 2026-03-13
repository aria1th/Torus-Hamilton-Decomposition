# RoundY — d=5 Hamilton Decomposition

Hamilton decomposition of the directed `5`-torus

`D_5(m) = Cay((Z_m)^5, {e_0, e_1, e_2, e_3, e_4})`.

**Status:** `[O]` open.  
**Current frontier:** after artifacts `049` and `050`, the theorem-side D5 chain is still the minimal `044–048` normal form, but the compute side is stronger and cleaner than before. Through `m=19`, the countdown-carrier picture stays stable, the stronger current-memory refinement via `rho = source_u + 1 mod m` is exact, and the two highest-value proof-support checks also persist. The open problem is still: **seek an admissible/local coding of the countdown carrier `tau`, not a generic broader future sheet.**

This README is the current top-level map. It replaces the older Session-20-only
snapshot and is organized around the actual D5 branch progression through the
recent artifacts.

## Larger Program Status

RoundY is only the live `d=5` frontier. The broader low-dimensional program is
already in much better shape:

- `d=3` is mathematically solved in the current odometer manuscript;
- `d=4` is mathematically solved in the same return-map / odometer language;
- `d=4` is also fully Lean-formalized in [formal/README.md](../formal/README.md);
- `d=3` has an active Lean cleanup / odometer repackaging branch, but it is
  not the current frontier.

So this README should be read as: the remaining open low-dimensional case is
`d=5`, not as a statement that the whole `d=3,4,5` program is equally open.

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
now ruled out, the carry bit exposed as a future-transition event, the first
exact checked-range carry coding extracted, and the hidden datum `tau` reduced
further to countdown plus a tiny boundary reset law.

## Brief Mathematical Summary

For a reader who does not have the artifacts open, the current D5 picture is:

1. there is a genuine mixed D5 witness, so the problem is no longer existence
   of mixed cycle-plus-monodromy dynamics;
2. the grouped dynamics already have a clean reduced model, and the best
   reduced perturbation target is known;
3. on the active best-seed branch of the unresolved local channel, the checked
   structure factors as
   `B <- B+c <- B+c+d`,
   where
   `B = (s,u,v,layer,family)`,
   `c = 1_{q=m-1}`,
   and
   `d = 1_{next carry u >= m-3}`;
4. the carry sheet `c` is not a function of the current grouped base `B`, so
   the missing ingredient is not another current-state separator;
5. `c` is already an exact one-sided anticipation datum on the grouped
   dynamics: it is determined by the first future nonflat grouped-transition
   event;
6. on the checked moduli `m=5,7,9,11`, the live hidden datum sharpens to
   `tau`, the initial flat-run length for `dn=(0,0,0,1)`, together with a tiny
   boundary correction `epsilon4` at `tau=0`;
7. after `048`, `tau` itself already has exact internal dynamics on the
   checked active nonterminal branch:
   positive values propagate by countdown, and only the boundary reset remains
   to be coded locally.
8. on the larger tested range `m=13,15,17,19`, the compute-side refinement
   through `rho = source_u + 1 mod m` stays exact, and the two narrow
   proof-support checks also persist:
   the `048` reset law remains exact on the same theorem-side quotients, and
   the explicit `047/048` witness pair keeps the same `m-4` lower-bound shape.

So the mathematical problem is now very narrow. The branch is no longer asking
for a new witness or a broader search over tiny controllers. It is asking for
one of two things:

- an admissible/local coding of the countdown carrier `tau`, or
- a theorem that the intended local mechanism class cannot code that carrier.

For context, this is exactly the point where `d=5` now differs from the lower
dimensions:

- `d=3` already closes by direct or finite-defect odometer return maps;
- `d=4` already closes by one more nested return and is fully machine-checked;
- `d=5` already has the same theorem-shaped language, but the last local
  anticipation obstruction is still open.

## Current proof strategy

The current proof attempt is no longer trying to invent a new mixed witness.
That part is already done. The live theorem strategy is:

1. fix the reduced perturbation target from `025`, where the grouped dynamics
   already have the right single-orbit shape;
2. use `044` to package the active best-seed branch as the checked normal form
   `B <- B+c <- B+c+d`, where
   `B = (s,u,v,layer,family)`,
   `c = 1_{q=m-1}`,
   and `d = 1_{next carry u >= m-3}`;
3. use `044–048` to sharpen the remaining gap:
   the missing ingredient is not more controller logic, but an admissible way
   to code the carry target now known as a countdown carrier with a tiny reset
   law:
   checked-range exact form `B + min(tau,8) + epsilon4`,
   equivalent future-window coding by current `B` plus current `epsilon4` plus
   the next `7` future flat/nonflat indicators after the current step,
   and internal `048` dynamics given by countdown away from the boundary plus a
   small boundary reset;
4. use `049/050` only as support around that theorem chain:
   `049` as the stronger constructive current-memory refinement,
   `050` as larger-modulus evidence for the reset law and the witness family;
5. once that carry event is realized in the intended local/admissible class,
   the trigger logic should descend to the reduced model cleanly, while `d`
   stays on the theorem side as a structural finite-cover coordinate.

So the proof is currently split into two coordinated branches:

- local branch:
  find an admissible/local coding of the countdown carrier `tau`;
- theorem branch:
  package `044`, `045`, `046`, `047`, and `048` as the checked normal-form
  chain behind the D5 mechanism.

## What To Do Now

The recommended next work is:

1. proof-first packaging:
   treat `044–048` as one theorem chain:
   finite-sheet normal form,
   first carry-only no-go,
   carry as an exact future-transition event,
   boundary sharpening to `tau` plus a tiny correction,
   then countdown-carrier dynamics for `tau` itself;
2. if any new search is opened, make it explicitly about coding the countdown
   carrier `tau`;
3. do not reopen:
   broad one-bit scans,
   generic tiny-transducer widening on the old alphabet,
   or more current-edge / short-transition carry catalogs unless they are
   justified as a real `tau`-coding family.

In short:

- proof question:
  can the `044–048` chain be turned into a clean theorem package?
- local question:
  can the countdown carrier `tau` be coded admissibly?
- no-go question:
  if not, can that be proved for the current mechanism class?

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
14. `first exact checked-range carry coding extracted`
15. `tau sharpened to an exact countdown carrier with tiny reset law`
16. `current frontier: admissible/local coding of that countdown carrier`

In short:

`clean frame -> Latin -> return dynamics -> reduced normal form -> local realization -> orbit phase -> lifted-coordinate admissibility -> tiny finite-sheet cover -> carry-only admissibility no-go -> future-transition carry sheet -> exact checked-range carry coding -> countdown carrier`

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

### `032–050`: best endpoint seed, defect quotient, corridor phase, static gate no-go, phase clarification, carrier target, birth-local split, exact raw birth formulas, realization boundary, first admissibility no-go, carry-slice / finite-cover extraction, first carry-only no-go, deep future-transition carry sheet, exact checked-range carry coding, countdown carrier, source-residue refinement, proof-support persistence

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
- `047`:
  the `046` target sharpens further.
  The boundary event class at `tau=0` is genuinely `3`-class minimal:
  `wrap`, `carry_jump`, `other`.
  The first exact checked-range quotient is
  `B + min(tau,8) + epsilon4`.
  Equivalently, the first exact checked-range transition-sheet coding is:
  current `B` plus current `epsilon4` plus the next `7` future binary
  flat/nonflat indicators after the current step.
  Full `4`-class event windows become exact at horizon `8`, while pure future
  binary windows become exact only at horizon `10`.
- `048`:
  `tau` itself already has exact internal dynamics on the checked active
  nonterminal branch:
  for `tau>0`, `tau_next = tau-1` exactly, while the boundary `tau=0` reset is
  tiny and current-state driven:
  `wrap -> 0`, `carry_jump` on `(s,v,layer)`, and `other` on `(s,u,layer)`.
- `049`:
  the compute branch gains a stronger current-state refinement through
  transported source residue.
  Through `m=19`, with `rho = source_u + 1 mod m`,
  `tau` is exact on `(s,u,v,layer,rho)`,
  `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
  `c` is exact on `(u,rho,epsilon4)`,
  and `q ≡ u-rho+1_{epsilon4=carry_jump} mod m`.
  But `rho` is not recoverable from `(B,tau,epsilon4)` once `m>=7`, so this is
  a stronger constructive refinement, not the theorem-side minimal object.
- `050`:
  the two highest-value proof-support checks persist through `m=19`.
  The `048` reset law stays exact on the same theorem-side quotients, and the
  explicit `047/048` witness pair persists exactly with
  `x^-_m=(m-2,2,1,2,0)`,
  `x^+_m=(m-1,2,1,2,0)`,
  common `B=(3,1,2,0,regular)`,
  and common future-binary prefix length `m-5`.

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
- The exact checked-range carry target is no longer the whole future window.
- It sharpens to `tau` plus a tiny boundary correction.
- `tau` itself is now known to be a countdown carrier with tiny reset law.
- The compute branch also has a stronger current-memory refinement through
  `rho`, but that is not the theorem-side minimal object.
- The proof branch now has larger-modulus support for both the `048` reset law
  and the `047/048` witness family.
- The remaining live local branch is admissible/local coding of that carrier.
- But the closed structural lift is still not just the carry bit.
- So the missing admissibility ingredient is the smallest finite lifted sheet
  over the grouped base beyond current edge / `1`-step / `2`-step /
  low-cardinality anchored-gauge data, now targeted specifically at `tau`
  rather than a generic broader future sheet.

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
13. The first carry-only admissible catalogs are also exhausted exactly.
14. The carry sheet is already the first exact future grouped-transition
    event, not an unspecified deeper lift.
15. The first exact checked-range carry coding is already extracted:
    `B + min(tau,8) + epsilon4`, or equivalently current `B` plus current
    `epsilon4` plus the next `7` future flat/nonflat indicators after the
    current step.
16. `tau` itself already has exact internal dynamics on the checked active
    nonterminal branch: positive values count down, and only the boundary
    reset is nontrivial.
17. Through `m=19`, the stronger compute-side refinement through `rho`
    remains exact:
    `tau` on `(s,u,v,layer,rho)`,
    `next_tau` on `(s,u,layer,rho,epsilon4)`,
    and `c` on `(u,rho,epsilon4)`.
18. Through `m=19`, the proof-side reset law and the explicit lower-bound
    witness pair both persist.

So the current question is not:

- “does mixed dynamics exist?”
- “can we guess another one-bit repair?”
- “should we widen tiny transducer search again?”

It is:

**what is the smallest admissible/local coding of the countdown carrier
`tau`, now that the checked carry target is already reduced to
`B + min(tau,8) + epsilon4`,
the first exact transition-sheet coding is explicit,
and the internal `tau` dynamics are already reduced to countdown plus reset?**

## Current next branch

After `050`, the honest next branch is:

1. package `044`, `045`, `046`, `047`, and `048` as one theorem chain:
   grouped base, carry sheet, binary anticipation cover, first carry-catalog
   no-go, exact future-transition carry event, the first exact checked-range
   carry coding, and the countdown-carrier law for `tau`;
2. keep `049` as a constructive refinement only:
   use `(B,rho)` if it helps computation, but do not replace the theorem-side
   minimal object `(B,tau,epsilon4)`;
3. use `050` as proof support:
   the reset law and the witness family now have larger-modulus backing
   through `m=19`;
4. only then ask for the next real local step:
   an admissible/local coding of the countdown carrier `tau`, or a reduction
   lemma showing the intended local class cannot code it.

What is not recommended now:

- reopening the first carry-only catalogs already killed by `045`,
- broader one-bit scans,
- generic `2`-state / `3`-state transducer widening on the same alphabet,
- reopening static endpoint-word families without a phase-aware ingredient.

## Recommended companion files

Use these together:

- [`RoundY/d5_progress_master_summary.md`](./d5_progress_master_summary.md)
  for the compressed exact history through the earlier D5 pilot chain
- [`RoundY/current-frontier-and-approach.md`](./current-frontier-and-approach.md)
  for the current problem statement, workflow note, and theorem targets
- [`RoundY/d5_revealed_and_next_split_049.md`](./d5_revealed_and_next_split_049.md)
  for the current revealed facts and the split between proof and compute next directions
- [`RoundY/theorem/d5_proof_direction_compute_support_052.md`](./theorem/d5_proof_direction_compute_support_052.md)
  for the consolidated compute evidence supporting the current proof directions
- [`RoundY/theorem/d5_proof_program_050.md`](./theorem/d5_proof_program_050.md)
  for the explicit split between the negative bounded-horizon route and the
  positive countdown/reset route
- [`RoundY/theorem/d5_boundary_reset_and_tau_proof_052.md`](./theorem/d5_boundary_reset_and_tau_proof_052.md)
  for the current theorem-side packaging of the countdown/reset law
- [`RoundY/theorem/d5_positive_theorem_chain_054.md`](./theorem/d5_positive_theorem_chain_054.md)
  for the current positive-route theorem chain after the reset-law package
- [`RoundY/instruction_for_codex.md`](./instruction_for_codex.md)
  for the short Codex-oriented reading order and thinking patterns
- [`DOCUMENT_FOR_EXTERNAL_REVIEW.md`](../DOCUMENT_FOR_EXTERNAL_REVIEW.md)
  for the branch decisions `D17` through `D45`
- [`RoundY/autonomous/d5_autonomous_perturbation_note_v25.md`](./autonomous/d5_autonomous_perturbation_note_v25.md)
  for the latest compute-branch summary
- [`RoundY/routeY_status_summary_045.md`](./routeY_status_summary_045.md)
  for the compact branch-status freeze at the start of the carry-only search
- [`artifacts/d5_future_transition_carry_coding_047/README.md`](../artifacts/d5_future_transition_carry_coding_047/README.md)
  for the exact checked-range `047` carry-coding extraction
- [`artifacts/d5_tau_countdown_carrier_048/README.md`](../artifacts/d5_tau_countdown_carrier_048/README.md)
  for the countdown-carrier `047A` extraction
- [`artifacts/d5_source_residue_refinement_049/README.md`](../artifacts/d5_source_residue_refinement_049/README.md)
  for the stronger compute-side current-memory refinement
- [`artifacts/d5_proof_support_generalization_050/README.md`](../artifacts/d5_proof_support_generalization_050/README.md)
  for the larger-modulus reset-law and witness-pair proof support
- [`artifacts/d5_proof_direction_evidence_052/README.md`](../artifacts/d5_proof_direction_evidence_052/README.md)
  for the consolidated theorem-side compute evidence through `m=19`
- [`formal/README-D5.md`](../formal/README-D5.md)
  for the Lean / formalization side of the extracted D5 model

## Working files

RoundY now keeps active D5 support files inside `RoundY/`, not `tmp/`.

- root `RoundY/`:
  session summaries and short branch notes such as
  `codex_work_s59.md`,
  `codex_work_s60.md`,
  `codex_work_s61.md`,
  `codex_work_s62.md`,
  `feedback_s63.md`,
  `note_s61.md`,
  `note_s63.md`,
  `routeY_status_summary_045.md`,
  and `d5_carry_transition_horizon_followup_045.md`
- [`RoundY/specs/`](./specs/):
  executable specs and work templates for artifact branches, including
  `d5_future_transition_carry_coding_047_work_template.md`,
  `d5_tau_reset_coding_parallel_work_request_049.md`,
  `d5_parallel_compute_requests_050.md`,
  and `d5_reset_formula_probe_optional_052.md`
- [`RoundY/checks/`](./checks/):
  small JSON prep checks and follow-up machine summaries such as
  `d5_046_boundary_followon_analysis.json`,
  `d5_047_per_modulus_horizon_pattern.json`,
  and `d5_tau_rule_validation_048a.json`
- [`RoundY/theorem/`](./theorem/):
  theorem-packaging notes and manuscript snippets such as
  `d5_tau_admissibility_no_go_proof_progress_048.md`,
  `d5_tau_countdown_proof_progress_049.md`,
  `d5_proof_program_050.md`,
  `d5_proof_generalization_051.md`,
  `d5_boundary_reset_and_tau_proof_052.md`,
  and `d5_positive_theorem_chain_054.md`

These files are research assets for the D5 branch, not transient scratch.

## Current proof program

The D5 theorem side is no longer a generic search. It is now a clean
two-route proof program around the same reduced object.

- Negative route:
  package `046/047/048` as a bounded-horizon no-go statement.
  The target reduction is that an intended admissible/local mechanism should
  factor through current `B`, the boundary class `epsilon4`, and a bounded
  future flat/nonflat window; the witness family from the `047/048` notes then
  blocks any fixed horizon uniformly in `m`.
- Positive route:
  package `048/050/052` as the countdown/reset theorem.
  Here `tau` is the main hidden datum, `tau_next = tau-1` on the positive
  branch, and the only nontrivial dynamics are the tiny `tau=0` reset classes
  `wrap`, `carry_jump`, and `other`.
- Structural wrapper:
  both routes sit inside the same cover picture
  `B <- B+c <- B+c+d`,
  where `c = 1_{q=m-1}` and
  `d = 1_{next carry u >= m-3}`.
- Compute support:
  the stronger current-memory refinement `(B,rho)` from `049` is useful for
  constructive evidence, but it is not the main theorem object.

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
| `047` | **exact checked-range carry coding extracted**: boundary event class is `3`-class minimal; first exact quotient = `B + min(tau,8) + epsilon4`; first exact transition-sheet coding = current `B` + current `epsilon4` + next `7` future flat/nonflat indicators |
| `048` | **countdown-carrier law extracted**: for `tau>0`, `tau_next = tau-1` exactly; boundary reset is tiny with `wrap -> 0`, `carry_jump` on `(s,v,layer)`, and `other` on `(s,u,layer)` |
| `049` | **source-residue refinement extracted**: through `m=19`, `tau` is exact on `(s,u,v,layer,rho)`, `next_tau` on `(s,u,layer,rho,epsilon4)`, and `c` on `(u,rho,epsilon4)`; but `rho` is not recoverable from `(B,tau,epsilon4)`, so this is a stronger compute-side refinement rather than a new theorem object |
| `050` | **proof-support persistence extracted**: through `m=19`, the `048` reset law remains exact on the same theorem-side quotients, and the explicit `047/048` witness pair persists with the same `h < m-4` lower-bound shape |
| `052` | **proof-direction evidence consolidated**: through `m=19`, the `047` theorem-side quotient and horizon patterns persist in the expected per-modulus form, the positive-route reset-law support remains exact, and the negative-route bounded-horizon witness support stays stable |

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
| 3 | solved: odometer / finite-defect odometer return maps |
| 4 | solved + Lean-formalized: affine / second-return odometer |
| 5 | grouped base + carry sheet + binary anticipation cover |

Next branches:

1. **Proof / theorem side:** formalize and write the `044–048` chain cleanly, using `050` only as larger-modulus support.
2. **Constructive compute side:** if search reopens, either target an admissible/local coding of the countdown carrier `tau`, or explicitly pursue the stronger `rho`-transport route from `049`.
