# Codex Work S72

Executed the `068` compute-support extension with a new extractor:

- `scripts/torus_nd_d5_exact_reduction_support_068.py`

Saved artifact:

- `artifacts/d5_exact_reduction_support_068b/`

Scope:

- exhaustive regenerated active rows on
  `m = 13, 15, 17, 19, 21`
- branch-local exact extension on
  `m = 31, 33, 35, 37, 39, 41`

Main outcome:

- the safer first exact reduction object remains a marked length-`m` chain;
- `(B,beta)` remains exact for
  `q`, `c`, `epsilon4`, `tau`, `next_tau`, `next_B`
  on the full regenerated range;
- the first quotient diagnostics cleanly separate
  small exact carry readout from deterministic transport, which already forces
  full `m`-scale state on the chain;
- larger branch-local support keeps the raw scheduler and beta drift exact
  through `m = 41`.
