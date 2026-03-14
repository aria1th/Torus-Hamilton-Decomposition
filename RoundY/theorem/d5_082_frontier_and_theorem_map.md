# D5 082 Frontier And Theorem Map

This note is the canonical D5 theorem-map summary.

It has two jobs:

1. record the current accepted theorem package in one place;
2. record how the old exceptional-row bottleneck was discharged inside the
   accepted package, and what still deserves audit.

## 1. Current status in one sentence

For odd `m` in `d=5`, the global safe bridge `(beta,rho)` is accepted, the
concrete bridge `(beta,delta)` is accepted componentwise, the regular raw
gluing problem is closed, and the old exceptional-row bottleneck is now
closed within the accepted `076–082` package by
`theorem/d5_083_final_theorem_proof.md`.

## 2. Accepted theorem layers

### 2.1 Structural theorem package

Accepted theorem-level content:

- the active branch is governed by the phase-corner machine;
- the universal first-exit targets are derived from the explicit `H_{L1}`
  trigger law;
- the structural spine closes through the `033 -> 062 -> 059` route.

Main proof references:

- `theorem/d5_first_exit_target_proof_062.md`
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

### 2.5 Regular-union theorem

Accepted raw theorem on the regular sector:

every regular realization of every realized `delta` continues.

So the regular union contributes no mixed-status or tail-length ambiguity.

Main proof references:

- `theorem/d5_081_regular_union_and_gluing_support.md`
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

- whether the imported accepted inputs, especially the `033 -> 062` structural
  route and the `079` chart/interface theorem, are packaged tightly enough for
  a final manuscript-order proof chain.

Main proof references:

- `theorem/d5_086_dependency_audit_and_generalization_gate.md`

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

- `033 -> 062`,
- the componentwise concrete bridge package,
- the `079` interface theorem.

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
