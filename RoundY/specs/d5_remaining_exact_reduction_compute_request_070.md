# D5 Remaining Exact-Reduction Compute Request 070

This request is only for the next heavier support step if desired.

## Goal
Push the exact-reduction / realization validation beyond the frozen checked-range branch without reopening broad controller search.

## Requested compute
1. Exhaustive larger-odd-modulus regeneration of the active best-seed branch for `m = 13,15,...,41`.
2. Rebuild the marked carry-jump slice chains and longer spliced source-chains.
3. Re-run the same quotient diagnostics on:
   - all `045` catalog families on the slice chains,
   - all `045` catalog families on the spliced source-chains,
   - the full active branch for exact deterministic `event5` quotient (start with `core_transition`, `point_defect_basis`, then the full `gauge_transition_basis` catalog if budget permits).
4. Check whether the minimal exact deterministic quotient scale on the slice chains remains exactly `m`, and whether the spliced source-chains still refuse to compress below `m(m-3)`.

## Expected compute envelope
- CPU: 16–32 workers helpful but not required
- RAM: 16–32 GB should be comfortable
- Wall time:
  - full branch regeneration dominates,
  - quotient searches themselves should be on the order of minutes once the raw rows are frozen.
