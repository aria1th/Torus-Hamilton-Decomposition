# Task: D5-MASTER-FIELD-JOIN-QUOTIENT-001

## Executive Summary
- `[C]` The joined quotient `Theta_AB` is Latin-feasible: the free-anchor CP-SAT search found cyclic-equivariant Latin fields.
- `[C]` The best saved field is stable on `m=5,7,9,11,13`, and it preserves `clean_frame = True` and `strict_clock = True`.
- `[F]` Even on the joined quotient, the section return still collapses: for every tested odd modulus, `U_0` breaks into `m^2` fixed points and every monodromy is `0`.
- `[F]` The second saved feasible field is weaker: it matches the same degenerate behavior on `m=5,7,9` but loses Latin and clean frame on `m=11,13`.
- `[C/H]` Branch decision: `needs one extra flux bit`. Quotient enlargement from `A` and `B` to `Theta_AB` is not enough by itself.

## Exact Quotient Definition And Size Statistics
- Dimension `d = 5`.
- Layer bucket: `L(x) in {0,1,2,3,4+}`.
- Per-color relative coordinates:
  - `q_c = x_{c+1}`
  - `w_c = x_{c+2}`
  - `u_c = x_{c+4}`
- Joined signature atoms:
  1. `q_c = -1`
  2. `q_c + u_c = 1`
  3. `w_c + u_c = 2`
  4. `q_c + u_c = -1`
  5. `u_c = -1`
- State counts by modulus:
  - `m=5`: `2882`
  - `m=7`: `7609`
  - `m=9`: `8754`
  - `m=11`: `8899`
  - `m=13`: `8904`
- Union state count over `m=5,7,9,11,13`: `9427`.
- Rotation orbit count: `1899`.
- Rotation-orbit size histogram:
  - size `1`: `17`
  - size `5`: `1882`
- Pilot predecessor-pattern counts:
  - `m=5`: `3125`
  - `m=7`: `15774`
  - `m=9`: `34631`

Files:
- `data/quotient_state_table.json`
- `data/rotation_orbits.json`

## Search Constraints And Solver Status
- Search variables: one anchor value `a(theta) in {0,1,2,3,4}` per joined quotient state.
- Reconstructed field:
  - `Pi_theta(c) = a(rho^{-c} theta) + c mod 5`
- Hard constraints:
  - outgoing Latin on every joined quotient state
  - incoming Latin on predecessor-pattern classes for `m=5,7,9`
  - cyclic equivariance through the reconstruction formula
- Soft preferences:
  - layer `0` prefers anchor `1`
  - layer `4+` prefers anchor `0`
- Solver:
  - OR-Tools CP-SAT `9.11.4210`
  - random seed `20260310`
  - worker count `8`
  - per-schema time budget `20s`
- Search outcome:
  - solver status: `OPTIMAL`
  - total search runtime: `92.952s`
  - schema solve runtime: `33.266s`
  - optimal preference score: `4945`
  - saved feasible fields: `2`
  - composition: `1` optimal-preference field, `1` additional sampled feasible field

## Saved Feasible Fields
### Field 0: stable representative
- File: `data/best_stable_field.json`
- `[C]` Latin on every tested modulus `m=5,7,9,11,13`
- `[C]` `clean_frame = True`, `strict_clock = True` on every tested modulus
- `[F]` `U_0` has `m^2` cycles of length `1`
- `[F]` all monodromies are `0`
- `[F]` full color cycle counts are `[m^3, m^3, m^3, m^3, m^3]`

The stable field still collapses to a tiny local-permutation palette:
- permutation histogram:
  - `01234`: `6405`
  - `34012`: `1657`
  - `12340`: `1365`
- by layer:
  - layer `0`: all `12340`
  - layer `1`: all `34012`
  - layers `2,3,4+`: all `01234`

This is the same structural failure mode as before: the larger quotient remains Latin-compatible but still reduces the representative-color dynamics to a trivial section return.

### Field 1: unstable sampled field
- File: `data/second_field.json`
- `[C]` Latin, clean frame, and strict clock on `m=5,7,9`
- `[F]` fails Latin and clean frame on `m=11,13`
- `[F]` on the pilot range it has the same degenerate `U_0` and zero-monodromy behavior as Field 0

## Validation Table For `m=5,7,9,11,13`
### Field 0
| `m` | Latin | clean frame | strict clock | `U_0` cycle count | `U_0` lengths | monodromies | full color cycle counts |
|---|---|---|---|---:|---|---|---|
| 5 | yes | yes | yes | 25 | `[1,1,...,1]` | all `0` | `[125,125,125,125,125]` |
| 7 | yes | yes | yes | 49 | `[1,1,...,1]` | all `0` | `[343,343,343,343,343]` |
| 9 | yes | yes | yes | 81 | `[1,1,...,1]` | all `0` | `[729,729,729,729,729]` |
| 11 | yes | yes | yes | 121 | `[1,1,...,1]` | all `0` | `[1331,1331,1331,1331,1331]` |
| 13 | yes | yes | yes | 169 | `[1,1,...,1]` | all `0` | `[2197,2197,2197,2197,2197]` |

### Field 1
| `m` | Latin | clean frame | strict clock | `U_0` cycle count | monodromies | full color cycle counts |
|---|---|---|---|---:|---|---|
| 5 | yes | yes | yes | 25 | all `0` | `[125,125,125,125,125]` |
| 7 | yes | yes | yes | 49 | all `0` | `[343,343,343,343,343]` |
| 9 | yes | yes | yes | 81 | all `0` | `[729,729,729,729,729]` |
| 11 | no | no | no | 0 | `[]` | `[1331,1331,1331,1331,1331]` |
| 13 | no | no | no | 0 | `[]` | `[2197,2197,2197,2197,2197]` |

Validator runtime: `36.548s`.

## Branch Decision
- Decision: `needs one extra flux bit`.
- Reason:
  - `[C]` `Theta_AB` does solve the old Latin infeasibility.
  - `[F]` It does not solve the actual dynamical obstruction: the stable field still yields identity-like section return with `m^2` fixed points and zero monodromy.
  - `[H]` The next quotient enlargement should add exactly one predecessor-phase / flux bit, rather than spending more search effort on the current joined quotient.
