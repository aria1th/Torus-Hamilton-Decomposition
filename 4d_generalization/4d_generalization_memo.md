# 4D Generalization Memo

## Purpose

This note records the first scouting pass aimed at two questions:

1. Is there an immediate small-`m` counterexample signal in dimension `4`?
2. Does the simplest "Claude-style" low-layer pattern already generalize?

The goal here is not proof. It is to decide which computational signals are
strong enough to justify a theorem-seeking proof program.

## What was implemented

- `torus_nd_exact_search.py` now preserves the last incumbent on timeout as
  `incumbent_direction_tuples`, so partial exact-search progress can be
  analyzed rather than discarded.
- `torus_nd_layer_template_search.py` exhaustively searches the narrow family:
  canonical bulk, and one uniform permutation assigned to each selected layer
  residue `S mod m`.
- `candidates/layer0_swap01_swap23.py` packages the repeated best simple
  template found by the search.

## Results

### A. Exact search at `d=4, m=3`

Artifact:
- `artifacts/4d_generalization/exact_d4_m3_120s.json`

Outcome:
- status: `timeout`
- runtime: about `120.0s`
- iterations: `475`
- subtour cuts added: `5277`
- incumbent cycle counts: `[4, 1, 4, 4]`

Interpretation:
- the unrestricted exact search did not find a Hamilton decomposition in this
  budget, but it did find a much stronger incumbent than the simple template
  family;
- one color is already Hamiltonian, while the other three remain at four
  cycles each.

Structural summary of the incumbent:
- `24` distinct local direction tuples appear;
- only `2` of the `81` vertices remain canonical;
- `79` vertices are modified;
- because `m=3`, every vertex lies in a low residue layer, so "low-layer only"
  is vacuous here.

This is important because it shows the unrestricted search is already using
substantial coordinate-dependent structure, not a one-per-layer rule.

### B. Exhaustive search in the simplest layer-template family

Artifacts:
- `artifacts/4d_generalization/layer_template_m3.json`
- `artifacts/4d_generalization/layer_template_m4.json`
- `artifacts/4d_generalization/layer_template_m5.json`
- `artifacts/4d_generalization/layer_template_m6.json`

Family searched:
- bulk tuple `(0,1,2,3)`;
- selected residues `S in {0,1,2,3}`;
- each active residue gets a single permutation used uniformly on that whole
  residue layer.

Exhaustive result:

| `m` | templates checked | best full cycle counts | best `P0` cycle counts | Hamilton hits |
| --- | ---: | --- | --- | ---: |
| `3` | `24^3 = 13824` | `[9, 9, 9, 9]` | `[9, 9, 9, 9]` | `0` |
| `4` | `24^4 = 331776` | `[16, 16, 16, 16]` | `[16, 16, 16, 16]` | `0` |
| `5` | `24^4 = 331776` | `[25, 25, 25, 25]` | `[25, 25, 25, 25]` | `0` |
| `6` | `24^4 = 331776` | `[36, 36, 36, 36]` | `[36, 36, 36, 36]` | `0` |

The repeated best template is the same in every tested case:
- use `(1,0,3,2)` on residue layer `S = 0`;
- keep the canonical tuple on all other layers.

That template is now recorded as:
- `candidates/layer0_swap01_swap23.py`

Its scan summary is:
- `artifacts/4d_generalization/d4_layer0_swap01_swap23_direction_tuple/summary.json`

The failure is rigid:
- each color still has exactly `m^2` cycles;
- each induced `P0` map also has exactly `m^2` cycles;
- no odd/even improvement appears in this family;
- the best family member only modifies one residue layer, with defect size
  exactly `m^3`.

### C. One-slice affine refinement inside the active layer

Artifacts:
- `artifacts/4d_generalization/affine_low_layer_m3.json`
- `artifacts/4d_generalization/affine_low_layer_m4.json`
- `artifacts/4d_generalization/affine_low_layer_m5.json`
- `artifacts/4d_generalization/affine_low_layer_m6.json`

Family searched:
- canonical bulk outside one active low layer;
- on that active layer, a default permutation `p_default`;
- on one affine slice `L(v) = r (mod m)` inside the layer, a special
  permutation `p_special`.

Best result found:
- active layer `S = 0`;
- default permutation `(1,0,3,2)`;
- affine form `x0 + x2`;
- special permutation `(3,2,1,0)`;
- the residue choice is translation-equivalent and does not affect the cycle
  counts in the tested cases.

Observed cycle law:

| `m` | best full cycle counts | best `P0` cycle counts | Hamilton hits |
| --- | --- | --- | ---: |
| `3` | `[3, 3, 3, 3]` | `[3, 3, 3, 3]` | `0` |
| `4` | `[4, 4, 4, 4]` | `[4, 4, 4, 4]` | `0` |
| `5` | `[5, 5, 5, 5]` | `[5, 5, 5, 5]` | `0` |
| `6` | `[6, 6, 6, 6]` | `[6, 6, 6, 6]` | `0` |

This is the first robust structured signal in dimension `4`. The family still
fails Hamiltonicity, but it compresses the cycle count all the way from `m^2`
to exactly `m` for every color and for the induced `P0` maps.

That repeated best candidate is now packaged as:
- `candidates/layer0_x0plusx2_affine_split.py`

and scanned directly in:
- `artifacts/4d_generalization/d4_layer0_x0plusx2_affine_split_direction_tuple/summary.json`

That fixed candidate keeps the same cycle law on the larger scan set
`m = 3,4,5,6,7,8,10,12`.

### D. Fixed-stripe refinement on the observed geometry

Artifacts:
- `artifacts/4d_generalization/affine_stripe_x0plusx2_layer0_m3.json`
- `artifacts/4d_generalization/affine_stripe_x0plusx2_layer0_m4.json`

Family searched:
- keep the same active layer `S = 0` and affine form `x0 + x2`;
- allow a separate permutation for every residue class of `x0 + x2 (mod m)`.

Outcome:
- no Hamilton hits for `m=3` or `m=4`;
- the best cycle counts remain `[m, m, m, m]`.

So the affine-slice family already captures the best behavior visible in this
more flexible stripe refinement, at least in the smallest exact cases checked.

## Main conclusion

The current scouting pass now gives two clear answers.

- No theorem-level counterexample was found.
- The simplest low-layer uniform generalization fails decisively.
- A specific coordinate-conditional affine family on layer `S=0` produces the
  stable law "exactly `m` cycles per color" across odd and even `m`.
- The unrestricted exact search behaves differently again and already uses many
  local permutations, but the affine family is the first proof-shaped pattern.

This suggests a plausible theorem route:
- start from the affine-split candidate, which already reduces the problem to
  `m` cycles per color;
- then seek a bounded splice mechanism that merges those `m` cycles.

## Boundary

This is the point where new mathematics becomes the bottleneck.

The next natural step is no longer "search another small family." It is to
understand why the affine-split rule gives exactly `m` cycles, and whether a
finite splice can merge them. That is a genuine 4D proof-design question.

So this is the appropriate stopping point for purely automatic scouting.
