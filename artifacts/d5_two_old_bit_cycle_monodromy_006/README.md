# D5-TWO-OLD-BIT-CYCLE-MONODROMY-006

This artifact supports Session 24:

- research note: `tmp/note_s24.md`
- executable work item: `tmp/codex_work_s24.md`

## Result

Negative for the specific Session 24 target.

The minimal decoupled two-old-bit family does produce many exact clean strict witnesses on `m=5,7,9`, but it does **not** combine the cycle mechanism and the monodromy mechanism in one witness.

Exact pilot outcome:

- clean survivors: `200`
- strict survivors: `200`
- combined cycle+monodromy survivors: `0`
- cycle-only survivors: `200`
- monodromy-only survivors: `0`
- trivial survivors: `0`

All `200` clean survivors were revalidated on the full torus and all five colors, and the validation matches the search summary exactly.

So this branch is not a global no-go. It is a much sharper statement:

- decoupling the old-bit choice by layer is enough to keep strict clean cycle witnesses,
- but it is **not** enough to preserve the monodromy mechanism.

## Searched family

I exhaustively searched the exact minimal family proposed in the note:

- ordered bit pair `(s2,s3)` from
  - `q=-1`
  - `q+u=1`
  - `w+u=2`
  - `q+u=-1`
  - `u=-1`
- layer 2:
  - seed anchor `2`
  - alternate anchor `a in {0,3,4}`
  - `s2`-only table, with orientations `2/a` and `a/2`
- layer 3:
  - seed anchor `3`
  - alternate anchor `0`
  - `s3`-only table, with orientations `3/0` and `0/3`
- `phase_align`, `b1`, `b2` intentionally excluded

Total exact search size:

- `25` ordered bit pairs
- `12` rules per pair
- `300` rules total

Search runtime: `38.57s`

Validation runtime: `32.57s`

The family choice is recorded in `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`.

## Structural outcome

The pair-level pattern is stronger than the raw survivor count:

- every ordered pair `(s2,s3)` has clean strict survivors;
- the survivor count depends only on `s2`, not on `s3`;
- the layer-3 orientation `3/0` versus `0/3` does not rescue monodromy;
- every surviving rule is cycle-only.

Per layer-2 bit, the clean survivor counts are:

- `q=-1`: `12` per ordered pair, `60` total
- `q+u=1`: `8` per ordered pair, `40` total
- `q+u=-1`: `8` per ordered pair, `40` total
- `u=-1`: `8` per ordered pair, `40` total
- `w+u=2`: `4` per ordered pair, `20` total

This means the minimal two-old-bit family effectively collapses back to a layer-2 cycle mechanism.

## Representative witness

The highest-ranked clean strict witnesses are still cycle-only. A representative example is:

- `s2 = q+u=-1`
- `s3 = q+u=-1` (but any `s3` with the same layer-2 choice gives the same qualitative outcome)
- layer 2 orientation `0/2`
- layer 3 orientation `0/3`

On `m=5,7,9` this witness is:

- full-color Latin
- clean-frame
- strict-clock
- `U_0 = m` cycles of length `m`
- all monodromies `0`

So the best exact witness in this branch does not improve beyond the Session 23 cycle regime.

## Strongest supported conclusion

Session 24 gives a clean negative answer to the precise question it asked.

Two independent old bits, used asymmetrically on layers 2 and 3 in this minimal decoupled family, do **not** combine orbit structure and monodromy.

What the result suggests:

- the layer-2 `s`-split cycle mechanism is robust;
- the layer-3 monodromy mechanism is fragile and is neutralized in this decoupled coupling;
- the next credible branch should enrich layer 3, not layer 2.

The most natural follow-up is:

- add one predecessor-tail flag to layer 3 only, or
- add one second local bit to layer 3 while keeping the successful layer-2 cycle split fixed.

## Files

- `code/torus_nd_d5_two_old_bit_cycle_monodromy_common.py`
- `code/torus_nd_d5_two_old_bit_cycle_monodromy_search.py`
- `code/torus_nd_d5_two_old_bit_cycle_monodromy_validate.py`
- `inputs/note_s24.md`
- `inputs/codex_work_s24.md`
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
  scripts/torus_nd_d5_two_old_bit_cycle_monodromy_common.py \
  scripts/torus_nd_d5_two_old_bit_cycle_monodromy_search.py \
  scripts/torus_nd_d5_two_old_bit_cycle_monodromy_validate.py

python scripts/torus_nd_d5_two_old_bit_cycle_monodromy_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_two_old_bit_cycle_monodromy_006/data/search_summary.json \
  --candidates-out artifacts/d5_two_old_bit_cycle_monodromy_006/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_two_old_bit_cycle_monodromy_validate.py \
  --candidates-json artifacts/d5_two_old_bit_cycle_monodromy_006/data/validation_candidates.json \
  --m-list 5,7,9 \
  --out artifacts/d5_two_old_bit_cycle_monodromy_006/data/validation_summary.json \
  --no-rich
```
