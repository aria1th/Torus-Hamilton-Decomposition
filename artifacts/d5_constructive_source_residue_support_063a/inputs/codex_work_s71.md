# Codex Work S71

Task: execute the optional narrow constructive support request
[inputs/d5_constructive_source_residue_optional_request_063.md](./d5_constructive_source_residue_optional_request_063.md).

Scope:

- do not reopen theorem-side `(B,tau,epsilon4)` searches
- only stress-test the explicit current-state `063` formulas on the extended
  `049/050` support range
- validate:
  - `tau` piecewise delta-formula
  - `next_tau` branchwise current-state formula
  - current formulas for `c` and `q`

Implementation:

- added validator
  [scripts/torus_nd_d5_constructive_source_residue_support.py](../../../scripts/torus_nd_d5_constructive_source_residue_support.py)
- reused the existing active-branch row builder from
  [scripts/torus_nd_d5_source_residue_refinement.py](../../../scripts/torus_nd_d5_source_residue_refinement.py)
- ran on `m=13,15,17,19` with `4` worker processes

Result:

- all requested checks are exact on the extended range
- no collisions
- no unexpected branch rows
- constructive route is stable through `m=19`

Artifact:

- [artifacts/d5_constructive_source_residue_support_063a/README.md](../README.md)
