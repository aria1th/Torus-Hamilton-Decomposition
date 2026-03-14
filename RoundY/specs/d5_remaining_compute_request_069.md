# D5 Remaining Compute Request 069

## Why this remains
The small support computations in 069 completed, but they deliberately stayed inside the frozen/support datasets. I did not rerun exhaustive raw branch generation for larger odd moduli.

## Narrow remaining task
Regenerate exhaustive active best-seed rows for odd `m = 13,15,...,41` (or as far as practical) and repeat:

1. full phase-corner / `tau` / `next_tau` exactness on all rows,
2. full `(B,beta)` injectivity and exact readout on all nonterminal rows,
3. exact marked-chain / cycle validation on the regular carry-jump reduction object,
4. accessible quotient extraction for the intended local/admissible class on that exact reduction object.

## Suggested envelope
- CPU: 16-32 workers
- RAM: 16-32 GB
- Expected wall time: 30-90 minutes if cached branch generation is available; longer if the raw generator must rebuild states from scratch
- Disk: 2-5 GB for cached row tables and quotient summaries

## Deliverables
- `analysis_summary.json`
- `full_phase_corner_extension.json`
- `full_B_beta_injectivity_extension.json`
- `marked_chain_cycle_extension.json`
- `accessible_quotient_extension.json`
