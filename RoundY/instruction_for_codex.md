# Instruction For Codex

This file is the shortest practical briefing for a Codex-style agent entering
the current RoundY `d=5` branch.

It is not a full history. It is the minimum orientation needed to avoid
restarting dead branches and to think in the right coordinates from the start.

## Read this first

Read in this order:

1. [README.md](./README.md)
2. [current-frontier-and-approach.md](./current-frontier-and-approach.md)
3. [../DOCUMENT_FOR_EXTERNAL_REVIEW.md](../DOCUMENT_FOR_EXTERNAL_REVIEW.md)
   Focus on `D23`, `D24`, `D25`, `D26`, `D27`, `D28`, `D29`, `D30`, `D31`,
   `D32`, `D33`, `D34`, `D35`, `D37`, `D38`, `D40`, `D42`, `D45`.
4. [autonomous/d5_autonomous_perturbation_note_v25.md](./autonomous/d5_autonomous_perturbation_note_v25.md)

Then read the key artifact READMEs in this order:

1. [../artifacts/d5_return_map_model_017/README.md](../artifacts/d5_return_map_model_017/README.md)
2. [../artifacts/d5_mixed_normal_form_and_u_obstruction_019/README.md](../artifacts/d5_mixed_normal_form_and_u_obstruction_019/README.md)
3. [../artifacts/d5_grouped_transposition_family_023/README.md](../artifacts/d5_grouped_transposition_family_023/README.md)
4. [../artifacts/d5_omit_base_cocycle_defect_025/README.md](../artifacts/d5_omit_base_cocycle_defect_025/README.md)
5. [../artifacts/d5_endpoint_latin_repair_032/README.md](../artifacts/d5_endpoint_latin_repair_032/README.md)
6. [../artifacts/d5_defect_splice_transducer_033/README.md](../artifacts/d5_defect_splice_transducer_033/README.md)
7. [../artifacts/d5_corridor_phase_extraction_034/README.md](../artifacts/d5_corridor_phase_extraction_034/README.md)
8. [../artifacts/d5_static_phase_gate_nogo_035/README.md](../artifacts/d5_static_phase_gate_nogo_035/README.md)
9. [../artifacts/d5_corridor_phase_clarification_036/README.md](../artifacts/d5_corridor_phase_clarification_036/README.md)
10. [../artifacts/d5_lifted_corridor_carrier_target_037/README.md](../artifacts/d5_lifted_corridor_carrier_target_037/README.md)
11. [../artifacts/d5_birth_local_signature_search_038/README.md](../artifacts/d5_birth_local_signature_search_038/README.md)
12. [../artifacts/d5_raw_birth_marker_transport_039/README.md](../artifacts/d5_raw_birth_marker_transport_039/README.md)
13. [../artifacts/d5_rich_observable_realization_040/README.md](../artifacts/d5_rich_observable_realization_040/README.md)
14. [../artifacts/d5_coordinate_exposure_admissibility_041/README.md](../artifacts/d5_coordinate_exposure_admissibility_041/README.md)
15. [../artifacts/d5_carry_slice_cover_042/README.md](../artifacts/d5_carry_slice_cover_042/README.md)
16. [../artifacts/d5_finite_cover_admissibility_043/README.md](../artifacts/d5_finite_cover_admissibility_043/README.md)
17. [../artifacts/d5_carry_and_finite_cover_044/README.md](../artifacts/d5_carry_and_finite_cover_044/README.md)
18. [../artifacts/d5_carry_admissibility_search_045/README.md](../artifacts/d5_carry_admissibility_search_045/README.md)
19. [../artifacts/d5_deep_transition_carry_sheet_046/README.md](../artifacts/d5_deep_transition_carry_sheet_046/README.md)
20. [../artifacts/d5_future_transition_carry_coding_047/README.md](../artifacts/d5_future_transition_carry_coding_047/README.md)
21. [../artifacts/d5_tau_countdown_carrier_048/README.md](../artifacts/d5_tau_countdown_carrier_048/README.md)
22. [../artifacts/d5_source_residue_refinement_049/README.md](../artifacts/d5_source_residue_refinement_049/README.md)
23. [../artifacts/d5_proof_support_generalization_050/README.md](../artifacts/d5_proof_support_generalization_050/README.md)

If working on Lean / formalization, then also read:

1. [../formal/README-D5.md](../formal/README-D5.md)
2. [../formal/D5_LEAN_PROGRESS.md](../formal/D5_LEAN_PROGRESS.md)

If producing a new research note or work spec, use:

1. [../docs/template_to_use.md](../docs/template_to_use.md)
2. [../docs/suggested_workflow.md](../docs/suggested_workflow.md)

For D5 support files inside this repo, use this layout:

- `RoundY/specs/` for executable specs and work templates
- `RoundY/checks/` for small JSON prep checks and follow-up summaries
- `RoundY/theorem/` for theorem-shaping notes and snippets
- root `RoundY/` for short session summaries such as `codex_work_s59.md`

For the current theorem-side packaging around `047–054`, start with:

