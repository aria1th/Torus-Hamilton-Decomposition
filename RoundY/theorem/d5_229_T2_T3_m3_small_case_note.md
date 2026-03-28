# D5 note: the `m=3` small case for `T2` and `T3`

This note records the `m=3` edge case that lies outside the clean symbolic `m>=5` obstruction proofs for `T2` and `T3`.

## What was checked

Using the surfaced 2026-03-21 bundle and the same one-label repair scope as d5_226,
I ran an exhaustive `m=3` scan for

- `T2 = sigma22 = [4,1,4]/[2,1,2]`
- `T3 = sigma33 = [4,4,1]/[2,2,1]`

across

- all `96` one-gate repairs,
- all `1920` one-bit repairs,
- with cocycle defect in `none / left / right / both`.

The script is:

- `d5_229_T2_T3_m3_one_label_scan.py`

and the machine summary is:

- `d5_229_T2_T3_m3_one_label_scan_summary.json`

## Result

For `m=3`:

- both base rows are already non-Latin;
- no one-gate repair is Latin for either `T2` or `T3`;
- no one-bit repair is Latin for either `T2` or `T3`.

More explicitly:

### `T2`

- `latin_all_colors_base = false`
- `overfull_targets_all_colors = 120`
- one-gate Latin count = `0 / 96`
- one-bit Latin count = `0 / 1920`

The color-0 collision profile differs from the clean `m>=5` theorem:

- `(B,R1)` occurs `6` times,
- `(B,R2)` occurs `6` times,
- `(B,L2)` occurs `6` times,
- `(B,L3,R3)` occurs `6` times.

So `m=3` is an exceptional small-modulus shape, but it is still dead on the full one-label repair scope.

### `T3`

- `latin_all_colors_base = false`
- `overfull_targets_all_colors = 60`
- one-gate Latin count = `0 / 96`
- one-bit Latin count = `0 / 1920`

Its color-0 profile is also exceptional:

- `(B,R1)` occurs `6` times,
- `(L2,R2)` occurs `6` times.

Again, the clean `m>=5` four-family proof does not describe `m=3`, but the whole one-label repair scope still fails.

## Interpretation

So the status is now:

- symbolic obstruction proofs for `T2` and `T3` on odd `m>=5`,
- exhaustive compute closure for the remaining odd modulus `m=3` on the same sharpened one-label repair scope.

That is enough to treat `T2` and `T3` as closed under the sharpened `T0` convention for **all odd `m>2`**.
