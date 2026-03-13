# D5 Constructive Source-Residue Support 063A

This artifact executes the optional narrow compute request
[inputs/d5_constructive_source_residue_optional_request_063.md](./inputs/d5_constructive_source_residue_optional_request_063.md).

It validates the explicit current-state constructive formulas proposed in
[inputs/d5_constructive_source_residue_route_063.md](./inputs/d5_constructive_source_residue_route_063.md)
on the extended `049/050` support range.

## Main result

On `m = 13,15,17,19`, all requested checks are exact:

- the explicit piecewise `tau` formula in
  `delta = rho - (s+u+v+layer) mod m`
- the branchwise `next_tau` current-state formula on
  `(s,u,layer,rho,epsilon4)`
- the current formulas for
  `c = 1_{rho = u + 1 + 1_{epsilon4=carry_jump}}`
  and
  `q ≡ u - rho + 1_{epsilon4=carry_jump} mod m`

There are:

- `0` tau-formula collisions
- `0` next-tau collisions
- `0` carry collisions
- `0` q-formula collisions
- `0` unexpected branch rows

So the constructive route through transported source residue is now explicitly
stable through `m=19` at the formula level, not just at the minimal-subset
exactness level from `049`.

## Files

- [data/analysis_summary.json](./data/analysis_summary.json):
  top-level exactness summary and yes/no stability verdict
- [data/constructive_source_residue_extension_checks_063a.json](./data/constructive_source_residue_extension_checks_063a.json):
  per-modulus check results
- [data/constructive_route_compression_063a.json](./data/constructive_route_compression_063a.json):
  compressed statement of the current-route formulas
- [data/first_collision_witnesses_063a.json](./data/first_collision_witnesses_063a.json):
  first collision witness if any formula failed
- [logs/summary.json](./logs/summary.json):
  duplicate run summary for quick inspection
- [inputs/d5_constructive_source_residue_optional_request_063.md](./inputs/d5_constructive_source_residue_optional_request_063.md):
  the request spec
- [inputs/d5_constructive_source_residue_route_063.md](./inputs/d5_constructive_source_residue_route_063.md):
  the source constructive note
- [inputs/codex_work_s71.md](./inputs/codex_work_s71.md):
  short execution note

## Execution

Validator:

- [scripts/torus_nd_d5_constructive_source_residue_support.py](../../scripts/torus_nd_d5_constructive_source_residue_support.py)

Command used:

```bash
PYTHONPATH=scripts python scripts/torus_nd_d5_constructive_source_residue_support.py \
  --out-dir artifacts/d5_constructive_source_residue_support_063a/data \
  --summary-out artifacts/d5_constructive_source_residue_support_063a/logs/summary.json \
  --m-values 13 15 17 19 \
  --jobs 4
```

Runtime on this machine: about `128s`.
