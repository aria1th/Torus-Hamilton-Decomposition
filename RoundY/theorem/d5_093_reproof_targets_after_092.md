# D5 093: Reproof Targets After The Cleaned 092 Suite

This note answers one narrow question:

> after `092`, which theorems still remain in accepted-support form, and which
> of them really need re-proving or further inlining before we call the odd-`m`
> D5 package independently proved?

The answer is short:

- `092` largely closes the manuscript-order packaging gap;
- the remaining issue is not a new D5 bottleneck;
- the only serious "reproof" targets are the support theorems still imported
  as accepted theorem packages.

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

`092` itself states the remaining imported support clearly.

These are:

1. **componentwise concrete bridge package** from `076`;
2. **fixed-`delta` tail-length reduction** from `077`;
3. **chart/interface theorem** from `079`;
4. **regular continuation theorem** from `081`.

Those are the only theorems that still sit outside the fully inlined `092`
suite.

Update after `095`:

- the `079` chart/interface role is now compactly reproved in
  [d5_095_compact_reproof_079_chart_interface_landing.md](./d5_095_compact_reproof_079_chart_interface_landing.md);
- so the live selective reproof set is now best read as `076`, `077`, `081`,
  and the upstream `033/062` structural compression, rather than `079`.

## 3. Which of these most deserve re-proving or inlining

Not all four are equally urgent.

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

### 3.3 Active reproof track: `081`

Why:

- `081` is now conceptually clean and theorem-level;
- it closes the regular sector and does not seem like a mathematical risk.

What would count as reproof:

- a shorter proposition proving regular continuation in the exact language of
  `092`.

This is useful for manuscript cleanliness, but it is not the place where the
package still feels fragile.

### 3.4 Active reproof track: `077`

Why:

- `077` is already a conceptual reduction theorem:
  fixed-`delta` ambiguity reduces to tail length.
- Once totality is proved, the use of `077` inside `092` is very clean.

What would count as reproof:

- a shorter proposition on endpoint ambiguity at fixed `delta`, stated directly
  in the final definitions of `092`.

This would improve compactness, but it is the least urgent of the four.

## 4. One subtle additional item inside Section 3 of `092`

Although `092` writes Theorem 3.1 as a continuous proof, it still explicitly
uses one accepted `062` ingredient in proof form:

- pre-exit patch avoidance.

So if one wants to be very strict, the remaining upstream inlining target is:

5. **the pre-exit patch-avoidance clause inside the structural first-exit
   theorem**.

This is not a new theorem search target. It is a compression target:

- isolate the patch-avoidance lemma cleanly inside the structural block, or
- keep citing `062` explicitly as the proof source for that clause.

## 5. Recommended reproof order

If the goal is a genuinely tighter independent package, the best order is now:

1. compact reproof / inline version of `076`;
2. isolate or inline the `062` pre-exit patch-avoidance clause in Theorem 3.1;
3. compress `081`;
4. compress `077`;
5. if useful, rewrite Theorem 3.1 so the `033 -> 062` structural block is more
   self-contained.

This order matches both `087` and the structure of `092`.

## 6. What does not need rethinking

The following no longer look like dangerous accepted-without-proof steps:

- the `033 -> 062` trigger/first-exit chain at theorem level,
- the `083` final globalization proof pattern,
- the final odd-`m` theorem claim itself.

So the remaining task is not new mathematics. It is selective inlining of the
few support theorems still imported by `092`.

## 7. Bottom line

After `092`, the cleaned odd-`m` D5 package is close to independent.

The main remaining reproof targets are now:

1. `076` concrete componentwise bridge;
2. the `062` pre-exit patch-avoidance clause used inside Theorem 3.1;
3. the in-progress `081` and `077` compressions;
4. the upstream `033/062` structural cleanup where needed.

`079` has effectively moved off this list because `095` now supplies the
compact chart/interface reproof needed by the cleaned suite.
