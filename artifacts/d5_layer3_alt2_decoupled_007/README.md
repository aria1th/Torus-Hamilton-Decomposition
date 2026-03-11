# D5-LAYER3-ALT2-DECOUPLED-007

This artifact supports Session 25:

- research note: `tmp/note_s25.md`
- executable work item: `tmp/codex_work_s25.md`

## Result

Negative for the specific Session 25 target, but sharper than Session 24.

Allowing layer 3 to use alternate anchor `2` as well as `0` does revive monodromy-bearing rules, but it still does **not** produce any witness with both nontrivial cycles and nonzero monodromy on `m=5,7,9`.

Exact pilot outcome:

- clean survivors: `360`
- strict survivors: `360`
- combined cycle+monodromy survivors: `0`
- cycle-only survivors: `296`
- monodromy-only survivors: `32`
- trivial survivors: `32`

All `360` clean survivors were revalidated on the full torus and all five colors, and the validation matches the search summary exactly.

So Session 25 improves on Session 24 in one precise way:

- the layer-3 alt-`2` palette restores monodromy-only behavior,

but it still fails in the way that matters most:

- no rule combines the cycle mechanism and the monodromy mechanism.

## Searched family

I exhausted the full exact decoupled family:

- ordered pair `(s2,s3)` from
  - `q=-1`
  - `q+u=1`
  - `w+u=2`
  - `q+u=-1`
  - `u=-1`
- layer 2:
  - seed anchor `2`
  - alternate `a in {0,3,4}`
  - `s2`-only tables with orientations `2/a` and `a/2`
- layer 3:
  - seed anchor `3`
  - alternate `b in {0,2}`
  - `s3`-only tables with orientations `3/b` and `b/3`
- `phase_align`, `b1`, `b2` excluded

Exact search size:

- `25` ordered bit pairs
- `24` rules per pair
- `600` rules total

Search runtime: `58.28s`

Validation runtime: `51.52s`

The family choice is recorded in `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`.

## Structural outcome

Session 24 gave:

- `200` cycle-only clean survivors
- `0` monodromy-only
- `0` combined

Session 25 changes that to:

- layer-3 alt `0`: still exactly `200` cycle-only survivors
- layer-3 alt `2`: adds
  - `96` more cycle-only survivors
  - `32` monodromy-only survivors
  - `32` trivial survivors

What it does **not** add is any combined witness.

So the exact reading is:

- layer 3 alternate `2` is genuinely live;
- it can recover the missing monodromy mechanism;
- but in this decoupled family it either stays separate from the cycle mechanism or cancels against it.

## Exact monodromy-only regime

The `32` monodromy-only survivors occur in a very specific subfamily:

- layer 3 must use alternate `2`
- layer 3 orientation must be `2/3` or `3/2`
- layer 2 must use the `0/2` or `2/0` cycle split
- `s2` must be one of
  - `q=-1`
  - `q+u=1`
  - `q+u=-1`
  - `u=-1`
- `s3` must be one of the same four old bits

These rules recover twist, but lose the moving-cycle regime.

## Exact cancellation regime

The `32` trivial clean survivors are also new in Session 25. They occur when:

- layer 3 uses alternate `2`
- layer 3 orientation is again `2/3` or `3/2`
- layer 2 uses the `2/3` or `3/2` split

So the `{0,2}` enrichment does not just add monodromy. It also introduces exact cancellations back to trivial `U_0`.

## Best surviving cycle witness

The top-ranked cycle-only witnesses now include the stronger `w+u=2` layer-2 split:

- `s2 = w+u=2`
- `s3 = q+u=-1` (representative; the best cycle regime is still largely governed by layer 2)
- layer 2 orientation `2/4` or `4/2`
- layer 3 orientation `2/3` or `3/2`

On `m=5,7,9` this witness is:

- full-color Latin
- clean-frame
- strict-clock
- cycle-only
- total `U_0` cycle count `15` across the pilot range, i.e. the improved `m`-cycle regime already seen in the strongest one-old-bit branch

So Session 25 does not improve the orbit structure beyond the best existing cycle mechanism either.

## Strongest supported conclusion

Session 25 rules out another precise candidate family.

The decoupled two-old-bit branch with layer-3 palette `{0,2}` is still not enough to combine cycle structure and monodromy. It only yields three regimes:

- cycle-only
- monodromy-only
- exact cancellation to trivial `U_0`

but never both cycle and monodromy together.

The next credible branch should therefore enrich layer 3, not layer 2:

- keep one successful layer-2 cycle split fixed,
- add one predecessor-tail flag to layer 3 only, or
- add one second local layer-3 bit beyond the pure `s3` split.

## Files

- `code/torus_nd_d5_layer3_alt2_decoupled_common.py`
- `code/torus_nd_d5_layer3_alt2_decoupled_search.py`
- `code/torus_nd_d5_layer3_alt2_decoupled_validate.py`
- `inputs/note_s25.md`
- `inputs/codex_work_s25.md`
- `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`
- `data/search_summary.json`
- `data/validation_candidates.json`
- `data/validation_summary.json`
- `data/search.log`
- `data/validation.log`

## Reproduction

From the repo root:

```bash
python -m py_compile \
  scripts/torus_nd_d5_layer3_alt2_decoupled_common.py \
  scripts/torus_nd_d5_layer3_alt2_decoupled_search.py \
  scripts/torus_nd_d5_layer3_alt2_decoupled_validate.py

python scripts/torus_nd_d5_layer3_alt2_decoupled_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_layer3_alt2_decoupled_007/data/search_summary.json \
  --candidates-out artifacts/d5_layer3_alt2_decoupled_007/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_layer3_alt2_decoupled_validate.py \
  --candidates-json artifacts/d5_layer3_alt2_decoupled_007/data/validation_candidates.json \
  --m-list 5,7,9 \
  --out artifacts/d5_layer3_alt2_decoupled_007/data/validation_summary.json \
  --no-rich
```
