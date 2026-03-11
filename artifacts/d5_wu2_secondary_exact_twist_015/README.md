# D5-WU2-SECONDARY-EXACT-TWIST-015

## Question

Can the exact bit

- `pred_sig1_phase_align`

work as a **secondary** layer-3 controller inside the already-validated `wu2` twist gadget, rather than as a standalone controller?

## Family

Fixed ingredients:

- layer `0 -> 1`
- layer `1 -> 4`
- layer `4+ -> 0`
- layer-2 base:
  - `const_2/4 = w+u=2 : 2/4`
  - `const_4/2 = w+u=2 : 4/2`
- layer-3 controller flag:
  - `pred_sig1_wu2`
  - `pred_sig4_wu2`
- exact secondary bit:
  - `pred_sig1_phase_align`
- controller state:
  - `(r,p) in {0,1}^2`
- slice palette:
  - `0/3`
  - `3/0`
  - `3/3`

Stage 1:

- old bit fixed to `q+u=-1`
- exact rules: `324`

Stage 2:

- old bits widened to `{q+u=1, q+u=-1, u=-1}`
- exact rules: `972`

## Main result

This is another clean negative, but a more informative one than `014`.

The `wu2` twist gadget survives exactly:

- Stage 1 clean strict survivors: `36`
- Stage 1 mixed survivors: `24`
- Stage 1 cycle-only survivors: `12`

- Stage 2 clean strict survivors: `108`
- Stage 2 mixed survivors: `72`
- Stage 2 cycle-only survivors: `36`

But every clean survivor is still on the old baseline:

- total pilot cycle count `21`
- no improved mixed survivor
- no new regime beyond the old mixed baseline

So the branch is live enough to preserve the old mixed mechanism, but not live enough to produce any positive new geometry.

## Strongest exact fact

Every clean survivor is `p`-trivial inside each active `wu2` slice.

Dependency-class counts:

Stage 1:

- `constant`: `12`
- `p_trivial_within_r`: `24`

Stage 2:

- `constant`: `36`
- `p_trivial_within_r`: `72`

There are:

- `0` clean survivors with genuine `p`-dependence
- `0` clean survivors of `xor_like`
- `0` clean survivors of `r_trivial_within_p`

So the exact bit never survives as a true secondary refinement. Whenever clean-frame + strict-clock survives, the table collapses to being constant in `p` inside each `wu2` branch.

## Regime summary

Stage 1:

- mixed `21`: `24`
- cycle-only `21`: `12`

Stage 2:

- mixed `21`: `72`
- cycle-only `21`: `36`

No anti-compressive classes `35/39/57/119/137/155` appear, but there is also no improvement below the old mixed baseline `21`.

## Representative survivors

Typical clean mixed survivor:

- base `const_2/4`
- controller `pred_sig1_wu2`
- old bit `q+u=-1`
- controller table:
  - `00 -> 0/3`
  - `01 -> 0/3`
  - `10 -> 3/0`
  - `11 -> 3/0`

This is mixed and clean, but it is exactly `p`-trivial: only `r` matters.

The same collapse holds throughout the clean survivor set.

## Validation

All `144` reported clean candidates were validated on the full torus and all five colors.

Results:

- all `144/144` match the search summary exactly
- all `144/144` are full-color Latin on `m=5,7,9`
- all clean candidates remain strict
- top `20` stability spot-checks on `m=11,13` remain mixed with total cycle count `24`
- top `20` control-twist checks keep the same cycle signature

So the failure is stable and not a search/validation mismatch.

## Strongest conclusion

This prunes the next natural refinement of `014`.

What `015` shows is:

- the exact bit is not dead in principle
- the `wu2` gadget is genuinely the live mixed mechanism
- but the exact bit still does not survive as a meaningful secondary controller inside that gadget

So the exact bit is neither:

- a viable standalone controller (`014`), nor
- a viable one-bit secondary refinement of the existing `wu2` controller (`015`)

## Recommended next widening

Do not reopen:

- larger one-bit exact refinements of the same `wu2` gadget

The next honest branch should introduce:

- either a second exact local bit,
- or a minimally synchronized two-layer family where the new exact bit and another local controller can act together.

## Files

- `data/search_summary.json`
- `data/validation_candidates.json`
- `data/validation_summary.json`
- `logs/search.log`
- `logs/validation.log`
- `code/`
- `inputs/`
- `SHA256SUMS.txt`

## Reproduction

```bash
python -m py_compile \
  scripts/torus_nd_d5_wu2_secondary_exact_twist_common.py \
  scripts/torus_nd_d5_wu2_secondary_exact_twist_search.py \
  scripts/torus_nd_d5_wu2_secondary_exact_twist_validate.py

python scripts/torus_nd_d5_wu2_secondary_exact_twist_search.py \
  --pilot-m-list 5,7,9 \
  --out artifacts/d5_wu2_secondary_exact_twist_015/data/search_summary.json \
  --candidates-out artifacts/d5_wu2_secondary_exact_twist_015/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_wu2_secondary_exact_twist_validate.py \
  --candidates-json artifacts/d5_wu2_secondary_exact_twist_015/data/validation_candidates.json \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --stability-limit 20 \
  --control-limit 20 \
  --out artifacts/d5_wu2_secondary_exact_twist_015/data/validation_summary.json \
  --no-rich
```
