# 4D Generalization Trace

Date: `2026-03-08`

## Goal

Run one bounded scouting slice for the 4D generalization question:
- characterize the smallest low-layer template family;
- compare it to a time-bounded unrestricted exact search;
- leave reproducible artifacts and a short memo.

## Commands Run

### 1. Layer-template exhaustive search

```bash
python torus_nd_layer_template_search.py --dim 4 --m 3 --top-k 3 --workers 4 --chunk-size 512 --out artifacts/4d_generalization/layer_template_m3.json
python torus_nd_layer_template_search.py --dim 4 --m 4 --top-k 3 --workers 8 --chunk-size 2048 --out artifacts/4d_generalization/layer_template_m4.json
python torus_nd_layer_template_search.py --dim 4 --m 5 --top-k 5 --workers 8 --chunk-size 2048 --out artifacts/4d_generalization/layer_template_m5.json
python torus_nd_layer_template_search.py --dim 4 --m 6 --top-k 3 --workers 8 --chunk-size 2048 --out artifacts/4d_generalization/layer_template_m6.json
```

Observed runtimes:
- `m=3`: about `0.23s`
- `m=4`: about `8.28s`
- `m=5`: about `19.27s`
- `m=6`: about `40.66s`

Key outcome:
- no Hamilton hits in any of the four exhaustive searches;
- the same best template reappeared every time:
  - layer `S=0`: `(1,0,3,2)`
  - all other layers: `(0,1,2,3)`

Best cycle counts by `m`:
- `m=3`: `[9, 9, 9, 9]`
- `m=4`: `[16, 16, 16, 16]`
- `m=5`: `[25, 25, 25, 25]`
- `m=6`: `[36, 36, 36, 36]`

The induced `P0` return maps had the same cycle counts as the full color maps
in every one of those best-template cases.

### 2. Package the repeated best template as a candidate rule

```bash
python torus_nd_scan.py --dim 4 --m-list 3,4,5,6 --module candidates/layer0_swap01_swap23.py --function direction_tuple --out-dir artifacts/4d_generalization
```

Artifact:
- `artifacts/4d_generalization/d4_layer0_swap01_swap23_direction_tuple/summary.json`

Outcome:
- family status: `candidate_fail`
- all four runs are valid rules, all four fail Hamiltonicity

### 3. Exact search with incumbent retention

```bash
python torus_nd_exact_search.py --dim 4 --m 3 --time-limit-sec 120 --workers 8 --out artifacts/4d_generalization/exact_d4_m3_120s.json
```

Artifact:
- `artifacts/4d_generalization/exact_d4_m3_120s.json`

Observed outcome:
- status: `timeout`
- runtime: about `120.01s`
- iterations: `475`
- cuts: `5277`
- incumbent cycle counts: `[4, 1, 4, 4]`

Compact incumbent summary:
- distinct local tuples: `24`
- canonical vertices: `2`
- noncanonical vertices: `79`
- sign product: `-1`

### 4. One-slice affine search inside one active layer

```bash
python torus_nd_affine_low_layer_search.py --dim 4 --m 3 --top-k 5 --workers 8 --chunk-size 2048 --out artifacts/4d_generalization/affine_low_layer_m3.json
python torus_nd_affine_low_layer_search.py --dim 4 --m 4 --top-k 5 --workers 8 --chunk-size 4096 --out artifacts/4d_generalization/affine_low_layer_m4.json
python torus_nd_affine_low_layer_search.py --dim 4 --m 5 --top-k 5 --workers 8 --chunk-size 4096 --out artifacts/4d_generalization/affine_low_layer_m5.json
python torus_nd_affine_low_layer_search.py --dim 4 --m 6 --top-k 5 --workers 8 --chunk-size 4096 --out artifacts/4d_generalization/affine_low_layer_m6.json
```

Observed runtimes:
- `m=3`: about `0.71s`
- `m=4`: about `3.93s`
- `m=5`: about `10.96s`
- `m=6`: about `25.80s`

Key outcome:
- no Hamilton hits;
- the same best pattern appears for every tested `m`:
  - active layer `S=0`
  - default permutation `(1,0,3,2)`
  - affine form `x0+x2`
  - special permutation `(3,2,1,0)` on one residue class

Best cycle counts by `m`:
- `m=3`: `[3, 3, 3, 3]`
- `m=4`: `[4, 4, 4, 4]`
- `m=5`: `[5, 5, 5, 5]`
- `m=6`: `[6, 6, 6, 6]`

This is a strict improvement over the uniform layer family, which bottomed out
at `[m^2, m^2, m^2, m^2]`.

### 5. Package the affine-split rule and scan a broader range

```bash
python torus_nd_scan.py --dim 4 --m-list 3,4,5,6,7,8,10,12 --module candidates/layer0_x0plusx2_affine_split.py --function direction_tuple --out-dir artifacts/4d_generalization
```

Artifact:
- `artifacts/4d_generalization/d4_layer0_x0plusx2_affine_split_direction_tuple/summary.json`

Outcome:
- family status: `candidate_fail`
- but the cycle law remains exact on the scanned set:
  - full color maps: `[m, m, m, m]`
  - induced `P0` maps: `[m, m, m, m]`
  - sign product: `1`

### 6. Fixed-stripe refinement on the observed geometry

```bash
python torus_nd_affine_stripe_search.py --dim 4 --m 3 --active-layer 0 --form x0+x2 --top-k 5 --workers 8 --chunk-size 2048 --out artifacts/4d_generalization/affine_stripe_x0plusx2_layer0_m3.json
python torus_nd_affine_stripe_search.py --dim 4 --m 4 --active-layer 0 --form x0+x2 --top-k 5 --workers 8 --chunk-size 4096 --out artifacts/4d_generalization/affine_stripe_x0plusx2_layer0_m4.json
```

Observed outcome:
- no Hamilton hits for `m=3` or `m=4`;
- the best cycle counts remain `[m, m, m, m]`.

So the one-slice affine pattern already captures the best behavior visible in
this more flexible stripe family.

## Immediate Read

The trace separates two statements cleanly.

1. The theorem has not been disproved by this scouting pass.
2. The naive layer-uniform low-layer ansatz is a bad model for the 4D problem.
3. A specific affine-split low-layer rule is a real structural lead: it
   produces exactly `m` cycles per color across all tested `m`.

That is the main value of this trace: it rules out one easy generalization path
and isolates the next mathematical target, namely a bounded splice that would
merge those `m` cycles.
