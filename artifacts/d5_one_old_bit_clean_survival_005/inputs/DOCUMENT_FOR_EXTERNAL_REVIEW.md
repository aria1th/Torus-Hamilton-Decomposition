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
