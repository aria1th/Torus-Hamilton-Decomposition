# D4 Line-Union General Theorem Validation 01

## Scope

This bundle validates the finalized proof file

- `RoundX/d4_line_union_general_theorem_proof_final.tex`

against the existing line-union validator.

No new theorem-specific checker was required, because the finalized TeX uses
the same mathematical contract already implemented in

- `torus_nd_line_union_validate.py`

namely:

- the same line-union witness,
- the same first-return formulas `R_c`,
- the same second-return formulas `T_c`,
- the same odometer conjugacies.

So the right validation action was to run the existing proof-backed validator
against the finalized theorem, not to create a second near-duplicate script.

## Validation Run

The validator was run on

`m = 3,4,5,6,7,8,9,10,12,15,20,25,30,40,50,75,100,200,500,1000,2000,1000000,1000000000`

with automatic mode switching:

- exact full-Hamiltonicity:
  - `m = 3,4,5,6,7,8,9,10,12`
- exact `R_c/T_c` formula checks:
  - `m = 15,20,25,30`
- odometer-conjugacy checks:
  - `m = 40,50,75,100,200,500,1000,2000`
- proof-backed certificates:
  - `m = 1000000,1000000000`

Every tested value passed.

Runtime:

- total: `28.653s`
- `m=30` formula mode: `3.539s`
- `m=1000` odometer mode: `4.187s`
- `m=2000` odometer mode: `16.845s`

The candidate module also matched the intended reduced-code representative.

## Files

Final proof:
- `../../../RoundX/d4_line_union_general_theorem_proof_final.tex`

Validator:
- `../../../torus_nd_line_union_validate.py`

Candidate module:
- `../../../candidates/hyperplane_fusion_line_union_v1.py`

Validation summary:
- `validation_summary.json`

Validation log:
- `validation.log`

Representative `Q` traces:
- `traces/line_union_q_traces_m5.json`
- `traces/line_union_q_traces_m7.json`

## Reproduction

```bash
python torus_nd_line_union_validate.py \
  --out artifacts/4d_generalization/d4_line_union_general_theorem_validation_01/validation_summary.json \
  --trace-dir artifacts/4d_generalization/d4_line_union_general_theorem_validation_01/traces
```
