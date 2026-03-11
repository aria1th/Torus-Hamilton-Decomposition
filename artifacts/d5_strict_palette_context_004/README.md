# D5-STRICT-PALETTE-CONTEXT-004

This artifact supports the Session 22 branch:

- input note: `tmp/note_s22.md`
- executable work item: `tmp/codex_work_s22.md`

Question:

Can a 5-context active layer-2/3 grammar depending only on
`phase_align, b1, b2`
produce nontrivial section dynamics if the alternate anchors are taken from the strict-friendly set
`{0,2,3,4}` rather than `1`?

## Result

Negative on the exact pilot range `m=5,7,9`.

- Exhaustive search space: `16` strict-friendly anchor families `(a,b)` with `1024` raw bit-table rules each, `16384` raw rules total.
- Search optimization 1: deduplicate bit tables to effective anchor tables inside each family before evaluation.
- Search optimization 2: test the color-0 Latin condition on the small `(S, delta)` quotient instead of the full torus; only actual survivors get full first-return analysis.
- Effective survivor counts by family sum to `49`, but globally these collapse to exactly `16` unique actual rules.
- All `16` unique survivors are context-independent constant tables.
- All `16` are `Latin + clean_frame + strict_clock` on the pilot range.
- All `16` still have trivial `U_0`: exactly `m^2` fixed points and monodromy `0` on `m=5,7,9`.
- There are `0` context-dependent clean survivors, `0` context-dependent strict survivors, and `0` nontrivial-`U_0` survivors.

So the strengthened conclusion is:

Within the context-only two-anchor family using the exact pilot bits `phase_align, b1, b2` and strict-friendly alternates `{0,2,3,4}`, every surviving rule collapses to a constant anchor pair. Context dependence does not survive Latin.

## Surviving Constant Pairs

The `16` unique surviving actual rules are exactly the constant pairs

- layer 2 anchor in `{0,2,3,4}`
- layer 3 anchor in `{0,2,3,4}`

with no context dependence in either layer.

Equivalently, the surviving pairs are:

- `(0,0)`, `(0,2)`, `(0,3)`, `(0,4)`
- `(2,0)`, `(2,2)`, `(2,3)`, `(2,4)`
- `(3,0)`, `(3,2)`, `(3,3)`, `(3,4)`
- `(4,0)`, `(4,2)`, `(4,3)`, `(4,4)`

## Validation

The search script uses the quotient-based color-0 Latin filter for speed. The validation script then rechecks every unique surviving actual rule on the full torus with all five colors.

Validated set:

- `16` unique surviving actual rules
- full-color Latin check: all pass on `m=5,7,9`
- search/validation summary agreement: exact
- nontrivial `U_0` witnesses: none

Note:

- This branch is only defined on the pilot moduli `m=5,7,9`, because the exact `b1,b2` lookup tables used here are only available on that range. Extending to `m=11,13` would require a new bit-definition step, not just rerunning the validator.

## Files

- `code/torus_nd_d5_strict_palette_context_common.py`
- `code/torus_nd_d5_strict_palette_context_search.py`
- `code/torus_nd_d5_strict_palette_context_validate.py`
- `inputs/note_s22.md`
- `inputs/codex_work_s22.md`
- `data/search_summary.json`
- `data/validation_candidates.json`
- `data/validation_summary.json`
- `data/search.log`
- `data/validation.log`

## Reproduction

From the repo root:

```bash
python -m py_compile \
  scripts/torus_nd_d5_strict_palette_context_common.py \
  scripts/torus_nd_d5_strict_palette_context_search.py \
  scripts/torus_nd_d5_strict_palette_context_validate.py

python scripts/torus_nd_d5_strict_palette_context_search.py \
  --m-list 5,7,9 \
  --out artifacts/d5_strict_palette_context_004/data/search_summary.json \
  --candidates-out artifacts/d5_strict_palette_context_004/data/validation_candidates.json \
  --no-rich

python scripts/torus_nd_d5_strict_palette_context_validate.py \
  --candidates-json artifacts/d5_strict_palette_context_004/data/validation_candidates.json \
  --m-list 5,7,9 \
  --out artifacts/d5_strict_palette_context_004/data/validation_summary.json \
  --no-rich
```

## Recommended Next Branch

This closes the context-only strict-friendly two-anchor branch.

The next credible constructive branch is:

- add one old atom bit to the active layer-2/3 output grammar, or
- move directly to a larger active grammar where Latin can distinguish states beyond `phase_align, b1, b2`.
