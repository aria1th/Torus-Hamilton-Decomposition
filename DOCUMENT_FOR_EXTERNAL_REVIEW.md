## D1) D5 one-old-bit search factorization

**Decision:** For `D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005`, use an exact staged search that enumerates one-layer-active tables first, factors the color-0 Latin stage by active layer, and only forms full two-layer candidates from layer-level Latin survivors.

Options:
1. Enumerate every full two-layer table directly for every old bit and anchor pair.
2. Use an exact staged search:
   one-layer-active exact passes, layer-level Latin survivor tables, then full two-layer clean-frame evaluation only on the Cartesian product of layer-level Latin survivors.
3. Use heuristic sampling or SAT/CP only for a subset of families.

Recommendation:
- Option 2.
- It stays exact on the pilot range, preserves deterministic reproducibility, and removes the avoidable `2^20` brute-force blowup in the full two-layer family.

Risks / mitigations:
- The factorization could be implemented incorrectly -> validate every reported unique survivor on the full torus and all five colors.
- The staged Latin pass could still leave too many full candidates -> save layer-level survivor counts explicitly so the reduction can be audited.

Open questions:
- Whether any one-old-bit family produces a context-dependent clean survivor at all.
- Whether the first success, if any, already appears in a one-layer-active family or only after full two-layer coupling.

Rollout / acceptance:
- Save per-bit and per-family survivor counts.
- Save the unique validated survivors.
- If no context-dependent clean survivor exists, return a clean negative conclusion and the next recommended branch.

## D2) D5 two-old-bit minimal family

**Decision:** For `D5-TWO-OLD-BIT-CYCLE-MONODROMY-006`, start with the exact decoupled two-old-bit family where layer 2 depends only on one old bit, layer 3 depends only on one old bit, and tail bits `phase_align, b1, b2` are excluded.

Options:
1. Reintroduce `phase_align, b1, b2` immediately in the new family.
2. Start with the minimal decoupled two-old-bit family and only add predecessor-tail or tail bits if that family fails.
3. Jump directly to predecessor-tail hybrids.

Recommendation:
- Option 2.
- The exact Session 23 survivor classification says all successful context-dependent rules ignored `phase_align, b1, b2` entirely, so the smallest honest next branch is to decouple the successful `s`-only mechanisms by layer before adding more state.

Risks / mitigations:
- The minimal family may still be too narrow -> include same-bit controls and save per-pair survivor counts so failure is interpretable rather than ambiguous.
- A positive result may still only reproduce cycle-only or monodromy-only behavior -> rank survivors by combined cycle structure and nonzero monodromy, not just by clean/strict status.

Open questions:
- Whether two independent old bits already combine orbit structure and monodromy.
- Whether same-bit controls exhibit cancellation again in this reduced family.

Rollout / acceptance:
- Exhaust the ordered bit-pair family exactly on `m=5,7,9`.
- Validate every reported survivor on the full torus and all five colors.
- If no combined witness exists, the next branch is predecessor-tail on one layer.

## D3) D5 layer-3 alt-2 follow-up scope

**Decision:** For `D5-LAYER3-ALT2-DECOUPLED-007`, search the full exact decoupled two-old-bit family with layer-3 alternate palette `{0,2}` instead of restricting to the 400-rule follow-on seeded only by Session 24 survivors.

Options:
1. Search only the reduced family built from the previously surviving layer-2 patterns.
2. Search the full exact `{0,2}` family: all ordered bit pairs, all layer-2 alternates `{0,3,4}`, both layer-2 orientations, both layer-3 alternates `{0,2}`, both layer-3 orientations.

Recommendation:
- Option 2.
- The full family is still small (`600` rules), and using it avoids baking the Session 24 factorization into the definition of the next branch.

Risks / mitigations:
- The extra 200 rules could be redundant -> save per-pair survivor counts so that redundancy or new behavior is visible in the artifact.
- A negative result could still be misread as too narrow -> keep the family definition explicit in the README and the decision log.

Open questions:
- Whether layer-3 alternate `2` can preserve the cycle mechanism while introducing nonzero monodromy.
- Whether the full family still factors through layer-2 behavior as in Session 24.

Rollout / acceptance:
- Exhaust all `600` rules on `m=5,7,9`.
- Validate every reported clean survivor on the full torus and all five colors.
- If no combined witness exists, recommend a layer-3-only predecessor-tail enrichment.

## D4) D5 layer-3 one-flag mode-switch scope

**Decision:** For `D5-LAYER3-MODE-SWITCH-008`, start with the smallest representative one-extra-flag family: fix layer 2 to the representative bifurcation-capable `q=-1` split with alternate `0`, keep both layer-2 orientations, fix layer-3 old bit to representative `q=-1`, test the named predecessor-flag pool first, and only if that fails widen to an exact predecessor-local-signature one-bit search.

Options:
1. Reopen the full `4 x 4 x 2 x 2` old-bit representative family immediately and add predecessor flags everywhere.
2. Use one representative old-bit family first:
   `s_2 = q=-1`, `s_3 = q=-1`, both layer-2 orientations, one extra layer-3 flag from the named predecessor pool, then exact local-signature fallback.
3. Skip the named flags and jump directly to a two-bit layer-3 local grammar.

Recommendation:
- Option 2.
- Session `007` already showed the live layer-2 and layer-3 old-bit pools collapse to the same regime counts on the pilot range, so the right next question is whether one extra layer-3 flag can create a mixed regime at all. The representative family answers that exactly without paying for a broader search upfront.

Risks / mitigations:
- The note’s predecessor-flag names are not backed by a checked code module -> define their operational formulas explicitly in the new script and README.
- A negative result on the named flag pool could still be an artifact of the chosen formulas -> add the exact predecessor-local-signature fallback in the same artifact.

Open questions:
- Whether any single extra layer-3 flag can combine moving `U_0` cycles with nonzero monodromy on `m=5,7,9`.
- Whether the representative `q=-1` old bits are already enough, or whether a later rerun needs the full four-bit pool `T`.

Rollout / acceptance:
- Exhaust the named one-flag families exactly on `m=5,7,9`.
- Validate every reported clean survivor on the full torus and all five colors.
- If the named flags fail, exhaust an exact one-bit search over the observed predecessor-local signature classes.
- Save per-flag regime counts and a clear next-branch recommendation.

## D5) D5 strong mixed graft scope

**Decision:** For `D5-STRONG-CYCLE-MIX-009`, start with an exact Stage 1 graft search that keeps the successful Session 26 twist gadget fixed and transplants it onto the full exact list of `20` previously validated cycle-capable layer-2 seeds; only if Stage 1 fails to beat the mixed baseline should Stage 2 widen the layer-3 old bit from representative `q=-1` to the full four-bit pool `T`.

Options:
1. Jump directly to the widened Stage 2 family with all four layer-3 old bits in `T`.
2. Run the narrow Stage 1 graft first:
   `20` exact layer-2 seeds, `2` successful predecessor flags, `6` ordered off-diagonal slice pairs, representative layer-3 old bit `q=-1`.
3. Ignore the Session 26 twist gadget and reopen a broader new mixed-family search.

Recommendation:
- Option 2.
- Session 26 already isolated the exact successful twist gadget, so the next honest question is whether that gadget survives on stronger cycle seeds. Stage 1 answers that directly in only `240` exact rules and keeps the interpretation clean if it succeeds.

Risks / mitigations:
- The representative layer-3 old bit `q=-1` might be too narrow -> widen to the full four-bit pool only if Stage 1 fails to improve the cycle profile.
- The new mixed survivors could be numerous -> save exact per-seed and per-gadget rows, then validate every reported clean survivor on the pilot range with optional stability spot-checks on the best ones.

Open questions:
- Whether the Session 26 twist gadget can preserve nonzero monodromy while improving beyond the `m`-cycle mixed baseline.
- Whether the strongest cycle-compression seeds, especially the `w+u=2` / alt-`4` family, remain compatible with the twist gadget.

Rollout / acceptance:
- Exhaust Stage 1 exactly on `m=5,7,9`.
- Compare the best mixed survivor against the stored Session 26 mixed baseline and the strongest earlier cycle-only baseline.
- If no Stage 1 rule beats the mixed baseline, run Stage 2 with the widened layer-3 old-bit pool.
- Validate every reported clean survivor on `m=5,7,9` and spot-check the best survivors on `m=11,13`.

## D6) Lean formalization scope for the current `d=3` and `d=4` proofs

**Decision:** Use Lean selectively: treat the `d=4` proof and the `d=3` odd case as good formalization targets now, but do not make a full Lean formalization of the current `d=3` even Route E proof the primary path until its finite-defect / splice machinery is compressed into a cleaner abstract theorem.

Options:
1. Formalize the current full `d=3` and `d=4` manuscripts in Lean immediately, essentially as written.
2. Formalize the clean proof kernel first:
   full `d=4`, the `d=3` odd case, and the `m=4` finite witness checker; treat the `d=3` Route E even case as decision pending until the defect-itinerary / splice layer is abstracted.
3. Avoid Lean entirely and keep only LaTeX plus Python validation.

Recommendation:
- Option 2.
- The current `d=4` proof is already close to Lean-native structure: an explicit witness, explicit return maps, a second-return reduction, affine conjugacy to an odometer, and two lifting lemmas.
- The `d=3` odd case has the same favorable shape: closed-form maps plus modular cycle arguments.
- The current `d=3` even proof is mathematically formalizable, but as written it would force Lean to encode a large amount of low-level itinerary bookkeeping and splice-block administration before delivering conceptual payoff.

Risks / mitigations:
- A full Route E formalization now could become a proof-engineering sink -> first package the finite-defect affine-itinerary and splice-permutation mechanism as reusable abstract lemmas.
- Fresh Lean adoption would add project setup and mathlib-learning overhead -> keep the first milestone small and theorem-shaped, with `d=4` as the pilot.
- The `m=4` boundary case is currently archived as an explicit table plus Python checker -> either import the witness as data and prove the checker correct in Lean, or keep it as an external audited certificate until the main infinite-family kernel is formalized.

Open questions:
- Whether the current Route E appendices can be replaced by a concise general finite-defect / splice theorem that Lean can consume cleanly.
- Whether the `m=4` witness should be re-proved internally in Lean or accepted as an external finite certificate.
- Whether the formalization goal is only trusted verification, or also a reusable library for higher-dimensional torus return maps.

Rollout / acceptance:
- Create a minimal Lean project and encode the torus, layer function, return maps, and cycle-lifting lemmas.
- Formalize the full `d=4` theorem end to end.
- Formalize the `d=3` odd theorem end to end.
- Add either a Lean checker or a clearly documented external certificate path for the `m=4` witness.
- Reassess the `d=3` even Route E branch only after the abstract finite-defect / splice interface is stated cleanly enough that the Lean proof is mostly theorem application rather than itinerary transcription.

## D7) D5 shared predecessor interaction scope

**Decision:** For `D5-SHARED-PRED-INTERACTION-010`, run the exact shared-predecessor interaction family in two stages: Stage 1 uses only the strong alt-`4` layer-2 modes on the shared predecessor switch, and Stage 2 widens minimally by adding four representative non-alt-`4` `q=-1` layer-2 modes if Stage 1 fails to beat the mixed baseline.

Options:
1. Search only the strong alt-`4` shared-switch family from the note and stop there.
2. Run the strong alt-`4` shared-switch family first, then widen one notch to a minimal representative non-alt-`4` layer-2 pool only if needed.
3. Reopen the full previously validated non-alt-`4` layer-2 seed list immediately.

Recommendation:
- Option 2.
- Stage 1 is the exact smallest interactive family suggested by the `009` separability diagnosis. If it fails, a minimal representative widening is enough to test whether genuine layer-2/layer-3 interaction needs mixed strong/simple cycle modes, without paying for the full earlier seed pool.

Risks / mitigations:
- The note’s Stage 2 widening is under-specified -> make it explicit in the codex work spec and README as the four representative `q=-1` modes `0/2, 2/0, 2/3, 3/2`.
- A negative result on the representative widening could still be accused of being too narrow -> save exact survivor counts by predecessor flag, layer-2 slice pair, and layer-3 gadget so the failure mode is inspectable.

Open questions:
- Whether a shared predecessor switch can break the universal `m`-cycle collapse of `009`.
- Whether the strong alt-`4` cycle mechanism and the Session `008/009` twist gadget can coexist once both layers respond to the same local flag.
- If Stage 2 still fails, whether the right next move is a theorem-level separability statement or a broader genuinely interactive family.

Rollout / acceptance:
- Exhaust Stage 1 exactly on `m=5,7,9`.
- If no Stage 1 rule improves the mixed baseline, exhaust the minimal Stage 2 widening exactly on `m=5,7,9`.
- Validate every reported clean survivor on the full torus and all five colors.
- Save exact summaries by predecessor flag, layer-2 slice pair, and layer-3 gadget, plus stability spot-checks on the best mixed survivors.

## D8) D5 layer-2 geometry under fixed twist scope

**Decision:** For `D5-LAYER2-GEOMETRY-UNDER-FIXED-TWIST-011`, Stage 1 searches only the layer-2 geometry family under one canonical fixed twist gadget, and treats the sign-reversed twist only as an auxiliary control comparison; Stage 2 reopens the full layer-3 twist family only around any Stage 1 layer-2 geometry rules that actually improve the mixed baseline.

Options:
1. Search Stage 1 with both twist signs folded into the main family.
2. Search Stage 1 with one canonical fixed twist, keep the sign-reversed twist only as a control comparison, and only widen layer 3 if Stage 1 finds actual geometry improvement.
3. Skip the fixed-twist reduction and reopen the full shared layer-2/layer-3 family immediately.

Recommendation:
- Option 2.
- Session `010` already says the geometry action in the searched family is layer-2-driven and independent of layer-3 bit/pair once the layer-2 pair and predecessor flag are fixed. So the honest next question is whether any layer-2 geometry rule can beat the baseline under one exact mixed twist. The sign-reversed twist is still useful as a check, but it should not double the main search or blur the primary branch answer.

Risks / mitigations:
- A single canonical twist might hide a geometry improvement that only appears at the opposite sign -> run the sign-reversed twist as an auxiliary control on the same layer-2 family and save the comparison.
- If Stage 1 finds no improvement, users may still worry that layer 3 was frozen too aggressively -> keep Stage 2 coded and documented as the conditional follow-up only when Stage 1 produces an actually better geometry rule.

Open questions:
- Whether any layer-2 predecessor-flag plus slice-pair rule can reduce pilot cycle count below `21` while keeping nonzero monodromy under the canonical twist.
- Whether any geometry improvement that appears under the canonical twist survives the full layer-3 twist family.
- If Stage 1 fails, whether the next live branch is a richer layer-2 local state rather than more layer-3 widening.

Rollout / acceptance:
- Exhaust the `2 x 8 x 8 = 128` canonical-twist Stage 1 rules exactly on `m=5,7,9`.
- Run the sign-reversed control twist on the same layer-2 family and save the comparison.
- If Stage 1 finds any improved geometry rules, run Stage 2 on those rules across the full live layer-3 bit/pair family.
- Validate every reported clean survivor on the full torus and all five colors, with stability spot-checks on the best mixed survivors.

## D9) D5 three-flag layer-2 state widening under fixed twist

**Decision:** For `D5-ALT4-THREE-FLAG-GEOMETRY-013`, keep the canonical mixed twist gadget fixed, keep the pure alt-`4` layer-2 mode pool fixed, and widen only the layer-2 local state by testing one extra named predecessor flag at a time: first `pred_any_phase_align`, then `pred_sig0_phase_align`.

Options:
1. Reopen the widened Session `012` layer-2 mode pool together with the larger state space.
2. Freeze twist and freeze the pure alt-`4` layer-2 pool, then exhaust the two exact three-flag eight-state families separately.
3. Skip the named-flag widening and jump directly to exact predecessor-tail local-signature state on layer 2.

Recommendation:
- Option 2.
- Session `012` already showed two important exact facts: the pure alt-`4` family is fully admissible and genuinely geometry-active, while widening the layer-2 mode pool adds no positive mixed regime. So the smallest honest next branch is to widen only the local state and leave both twist and mode palette unchanged.

Risks / mitigations:
- The extra named flags might still be too coarse -> save exact per-flag regime histograms, dependence-class summaries, and representative survivors so failure distinguishes “no effect” from “wrong-sign effect”.
- The full `2 x 4^8 = 131072` search is large enough that naive full-color evaluation is wasteful -> run the exact search on color-0 return dynamics under cyclic equivariance, then do full-color validation on the reported frontier and stability spot-checks.

Open questions:
- Whether either named three-flag family can beat the mixed baseline total `21` while preserving nonzero monodromy.
- Whether the best surviving tables genuinely use the full eight-state partition or collapse to a smaller effective dependence class.
- If both named flags fail, whether the right next branch is an exact predecessor-tail local-signature bit on layer 2.

Rollout / acceptance:
- Exhaust both three-flag eight-state families exactly on `m=5,7,9`.
- Save compact JSON rows for all tested assignments, plus aggregate regime and dependence-class summaries by extra flag.
- Full-color validate the reported frontier and spot-check the best survivors on `m=11,13` plus sign-reversed control twist.
- If neither named flag improves the baseline, recommend the exact predecessor-tail local-signature follow-up explicitly.

## D10) D5 exact-signature diagnostic versus coupled controller scope

**Decision:** For `D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014`, do not promote a broad layer-2-only exact-signature table search as the main branch. First run a short exact sterility diagnostic on the fixed-twist / pure-alt-4 branch, then use the extracted exact bit as a coupled layer-3 controller in a small mode-switch family, with only a tiny synchronized layer-2 flip as fallback.

Options:
1. Make the old `014` plan the main branch: a larger layer-2-only exact-signature search under fixed twist and pure alt-4.
2. Run a short exact diagnostic on the true predecessor-tail signature, then pivot immediately to a coupled layer-3 mode-switch controlled by the extracted exact bit.
3. Skip the exact diagnostic and jump directly to a broader two-layer local-signature family.

Recommendation:
- Option 2.
- Session `013` already shows that richer layer-2-only refinements can survive clean/strict while producing no new pilot regime. The right next question is therefore not “how many more layer-2 states can survive,” but “whether the exact new local bit can change the return dynamics once it is allowed to control twist.” A short diagnostic still keeps the exact-signature branch honest before pruning it.

Risks / mitigations:
- The exact signature could still hide more than one genuinely new bit -> extract the full exact class table first and record how it sits over the named partition before choosing the coupled controller.
- The coupled layer-3 family could be too weak with layer 2 held fixed -> include a very small synchronized layer-2 flip fallback, but do not reopen a general layer-2 table search in the same session.

Open questions:
- Whether the exact predecessor-tail signature adds any pilot-return information beyond the named three-flag partition in the fixed-twist branch.
- Whether the extracted exact bit can improve mixed cycle compression once it controls layer-3 mode.
- Whether a tiny synchronized layer-2 flip is enough if pure layer-3 coupling still fails.

Rollout / acceptance:
- Save the exact signature class table and its quotient by the named flags.
- Run the short sterility diagnostic on `m=5,7,9`.
- If the diagnostic is negative, state that pruning result explicitly for the old layer-2-only exact-signature branch.
- Exhaust the small coupled mode-switch family exactly on `m=5,7,9`.
- Validate every reported clean survivor on the full torus and all five colors, with stability spot-checks on `m=11,13` and sign-reversed control-twist checks on the best survivors.

## D11) D5 synchronized exact-bit use around the live `wu2` gadget

**Decision:** For `D5-SYNCHRONIZED-WU2-EXACT-016`, do not reopen larger one-bit exact refinements of the fixed-base `wu2` branch. Instead, test the last small exact-bit role that is still structurally live: a minimally synchronized two-layer family where the same controller state `(r,p)` drives layer-3 mode and also flips layer-2 orientation on the active `wu2` slice.

Options:
1. Reopen broader one-layer exact-bit refinements around the `wu2` gadget.
2. Keep the live `wu2` controller and let the exact bit act only in a minimally synchronized two-layer role:
   fixed inactive slice, active-slice `p`-dependent layer-2 flip, and a `3^4` layer-3 mode table on `(r,p)`.
3. Skip this synchronized exact-bit test and jump directly to a second exact local bit or a larger exact local-signature state.

Recommendation:
- Option 2.
- `014A`, `014B`, and `015` already form a clean pruning chain against one-layer uses of `pred_sig1_phase_align`: it is locally real, but sterile as a layer-2-only refinement, sterile as a standalone layer-3 controller, and sterile as a one-bit secondary refinement inside the live `wu2` gadget. The only still-plausible small role is therefore synchronized use on geometry and twist together. That is the smallest honest next branch before paying for a second exact bit.

Risks / mitigations:
- The synchronized family may still be too weak -> stage the search by old-bit width, starting with `q+u=-1` and widening to `{q+u=1, q+u=-1, u=-1}` only if Stage 1 finds no improved mixed rule.
- Clean survivors may exist but only reproduce the old baseline -> compare every clean strict mixed survivor explicitly against the Session `008` mixed baseline total `21` and the earlier cycle-only baseline total `15`.
- The exact bit may survive only syntactically while layer-3 tables ignore it -> save layer-3 dependence classes alongside the combined synchronized rule rows.

Open questions:
- Can the exact bit survive only when it acts on geometry and twist together?
- Does the synchronized layer-2 flip produce any clean strict mixed witness with total pilot cycle count `< 21`?
- If the synchronized family still fails, is the exact bit effectively exhausted in the current local neighborhood?

Rollout / acceptance:
- Fix anchors `0 -> 1`, `1 -> 4`, `4+ -> 0`.
- Exhaust Stage 1 exactly on `m=5,7,9` with:
  `2` bases x `2` controller flags x `1` old bit x `2` synchronized flip patterns x `3^4` layer-3 tables.
- Run Stage 2 only if Stage 1 has no improved mixed rule.
- Validate every reported clean survivor on the full torus and all five colors.
- Save survivor counts by base, controller flag, old bit, flip pattern, and layer-3 table, plus stability spot-checks on `m=11,13` and sign-reversed control-twist checks on the best survivors.

## D12) D5 phase shift from local-family search to return-map extraction