1. [theorem/d5_proof_program_050.md](./theorem/d5_proof_program_050.md)
2. [theorem/d5_proof_generalization_051.md](./theorem/d5_proof_generalization_051.md)
3. [theorem/d5_boundary_reset_and_tau_proof_052.md](./theorem/d5_boundary_reset_and_tau_proof_052.md)
4. [theorem/d5_positive_theorem_chain_054.md](./theorem/d5_positive_theorem_chain_054.md)

These notes spell out the actual proof split:

- negative route:
  bounded-horizon no-go via the `046/047/048` witness family
- positive route:
  countdown/reset theorem packaging for `tau`
- compute support:
  stronger `(B,rho)` refinement only when explicitly using a constructive
  branch

## Real current problem

Do not frame the problem as:

- “find any mixed witness”
- “find a better one-bit separator”
- “try a slightly larger tiny transducer”

The real frontier after `050` is:

**find an admissible/local coding of the countdown carrier `tau`, now that the structural theorem
branch is explicit, the first carry-only admissible catalogs are dead, the
carry sheet is already the first exact future-transition event, and the first
exact checked-range carry coding is known**

`R1 -> H_L1`

for the best endpoint seed:

- left `[2,2,1]`
- right `[1,4,4]`

## What is already known

Treat these as current working facts unless you are explicitly revisiting them.

1. `019`
   The canonical mixed witness already has an explicit reduced return-map
   model.

2. `023–025`
   The right reduced perturbation target is known:
   the grouped target is not vague anymore.

3. `032`
   The best local endpoint seed is known.

4. `033`
   The defect graph is bounded and the natural small transducer branch is
   already pruned on the current alphabet.

5. `034`
   The unresolved corridor admits a first-pass projected phase model on
   `(s, layer)`.

6. `035`
   The first raw static phase-exposure layer is already pruned:
   no `1`- or `2`-coordinate projection isolates the first exit, and every
   static `B`-state gate built from the separating `3`-coordinate projections
   fails Latin.

7. `036`
   The saved `034` `(s, layer)` rule is only a first-pass projected lap, while
   the traced long corridor lifts exactly to `(q, a, layer)`.

8. `037`
   That lifted state is already visible on raw `(q,w,layer)`, and the traced
   corridor is an exact raw-coordinate odometer with two universal first-exit
   targets.

9. `038`
   In the simple one-step predecessor/successor neighborhood-bit family, the
   exceptional source slice is already locally visible, but the source marker
   and entry marker are not isolated up to projection size `5`.

10. `039`
   In exact raw current coordinates, the source and entry birth classes are
   already explicit, but current raw `u` drifts through all residues later, so
   the family tag still has to be transported.

11. `040`
   The first richer source-edge / lagged lifts of the simple `038` row still
   fail, but raw current coordinates already realize birth, active family
   separation, and active-conditioned target firing on the checked active
   union.
12. `041`
   The first `025`-style grouped-state-descending admissible families still
   fail exactly. `w` already descends as `s-u`, but the fire predicates do not
   descend to current grouped state `(s,u,v)`, even after conditioning on
   family. So the next honest target is one lifted coordinate beyond current
   grouped state.
13. `042`
   The carry-slice bit `c = 1_{q=m-1}` is the smallest verified trigger lift:
   exceptional fire already descends to
   `B = (s,u,v,layer,family)`, and regular fire descends to `B` plus `c`.
   But `(B,c)` is still not a closed deterministic dynamics. The structural
   lift is therefore better read as a tiny finite cover over `B`, with fiber
   size at most `3` on the checked range.
14. `043`
   That finite-cover statement sharpens:
   the minimal deterministic cover over `B+c` is `2`-sheet on
   `m=5,7,9,11`, supported entirely on the regular noncarry branch.
   The residual sheet is not the obvious bit `1_{q=m-2}` on `m=7,9,11`, while
   `time to next carry` already gives a theorem-friendly nonlocal
   coordinatization.
15. `044`
   The theorem branch becomes explicit:
   the residual sheet can be chosen as
   `d = 1_{next carry u >= m-3}`.
   So the checked active branch factors as
   `B <- B+c <- B+c+d`,
   with `d` a binary anticipation sheet and carry states singleton over `B+c`.

16. `045`
   The first carry-only admissible catalogs are already pruned exactly:
   `0` exact candidates across the checked
   current-edge / label / delta core catalog up to size `5`,
   low-cardinality gauge-transition catalog up to size `5`,
   and targeted point-defect catalog up to size `4`.
   Full `B -> B_next` and `B -> B_next -> B_next2` grouped transition classes
   still fail.

17. `046`
   The carry sheet is already an exact future-transition event on the checked
   active grouped base.
   The minimal exact future `dn` horizon is `m-3`, the minimal exact future
   grouped-state horizon is `m-2`, and the exact future window compresses to
   current `B` plus `flat-run length + first nonflat dn`.
