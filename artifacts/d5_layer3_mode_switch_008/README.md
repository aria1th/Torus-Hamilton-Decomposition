# D5-LAYER3-MODE-SWITCH-008

## Executive summary

I split the Session 26 note into:

- `tmp/note_s26.md`
- `tmp/codex_work_s26.md`

and then executed the exact representative one-extra-flag search.

Main result:

- The simple named predecessor-flag family already succeeds.
- On the pilot range `m=5,7,9`, the simple family has:
  - `64` clean survivors
  - `64` strict survivors
  - `24` combined cycle+monodromy survivors
  - `32` cycle-only survivors
  - `8` monodromy-only survivors
  - `0` trivial survivors
- Because `both_count > 0` already occurs in the simple family, the exact predecessor-local-signature fallback was **not** needed and was not run.

So Session 26 is a genuine positive result:

one extra layer-3 local flag is already enough to mix the cycle-preserving and monodromy-producing regimes.

## Search family

Fixed data:

- layer `0` anchor `1`
- layer `1` anchor `4`
- layer `4+` anchor `0`
- representative old bit on layers `2` and `3`: `q=-1`
- layer `2` fixed to representative alternate `0`
- both layer-2 orientations tested:
  - `0/2`
  - `2/0`

Layer-3 mode tables:

- for each flag value `p in {0,1}`, choose one mode from
  - `0/3`
  - `3/0`
  - `2/3`
  - `3/2`
  - `3/3`

Simple predecessor flags tested:

- `pred_any_phase_align`
  - `1` iff at least one color-relative predecessor has `phase_align = 1`
- `pred_sig0_phase_align`
  - `1` iff the color-relative predecessor in direction `0` has `phase_align = 1`
- `pred_sig1_wu2`
  - `1` iff the color-relative predecessor in direction `1` satisfies `w+u = 2`
- `pred_sig4_wu2`
  - `1` iff the color-relative predecessor in direction `4` satisfies `w+u = 2`

Important note:

- the Session 26 note named these four flags, but the repo did not contain a canonical earlier implementation module for them;
- the formulas above are the explicit operationalization used in this artifact.

Optimization used:

- exact pattern-based color-0 Latin pruning on unique predecessor-feature patterns;
- exact full-color Latin + first-return evaluation only on Latin survivors.

This keeps the search exact while avoiding per-vertex incoming-degree scans on every raw rule.

## Strongest witness

Representative combined witness:

- predecessor flag: `pred_sig1_wu2`
- layer `2`: `0/2`
- layer `3`, `p=0`: `0/3`
- layer `3`, `p=1`: `3/0`

An equivalent family also appears with `pred_sig4_wu2`.

Validated color-0 return on the pilot range:

- `m=5`
  - `U_0` has `5` cycles, all length `5`
  - all monodromies are `3`
- `m=7`
  - `U_0` has `7` cycles, all length `7`
  - all monodromies are `5`
- `m=9`
  - `U_0` has `9` cycles, all length `9`
  - all monodromies are `7`

So the mixed regime is clean, strict, and structurally simple:

- moving cycles persist;
- every cycle carries uniform nonzero monodromy;
- the mixed witness is not a fragile one-off.

## Family breakdown

Per-flag results:

- `pred_any_phase_align`
  - `10` clean strict survivors
  - `0` combined
  - `8` cycle-only
  - `2` monodromy-only
- `pred_sig0_phase_align`
  - `10` clean strict survivors
  - `0` combined
  - `8` cycle-only
  - `2` monodromy-only
- `pred_sig1_wu2`
  - `22` clean strict survivors
  - `12` combined
  - `8` cycle-only
  - `2` monodromy-only
- `pred_sig4_wu2`
  - `22` clean strict survivors
  - `12` combined
  - `8` cycle-only
  - `2` monodromy-only

The positive mechanism is therefore concentrated in the `wu2` predecessor tests, not the phase-align tests.

## Files

Primary machine outputs:

- `data/search_summary.json`
- `data/validation_candidates.json`
- `data/validation_summary.json`

Logs:

- `logs/search.log`
- `logs/validation.log`

Code:

- `code/torus_nd_d5_layer3_mode_switch_common.py`
- `code/torus_nd_d5_layer3_mode_switch_search.py`
- `code/torus_nd_d5_layer3_mode_switch_validate.py`

Inputs:

- `inputs/note_s26.md`
- `inputs/codex_work_s26.md`
- `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`

## Reproducibility

Commands used:

```bash
python -m py_compile \
  scripts/torus_nd_d5_layer3_mode_switch_common.py \
  scripts/torus_nd_d5_layer3_mode_switch_search.py \
  scripts/torus_nd_d5_layer3_mode_switch_validate.py

python scripts/torus_nd_d5_layer3_mode_switch_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_layer3_mode_switch_008/data/search_summary.json \
  --candidates-out artifacts/d5_layer3_mode_switch_008/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_layer3_mode_switch_validate.py \
  --candidates-json artifacts/d5_layer3_mode_switch_008/data/validation_candidates.json \
  --m-list 5,7,9 \
  --out artifacts/d5_layer3_mode_switch_008/data/validation_summary.json \
  --no-rich
```

Search runtime in this run:

- `8.750s`

Validation runtime in this run:

- `4.421s`

The bundle also includes `SHA256SUMS.txt`.
