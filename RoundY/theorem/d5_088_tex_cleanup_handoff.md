# D5 088 TeX Cleanup Handoff

This note is the cleanup-facing handoff for turning the current D5 odd-`m`
proof chain into a clean `.tex` manuscript section.

It is not a new theorem note. It says:

1. what theorem we now claim,
2. what files are actually needed to typeset that claim cleanly,
3. what theorem/support boundary should be preserved during cleanup.

## 1. Exact theorem claim to typeset

The current theorem claim is:

> For odd `m` in the accepted D5 regime, raw global `(beta,delta)` is exact on
> the true accessible boundary union.

Equivalent final form:

> every actual lift of the exceptional cutoff row `delta = 3m-3` continues
> through `3m-2 -> 3m-1` and lies in the regular continuing endpoint class
> there; hence `rho = rho(delta)` globally.

This is now proved **inside the accepted `076–082` package** by:

- `theorem/d5_083_final_theorem_proof.md`

## 2. Minimal theorem chain to keep in the TeX cleanup

The shortest clean chain is:

1. `theorem/d5_033_explicit_trigger_family.md`
2. `theorem/d5_first_exit_target_proof_062.md`
3. `theorem/d5_076_concrete_bridge_proof.md`
4. `theorem/d5_077_tail_length_and_actual_union.md`
5. `theorem/d5_079_exceptional_interface_support.md`
6. `theorem/d5_081_regular_union_and_gluing_support.md`
7. `theorem/d5_082_exceptional_row_reduction.md`
8. `theorem/d5_083_final_theorem_proof.md`

These are the only notes that need to survive in theorem form for a compact
manuscript proof of the D5 odd-`m` result.

## 3. Recommended theorem order in TeX

Use this order:

### Structural input

- explicit trigger family for `H_L1`
- universal first-exit targets

### Concrete bridge package

- intrinsic boundary digit `delta`
- componentwise splice law `delta -> delta + 1`
- componentwise current-event readout

### Globalization reduction

- fixed-`delta` ambiguity reduces to tail length
- regular raw continuation theorem
- exceptional interface theorem
- exceptional-row reduction

### Final theorem

- exceptional cutoff continues through `3m-2 -> 3m-1`
- every accessible component is total
- tail length is determined by `delta`
- `rho = rho(delta)` globally
- raw global `(beta,delta)` exact

## 4. What should stay explicit during cleanup

These distinctions should not be blurred in the `.tex` rewrite:

- `076` is **componentwise** concrete, not yet global by itself
- `079` is a **chart/interface** theorem, not a standalone raw continuation
  theorem
- `083` is final only because it uses `062 + 079 + 081 + 077` together

So the TeX cleanup should preserve the words:

- “componentwise” for `076`
- “chart/interface” for `079`
- “within the accepted package” only if the upstream notes are not fully
  inlined into the TeX section

## 5. Best cleanup target

Adopt:

- `RoundY/tex/d5_odd_m_globalization_note_20260314.tex`

as the primary manuscript base.

Use:

- `RoundY/theorem/d5_088_tex_cleanup_outline.tex`

only as a checklist for section order and theorem dependencies.

Use:

- `tex/d3torus_complete_m_ge_3_odometer_revision_v9_with_d4_patched.tex`

as the preamble / theorem-style reference when the D5 section is folded into a
larger manuscript.

Do not use as the main base:

- `RoundY/tex/d5_odd_m_boundary_globalization_note.tex`
  because it mixes a standalone note with a supplement-style section and is too
  large for the present cleanup task;
- `RoundY/tex/d5_odd_m_globalization_note.tex`
  because it is cleaner than the boundary note but weaker than the
  `20260314` draft on scope discipline and provenance.

The cleanest target structure remains one theorem section with:

1. two imported propositions:
   trigger family and first-exit targets
2. one bridge proposition:
   componentwise `(beta,delta)` package
3. one regular continuation proposition
4. one exceptional interface proposition
5. one final globalization theorem

That is enough. Do not carry the whole historical `055–082` story into the
cleanup file.

## 6. Supporting files worth bundling

The two small check files still worth carrying are:

- `checks/d5_077_compact_interval_summary.json`
- `checks/d5_081_regular_union_endpoint_table.csv`

They are not part of the final theorem statement, but they are the shortest
verifiable evidence files behind the bridge/interface/regular-continuation
story.
