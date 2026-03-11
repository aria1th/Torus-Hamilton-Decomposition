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