**Decision:** For `D5-RETURN-MAP-MODEL-017`, stop treating broader local-family widening as the main branch. Use the exact witness chain through `016` as quotient discovery, fix a small witness set, and make return-map extraction the primary task: section, first return, grouped return, reduced state, and candidate canonical model.

Options:
1. Continue broadening local families near the current `wu2` mixed gadget.
2. Treat `005`–`016` as quotient discovery and pivot to return-map extraction on a fixed witness set.
3. Jump directly to a conjectural theorem-level D5 normal form without building an exact extraction artifact first.

Recommendation:
- Option 2.
- The recent chain has already done the expensive local pruning work: it found the live mixed mechanism, identified robust controls, and ruled out many fake or sterile one-bit coordinates. After `016`, more broad widening in the same local neighborhood is unlikely to be informative. The honest next move is to extract the reduced return dynamics that those searches have been circling around.

Risks / mitigations:
- The first return may still be too noisy -> analyze both raw first return and the natural grouped return `U = R^m|_{q=0}` before escalating to bigger grouped-return experiments.
- The extracted quotient may depend on witness choice -> use a fixed comparison set: mixed, cycle-only, monodromy-only, and anti-compressive mixed witnesses.
- The analysis could drift into vague pattern recognition -> save exact state tables, exact transition tables, and exact affine / invariant checks, not just prose conclusions.

Open questions:
- Whether the right D5 normal form lives at raw first return or at grouped return.
- Whether the mixed witness base is an odometer, a skew-odometer, or a finite-state carry automaton.
- Which reduced coordinates are structural and which are just artifacts of a particular witness encoding.

Rollout / acceptance:
- Fix a witness set from existing validated artifacts.
- Extract exact first-return and grouped-return tables on `m=5,7,9`, with spot-checks on `m=11,13`.
- Save low-layer trace words, return increments, grouped-return maps, minimal deterministic quotients, and affine / linear-form checks.
- If a canonical reduced model is visible, state it explicitly.
- If not, return the sharpest obstruction and the next missing coordinate or grouped-return candidate.

## D13) Lean strategy for the current `d=3` even case

**Decision:** Treat `formal/TorusD3Draft/d3torus_lean_draft.zip` as an architectural outline only, not a bypass; continue the current `d=3` even Lean work with a hybrid strategy: keep Route E color `2` on the direct return-map path, introduce an abstract splice theorem for colors `1` and `0`, use reflection / `decide` only for bounded finite checks, and keep any new gauge-style proof as a parallel research branch rather than the main delivery path.

Options:
1. Follow the draft archive as if it already resolves the Lean bottleneck.
2. Continue direct symbolic formalization of the current Route E proof, but improve proof engineering:
   reflection for bounded finite steps, `omega` for interval arithmetic, and an abstract splice theorem for colors `1/0`.
3. Stop formalizing the current even proof and first search for a brand new clean `d=3` gauge-style proof.

Recommendation:
- Option 2.
- The archive is useful, but it is only a stubbed module plan plus comments; it does not contain definitions, formulas, or proofs that bypass the current obstacle.
- Reflection is useful only in a bounded role. It can discharge finite tables, fixed small orbit prefixes, and the `m = 4` witness, but it does not by itself prove the parameterized `m ≥ 6` orbit segments whose lengths depend on `m`.
- The strongest bypass for the current proof is to separate splice closure from geometry. That should let colors `1` and `0` consume a theorem instead of re-encoding itinerary bookkeeping inline.
- A brand new clean proof could be best long-term, but it is still a mathematics project, not a short Lean refactor.

Risks / mitigations:
- Direct Route E transcription may still bog down in branch collisions for small moduli -> state the 2D Route E lemmas under the true regime `m ≥ 6` and build explicit nat-cast nonvanishing helpers before long orbit traces.
- Reflection may be over-trusted -> reserve `decide` / `native_decide` for genuinely closed finite checks and keep generic orbit blocks on symbolic lemmas like `G^[n]`.
- The splice abstraction could be too weak or too paper-specific -> formulate it as a permutation-level theorem on arithmetic family blocks, independent of Route E coordinates.
- A new gauge proof could consume time without landing -> keep it as a parallel exploratory branch until it yields a clearly simpler return-map theorem.

Open questions:
- What is the cleanest permutation-level statement that captures the current splice closure for colors `1` and `0`?
- Whether Route E color `2` should remain on the current explicit-coordinate path, or also be refactored through a stronger generic first-return theorem.
- Whether a genuine `d=3` even gauge/odometer reduction exists that materially shortens the current even proof rather than merely rephrasing it.

Rollout / acceptance:
- Keep the current verified base for `TorusD3Even/Counting.lean` and `TorusD3Even/Color2.lean`.
- Finish color `2` under the explicit `m ≥ 6` Route E assumptions.
- Design and prove a stand-alone splice-permutation theorem for colors `1` and `0`.
- Use reflection only where the terms are genuinely closed and finite.
- Reassess the “new clean proof” branch only if it produces a demonstrably shorter theorem kernel than Route E plus splice abstraction.

Immediate working reminder for the next Lean session:
- Read `formal/LEAN_KNOWHOW.md`, especially the `D3 even color-2 status` note and its warning that the branch lemmas must be stated under the real regime `m ≥ 6`.
- Read `formal/TorusD3Even/Color2.lean`; this is the active file, and the verified bridge currently stops at the easy theorem `firstReturn_zero`.
- Read `formal/TorusD3Even/Counting.lean`; the endgame for color `2` is to instantiate `firstReturn_counting` with `F := R2xy`, `embed := linePoint`, `T := T2`, `rho := rho2`, `M := m`, and `x0 := 0`.
- Read `tex/d3torus_complete_m_ge_3_editorial_revision_reworked_forced_repair_v2.tex`, the color-`2` proposition and corollary giving the seven return cases, the formulas for `T_2` and `rho_2`, and the final `m^2`-cycle conclusion.
- Read `anc/routee_first_return_check.py` as the external regression checker for the displayed `T2` / `rho2` formulas.

Immediate theorem target for color `2`:
- Stay on the direct explicit-coordinate path in `formal/TorusD3Even/Color2.lean`.
- Under the explicit even Route E assumptions `m ≥ 6`, treat the boundary values `x = 1`, `x = 2`, `x = 4`, `x = 6`, `x = m - 2`, and `x = m - 1` separately, then prove the symbolic odd generic family `3 ≤ x ≤ m - 3` and the symbolic even generic family `8 ≤ x ≤ m - 4`.
- Build the helper layer first: nat-cast nonvanishing / separation for `3`, `4`, `m - 3`, `m - 4`, characterization of `Set.range linePoint`, and the no-early-return facts needed for the `hfirst` hypothesis in `firstReturn_counting`.
- Use symbolic orbit blocks such as `G^[n]` and the existing branch lemmas, rather than trying to close the long generic segments by brute-force `simp` or unrestricted reflection.

Progress checkpoint after the current Lean session:
- `formal/TorusD3Even/Color2.lean` now compiles with the helper layer for `linePoint` range / injectivity and the nat-cast separation lemmas needed for the true `m ≥ 6` regime.
- The `x = 1` color-`2` case is no longer just a return equality: the file now contains the orbit-segment lemmas behind it, `firstReturn_one`, and the matching no-early-return lemma `hfirst_one`.
- The `x = 2` color-`2` case is now also packaged end-to-end. The file contains the intermediate checkpoint lemmas
  `(R2xy^[m-2])(2,0) = (m-1,2)`,
  `(R2xy^[m-1])(2,0) = (0,2)`,
  `(R2xy^[m])(2,0) = (1,1)`,
  `(R2xy^[m+1])(2,0) = (1,m-1)`,
  `(R2xy^[m+2])(2,0) = (1,m-2)`,
  plus `firstReturn_two` and `hfirst_two`.
- The `x = m - 1` boundary case is now also formalized and compiling, including the short three-step entry orbit, the generic tail from `(0,m-3)` to `(m-4,1)`, `firstReturn_m_sub_one`, and `hfirst_m_sub_one`.
- The `x = 4` boundary case is now formalized and compiling in the corrected split form:
  `m = 6` is discharged by an explicit finite proof, while the symbolic orbit
  `(4,0) -> (5,m-1) -> (5,m-2) -> G^(m-6) -> (m-1,4) -> E -> (0,4) -> G^2 -> (2,2) -> A -> (3,0)`
  is only used under the honest regime `m >= 8`. The file now contains `firstReturn_four` and `hfirst_four`.
- The `x = 6` boundary case is now also formalized and compiling in the analogous split form:
  `m = 8` is discharged by an explicit finite proof, while for `m >= 10` the symbolic orbit
  `(6,0) -> (7,m-1) -> (7,m-2) -> G^(m-8) -> (m-1,6) -> E -> (0,6) -> G^3 -> (3,3) -> D -> (3,1) -> B -> (5,0)`
  is used. The file now contains `firstReturn_six` and `hfirst_six`.
- The generic even family has now been started in natural-`x` form. `formal/TorusD3Even/Color2.lean` contains reusable front-half lemmas for even `x` with `8 ≤ x ≤ m - 4`: the initial `G/C` entry, the generic segment to `(m-1,x)`, and the endpoint theorem
  `(R2xy^[m-x])(x,0) = (m-1,x)`.
  The remaining generic-even work is the second half:
  `(m-1,x) -> E -> (0,x) -> G^(x/2) -> (x/2,x/2) -> D -> G^(x/2-3) -> (x-3,1) -> B -> (x-1,0)`,
  together with the no-early-return proof in the same natural-`x` parameterization.
- Update: that generic-even second half is now also formalized and compiling. `formal/TorusD3Even/Color2.lean` contains both `firstReturn_even_generic` and `hfirst_even_generic`, and the reusable zero/half/tail lemmas were relaxed to the honest range they need (`x ≤ m - 2`) so they can be reused by later boundary cases.
- The `x = m - 2` boundary case is now formalized and compiling as well. The checked symbolic orbit is
  `(m-2,0) -> (m-1,m-1) -> (0,m-1) -> (0,m-2) -> G^((m-2)/2) -> ((m-2)/2,(m-2)/2) -> D -> ((m-2)/2,(m-6)/2) -> G^((m-8)/2) -> (m-5,1) -> B -> (m-3,0)`.
  The important reminder is that the correct breakpoint is `(m-5,1)`, not `(m-4,1)`.
- Update: the generic odd family `3 ≤ x ≤ m - 3` is now also formalized and compiling, including the three-block decomposition
  `(x+1,-2) -> (d,d)`, `(d,d-2) -> (m-1,x-2)`, and `(0,x-2) -> (x-3,1)`,
  plus `firstReturn_odd_generic` and `hfirst_odd_generic`.
- Color `2` is now formally closed end-to-end in `formal/TorusD3Even/Color2.lean`: the file contains the global dispatch theorems `hreturn` and `hfirst`, the counting input `hsum`, and the final cycle theorem `cycleOn_color2 : CycleOn (m^2) R2xy (linePoint 0)`.
- For later reread before touching colors `1/0`, use:
  `formal/TorusD3Even/Color2.lean`, `formal/TorusD3Even/Counting.lean`, `formal/LEAN_KNOWHOW.md`, and this note’s `D6` / `D13` entries.
- The direct Route-E transcription task for color `2` should now be treated as complete. The next real design work is the abstract splice-permutation theorem for colors `1` and `0`, not more itinerary transcription here.
- Update: `formal/TorusD3Even/Color1.lean` is now theorem-complete for the manuscript’s splice row `T_1, m ≡ 2 (mod 6)` from Proposition `routeE-splice` item `(ii)`. The file contains the common lane map `T1CaseI`, the return-time function `rho1CaseI`, the block data
  `F11 = (0,2,5,...,m-3)`, `F12 = (1,4,7,...,m-1)`, `F13 = (3,6,9,...,m-2)`, the sigma encoding / inverse / equivalence layer, the inside-block and wrap lemmas, and the final cycle theorem `cycleOn_T1CaseIModTwo`.
- Verification checkpoint: `lake build TorusD3Even.Color1` and `lake build TorusD3Even` both succeed after this completion. Remaining output is linter cleanup only, not missing proof content.
- Update: the first reusable splice-side proof-engineering layer is now in `formal/TorusD3Even/Splice.lean`. Besides the abstract cycle theorem, the file now contains arithmetic block encodings
  `affinePoint`, `headAffinePoint`, and `tailAffinePoint`, with value and injectivity lemmas. This is the right first abstraction for the remaining color `1/0` rows because the current bottleneck is repeated block encoding, not the global cycle theorem itself.
- Scope control: do not jump straight to a full “lane map = bulk translation plus finitely many exceptions” theorem yet. The next residue class already shows that a one-tail exception block (`...,m-3,1`) is the immediate reuse point, so the profitable order is:
  pure arithmetic block -> arithmetic block with one exceptional head/tail -> only then reconsider a global finite-exception lane-map theorem.
- Update: `formal/TorusD3Even/Color1.lean` is now theorem-complete for Proposition `routeE-splice` item `(iii)`, namely `T_1, m ≡ 0 (mod 6)`. The file now contains the block data
  `F11 = (0,2,5,...,m-1)`, `F12 = (3,6,9,...,m-3,1)`, `F13 = (4,7,10,...,m-2)`, the block-size arithmetic, sigma encoding, cardinality / injectivity / equivalence layer, the inside-block successor theorem `pointT1CaseIModZero_step`, the wrap theorem `pointT1CaseIModZero_wrap`, and the final cycle theorem `cycleOn_T1CaseIModZero`.
- Verification checkpoint: `lake build TorusD3Even.Color1` and `lake build TorusD3Even` both succeed after this completion. Remaining output is linter cleanup only.
- Concrete next splice target: stay on color `1` and formalize Proposition `routeE-splice` item `(iv)`, namely `T_1, m ≡ 4 (mod 6)` with
  `F11 = (0,2,5,11,...,m-5,1)`, `F12 = (3,9,15,...,m-1,7,13,...,m-3)`, `F13 = (4,6,8,...,m-2)`.
- New abstraction frontier: the current arithmetic-block layer is sufficient for items `(ii)` and `(iii)`, but item `(iv)` is the first row that genuinely wants a two-piece block representation or a small block-concatenation helper inside `formal/TorusD3Even/Splice.lean`. Do not jump to the color-`0` rows before deciding that representation.
- Update: the first `T_1, m ≡ 4 (mod 6)` scaffold is now in `formal/TorusD3Even/Color1.lean` and compiles. It contains the Case-II lane map `T1CaseII`, the block-size arithmetic `qCaseIIModFour` / `lenT1CaseIIModFour`, the two-piece block encodings based on `appendPoint`, named block functions for the three splice rows, the cardinality theorem, the Case-II special-value lemmas, and the piecewise block-value / piece-injectivity lemmas.
- Update: the `cast`-transport issue is now solved by a small reusable helper in `formal/TorusD3Even/Splice.lean` (`castFinFun` plus `castFinFun_injective`). The row `(iv)` named block functions in `formal/TorusD3Even/Color1.lean` now use that helper explicitly instead of burying type-transport inside `rw` / `simpa`, and the block-level injectivity layer compiles cleanly again.
- Resolved row `(iv)` proof-engineering frontier: the cross-block disjointness, sigma injectivity / equivalence layer, inside-block successor theorem, and wrap theorem are now all in `formal/TorusD3Even/Color1.lean`.
- Update: `formal/TorusD3Even/Color1.lean` is now theorem-complete for Proposition `routeE-splice` item `(iv)`, namely `T_1, m ≡ 4 (mod 6)`. The file now contains the Case-II lane map `T1CaseII`, the block data
  `F11 = (0,2,5,11,...,m-5,1)`, `F12 = (3,9,15,...,m-1,7,13,...,m-3)`, `F13 = (4,6,8,...,m-2)`, the named block encoding and sigma equivalence layer, the inside-block successor theorem `pointT1CaseIIModFour_step`, the wrap theorem `pointT1CaseIIModFour_wrap`, and the final cycle theorem `cycleOn_T1CaseIIModFour`.
- Verification checkpoint: `lake build TorusD3Even.Color1` and `lake build TorusD3Even` both succeed after the row `(iv)` closure. Remaining output is linter cleanup only.
- Updated color-`1` status: Proposition `routeE-splice` items `(ii)`–`(iv)` are now all formally closed in `formal/TorusD3Even/Color1.lean`.
- Concrete next splice target: move to color `0`, starting with Proposition `routeE-splice` item `(v)` for
  `T_0, m ≡ 0,2 (mod 6)`, since the color-`1` direct splice work is now complete.
- Update: `formal/TorusD3Even/Color0.lean` is now theorem-complete for Proposition `routeE-splice` item `(v)`, namely
  `T_0, m ≡ 0,2 (mod 6)`. The file now contains the Case-I lane map `T0CaseI`, the block data
  `F_{0,1} = (0,m-2)`, `F_{0,2} = (1,3,5,...,m-3)`, `F_{0,3} = (2,4,6,...,m-4)`, `F_{0,4} = (m-1)`,
  the sigma encoding / injectivity / equivalence layer, the inside-block successor theorem
  `pointT0CaseIModZeroTwo_step`, the wrap theorem `pointT0CaseIModZeroTwo_wrap`, and the final cycle theorem
  `cycleOn_T0CaseIModZeroTwo`.
- Integration note: importing `formal/TorusD3Even/Color0.lean` into `formal/TorusD3Even.lean` required naming the local
  `Fact (0 < 4)` instance explicitly (`instFactZeroLtFour`) so it no longer collides with the generated name from
  `formal/TorusD3Even/Color1.lean` during the top-level import replay.
- Verification checkpoint: `lake build TorusD3Even.Color0` and `lake build TorusD3Even` both succeed after the row `(v)`
  closure. Remaining output is linter cleanup only.
- Updated color-`0` status: Proposition `routeE-splice` item `(v)` is formally closed in `formal/TorusD3Even/Color0.lean`.
- Concrete next splice target: continue in `formal/TorusD3Even/Color0.lean` with Proposition `routeE-splice` item `(vi)`,
  namely `T_0, m ≡ 10 (mod 12)` with
  `F_{0,1} = (0,m-2,5,9,...,m-1,1)`, `F_{0,2} = (4,8,...,m-6)`, `F_{0,3} = (3,7,...,m-3)`,
  `F_{0,4} = (2,6,...,m-4)`.
- Expected proof-engineering reuse for row `(vi)`: reread `formal/TorusD3Even/Color0.lean`,
  `formal/TorusD3Even/Color1.lean` item `(iv)`, `formal/TorusD3Even/Splice.lean`, and manuscript row `(vi)` at
  `tex/d3torus_complete_m_ge_3_editorial_revision_splice_integrated.tex`. The likely reusable pattern is one exceptional
  multi-piece block plus three pure arithmetic stride blocks; do not jump to a bigger global lane-map abstraction unless
  row `(vi)` genuinely forces it.
- Update: the first row `(vi)` scaffold now compiles in `formal/TorusD3Even/Color0.lean`. The file now contains the
  shared Case-II lane map `T0CaseII`, the residue-class arithmetic helpers `eq_twelve_mul_add_ten_of_mod_twelve_eq_ten`
  and `qCaseIIModTen`, the block-size data `lenT0CaseIIModTen`, the block encoding
  `pointT0CaseIIModTen` / `pointT0CaseIIModTenSigma`, and the cardinality theorem
  `card_splicePoint_lenT0CaseIIModTen`.
- Exact next row `(vi)` proof frontier: prove the block-value lemmas for the exceptional block
  `F_{0,1} = (0,m-2,5,9,...,m-1,1)`, then the block injectivity / cross-block disjointness layer, and only after that
  the sigma equivalence, `step`, and `wrap` theorems. The current scaffold is intended to keep that next pass local to
  `formal/TorusD3Even/Color0.lean`.
- Verification checkpoint: after adding the row `(vi)` scaffold, `lake build TorusD3Even.Color0` and
  `lake build TorusD3Even` both still succeed. Remaining output is linter cleanup only.
- Update: Proposition `routeE-splice` item `(vi)`, namely `T_0, m ≡ 10 (mod 12)`, is now theorem-complete in
  `formal/TorusD3Even/Color0.lean`. The file now contains the Case-II block data
  `F_{0,1} = (0,m-2,5,9,...,m-1,1)`, `F_{0,2} = (4,8,...,m-6)`, `F_{0,3} = (3,7,...,m-3)`,
  `F_{0,4} = (2,6,...,m-4)`, together with the sigma encoding / injectivity / equivalence layer, the inside-block
  successor theorem `pointT0CaseIIModTen_step`, the wrap theorem `pointT0CaseIIModTen_wrap`, and the final cycle theorem
  `cycleOn_T0CaseIIModTen`.
- Verification checkpoint: `lake build TorusD3Even.Color0` and `lake build TorusD3Even` both succeed after the row `(vi)`
  closure. Remaining output is linter cleanup only.
- Updated color-`0` status: Proposition `routeE-splice` items `(v)` and `(vi)` are formally closed in
  `formal/TorusD3Even/Color0.lean`.
- Concrete next splice target: stay in `formal/TorusD3Even/Color0.lean` and finish Proposition `routeE-splice`
  item `(vii)`, namely `T_0, m ≡ 4 (mod 12)` with
  `F_{0,1} = (0,m-2,5,9,...,m-3)`, `F_{0,2} = (2,6,...,m-6)`, `F_{0,3} = (3,7,...,m-1,1)`,
  `F_{0,4} = (4,8,...,m-4)`.
- Update: the row `(vii)` block model now compiles in `formal/TorusD3Even/Color0.lean`. The file contains the residue
  arithmetic `eq_twelve_mul_add_four_of_mod_twelve_eq_four` / `qT0CaseIIModFour`, the block-size data
  `lenT0CaseIIModFour`, the concrete block maps `pointT0CaseIIModFour`, the cardinality theorem
  `card_splicePoint_lenT0CaseIIModFour`, the sigma injectivity / equivalence layer
  `pointT0CaseIIModFourSigma_injective` / `spliceEquivT0CaseIIModFour`, and the endpoint-value lemmas needed for the
  remaining dynamics.