18. `047`
   The exact checked-range carry target sharpens to
   `B + min(tau,8) + epsilon4`.
   The boundary event class at `tau=0` is `3`-class minimal, and the first
   exact transition-sheet coding is current `B` plus current `epsilon4` plus
   the next `7` future flat/nonflat indicators after the current step.
19. `048`
   `tau` itself already has exact internal dynamics on the checked active
   nonterminal branch:
   for `tau>0`, the next value is `tau-1`,
   while the boundary reset at `tau=0` is tiny and current-state driven:
   `wrap -> 0`, `carry_jump` on `(s,v,layer)`, and `other` on `(s,u,layer)`.
20. `049`
   a stronger constructive refinement persists through `m=19`:
   with `rho = source_u + 1 mod m`,
   `tau` is exact on `(s,u,v,layer,rho)`,
   `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
   and `c` is exact on `(u,rho,epsilon4)`.
   But `rho` is not recoverable from `(B,tau,epsilon4)` once `m>=7`, so this
   is a compute-side refinement, not the main theorem object.
21. `050`
   the two narrow proof-support checks persist through `m=19`:
   the `048` reset law remains exact on the same theorem-side quotients,
   and the explicit `047/048` witness pair persists with the same
   `h < m-4` lower-bound shape.

So the branch is now:

**projected phase known, raw odometer known, raw control logic explicit, grouped-state descent exhausted, carry lift identified, binary anticipation cover explicit, first carry-only catalogs exhausted, future-transition carry sheet extracted, exact checked-range carry coding extracted, countdown carrier extracted, stronger current-memory refinement available, larger-modulus proof support in place**

## Patterns to think in first

These patterns should come before any broad search.

### 1. Reduced model first, local realization second

Always ask:

- what reduced map is already known?
- what exact obstruction remains in that reduced map?
- what is the smallest local mechanism that could realize or expose it?

Do not jump to local-rule widening before answering those.

### 2. One best seed first

Use the best seed from `032` first:

- left `[2,2,1]`
- right `[1,4,4]`

Do not widen to lower-ranked seeds unless the best-seed branch is genuinely
exhausted or the new mechanism clearly cannot act on that seed.

### 3. Preserve the `025` target unless there is evidence to leave it

The current reduced target is not a vague heuristic. It is the best exact
reduced object we have.

Default assumption:

- preserve the `025` grouped target to first order

Only leave it if a branch gives concrete evidence that the true target must be
different.

### 4. Treat failure as obstruction sharpening

Every failed branch must return one of:

- a smaller live search space
- a structural no-go
- a cleaner reduced target
- a sharper theorem-shaped conjecture

“No survivors” by itself is not enough.

### 5. Think in orbit phase, not opaque controller state

After `034–037`, the live obstruction is best thought of as corridor
localization on top of an already-visible raw odometer.

Default question:

- how can a local rule read or carry the extracted phase?

not:

- how can we add more abstract controller states?

### 6. Prefer theorem-shaped outputs

The strongest outputs now are not huge candidate lists.
They are:

- exact reduced formulas
- exact obstruction statements
- exact quotient laws
- exact phase rules
- exact “if this local mechanism exists, then the grouped target follows”
  bridge lemmas

## Anti-patterns to avoid

Do not default to:

1. broad one-bit scans
2. broad generic `2`-state / `3`-state transducer widening on the same local
   alphabet
3. reopening static endpoint-word catalogs without a phase-aware ingredient
4. abandoning the best seed too early
5. abandoning the `025` reduced target without hard evidence
6. treating computational extraction as a proof without isolating the
   theorem-shaped statement behind it

## Standard pilot discipline

Unless there is a reason not to:

- pilot on `m = 5,7,9`
- use `m = 11` as the first control
- keep the best-seed branch fixed
- save exact JSON summaries
- separate:
  - extracted facts
  - heuristic interpretation
  - failed search facts

## Critical theorem targets

If you are trying to make mathematical progress, these are the best theorem
targets to seek.

### Already extracted, worth proving cleanly

1. Mixed return-map theorem from `019`
2. Reduced perturbation target theorem from `025`
3. Best-seed defect quotient theorem from `033`
4. Corridor phase theorem from `034`
5. Static phase-gate no-go theorem from `035`
6. Corridor lift theorem from `036`
7. Raw odometer theorem from `037`

### Next real targets

8. Localized-carrier theorem
9. Visible-phase no-go theorem
10. Local-to-reduced realization theorem
11. Bridge-to-full-D5 theorem

Useful supporting lemmas:

9. exceptional-slice lemma (`u_source = 3`)
10. delay law lemma
11. orbit-residue lemma
12. small-orbit description lemma

## Expected output style

When starting a new branch, the default output should be:

1. a research note in the `template_to_use.md` format
2. a narrow executable work spec if computation is needed
3. an artifact bundle if real search / extraction is performed
4. an explicit branch recommendation at the end

Good outputs answer:

- what was learned?
- what was pruned?
- what is now the honest next branch?

## Short version

If you remember only one line, remember this:

**Do not search generically. Read the branch as a corridor-local carrier problem
on top of an already-visible raw odometer.**
