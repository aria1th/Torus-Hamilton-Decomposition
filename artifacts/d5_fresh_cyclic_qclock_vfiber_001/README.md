# D5 Fresh Cyclic QClock VFiber 001

This artifact packages the reduced-state search requested by `tmp/d5_fresh_cyclic_family_codex_template.md`.

## Contents
- `scripts/`: the reduced family helper, searcher, and validator
- `data/search_summary.json`: full search output
- `data/frontier_candidates.json`: full nondominated pilot frontier
- `data/selected_candidate.json`: strongest single-cycle / zero-monodromy candidate
- `data/handoff_candidates.json`: six representative candidates used for the handoff validation pass
- `data/validation_summary.json`: exact cross-modulus validation for the handoff candidates
- `logs/search.log`: plain-text search log
- `logs/validation.log`: plain-text validation log
- `traces/`: saved `U`-orbit traces for the handoff candidates
- `summary.md`: research report with status tags and proof-skeleton notes

## Reproduction
```bash
python scripts/torus_nd_d5_fresh_cyclic_qclock_search.py \
  --phase1-m 5 \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --top-k 50 \
  --sample-count 50000 \
  --mutation-seed 20260310 \
  --max-clauses 2 \
  --jobs 8 \
  --out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/search_summary.json \
  --frontier-out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/frontier_candidates.json \
  --selected-out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/selected_candidate.json \
  --no-rich

python scripts/torus_nd_d5_fresh_cyclic_qclock_validate.py \
  --candidates-json artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/handoff_candidates.json \
  --m-list 5,7,9,11,13 \
  --full-check-m-list 5,7,9,11,13 \
  --full-check-colors 0,1,2,3,4 \
  --trace-limit 3 \
  --out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/validation_summary.json \
  --trace-dir artifacts/d5_fresh_cyclic_qclock_vfiber_001/traces \
  --no-rich
```

## Packaging
```bash
tar -czf artifacts/d5_fresh_cyclic_qclock_vfiber_001.tar.gz artifacts/d5_fresh_cyclic_qclock_vfiber_001
```
