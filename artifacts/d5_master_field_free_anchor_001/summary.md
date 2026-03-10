# Task: D5-MASTER-FIELD-FREE-ANCHOR-001

## Executive Summary
- `[C]` Relaxing the anchored color-0 requirement removes the immediate Latin obstruction: both quotient schemas admit cyclic-equivariant Latin fields.
- `[C]` In the searched slice, however, every feasible field still fails the representative-color dynamics:
  - one sampled field per schema has `clean_frame = True` but `strict_clock = False`;
  - the best strict-clock field per schema has `clean_frame = True` and `strict_clock = True`, but the section return `U_0` breaks into `m^2` fixed points and every monodromy is `0`.
- `[C]` So the free-anchor move solves coupling, but only by collapsing the return-map dynamics into a trivial regime.

## Exact Phase-Space Definition

### Schema A: `stable_anchor_two_atom`
- `theta(x) = (L(x), (s_0,\dots,s_4))`
- `L in {0,1,2,3,4+}`
- `s_c in {0,1,2,3}` from bits:
  - `q_c = -1`
  - `q_c + u_c = 1`
- union state count over `m=5,7,9,11,13`: `1005`

### Schema B: `unit_anchor_three_atom`
- `theta(x) = (L(x), (s_0,\dots,s_4))`
- `L in {0,1,2,3,4+}`
- `s_c in {0,\dots,7}` from bits:
  - `w_c + u_c = 2`
  - `q_c + u_c = -1`
  - `u_c = -1`
- union state count over `m=5,7,9,11,13`: `3805`

## Search Variable Definition
- searched variables: one anchor value `a(theta) in {0,1,2,3,4}` per quotient state
- reconstructed local field:
  - `Pi_theta(c) = a(rho^{-c} theta) + c mod 5`
- constraints:
  - outgoing Latin on every quotient state
  - incoming Latin on predecessor-pattern classes for `m=5,7,9`
  - cyclic equivariance via the reconstruction formula
- preferences:
  - layer `0` prefers anchor value `1`
  - layer `4+` prefers anchor value `0`

## Feasible Field Count
- `stable_anchor_two_atom`
  - optimal preference score: `456`
  - saved fields: `2`
  - composition: `1` optimal-preference field, `1` additional sampled feasible field
- `unit_anchor_three_atom`
  - optimal preference score: `1538`
  - saved fields: `2`
  - composition: `1` optimal-preference field, `1` additional sampled feasible field

This is not an exhaustive count of all feasible fields. It is the exact set saved under the capped optimal-plus-sample enumeration used here.

## Best Candidates And Diagnostics

### Strict-clock representatives

Files:
- `data/stable_anchor_two_atom_best_field.json`
- `data/unit_anchor_three_atom_best_field.json`

For both schemas, the best strict-clock field has the same qualitative behavior:

| `m` | `clean_frame` | `strict_clock` | `U_0` cycle count | `U_0` cycle lengths | monodromies | color cycle counts |
|---|---|---|---:|---|---|---|
| 5 | yes | yes | 25 | `[1,1,...,1]` | all `0` | `[125,125,125,125,125]` |
| 7 | yes | yes | 49 | `[1,1,...,1]` | all `0` | `[343,343,343,343,343]` |
| 9 | yes | yes | 81 | `[1,1,...,1]` | all `0` | `[729,729,729,729,729]` |
| 11 | yes | yes | 121 | `[1,1,...,1]` | all `0` | `[1331,1331,1331,1331,1331]` |
| 13 | yes | yes | 169 | `[1,1,...,1]` | all `0` | `[2197,2197,2197,2197,2197]` |

So these fields are Latin and have a clean first-return frame, but the section return is the opposite of what is needed: it is completely fractured, with zero monodromy.

### Non-clock representatives

The additional sampled feasible field in each schema has:
- `[C]` `clean_frame = True`
- `[F]` `strict_clock = False`
- `[F]` no defined `U_0` / monodromy diagnostic because the clock axis fails first

## Cross-Modulus Summary
- `[C]` The degeneration is stable across `m=5,7,9,11,13`.
- `[C]` No saved field in either schema produced:
  - a single-cycle `U_0`,
  - a nonzero unit monodromy,
  - or a Hamiltonian full color map on any tested modulus.

## Suggested No-Go Skeleton
- `[C/H]` Current evidence suggests a dichotomy on the present phase spaces:
  1. if the free-anchor Latin field preserves a clean frame but not a strict clock, then the return reduction stops immediately;
  2. if it preserves both clean frame and strict clock, then `U_0` collapses to the identity-like regime on the section, with monodromy `0`.
- `[O]` The next search should enlarge the quotient state space itself, not merely relax the anchor values on the old one.

## Reproduce
```bash
python scripts/torus_nd_d5_master_field_free_anchor_search.py \
  --schemas stable_anchor_two_atom,unit_anchor_three_atom \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --max-time-sec 20 \
  --workers 8 \
  --random-seed 20260310 \
  --solution-limit 3 \
  --out artifacts/d5_master_field_free_anchor_001/data/search_summary.json \
  --no-rich

python scripts/torus_nd_d5_master_field_free_anchor_validate.py \
  --search-summary-json artifacts/d5_master_field_free_anchor_001/data/search_summary.json \
  --m-list 5,7,9,11,13 \
  --field-limit 5 \
  --out artifacts/d5_master_field_free_anchor_001/data/validation_summary.json \
  --no-rich
```
