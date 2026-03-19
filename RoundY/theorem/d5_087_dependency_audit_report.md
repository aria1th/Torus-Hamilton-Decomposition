# D5 087 Dependency Audit Report

This note records the first post-`083` dependency audit.

Its purpose is to answer one precise question:

> now that odd-`m` D5 closes inside the accepted package, which imported
> theorems are already safe as theorem-level inputs, and which still deserve
> tightening before broader generalization?

## Executive verdict

The D5 odd-`m` theorem is closed **inside the accepted package**.

No new mathematical bottleneck was found in this audit.

The only issues are packaging and citation discipline:

1. promote the `033` trigger-family formula to a stable theorem note;
2. cite `079` only in its correct role as a chart/interface theorem, not as a
   standalone raw-state continuation theorem;
3. keep `076` labeled as a **componentwise** concrete bridge package, not a
   global one, unless the citation also includes the later globalization steps.

## Audit table

| Input | Role in final proof | Audit result | Action |
|------|----------------------|--------------|--------|
| `033 -> 062` | structural first-exit chain | sound, and now compactly rewritten in `098` | use `098` for cleaned-package citations and keep `033` provenance explicit when needed |
| `076` concrete bridge | componentwise odometer law and event readout | sound at stated scope | keep “componentwise” explicit in citations |
| `077` tail-length reduction | converts endpoint ambiguity to tail-length ambiguity | sound and theorem-level | use `097` for the cleaned-package compact reproof where appropriate |
| `079` interface theorem | pins chart/interface landing to `3m-3 -> 3m-2 -> 3m-1` | sound, but only as chart/interface theorem | use `095` for the cleaned-package compact reproof where appropriate |
| `081` regular continuation | closes regular raw gluing | sound and theorem-level | use `096` for the cleaned-package compact reproof where appropriate |
| `082` exceptional-row reduction | reduces globalization to one clause | sound and theorem-level | no change |
| `083` final proof | closes theorem in-package | sound relative to imported chain | no change |

## Detailed findings

### 1. `033 -> 062` is the main upstream dependency, but it looks coherent

`theorem/d5_first_exit_target_proof_062.md` is the most important structural
import used later.

The audit found no new logical gap there. The note clearly states the required
inputs:

- the exact `H_L1` trigger family,
- the mixed witness rule on current `B`-states,
- the candidate active orbit,
- and the phase-`1` source-residue invariant.

The main packaging issue was simply that the exact `H_L1` formula still lived
implicitly in the `033` artifact line rather than in its own stable theorem
note.

That is now fixed by:

- `theorem/d5_033_explicit_trigger_family.md`

Update after `098`:

- the cleaned package now has the compact structural block at
  `theorem/d5_098_compact_cleanup_033_062_structural_block.md`;
- so the old `033 -> 062` route remains important mainly as provenance for the
  exact trigger-family classification, not as a live theorem-packaging gap.

### 2. `076` is safe, but only at its stated scope

`theorem/d5_076_concrete_bridge_proof.md` is correctly scoped:

- it gives the intrinsic boundary digits,
- the uniform splice law `delta -> delta+1`,
- the current-event readout from `(beta,delta)`,
- and the componentwise image structure.

The audit found no new proof concern there.

The only caution is presentational:

- `076` should never be cited as if it already gave **global** raw
  `(beta,delta)`;
- it gives the concrete bridge package **on each splice-connected accessible
  component**.

That distinction remains important in any final manuscript or summary note.

### 3. `079` was the main chart/interface citation-discipline point

`theorem/d5_079_exceptional_interface_support.md` is deliberately conservative.
It says:

- chart/chain-label exceptional landing is settled;
- raw endpoint compatibility is not yet settled there.

That is the correct scope.

The final `083` proof uses `079` correctly only when combined with `062`:

- `062` gives the actual universal exceptional first exit and branch
  direction;
- `079` pins the corresponding continuation in chart/interface labels to
  `3m-3 -> 3m-2 -> 3m-1`.

So the audit verdict is:

- `079` is sound;
- but it should not be cited alone as an actual-lift continuation theorem.

Update after `095`:

- the exact chain-label statement needed by the cleaned `092` suite is now
  reproved directly in
  `theorem/d5_095_compact_reproof_079_chart_interface_landing.md`;
- so `079` remains important as historical support, but it is no longer the
  main remaining selective reproof target.

### 4. `081`, `082`, and `083` do not need rethinking

The audit found no reason to reopen:

- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_082_exceptional_row_reduction.md`
- `theorem/d5_083_final_theorem_proof.md`

Once the `062 + 079` pairing is cited correctly, the end of the chain is
internally coherent.

Update after `096`:

- the exact regular-closure statement needed by the cleaned `092` suite is now
  reproved directly in
  `theorem/d5_096_compact_reproof_081_regular_closure.md`;
- `081` remains the historical promoted support note, but it is no longer a
  live selective reproof target.

Update after `097/098`:

- the tail-length role of `077` is now compactly reproved in
  `theorem/d5_097_compact_reproof_077_tail_length_reduction.md`;
- the separate `062` structural role is now compacted in
  `theorem/d5_098_compact_cleanup_033_062_structural_block.md`;
- so the main remaining manuscript cleanup target is the compact bridge theorem
  around `076`.

## Practical conclusion

The current D5 odd-`m` theorem package is stable enough to stop calling the
result “open”.

What still deserves work before broader generalization is not theorem search,
but theorem cleanup:

1. keep the new stable `033` trigger note in the citation chain;
2. keep the scope of `076` explicit and use `095`--`098` for the compact
   chart / regular / tail-length / structural steps where appropriate;
3. optionally rewrite the final D5 proof in one shorter manuscript-order note.

## Recommendation on next step

Proceed to a **short cleanup pass**, not a new search:

- tighten theorem citations,
- keep the dependency flow visible,
- then move to generalization questions.

Broad generalization is now reasonable, but only after that cleanup.
