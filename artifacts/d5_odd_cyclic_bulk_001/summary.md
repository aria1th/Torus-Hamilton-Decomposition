# Task: D5-ODD-CYCLIC-BULK-001

## Question
Does the restricted odd-`m` d=5 cyclic-bulk family with a single `5`-cycle bulk and rotating zero-swap low-layer gates contain a Hamiltonian pilot witness, and if not, what return-map failure is visible on the best candidate?

## Results
- 탐색 범위: `d=5`, odd `m=3` stage-1 exact search, later exact validation on `m=5,7`
- 소요 시간: search `15.555s`, selected-candidate validation `0.324s`
- `[F]` Exhaustive single-gate family failed: all `31,944` configurations in the `24`-element layer-0 five-cycle family with at most one rotating zero-swap on each of layers `1,2,3` had `0` Hamiltonian colors at `m=3`.
- `[C]` Random widened family also failed: `39,336` unique sampled configurations with up to two rotating zero-swaps per layer had `0` Hamiltonian witnesses at `m=3`.
- `[C]` No candidate survived the later-`m` filter on `m=5,7`.

## Best Candidate
- Selected fallback candidate: `q0=42013|L1:none|L2:swap_1_4|L3:none`
- Config JSON: `data/best_config.json`
- Stage-1 cycle counts at `m=3`: `V=[6,9,3,6,5]`, `P0=[7,9,3,5,5]`, `Q=[3,9,3,5,1]`

## Observed Failure Pattern
- `[C]` The selected candidate does not show a 3-carry normal form signature on `m=5,7`.
- `[C]` The first-return `q`-shift is not uniform for any color except trivially degenerate cases. Example at `m=5`: the color-wise `q`-shift sets are `[[0,1,2,3,4],[1,3,4],[0,1,2,3,4],[0,1,2,3,4],[0,1,2,3,4]]`.
- `[C]` Second-return lengths on `Q` are non-uniform. Example at `m=7`: `[[1,2,4,6,9,12],[2,5,9,12],[1,3,4,5,6,7,8,9,10],[3,4,5,6,7,8,9,10,11],[3,4,6,7]]`.
- `[C]` This indicates the current low-layer family is not producing the desired `V -> P0 -> Q -> O3` pilot structure.

## Negative Conclusion
- `[F]` The restricted family `d5_odd_cyclic_bulk_rotating_zero_swaps_v1` is ruled out as a positive odd-`m` pilot family in the searched range.
- `[O]` Broader d=5 odd families remain open, especially families with richer layer-`2/3` gates or nontrivial section-dependent bulk corrections.

## Reproduce
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