- Exact row `(vii)` proof frontier: the missing theorems are now only the dynamic layer for the already-encoded blocks:
  `pointT0CaseIIModFourZero_step`, `pointT0CaseIIModFourOne_step`, `pointT0CaseIIModFourTwo_step`,
  `pointT0CaseIIModFourThree_step`, the dispatcher `pointT0CaseIIModFour_step`, the wrap theorem
  `pointT0CaseIIModFour_wrap`, and the final cycle theorem `cycleOn_T0CaseIIModFour`.
- Local proof-engineering recommendation for row `(vii)`: keep the current block encoding and finish the dynamics by case
  splits on the few exceptional indices rather than introducing a new global abstraction. The remaining obstacles are
  local `Fin` normalization / `omega` obligations in `formal/TorusD3Even/Color0.lean`, not a new mathematical pattern.
- Update: Proposition `routeE-splice` item `(vii)`, namely `T_0, m ≡ 4 (mod 12)`, is now theorem-complete in
  `formal/TorusD3Even/Color0.lean`. The file now contains the block data
  `F_{0,1} = (0,m-2,5,9,...,m-3)`, `F_{0,2} = (2,6,...,m-6)`, `F_{0,3} = (3,7,...,m-1,1)`,
  `F_{0,4} = (4,8,...,m-4)`, together with the inside-block successor theorem
  `pointT0CaseIIModFour_step`, the wrap theorem `pointT0CaseIIModFour_wrap`, and the final cycle theorem
  `cycleOn_T0CaseIIModFour`.
- Updated color-`0` status: Proposition `routeE-splice` items `(v)`–`(vii)` are now all formally closed in
  `formal/TorusD3Even/Color0.lean`.
- Updated D3-even Route-E status: combined with `formal/TorusD3Even/Color1.lean`,
  `formal/TorusD3Even/Color2.lean`, `formal/TorusD3Even/Splice.lean`, and
  `formal/TorusD3Even/Counting.lean`, the current Lean package for the `d = 3` even Route-E case should now be treated
  as complete. Verification checkpoint: `lake build TorusD3Even.Color0` and `lake build TorusD3Even` both succeed;
  remaining output is linter cleanup only.
- Important boundary correction before formalizing `x = 4`: the first-return formula still passes the checker at `m = 6`, but the manuscript’s displayed orbit is not literally valid there. At `m = 6`, the actual orbit is
  `(4,0) -> (5,5) -> (0,5) -> (0,4) -> (1,3) -> (2,2) -> (3,0)`,
  so the printed step `(m-1,4) -> E -> (0,4)` only matches the symbolic branch analysis for `m >= 8`.
- Current Lean recommendation for `x = 4`: split off the `m = 6` border case explicitly and keep the symbolic `G^{m-6}` / `E` proof only under the sharper regime `m >= 8`.
- Parallel boundary correction for `x = 6`: at `m = 8`, the actual orbit is
  `(6,0) -> (7,7) -> (0,7) -> (0,6) -> (1,5) -> (2,4) -> (3,3) -> (3,1) -> (5,0)`,
  so the symbolic front segment with the explicit `C` step only becomes literally valid from `m >= 10` onward.
- Current Lean recommendation for `x = 6`: split off the `m = 8` border case explicitly and keep the symbolic `G^{m-8}` / `E` proof only under the sharper regime `m >= 10`.

## D14) D5 grouped `u`-carry mechanism scope

**Decision:** For `D5-U-CARRY-MECHANISM-020`, do not search generically for “any grouped `u`-carry” over the current one-dimensional base. Start with the smallest mechanism that preserves the current `s = w+u` carry system by design: a layer-2 carry-digit swap that replaces direction `2` by direction `4` on selected `q = m-2` carry states, and track the first extra base-coordinate candidate as `d = u-w` rather than `u` alone.

Options:
1. Search broadly for any local perturbation that creates grouped `u`-carry over the existing grouped base `s -> s+1`.
2. Restrict first to carry-preserving layer-2 swaps:
   keep the current mixed witness skeleton, but on selected carry states replace the layer-2 carry digit `2` by `4`, so `s = w+u` keeps the same increment while `u` changes relative to `w`.
3. Skip the carry-swap reduction and jump directly to a broader search for a genuinely higher-dimensional grouped base.

Recommendation:
- Option 2.
- The current obstruction analysis says the mixed witness already has the correct skew-odometer on `(s,v)`, and that the missing mechanism is grouped `u`-invariance caused by having exactly one direction-4 event per first return.
- A generic grouped `u`-carry cocycle over the existing one-dimensional base is likely too weak or gauge-trivial.
- The first honest candidate for a new active base coordinate is therefore not `u` by itself, but a coordinate that changes when `2` and `4` are swapped while preserving `s`; the natural reduced candidate is `d = u-w`.
- A carry-digit swap on the `q=-1` carry slice does exactly that:
  it preserves `Δs = 1 + 1_{q=m-2}` by construction, while changing how carry is distributed between `w` and `u`.

Risks / mitigations:
- If the selector for the `2 -> 4` swap depends only on `s`, the resulting grouped `u`-carry may still be reducible over the same one-dimensional base -> explicitly test whether the induced second coordinate collapses to an `s`-only cocycle or yields a genuine new deterministic quotient.
- Existing searched layer-2 mode families such as `2/4` and `4/2` are too coarse: they change the non-carry layer-2 behavior as well, not just the carry digit -> define the new family so the swap is allowed only on the `q=-1` carry slice.
- Extra direction-4 events can easily destroy clean frame or strictness -> keep the mixed skeleton fixed and evaluate candidates first in reduced first-return language before any broader validation.

Open questions:
- Which smallest local selector can split the `q=-1` carry slice nontrivially while preserving the current `(q,s)` carry law?
- Is the true first extra base coordinate `d = u-w`, `u` modulo a gauge, or some nearby equivalent coordinate?
- Can a carry-digit swap be realized inside the existing predecessor/exact-bit language, or does it require a genuinely new family definition such as a `0/2` versus `0/4` switch on carry states?

Rollout / acceptance:
- Keep the `mixed_008` first-return skeleton fixed and target only perturbations that preserve the current `s` increment.
- Extract first-return direction-count vectors and reduced transitions on candidate coordinates `(q,s,d,v)` with `d = u-w`, or an equivalent coordinate if better.
- Compare controls in the same language to identify where extra direction-4 events first appear and whether they preserve or destroy the `(q,s)` carry system.
- Only if a selector is found that preserves the `(q,s)` carry system and creates a genuine extra deterministic quotient beyond `s`, run a tiny targeted search in that family.

## D15) D5 single carry-swap versus paired carry mechanism scope

**Decision:** For `D5-CARRY-SWAP-U-CARRY-020`, treat a single binary carry-slice `2->4` swap as a diagnostic family only. Do not treat it as the main next search family unless it is paired or otherwise enriched so that the induced grouped second-coordinate update is genuinely permutative.

Options:
1. Use a single binary carry-slice swap as the main next search family.
2. Use the single binary carry-slice swap only as a reduced-language diagnostic, and treat the first viable search family as a paired or multi-valued carry mechanism.
3. Abandon carry-swap analysis and return to a broader generic local-family search.

Recommendation:
- Option 2.
- The exact reduced analysis says a single binary carry-swap induces grouped base maps of the form `(s,u) -> (s+1, u + Psi(s,u))` with `Psi` binary.
- For such maps to stay bijective, each fixed-`s` profile `u -> u + Psi(s,u)` must be a permutation, and exhaustive checks on odd moduli `5,7,9,11,13,15,17,19` show that for binary `Psi` this happens only when `Psi` is constant in `u`.
- So a single binary carry-swap splits into two cases only:
  - `Psi = Psi(s)` only, which is valid but still one-dimensional over the same base;
  - or `Psi` depends on a true second coordinate, in which case the grouped base map becomes non-permutative.
- Therefore the first honest family capable of producing a genuine extra base coordinate must be richer than a single binary swap, for example a paired `2->4` and `4->2` mechanism or any equivalent `{-1,0,1}`-valued second-coordinate update.

Risks / mitigations:
- The reduced obstruction might fail to transfer to a local realization -> keep the single-swap family as a diagnostic control and save its exact grouped-base behavior explicitly.
- A paired mechanism might be too broad too early -> start with the smallest paired family that preserves the current `(q,s,v)` law and changes only carry distribution.
- The real new coordinate might not be `u` itself -> continue tracking `d = u-w` in the reduced model rather than hard-coding `u` as the target coordinate.

Open questions:
- What is the smallest paired local mechanism that realizes both `+1` and `-1` relative `u`-shifts while preserving the current `(q,s,v)` dynamics?
- Can such a paired mechanism be expressed using existing named bits, or does it require a genuinely new layer-2 family?
- Does the first viable paired family still collapse to a 1D base with a vector cocycle, or does it finally produce a genuine second deterministic base coordinate?

Rollout / acceptance:
- Keep the single binary carry-swap family as a diagnostic control and save its reduced grouped maps.
- Define the smallest paired carry mechanism whose induced grouped second-coordinate update can take values in `{-1,0,1}`.
- Analyze that family first in reduced coordinates `(q,s,d,v)` before any broader torus search.
- Only if the reduced paired family yields a genuine new deterministic quotient beyond `s`, run a tiny exact realization search.

## D16) D5 affine one-surface paired selector scope

**Decision:** Treat single affine selector surfaces in the paired carry mechanism as an exhausted diagnostic family. Do not keep widening that class as the main next search branch.

Options:
1. Keep broadening the paired carry search within one-surface affine selectors
   `1_{a q + b s + c u = t}`.
2. Use the affine one-surface family only as a structural boundary test, then move to richer non-affine or multi-surface controllers.
3. Drop the reduced selector analysis and return to broader local-family search immediately.

Recommendation:
- Option 2.
- The searched affine family is already much richer than the old named atom catalog: it uses `93` selectors and `8649` ordered pairs at pilot modulus `m = 11`.
- Yet it still produces `0` genuine second-coordinate grouped base candidates.
- More sharply, every valid affine pair at the pilot modulus avoids `u` entirely. So within this one-surface affine family, any attempt to use a true `u`-dependent selector destroys grouped-base bijectivity.
- That means continuing to widen the same one-surface affine class is unlikely to uncover the missing mechanism.

Risks / mitigations:
- A larger affine coefficient range could hide an exception -> keep the current result framed honestly as a boundary test for the first simple affine family, not a universal no-go theorem.
- A viable local mechanism might still induce a non-affine grouped effect even if its raw predicates look affine -> move the next branch toward exact predecessor/tail bits or genuinely multi-surface rules rather than abandoning the carry-mechanism approach entirely.
- The pilot modulus could be misleading -> cross-check only the best surviving affine pairs on `m = 5,7,9,11,13,15,17,19`; they remain `s`-only and do not change the conclusion.

Open questions:
- Which smallest non-affine or multi-surface selector is capable of creating a genuine second grouped base coordinate?
- Can an exact predecessor / tail observable realize that selector while preserving the current `(q,s,v)` law?
- Is the right next family still local on one return, or does it need a short-memory bit by design?

Rollout / acceptance:
- Save the affine one-surface search artifact explicitly.
- Record the sharpest obstruction: `0` genuine 2D candidates and `0` valid pilot pairs using a true `u` coefficient.
- Stop widening that family and move the next reduced search to richer controller classes.

## D17) D5 next reduced perturbation target after the affine obstruction

**Decision:** Use the grouped moving adjacent transposition family as the next reduced target model: a paired perturbation that swaps `u = g(s)` with `u = g(s)+1`, especially along diagonal or anti-diagonal graphs `g(s) = ±s + b`, and then study the smallest defect that breaks the residual invariant diagonal.

Options:
1. Continue searching for a single grouped-base orbit directly inside generic multi-surface families.
2. Adopt the first genuinely two-dimensional reduced family already visible in grouped coordinates, even if it still has a small invariant orbit.
3. Ignore grouped reduced models and return directly to local rule search without a concrete target shape.

Recommendation:
- Option 2.
- The grouped transposition search shows that diagonal and anti-diagonal moving adjacent transpositions are the first clean reduced perturbations that genuinely break the old `s`-only collapse.
- For every checked odd modulus `m = 5,7,9,11,13,15,17,19`, they yield grouped base orbit sizes
  `[m, m(m-1)]`
  and full grouped orbit sizes
  `[m^2, m^2(m-1)]`.
- So they are already “almost transitive” on the full grouped state and isolate one explicit residual obstruction: an invariant diagonal orbit.
- No searched one-graph or two-graph affine transposition family yields a single grouped-base orbit of size `m^2`, so the next honest target is a controlled defect of this diagonal transposition model rather than another undirected widening.

Risks / mitigations:
- The grouped transposition family is only a reduced target, not yet a realized local rule -> use it as a target signature for local search, not as a theorem about realizability.
- The residual invariant diagonal may require a defect in the `v` law as well as the base map -> start by trying to break the diagonal in the base model, but keep open the possibility that the final perturbation must couple both base and twist.
- The best local selector may not look like a diagonal graph in raw coordinates -> allow predecessor/tail bits or paired selectors if their grouped effect matches the diagonal-transposition target.

Open questions:
- What is the smallest local paired carry mechanism whose grouped effect emulates the diagonal moving transposition?
- What is the smallest defect that breaks the invariant diagonal orbit without destroying the large `m^2(m-1)` complement orbit?
- Is the final defect best modeled in the grouped base, in the twist cocycle, or simultaneously in both?

Rollout / acceptance:
- Save the grouped transposition family search as a reduced-model artifact.
- Treat the diagonal moving adjacent transposition as the next explicit target signature for local search.
- Search next for a one-defect or predecessor-driven perturbation of that target, rather than for another generic cocycle bit.

## D18) D5 one-defect adjacent-transposition target

**Decision:** After the `s41` adjacent-transposition observation, use the one-defect diagonal/anti-diagonal transposition family as the next explicit reduced target: apply the moving adjacent transposition on every `s`-row except one chosen defect row, where the row map is left as fixed points.

Options:
1. Keep searching generic one-defect grouped perturbations without a fixed target shape.
2. Lock the next reduced target to the omission defect of the diagonal moving adjacent transposition.
3. Skip the grouped one-defect target and return directly to local selector search.

Recommendation:
- Option 2.
- `s41` sharpens the reduced language: permutation-valid ternary slice updates are built from fixed points and adjacent transpositions.
- `023` identified the first genuine 2D reduced family: the diagonal moving adjacent transposition, but it still left one invariant diagonal orbit.
- `024` now shows the smallest clean defect is enough: if the transposition is omitted on a single chosen `s`-row, the grouped base becomes a single orbit of size `m^2` for all checked odd moduli `5,7,9,11,13,15,17,19`.
- Among `1190` valid one-row defect candidates, all `70` stable single-base-orbit families come from this omission mechanism; no shifted or doubled adjacent-transposition defect in the searched range matches it.

Risks / mitigations:
- This is still a reduced target, not a realized local rule -> treat it as the target grouped signature for the next local search, not as a theorem of realizability.
- The full grouped map still splits into `m` orbits of size `m^2` because the twist remains `phi(s)` only -> keep the base-target and twist-target explicitly separated.
- The best local realization may place the defect row at a more natural residue than the searched small constants -> use the current family as the pattern class, not as a hard-coded exact residue choice.

Open questions:
- Which smallest local paired carry mechanism realizes the omission defect while preserving the current reduced `(q,s)` carry law?
- Does the eventual full D5 perturbation need only this base defect plus a new `u`-dependent twist, or does it require a coupled base-and-twist realization from the start?
- Can a predecessor / tail bit realize the omitted-row behavior naturally?

Rollout / acceptance:
- Save the one-defect grouped transposition search as an artifact.
- Use its representative candidate as the next reduced target for local search.
- Search next for a local mechanism matching:
  diagonal or anti-diagonal moving adjacent transposition on all `s`-rows, with one omitted row.
- Keep the twist problem separate and explicit in the follow-up search.

## D19) D5 reduced normal form after the omit-base split

**Decision:** Treat the reduced `D5` target as a coupled base-and-twist defect model: use the `024` omit-base candidate as the grouped base, and add a pointwise or two-point cocycle defect on the omitted edge endpoints as the smallest twist correction.

Options:
1. Keep searching only for grouped-base defects and postpone the twist issue.
2. Use the omit-base candidate from `024` together with the smallest local cocycle defect tied to the omitted edge.
3. Jump directly to a broad local realization search without fixing the reduced twist target.

Recommendation:
- Option 2.
- `024` solved the grouped-base obstruction at the reduced level: the omit-base family gives a single grouped-base orbit of size `m^2`.
- `025` now shows the twist obstruction is also sharply solvable in reduced form:
  on top of the omit-base candidate, a single-point cocycle defect at either omitted edge endpoint already yields a single full grouped orbit of size `m^3` across the checked odd moduli `5,7,9,11,13,15,17,19`.
- The two-point omitted-edge defect also works.
- By contrast, row-sized and graph-sized cocycle defects still collapse because their total contribution over the unique base orbit is `0 mod m`.
- So the first full reduced normal form is no longer hypothetical: it is
  omit-base plus a pointwise edge-tied cocycle defect.

Risks / mitigations:
- This remains a reduced target, not a local realization theorem -> keep the next search explicitly targeted at emulating this reduced signature.
- A local mechanism may realize a gauge-equivalent twist defect rather than the exact point defect -> allow equivalent small defect sets tied to the omitted edge, but keep the acceptance criterion on the grouped orbit result.
- The representative checks used the diagonal and anti-diagonal bases with defect row `0` -> treat that as a pattern class; the exact residue can shift under local conjugacy.

Open questions:
- Which smallest local paired carry mechanism can realize the omit-base defect and the pointwise edge cocycle defect simultaneously?
- Is the best local realization predecessor-driven, or does it require a new short-memory bit?
- Can the reduced point defect be recognized directly in the raw first-return traces of an eventual local witness?

Rollout / acceptance:
- Save the reduced cocycle-defect artifact.
- Treat the reduced full-orbit target as:
  one omitted-row diagonal/anti-diagonal adjacent-transposition base plus a pointwise edge cocycle defect.
- Only now start a tiny local search aimed at this exact reduced signature, rather than at generic grouped `u`-carry or generic twist noise.

## D20) D5 local realization scope after the fixed-`w` current-state obstruction

**Decision:** After `026`, stop widening current-state selector families around the diagonal fixed-`w` `B/P/M` palette. Treat the obstruction as structural and move the next local branch to genuinely history-sensitive or otherwise different mechanisms.

Options:
1. Keep widening current-state selector families around the same fixed-`w` `B/P/M` palette.
2. Treat the fixed-`w` current-state family as exhausted and move to a history-sensitive or genuinely different local mechanism.
3. Abandon the `025` reduced target and return to broader untargeted search.

Recommendation:
- Option 2.
- `025` identified the right reduced target.
- `026` tested the tiny diagonal current-state local emulation family suggested by `s43` directly and found:
  - baseline `mixed_008` still validates cleanly,
  - but none of the searched candidates is Latin on all colors for `m = 5,7,9`.
- `027` then checked the analogous anti-diagonal stationary branch and again found:
  - baseline control still validates cleanly,
  - but none of the searched candidates is Latin on all colors for `m = 5,7,9`.
- The reason is sharper than “no good parameter choice was found.” In both stationary rewrites, the intended `P` target and the adjacent `M` target collide at the exact same layer-2 current state. So a deterministic current-state layer-2 rule cannot separate them.
- Since that collision is an exact state collision, further widening of current-state or static local-observable selectors around the same palette is unlikely to solve the problem.

Risks / mitigations:
- The obstruction was tested only on the diagonal fixed-`w` branch -> keep the anti-diagonal branch available as a secondary check if needed, but do not treat it as the main immediate branch.
- A realizable local mechanism could still exist via a gauge-equivalent reduced target -> keep the acceptance criterion on the grouped orbit signature, not on the literal fixed-`w` wording.
- “History-sensitive” is broader than the current search scripts -> prototype the smallest such mechanism first rather than reopening a large family.

Open questions:
- What is the smallest genuine memory mechanism that can separate the colliding layer-2 states?
- Is a one-step history bit enough, or is a different local palette needed altogether?
- Can the omitted-edge cocycle defect be realized in the same memory mechanism, or only after the base part is solved?

Rollout / acceptance:
- Save the `026` and `027` negative artifacts with the exact layer-2 collision examples.
- Treat the current-state `B/P/M` branch as pruned on both stationary rewrites.
- Design the next local search around the smallest mechanism that genuinely escapes the exact layer-2 collision, while keeping the `025` grouped orbit signature as the target.

## D21) D5 edge-transducer scope after the smallest static two-layer test

**Decision:** After `028/029`, keep endpoint orientation as the right extracted signature, but stop widening the smallest static two-layer endpoint-controller family. Move the next local branch to a genuine extra local state carrier beyond static two-layer endpoint control.

Options:
1. Keep widening static two-layer endpoint-controlled families around the same `off/L/R` transducer idea.
2. Treat the smallest static two-layer endpoint-controller family as exhausted and move to a three-layer, two-step, or otherwise genuinely richer state-carrier mechanism.
3. Abandon the `025` reduced target and return to broader untargeted search.

Recommendation:
- Option 2.
- `028` identified the right missing local signature: endpoint orientation on the active adjacent edge.
- `029` then tested the smallest actual static realization of that idea on the representative diagonal branch:
  - `2500` exact candidates on each of `m=5,7,9`,
  - `240` layer-2 conflicts per modulus,
  - only `4` Latin / clean / strict survivors per modulus,
  - `0` candidates with a single grouped orbit of size `m^2`.
- More sharply, every Latin survivor is degenerate:
  - all `4` are the baseline word `(4,4;2,2)` with the four cocycle-defect choices,
  - there are `0` nonbaseline Latin survivors,
  - there are `0` endpoint-asymmetric Latin survivors.
- So the extracted edge signature is real, but it is not enough by itself as the smallest static two-layer local realization.

Risks / mitigations:
- `029` searched the representative diagonal branch `(w0,s0)=(0,0)` rather than every translated copy -> rely on the branch symmetry for the search stage, and only widen translation copies if a later richer family produces a live candidate.
- “Genuine extra local state carrier” is broader than the current exact scripts -> keep the next branch small by insisting it changes the intermediate current-state class or carries an extra state across one more layer, rather than reopening a broad selector grammar.
- A successful realization may still look different from the current endpoint language -> keep the acceptance criterion on the grouped orbit signature and the reduced target, not on the literal endpoint-controller wording.

