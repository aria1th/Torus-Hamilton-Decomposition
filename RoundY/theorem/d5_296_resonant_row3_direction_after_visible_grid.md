# D5 296 Resonant Row-3 Direction After Visible-Grid Notes

This note synthesizes the current stable resonant pure color-`1` packet with
the `2026-03-25/26` `tmp/resonant_row3_*` research notes.

It is not a theorem claim.
Its job is to say which next direction now looks most realistic.

The key stable references are:

- [d5_289_promoted_collar_base_section_reduction_and_no_go.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_289_promoted_collar_base_section_reduction_and_no_go.md)
- [d5_291_residual_compute_campaign_conclusion.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_291_residual_compute_campaign_conclusion.md)
- [d5_294_residual_package_alignment_after_tar.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_294_residual_package_alignment_after_tar.md)
- [d5_295_promoted_collar_dualA_vs_singleB_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md)

The `tmp` notes most relevant here are:

- [resonant_row3_rho_splicer_note_2026-03-25 (1).md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/resonant_row3_rho_splicer_note_2026-03-25%20(1).md)
- [resonant_row3_splicer_57_anomaly_and_twoA_probe_2026-03-25.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/resonant_row3_splicer_57_anomaly_and_twoA_probe_2026-03-25.md)
- [resonant_row3_visible_grid_and_B_spectator_note_2026-03-26.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/tmp/resonant_row3_visible_grid_and_B_spectator_note_2026-03-26.md)

## 1. What the new row-3 notes add

The row-3 notes sharpen the pure color-`1` branch in three ways.

### A. A genuine nonuniform seed exists

The row-3 `rho` splicer is not a fluke:

- it closes the checked `H_m/B_m` reductions at `39,51,63,69`;
- but it fails at `57`.

So the row-3 mechanism is structurally real, but it is not a universal all-odd
seed in its current form.

### B. `B` is not a pure color-1 repair channel

The `2026-03-26` note makes the color-`1` role of `B` much sharper than the
older quotient-language heuristic.

For the exact color-`1` `Sigma=0` dynamics, `B=(02)` is an **exact spectator**:
it does not move the chosen color-`1` update coordinate at any step.

This is fully compatible with the stable note
[d5_295_promoted_collar_dualA_vs_singleB_probe.md](/data/angel/repos/modulation-guidance/Torus-Hamilton-Decomposition/RoundY/theorem/d5_295_promoted_collar_dualA_vs_singleB_probe.md),
which shows that on the promoted-collar baseline every one-row `B_{s,3}`
refinement is reducedly inert on `P_m` for the checked resonant moduli.

So any future `A+B` or `C+B` language must be read in two stages:

1. pick the genuinely color-`1` visible move first;
2. only then ask whether `B` repairs donor colors `0` or `2`.

### C. The first-pass 7-row visible grid already shows arithmetic splitting

On the row-3 seed, the visible-row grid

`{1,3,r-2,r-1,r,r+1,r+2}`

does not produce a universal one-line stabilizer across the discrimination pair
`m=51,57`.

Instead, it shows a clean split:

- `51` prefers rows such as `1`, `r+1`, and `C_{r-1,3}`;
- `57` prefers rows such as `3`, `r-2`, `r`, `r+2`;
- there is no overlap inside that first-pass grid.

This is exact evidence for a residue-sensitive split of the visible-row seed.

## 2. What this means when combined with the stable packet

Combining `289–295` with the row-3 notes gives the following picture.

### A. The pure color-1 frontier is no longer “find a compensator”

That reading is now too coarse.

- `289` says the promoted-collar packet is already a reduced control/no-go.
- `295` says a lone extra `B` row does not change the reduced base permutation.
- the row-3 notes say `B` is exact spectator for pure color `1`.

So the next step is not “find a compensator first”.
The next step is “choose the right visible seed first”.

### B. Residue-sensitive seed selection is now the leading direction

Among the options currently on the table, this one now looks most realistic:

> allow the resonant pure color-`1` theorem to branch by arithmetic subclass,
> and choose different visible row seeds in different subclasses.

Why this looks strongest now:

- the row-3 seed is strong but nonuniform;
- the first-pass visible grid already separates `51`-type and `57`-type
  behavior exactly;
- this points to a seed-selection problem, not yet to a missing support
  geometry problem.

In other words, the current data say:

- not “we have not found the right visible row yet”;
- but rather “the right visible row is probably not the same on all resonant
  subclasses”.

### C. New visible support outside the 7-row grid is a real but second-line option

This remains plausible, but it is no longer the first thing I would try.

Why it is second-line:

- the 7-row grid already contains several exact good rows;
- they simply disagree by modulus;
- that is stronger evidence for arithmetic seed-splitting than for missing
  geometry.

So “go outside the current 7-row grid” should now be read as:

- the fallback if residue-sensitive seed splitting inside the existing visible
  row geometry still fails.

### D. Moving to `k=4` is even more secondary

At the pure color-`1` level, `k=4` support is not yet forced by the current
exact data.

The present packet still points first to row-`3` visible geometry because:

- the stable control/no-go packet and the row-3 seed both live there;
- the exact visible-row grid failure is already visible there;
- the donor-aware role of `B` only becomes meaningful after the visible seed is
  fixed.

So `k=4` should currently be read as:

- a donor-aware or new-geometry escalation,
- not the next default move in the pure color-`1` branch.

## 3. Current recommended direction order

The best present order is:

1. **Residue-sensitive seed first.**
   Treat `51`-type and `57`-type moduli as potentially different visible-row
   seed classes, and try to phrase the next exact theorem packet that way.
2. **Only then search for a stabilizer/compensator on top of the chosen seed.**
   Since `B` is pure color-`1` spectator, this second stage should be justified
   by donor-color needs, not by the pure color-`1` reduced map.
3. **Only if this still fails, enlarge visible support geometry beyond the
   current 7-row grid.**
4. **Only after that consider `k=4` as the next default axis.**

## 4. Operational consequence

The immediate computational/theorem-shaping target is therefore not

- generic `A+B` search,
- generic new support search,
- or immediate `k=4` migration.

It is:

> formulate and test a residue-sensitive visible-row seed table for the
> resonant pure color-`1` branch, using `51`-type and `57`-type behavior as the
> first discrimination pair.

That is the sharpest next direction supported by the current exact evidence.
