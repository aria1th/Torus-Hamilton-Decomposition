# D5-ALT4-THREE-FLAG-GEOMETRY-013

## Question

With the canonical mixed twist gadget fixed, can adding one extra named predecessor flag to the current two-flag layer-2 state produce a clean strict mixed witness with better cycle compression than the current mixed baseline on `m=5,7,9`?

Tested extra flags:

- `pred_any_phase_align`
- `pred_sig0_phase_align`

Fixed ingredients:

- layer `0 -> 1`
- layer `1 -> 4`
- layer `4+ -> 0`
- layer-3 flag `pred_sig1_wu2`
- layer-3 old bit `q+u=-1`
- canonical layer-3 slice pair `0/3 , 3/0`
- pure layer-2 mode pool
  - `q=-1:2/4`
  - `q=-1:4/2`
  - `w+u=2:2/4`
  - `w+u=2:4/2`

Per extra flag, the search exhausts all `4^8 = 65536` eight-state tables, for `131072` exact rules total.

## Method

The exhaustive pass is exact on the full torus, but optimized:

- search step:
  - exact color-0 Latin and exact color-0 first-return dynamics on `m=5,7,9`
  - cyclic equivariance is used to avoid recomputing all five colors during the exhaustive pass
  - compact JSON rows are saved for every tested eight-state assignment
- validation step:
  - exact full-color Latin and full-color return checks on the reported frontier
  - stability spot-checks on `m=11,13`
  - sign-reversed control twist checks on the top frontier rules

## Main result

This is a clean negative.

Both extra flags give the same exact outcome:

- clean strict survivors: `1024`
- mixed survivors: `992`
- monodromy-only survivors: `32`
- cycle-only survivors: `0`
- improved mixed survivors: `0`

So neither three-flag family beats the current mixed baseline total cycle count `21`.

The exact regime histogram is identical for both extra flags:

- mixed `21`: `416`
- mixed `35`: `128`
- mixed `39`: `320`
- mixed `57`: `32`
- mixed `119`: `32`
- mixed `137`: `64`
- monodromy-only `155`: `32`

No new pilot regime appears beyond the exact landscape already seen in Session `012`. The three-flag widening is therefore live at the table level, but dynamically sterile with respect to the sign problem.

## Dependence-class summary

Among the `1024` clean strict survivors for each extra flag:

- `4` are constant
- `12` factor through `pred_sig1_wu2`
- `12` factor through `pred_sig4_wu2`
- `12` factor through `pred_sig1_wu2 ^ pred_sig4_wu2`
- `216` are `genuine_multi_state`
- `768` are `genuine_eight_state`

So this is not a collapse-to-coarse-state failure. Most surviving tables genuinely use the full eight-state partition, but they still realize only the old anti-compressive regime set.

## Validation

The search selected `56` frontier candidates for exact full-color validation.

Validation results:

- all `56/56` frontier candidates match the search summary exactly
- all `56/56` are full-color Latin on `m=5,7,9`
- all clean frontier candidates remain strict
- the top `20` stability spot-checks on `m=11,13` stay mixed, with total cycle count `24`
- the top `20` sign-reversed control-twist checks keep the same cycle signature

So the negative is stable on the checked range and is not sensitive to twist sign on the tested frontier.

## Strongest conclusion

`pred_any_phase_align` and `pred_sig0_phase_align` are not the missing layer-2 resolution.

They are strong enough to support many genuinely eight-state clean strict tables, but they do not create any new positive geometry. The best mixed witness remains the old baseline `m`-cycle profile.

The next credible branch is:

- exact predecessor-tail local-signature state on layer `2`

not:

- more pure alt-`4` mode widening
- more named phase-align predecessor flags
- more twist-sign variation

## Files

- `data/search_summary.json`: aggregate exact search result
- `data/rule_rows/rule_rows_pred_any_phase_align.json`: compact rows for all `65536` rules in that family
- `data/rule_rows/rule_rows_pred_sig0_phase_align.json`: compact rows for all `65536` rules in that family
- `data/validation_candidates.json`: reported frontier
- `data/validation_summary.json`: exact full-color validation
- `logs/search.log`: search stdout summary
- `logs/validation.log`: validation stdout summary
- `code/`: copied search scripts
- `inputs/`: copied Session 31 note and codex work spec
- `SHA256SUMS.txt`: checksum manifest

## Reproduction

```bash
python -m py_compile \
  scripts/torus_nd_d5_alt4_three_flag_geometry_common.py \
  scripts/torus_nd_d5_alt4_three_flag_geometry_search.py \
  scripts/torus_nd_d5_alt4_three_flag_geometry_validate.py

python scripts/torus_nd_d5_alt4_three_flag_geometry_search.py \
  --pilot-m-list 5,7,9 \
  --out artifacts/d5_alt4_three_flag_geometry_013/data/search_summary.json \
  --rows-dir artifacts/d5_alt4_three_flag_geometry_013/data/rule_rows \
  --candidates-out artifacts/d5_alt4_three_flag_geometry_013/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_alt4_three_flag_geometry_validate.py \
  --candidates-json artifacts/d5_alt4_three_flag_geometry_013/data/validation_candidates.json \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --stability-limit 20 \
  --control-limit 20 \
  --out artifacts/d5_alt4_three_flag_geometry_013/data/validation_summary.json \
  --no-rich
```