Open questions:
- What is the smallest richer local mechanism that produces a nonbaseline endpoint-asymmetric Latin survivor?
- Is a three-layer local word enough, or is an explicit two-step memory carrier required?
- Can the omitted-edge cocycle defect be folded into the same richer mechanism, or should it stay as a second-stage toggle?

Rollout / acceptance:
- Save `028` as the edge-signature extraction artifact.
- Save `029` as the smallest static two-layer endpoint-controller negative artifact.
- Treat the next live local branch as:
  a genuine extra local state carrier beyond static two-layer endpoint control, with the `025` grouped orbit signature still as the target.

## D22) D5 short endpoint-word scope after the three-layer promotion test

**Decision:** Use `030` only as a path-level guide and stop widening fixed short endpoint-word families after `031`. The next branch must add a genuine memory or Latin-repair mechanism beyond fixed static endpoint words.

Options:
1. Keep widening fixed short endpoint-word families because `030` found viable path-level candidates.
2. Treat `030` as a guide only, and after `031` move to a richer mechanism that carries extra state or repairs Latin more globally.
3. Ignore the short endpoint-word catalog entirely and return to broad untargeted search.

Recommendation:
- Option 2.
- `030` is genuinely useful:
  - it found `6` desired left words, `6` desired right words, and `18` opposite-sign candidate pairs on `m=5,7,9`,
  - `14` of those pairs already separate at both layer 2 and layer 3 across the checked moduli.
- But `031` then promoted exactly that data into the smallest static three-layer field family and found:
  - `72` exact candidates per modulus,
  - `12` layer-2 conflicts,
  - `16` layer-3 conflicts,
  - `0` Latin survivors on each of `m=5,7,9`.
- So the short endpoint-word catalog is informative about what a richer mechanism might need to emulate, but it is not itself a live realizable family.

Risks / mitigations:
- `031` used only the fixed short words extracted in `030` -> if a later branch needs longer words, treat `030/031` as pruning only the length-3 fixed-word family, not all richer local mechanisms.
- “Latin-repair mechanism” is broader than the current scripts -> keep the next family small by insisting it explicitly addresses the Latin failure of `031`, rather than only reproducing path-level endpoint behavior.
- A longer or memory-carrying family could still realize a conjugate of the same reduced target -> keep the target on the grouped orbit signature, not on the literal word list.

Open questions:
- What is the smallest mechanism that turns a path-level viable endpoint word pair into an actual Latin field?
- Is the missing ingredient a true memory bit, or a coupled repair on neighboring off-edge states?
- Does the next positive family need longer words, or just a minimal Latin repair around the `030` pairs?

Rollout / acceptance:
- Save `030` as the short endpoint-word catalog.
- Save `031` as the static three-layer endpoint-word negative artifact.
- Treat the next live branch as:
  a richer mechanism that uses `030` as guidance but explicitly solves the Latin failure exposed by `031`.

## D23) D5 endpoint Latin-repair scope after the one-bit negative

**Decision:** After `032`, stop looking for a one-class or one-bit repair of the endpoint-word seeds. The next live branch must be at least a genuine multi-class transducer or another coupled Latin-repair mechanism.

Options:
1. Keep searching one-class repair gates or one-bit refinements around the `030` seed pairs.
2. Treat one-gate / one-bit repair as exhausted and move to a genuine multi-class repair mechanism.
3. Abandon the endpoint-seed branch entirely and return to untargeted search.

Recommendation:
- Option 2.
- `032` implemented the exact `s45` branch:
  - extract collision certificates for the `030` seed pairs,
  - rank them by collision support,
  - search one-gate and one-bit repairs on the best seeds.
- The result is sharp:
  - only `11` seed pairs are distinct at both layer 2 and layer 3 simultaneously,
  - best-ranked seed: left `[2,2,1]`, right `[1,4,4]`,
  - one-gate search on the top `3` seeds: `208` candidates, `0` Latin survivors,
  - one-bit search on the top `3` seeds: `4160` candidates, `0` Latin survivors.
- The obstruction is stronger than “the wrong bit was tried.”
  For the best seeds, the colliding incoming sources are already separated by:
  - current label plus every tested bit,
  - exact predecessor/current label pair,
  - exact current/successor label pair.
- `032` also probed the best seed with the smallest two-class static repair:
  - `384` candidates,
  - again `0` Latin survivors.
- So the failure is no longer a missing separator bit. The colliders are already classifiable; the remaining problem is that no one-class or one-bit local repair fixes the balanced hole/collision pattern.

Risks / mitigations:
- `032` searched only one-gate, one-bit, and a best-seed two-class static probe -> treat this as pruning the smallest repair scope, not every richer transducer mechanism.
- The best seed was chosen by exact collision ranking, but a later richer family could prefer a different seed -> keep the ranking data saved and reuse it if the next branch needs to widen beyond the top seed.
- A successful mechanism may still look more global than “endpoint repair” while remaining on the same reduced target -> keep the acceptance criterion on Latin plus the `025` grouped-orbit signature, not on the exact repair vocabulary.

Open questions:
- What is the smallest multi-class transducer that can repair the balanced hole/collision pattern exposed in `032`?
- Does the next positive family need explicit short memory, or just two or three coordinated repair classes?
- Is the best next branch a dynamic transducer on the ranked best seed, or a defect-splice that modifies neighboring off-edge states as well?

Rollout / acceptance:
- Save `032` as the endpoint Latin-repair artifact.
- Treat one-gate and one-bit repair as exhausted.
- Use the saved collision rankings to seed the next genuinely multi-class repair/transducer branch.

## D24) D5 best-seed defect-splice scope after the quotient extraction

**Decision:** After `033`, stop searching `2`-state and `3`-state defect-splice transducers on the current best-seed local alphabet. The next live branch must add a new observable local signature or change the splice mechanism itself.

Options:
1. Keep searching tiny `2`-state or `3`-state transducers on the best seed from `032`.
2. Treat the small-state transducer branch as pruned under the extracted local template/context alphabet and move to a richer observable or a different splice mechanism.
3. Abandon the best-seed defect-splice branch entirely and return to broad untargeted search.

Recommendation:
- Option 2.
- `033` sharpens the `032` branch instead of merely extending it.
- The balanced defect count
  `250, 490, 810 = 10 m^2`
  is now explained exactly:
  - per color the defect is `2 m^2`,
  - per color quotient this is `2 m = (m-1)+1+1+(m-1)` templates,
  - each quotient template carries `m` free `v`-translates.
- Per color, the defect graph is already small:
  - overfull families: `O_R1, O_R2, O_R3, O_L3`,
  - hole families: `H_L1, H_R2, H_R3, H_L3`.
- Three changed source families repair directly:
  - `L3 -> H_L3`,
  - `R2 -> H_R2`,
  - `R3 -> H_R3`.
- So only one channel remains:
  `R1 -> H_L1`.
- `033` then shows that the natural shortest realization of that channel is not a tiny transducer problem.
  The shortest splice is:
  - first alter `R1` by direction `2`,
  - then follow a long run of the same local context `BBB`,
  - then exit from a later `BBB` state by direction `2` into `H_L1`.
- On `m=5,7,9`, the shortest unary corridor lengths are `49, 195, 485`, with a longer `u=3` subfamily at `69, 237, 557`.
- Therefore, under the extracted local template/context alphabet, any controller already needs at least `50, 196, 486` internal states on the pilot range just to count to the first legal exit.
- That kills the natural `2`-state and `3`-state search before synthesis.

Risks / mitigations:
- The lower bound is stated for the current extracted local template/context alphabet and the natural one-channel splice framing -> keep that assumption explicit in the artifact and do not overstate it as a no-go for every richer local mechanism.
- The result uses the best seed only -> retain the saved `032` rankings so a later enriched local alphabet can still be tested first on the same seed and widened only if needed.
- A later positive branch may change the corridor rather than counting through it -> state the next branch in terms of adding a new observable signature or changing the splice mechanism, not merely increasing state count.

Open questions:
- What is the smallest additional local observable that breaks the unary `BBB` corridor?
- Is there a coupled local splice that reroutes `R1` mass without entering the long `BBB` run?
- Once the local alphabet is enriched, does the same best seed remain optimal?

Rollout / acceptance:
- Save `033` as the defect-quotient and unary lower-bound artifact.
- Treat `2`-state and `3`-state best-seed transducer search as pruned on the current alphabet.
- Use the next branch to search for:
  - a new observable local signature, or
  - a different splice mechanism that changes the corridor itself.

## D25) D5 corridor-phase scope after the best-seed orbit extraction

**Decision:** After `034`, stop treating the unresolved best-seed channel as a generic bounded-state transducer problem. The next live branch should expose or carry the extracted corridor phase.

Options:
1. Keep framing the best-seed obstruction as “find a somewhat larger transducer state”.
2. Treat the unresolved channel as an explicit reduced orbit-phase problem and move to phase-exposing local mechanisms.
3. Abandon the best-seed corridor branch and return to untargeted local search.

Recommendation:
- Option 2.
- `034` turns the `033` obstruction into an exact reduced model instead of another heuristic.
- After the initial `R1` alternate-`2` entry, the unresolved `BBB` corridor projects to `(s, layer)` and follows the exact source-parameterized map `F_rho`, with `rho = u_source + 1`.
- For every checked source slice and every checked modulus `m = 5,7,9,11`, that projected model has:
  - one small orbit of size `m`,
  - one large orbit of size `m(m-1)`.
- The small orbit is explicit:
  `M_rho = {(rho, layer): layer != 2} union {(rho+1,2)}`,
  and the corridor runs on its complement.
- So the unresolved channel already reproduces the same qualitative orbit split that `023` exposed in the reduced grouped-base branch.
- The delay law is now phase-theoretic, not generic transducer combinatorics:
  - `Delta_short = (m-3)m^2 - 1`,
  - `Delta_long = Delta_short + m(m-1)`,
  - `Delta mod m(m-1) = m^2 - 3m - 1`,
  - the exceptional slice is exactly `u_source = 3`.
- Therefore the old short/long gap is exactly one full large-orbit lap.
- This means the missing state is best understood as orbit phase on the extracted corridor model, not as a tiny opaque controller state.

Risks / mitigations:
- `034` is still a reduced model, not yet a local realization -> keep the next branch focused on exposing or carrying the extracted phase, not on claiming the local problem is solved.
- The phase model uses the projection `(s, layer)` and a source parameter `rho` -> save the exact per-source rows and formulas so any later local mechanism can be checked against the same target.
- A later positive mechanism might alter the corridor phase map rather than merely reading it -> keep the secondary branch open for small coupled perturbations that change the phase dynamics itself.

Open questions:
- What is the smallest local observable or carrier that exposes the extracted corridor phase?
- Can the phase be read directly from a tiny predecessor/current signature, or does it need a true moving carrier?
- Is the most realistic next branch “phase exposure” or “phase map perturbation”?

Rollout / acceptance:
- Save `034` as the corridor-phase extraction artifact.
- Treat the best-seed obstruction as an orbit-phase problem from now on.
- Use the next local branch to search for:
  - a phase-exposing mechanism, or
  - a small perturbation that changes the extracted phase map.

## D26) D5 first static phase-exposure scope after corridor extraction

**Decision:** After `035`, treat raw static `B`-state phase gates keyed only by
current-coordinate projections as pruned on the best seed. The next live
branch must use a dynamic/coupled phase carrier or a richer observable.

Options:
1. Keep widening raw static coordinate-gated `B`-state repair families on the
   best seed.
2. Treat the first static phase-exposure layer as pruned and move to
   dynamic/coupled carriers or richer observables.
3. Abandon the best-seed phase branch and return to broad untargeted search.

Recommendation:
- Option 2.
- `035` is the first exact no-go that sits directly on top of the `034`
  phase model rather than beside it.
- On the best seed `[2,2,1] / [1,4,4]`, no `1`-coordinate projection of
  `(q,w,v,u,s,layer)` isolates the first `H_L1` exit on every best-seed
  corridor.
- No `2`-coordinate projection does either.
- Exactly `8` `3`-coordinate projections do isolate that first exit:
  - `(q,w,u)`,
  - `(q,w,s)`,
  - `(q,w,layer)`,
  - `(q,u,s)`,
  - `(q,s,layer)`,
  - `(w,u,layer)`,
  - `(w,s,layer)`,
  - `(u,s,layer)`.
- `035` then tests the full exact static phase-gate family built from those
  projections:
  - `8` projections,
  - `3` gate modes,
  - `4` cocycle-defect choices,
  for `96` exact candidates total.
- All `96` candidates fail incoming Latin already on the pilot range, so
  there are:
  - `0` Latin survivors,
  - `0` clean survivors,
  - `0` strict survivors,
  - `0` grouped-target survivors.
- So `034` remains right about the obstruction being phase, but the first naive
  static attempt to expose that phase is already dead.

Risks / mitigations:
- The no-go is stated for the best seed and for raw current-coordinate
  projections only -> keep those scope limits explicit and preserve the saved
  separating-projection catalog so later branches can measure genuine progress.
- The result does not rule out richer observables or dynamic carriers -> state
  the next branch positively in those terms rather than overstating `035` as a
  universal impossibility theorem.
- A later positive branch may still use one of the saved `3`-coordinate
  projections, but only as part of a coupled mechanism -> keep the exact list
  of the `8` viable separating triples in the artifact.

Open questions:
- What is the smallest dynamic/coupled carrier that can transport corridor
  phase without immediately breaking Latin?
- Is there a richer observable than raw current-coordinate projection that can
  see the phase while still remaining local?
- Can the corridor phase be exposed by a coupled perturbation that changes the
  phase map itself instead of reading it directly?

Rollout / acceptance:
- Save `035` as the static phase-gate no-go artifact.
- Treat raw static coordinate-gated `B`-state repairs as pruned on the best
  seed.
- Use the next branch to search for:
  - a dynamic/coupled phase carrier, or
  - a richer local observable than raw current-coordinate projection.

## D27) D5 corridor-phase interpretation scope after the external-reader mismatch

**Decision:** After `036`, do not treat the saved `034` `(s,layer)` rule as the
final long-run deterministic corridor model. Treat it as a first-pass projected
phase lap, and use the lifted traced model `(q,a,layer)` with
`a = s - rho mod m` for the next branch analysis.

Options:
1. Keep treating `034` as if `(s,layer)` were already the true long-run
   corridor state.
2. Read `034` as a first-pass projection only, and use the lifted traced model
   `(q,a,layer)` extracted by `036`.
3. Discard the corridor-phase branch and reopen broad local search.

Recommendation:
- Option 2.
- The external-reader objection was mathematically correct.
- `036` verifies that the saved `034` rule on `(s,layer)` matches only until
  the first repeated projected phase.
- Immediately after one projected lap, the same `(s,layer)` already has a
  different projected successor, so `(s,layer)` is not a deterministic factor
  of the full long corridor.
- That resolves the old mismatch:
  - `first_exit_phase` is the actual projected phase of the first exit-capable
    corridor state,
  - `phase_residue_mod_period` is only the delay residue against the first-pass
    projected `(s,layer)` cycle.
- `036` also identifies a clean lifted traced model.
  After normalizing by
  `rho = u_source + 1` and `a = s - rho mod m`, the corridor follows an exact
  deterministic rule on `(q,a,layer)` up to first exit on every checked source
  family and every checked `m = 5,7,9,11`:
  - `(q,a,0) -> (q+1, a, 1)`
  - `(q,a,1) -> (q, a+1, 2)`
  - `(q,a,2) -> (q, a+1, 3)` if `q = m-1`, else `(q,a,3)`
  - otherwise `(q,a,layer) -> (q,a,layer+1 mod m)`
- The lifted entry and first exits are now uniform:
  - entry lift `(m-1, 0, 2)`
  - regular first exit `(m-1, m-4, 1)` via `[2]`
  - exceptional first exit `(m-2, m-4, 1)` via `[1]`

Risks / mitigations:
- `036` is a traced-lift statement up to first exit, not yet a full theorem for
  the entire infinite branch -> keep that scope explicit in the artifact and do
  not overstate it as the final D5 normal form.
- The lifted state uses `q`, which is not yet a proved minimal local observable
  -> state the next branch as “design against the lifted model,” not “q alone is
  locally readable.”
- The external researcher also asked for runnable code -> include a runnable
  `scripts/` tree and raw corridor traces in the next distribution bundle.

Open questions:
- Can the lifted traced model on `(q,a,layer)` be promoted to a full theorem
  for the entire corridor branch?
- What is the smallest local mechanism that can read or carry the relevant
  lifted state, especially the `q`-controlled layer-2 event?
- Is there a no-go theorem for any mechanism that only sees `(s,layer)`-type
  phase data?

Rollout / acceptance:
- Save `036` as the corridor-phase clarification artifact.
- Stop reading `034` as the final long-run corridor normal form.
- Use the next branch to design against the lifted `(q,a,layer)` model.
- Ship a refreshed external-reader bundle with:
  - updated docs,
  - `035` and `036`,
  - raw representative corridor traces,
  - and a runnable `scripts/` tree.

## D28) D5 next-branch scope after the lifted raw-odometer extraction

**Decision:** After `037`, stop treating the next local branch as a phase
exposure problem. The lifted corridor phase is already visible on raw
`(q,w,layer)`; the next live branch is a localized carrier search.

Options:
1. Keep searching for new phase coordinates or new phase-exposure gadgets.
2. Treat the raw odometer as already exposed and move to a corridor-local
   carrier / trigger mechanism.
3. Reopen broad local search without using the extracted corridor target.

Recommendation:
- Option 2.
- `037` verifies exactly, on every traced best-seed corridor state up to first
  exit and for every checked `m = 5,7,9,11`, that the lifted `036` coordinate
  is already visible on raw current coordinates:
  `a = q + w - 1_{layer=1} mod m`.
- The raw triple `(q,w,layer)` follows an exact odometer rule on the corridor:
  - `(q,w,0) -> (q+1,w,1)`
  - `(q,w,1) -> (q,w,2)`
  - `(q,w,2) -> (q,w+1,3)` if `q = m-1`, else `(q,w,3)`
  - otherwise `(q,w,layer) -> (q,w,layer+1 mod m)`.
- The raw coordinate `chi` extracted in `037` increments by exactly `1` on
  every traced corridor step, with entry state `(m-1,1,2)` at `chi = 0`.
- The first exits become two universal raw targets:
  - regular family: `(m-1,m-2,1)` via `[2]`
  - exceptional family: `(m-2,m-1,1)` via `[1]`
  and their phase gap is exactly `m(m-1)`.
- So phase itself is no longer the hidden ingredient. What is still missing is
  corridor localization: a marker that is born on the intended `R1` alt-`2`
  entry, transported through `BBB`, and fires only at the family-specific
  target phase.

Risks / mitigations:
- `037` is still a reduced-model extraction, not a local realization -> keep
  the next branch framed as a carrier search, not as “the local problem is
  solved.”
- Raw phase visibility does not mean the target is globally safe to gate -> the
  whole point of the next branch is to add corridor localization explicitly.
- The exceptional family still needs one extra class bit -> keep the next
  reduced target as “one active marker plus one family bit,” not only a single
  undifferentiated carrier.

Open questions:
- What is the smallest local mechanism that can create and preserve the
  corridor-local marker?
- Can the exceptional family bit be generated locally at entry, or must it be
  transported from an earlier signature?
- Is there a no-go theorem for any mechanism that uses visible raw phase
  without corridor localization?

Rollout / acceptance:
- Save `037` as the lifted raw-odometer / carrier-target artifact.
- Stop framing the next live branch as phase exposure.
- Use the next branch to search for:
  - a corridor-local marker,
  - plus the smallest family bit needed to choose the regular vs exceptional
    target.

## D29) D5 next-branch split after the birth-local source-signature search

**Decision:** After `038`, stop treating the source marker and exceptional
family bit as one coupled missing ingredient. Treat the family bit as already
locally solved at the source in the smallest birth-local neighborhood family,
and focus the next live branch on creating the source-local marker itself.

Options:
1. Keep searching for marker and family bit together as one joint local
   synthesis problem.
2. Split them: treat the family bit as already cheap at birth, and focus the
   next branch on source-local marker creation.
3. Move the search to entry-local exceptional detection instead of source-local
   birth.

Recommendation:
- Option 2.
- `038` searches the simple one-step birth-local neighborhood alphabet built
  from current and predecessor/successor `phase_align, wu2` bits, across
  `m = 5,7,9,11`.
- In that family:
  - source marker isolation counts are `0` at sizes `1,2,3,4,5`
  - entry marker isolation counts are `0` at sizes `1,2,3,4,5`
  - entry exceptional isolation counts are `0` at sizes `1,2,3,4,5`
  - but the exceptional source slice is already isolated at size `1` by
    either `pred2_wu2` or `pred4_wu2`
- So the family bit is no longer the sharp local obstruction. The marker is.

Risks / mitigations:
- `038` only covers the smallest simple birth-local neighborhood alphabet ->
  keep the result framed as a sharp small-family no-go / split, not a universal
  impossibility theorem.
- The source marker may still exist in a richer observable or dynamic carrier
  family -> move the next branch there directly instead of reopening entry-bit
  search.
- The one-bit exceptional test is inside the source class, not a global marker
  by itself -> continue to treat it as a secondary bit that becomes useful once
  the source class is localized.

Open questions:
- What is the smallest richer observable that isolates the source class?
- Is the right next family a dynamic carrier, a coupled source/entry mechanism,
  or a provable no-go for a broader birth-local alphabet?
- Can the size-`<=5` simple-neighborhood no-go be upgraded to a theorem?

Rollout / acceptance:
- Save `038` as the birth-local source-signature artifact.
- Stop treating the family bit as the hard part of the next branch.
- Use the next branch to search for:
  - a source-local marker / carrier,
  - with the exceptional bit supplied cheaply at birth once the source class is
    captured.

## D30) D5 next-branch scope after exact raw birth extraction

**Decision:** After `039`, treat birth as already explicit at the reduced
raw-coordinate level, and move the next live branch to tagged carrier
transport. Keep the admissibility of exact raw birth observables as an explicit
open caveat rather than silently folding it into the transport problem.

Options:
1. Keep treating birth discovery as the main reduced obstruction.
2. Treat exact raw birth as solved at the reduced level and move to tagged
   transport, while keeping admissibility explicit.
