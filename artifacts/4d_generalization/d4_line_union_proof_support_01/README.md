# D4 Line-Union Proof Support 01

## Goal

This bundle supports the line-union proof draft in

- `RoundX/d4_line_union_proof_note_draft.md`

under the assumption that the proof architecture is correct.

The bundle contains two new scripts:

- `torus_nd_line_union_search.py`
  - derives the line-union witness from the reduced 2-bit layer-2 family;
- `torus_nd_line_union_validate.py`
  - validates the fixed line-union witness with automatic mode switching:
    - exact full-Hamiltonicity checks on small `m`,
    - exact `R_c/T_c` formula checks on moderate `m`,
    - odometer-conjugacy checks on larger `m`,
    - proof-backed constant-time certificates on huge `m`.

Both scripts use Rich progress output when available, and both degrade cleanly
to plain-text output with `--no-rich`.

## Search Result

The reduced-family search was run on

`m = 3,4,5,...,20`

over the full `256` truth tables on the two bits

- `u = 1_{x0 != 0}`
- `v = 1_{x3 = 0}`

with layer `0`, layer `1`, and layers `>= 3` fixed.

Outcome:

- survivor count: `4`
- survivor codes:
  - `[0,1,2,3]`
  - `[1,0,3,2]`
  - `[2,3,0,1]`
  - `[3,2,1,0]`
- the survivors exactly equal the affine/Klein-four family
- the minimal-support survivor is `[1,0,3,2]`
- selected name: `line_union_gauge`
- selected support formula: `2m - 1`

So the search script recovers the line-union witness as the smallest-support
representative in the surviving affine orbit.

Runtime:

- `12.078s`

## Validation Result

The validator was run on

`m = 3,4,5,6,7,8,9,10,12,15,20,25,30,40,50,75,100,200,500,1000,2000,1000000,1000000000`

with automatic mode switching.

Observed mode split:

- exact full-Hamiltonicity:
  - `m = 3,4,5,6,7,8,9,10,12`
- exact `R_c/T_c` formula checks:
  - `m = 15,20,25,30`
- odometer-conjugacy checks:
  - `m = 40,50,75,100,200,500,1000,2000`
- proof-backed certificates:
  - `m = 1000000,1000000000`

Every tested value passed.

Selected timings:

- `m=30` formula mode: `3.649s`
- `m=1000` odometer mode: `4.110s`
- `m=2000` odometer mode: `16.949s`
- `m=1000000` certificate mode: effectively instantaneous

Total validation runtime:

- `28.845s`

## Optimization Notes

- The expensive part is not the full torus check; it is the exact
  `R_c/T_c` comparison, because `actual_T` is built from repeated `actual_R`
  calls.
- The large-`m` path is therefore split intentionally:
  - exact/formula modes are regression checks;
  - odometer/certificate modes are proof-backed stress-test modes.
- This mirrors the earlier Route E optimization: once the proof is accepted,
  the right scalable validation object is the nested-return odometer, not the
  raw orbit computation on `V`.

## Files

Search script:
- `../../../torus_nd_line_union_search.py`

Validation script:
- `../../../torus_nd_line_union_validate.py`

Candidate module:
- `../../../candidates/hyperplane_fusion_line_union_v1.py`

Dependency note:
- `../../../requirements-search.txt`

Search summary:
- `search_summary.json`

Search log:
- `search.log`

Validation summary:
- `validation_summary.json`

Validation log:
- `validation.log`

Representative `Q` traces:
- `traces/line_union_q_traces_m5.json`
- `traces/line_union_q_traces_m7.json`

## Reproduction

Search:

```bash
python torus_nd_line_union_search.py \
  --out artifacts/4d_generalization/d4_line_union_proof_support_01/search_summary.json
```

Validation:

```bash
python torus_nd_line_union_validate.py \
  --out artifacts/4d_generalization/d4_line_union_proof_support_01/validation_summary.json \
  --trace-dir artifacts/4d_generalization/d4_line_union_proof_support_01/traces
```
