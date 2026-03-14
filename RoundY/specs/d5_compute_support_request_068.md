# D5 Compute Support Request 068

## Goal
Extend the exact reduction-object validation beyond the frozen small/full-row range and compute the accessible quotient for the intended local/admissible class on the extracted marked chain/cycle.

## Required repository state
A full repo checkout with the raw D5 branch generator and the current scripts that produced 037/045/047/059b/063a, not just the reading bundle.

## Requested tasks
1. Regenerate exhaustive active best-seed rows for odd moduli `m = 13,15,...,41` (or as far as practical).
2. Extract regular carry-jump marked chains `(source_u,w)` and test:
   - chain law `q=0..m-1`,
   - carry mark only at `q=m-1`,
   - endpoint splice to next `w`-slice,
   - whether quotienting successive slices gives a clean cycle statement.
3. Validate canonical clock support on those exhaustive rows:
   - `beta = -(q+s+v+layer) mod m`,
   - unit drift `beta' = beta - 1`,
   - exact readout of `q,c,epsilon4,tau,next_tau,next_B` from `(B,beta)`.
4. For the intended local/admissible class, compute the induced quotient on the extracted marked chain/cycle and record:
   - quotient size as a function of `m`,
   - whether the induced chain/cycle successor is deterministic,
   - whether carry readout is exact.

## Suggested compute envelope
- CPU: 16-32 workers
- RAM: 16-32 GB
- Expected wall time: 30-90 minutes for `m <= 41`, depending on whether raw row regeneration is cached
- Disk: 2-5 GB for cached row tables and quotient summaries

## Deliverables
- `analysis_summary.json`
- `marked_chain_validation.json`
- `beta_exactness_extension.json`
- `accessible_quotient_on_chain.json`
- a short README with per-modulus failures, if any

## Why this is the right next compute
The 067 handoff says compute should validate the exact reduction object and the canonical clock, not reopen generic search. The remaining unresolved support is exactly larger-modulus exhaustive validation of the chain/cycle object and the quotient induced by the intended class.