3. Skip the reduced birth result and reopen richer source-edge / temporal birth
   mechanisms immediately.

Recommendation:
- Option 2.
- `039` verifies exactly on `m = 5,7,9,11` that:
  - source `R1` is exactly `layer=1, q=m-1, w=0, u!=0`
  - exceptional source is exactly `u=3` inside that class
  - entry `alt-2(R1)` is exactly `layer=2, q=m-1, w=1, u!=0`
  - exceptional entry is exactly `u=3` inside that class
- So the reduced birth predicates are no longer vague.
- `039` also verifies on representative regular and exceptional corridor traces
  that current raw `u` visits all residues, so the family bit cannot be
  statically re-read later from current `u`; it must be initialized at birth
  and transported.
- Therefore the live reduced obstruction is tagged transport, not birth
  discovery.

Risks / mitigations:
- “Exact raw current coordinates” may be too strong for the intended local
  mechanism class -> keep admissibility explicit as an open question instead of
  overstating `039` as a solved local realization.
- Transport is still only reduced-model packaging here -> the next branch must
  still search for or rule out actual tagged carrier mechanisms.
- The exact birth formulas do not by themselves localize a realizable rule ->
  if admissibility fails, reopen richer source-edge / temporal birth only then.

Open questions:
- Are exact raw birth observables admissible for the intended local mechanism
  class?
- What is the smallest tagged carrier that transports `active_reg / active_exc`
  through the visible raw odometer corridor?
- Can the transport problem be separated cleanly from the admissibility
  question in theorem form?

Rollout / acceptance:
- Save `039` as the raw birth / tagged transport artifact.
- Stop treating birth discovery as the main reduced obstruction.
- Use the next branch to search for:
  - tagged carrier transport on top of the exact raw birth formulas,
  - or an explicit admissibility / no-go statement if those observables are not
    allowed.

## D31) D5 next-branch scope after the rich-observable realization boundary

**Decision:** After `040`, stop treating reduced controller logic as the live
problem. The fixed raw carrier logic is already exact on coordinate-level
current observables on the checked active union. The next live branch is
exposure / admissibility of those observables, not another lift of the same
simple `038` row.

Options:
1. Keep widening source-edge or short temporal lifts of the same simple `038`
   row.
2. Treat controller logic as settled at the reduced raw-coordinate level and
   move to coordinate exposure / admissibility.
3. Reopen generic carrier / transducer search without preserving the fixed raw
   control model.

Recommendation:
- Option 2.
- `040` verifies that the first richer families still generated from the same
  simple row fail:
  - full-row source-edge pairs do not isolate the source class
  - full-row lag-1 / lag-2 temporal pairs do not stabilize the exceptional
    trigger on any checked modulus
- `040` also verifies that, on checked moduli `m = 5,7,9,11`:
  - birth is exact on raw current coordinates
  - current `(q,w,u,layer)` already separates the active source families on the
    traced active union
  - active-conditioned current `(q,w,layer)` fires with zero prehits on both
    regular and exceptional branches
- So the remaining gap is not reduced controller logic. It is exposure /
  admissibility of those coordinate-level observables.

Risks / mitigations:
- The positive part of `040` is still phrased on the checked active union ->
  keep it as a realization-boundary result, not a complete local-mechanism
  theorem.
- “Coordinate-level observables” may still be inadmissible in the intended
  local class -> make admissibility explicit rather than conflating it with the
  control logic.
- The result does not license reopening arbitrary new observables -> first
  target observables that explain the already-extracted raw coordinates.

Open questions:
- What is the smallest admissible observable family that exposes the needed raw
  current quantities?
- Can the failure of all simple-row-derived source-edge / short temporal lifts
  be upgraded to a theorem?
- Is there a clean compression from the raw current control model to a more
  abstract invariant that is still locally exposable?

Rollout / acceptance:
- Save `040` as the rich-observable realization boundary artifact.
- Stop widening the same simple `038` row by source-edge or short temporal
  lifts.
- Use the next branch to search for:
  - coordinate exposure / admissibility mechanisms for the raw current
    observables already identified,
  - or an explicit no-go theorem for those observables in the intended local
    class.

## D32) D5 next-branch scope after the first grouped-state admissibility no-go

**Decision:** After `041`, stop treating grouped-state-descending admissible
observables as the main next search. The first `025`-style grouped-state
families are already exhausted, and the exact remaining admissibility
ingredient is one lifted coordinate beyond current grouped state `(s,u,v)`.

Options:
1. Keep searching grouped-state-descending observables built from the same
   `025` omit-base / edge-tied cocycle ingredients.
2. Treat `041` as the first exact admissibility no-go for that class and move
   to the smallest admissible lifted coordinate beyond current grouped state.
3. Reopen broader raw neighborhood or generic transducer search without using
   the grouped-state obstruction.

Recommendation:
- Option 2.
- `041` verifies on `m = 5,7,9,11` that:
  - `w` already descends exactly as `s-u`
  - the regular and exceptional fire predicates are not functions of current
    grouped state `(s,u,v)`, even after conditioning on family
  - canonical omit-base base gauges and edge-tied point cocycles have exactly
    the same collision counts because they still descend to the same grouped
    state
- So the next live question is not “which grouped-state observable next?” It
  is “what is the smallest admissible lifted coordinate beyond grouped state?”

Risks / mitigations:
- `041` is still phrased on the checked active union -> keep it as a sharp
  admissibility-boundary result, not as a global local-mechanism theorem.
- A future branch could realize a lift in a way not obvious from the reduced
  cocycle language -> permit lifted-coordinate mechanisms, but do not return to
  grouped-state-descending search without new evidence.
- The result could be overread as saying no admissible mechanism exists ->
  phrase the conclusion narrowly: grouped-state descent is exhausted; lifted
  coordinates remain open.

Open questions:
- What is the smallest admissible lifted coordinate beyond current grouped
  state?
- Can the grouped-state-descending no-go be upgraded from computational result
  to theorem?
- Is the right lift best thought of as a `q`-like phase coordinate, a one-step
  pre-grouped observable, or an explicitly transported marker?

Rollout / acceptance:
- Save `041` as the first grouped-state admissibility no-go artifact.
- Stop opening new grouped-state-descending observable families as the main
  branch.
- Use the next branch to target:
  - the smallest admissible lifted coordinate, or
  - a theorem/no-go for an even narrower lifted class if that branch also
    fails.

## D33) D5 next-branch scope after the carry-slice / finite-cover split

**Decision:** After `042`, split the D5 lifted branch into:
1. trigger-level carry-slice realization, and
2. structural finite-cover extraction over the grouped base.
Do not jump straight to full raw `q` as the default lifted object.

Options:
1. Treat full raw `q` as the next main lifted coordinate.
2. Treat the carry-slice bit `c = 1_{q=m-1}` as the smallest positive target,
   while separately extracting the tiny finite cover over
   `B = (s,u,v,layer,family)` as the structural object.
3. Ignore the lifted split and reopen broader controller or transducer search.

Recommendation:
- Option 2.
- `042` verifies on `m = 5,7,9,11` that:
  - `w` already descends as `s-u`
  - exceptional fire already descends to
    `B = (s,u,v,layer,family)`
  - regular fire descends to `B` plus the carry-slice bit
    `c = 1_{q=m-1}`
  - `c` is not a function of `B`
  - `(B,c)` is still not a closed deterministic dynamics
  - the extracted future-signature lift has fiber size at most `3` over `B`
- So full raw `q` is too coarse as the default target, and grouped-state
  descent is already too small. The right next language is:
  carry bit for trigger, tiny finite cover for structure.

Risks / mitigations:
- The finite-cover extraction is still computational, not yet theorem-shaped ->
  keep the statement at the level of checked active-union cover size.
- The carry bit could be locally inadmissible even if it is the right trigger
  lift -> treat admissible realization as a separate task from structural
  extraction.
- The cover may admit several equivalent coordinatizations -> phrase the target
  as “small finite-sheet lift” rather than overcommitting to one coding.

Open questions:
- Can the carry-slice bit be realized admissibly in the intended local class?
- Can the finite cover over `B` be extracted theorem-first, without searching a
  large lifted observable space?
- Is the right D5 manuscript language “skew odometer plus finite-sheet cover”?

Rollout / acceptance:
- Save `042` as the carry-slice / finite-cover artifact.
- Use the next branch to target either:
  - admissible carry-slice realization, or
  - theorem/no-go extraction for the tiny finite cover.
- Keep the D3/D4/D5 comparison framed in odometer language rather than raw
  controller language.

## D34) D5 next-branch scope after the residual two-sheet extraction

**Decision:** After `043`, keep the D5 split, but sharpen the structural side
from “tiny cover over `B`” to:
`B`, then `B+c`, then a residual binary noncarry sheet over `B+c`.
Prioritize admissible realization of the carry sheet before reopening broader
lifted-observable search.

Options:
1. Treat the `043` residual `2`-sheet as the next immediate local-observable
   target.
2. Treat the carry slice as the next main local target, while using the
   residual `2`-sheet as the theorem / narrative object.
3. Reopen broader lifted-observable search now that the finite cover is
   sharper.

Recommendation:
- Option 2.
- `043` verifies on `m = 5,7,9,11` that:
  - the minimal deterministic cover over `B+c` has fiber size at most `2`
  - the support of that residual `2`-sheet lies entirely on the regular
    noncarry branch
  - the residual sheet is not the obvious bit `1_{q=m-2}` on `m=7,9,11`
  - short future-carry windows still do not coordinatize it on larger `m`
  - a theorem-friendly but nonlocal coordinatization exists via time to next
    carry
- So the structural object is now sharp enough for theorem language, but not
  yet sharp enough to justify jumping straight into a new local-realization
  search for the residual sheet. The carry slice is still the smallest live
  local target.

Risks / mitigations:
- The residual `2`-sheet could tempt a premature broader search ->
  keep the next local branch on admissible carry-slice realization first.
- The nonlocal `time to next carry` coordinatization could be mistaken for an
  admissible observable ->
  record it as a theorem aid, not as a local-mechanism answer.
- Some moduli admit ad hoc `q`-only partitions ->
  do not over-read those as a stable structural law unless they persist across
  the checked range.

Open questions:
- Can the carry sheet be realized admissibly in the intended local class?
- Once the carry sheet is realized, is the residual `2`-sheet forced or does
  it need its own mechanism?
- Is there a small local no-go showing the residual sheet cannot be a current
  observable of the same type?

Rollout / acceptance:
- Save `043` as the residual-two-sheet artifact.
- Update the RoundY frontier docs to use the language:
  grouped base + carry sheet + residual binary noncarry sheet.
- Use the next main local branch to target admissible realization of the carry
  slice, not a broad lifted-observable search.

## D35) D5 next-branch scope after the binary anticipation normal form

**Decision:** After `044`, treat the theorem branch as structurally explicit
and keep the main local branch focused on admissible realization of the carry
sheet `c = 1_{q=m-1}`.

Options:
1. Shift the main branch to admissible realization of the full residual sheet
   now that it has a canonical binary form.
2. Keep the local branch on the carry sheet, while using the explicit binary
   anticipation normal form as the theorem object.
3. Reopen broader lifted-observable search because the residual sheet is now
   simpler.

Recommendation:
- Option 2.
- `044` verifies on `m = 5,7,9,11` that:
  - the checked active branch factors as
    `B <- B+c <- B+c+d`
  - `d` can be chosen canonically as
    `1_{next carry u >= m-3}`
  - carry states are singleton over `B+c`
  - the support of `d` is regular noncarry only
  - deterministic active evolution closes on `B+c+d`
- So the structural branch is no longer the bottleneck. The remaining local
  bottleneck is still the carry slice itself.

Risks / mitigations:
- The explicit binary `d` could look temptingly local ->
  keep emphasizing that `044` extracted a structural anticipation coordinate,
  not an admissible current observable.
- The theorem branch could drift into overdescribing the cover ->
  keep the manuscript statement short: grouped base + carry sheet + binary
  anticipation cover.
- The carry branch could still fail in the first admissible families ->
  if that happens, return a carry-specific no-go, not a generic search result.

Open questions:
- What is the smallest admissible observable family that realizes `c`?
- Does a clean no-go exist for the first carry-realization families beyond the
  old grouped-state obstruction?
- Does the full global proof ever need admissible realization of `d`, or is
  the theorem branch enough once `c` is local?

Rollout / acceptance:
- Save `044` as the carry-and-finite-cover artifact.
- Update the RoundY docs so the current message is:
  theorem branch explicit, carry realization still open.
- Keep the next autonomous local branch focused on the carry sheet.

## D37) D5 next-branch scope after the first carry-only admissibility no-go

**Decision:** After `045`, stop widening the first carry-only admissible
catalogs built from current edge / label / delta data, `1`-step and `2`-step
grouped transition signatures, and low-cardinality `025`-style anchored gauge
bits. The next honest local branch is a broader lifted gauge or a
deeper-than-`2`-step transition sheet, still targeting only the carry bit
`c = 1_{q=m-1}`.

Options:
1. Keep widening the same first carry-only catalogs with more combinations of
   current-edge, `1`-step, `2`-step, and low-cardinality anchored-gauge data.
2. Treat `045` as the first carry-specific admissibility no-go and move to the
   next lifted datum: broader lifted gauge or deeper transition sheet.
3. Skip the carry branch and reopen local realization of the residual
   anticipation sheet `d`.

Recommendation:
- Option 2.
- `045` verifies on `m = 5,7,9,11` that:
  - `69,994` exact carry-family candidates were tested in the first carry-only
    catalogs,
  - there are `0` exact positives,
  - full `B`, `B -> B_next`, and `B -> B_next -> B_next2` grouped transition
    classes all still fail,
  - the best negatives are `next_dn` and `dn + next_dn`, which are exact on
    `m=5` but miss only regular carry `B`-states on `m=7,9,11`,
  - adding the first low-cardinality anchored-gauge bits does not improve that
    boundary.
- So the right next move is no longer “try more of the same carry features.”
  It is “identify the next lifted admissibility datum beyond those first
  catalogs.”

Risks / mitigations:
- `045` is still a checked active-union result -> phrase it as a first
  carry-catalog no-go, not as a theorem that no carry observable exists.
- A broader lifted gauge or deeper transition sheet may still be too broad if
  opened carelessly -> keep the next branch carry-specific and exact, not a
  generic transducer reopening.
- The theorem branch could get neglected while local search pivots ->
  keep `044` proof work in parallel because it is already theorem-shaped.

Open questions:
- What is the smallest lifted datum beyond current edge / `1`-step / `2`-step
  / low-cardinality anchored-gauge data that realizes `c`?
- Can the `045` first-catalog no-go be upgraded from computation to theorem?
- Is the next live object better thought of as a richer anchored gauge, a
  deeper transition signature, or a small finite-state cover over the carry
  branch?

Rollout / acceptance:
- Save `045` as the first carry-only admissibility no-go artifact.
- Update the RoundY docs so the current message is:
  theorem branch explicit, first carry-only catalogs dead, next local target =
  broader lifted gauge or deeper transition sheet for `c`.
- Keep the next autonomous local branch on the carry sheet only; do not reopen
  residual-sheet realization as the main branch.

## D38) D5 next-branch scope after the deep future-transition carry-sheet extraction

**Decision:** After `046`, stop describing the next carry branch as a vague
“broader lifted gauge or deeper transition sheet.” The carry bit is already an
exact future grouped-transition event on the checked active base, so the next
honest local branch is admissible coding of that event:
current `B` plus
`initial flat-run length + first nonflat dn`.

Options:
1. Keep the next branch phrased loosely as a broader lifted gauge or deeper
   transition sheet.
2. Treat `046` as the structural target and search for an admissible surrogate
   for the exact future-transition signature.
3. Stop local search and move only to proof work on `044/045/046`.

Recommendation:
- Option 2.
- `046` verifies on `m = 5,7,9,11` that:
  - the minimal exact future `dn` horizon is `m-3`,
  - the minimal exact future grouped-state horizon is `m-2`,
  - the exact future window compresses to current `B` plus
    `initial flat-run length + first nonflat dn`,
  - flat-run length alone is not exact,
  - the `H-1` ambiguity is confined to regular carry `B`-states.
- So the next object is no longer unknown in kind. It is known exactly at the
  reduced future-transition level.

Risks / mitigations:
- `046` is still a checked active-union extraction -> keep it as a structural
  target, not yet a theorem for all odd `m`.
- “Admissible coding” could be overread as a promise that a simple observable
  exists -> keep the next local branch exact and narrow, and allow a no-go if
  the first codings fail.
- The theorem branch could drift behind -> keep `044/045/046` proof packaging
  in parallel because the structural story is now much cleaner.

Open questions:
- Can the `m-3` future `dn` horizon be proved symbolically for all odd `m`?
- What is the smallest admissible surrogate for
  `B + flat-run length + first nonflat dn`?
- Does the exact future signature admit a smaller equivalent coding, or is
  this already minimal in a theorem-friendly sense?

Rollout / acceptance:
- Save `046` as the deep future-transition carry-sheet artifact.
- Update the RoundY docs so the current message is:
  future-transition carry sheet extracted; next local target = admissible
  coding of that event.
- Keep the next autonomous local branch on carry-only admissibility, not on
  residual-sheet realization or generic controller search.

## D36) D3 odometer Lean rewrite strategy

**Decision:** Keep the finished `formal/TorusD3Even` development as the checked baseline, and prototype the odometer-oriented D3 rewrite in a parallel module tree rather than refactoring the live completed files in place.

Options:
1. Rewrite `formal/TorusD3Even` in place so the current Route-E proofs are replaced directly by the odometer narrative.
2. Create a parallel D3 odometer tree that reuses the current finished theorems as acceptance targets, then swap over only after the new structure is theorem-complete.
3. Leave the current Lean exactly as-is and use the odometer rewrite only in the tex exposition.

Recommendation:
- Option 2.
- The current `formal/TorusD3Even` tree is now complete and valuable as a checked reference point, so it should not be destabilized during an architectural rewrite.
- The main cleanup opportunity is real, but it is narrower than “reuse the D4 theorem verbatim”:
  - D4’s `psi2Equiv` / `cycleOn_T2` live on the two-dimensional `QCoord` lane map.
  - D3-even color `2` already has its own one-dimensional odometer-style conjugacy in `formal/TorusD3Even/Color2.lean` via `psiT2Equiv`, `psiT2_conj`, and `cycleOn_T2`.
  - The hard part in D3-even is not the final cycle theorem anymore; it is the derivation of the first-return data `T_c`, `rho_c`, and the no-early-return facts from the finite-defect return maps on `P_0`.
- So the right odometer rewrite target is:
  1. a shared full-map-to-section lifting layer for D3, analogous to `formal/TorusD3Odd/FullCycles.lean` and `formal/TorusD4/Lifts.lean`;
  2. a finite-defect odometer normal-form layer on `P_0`;
  3. a reusable first-return / splice layer that derives the one-dimensional lane maps from that normal form.

Risks / mitigations:
- The rewrite could duplicate a lot of completed code without actually shrinking the proof burden ->
  start with color `2` only and require theorem parity with the current `cycleOn_color2` before touching colors `1/0`.
- The D4 odometer API could be overfit to the wrong state space ->
  keep explicit notes that D3-even uses a one-dimensional first-return map on the lane transversal, not D4’s two-dimensional `T2`.
- Refactoring in place could break the already-complete development ->
  keep the current files untouched except for optional wrapper theorems until the new tree is complete.

Open questions:
- How much of the current `Color2.lean` orbit-trace layer can actually be replaced by a generic finite-defect lemma, rather than moved around?
- Whether the best experimental tree is `formal/TorusD3Odometer/` or a parallel `formal/TorusD3EvenOdometer/` subdirectory.
- Whether the eventual clean endpoint should unify odd and even D3 under one return-map API, or only repackage the even proof.

Rollout / acceptance:
- First milestone: a parallel color-`2` odometer file that proves the same endpoint as
  `formal/TorusD3Even/Color2.lean` and still builds with `lake build TorusD3Even`.
- Second milestone: add the D3 full lifting theorem from the `P_0` cycle to the full `m^3` cycle, mirroring the odd-case pattern.
- Final acceptance: the odometer tree reproduces the current D3-even theorems with less case-local duplication, and the old `formal/TorusD3Even` tree can remain as a baseline until the replacement is clearly superior.

Current checkpoint:
- The parallel tree now exists and builds with `lake build TorusD3Odometer`.
- New files:
  - `formal/TorusD3Odometer/Basic.lean`
  - `formal/TorusD3Odometer/Lift.lean`
  - `formal/TorusD3Odometer/Color2.lean`
  - `formal/TorusD3Odometer/Color2Full.lean`
  - root import file `formal/TorusD3Odometer.lean`
- `Basic.lean` contains the shared D3 full-coordinate geometry and a generic transport
  `liftPointMap` through `splitPointEquiv`.
- `Lift.lean` contains the generic slice-to-full cycle theorem
  `cycleOn_full_of_cycleOn_slice` and the `P_0` specialization
  `cycleOn_full_of_cycleOn_p0`.
- `Color2.lean` already exposes the odometer-facing wrappers for the finished even
  color-`2` section theory, plus the specialization
  `cycleOn_full_of_color2_return`:
  if a future full D3-even color-`2` map is shown to advance the slice coordinate by `+1`
  and to return after `m` steps by `R2xy`, the full `m^3` cycle follows immediately.
- `Color2Full.lean` now defines that actual parallel full color-`2` map,
  proves the `m`-step return theorem
  `iterate_m_fullMap2XY_slice_zero`,
  proves the full `m^3` cycle theorem
  `cycleOn_fullMap2XY`,
  and is imported by `formal/TorusD3Odometer.lean`.
- Wrapper-level acceptance modules for the finished splice proofs now also live in the
  odometer tree:
  - `formal/TorusD3Odometer/Color1.lean`
  - `formal/TorusD3Odometer/Color0.lean`
- These expose the checked lane-cycle theorems for all verified color-`1/0`
  congruence families without introducing new full-map rewrites.

Next exact target:
- The color-`2` milestone is now complete.
- The next live issue is no longer a local proof bug in the color-`2` branch.
  It is the scope decision recorded in `D39`: whether colors `1/0`
  should enter the odometer tree only as wrapper-level acceptance targets over the
  finished splice proofs, or as genuine new full-map rewrites.

