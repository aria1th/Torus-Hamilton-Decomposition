# D4 Hyperplane Fusion 01

## Overview

This bundle records the outcome of the restricted-family search requested in
`RoundX/codex_job_request.md` under Task ID `D4-HYPERPLANE-FUSION-01`.

The searched family was:

- `d = 4`;
- outside low layers `S in {0,1,2}`, keep the affine-split baseline;
- inside low layers, assign one permutation in `S_4` to each realized local
  pattern
  `(S, x0=0, x1=0, x2=0, x3=0, q=0)` with `q = x0 + x2 mod m`;
- use one shared table across all searched `m`.

The normalized pattern space has `49` realized low-layer rows for all `m >= 3`.

## Symmetry Reductions

- Hyperplane residues were translation-normalized to `x_i = 0`.
- The `q` trigger was normalized to `x0 + x2 = 0`.
- A single common row table was constrained across all searched `m`, rather
  than allowing an `m`-dependent table.
- Outside the low layers, the rule was fixed rather than searched.

## Search Result

The CP-SAT row-table search found a Hamilton witness simultaneously for
`m = 3,4,5,6`.

Search artifact:
- `search_result.json`

Raw solver log:
- `search.log`

Search statistics:
- status: `hamilton_witness`
- runtime: about `1.97s`
- iterations: `3`
- subtour cuts: `198`

Cycle statistics on the search range:

| `m` | full color cycles | `P0` return cycles | sign product |
| --- | --- | --- | --- |
| `3` | `[1,1,1,1]` | `[1,1,1,1]` | `+1` |
| `4` | `[1,1,1,1]` | `[1,1,1,1]` | `+1` |
| `5` | `[1,1,1,1]` | `[1,1,1,1]` | `+1` |
| `6` | `[1,1,1,1]` | `[1,1,1,1]` | `+1` |

Matched hyperplane first-return maps `A_c = {x_c = 0}` are also single cycles
for `m = 3,4,5,6`, but their return times are not uniform, so this bundle does
not yet claim a simple odometer closed form for those first returns.

## Compact Candidate

The discovered rule uses only `17` noncanonical row types out of the `49`
realized rows.

Compact module:
- `../../../candidates/hyperplane_fusion_low_layers_v1.py`

Canonical table JSON:
- `candidate_table.json`

Noncanonical rows only:
- `noncanonical_rows.json`

Concise rule description:

1. `S = 0`: use the affine-split pair
   - `q = 0` -> `(3,2,1,0)`
   - `q != 0` -> `(1,0,3,2)`
2. `S = 1`: canonical `(0,1,2,3)`
3. `S = 2`: canonical except for four `q = 0` pattern rows
4. `S >= 3`: canonical `(0,1,2,3)`

The defect support is supported only on layers `0` and `2`.
Empirically, the defect count is

`m^3 + m^2 - m + 1 = m^3 + (m^2 - m + 1)`,

with:

- layer `0` contribution: `m^3`
- layer `2` contribution: `m^2 - m + 1`

## Validation Extension

The compact module was scanned directly on
`m = 3,4,5,6,7,8,9,10,11,12,13,14,15`.

Validation artifact directory:
- `../d4_hyperplane_fusion_low_layers_v1_direction_tuple/`

Summary:
- every tested `m` is `candidate_pass`
- every tested `m` has `all_hamilton = true`
- every tested `m` has sign product `+1`

This is computational evidence only, not a proof for all `m`.

## Reproduction

Search:

```bash
python torus_nd_hyperplane_fusion_search.py \
  --m-list 3,4,5,6 \
  --time-limit-sec 600 \
  --workers 8 \
  --out artifacts/4d_generalization/d4_hyperplane_fusion_01/search_result.json
```

Broader validation scan:

```bash
python torus_nd_scan.py \
  --dim 4 \
  --m-list 3,4,5,6,7,8,9,10,11,12,13,14,15 \
  --module candidates/hyperplane_fusion_low_layers_v1.py \
  --function direction_tuple \
  --out-dir artifacts/4d_generalization
```

## Recommended Next Step

The search goal changed from "find any compatible table" to "explain the
layer-2 patch."

The next proof-oriented task should be:

- derive a conceptual description of the four exceptional `S = 2, q = 0`
  pattern rows;
- prove that this finite patch splices the affine-split `m`-cycle law into a
  single cycle;
- extract a closed-form first-return or second-return model for the repaired
  rule.
