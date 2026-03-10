# Task: D5-THETA-AB-PHASE-ALIGN-001

## Executive Summary
- `[C]` The one-bit refinement `Theta_AB_plus_phase_align` is Latin-feasible. The search found `10` saved cyclic-equivariant fields.
- `[C]` The saved fields split into exactly two pilot classes:
  - strict-collapse fields `0..4`
  - clean-but-nonclock fields `5..9`
- `[F]` The strict-collapse class still reproduces the old law
  - `R_0(q,w,v,u) = (q+1,w,v+1,u)`
  on `m=5,7,9`, so `U_0` is still `m^2` fixed points with zero monodromy.
- `[C/F]` The clean-but-nonclock class does break the old collapse law, but only by losing strict q-clock immediately; it does not produce a usable `U_0`.
- `[F]` No saved field remains Latin on `m=11,13`.
- `[C/H]` Branch decision: `phase_align` is useful but insufficient. The next refinement should add one predecessor-tail nonzero-phase bit, not more anchor freedom.

## Quotient Size And Orbit Count
- Refined quotient:
  - `theta_plus(x) = (L(x), (s_c(x), phase_align_c(x))_{c in Z/5Z})`
  - `phase_align_c(x) = 1_{(x_{c+3}-x_{c+1}) mod m = 0}`
- State counts by modulus:
  - `m=5`: `3015`
  - `m=7`: `11497`
  - `m=9`: `18408`
  - `m=11`: `21348`
  - `m=13`: `22309`
- Union state count over `m=5,7,9,11,13`: `25117`
- Rotation orbit count: `5041`
- Rotation-orbit size histogram:
  - size `1`: `22`
  - size `5`: `5019`
- Pilot predecessor-pattern counts:
  - `m=5`: `3125`
  - `m=7`: `16657`
  - `m=9`: `52858`

Files:
- `data/quotient_state_table.json`
- `data/rotation_orbits.json`

## Search Constraints And Solver Status
- Search variables:
  - one anchor value `a(theta_plus) in {0,1,2,3,4}` per refined quotient state
- Reconstruction:
  - `Pi_theta(c) = a(rho^{-c} theta) + c mod 5`
- Hard constraints:
  - cyclic equivariance
  - outgoing Latin on every refined quotient state
  - incoming Latin on predecessor-pattern classes for `m=5,7,9`
- Soft preferences:
  - layer `0` prefers anchor `1`
  - layer `4+` prefers anchor `0`
- Solver:
  - OR-Tools CP-SAT `9.11.4210`
  - random seed `20260310`
  - worker count `8`
  - per-schema time budget `60s`
- Search outcome:
  - solver status: `OPTIMAL`
  - search runtime: `147.802s`
  - schema solve runtime: `56.047s`
  - optimal preference score: `13502`
  - saved feasible fields: `10`

## Best Latin-Feasible Fields Found
### Class A: strict-collapse fields `0..4`
- Representative file:
  - `data/best_strict_collapse_field.json`
- Pilot behavior on `m=5,7,9`:
  - Latin: yes
  - old collapse law: yes
  - clean frame: yes
  - strict clock: yes
  - `U_0` cycle count: `m^2`
  - `U_0` lengths: all `1`
  - monodromies: all `0`
  - full color cycle counts: `[m^3,m^3,m^3,m^3,m^3]`
- Stability behavior on `m=11,13`:
  - Latin: no
  - clean frame: no
  - strict clock: no
  - full color cycle counts:
    - `m=11`: `[828,828,828,828,828]`
    - `m=13`: typically `[1377,1377,1377,1377,1377]` up to one off-by-one split in some saved variants

So the strict-clock survivors are not improvements. They are still the old collapse on the pilot range, then they break before the stability range.

### Class B: clean-but-nonclock fields `5..9`
- Representative file:
  - `data/best_clean_nonclock_field.json`
- Pilot behavior on `m=5,7,9`:
  - Latin: yes
  - old collapse law: no
  - clean frame: yes
  - strict clock: no
  - `U_0`: undefined because the clock already fails
  - full color cycle counts: `[m^3,m^3,m^3,m^3,m^3]`
- Stability behavior on `m=11,13`:
  - Latin: no
  - clean frame: no
  - strict clock: no
  - full color cycle counts:
    - `m=11`: around `[1669..1673]` repeated by color
    - `m=13`: around `[2711..2727]` repeated by color

So `phase_align` can break the old collapse law, but only in the bad way: it destroys strict q-clock instead of producing nontrivial section dynamics.

Files:
- `data/field_class_summary.json`
- `data/best_strict_collapse_field.json`
- `data/best_clean_nonclock_field.json`

## Representative-Color Diagnostics
### Strict-collapse representative
| `m` | Latin | old collapse law | clean frame | strict clock | `U_0` cycle count | monodromies | full color cycle counts |
|---|---|---|---|---|---:|---|---|
| 5 | yes | yes | yes | yes | 25 | all `0` | `[125,125,125,125,125]` |
| 7 | yes | yes | yes | yes | 49 | all `0` | `[343,343,343,343,343]` |
| 9 | yes | yes | yes | yes | 81 | all `0` | `[729,729,729,729,729]` |
| 11 | no | no | no | no | 0 | `[]` | `[828,828,828,828,828]` |
| 13 | no | no | no | no | 0 | `[]` | `[1377,1377,1377,1377,1377]` |

### Clean-but-nonclock representative
| `m` | Latin | old collapse law | clean frame | strict clock | `U_0` cycle count | monodromies | full color cycle counts |
|---|---|---|---|---|---:|---|---|
| 5 | yes | no | yes | no | 0 | `[]` | `[125,125,125,125,125]` |
| 7 | yes | no | yes | no | 0 | `[]` | `[343,343,343,343,343]` |
| 9 | yes | no | yes | no | 0 | `[]` | `[729,729,729,729,729]` |
| 11 | no | no | no | no | 0 | `[]` | `[1673,1673,1673,1673,1673]` |
| 13 | no | no | no | no | 0 | `[]` | `[2727,2727,2727,2727,2727]` |

Validation runtime: `100.422s`.

## Residual Conflict On The Refined Quotient
- The refinement removes the aligned branch, but it still merges many nonzero phase classes.
- On the representative strict-collapse field, residual multi-`delta` state counts are:
  - `m=5`: `58`
  - `m=7`: `1829`
  - `m=9`: `5509`
  - `m=11`: `7387`
  - `m=13`: `8172`
- States with full nonzero support `{1,2,...,m-1}` are:
  - `m=5`: `0`
  - `m=7`: `28`
  - `m=9`: `228`
  - `m=11`: `492`
  - `m=13`: `701`

Canonical residual conflict:
- modulus `m=7`
- state `L=2|sig=00000`
- this single refined state supports every nonzero phase
  - `delta in {1,2,3,4,5,6}`
- explicit examples:
  - `delta=1`: `[3,1,0,2,3]`
  - `delta=6`: `[3,2,0,1,3]`

So even after splitting `delta=0` from `delta!=0`, the refined quotient still merges all nonzero tail phases in one local state family. That is the residual obstruction.

File:
- `data/residual_conflict_summary.json`

## Recommendation
- Do not stop at `phase_align`.
- Do not spend more effort on freer anchor values on this quotient.
- The next refinement should add one predecessor-tail nonzero-phase bit, i.e. a bit that separates at least one nonzero `delta` tail class inside `phase_align=0`.

Suggested next scripts:
- `scripts/torus_nd_d5_theta_ab_phase_align_tailbit_search.py`
- `scripts/torus_nd_d5_theta_ab_phase_align_tailbit_validate.py`