## D39) D3 odometer tree scope after the color-2 full-map milestone

**Decision:** After the completed parallel color-`2` full-map proof, do not immediately commit to the full explicit color-`1/0` full-map rewrites; first decide whether the parallel tree is meant to be a wrapper/staging layer or a full replacement path.

Options:
1. Stop the odometer tree at color `2` and keep colors `1/0` only in `formal/TorusD3Even`.
2. Add colors `1/0` to `formal/TorusD3Odometer` first as wrapper-level acceptance targets over the finished splice-cycle theorems in `formal/TorusD3Even/Color1.lean` and `formal/TorusD3Even/Color0.lean`, and postpone any new full-map rewrites.
3. Continue directly to genuine parallel rewrites for colors `1/0`, including explicit full maps and `m`-step return theorems in each congruence family.

Recommendation:
- Option 2.
- Color `2` is the honest odometer/full-map prototype because its section return is already a clean one-dimensional odometer-like map.
- Colors `1/0` are structurally different: the current verified objects are splice-normal-form lane maps with congruence-family splits, not a single uniform full-map normal form.
- A wrapper layer gives the parallel tree a complete lane-cycle API without forcing immediate duplication of the largest case split in the finished baseline.

Risks / mitigations:
- Option 2 could degenerate into a thin alias layer with little mathematical compression ->
  keep it explicitly as a staging path and record which theorems are wrappers versus genuine rewrites.
- Option 3 may still be the right end state ->
  revisit only after the wrapper layer is in place and after checking whether a shared color-`1/0`
  full-map schema exists that is materially smaller than the current baseline transcription.
- Stopping at Option 1 would waste the successful color-`2` prototype ->
  keep the current imported `Color2Full.lean` as the minimum accepted rewrite artifact.

Open questions:
- For the manuscript cleanup, is it enough that the odometer tree reproduces the lane-cycle theorems for colors `1/0`, or is a full-map `m^3` rewrite also required?
- Is there a shared full-map schema for colors `1/0` analogous to `Color2Full.lean`,
  or do the splice-family splits make that unrealistic?

Rollout / acceptance:
- Keep `formal/TorusD3Odometer/Color2Full.lean` imported and building.
- If Option 2 is taken, the next code milestone is wrapper modules for colors `1/0`
  that expose the finished splice-cycle theorems inside the odometer tree.
- If Option 3 is taken later, do it one congruence family at a time and compare code size / theorem shape directly against the current finished baseline.

Current checkpoint after decision:
- Option 2 is now implemented at the wrapper level.
- `formal/TorusD3Odometer/Color1.lean` exports:
  - `cycleOn_laneMap1_caseI_mod_two`
  - `cycleOn_laneMap1_caseI_mod_zero`
  - `cycleOn_laneMap1_caseII_mod_four`
- `formal/TorusD3Odometer/Color0.lean` exports:
  - `cycleOn_laneMap0_caseI_mod_zeroTwo`
  - `cycleOn_laneMap0_caseII_mod_ten`
  - `cycleOn_laneMap0_caseII_mod_four`
- `formal/TorusD3Odometer.lean` imports those wrappers, and
  `lake build TorusD3Odometer` succeeds.
- The wrapper layer is now compressed into canonical residue-dispatch APIs:
  - `formal/TorusD3Odometer/Color1.lean` defines `laneMap1` and proves
    `cycleOn_laneMap1` under `Even m` and `Fact (9 < m)`.
  - `formal/TorusD3Odometer/Color0.lean` defines `laneMap0` and proves
    `cycleOn_laneMap0` under `Even m` and `Fact (9 < m)`.
- So the odometer tree now exposes one wrapper theorem per color for the lane-cycle
  endpoint, rather than only residue-local theorem names.
- The first bounded full-map probe beyond color `2` is now implemented for color `1`,
  Case I, in `formal/TorusD3Odometer/Color1FullCaseI.lean`.
- That file defines:
  - the explicit one-step map `fullMap1CaseI` on `FullCoord`,
  - the compact layer-zero dispatcher `dir1CaseILayerZero`,
  - the induced `m`-step return map `returnMap1CaseI` on `P_0`,
  - and proves the key return theorem
    `iterate_m_fullMap1CaseI_slicePoint_zero`.
- Structurally, this prototype is genuinely smaller than the splice proof at the
  `m`-step return level: for color `1`, Case I, layers `1` and `2` are fixed and
  layers `S ≥ 2` use only direction `1`, so the full `m`-step return is determined by
  the first two low-layer steps and then a trivial tail.
- Important correction after the first probe:
  - the initial dispatcher was not yet the exact Case-I color-`1` geometry, because it
    treated `(m-2,1)` as part of the diagonal `+2` family.
  - the manuscript’s actual Case-I formula for `R_1` excludes `i = m - 2` from the
    diagonal family, so `(m-2,1)` is an isolated `+1` stall.
  - `formal/TorusD3Odometer/Color1FullCaseI.lean` is now corrected to that actual
    geometry.
- After that correction:
  - small finite checks agree with the manuscript’s Case-I first-return formulas
    `T1CaseI / rho1CaseI`,
  - the induced `P_0` return map is again bijective in the actual Case-I congruence
    classes,
  - and the file now contains the first reusable first-return layer:
    `linePoint1`, its range lemma, the bulk iterate lemma, branch lemmas for the
    corrected `R_1`, and the exact line-return cases `x = 0` and `x = m - 2`.
  - Update: the generic odd Case-I family is now fully wired in
    `formal/TorusD3Odometer/Color1FullCaseI.lean`.
  - The file now contains the explicit odd-family chain
    `prefix -> diagonal +2 stall -> middle bulk -> vertical +1 stall -> suffix bulk`,
    packaged as `iterate_returnMap1CaseI_odd_generic` and
    `firstReturn_line_odd_generic`.
  - So the bounded probe has passed the first real stress test: at least for the odd
    generic lanes, the odometer rewrite still closes by composing a small number of
    reusable geometric blocks rather than collapsing back into splice-style row
    transcription.
  - Update: the even generic family is now also fully wired in the same style.
  - `formal/TorusD3Odometer/Color1FullCaseI.lean` now contains the full even-family
    chain
    `prefix -> vertical +1 stall -> middle bulk -> diagonal +2 stall -> suffix bulk`,
    packaged as `iterate_returnMap1CaseI_even_generic` and
    `firstReturn_line_even_generic`.
  - So the bounded probe now closes both generic families by composing a small number
    of reusable geometric blocks.
  - Important negative checkpoint:
    the first direct attempt to package the boundary lane `x = m - 3` as one long
    monolithic theorem was rolled back.
  - The rollback was not due to a mathematical error; it was due to proof-shape blowup
    around nested `Function.iterate_add_apply` rewrites, endpoint cast normalizations,
    and low-level `Fin` / `ZMod` bookkeeping.
  - `formal/TorusD3Odometer/Color1FullCaseI.lean` is clean again after that rollback,
    and the live frontier is now specifically the boundary-proof shape, not the generic
    odometer derivation.

Next exact target:
- The unified congruence-dispatch API for colors `1/0` is now implemented.
- The new immediate design question is narrower and more informative:
  does the color-`1`, Case-I prototype remain materially shorter when pushed one layer
  further, namely from the explicit `m`-step return theorem on `P_0` to the
  first-return-to-line theorem recovering `T1CaseI` and `rho1CaseI`?
  - The exact remaining Case-I frontier is now concrete:
  - close the two boundary lanes `x = m - 3` and `x = m - 1`,
  - then decide whether the rewrite is still genuinely shorter than the splice proof
    once the boundary bookkeeping is included.
  - If yes, then the full-map rewrite path for color `1` is likely real.
  - If no, then the correct end state is probably the current hybrid architecture:
  genuine full-map rewrite for color `2`, explicit `m`-step return prototypes where
  they collapse cleanly, and wrapper-level acceptance theorems for the rest.

## D41) D3 color-1 Case-I boundary-lane proof shape after the generic-even milestone

**Decision:** After the generic odd/even Case-I families closed in `formal/TorusD3Odometer/Color1FullCaseI.lean`, do not continue the two boundary lanes as one-off monolithic calc proofs; first decide whether to add a small reusable boundary-lane helper layer or stop the full rewrite at the generic-family milestone.

Options:
1. Keep proving `x = m - 3` and `x = m - 1` directly as large lane-specific calc chains inside `formal/TorusD3Odometer/Color1FullCaseI.lean`.
2. Add a small helper layer in `formal/TorusD3Odometer/Color1FullCaseI.lean` for boundary-lane segments:
   explicit endpoint step lemmas plus reusable bulk-segment lemmas on fixed `u = i - k` lanes, then repackage the two boundary cases from those blocks.
3. Stop the full Case-I rewrite after the generic odd/even milestone and keep the remaining boundary closure only at the wrapper/splice level.

Recommendation:
- Option 2.
- Option 1 already showed the wrong proof shape: the mathematics remained correct, but the proof exploded into nested `iterate_add_apply` bookkeeping and endpoint cast rewrites.
- Option 3 would stop the experiment before testing the only remaining interesting question, namely whether the boundary lanes can still be made block-structured enough to stay materially cleaner than splice transcription.
- A very small helper layer is the honest next experiment because the boundary lanes are not generic, but they still visibly decompose into a short list of bulk segments and isolated stalls in the manuscript.

Risks / mitigations:
- The helper layer could become another local mini-framework with no reuse beyond the two boundary lanes -> keep the helper scope strict: only lane-segment lemmas actually used by `x = m - 3` and `x = m - 1`.
- Even with helpers, the boundary cases may still remain uglier than the splice proof -> treat that as a valid negative result and stop the full rewrite there instead of forcing completion.
- The current file is already buildable -> keep `formal/TorusD3Odometer/Color1FullCaseI.lean` clean after every helper addition so the experiment remains low-risk.

Open questions:
- Can one shared boundary helper layer cover both `x = m - 3` and `x = m - 1`, or do they need unrelated local proofs?
- If the boundary lanes close, does the remaining `hfirst` / counting layer still look cleaner than the existing splice proof, or does the complexity reappear there?

Rollout / acceptance:
- First add only the smallest helper layer needed for the boundary lanes.
- Accept Option 2 only if both Case-I boundary lanes close from those helpers while keeping `formal/TorusD3Odometer/Color1FullCaseI.lean` materially smaller in structure than the splice baseline.
- If the helper layer itself becomes another large case-split framework, stop and keep the current hybrid architecture.

## D40) D5 next-branch scope after the exact checked-range carry-coding extraction

**Decision:** After `047`, stop describing the next D5 carry branch as a vague
search over larger future sheets. On the checked active branch, the hidden
datum has sharpened to `tau` with a tiny boundary correction, and the next
honest local branch is admissible/local coding of that `tau` target.

Options:
1. Keep describing the next branch broadly as a future-sheet search.
2. Treat `047` as the new exact checked-range carry target and search for an
   admissible/local coding of `tau`, using the boundary event class only as a
   secondary correction.
3. Stop local search and move only to theorem packaging of `044/045/046/047`.

Recommendation:
- Option 2.
- `047` verifies on `m = 5,7,9,11` that:
  - the `tau=0` boundary event class is genuinely `3`-class minimal,
  - the first exact checked-range quotient is
    `B + min(tau,8) + epsilon4`,
  - the unique minimal exact contiguous interval quotient on
    `tau in {0,...,9}` is
    `{0,1}|{2}|{3}|{4}|{5}|{6}|{7}|{8,9}`,
  - the first exact checked-range transition-sheet coding is
    current `B` plus current `epsilon4` plus the next `7` future binary
    flat/nonflat indicators after the current step,
  - full `4`-class event windows become exact at horizon `8`,
  - pure future binary windows become exact only at horizon `10`.
- So the next live object is no longer “some larger future window.” It is
  `tau`, with `epsilon` as a boundary correction.

Risks / mitigations:
- `047` is still a checked active-union extraction, not yet a theorem for all
  odd `m` -> keep it as a structural boundary, and package theorem work in
  parallel instead of overclaiming uniformity.
- The checked-range cap `min(tau,8)` could be overread as a universal closed
  form -> record it as a checked-range fact, and treat the theorem-side
  question as whether the real uniform target is full `tau` or a capped form.
- Local search could still drift back into generic observable widening ->
  require future branches to state explicitly how they code `tau`, not merely
  “more future data.”

Open questions:
- Can the checked-range `047` target be upgraded symbolically to a uniform-in-`m`
  theorem?
- What is the smallest admissible/local coding of `tau`?
- Is the exact checked-range `7`-step binary-after-current coding already the
  right manuscript object, or just the first surviving computational family?

Rollout / acceptance:
- Save `047` as the exact checked-range carry-coding artifact.
- Update the RoundY docs so the current message is:
  `046` found the exact future-transition carry event, `047` pruned it to
  `tau` plus a boundary correction and extracted the first exact checked-range
  transition-sheet coding.
- Keep the next autonomous local branch on admissible/local coding of `tau`,
  not on generic broader future-sheet search or residual-sheet realization.

## D42) D5 next-branch scope after the tau countdown-carrier extraction

**Decision:** After `048`, stop treating the live D5 carry datum as an opaque
future window. On the checked active nonterminal branch, `tau` already has
exact internal dynamics as a countdown carrier with a tiny boundary reset law,
so the next honest local branch should target that carrier explicitly.

Options:
1. Keep framing the next local branch as admissible coding of a generic future
   `tau` window.
2. Treat `048` as closing the autonomous `047A` question and target an
   admissible/local coding of the countdown carrier itself, with the boundary
   reset handled as a small current-state micro-law.
3. Stop local search entirely and move only to theorem packaging of
   `044/045/046/047/048`.

Recommendation:
- Option 2.
- `048` verifies on `m = 5,7,9,11` that:
  - for every checked active nonterminal row with `tau > 0`,
    `tau_next = tau - 1` exactly;
  - all nontrivial dynamics are confined to the boundary `tau = 0`;
  - on that boundary,
    `wrap -> 0`,
    `carry_jump` resets exactly on `(s,v,layer)`,
    and `other` resets exactly on `(s,u,layer)`;
  - equivalently, the full next-`tau` map is exact on
    `(tau, epsilon4, s, u, v, layer)`,
    and no smaller current `B`-subset with `epsilon4` is exact on the
    boundary.
- So the live object is no longer “future data about tau.” It is a countdown
  carrier plus a tiny reset law.

Risks / mitigations:
- `048` is still a checked active-union extraction on `m = 5,7,9,11`, not yet
  a symbolic theorem for all odd `m` -> keep it as a structural boundary and
  package proof work in parallel.
- The boundary reset quotients could be overread as the final admissible/local
  answer -> state them honestly as reduced dynamic targets, not as already
  exposed local observables.
- Local work could still drift into generic observable widening -> require any
  new branch to say explicitly how it codes the positive countdown and how it
  handles the `tau=0` reset.

Open questions:
- Can the countdown/reset law be upgraded symbolically to a uniform-in-`m`
  theorem?
- What is the smallest admissible/local coding of the positive countdown of
  `tau`?
- Is the right next local object a direct `tau`-carrier, or a surrogate whose
  dynamics semiconjugate to this countdown/reset law?

Rollout / acceptance:
- Save `048` as the tau countdown-carrier artifact.
- Update the RoundY docs so the current message is:
  `046` found the exact future-transition carry event, `047` pruned it to
  `tau` plus a boundary correction, and `048` reduced `tau` itself to a
  countdown carrier with tiny reset law.
- Keep any further autonomous local search explicitly on countdown-carrier
  coding, not on generic future-window widening.

## D43) D3 color-1 Case-I odometer package after the boundary dispatcher milestone

**Decision:** After `formal/TorusD3Odometer/Color1FullCaseI.lean` closed the
full Case-I line first-return dispatcher and the full-map `m`-step return to
`returnMap1CaseI`, do not immediately brute-force the remaining Case-I endgame
(`sum_rho1CaseI`, `hsum_caseI`, `hfirst`, final `m^2` / `m^3` cycle theorems)
as more local calc code. First decide whether to add one tiny reusable
finite-sum helper layer, or stop the Case-I full rewrite at the current clean
dispatcher milestone.

Options:
1. Keep all remaining work local to
   `formal/TorusD3Odometer/Color1FullCaseI.lean`: brute-force the `rho1CaseI`
   sum over `Fin m`, then add `hfirst`, then finish the counting/lift package.
2. Add one very small reusable helper layer for the sum/counting part
   (for example a `Fin`/`range` transport lemma and/or a short range-tail split
   lemma in `formal/TorusD3Even/Counting.lean` or locally in
   `formal/TorusD3Odometer/Color1FullCaseI.lean`), then finish the Case-I
   package on top of that.
3. Stop the full Case-I odometer rewrite at the current buildable milestone:
   keep the proved dispatcher/return theorems, but leave the final cycle
   package to the existing splice-based results.

Recommendation:
- Option 2.
- The mathematics is no longer the issue. `formal/TorusD3Odometer/Color1FullCaseI.lean`
  already has:
  - the full Case-I line first-return dispatcher,
  - `cycleOn_T1CaseI_caseI`,
  - `hreturn_line_caseI`,
  - `blockTime_eq_sum_range`,
  - and the full-map `m`-step return theorem `iterate_m_fullMap1CaseI_slicePoint_zero`.
- The first failed continuation attempt showed the real remaining friction:
  finite-sum proof engineering around `sum_rho1CaseI` / `hsum_caseI`, not new
  orbit structure.
- A tiny helper layer is the honest next experiment because the same
  `Fin`/`range` transport and short tail-splitting pattern is exactly the sort
  of proof noise that will recur if the odometer tree grows further.
- Update: this experiment succeeded on the sum/counting side. The file now has
  explicit `rho1CaseI` endpoint/generic value lemmas together with
  `sum_rho1CaseI` and `hsum_caseI`, and `lake build TorusD3Odometer` is clean
  again after that addition.
- Update: the original D43 question is therefore resolved in the positive for
  the arithmetic layer. The remaining unresolved part is no longer
  `Fin`/`range` transport; it is the Case-I no-early-return package `hfirst`,
  which still appears to require genuinely casewise reasoning.
- Update: the remaining `hfirst` package also closed cleanly enough. The file
  `formal/TorusD3Odometer/Color1FullCaseI.lean` now contains
  `hfirst_line_caseI`, `cycleOn_returnMap1CaseI_caseI`, and
  `cycleOn_fullMap1CaseI_caseI`, and `lake build TorusD3Odometer` succeeds.
- Update: D43 is therefore resolved positively end-to-end for color `1`,
  Case I. The real remaining question is no longer local proof engineering
  inside this file; it is whether the odometer tree should now pursue another
  genuine full rewrite family, or stop at this successful prototype boundary.

Risks / mitigations:
- The helper layer could sprawl into a generic arithmetic library unrelated to
  the actual D3 goal -> keep it strict: only the lemmas needed to close
  `sum_rho1CaseI` / `hsum_caseI`.
- The helper may not pay off if `hfirst` still dominates the remaining work ->
  reassess immediately after the sum/counting layer closes; do not auto-commit
  to full Case-I completion beyond that.
- The current file is buildable again -> preserve that invariant after every
  helper attempt.

Open questions:
- Answered: yes, a tiny arithmetic/helper layer was enough to make the
  Case-I sum/counting layer routine.
- Remaining: after the sum/counting layer is closed, does `hfirst` still look
  materially cleaner than the splice proof, or does the rewrite lose its
  aesthetic edge there?

Rollout / acceptance:
- Keep the current buildable checkpoint in
  `formal/TorusD3Odometer/Color1FullCaseI.lean`.
- Completed: add only the smallest helper layer required to prove
  `sum_rho1CaseI` and `hsum_caseI`.
- Completed: the `hfirst` layer and the final `m^2` / `m^3` closure remained
  small enough to justify the experiment.
- Next acceptance gate: decide whether to attempt one more genuine full-family
  odometer rewrite beyond Case I, or freeze the odometer tree at the current
  successful prototype boundary.

## D44) D3 odometer scope after the completed color-1 Case-I prototype

**Decision:** After `formal/TorusD3Odometer/Color1FullCaseI.lean` closed all
of Case I through the full `m^3` cycle theorem, decide whether to continue the
parallel odometer rewrite beyond the current asymmetric but successful
checkpoint.

Options:
1. Stop here and accept the current odometer tree as the final presentation:
   - full rewrite for color `2`,
   - full rewrite for color `1`, Case I,
   - wrapper-level lane-cycle APIs for the remaining color `1` / `0` families.
2. Run one bounded second full-rewrite experiment on color `1`, Case II,
   using a new file and the same acceptance bar as Case I.
3. Commit now to full explicit odometer rewrites for all remaining color `1`
   and color `0` families.

Recommendation:
- Option 2.
- We now have enough evidence that the full-rewrite idea is real, but not yet
  enough evidence that it scales gracefully beyond the cleanest nontrivial
  family.
- Case I is no longer just a promising scaffold; it is a completed parallel
  rewrite. That makes one more bounded experiment worthwhile.
- Color `1`, Case II is the right test: it is closer to the Case-I geometry and
  helper layer than color `0`, but it is still materially more complex than the
  current success case.
- Do not jump directly to Option 3. That would spend effort before answering
  the actual architectural question.

Risks / mitigations:
- Case II may collapse into disguised splice transcription rather than a clean
  odometer derivation -> stop immediately if the proof shape starts replicating
  the old case-by-case route at comparable size.
- A second rewrite attempt could create a parallel helper forest ->
  any new helper must either be shared with `formal/TorusD3Odometer/Color1FullCaseI.lean`
  or remain strictly local to the new prototype file.
- The current checkpoint is already mathematically valuable -> preserve the
  buildable `TorusD3Odometer` baseline before every new experiment.

Open questions:
- Does color `1`, Case II admit the same clean pattern:
  lane cycle -> return-time sum -> casewise `hfirst` -> full-map lift?
- If Case II fails the cleanliness bar, is that enough evidence to declare the
  current wrapper architecture the final endpoint for the remaining families?

