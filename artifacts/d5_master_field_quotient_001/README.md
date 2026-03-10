# D5 Master Field Quotient 001

This artifact packages the master-field quotient search requested by `tmp/d5_master_field_codex_template.md`.

## Contents
- `scripts/`: schema helper, exact CP-SAT searcher, and validator
- `data/search_summary.json`: exact search result for the anchored quotient schemas
- `data/validation_summary.json`: post-search validation summary
- `logs/search.log`: raw CP-SAT search log
- `logs/validation.log`: validator output
- `summary.md`: short report with the quotient definitions and the no-go conclusion

## Result
- `stable_anchor_two_atom`: `INFEASIBLE`
- `unit_anchor_three_atom`: `INFEASIBLE`

No feasible permutation table `\Pi_\theta` was found in the searched quotient families.

## Reproduction
```bash
python scripts/torus_nd_d5_master_field_quotient_search.py \
  --schemas stable_anchor_two_atom,unit_anchor_three_atom \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --max-time-sec 120 \
  --workers 8 \
  --random-seed 20260310 \
  --out artifacts/d5_master_field_quotient_001/data/search_summary.json \
  --no-rich

python scripts/torus_nd_d5_master_field_quotient_validate.py \
  --search-summary-json artifacts/d5_master_field_quotient_001/data/search_summary.json \
  --m-list 5,7,9,11,13 \
  --out artifacts/d5_master_field_quotient_001/data/validation_summary.json \
  --no-rich
```

## Packaging
```bash
tar -czf artifacts/d5_master_field_quotient_001.tar.gz artifacts/d5_master_field_quotient_001
```
