# D5 093: Reproof Targets After The Cleaned 092 Suite

This note answers one narrow question:

> after `092`, which theorems still remain in accepted-support form, and which
> of them really need re-proving or further inlining before we call the odd-`m`
> D5 package independently proved?

The answer is short:

- `092` largely closes the manuscript-order packaging gap;
- the remaining issue is not a new D5 bottleneck;
- the only serious remaining "reproof" target is the support theorem still
  imported in accepted form.

## 1. What `092` already fixes

Compared with the older gap note, `092` now makes explicit in one place:

1. the definition block for full chains, actual lifts, tail length, and
   endpoint class;
2. the structural first-exit theorem;
3. the chart-to-raw exceptional landing theorem;
4. the single-row globalization criterion;
5. the final globalization proof.

So the older missing items

- one structural theorem block,
- one explicit chart-to-raw composition theorem,
- one definition block,
- one continuous final proof

are no longer the main gap.

## 2. Theorems still used in accepted-support form

`092` originally stated the remaining imported support clearly. After the
`095`--`098` cleanup pass, the live imported support list for the cleaned suite
is shorter still.

These are now:

1. **componentwise concrete bridge package** from `076`.

Update after `095`--`098`:

- the `079` chart/interface role is now compactly reproved in
  [d5_095_compact_reproof_079_chart_interface_landing.md](./d5_095_compact_reproof_079_chart_interface_landing.md);
- the `081` regular-continuation role is now compactly reproved in
  [d5_096_compact_reproof_081_regular_closure.md](./d5_096_compact_reproof_081_regular_closure.md);
- the `077` tail-length role is now compactly reproved in
  [d5_097_compact_reproof_077_tail_length_reduction.md](./d5_097_compact_reproof_077_tail_length_reduction.md);
- the old `033/062` structural block is now compactly cleaned in
  [d5_098_compact_cleanup_033_062_structural_block.md](./d5_098_compact_cleanup_033_062_structural_block.md);
- the downstream globalization flow is now also assembled in one read-through
  note at
  [d5_099_one_pass_odd_m_globalization_package.md](./d5_099_one_pass_odd_m_globalization_package.md);
- so the live selective reproof set is now best read as the compact bridge
  theorem around `076`, with only optional first-principles `033` provenance
  beyond that.

## 3. Which of these most deserve re-proving or inlining

Most of the earlier targets are now resolved; one live item remains.

### 3.1 Highest priority: `076`

Why:

- `076` still carries the componentwise concrete bridge package:
  intrinsic coordinates, splice law, current-event readout, and component image.
- This is the most structural imported support still outside `092`.

What would count as a true reproof/inlining:

- one compact theorem note proving the intrinsic boundary digits,
- one compact proof of `delta' = delta + 1`,
- one compact proof of current-event readout from `(beta,delta)`,
- one compact statement of the component image.

This is the single most valuable target if the goal is a more self-contained
final odd-`m` package.

### 3.2 Reproved in compact form: `079`

Why:

- `079` is the chart/interface theorem used in the only place where chart-level
  language still touches the raw global proof.
- The `087` audit already identified this as the main citation-discipline
  point.

What now counts as the adopted compact reproof:

- [d5_095_compact_reproof_079_chart_interface_landing.md](./d5_095_compact_reproof_079_chart_interface_landing.md)
  proves the exact chain-label statement needed by `092` directly from the
  frozen regular-slice chart formulas.

So `079` is no longer a main remaining reproof target.

### 3.3 Reproved in compact form: `081`

Why:

- `081` was already conceptually clean and theorem-level;
- it closes the regular sector and never looked like the fragile point in the
  package.

What now counts as the adopted compact reproof:

- [d5_096_compact_reproof_081_regular_closure.md](./d5_096_compact_reproof_081_regular_closure.md)
  proves the exact regular-closure statement used by `092` directly from the
  frozen regular-window formulas and the promoted endpoint witness table.

So `081` is no longer a main remaining reproof target.

### 3.4 Reproved in compact form: `077`

Why:

- `077` was already a conceptual reduction theorem:
  fixed-`delta` ambiguity reduces to tail length;
- once totality is proved, its use inside `092` is very clean.

What now counts as the adopted compact reproof:

- [d5_097_compact_reproof_077_tail_length_reduction.md](./d5_097_compact_reproof_077_tail_length_reduction.md)
  proves directly that, at fixed realized `delta`, the padded future word and
  endpoint class are determined exactly by tail length.

So `077` is no longer a main remaining reproof target.

## 4. Structural cleanup after 098

The old localized `062` issue inside Section 3 of `092` was the pre-exit
patch-avoidance clause.

Update after `098`:

- [d5_098_compact_cleanup_033_062_structural_block.md](./d5_098_compact_cleanup_033_062_structural_block.md)
  now writes that structural block out explicitly in compact theorem form;
- so the remaining external issue there is only the broader defect-template
  provenance behind the trigger-family lemma, not a missing structural theorem
  for the odd-`m` globalization package itself.

This is not a new theorem search target. It is now best treated as a solved
cleanup item unless one insists on a full first-principles rebuild of the old
`033` classification layer.

## 5. Recommended reproof order

If the goal is a genuinely tighter independent package, the best order is now:

1. compact reproof / inline version of `076`;
2. if desired, keep `098` as the compact structural block and state its honest
   dependency boundary on the old `033` artifact line;
3. if useful, rewrite the bridge theorem and final theorem into one even
   shorter manuscript package around `092`.

This order matches both `087` and the structure of `092`.

## 6. What does not need rethinking

The following no longer look like dangerous accepted-without-proof steps:

- the `033 -> 062` trigger/first-exit chain at theorem level,
- the `083` final globalization proof pattern,
- the final odd-`m` theorem claim itself.

So the remaining task is not new mathematics. It is selective inlining of the
few support theorems still imported by `092`.

## 7. Bottom line

After `095`--`098`, the cleaned odd-`m` D5 package is close to independent.

The main remaining reproof targets are now:

1. `076` concrete componentwise bridge;
2. optional first-principles provenance for the old `033` trigger-family
   classification beyond what `098` already isolates.

`079`, `081`, `077`, and the separate `062` structural role have effectively
moved off this list because `095`--`098` now supply the compact cleaned-package
statements used by `092`.