Rollout / acceptance:
- Start with a separate `formal/TorusD3Odometer/Color1FullCaseII.lean` file.
- First milestone: full `m`-step return theorem to the Case-II return map.
- Second milestone: if that is clean, continue through `hreturn`, `hsum`,
  `hfirst`, and the final `m^2` / `m^3` cycle theorems.
- Abort the experiment if the proof shape becomes splice-sized or requires a
  second large ad hoc boundary framework.

Update:
- `formal/TorusD3Odometer/Color1FullCaseII.lean` now exists and builds as a
  separate prototype file.
- The first milestone is achieved: the file contains the full generic color-1
  low-layer core and the theorem
  `iterate_m_fullMap1CaseII_slicePoint_zero`.
- The implementation result is cleaner than the initial fear: Case II reuses
  the same low-layer `fullMapColor1` / `returnMapColor1` architecture as
  Case I, with only the layer-0 classifier changed.
- A small reusable local API was enough to keep the next step concrete:
  `dir1CaseIILayerZero_eq_two_of_not_special`,
  `returnMap1CaseII_eq_bulk_of_not_special`,
  the line compatibility lemmas for `x = 0, 1, m - 2`,
  and the first nontrivial return case
  `firstReturn_line_two`.
- The important engineering finding is that the right proof shape for the
  Case-II step chain is:
  bulk-prefix theorem -> named special-point lemmas -> short successor-chain
  packaging. Direct rewriting on iterate exponents was brittle because of the
  local `Fact (5 < m)` instance; auxiliary `1 + n` lemmas were stable.
- The generic even family is now closed in
  `formal/TorusD3Odometer/Color1FullCaseII.lean`. The odd family also now has
  a stable first-half core in the same file:
  odd bulk prefix -> first diagonal stall -> bulk middle -> the two vertical
  defects. Those lemmas build cleanly and confirm the manuscript stall pattern
  is the right organizing principle here too.
- The safe odd-generic package is now closed as well, but under the honest
  bound `3 ≤ x ≤ m - 7`: the file now builds through the full second-diagonal
  / tail block and the final `rho = m + 4` theorem for that uniform subfamily.
- The first genuine Case-II odd wrinkle is now explicit and local:
  the naive odd-tail bulk window is uniform only for `3 ≤ x ≤ m - 7`.
  The endpoint `x = m - 5` still belongs to the manuscript's generic odd
  family, but it needs a tiny separate tail argument because the post-second-
  diagonal tail reaches the `i = 0` boundary at height `m - 1`, where the
  "just keep using the same bulk bound" proof shape stops being literally
  true.
- Current next frontier: split off the small `x = m - 5` endpoint argument,
  then handle the true boundary lanes `x = m - 3` and `x = m - 1`.
- Current status judgment: the experiment is still inside the intended
  cleanliness bar. It has not yet collapsed into splice-sized transcription.
- The boundary lanes `x = m - 5`, `x = m - 3`, and `x = m - 1` are now all
  closed in `formal/TorusD3Odometer/Color1FullCaseII.lean`, and the file
  builds cleanly again.
- A useful next-layer artifact was added there: the standalone timing function
  `rho1CaseII`. This is the right data for the eventual
  `hreturn` / `hsum` / `hfirst` packaging.
- The first failed packaging attempt was informative and was rolled back
  before accepting the checkpoint. The blocker was not new orbit mathematics.
  It was proof engineering around the nested dependent `if` terms inside
  `rho1CaseII`: direct `rw` / `simp` on goals of the form
  `(returnMap^[rho1CaseII x]) ...` was brittle because the goal kept the
  local `Decidable` proof binders from the `if`s.
- Recommendation for the next pass: do not retry the full dispatcher/counting
  layer directly. First add tiny explicit value lemmas for `rho1CaseII`
  (`0`, `1`, `2`, generic even, generic odd, `m-5`, `m-3`, `m-2`, `m-1`)
  using `split_ifs` or a similarly stable local pattern, then build
  `hreturn_line_caseII` and `sum_rho1CaseII` on top of those lemmas.
- Current status judgment after that rollback: the experiment is still healthy,
  but the next bottleneck has shifted from orbit decomposition to the
  dependent-`if` normalization layer.
- That recommendation was correct. The explicit `rho1CaseII` value layer is
  now in place, and it was enough to close both `hreturn_line_caseII` and the
  counting side (`sum_rho1CaseII`, `hsum_caseII`) in
  `formal/TorusD3Odometer/Color1FullCaseII.lean`.
- `lake build TorusD3Odometer` now succeeds again with the Case-II counting
  layer included, so the prototype remains on a clean root-build checkpoint.
- The next remaining frontier is no longer the `rho` normalization or the
  `Finset` transport. It is `hfirst`.
- Current implementation reading: most of Case-II `hfirst` should be routine
  packaging over already-proved orbit segments. The likely only new helper is
  a generic-even suffix-partial theorem, because the even family currently has
  a full suffix theorem to time `x`, but not the corresponding partial version
  for `0 < t < x`.
- Recommendation for the next pass: keep the same bounded-experiment rule.
  First do the trivial `rho = 1` lanes and the `x = 2` case. If generic-even
  `hfirst` really needs only that one suffix-partial helper, add it and
  continue. Abort only if `hfirst` starts demanding a second ad hoc local
  framework instead of small packaging lemmas.
- That bounded pass succeeded for the endpoint layer. The file now builds with
  `hfirst_line_even_generic_caseII`, `hfirst_line_m_sub_three_caseII`, and
  `hfirst_line_m_sub_one_caseII` all closed, and `lake build TorusD3Odometer`
  succeeds again from the root.
- The useful proof-engineering finding is specific and reproducible: the
  unstable copied negative-tail proof for `x = m - 1` was the wrong shape.
  The stable shape was to reuse the already-proved positive-tail orbit
  milestones
  `iterate_returnMap1CaseII_m_sub_one_front`,
  `iterate_returnMap1CaseII_m_sub_one_middle`,
  `returnMap1CaseII_two_m_sub_three`,
  and the local partial bulk lemmas, then prove non-return from the second
  coordinate alone.
- Current next frontier: the remaining missing Case-II layer is now exactly the
  odd-family `hfirst` packaging (`3 ≤ x ≤ m - 7` and the endpoint `x = m - 5`)
  plus the final global dispatcher / `m^2` / `m^3` wrapper theorems.
- Current status judgment: this is still local proof packaging, not a new
  architectural decision. The next likely helpers are odd-family partial
  segment lemmas analogous to the already-successful Case-I odd partial layer.
- That final bounded pass also succeeded. `formal/TorusD3Odometer/Color1FullCaseII.lean`
  now closes the odd-family `hfirst` layer, the special endpoint
  `hfirst_line_m_sub_five_caseII`, the global dispatcher `hfirst_line_caseII`,
  and the full cycle theorems
  `cycleOn_returnMap1CaseII_caseII` / `cycleOn_fullMap1CaseII_caseII`.
- The small-helper strategy was the correct one. The reusable odd-family
  partial layer
  `iterate_returnMap1CaseII_odd_prefix_partial`,
  `iterate_returnMap1CaseII_odd_middle_partial`,
  `iterate_returnMap1CaseII_odd_suffix_prefix_partial`,
  `iterate_returnMap1CaseII_odd_suffix_tail_partial`
  was enough to close the generic odd `hfirst` package without re-expanding
  the full first-return proof.
- The one genuinely non-uniform endpoint remained `x = m - 5`, exactly as the
  earlier checkpoint predicted. The right resolution was not a second generic
  framework, but one local tail theorem
  `iterate_returnMap1CaseII_m_sub_five_suffix_tail_prefix_partial`
  plus explicit arithmetic normalizations for `a = 2`, `b = m / 2 - 3`, and
  the milestone `(m / 2 + 1, m / 2)`.
- Root verification remains clean: `lake build TorusD3Odometer` succeeds with
  the completed Case-II rewrite included.
- Outcome of the bounded Case-II experiment: it passed the cleanliness bar.
  The full color-1 odometer rewrite is now complete for both Case I and
  Case II, so the next scope question is no longer whether Case II works; it
  is whether the odometer tree should now stop at this strong color-1
  checkpoint or attempt a color-0 full rewrite.
- The bounded color-0 full-rewrite experiment has now started in
  `formal/TorusD3Odometer/Color0FullCaseI.lean`.
- The decisive architectural choice was to split the job in two layers:
  use the original `(i,k)` coordinates for the full-map object and its
  low-layer word table, but keep the linear change of variables
  `(x,y) = (i + 2k, k)` explicit as a separate equivalence for the later
  line-return proofs.
- That choice is now validated by code, not just by intent:
  the file contains the original Case-I layer-0 classifier
  `dir0CaseILayerZero`, the full map `fullMap0CaseI`, the explicit
  return map `returnMap0CaseI`, the equivalence
  `toXY` / `fromXY` / `xyEquiv`, and the line embedding `linePoint0`.
- The first reusable full-map core is also in place and builds:
  `iterate_KMap0`, `iterate_fullMap0CaseI_from_three`,
  `iterate_m_sub_three_fullMap0CaseI`, and the first batch of low-layer word
  lemmas, including the realized words `110`, `020`, `120`, `122`, `010`,
  `212`, and the remaining color-`2`-start packages
  `222` / `220` through the generic theorems
  `iterate_three_fullMap0CaseI_of_dir2_i_ne_zero_sum_zero` and
  `iterate_three_fullMap0CaseI_of_dir2_i_ne_zero_generic`.
- Important implementation finding: the original-coordinate full map is clean
  only if the layer-2 rule is stated with the actual middle coordinate
  condition `i + k = 2`. An earlier attempt that used `k = 0` was wrong and
  was corrected immediately before building further.
- Current next frontier: finish the remaining easy Case-I low-layer
  specializations on the `i = 0` / `dir = 2` side, then package
  the global `iterate_m_fullMap0CaseI_slicePoint_zero` theorem and only after
  that move on to the xy-side first-return / `hfirst` layer.
- Current status judgment: the color-0 experiment still satisfies the bounded
  prototype bar. No new architectural blocker has appeared; the remaining work
  is theorem packaging on top of an already-stable transducer shape.
- The full-map side is now actually closed for Case I:
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains the global
  `iterate_m_fullMap0CaseI_slicePoint_zero` theorem, the return-time layer
  `rho0CaseI`, and the counting identity `sum_rho0CaseI = m^2`.
- The xy-side bridge is also now started in the same file:
  `returnMap0CaseIXY`, the conjugacy lemmas
  `returnMap0CaseI_semiconj_xy` /
  `returnMap0CaseI_semiconj_xy_symm`, and the concrete special-point / line
  step lemmas for
  `(0,0)`, `(m-2,0)`, `(1,1)`, `(m-1,m-1)`, `(0,1)`, `(m-2,m-1)`,
  generic line starts, and the `x = m-1` start.
- Implementation finding from the first xy-side pass: a fully generic
  “vertical bulk step” or “diagonal bulk jump” theorem was the wrong proof
  shape here. The proof burden moves from geometry to ZMod/nat-cast transport,
  and the abstraction cost is higher than the reuse obtained.
- Recommendation for the next pass:
  keep the current xy-side point lemmas, do not generalize them further yet,
  and instead build the Case-I proof with the same pattern that worked in
  color `1`:
  case-specific partial iterate theorems first, then `hreturn`, then `hfirst`.
- That next pass is now partially realized and root-verified:
  `lake build TorusD3Odometer` succeeds with the expanded
  `formal/TorusD3Odometer/Color0FullCaseI.lean` checkpoint.
- The file now contains the first genuine xy-side partial-iterate layer for
  color `0`, Case I:
  `verticalMap0XY`,
  `iterate_returnMap0CaseIXY_prefix_partial`,
  `returnMap0CaseIXY_diag_step`,
  `iterate_returnMap0CaseIXY_suffix_partial`,
  and the first packaged generic return theorem
  `firstReturn_line_generic`.
- The important implementation finding is mathematical, not just proof
  engineering:
  the honest uniform generic band is `2 ≤ x ≤ m - 5`, not
  `1 ≤ x ≤ m - 5`.
  At `x = 1`, the point `(2,1)` is already a diagonal defect, so the naive
  “vertical prefix first” theorem is literally false there.
- This means the Case-I color-0 line analysis should now be organized as:
  special `x = 0`,
  boundary `x = 1`,
  generic `2 ≤ x ≤ m - 5`,
  and the upper boundary / specials near `m - 4`, `m - 3`, `m - 2`.
- Recommendation for the next pass:
  do not try to re-extend the generic theorem downward again.
  Instead, add the explicit `x = 1` boundary return package next, then check
  whether `x = m - 4` also needs its own short boundary theorem before
  attempting the global Case-I dispatcher.
- That `x = 1` boundary step is now done.
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains
  `firstReturn_line_one`, and `lake build TorusD3Odometer` still succeeds.
- The useful reproducible finding from that proof is that the right shape is
  not another mini-framework:
  one line-start lemma,
  one diagonal milestone,
  then a direct reuse of the already-proved suffix-partial theorem.
- Current next frontier: test the upper boundary `x = m - 4`.
  If it also needs a short explicit theorem, keep it local and then assemble
  the global Case-I `hreturn` dispatcher from
  `x = 0`, `x = 1`, generic `2 ≤ x ≤ m - 5`, and the upper boundary /
  special lanes near `m - 4`, `m - 3`, `m - 2`.
- That upper-boundary test has now been resolved positively:
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains the local boundary
  package `firstReturn_line_m_sub_four`, together with the auxiliary special
  point theorem `returnMap0CaseIXY_m_sub_two_m_sub_two`. The trivial
  `x = 0` lane is also now packaged explicitly as
  `firstReturn_line_zero_case0`.
- The reproducible proof-engineering finding is sharper than “add more
  boundary theorems”: the right generic/boundary split is to widen only the
  prefix and diagonal machinery from `x ≤ m - 5` to `x ≤ m - 4`, keep the
  suffix machinery on the honest generic range `x ≤ m - 5`, and bridge the
  actual upper boundary with one explicit top-corner point lemma at
  `(m - 2, m - 2) -> (m - 2, m - 1)`.
- This confirms that `x = m - 4` is a real local boundary, but not a reason
  to rebuild the generic framework. The successful shape is the same bounded
  style as for `x = 1`: reuse the generic partials up to the last honest
  milestone, then finish with one or two explicit special-point steps.
- Root verification remains clean after this extension:
  `lake env lean TorusD3Odometer/Color0FullCaseI.lean` and
  `lake build TorusD3Odometer` both succeed.
- Current next frontier: the remaining genuinely exceptional Case-I lanes are
  now concentrated in `x = m - 3`, `x = m - 2`, and `x = m - 1`. The next
  bounded pass should close those three lanes explicitly and only then decide
  whether the global Case-I `hreturn` dispatcher can be assembled without a
  new helper framework.
- That next bounded pass has already improved the reusable layer once more.
  The prefix / diagonal machinery in
  `formal/TorusD3Odometer/Color0FullCaseI.lean`
  (`returnMap0CaseIXY_prefix_step`,
  `returnMap0CaseIXY_diag_step`,
  `iterate_returnMap0CaseIXY_prefix_partial`)
  is now verified on the wider range `x ≤ m - 2`, not merely `x ≤ m - 4`.
- That widening is mathematically real, not a proof artifact. It closes the
  `x = m - 1` lane cleanly, and the file now contains the theorem
  `firstReturn_line_m_sub_one_case0` in addition to
  `firstReturn_line_zero_case0`,
  `firstReturn_line_one`,
  `firstReturn_line_generic`,
  and `firstReturn_line_m_sub_four`.
- The updated reusable picture is now:
  prefix / diagonal behavior remains valid through the last column
  `x = m - 2`,
  but the suffix behavior is still honestly generic only on
  `x ≤ m - 5`.
  This asymmetry is the key design fact for the remaining proofs.
- That asymmetry has now tightened further in a useful way.
  The suffix layer in `formal/TorusD3Odometer/Color0FullCaseI.lean`
  (`returnMap0CaseIXY_suffix_step`,
  `iterate_returnMap0CaseIXY_suffix_partial`)
  no longer needs the old lower-bound hypothesis `1 ≤ x`; it now works on the
  full natural range `0 ≤ x ≤ m - 5`.
- This was immediately strong enough to keep the `x = m - 1` lane short:
  `formal/TorusD3Odometer/Color0FullCaseI.lean` now contains
  `firstReturn_line_m_sub_one_case0`, and `lake build TorusD3Odometer`
  remains clean.
- The reusable picture is therefore now asymmetric in the productive way:
  prefix / diagonal reach all the way up to `x = m - 2`,
  suffix reaches all the way down to `x = 0`,
  and the remaining proof burden is concentrated only at the handful of true
  corner transitions where those bands meet.
- That prediction has now been tested once successfully.
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains the explicit theorem
  `firstReturn_line_m_sub_three_case0`, and it closed without adding a new
  family of helper lemmas. The winning proof shape was:
  line start at `x = m - 3`,
  widened prefix on the same column,
  widened diagonal at `x = m - 3`,
  the existing special point `(-1,-1) -> (2,2)`,
  then the widened suffix at `x = 0`.
- So the current residual difficulty is now sharply isolated:
  only the `x = m - 2` Case-I lane remains before attempting the global
  Case-I `hreturn` dispatcher.
- Current recommendation:
  treat `x = m - 2` as the next bounded experiment, but expect it to be the
  first place where a tiny dedicated helper layer for the `x = 0` / `x = 1`
  columns may actually be justified. If that helper layer stays small and
  local, keep going; if it starts growing into a second mini-framework, stop
  there and record the asymmetry explicitly.
- That bounded `x = m - 2` experiment has now succeeded cleanly.
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains the local helper
  layer
  `returnMap0CaseIXY_zero_column_step`,
  `iterate_returnMap0CaseIXY_zero_column_partial`,
  `returnMap0CaseIXY_zero_m_sub_one`,
  `returnMap0CaseIXY_one_column_step`,
  `iterate_returnMap0CaseIXY_one_column_partial`,
  `returnMap0CaseIXY_one_m_sub_one`,
  and the resulting boundary theorem
  `firstReturn_line_m_sub_two_case0`.
- The reproducible proof pattern is now explicit:
  `x = m - 2` is not another generic band extension.
  The right proof shape is
  start step to `(0,2)`,
  a zero-column climb to `(0,m-1)`,
  one special corner step to `(1,1)`,
  the existing short steps through `(0,1)` and `(1,2)`,
  then a one-column climb to `(1,m-1)` and the final special step to
  `(1,0)`.
  So the earlier “tiny dedicated helper layer for the `x = 0` / `x = 1`
  columns” prediction was exactly right.
- The next routine layer after that also now succeeds and builds:
  `formal/TorusD3Odometer/Color0FullCaseI.lean` contains the global Case-I
  line-return dispatcher `hreturn_line_case0_caseI` and the counting theorem
  `hsum_case0_caseI`.
- This means the remaining unfinished part of the color-0 Case-I odometer
  rewrite is no longer `hreturn` or the `m^2` timing sum. The next honest
  frontier is `hfirst`: a no-early-return package for the same Case-I lane
  families. Root verification remains clean after this extension:
  `lake env lean TorusD3Odometer/Color0FullCaseI.lean` and
  `lake build TorusD3Odometer` both succeed.
- Updated recommendation:
  the current checkpoint is strong enough to keep as-is. The next bounded
  experiment, if pursued, should be exactly the color-0 Case-I `hfirst`
  layer. If that stays on the same “generic family plus a few boundary
  packages” scale, then the full return-map and full-map cycle theorems are
  plausibly within reach. If it instead starts demanding a second local
  framework, that is the correct place to stop and record the asymmetry.
- That bounded `hfirst` experiment has now succeeded cleanly.
  `formal/TorusD3Odometer/Color0FullCaseI.lean` now closes the full Case-I
  odometer rewrite for color `0`, including the boundary packages
  `hfirst_line_one_case0`,
  `hfirst_line_m_sub_four_case0`,
  `hfirst_line_m_sub_three_case0`,
  `hfirst_line_m_sub_two_case0`,
  `hfirst_line_m_sub_one_case0`,
  the generic theorem `hfirst_line_generic_case0`,
  the global dispatcher `hfirst_line_case0_caseI`,
  and the final cycle theorems
  `cycleOn_returnMap0CaseI_caseI` /
  `cycleOn_fullMap0CaseI_caseI`.
- The important reproducible implementation finding is that the `hfirst` layer
  did not require a second helper framework. The successful proof shape stayed
  inside the existing bounded discipline:
  reuse the generic prefix / suffix partials where they are honest,
  add only short local packages for the true boundary lanes,
  and discharge non-return from the second coordinate.
- A second, more structural finding is that the full-map lift must happen on
  the original return map `returnMap0CaseI`, not directly on the xy-side map
  `returnMap0CaseIXY`.
  The correct final pattern is:
  first prove the `m^2` cycle on `returnMap0CaseIXY`,
  then conjugate it back through `xyEquiv.symm` to a cycle on
  `returnMap0CaseI`,
  and only then apply `cycleOn_full_of_cycleOn_p0` to get the `m^3` cycle.
- Root verification remains clean after this closure:
  `lake env lean TorusD3Odometer/Color0FullCaseI.lean` and
  `lake build TorusD3Odometer` both succeed.
- Updated scope judgment:
  color `0`, Case I now also passes the cleanliness bar as a genuine full
  odometer rewrite, not merely as a wrapper over the splice proof.
  This creates a new real scope boundary.
- Recommendation at the new boundary:
  do not automatically jump into all remaining color-0 families.
  The next bounded experiment, if pursued, should be exactly
  color `0`, Case II in a separate file, with the same acceptance bar used for
  color `1`, Case II:
  keep the current checkpoint as a valid endpoint, and continue only if the
  next family stays on the same local-helper scale.
- That bounded color-0 Case-II experiment has now started cleanly in
  `formal/TorusD3Odometer/Color0FullCaseII.lean`, and the first architectural
  milestone is positive.
  The file is imported by `formal/TorusD3Odometer.lean`, and the root build
  still succeeds.
- The confirmed design finding is that color `0`, Case II shares the same
  layer-1 / layer-2 transducer core as color `0`, Case I.
  The only real change at the full-map level is the layer-0 classifier.
  In code, that is now factored as the shared `fullMapColor0` core together
  with the new `dir0CaseIILayerZero`.
