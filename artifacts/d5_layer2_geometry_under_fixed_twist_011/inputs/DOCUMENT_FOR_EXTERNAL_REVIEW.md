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
