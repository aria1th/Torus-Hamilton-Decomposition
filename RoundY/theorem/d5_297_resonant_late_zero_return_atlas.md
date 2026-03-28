# D5 297 Resonant Late Zero-Return Atlas

This note records the first stable late-range exact atlas for the resonant pure
color-`1` branch after the `2026-03-26` schematic notes.

It is not a new theorem claim.  Its purpose is narrower:

- validate the corrected late family encoding against the schematic calibration
  points;
- extend the exact zero-state `B_m/H_m` first-return data to the next late
  resonant moduli;
- and use that atlas to decide which family should be promoted to the next
  full `B_m` decomposition.

The checked outputs are saved in:

- [d5_297_resonant_late_campaign_summary.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_297_resonant_late_campaign_summary.json)
- [zero_calibration.json](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/checks/d5_297_resonant_late_campaign/zero_calibration.json)
- [torus_nd_d5_resonant_late_campaign_297.py](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/scripts/torus_nd_d5_resonant_late_campaign_297.py)

## 1. Correct family encoding

The important correction is that the late families are encoded by **toggle**
semantics, not by naive set union.

Over the promoted `+` control
\[
\widehat{\mathfrak N}_m^{(+)},
\]
the late families
\[
\mathcal C_m=\widehat{\mathfrak N}_m^{(+)}\cup\{A_{r-2,3},A_{r,3}\},
\qquad
\mathcal F_m=\widehat{\mathfrak N}_m^{(+)}\cup\{A_{r-1,3},A_{r,3}\}
\]
must be read as surgery packets in which the added `A_{r,3}` toggles off the
built-in `A_{r,3}` from the control.

With that correction, the new runner reproduces the schematic calibration
values at `m = 177,183,189` exactly:

- `177`, central: `0 -> 45` on `B_m` after `2,224,421` section blocks;
- `177`, flank: `0 -> 35` on `B_m` after `1,127,720` section blocks;
- `183`, central: `0 -> 138` after `3,683,909`;
- `183`, flank: `0 -> 146` after `4,922,828`;
- `189`, central: `0 -> 140` after `4,072,222`;
- `189`, flank: `0 -> 113` after `4,072,175`.

So the current code path is now aligned with the checked late schematic notes.

## 2. Exact zero-state atlas on the late resonant range

The checked modulus set is
\[
171,177,183,189,201,207,213.
\]

For each modulus and each family among

- promoted `+` control,
- late central pair,
- late symmetric flank pair,

the script computes the exact first induced return of the zero state on

- `B_m = {c = 0, d = 0, e = 0}`, and
- `H_m = {c = 0, d = 0}`.

The resulting `B_m` zero-state depths are:

| `m` | promoted `+` | central pair | flank pair | cheapest family |
|---:|---:|---:|---:|---|
| `171` | `6,023,526` | `4,006,094` | `2,017,475` | flank |
| `177` | `14,473,936` | `2,224,421` | `1,127,720` | flank |
| `183` | `4,922,782` | `3,683,909` | `4,922,828` | central |
| `189` | `4,072,222` | `4,072,222` | `4,072,175` | near tie, slight flank edge |
| `201` | `9,776,901` | `6,504,752` | `3,272,300` | flank |
| `207` | `23,138,491` | `3,556,643` | `1,799,513` | flank |
| `213` | `7,758,088` | `5,807,264` | `7,758,035` | central |

The `H_m` first return remains cheap throughout this range, with block counts
close to `m^2`.  More importantly, the `H_m` image pattern itself is highly
structured:

- for every checked modulus, the central pair has the **same** zero-state
  `H_m` image as the promoted `+` control;
- for every checked modulus, the flank pair lands at `a = 1` on the first
  `H_m` return.

So the late branch is now visibly split at the zero-return level:

- `B_m` is the expensive and family-sensitive object;
- `H_m` is cheap and largely controlled by a small arithmetic pattern.

## 3. What this atlas means

This atlas does **not** prove winner status on `B_m`.
It is a routing and promotion tool, not a substitute for the full induced base
permutation.

In particular, `177` is the clean example of why the atlas must be read
carefully:

- the flank family has the cheaper zero-state `B_m` first return;
- but the earlier exact note still says the central family is less broken at the
  level of the zero-orbit cycle length on `B_m` (`108` versus `38`).

So the right operational reading is:

1. zero-state `B_m` first-return depth is a **cheap exact discriminator**;
2. it is not itself the final defect score;
3. the next full `B_m` promotion should still be chosen with branch context in
   mind.

## 4. Updated late-family picture

The late resonant branch is no longer well modeled by one universal 2-line law.

The zero-state atlas now supports the following more precise picture:

- a flank-favored subrange at `171,177,201,207`;
- a central-favored subrange at `183,213`;
- and an almost degenerate crossover point at `189`.

That is exactly the kind of residue-sensitive behavior suggested earlier by the
row-`3` visible-grid notes, now seen again in the later 2-line phase.

So the best current reading is:

> the late resonant pure color-`1` program should be treated as a
> residue-sensitive two-family atlas, not as a search for one universal late
> seed.

## 5. Compute consequence

Because `B_m` is the real cost object and the zero-state atlas is now exact, the
next full exact promotions should be selective.

The most natural next `B_m` decompositions are:

1. `171`, flank and central, to anchor the coexistence modulus with full cycle
   data;
2. `177`, central and flank, to anchor the first shared-defect modulus with
   full cycle data;
3. then `183` and `213`, where the zero-state atlas favors the central family;
4. and `201` / `207`, where it strongly favors the flank family.

That is the main value of this note.
It converts the late resonant branch from a broad compute request into a
sharper promotion order.