- A second useful implementation finding is that the counting side can be
  developed independently of the final orbit packaging.
  The file now has the induced `m`-step return map
  `returnMap0CaseII`,
  its xy transport `returnMap0CaseIIXY`,
  the tautological `iterate_m_fullMap0CaseII_slicePoint_zero` bridge,
  the Case-II return-time function `rho0CaseII`,
  and the completed sum theorem `sum_rho0CaseII`.
- That counting work also exposed a real arithmetic correction worth recording
  for reproducibility:
  the Case-II suffix block total is `9m - 15`, not `7m - 13`,
  because the lane `x = m - 4` remains generic and contributes `m - 2`.
  This was a genuine math/accounting correction, not just a Lean proof-shape
  issue.
- Current scope judgment:
  the experiment is still on the right bounded scale.
  No new framework was needed beyond the shared core and a small counting layer.
- New verified checkpoint in the same file:
  the first reusable xy-side local branch layer is now formalized.
  `formal/TorusD3Odometer/Color0FullCaseII.lean` now contains the missing
  three-step full-map helper packages for the Case-II `dir1` and `dir2`
  subcases, together with the first explicit xy branch lemmas:
  the warm-up `A` point `(2,1) -> (3,3)`,
  the warm-up `A` point `(3,2) -> (4,4)`,
  and the reusable `R`-line theorem on
  `(1 + 2y, y) -> (3 + 2y, y + 2)`.
- Reproducibility note:
  the odometer tex lemma
  `tex/d3torus_complete_m_ge_3_odometer_revision_v9_with_d4_patched.tex`,
  lines `2924–2975`,
  is now the right local blueprint for further Case-II work.
  The useful proof engineering lesson is that the stable reusable layer is
  not the old Case-I prefix/suffix engine, but this explicit branch API
  (`P/Q/R/S/A/B/G`) derived from the Case-II xy formula.
- Next exact frontier:
  use that branch layer to close the warm-up lanes `x = 1` and `x = 2`
  first.
  Concretely, the next local theorem should be the dedicated `G`-tail package
  on the even columns reached after the `A`-jump
  (starting with the column `x = 4` tail for `x = 1`),
  then the first-return theorem for `x = 1`,
  then `x = 2`,
  and only after that the generic band `3 ≤ x ≤ m - 7`.
- The first direct attempt at that `x = 1` step has now been tried and
  deliberately rolled back. The failed local abstraction was a single broad
  theorem for the whole `x = 4` column tail
  (`returnMap0CaseIIXY_four_column_step` plus its iterate wrapper and the
  resulting `firstReturn_line_one_caseII_mod_ten` package).
- That rollback is worth recording because it was a proof-shape failure, not an
  architectural failure. The shared Case-II full-map / return-map core still
  builds cleanly, and `lake build TorusD3Odometer` remains green. The problem
  was narrower: the over-broad four-column theorem mixed three genuinely
  different regimes into one statement:
  the generic band `4 ≤ y ≤ m - 3`,
  the top corner `y = m - 2`,
  and the wrap point `y = m - 1`.
- Reproducible engineering finding from that rollback:
  for color `0`, Case II mod `10`, the stable next layer should not be a
  single theorem over the whole `x = 4` column.
  The better shape is:
  one generic four-column step theorem on the honest band `4 ≤ y ≤ m - 3`,
  then tiny separate boundary lemmas for `y = m - 2` and `y = m - 1`,
  and only after that the partial iterate package and the `x = 1` first-return
  theorem.
- Practical status after the rollback:
  keep the already-verified local branch API,
  keep the full-map / return-map / counting layer,
  and restart from a clean checkpoint with the narrower theorem split above.
  This remains inside the bounded-experiment bar; no new negative evidence
  against the overall color-0 Case-II odometer rewrite has appeared.
- That narrower restart is now partially realized in code.
  `formal/TorusD3Odometer/Color0FullCaseII.lean` contains the explicit split
  of the `x = 4` column into three regimes on the original-coordinate side:
  `fromXY_four_column_lower`,
  `fromXY_four_column_mid`,
  `fromXY_four_column_upper`,
  together with the midpoint successor theorem
  `returnMap0CaseIIXY_four_column_mid_step`.
- Reproducible design finding from that successful helper layer:
  the real special height on the `x = 4` column is
  `y = m / 2 + 2`, where `fromXY (4,y)` lands exactly on the `i = 0` branch.
  Below that height the first coordinate is the explicit nat-cast
  `m + 4 - 2y`; above it the first coordinate is the explicit nat-cast
  `2m + 4 - 2y`.
  So the next pass should use this three-part column decomposition directly
  instead of reintroducing a by-cases theorem over all `4 ≤ y ≤ m - 1`.
- That columnwise approach has now closed the full warm-up lane `x = 1`.
  The file now contains the generic step theorems
  `returnMap0CaseIIXY_four_column_lower_step` and
  `returnMap0CaseIIXY_four_column_upper_step`,
  the partial iterate packages
  `iterate_returnMap0CaseIIXY_four_column_lower_partial`,
  `iterate_returnMap0CaseIIXY_four_column_to_upper_start`,
  `iterate_returnMap0CaseIIXY_four_column_upper_partial`,
  the two top-corner steps
  `returnMap0CaseIIXY_four_column_m_sub_two` and
  `returnMap0CaseIIXY_four_column_m_sub_one`,
  the composed tail theorem
  `iterate_returnMap0CaseIIXY_four_column_to_zero`,
  and the final first-return theorem
  `firstReturn_line_one_caseII_mod_ten`.
- Reproducible implementation lesson from that closure:
  the right unit of abstraction is not “one theorem for the whole repaired
  column,” but
  generic lower band ->
  midpoint step ->
  generic upper band ->
  explicit top-corner steps.
  Once that decomposition is stated, the `x = 1` proof is a short segment
  composition rather than a second monolithic orbit trace.
- Current next frontier:
  the next warm-up lane is `x = 2`, whose manuscript orbit is
  `(2,0) -> (3,1) -> (5,3) -> (5,4) -> (6,6) -> G^{m-6} -> (6,0)`.
  The new checkpoint strongly suggests the right next move is to repeat the
  same pattern on the `x = 6` column rather than to generalize prematurely.
- That `x = 2` warm-up lane is now closed in
  `formal/TorusD3Odometer/Color0FullCaseII.lean`.
  The local entry lemmas are
  `returnMap0CaseIIXY_five_three`,
  `returnMap0CaseIIXY_five_four`,
  the `x = 6` column layer
  `fromXY_six_column_lower`,
  `fromXY_six_column_mid`,
  `fromXY_six_column_upper`,
  the lower/upper generic step theorems,
  the composed tail theorem
  `iterate_returnMap0CaseIIXY_six_column_to_zero`,
  and the final warm-up theorem
  `firstReturn_line_two_caseII_mod_ten`.
- Reproducible design finding from that closure:
  the `x = 6` column is again a three-regime object on the
  original-coordinate side, but simpler than the `x = 4` column.
  The only interior special height is
  `y = m / 2 + 3`, where `fromXY (6,y)` lands on the `i = 0` branch.
  Below that height the first coordinate is the explicit nat-cast
  `m + 6 - 2y`; above it the first coordinate is
  `2m + 6 - 2y`.
- One additional boundary correction is worth recording for reproducibility:
  at the top corner `y = m - 2`, the original-coordinate representative is
  generically `(10,-2)`, but when `m = 10` it collapses to `(0,-2)`.
  So the stable theorem shape is:
  generic lower band ->
  midpoint `i = 0` step ->
  generic upper band ->
  explicit top corner(s),
  with a tiny `m = 10` subcase only at `y = m - 2`.
- Current next frontier:
  the warm-up lanes are now complete for the mod-`10` Case-II family.
  The next bounded step should be the generic band `3 ≤ x ≤ m - 7`,
  reusing the explicit Case-II branch API
  (`B`, `R`, `A`, and the repaired even-column `G` tails)
  rather than trying to compress everything into one global column theorem.
- That generic-band work has now moved from a broken scaffold to a clean,
  reusable checkpoint in
  `formal/TorusD3Odometer/Color0FullCaseII.lean`.
  The file now has the repaired odd generic prefix
  `returnMap0CaseIIXY_odd_generic_even_column_one_step`,
  the lower / midpoint / upper column step theorems on the even column
  `x + 1`,
  the assembled prefix theorem
  `iterate_returnMap0CaseIIXY_odd_generic_to_A`,
  and a new reusable pre-`R` upper-column layer:
  `returnMap0CaseIIXY_upper_column_step`,
  `iterate_returnMap0CaseIIXY_upper_column_partial`,
  the specialized odd-generic bridge
  `iterate_returnMap0CaseIIXY_odd_generic_after_A_to_R`,
  and the mod-`10` `R`-step theorem
  `returnMap0CaseIIXY_odd_generic_R_step`.
- Reproducible implementation finding from that extension:
  the odd generic mod-`10` orbit really does admit a clean decomposition
  matching the odometer tex:
  `B -> G^(x-1) -> A -> G^((m-x-3)/2) -> R`,
  and the right reusable object for the middle segment is not an
  x-specific theorem but a generic upper-column `G`-step on points
  `(c,y)` with `c ≤ y ≤ (m + c - 3)/2`.
  That helper already survives outside the original `x + 1` column.
- New non-routine frontier:
  the next missing block is the post-`R` wrapped upper-column tail on the
  column `x + 4`.
  This is the first place where the generic band meets the top-corner
  behavior, because after the `R` jump the orbit is already above the upper
  `R`-height and the original-coordinate representative switches to the
  wrapped form `2m + c - 2y`.
  The likely next helper layer is therefore:
  wrapped upper-column generic `G` step ->
  its partial iterate package ->
  explicit top-corner lemmas if the boundary lane `x = m - 7` forces them.
- Practical status:
  `lake env lean TorusD3Odometer/Color0FullCaseII.lean` and
  `lake build TorusD3Odometer` both succeed again after this extension.
  So the experiment remains on the accepted bounded scale, but the next step
  is no longer routine warm-up packaging; it is the first genuinely new
  generic-tail helper design for the color-`0`, Case-II mod-`10` rewrite.
- That wrapped-tail design is now implemented and verified in
  `formal/TorusD3Odometer/Color0FullCaseII.lean`.
  The new helper layer is:
  `returnMap0CaseIIXY_wrapped_upper_column_step`,
  `iterate_returnMap0CaseIIXY_wrapped_upper_column_partial`,
  the generic top-corner lemmas
  `returnMap0CaseIIXY_wrapped_upper_column_m_sub_two` /
  `returnMap0CaseIIXY_wrapped_upper_column_m_sub_one`,
  the assembled tail theorem
  `iterate_returnMap0CaseIIXY_wrapped_upper_column_to_zero`,
  the specialized odd-generic tail
  `iterate_returnMap0CaseIIXY_odd_generic_after_R_to_zero`,
  and the first safe generic theorem
  `firstReturn_line_odd_generic_caseII_mod_ten_safe`.
- Reproducible design finding from that closure:
  the wrapped upper-column helper cannot be stated honestly as a generic
  all-`c` theorem.
  The stable statement needs the real mod-`10` parity context plus an odd
  column assumption.
  Concretely, the safe generic odd family closes uniformly only on
  `3 <= x <= m - 11`, where the post-`R` column is `x + 4 <= m - 7`.
  That is exactly the range where the wrapped original-coordinate
  representative stays inside the generic `dir = 1` regime and the two
  generic top corners apply without extra collapse cases.
- Updated exact frontier:
  the next missing odd lanes are now the boundary values
  `x = m - 9` and `x = m - 7`.
  Those are the first places where the `x + 4` column leaves the safe
  wrapped-upper generic regime, so the right next proof shape is
  short boundary-specific tail theorems rather than a larger new framework.
  After those are closed, the odd-family dispatcher should be packaged before
  deciding whether to attack the even band or the global Case-II
  `hreturn`/`hfirst` layer.
- That odd-family branch is now closed through the safe generic theorem
  `firstReturn_line_odd_generic_caseII_mod_ten_safe`, and the next active
  work in `formal/TorusD3Odometer/Color0FullCaseII.lean` has moved to the
  even generic family.
- Reproducible design finding from the even-front-half implementation:
  the stable decomposition is not a direct even-column theorem from the line
  start, but the odometer-style sequence
  `line start -> odd column x + 1 -> R -> odd column x + 3 -> A`.
  Concretely, the reusable theorems are
  `iterate_returnMap0CaseIIXY_even_generic_to_R`
  and
  `iterate_returnMap0CaseIIXY_even_generic_to_A`,
  which close the generic even family on
  `4 <= x <= m - 8`, `Even x`
  through the point `A = (x + 4, x + 4)`.
- Current exact frontier:
  that final even-column tail is now implemented on the honest safe range
  `4 <= x <= m - 12`, `Even x`.
  The new reusable layer in
  `formal/TorusD3Odometer/Color0FullCaseII.lean`
  is:
  `fromXY_even_generic_final_column_lower`,
  `fromXY_even_generic_final_column_mid`,
  `fromXY_even_generic_final_column_upper`,
  the lower / midpoint / upper step theorems,
  the assembled tail theorem
  `iterate_returnMap0CaseIIXY_even_generic_final_column_to_zero_safe`,
  and the resulting safe generic first-return theorem
  `firstReturn_line_even_generic_caseII_mod_ten_safe`.
- Reproducible design finding from that closure:
  the even generic family does not stay uniform all the way to
  `x = m - 8`.
  The safe theorem really is
  `4 <= x <= m - 12`, `Even x`;
  the remaining boundary lanes `x = m - 10` and `x = m - 8`
  are short special cases because the final even column loses its honest
  upper generic band.
- That boundary split is now closed in
  `formal/TorusD3Odometer/Color0FullCaseII.lean` through
  `firstReturn_line_m_sub_ten_caseII_mod_ten`,
  `firstReturn_line_m_sub_eight_caseII_mod_ten`,
  and the full even-family dispatcher
  `firstReturn_line_even_generic_caseII_mod_ten`.
- Reproducible design finding from those two boundary lanes:
  the widened lower/mid final-column helper layer
  `x <= m - 8`
  was enough, but only because
  `x = m - 10` reaches the top via exactly two corner steps and
  `x = m - 8` reaches the top via exactly one corner step.
  No new framework was needed beyond explicit arithmetic equalities for the
  iterate counts and endpoint heights.
- Updated exact frontier:
  the even generic mod-`10` family is now complete, so the next missing
  Case-II inputs are the upper special lanes
  `x = m - 6`, `x = m - 5`, `x = m - 4`,
  `x = m - 3`, `x = m - 2`, `x = m - 1`.
  The correct next move is not another generic family theorem; it is a short
  batch of explicit upper-tail packages on top of the already-proved
  wrapped-upper-column lemmas, and only then the Case-II
  `hreturn` / `hfirst` layer.
- Practical status:
  `lake env lean TorusD3Odometer/Color0FullCaseII.lean` and
  `lake build TorusD3Odometer` both succeed after the full even-family
  extension,
  so the mod-`10` Case-II rewrite remains within the accepted bounded
  experiment scale.
- Incremental closure after that checkpoint:
  `formal/TorusD3Odometer/Color0FullCaseII.lean` now also contains
  `firstReturn_line_m_sub_five_caseII_mod_ten`.
  The key engineering fact from that repair is reproducible:
  the right tail proof does not need a new framework; it needs
  a tiny `dir = 0` original-coordinate kernel together with two explicit
  endpoint transport lemmas
  `returnMap0CaseIIXY_m_sub_three_m_sub_two`
  and
  `returnMap0CaseIIXY_m_sub_two_m_sub_one`,
  then a short four-step xy tail package.
- Updated exact frontier after the `x = m - 5` closure:
  the remaining upper special lanes are now
  `x = m - 6`, `x = m - 4`, `x = m - 3`, `x = m - 2`, `x = m - 1`,
  and after those the odd-family dispatcher should be widened to absorb
  `x = m - 5` before attempting the Case-II
  `hreturn` / `hfirst` layer.
- Incremental closure after that upper-tail batch:
  `formal/TorusD3Odometer/Color0FullCaseII.lean` now also contains
  `firstReturn_line_m_sub_four_caseII_mod_ten`
  and
  `firstReturn_line_m_sub_one_caseII_mod_ten`.
  The reproducible implementation fact is that no new orbit framework was
  needed:
  the clean path was to widen exactly two helper families and then package the
  manuscript traces.
  Concretely:
  the odd-column helpers were widened from `x <= m - 4` to `x <= m - 2`,
  and the wrapped-upper-column helpers were widened from `c >= 7` to
  `c >= 1`.
- Why those widenings are legitimate:
  they do not change the branch logic; they only expose already-valid generic
  zones that were previously left artificially narrow.
  The `x = m - 1` closure then becomes a short composition:
  one explicit start step at `(m - 1,0)`,
  the widened odd-column partial on the same column,
  one `R` hit at height `m / 2 - 1`,
  and the widened wrapped-upper-column tail on column `1`.
- Updated exact frontier after the `x = m - 4` / `x = m - 1` closures:
  the remaining mod-`10` Case-II upper special lanes are now
  `x = m - 6`, `x = m - 3`, and `x = m - 2`.
  After those, the correct next packaging target is the Case-II
  `hreturn` dispatcher, not another helper layer.
- Negative result from the immediately following probe:
  widening the wrapped-upper-column family from odd `c` to arbitrary
  `c >= 1` looked attractive for `x = m - 3`, but the current arithmetic
  proof does not support that simplification cleanly.
  The safe takeaway is narrower:
  keep the successful bound widening `c >= 1`,
  but keep the oddness hypothesis in place until a genuinely new proof is
  written.
- Concrete next-boundary reading of that failure:
  the lane `x = m - 3` does not naturally land in the existing wrapped
  odd-column tail family after the `Q` step; its post-`Q` column is `x = 2`.
  So the next reusable helper, if any, should be a tiny fixed even-column tail
  package for column `2`, not a further attempted widening of the odd-column
  machinery.
- That bounded helper experiment has now succeeded.
  `formal/TorusD3Odometer/Color0FullCaseII.lean`
  now contains the fixed column-`2` package
  `iterate_returnMap0CaseIIXY_two_column_to_zero`,
  the new `Q`-point bridge
  `returnMap0CaseIIXY_m_sub_one_m_sub_one`,
  and the upper-special theorem
  `firstReturn_line_m_sub_three_caseII_mod_ten`.
  The reproducible design fact is exact:
  the right abstraction was a tiny fixed even-column tail package on column
  `2`, not a parity-free widening of the wrapped odd-column family.
- Corrected mathematical endpoint from that closure:
  the lane `x = m - 3` returns to `2`, not to `1`.
  In the odometer rewrite that is now formalized with return time
  `2m - 3`, matching
  `rho0CaseII_eq_two_mul_sub_three_of_val_eq_m_sub_three`.
- Updated exact frontier after the `x = m - 3` closure:
  the remaining mod-`10` Case-II upper special lanes are now
  `x = m - 6` and `x = m - 2`.
  After those two, the correct next packaging target is the Case-II
  `hreturn` dispatcher, and only then the `hfirst` layer.
- Practical status:
  `lake env lean TorusD3Odometer/Color0FullCaseII.lean`
  and
  `lake build TorusD3Odometer`
  both succeed after the new closures, so the bounded color-`0` Case-II
  experiment remains healthy.

## D45) D5 theorem-side minimal object vs compute-side source-residue refinement after 049/050

**Decision:** Keep `(B,tau,epsilon4)` as the main D5 theorem-side object, and
treat `(B,rho)` with `rho = source_u + 1 mod m` as a stronger compute-side
constructive refinement rather than as a replacement coordinate.

Options:
1. Promote `rho` to the main theorem coordinate and rewrite the current
   `044–048` chain in source-memory language.
2. Keep the theorem side minimal on `(B,tau,epsilon4)`, use `049` only as a
   stronger constructive refinement, and use `050` as larger-modulus proof
   support for the existing theorem chain.
3. Ignore `rho` entirely and keep both proof and compute work strictly on the
   minimal future-side cover.

Recommendation:
- Option 2.
- `049` verifies through `m=19` that:
  - `tau` is exact on `(s,u,v,layer,rho)`,
  - `next_tau` is exact on `(s,u,layer,rho,epsilon4)`,
  - `c` is exact on `(u,rho,epsilon4)`,
  - and `q ≡ u-rho+1_{epsilon4=carry_jump} mod m`.
- But `049` also shows that `rho` is not recoverable from `(B,tau,epsilon4)`
  once `m>=7`; on the tested range the ambiguous bucket count matches
  `2m-11`. So `rho` is a stricter current-memory refinement, not the same
  object in different notation.
- `050` then strengthens the proof side without changing the theorem object:
  the `048` reset law remains exact on the same theorem-side quotients through
  `m=19`, and the explicit `047/048` witness pair persists with the same
  `h < m-4` lower-bound shape.
- So the clean split is:
  - proof / manuscript: stay on `(B,tau,epsilon4)`,
  - constructive compute: allow `(B,rho)`,
  - proof-support compute: use `050` to reinforce the existing theorem chain.

Risks / mitigations:
- The proof notes could drift toward the stronger current-memory coordinate and
  lose the clean minimal theorem story -> keep `rho` explicitly labeled as a
  constructive refinement / remark.
- Compute work could fork into incompatible goals -> require future compute
  branches to say whether they are theorem-side (`tau`) or constructive-side
  (`rho`) from the start.
- Larger-modulus support could be overread as a proof -> record `049/050` as
  extended evidence, not as a symbolic theorem for all odd `m`.

Open questions:
- Can a genuine admissible/local mechanism initialize and transport enough of
  `rho` to realize the constructive refinement?
- Can the intended local class be shown to collapse to bounded transition/reset
  data on the theorem-side object, yielding a real no-go theorem?
- Is there a smaller local quotient of `rho` that still realizes `tau` or `c`?

Rollout / acceptance:
- Update the RoundY docs so the current message is:
  theorem side stays minimal on `(B,tau,epsilon4)`,
  compute side may use `(B,rho)`,
  and `050` is proof support rather than a theorem-object change.
- Package `049` and `050` as reproducible artifacts with saved summaries.
- Use `050` in the proof notes only as extended support for the reset law and
  the witness family, not as a change in theorem statement.
