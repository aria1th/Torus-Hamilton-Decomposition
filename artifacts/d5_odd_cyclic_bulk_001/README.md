# D5 Odd Cyclic Bulk 001

This artifact packages the restricted odd-`m` d=5 pilot search requested in `tmp/codex_job_report_routex_0.md`.

## Contents
- `scripts/`: exact code used for the search and validation
- `data/search_summary.json`: machine-readable search result
- `data/best_config.json`: best stage-1 fallback candidate
- `data/validation_summary.json`: exact validation of the selected candidate on `m=3,5,7`
- `logs/search.log`: plain-text search log
- `logs/validation.log`: plain-text validation log
- `traces/q_traces_m*.json`: representative `Q`-section traces for the selected candidate
- `summary.md`: short research report with status tags

## Reproduction
```bash
python scripts/torus_nd_d5_odd_cyclic_bulk_search.py \
  --stage1-m 3 \
  --later-m-list 5,7 \
  --top-k 50 \
  --random-samples 50000 \
  --random-seed 12345 \
  --layer0-family five_cycle \
  --jobs 8 \
  --out artifacts/d5_odd_cyclic_bulk_001/data/search_summary.json \
  --best-config-out artifacts/d5_odd_cyclic_bulk_001/data/best_config.json \
  --no-rich

python scripts/torus_nd_d5_odd_cyclic_bulk_validate.py \
  --config-json artifacts/d5_odd_cyclic_bulk_001/data/best_config.json \
  --m-list 3,5,7 \
  --out artifacts/d5_odd_cyclic_bulk_001/data/validation_summary.json \
  --trace-dir artifacts/d5_odd_cyclic_bulk_001/traces \
  --no-rich
```

## Packaging
```bash
tar -czf artifacts/d5_odd_cyclic_bulk_001.tar.gz artifacts/d5_odd_cyclic_bulk_001
```
