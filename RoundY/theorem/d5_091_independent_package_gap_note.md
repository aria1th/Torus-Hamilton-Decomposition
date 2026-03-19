# From the Accepted Package to an Independent Odd-`m` D5 Theorem Package

## Abstract

This note answers one packaging question and does not search for a new theorem.
The odd-`m` `d=5` globalization theorem is already closed inside the accepted
chain

`033 -> 062 -> 076 -> 077 -> 079 -> 081 -> 082 -> 083`.

No new mathematical bottleneck is visible in that chain. What remains is to
rewrite the imported inputs so that the final theorem no longer reads as proved
only “within the accepted package.” The main missing item is now one compact
concrete bridge theorem that replaces the still-imported `076` package in
manuscript order.

Update:

- the first cleaned manuscript-order answer to this gap note is now
  `theorem/d5_092_cleaned_independent_theorem_suite.md`;
- the old standalone `079` chart/interface theorem is now compactly reproved by
  `theorem/d5_095_compact_reproof_079_chart_interface_landing.md`;
- the old standalone `081` regular-closure role is now compactly reproved by
  `theorem/d5_096_compact_reproof_081_regular_closure.md`;
- the old standalone `077` tail-length role is now compactly reproved by
  `theorem/d5_097_compact_reproof_077_tail_length_reduction.md`;
- the old separate `062` structural role is now compactly cleaned in
  `theorem/d5_098_compact_cleanup_033_062_structural_block.md`;
- the downstream odd-`m` globalization flow can now also be read in one pass in
  `theorem/d5_099_one_pass_odd_m_globalization_package.md`, with the standing
  theorem-package inputs written explicitly at the top;
- the remaining selective reproof targets after that cleanup are summarized in
  `theorem/d5_093_reproof_targets_after_092.md`, with the compact bridge
  package around `076` as the main live item.

## 1. Purpose and exact current status

This is a cleanup note, not a new theorem note. Its job is to separate two
claims that can otherwise get blurred together:

1. the odd-`m` `d=5` theorem is already closed inside the accepted package;
2. the theorem is not yet written as one independently self-contained
   manuscript-order package.

### Current accepted-package theorem

For odd `m` in the accepted D5 regime, every actual lift of the exceptional
cutoff row `delta = 3m-3` continues through

`3m-2 -> 3m-1`

and lies in the regular continuing endpoint class there. Consequently:

1. there is no mixed-status realized `delta`;
2. fixed realized `delta` determines tail length;
3. fixed realized `delta` determines endpoint class and future word;
4. `rho = rho(delta)` globally;
5. raw global `(beta,delta)` is exact on the true accessible boundary union.

### Scope reminder

The theorem above is exactly the current accepted conclusion, but its proof is
still distributed across imported notes. In particular, `076` remains a
componentwise concrete bridge theorem, and the accepted-chain proof still
passes through `062`, `077`, `079`, `081`, and `083`. In the cleaned package,
the exact `079`, `081`, `077`, and separate `062` roles are now supplied by
the compact notes `095`--`098`, leaving `076` as the main imported theorem
layer.

## 2. What an independent package should mean

An independent odd-`m` D5 theorem package is a manuscript-order theorem
package in which all proof-critical objects used by the final odd-`m` `d=5`
globalization argument are stated in place, with their exact scope visible, so
that the final theorem no longer depends on the phrase “within the accepted
package” for its mathematical status.

This notion of independence is deliberately modest. It does not ask for new
numerics, a new search, or a new idea. It asks for one self-contained
presentation layer in which the proof-critical imports have become theorems of
the package itself.

## 3. What already looks theorem-level enough

The following pieces already look strong enough to survive essentially
unchanged in an independent package:

1. the abstract bridge `(beta,rho)`;
2. the componentwise concrete bridge `(beta,delta)`;
3. the reduction from fixed-`delta` ambiguity to full-chain tail length;
4. the regular-union theorem;
5. the exceptional-row reduction;
6. the final gluing proof pattern.

So the missing work is not discovery. It is exposing the already-used inputs in
one clean order.

## 4. What is still missing

### 4.1 One self-contained structural theorem block

An independent package should contain one theorem block that states, in one
place:

1. the exact trigger family
   `H_{L1} = {(q,w,u,lambda) = (m-1,m-1,u,2) : u != 2}`;
2. the candidate active orbit on current coordinates;
3. the phase-`1` invariant
   `q ≡ u - rho + 1 (mod m)`;
