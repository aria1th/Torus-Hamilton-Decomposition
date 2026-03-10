# D5-THETA-AB-PHASE-ALIGN-001

Artifact bundle for the one-bit refinement search on `Theta_AB_plus_phase_align`.

Contents:
- `summary.md`: executor-facing report and branch recommendation.
- `data/search_summary.json`: raw CP-SAT search result and saved feasible fields.
- `data/validation_summary.json`: deterministic validation on `m=5,7,9,11,13`.
- `data/residual_conflict_summary.json`: residual nonzero-phase conflict analysis.
- `data/quotient_state_table.json`: full refined quotient state table.
- `data/rotation_orbits.json`: rotation-orbit table.
- `data/best_strict_collapse_field.json`: representative strict-collapse field.
- `data/best_clean_nonclock_field.json`: representative clean-but-nonclock field.
- `data/field_class_summary.json`: saved field classes.
- `logs/search.log`: search stdout/stderr.
- `logs/validation.log`: validator stdout/stderr.
- `logs/residual_conflict.log`: residual-conflict analysis stdout/stderr.
- `scripts/`: exact code used for the search and diagnostics.

Reproduce:

```bash
python scripts/torus_nd_d5_theta_ab_phase_align_search.py \
  --schemas joined_anchor_five_atom_phase_align \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --max-time-sec 60 \
  --workers 8 \
  --random-seed 20260310 \
  --solution-limit 5 \
  --out artifacts/d5_theta_ab_phase_align_001/data/search_summary.json \
  --state-table-out artifacts/d5_theta_ab_phase_align_001/data/quotient_state_table.json \
  --orbit-table-out artifacts/d5_theta_ab_phase_align_001/data/rotation_orbits.json \
  --no-rich

python scripts/torus_nd_d5_theta_ab_phase_align_validate.py \
  --search-summary-json artifacts/d5_theta_ab_phase_align_001/data/search_summary.json \
  --m-list 5,7,9,11,13 \
  --field-limit 10 \
  --out artifacts/d5_theta_ab_phase_align_001/data/validation_summary.json \
  --no-rich

python scripts/torus_nd_d5_theta_ab_phase_align_residual_conflict.py \
  --search-summary-json artifacts/d5_theta_ab_phase_align_001/data/search_summary.json \
  --validation-summary-json artifacts/d5_theta_ab_phase_align_001/data/validation_summary.json \
  --m-list 5,7,9,11,13 \
  --out artifacts/d5_theta_ab_phase_align_001/data/residual_conflict_summary.json \
  --no-rich
```
