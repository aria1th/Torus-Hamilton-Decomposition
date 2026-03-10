# D5-MASTER-FIELD-JOIN-QUOTIENT-001

Artifact bundle for the joined-quotient free-anchor search on the d=5 master-field problem.

Contents:
- `summary.md`: executor-facing report with the branch decision.
- `data/search_summary.json`: raw search result and saved feasible fields.
- `data/validation_summary.json`: deterministic validator output on `m=5,7,9,11,13`.
- `data/quotient_state_table.json`: full `Theta_AB` state table with rotation-orbit metadata.
- `data/rotation_orbits.json`: compact rotation-orbit table for `Theta_AB`.
- `data/best_stable_field.json`: stable representative field from the search.
- `data/second_field.json`: additional sampled feasible field.
- `data/best_field_permutation_histogram.json`: local permutation histogram for the stable representative.
- `logs/search.log`: stdout/stderr from the joined search.
- `logs/validation.log`: stdout/stderr from the validator.
- `scripts/`: exact code used for the search and validation.

Reproduce:

```bash
python scripts/torus_nd_d5_join_quotient_search.py \
  --schemas joined_anchor_five_atom \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --max-time-sec 20 \
  --workers 8 \
  --random-seed 20260310 \
  --solution-limit 3 \
  --out artifacts/d5_join_quotient_001/data/search_summary.json \
  --state-table-out artifacts/d5_join_quotient_001/data/quotient_state_table.json \
  --orbit-table-out artifacts/d5_join_quotient_001/data/rotation_orbits.json \
  --no-rich

python scripts/torus_nd_d5_join_quotient_validate.py \
  --search-summary-json artifacts/d5_join_quotient_001/data/search_summary.json \
  --m-list 5,7,9,11,13 \
  --field-limit 5 \
  --out artifacts/d5_join_quotient_001/data/validation_summary.json \
  --no-rich
```
