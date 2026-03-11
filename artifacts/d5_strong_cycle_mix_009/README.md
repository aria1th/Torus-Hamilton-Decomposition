# D5-STRONG-CYCLE-MIX-009

## Executive summary

I split the Session 27 note into:

- `tmp/note_s27.md`
- `tmp/codex_work_s27.md`

and then executed the exact staged graft search.

Main result:

- The Session 26 twist gadget is much more robust than expected.
- Stage 1, with only the representative layer-3 old bit `q=-1`, already gives:
  - `240` clean survivors
  - `240` strict survivors
  - `192` mixed survivors
  - `48` cycle-only survivors
  - `0` monodromy-only survivors
  - `0` trivial survivors
- But none of those mixed survivors improve the mixed baseline from Session 26.

So Stage 2 was triggered automatically.

Stage 2 result:

- widening the layer-3 old bit to
  `{q=-1, q+u=1, q+u=-1, u=-1}`
  gives
  - `960` clean survivors
  - `960` strict survivors
  - `912` mixed survivors
  - `48` cycle-only survivors
  - `0` monodromy-only survivors
  - `0` trivial survivors
- again, `0` mixed survivors improve the baseline cycle profile.

The sharp conclusion is:

- the twist graft survives on almost everything,
- but it never compresses cycles beyond the old mixed baseline
  `U_0 = m` cycles of length `m`.

## Search shape

Fixed anchors:

- layer `0` anchor `1`
- layer `1` anchor `4`
- layer `4+` anchor `0`

Stage 1:

- `20` exact layer-2 seeds
- layer-3 old bit fixed to `q=-1`
- predecessor flag in
  - `pred_sig1_wu2`
  - `pred_sig4_wu2`
- ordered distinct slice pair from
  - `0/3`
  - `3/0`
  - `3/3`
- raw rule count: `20 x 2 x 6 = 240`

Stage 2:

- same layer-2 seed list
- same predecessor flags
- same ordered slice-pair list
- widen layer-3 old bit to
  - `q=-1`
  - `q+u=1`
  - `q+u=-1`
  - `u=-1`
- raw rule count: `20 x 4 x 2 x 6 = 960`

Baseline comparison used in the search:

- Session 26 mixed baseline:
  - total pilot `U_0` cycle count `21`
  - profile `m` cycles of length `m`
- strongest earlier cycle-only baseline:
  - total pilot `U_0` cycle count `15`

Improvement test:

- a mixed survivor counts as improved iff
  - total pilot `U_0` cycle count `< 21`, or
  - at least one pilot modulus has fewer than `m` cycles

No rule in either stage passed that test.

## Structural outcome

### 1. Stage 1

Every non-alt-4 layer-2 seed keeps twist:

- `q=-1` with alternates `0,3`
- `q+u=1` with alternates `0,3`
- `q+u=-1` with alternates `0,3`
- `u=-1` with alternates `0,3`

For those seeds, all `12` gadgets survive and are mixed.

The two strongest cycle-compression seeds fail in the same way:

- `q=-1` with alternate `4`
- `w+u=2` with alternate `4`

For those seeds, all `12` Stage 1 gadgets survive, but only as cycle-only rules.

### 2. Stage 2

Widening the layer-3 old bit rescues the alt-`4` seeds dynamically, but not structurally:

- for `q=-1` alt `4` and `w+u=2` alt `4`
  - layer-3 bit `q=-1` still gives cycle-only behavior
  - layer-3 bits `q+u=1`, `q+u=-1`, `u=-1` all give mixed behavior

So Stage 2 does recover twist on the strongest layer-2 cycle seeds.

But even there the cycle profile stays exactly at the old mixed baseline:

- total pilot `U_0` cycle count `21`
- no pilot modulus has fewer than `m` cycles

That is the real no-go proved by this artifact.

## Validation

Pilot validation:

- every reported clean survivor was revalidated exactly on `m=5,7,9`
- candidate count: `960`
- all candidates matched the search summary
- all candidates are full-color Latin on the pilot range
- all clean candidates remain strict-clock

Stability spot-checks:

- the top `12` mixed survivors were rechecked on `m=11,13`
- all `12` remain mixed
- representative stability profile:
  - total `U_0` cycle count `24 = 11 + 13`
  - max cycle length `13`
  - total nonzero monodromies `24`

So the Session 26 mixed regime persists beyond the pilot range in the tested cases, but it persists in the same non-compressing form.

## Strongest supported conclusion

The Session 26 predecessor-twist gadget is now well understood operationally:

- it is easy to transplant,
- it is compatible with almost every tested cycle-capable layer-2 seed,
- Stage 2 even restores mixed behavior on the alt-`4` seeds,
- but it appears dynamically decoupled from the stronger cycle-compression mechanism.

In other words:

- twist generation is no longer the bottleneck;
- preserving twist while compressing cycles remains open.

The next credible branch is therefore not “wider one-bit grafting.” It should be one of:

- a genuinely interactive layer-2/layer-3 gadget, or
- a theorem-level statement that the current twist graft family is forced to stay in the `m`-cycle mixed regime.

## Files

Primary machine outputs:

- `data/search_summary.json`
- `data/validation_candidates.json`
- `data/validation_summary.json`

Logs:

- `logs/search.log`
- `logs/validation.log`

Code:

- `code/torus_nd_d5_strong_cycle_mix_common.py`
- `code/torus_nd_d5_strong_cycle_mix_search.py`
- `code/torus_nd_d5_strong_cycle_mix_validate.py`

Inputs:

- `inputs/note_s27.md`
- `inputs/codex_work_s27.md`
- `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`

## Reproducibility

Commands used:

```bash
python -m py_compile \
  scripts/torus_nd_d5_strong_cycle_mix_common.py \
  scripts/torus_nd_d5_strong_cycle_mix_search.py \
  scripts/torus_nd_d5_strong_cycle_mix_validate.py

python scripts/torus_nd_d5_strong_cycle_mix_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_strong_cycle_mix_009/data/search_summary.json \
  --candidates-out artifacts/d5_strong_cycle_mix_009/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_strong_cycle_mix_validate.py \
  --candidates-json artifacts/d5_strong_cycle_mix_009/data/validation_candidates.json \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --stability-limit 12 \
  --out artifacts/d5_strong_cycle_mix_009/data/validation_summary.json \
  --no-rich
```

Runtimes in this run:

- search: `145.530s`
- validation: `135.331s`

The bundle also includes `SHA256SUMS.txt`.
