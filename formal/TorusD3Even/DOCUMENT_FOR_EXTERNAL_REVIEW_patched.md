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
- Update: `formal/TorusD3Even/Color1.lean` now exists as the first concrete consumer scaffold for that splice path. It already matches the manuscript’s Case-I `m ≡ 2 mod 6` row structurally: the common lane map `T1CaseI`, the return-time function `rho1CaseI`, the block-length data for
  `F11 = (0,2,5,...,m-3)`, `F12 = (1,4,7,...,m-1)`, `F13 = (3,6,9,...,m-2)`, and the sigma-to-`Fin m` block encoding are in place and compile.
- Update: the inside-block successor lemma `pointT1CaseIModTwo_step` is now formalized and compiling, so the unresolved part is narrower than before.
- Update: `formal/TorusD3Even/Color1.lean` now contains the dedicated endpoint helper layer that the previous pass identified as the right proof shape: `T1CaseI_m_sub_three`, `T1CaseI_m_sub_one`, `T1CaseI_m_sub_two`, together with the matching splice-endpoint lemmas `pointT1CaseIModTwo_last_zero`, `pointT1CaseIModTwo_last_one`, and `pointT1CaseIModTwo_last_two`.
- Update: the two remaining code `sorry`s from that file have been replaced by explicit proofs. `index_pointT1CaseIModTwo` is now discharged by a three-case inverse computation on the splice blocks, and `pointT1CaseIModTwo_wrap` now reduces to three short endpoint rewrites instead of a raw nested-`if` normalization proof.
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
