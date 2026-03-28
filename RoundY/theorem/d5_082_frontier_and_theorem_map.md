# D5 082 Frontier And Theorem Map

This note is the canonical D5 theorem-map summary.

It has two jobs:

1. record the current accepted theorem package in one place;
2. record how the old exceptional-row bottleneck was discharged inside the
   accepted package, and what still deserves audit.

For a one-pass readable globalization package that states the standing inputs
and carries the downstream odd-`m` proofs in one place, see
`theorem/d5_099_one_pass_odd_m_globalization_package.md`.

For the current quotient-identification note that explains how the theorem-side
exact quotient compares to the dynamic bridge `(beta,q0,sigma)` /
`(beta,delta)`, see
`theorem/d5_106_intended_quotient_identification_and_comparison.md`.

For the current promoted manuscript-order proof slice after the `251` bundle,
see:

- `theorem/d5_249_master_status_after_G1.md`
- `theorem/d5_251_bundle_review_and_polish_note.md`
- `tex/d5_251_full_d5_working_manuscript_refined.tex`

For the current `0326` working frontier promotion after the later residual
search split, see:

- `theorem/d5_284_current_working_frontier_after_nonresonant_closure.md`
- `theorem/d5_285_residual_assembly_companion_memo.md`
- `tex/d5_284_full_d5_working_manuscript_after_nonresonant_closure.tex`
- `tex/d5_285_residual_assembly_companion_after_nonresonant_closure.tex`
- `theorem/d5_286_promoted_collar_complete_local_dynamics.md`

## 1. Current status in one sentence

For odd `m` in `d=5`, the global safe bridge `(beta,rho)` is accepted, the
concrete bridge `(beta,delta)` is accepted componentwise, the regular raw
gluing problem is closed, and the old exceptional-row bottleneck is now
closed within the accepted `076–082` package by
`theorem/d5_083_final_theorem_proof.md`.

For downstream M3 bookkeeping, the current sharpened message is:
the theorem-side intended quotient should still be stated as the exact
deterministic quotient retaining grouped base, while the concrete dynamic
bridge is the checked factor object. The current checked comparison is
`(B,beta) ~= (rho,beta,q0,sigma) -> (beta,q0,sigma)`.

## 2. Accepted theorem layers

### 2.1 Structural theorem package

Accepted theorem-level content:

- the active branch is governed by the phase-corner machine;
- the universal first-exit targets are derived from the explicit `H_{L1}`
  trigger law;
- the structural spine closes through the `033 -> 062 -> 059` route.

Main proof references:

- `theorem/d5_first_exit_target_proof_062.md`
- `theorem/d5_098_compact_cleanup_033_062_structural_block.md`
- `theorem/d5_076_bridge_main.md`
- `theorem/d5_076_concrete_bridge_proof.md`

### 2.2 Safe global bridge theorem

Accepted global theorem object:

`(beta,rho)`.

Meaning:

- `rho` is the boundary right-congruence class of the padded future
  current-event word;
- this is still the correct globally unconditional theorem object.

Main proof references:

- `theorem/d5_076_bridge_main.md`
- `theorem/d5_076_realization_trackB.md`
- `theorem/d5_079_exceptional_interface_support.md`

### 2.3 Concrete componentwise bridge theorem

Accepted componentwise concrete bridge:

`(beta,delta)`,

equivalently `(beta,q,sigma)` with `delta = q + m sigma`.

Accepted componentwise package:

- uniform splice law,
- uniform current-event readout,
- component boundary image is a forward `+1` orbit segment in `Z/m^2 Z`.

Main proof references:

- `theorem/d5_076_concrete_bridge_proof.md`
- `theorem/d5_077_tail_length_and_actual_union.md`
- `theorem/d5_097_compact_reproof_077_tail_length_reduction.md`
- `theorem/d5_079_exceptional_interface_support.md`

### 2.4 Chart-level exceptional continuation

Accepted chart / chain-label conclusion:

`3 -> (terminal chain of 4) -> 1`.

Equivalent interface form:

`3m-3 -> 3m-2 -> 3m-1`,

where:

- `3m-2` is the regular source-`4` terminal representative;
- `3m-1` is the regular source-`1` start representative.

Main proof references:

- `theorem/d5_079_exceptional_interface_support.md`
- `theorem/d5_095_compact_reproof_079_chart_interface_landing.md`

### 2.5 Regular-union theorem

Accepted raw theorem on the regular sector:

every regular realization of every realized `delta` continues.

So the regular union contributes no mixed-status or tail-length ambiguity.

Main proof references:

- `theorem/d5_081_regular_union_and_gluing_support.md`
- `theorem/d5_096_compact_reproof_081_regular_closure.md`
- `checks/d5_081_regular_union_endpoint_table.csv`

### 2.6 Exceptional-interface reduction

Accepted reduction:

the remaining exceptional issue is equivalent to ruling out a hidden second
endpoint sheet over the regular source-`1` start label

`delta = 3m-1`.

Main proof references:

- `theorem/d5_081_regular_union_and_gluing_support.md`

