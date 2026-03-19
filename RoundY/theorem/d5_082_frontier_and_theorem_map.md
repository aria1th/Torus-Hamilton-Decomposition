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

Main proof references:

- `theorem/d5_086_dependency_audit_and_generalization_gate.md`

### 3.4 Downstream graph-theoretic frontier after `111–122`

Separate from the accepted odd-`m` globalization package, the downstream
graph-theoretic frontier is now sharper than the old “finish M4 / M5” wording.

- `111` fills the raw M4-style tables on the actual `mixed_008` full torus and
  shows the blocker is not extraction.
- `112` proves that exact compression of the current raw selector row cannot
  close M4 while preserving that row as output.
- `113` rewrites M4 into:
  - a solved symbolic selector-existence half (`M4a`);
  - and a still-open D5 compatibility half (`M4b`).
- `114` then identifies `M4b` with a weighted pair of 1-factorizations on the
  defect slice graphs `G_2` and `G_3`, equivalently on `Sigma=2,3`.
- `115` executes the shrunk compute request:
  it reproduces the pattern-only selector packet, confirms transfer of the
  `m = 9` pattern assignment to `m = 11,13`, and shows that the first natural
  slice-4 intermediate families `(B_k for k in subset, Z, M)` with
  `subset ⊆ {0,1,2,3,4,5}` and the cyclic orbit quotient of
  `(fullpairs, Z, M)` are still no-go.
- `116` then proposes the explicit symbolic slice-4 transport field
  `F4sharp = (B2,B3,B4,Z,O,M)` and backs it with exact checks and ablations.
- `117` proposes a direct corrected-selector theorem for odd `m >= 5`.
- `118` gives the downstream interpretation:
  if `117` is accepted, then M4 and M6 are no longer the live graph-level
  burden, and M5 becomes the next package for the corrected maps.
- `119` then shows that the easiest low-complexity first-return factors for
  `Sel*` are still only `m^4`, so the live color-4 route should move from a
  generic `m^3` factor search to the final section return.
- `120` makes that sharp by reducing color-4 M5 to the final section
  `U_m = (F_4^*)^(m^3)|P2` and extracting an explicit corrected-row model.
- `121` proves that corrected-row model is one `m^2`-cycle for every odd
  `m >= 11`.
- `122` proves the actual/model identification and closes the live color-4
  Sel* M5 route for all odd moduli.

So the current downstream todo is:

- review and stabilize the corrected-selector theorem package `116/117`;
- decide whether to adopt the `118` reading that M4 and M6 are already closed
  in the needed sense;
- then integrate the promoted `119–122` color-4 M5 route with any adopted
  corrected-selector package and the remaining graph-level proof.

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
