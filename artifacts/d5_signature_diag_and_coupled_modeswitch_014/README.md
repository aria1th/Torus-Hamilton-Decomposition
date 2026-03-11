# D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014

## Question

Stage A:

Does the exact predecessor-tail local signature on layer 2 add any pilot-return information beyond the current named three-flag partition in the fixed-twist / pure-alt-4 branch?

Stage B:

If the exact signature contributes one real new bit, can that bit work better as a coupled layer-3 controller than as a finer layer-2 coloring?

## Exact signature outcome

The exact layer-2 predecessor-tail signature is much smaller than the old `014` worst-case framing suggested.

On both layers `2` and `3`, for `m=5,7,9`:

- exact signature classes: `12`
- named coarse cells: `9`
- the exact signature is generated exactly by:
  - the named 4-bit partition
  - plus one new bit

That new bit is:

- `pred_sig1_phase_align`
- definition: `phase_align` on the predecessor in color-relative direction `1`
- exact signature coordinate: position `2`

The only named cells that split are:

- mask `1`
- mask `5`
- mask `9`

and in every split the two exact classes differ only at exact-signature coordinates `2` and `6`.

So the old “broad exact-signature layer-2 table” branch collapses immediately to a one-bit refinement problem.

## Stage A

Stage A has two parts:

1. local sterility diagnostic on the fixed-twist / fixed-base branch
2. exact one-bit layer-2 search using the new bit `pred_sig1_phase_align`

### Local diagnostic

The new exact bit is not completely invisible locally.

Inside split masks `1,5,9`, the bit can change the 3-step low-layer word and the 3-step increment on some pilot moduli, depending on the fixed layer-2 base:

- under `const_2/4`, the effect appears only in mask `5` for `m=7,9`
- under `const_4/2`, the effect appears in some split cells, varying with `m`

So the exact bit is locally real.

### Pilot-return diagnostic

The exact one-bit layer-2 search has only `16` rules total.

Result:

- clean strict survivors: `4`
- mixed survivors: `4`
- improved mixed survivors: `0`
- new pilot regimes: `0`

The only clean survivors are the four constant tables:

- `q=-1:2/4`
- `q=-1:4/2`
- `w+u=2:2/4`
- `w+u=2:4/2`

Each gives the old mixed baseline total cycle count `21`.

So the exact predecessor-tail refinement is not locally fake, but it is **pilot-return sterile** in the fixed-twist layer-2-only branch.

## Stage B

Chosen exact bit:

- `p = pred_sig1_phase_align`

Search stages:

1. `stage_b1`
   - layer-2 base fixed to `const_2/4` or `const_4/2`
   - layer-3 old bit fixed to `q+u=-1`
   - layer-3 slice modes `mode_p0, mode_p1` drawn from `{0/3, 3/0, 3/3}`

2. `stage_b2`
   - same fixed layer-2 bases
   - widen the layer-3 old bit to `{q+u=1, u=-1}`

3. `stage_b3`
   - allow the tiny synchronized layer-2 flip `flip_p0` or `flip_p1`
   - use old bits `{q+u=1, q+u=-1, u=-1}`

### Results

`stage_b1`:

- rules: `18`
- clean strict survivors: `6`
- profile: all `6` are `cycle_only`
- improved mixed survivors: `0`

`stage_b2`:

- rules: `36`
- clean strict survivors: `12`
- profile: all `12` are `cycle_only`
- improved mixed survivors: `0`

`stage_b3`:

- rules: `54`
- clean strict survivors: `0`

The clean survivors in `stage_b1` and `stage_b2` are even sharper than a generic negative:

- every clean survivor has `mode_p0 = mode_p1`
- so every clean survivor **ignores the exact bit completely on layer 3**
- the surviving rules are just constant slice choices `0/3`, `3/0`, or `3/3`

So the genuine coupled controller never survives clean-frame + strict-clock.

## Validation

The validation set includes:

- all `16` Stage A rules
- all `18` clean Stage B survivors

Validation results:

- total validated candidates: `34`
- Stage B validated candidates: `18`
- all `34/34` match the search summary exactly
- all `34/34` are full-color Latin on `m=5,7,9`
- all clean candidates remain strict
- top `18` Stage B stability spot-checks on `m=11,13` remain `cycle_only` with total cycle count `24`
- top `18` control-twist checks keep the same cycle signature

## Strongest conclusion

This is a strong double negative.

1. The old layer-2-only exact-signature main branch should be pruned.
   - The exact signature adds only one new bit.
   - That bit is locally visible.
   - But the exact one-bit layer-2 search produces no new pilot regime and no improved mixed witness.

2. The first coupled use of that exact bit also fails.
   - If layer 3 is allowed to depend on the bit, every clean survivor collapses back to a constant slice mode.
   - If a tiny synchronized layer-2 flip is added, no clean survivor remains.

So `pred_sig1_phase_align` is the correct exact extracted bit, but it is not the missing bulk/carry controller.

## Recommended next branch

Do not reopen:

- broad layer-2-only exact-signature table search
- more one-bit coupled layer-3 mode-switches built from this exact bit alone

The next honest widening should be:

- a slightly richer exact local-signature state, or
- a minimally synchronized two-layer family with more than one new local exact bit active at once

## Files

- `data/search_summary.json`: overall Stage A + Stage B summary
- `data/sigma2_summary.json`: exact signature class table
- `data/sterility_diagnostic.json`: local split-cell word/increment tables
- `data/stage_a_rule_rows.json`: all `16` Stage A rules
- `data/stage_b_rule_rows.json`: all Stage B rules
- `data/validation_candidates.json`: all reported candidates
- `data/validation_summary.json`: exact validation output
- `logs/search.log`: search stdout summary
- `logs/validation.log`: validation stdout summary
- `code/`: copied scripts
- `inputs/`: copied Session 32 note and codex work spec
- `SHA256SUMS.txt`: checksum manifest

## Reproduction

```bash
python -m py_compile \
  scripts/torus_nd_d5_signature_diag_and_coupled_modeswitch_common.py \
  scripts/torus_nd_d5_signature_diag_and_coupled_modeswitch_search.py \
  scripts/torus_nd_d5_signature_diag_and_coupled_modeswitch_validate.py

python scripts/torus_nd_d5_signature_diag_and_coupled_modeswitch_search.py \
  --pilot-m-list 5,7,9 \
  --out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/search_summary.json \
  --sigma-out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/sigma2_summary.json \
  --diagnostic-out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/sterility_diagnostic.json \
  --stage-a-out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/stage_a_rule_rows.json \
  --stage-b-out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/stage_b_rule_rows.json \
  --candidates-out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_signature_diag_and_coupled_modeswitch_validate.py \
  --candidates-json artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/validation_candidates.json \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --stability-limit 20 \
  --control-limit 20 \
  --out artifacts/d5_signature_diag_and_coupled_modeswitch_014/data/validation_summary.json \
  --no-rich
```