### 2.7 Finite proof object

Accepted proof-object correction:

the right finite object is an **end-gluing table on actual lifts**, not merely
on the reconstructed quotient.

Main proof references:

- `theorem/d5_081_regular_union_and_gluing_support.md`

## 3. What is already proved vs. what still needs audit

### 3.1 Proved / accepted

The following should be treated as proved within the current accepted package:

- structural phase-corner package through universal first exits;
- global abstract bridge `(beta,rho)`;
- componentwise concrete bridge `(beta,delta)`;
- chart-level exceptional landing `3m-3 -> 3m-2 -> 3m-1`;
- regular raw continuation theorem;
- reduction of the full raw theorem to the exceptional interface row.

### 3.2 Final in-package globalization theorem

Within the accepted `076–082` theorem package:

- every actual lift of the exceptional cutoff `3m-3` continues through
  `3m-2 -> 3m-1` and lands in the regular continuing class there;
- no mixed-status `delta` exists on the true accessible union;
- fixed realized `delta` determines tail length / endpoint class;
- `rho = rho(delta)` globally;
- raw global `(beta,delta)` is exact.

Main proof references:

- `theorem/d5_083_final_theorem_proof.md`

### 3.3 What still deserves audit

What remains is no longer a D5 bottleneck but an audit question:

- whether the remaining imported bridge layer around `076`, the retained
  trigger-family / regular-support provenance behind the compact `098` and
  `099` package inputs, and the final graph-level translation from globalization
  to Hamilton decomposition are packaged tightly enough for a final
  manuscript-order proof chain.
- in the promoted `251` manuscript-order slice, how much of the imported
  post-entry odometer packet and the imported final graph-side/globalization
  packet should be internalized directly into the main manuscript.

Main proof references:

- `theorem/d5_086_dependency_audit_and_generalization_gate.md`

### 3.4 Downstream manuscript package after `219–251`

Separate from the accepted odd-`m` globalization package, the downstream
graph/manuscript line has now advanced beyond the earlier `111–122` frontier
discussion.

- the promoted `219–233` front-end packet closes the present theorem block
  `T0--T4`;
- the promoted `236/245/247` graph-side packet closes `G1` by an explicit
  two-defect-set splice of the valid baseline package;
- the promoted `234` transport note closes `G2` from `G1` by cyclic conjugacy;
- the short status note `249` records that no live theorem object remains
  inside the present `T0--T4, G1, G2` slice;
- the refined manuscript package `251` then presents that closed slice
  honestly, while leaving two blocks imported rather than reproved:
  the post-entry odometer packet and the final graph-side/globalization packet.

So the current downstream todo is no longer “finish M4 / M5” inside this slice.
It is:

- keep the promoted `T0--T4, G1, G2` slice fixed;
- decide how much of the imported post-entry odometer packet to internalize
  into the refined manuscript;
- decide how much of the imported final graph-side/globalization packet to
  internalize into the refined manuscript;
- keep the newly promoted scripts/checks/overview synchronized with that
  manuscript-order presentation.

Later residual notes then sharpen the downstream read again:

- `256–266` close the actual color-`3` Route-E branch;
- `269–281` narrow the remaining residual assembly problem by successive
  obstruction notes and repaired-family refinements;
- `284–286` then promote the current working memo that treats small odd packets
  and the nonresonant packet as closed working blocks and records the live
  downstream burden as a resonant residual program.

This does not change the accepted `076–083` theorem package itself.
It changes only the best current downstream organizational read.

## 4. Final theorem now in force

The final theorem now in force inside the accepted package is:

> every actual lift of the exceptional cutoff row `3m-3` lands in the regular
> continuing class through the interface `3m-2 -> 3m-1`.

Equivalent corollaries:

- no hidden second endpoint sheet over `delta = 3m-1`;
- no mixed-status `delta` on the true accessible union;
- `rho = rho(delta)` globally;
- raw global `(beta,delta)` is exact.

## 5. Best current next split

The current split should now be:

### 5.1 Keep the safe theorem language explicit

The abstract bridge `(beta,rho)` is still the safest global theorem object for
presentation, even though raw global `(beta,delta)` is now derived inside the
accepted package.

### 5.2 Audit imported structural inputs

Recheck and, if useful, repackage:

- the componentwise concrete bridge package,
- and, only if desired for full first-principles provenance, the trigger-family
  source behind `098`.

### 5.3 Defer broad generalization until after audit

The next serious task is dependency stabilization, not reopening D5 search.

## 6. What should not be reopened

Do not reopen:

- broad witness search;
- local event-readout discovery;
- regular-union ambiguity;
- chart-level exceptional landing discovery;
- composite-dimension side work;
- even-`m` speculation.

Those are no longer the bottleneck.

## 7. Bottom line

Post-`083`, the D5 odd-`m` frontier is no longer the exceptional row itself.

Inside the accepted package, that row is closed and raw global `(beta,delta)`
follows.

The next job is to tighten the imported dependency chain before using the D5
result as the base for broader generalization.