4. the universal first-exit targets
   `T_reg = (m-1,m-2,1)` and `T_exc = (m-2,m-1,1)`;
5. the conclusion that, on the actual active branch, the true orbit agrees with
   the candidate orbit up to first exit.

At present this content is mathematically sound but distributed across `033`
and `062`. Independence asks for one theorem block, not a new proof idea.

Update after `098`:

- this structural block is now written explicitly in
  `theorem/d5_098_compact_cleanup_033_062_structural_block.md`;
- the only remaining issue there is the broader defect-template provenance
  behind the trigger-family lemma, not a missing structural theorem for the
  odd-`m` globalization package.

### 4.2 One explicit chart-to-raw continuation theorem

An independent package should include one theorem that packages the current
composition of `062` and `079` into a single proof object:

- every actual lift of the exceptional cutoff row reaches the universal raw
  first-exit target `T_exc = (m-2,m-1,1)` by direction `1`, and therefore
  continues in chain labels through `3m-3 -> 3m-2 -> 3m-1`, where `3m-2` is
  the terminal regular source-`4` occurrence and `3m-1` is the regular
  source-`1` start.

This is the one place where the current proof still feels assembled from
accepted notes rather than written as a single theorem object. This theorem is
weaker than the final endpoint-class gluing theorem: it packages only the
actual exceptional continuation, not the later tail-length or regular-union
arguments that promote that continuation to global `rho = rho(delta)`.

Update after `095` and `098`:

- the cleaned suite now has this role through the `095` chart/interface reproof
  together with the explicit structural block in `098`;
- so this is no longer the main missing item in the independent-package gap.

### 4.3 One compact concrete bridge theorem

An independent package should contain one compact theorem that states, in one
place, the intrinsic boundary coordinates

- `sigma ≡ w + u - q - 1 (mod m)`,
- `delta = q + m sigma`,

the splice law `delta' = delta + 1 (mod m^2)`, the current-event readout from
`(beta,delta)`, and the component-image statement that each splice-connected
accessible component maps to one forward `+1` orbit segment in `Z/m^2 Z`.

This content already exists in `076`. The missing work is only to present it as
one compact theorem in manuscript order.

### 4.4 One theorem-level definition block

An independent package should define in one place the final proof objects used
later without reconstruction from earlier notes:

1. the accessible boundary union;
2. a splice-connected accessible component;
3. a full regular chain;
4. the exceptional cutoff row;
5. an actual lift;
6. endpoint class, padded future word, and right-congruence state.

These notions are already present in the chain, but they are spread across
notes. An independent package should not force the reader to reconstruct them
from context.

Update after `092`:

- the cleaned theorem suite now effectively contains this definition block;
- so this is no longer a serious remaining gap.

### 4.5 Support files should become verification aids only

The support files

- `checks/d5_077_compact_interval_summary.json`
- `checks/d5_081_regular_union_endpoint_table.csv`

should remain attached as verification aids, but any proof-critical content now
navigated through them should be restated as lemmas or propositions in the
manuscript-order theorem notes.

Again, this is a packaging requirement, not evidence of a missing theorem idea.

## 5. Recommended manuscript order

A compact independent package can be organized in the following order:

1. the cleaned definition block already present in `092`;
2. the compact structural theorem note `098`;
3. one concrete bridge theorem note replacing the current promoted-support
   status of `076`;
4. the compact cleanup notes `097`, `096`, and `095`;
5. the final globalization theorem.

That order makes the final proof read as a forward argument rather than as a
reconstruction from accepted imports.

## 6. Smallest honest checklist

The shortest path from “closed inside the accepted package” to “proved in a
self-contained package” is:

1. keep `098` as the compact structural theorem block;
2. compress `076` into one final concrete bridge theorem note;
3. keep the `095`--`097` cleanup notes as the stable compact support layers;
4. keep the JSON and CSV files as support only, not as implicit proof steps;
5. keep the broader `033` defect-template provenance explicit only where it is
   genuinely needed.

If those five items are done, the phrase

> closed inside the accepted package

should be replaceable by

> proved in a self-contained odd-`m` D5 theorem package.

## 7. Bottom line

The remaining gap is no longer a theorem-search gap. It is a theorem-packaging
gap:

1. one compact concrete bridge theorem statement replacing `076`, and
2. optionally, a first-principles proof of the broader `033` trigger-family
   classification beyond what `098` isolates for the globalization chain.

So the right next work is theorem cleanup, not new theorem search.
