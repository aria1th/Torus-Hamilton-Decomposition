# D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005

This artifact supports Session 23:

- research note: `tmp/note_s23.md`
- executable work item: `tmp/codex_work_s23.md`

## Result

Positive on the exact pilot range `m=5,7,9`.

The previous branch conclusion was:

- context-only dependence on `phase_align, b1, b2` never survives the clean-frame stage.

This branch changes that immediately:

- adding a single old quotient bit is already enough to produce context-dependent clean survivors;
- this happens already in exact one-layer-active families;
- many of those survivors are also strict-clock and have nontrivial `U_0`.

## Search design

I tested all five existing old quotient atoms as the extra bit:

- `q=-1`
- `q+u=1`
- `w+u=2`
- `q+u=-1`
- `u=-1`

For each bit:

- exact pilot moduli: `m=5,7,9`
- strict-friendly alternates:
  - layer 2 alternate `a in {0,2,3,4}`
  - layer 3 alternate `b in {0,2,3,4}`
- active contexts:
  - `align_s0`, `align_s1`
  - `00_s0`, `00_s1`
  - `01_s0`, `01_s1`
  - `10_s0`, `10_s1`
  - `11_s0`, `11_s1`

Exact search stages:

1. one-layer-active families:
   - `(a,3)` with only layer 2 active
   - `(2,b)` with only layer 3 active
2. full two-layer families `(a,b)`

Optimization choice:

- the color-0 Latin stage is factored by active layer;
- only layer-level Latin survivor tables are sent into the full clean-frame / `U_0` evaluation;
- every unique reported survivor is then validated on the full torus and all five colors.

The search-shape decision is recorded in `inputs/DOCUMENT_FOR_EXTERNAL_REVIEW.md`.

## Exact outcomes

Search runtime: `91.31s`

Validation runtime: `35.59s`

Global exact counts:

- family-aggregated clean survivors: `723`
- family-aggregated strict survivors: `723`
- unique clean survivors: `328`
- unique strict survivors: `328`
- unique context-dependent clean survivors: `248`
- unique context-dependent strict survivors: `248`
- unique strict survivors with nontrivial `U_0`: `240`

Validation:

- unique survivors validated: `328`
- full-color Latin on `m=5,7,9`: all pass
- search/validation summary agreement: exact

### One-layer-active success

This already succeeds before any two-layer coupling.

Context-dependent clean families by extra bit:

- `q=-1`: `6`
- `q+u=1`: `4`
- `w+u=2`: `2`
- `q+u=-1`: `4`
- `u=-1`: `4`

So every tested old bit produces at least one context-dependent clean survivor in a one-layer-active family.

### Full two-layer expansion

Full two-layer families with context-dependent clean survivors by extra bit:

- `q=-1`: `15`
- `q+u=1`: `12`
- `w+u=2`: `7`
- `q+u=-1`: `12`
- `u=-1`: `12`

So the one-old-bit branch is not marginal; it opens a large exact witness set.

## Representative witnesses

### First simple one-layer witness

The first strong one-layer-active witness is:

- extra bit: `q=-1`
- only layer 2 active
- layer 2 alternate anchor: `0`
- layer 2 table:
  - use anchor `2` on every `s=0` context
  - use anchor `0` on every `s=1` context
- layer 3 fixed at the seed anchor `3`

On `m=5,7,9` this witness is:

- full-color Latin
- clean-frame
- strict-clock
- `U_0` nontrivial, with exactly `m` cycles of length `m`
- all monodromies still `0`

### Highest-ranked strict witness in the global list

The top-ranked strict witness uses:

- extra bit: `q+u=-1`
- family `(a,b) = (0,0)`
- layer 2 table again split only by `s`
- layer 3 constant `3`

It has the same qualitative pilot dynamics:

- strict-clock `True`
- `U_0` has `m` cycles of length `m`
- monodromies all `0`

## Strongest supported conclusion

Session 23 is a positive branch result.

The clean-frame barrier from the context-only branch is not fundamental. One extra old quotient bit already breaks it, and it does so in the smallest staged search:

- first at one-layer-active level,
- then more broadly in full two-layer families.

So the next constructive branch should not ask
"is one old bit enough?"

That is now answered: yes.

The next honest question is:

- which one-old-bit witness is the best seed for pushing beyond `m` cycles of length `m`, and
- whether adding predecessor-tail structure or a second active bit can turn these `U_0` dynamics into fewer, longer cycles or nonzero monodromy.

## Files

- `code/torus_nd_d5_one_old_bit_clean_common.py`
- `code/torus_nd_d5_one_old_bit_clean_survival_search.py`
- `code/torus_nd_d5_one_old_bit_clean_survival_validate.py`
- `inputs/note_s23.md`
- `inputs/codex_work_s23.md`
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
  scripts/torus_nd_d5_one_old_bit_clean_common.py \
  scripts/torus_nd_d5_one_old_bit_clean_survival_search.py \
  scripts/torus_nd_d5_one_old_bit_clean_survival_validate.py

python scripts/torus_nd_d5_one_old_bit_clean_survival_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_one_old_bit_clean_survival_005/data/search_summary.json \
  --candidates-out artifacts/d5_one_old_bit_clean_survival_005/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_one_old_bit_clean_survival_validate.py \
  --candidates-json artifacts/d5_one_old_bit_clean_survival_005/data/validation_candidates.json \
  --m-list 5,7,9 \
  --out artifacts/d5_one_old_bit_clean_survival_005/data/validation_summary.json \
  --no-rich
```
