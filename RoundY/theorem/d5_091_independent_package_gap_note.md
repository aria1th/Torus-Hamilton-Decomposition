# From the Accepted Package to an Independent Odd-`m` D5 Theorem Package

## Abstract

This note answers one packaging question and does not search for a new theorem.
The odd-`m` `d=5` globalization theorem is already closed inside the accepted
chain

`033 -> 062 -> 076 -> 077 -> 079 -> 081 -> 082 -> 083`.

No new mathematical bottleneck is visible in that chain. What remains is to
rewrite the imported inputs so that the final theorem no longer reads as proved
only “within the accepted package.” The main missing item is one explicit
chart-to-raw continuation theorem that packages the current use of `062` and
`079` into a single proof object.

Update:

- the first cleaned manuscript-order answer to this gap note is now
  `theorem/d5_092_cleaned_independent_theorem_suite.md`;
- the old standalone `079` chart/interface theorem is now compactly reproved by
  `theorem/d5_095_compact_reproof_079_chart_interface_landing.md`;
- the remaining selective reproof targets after that cleanup are summarized in
  `theorem/d5_093_reproof_targets_after_092.md`.

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
componentwise concrete bridge theorem, `079` remains a chart/interface
theorem, and `083` becomes final only after those inputs are combined with
`062`, `077`, and `081`.

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

1. one definition note collecting the final objects;
2. one structural theorem note replacing the distributed `033 -> 062` block;
3. one concrete bridge theorem note replacing the current promoted-support
   status of `076`;
4. the fixed-`delta` tail-length reduction;
5. the regular-union theorem;
6. the explicit chart-to-raw exceptional continuation theorem;
7. the final globalization theorem.

That order makes the final proof read as a forward argument rather than as a
reconstruction from accepted imports.

## 6. Smallest honest checklist

The shortest path from “closed inside the accepted package” to “proved in a
self-contained package” is:

1. write one self-contained `033 -> 062` structural theorem block;
2. write one explicit theorem packaging raw exceptional first exit with the
   chart/interface continuation;
3. compress `076` into one final concrete bridge theorem note;
4. gather the final definitions in one manuscript-order theorem note;
5. keep the JSON and CSV files as support only, not as implicit proof steps.

If those five items are done, the phrase

> closed inside the accepted package

should be replaceable by

> proved in a self-contained odd-`m` D5 theorem package.

## 7. Bottom line

The remaining gap is no longer a theorem-search gap. It is a theorem-packaging
gap:

1. one distributed structural block,
2. one missing chart-to-raw composition theorem,
3. one compact concrete bridge theorem statement, and
4. one final definitions block.

So the right next work is theorem cleanup, not new theorem search.
