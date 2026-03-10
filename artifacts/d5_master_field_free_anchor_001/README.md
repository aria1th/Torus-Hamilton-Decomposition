# D5 Master Field Free Anchor 001

This artifact packages the free-anchor master-field search requested by `tmp/d5_master_field_free_anchor_codex_template.md`.

## Contents
- `scripts/`: shared quotient helper plus the free-anchor searcher and validator
- `data/search_summary.json`: exact search results and saved feasible fields
- `data/validation_summary.json`: deterministic revalidation on `m=5,7,9,11,13`
- `data/stable_anchor_two_atom_best_field.json`: best strict-clock field from Schema A
- `data/unit_anchor_three_atom_best_field.json`: best strict-clock field from Schema B
- `logs/search.log`: raw search output
- `logs/validation.log`: raw validation output
- `summary.md`: condensed report

## Main Result
- Feasible cyclic-equivariant Latin fields exist on both quotient schemas.
- None of the saved fields has the desired representative-color section dynamics.
- The best strict-clock fields on both schemas have `U_0` equal to `m^2` fixed points with monodromy `0`.

## Reproduction
```bash
python scripts/torus_nd_d5_master_field_free_anchor_search.py \
  --schemas stable_anchor_two_atom,unit_anchor_three_atom \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --max-time-sec 20 \
  --workers 8 \
  --random-seed 20260310 \
  --solution-limit 3 \
  --out artifacts/d5_master_field_free_anchor_001/data/search_summary.json \
  --no-rich

python scripts/torus_nd_d5_master_field_free_anchor_validate.py \
  --search-summary-json artifacts/d5_master_field_free_anchor_001/data/search_summary.json \
  --m-list 5,7,9,11,13 \
  --field-limit 5 \
  --out artifacts/d5_master_field_free_anchor_001/data/validation_summary.json \
  --no-rich
```

## Packaging
```bash
tar -czf artifacts/d5_master_field_free_anchor_001.tar.gz artifacts/d5_master_field_free_anchor_001
```
