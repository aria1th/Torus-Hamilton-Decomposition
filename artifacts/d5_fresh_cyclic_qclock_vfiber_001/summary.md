# Task: D5-FRESH-CYCLIC-QCLOCK-VFIBER-001

## Executive Summary
- `[C]` I searched a fresh d=5 odd-`m` cyclic family whose layer-`1,2,3` rules depend only on affine atoms in `(q,w,u)` and never on `v`.
- `[P/C]` In this family, `q`-clock and `v`-fiber are built in by construction. The reduced `(q,w,u)` model was then validated against the full five-color dynamics on `m=5,7,9,11,13`.
- `[F]` No candidate in the searched family achieved both:
  - single-cycle section return `U_c` on `m=5,7,9`, and
  - unit orbitwise monodromy on `m=5,7,9`.
- `[C]` The strongest surviving family splits into two clean classes:
  - a stable `U`-single-cycle / zero-monodromy / permutation class;
  - a stable unit-monodromy / fractured-`U` / indegree-defect class.

## Search Scope
- Phase 1 exact search: all `1,191,016 = 106^3` candidates in the one-clause, default-`0` subfamily at `m=5`.
- Phase 2 seeded mutation search: `30,840` unique candidates with up to two clauses per layer, mixed defaults, tested on `m=5,7,9`.
- Stability check: top frontier slice rechecked on `m=11,13`.
- Full reduced-vs-full verification: all five colors validated on `m=5,7,9,11,13` for the six handoff candidates.

## Best Candidates

### Class A: Single-cycle section return, zero monodromy, no indegree defect

These candidates satisfy:
- `[C]` clean frame for all colors,
- `[C]` `U_c` is a single cycle for `m=5,7,9,11,13`,
- `[C]` `R_c` is a permutation on the reduced state space,
- `[F]` monodromy is always `0`, so the `v`-fiber does not lift to a full `m^3`-cycle.

Representative rules:

1. `L1:d3 | L2:d2[q=-1->4; q+u=1->0] | L3:d4`
2. `L1:d4[q=0->3; q+w+u=-2->2] | L2:d0 | L3:d0`
3. `L1:d2[q=0->3; w+u=1->4] | L2:d2 | L3:d4`

Cross-modulus behavior for all three representatives:

| `m` | `U_c` cycle lengths | monodromy | `R_c` indegree histogram |
|---|---|---|---|
| 5 | `[25]` | `[0]` | `{1: 125}` |
| 7 | `[49]` | `[0]` | `{1: 343}` |
| 9 | `[81]` | `[0]` | `{1: 729}` |
| 11 | `[121]` | `[0]` | `{1: 1331}` |
| 13 | `[169]` | `[0]` | `{1: 2197}` |

### Class B: Unit monodromy, fractured section return, indegree defects

These candidates satisfy:
- `[C]` clean frame for all colors,
- `[C]` all `U`-cycle monodromies are units on `m=5,7,9,11,13`,
- `[F]` `U_c` is not a single cycle,
- `[F]` `R_c` has indegree defects.

Representative rules:

1. `L1:d4 | L2:d2[w+u=2->4; q+u=-1->3] | L3:d0[u=-1->3]`
2. `L1:d3[q=-2->0] | L2:d2[q+u=2->3; w+u=2->4] | L3:d3`
3. `L1:d3[q=2->2] | L2:d3 | L3:d0[q+w+u=1->3; w=1->4]`

Cross-modulus behavior:

| Candidate | `m=5` | `m=7` | `m=9` | `m=11` | `m=13` |
|---|---|---|---|---|---|
| Rule 1 | cycle `[11]`, mono `[1]`, indegree `{0:5,1:115,2:5}` | `[19]`, `[5]`, `{0:7,1:329,2:7}` | `[29]`, `[2]`, `{0:9,1:711,2:9}` | `[41]`, `[8]`, `{0:11,1:1309,2:11}` | `[55]`, `[3]`, `{0:13,1:2171,2:13}` |
| Rule 2 | `[13]`, `[2]`, `{0:5,1:115,2:5}` | `[25]`, `[3]`, `{0:7,1:329,2:7}` | `[41]`, `[4]`, `{0:9,1:711,2:9}` | `[61]`, `[5]`, `{0:11,1:1309,2:11}` | `[85]`, `[6]`, `{0:13,1:2171,2:13}` |
| Rule 3 | `[15]`, `[2]`, `{0:5,1:115,2:5}` | `[28]`, `[3]`, `{0:7,1:329,2:7}` | `[45]`, `[4]`, `{0:9,1:711,2:9}` | `[66]`, `[5]`, `{0:11,1:1309,2:11}` | `[91]`, `[6]`, `{0:13,1:2171,2:13}` |

## Per-color Validation
- `[C]` All reported families are rotationally covariant by construction, so all colors should be equivalent.
- `[C]` This was checked directly: for each of the six handoff candidates, the reduced `R` model matched the full first-return dynamics for colors `0,1,2,3,4` on every tested modulus `m=5,7,9,11,13`.
- Validation output: `data/validation_summary.json`.

## Minimal Counterexamples
- `[F]` Exact phase-1 failure already appears in the one-clause family:
  - best single-cycle candidates at `m=5` have objective `[1,1,0,-1,0,-3]` and monodromy `[0]`;
  - best unit-monodromy candidates at `m=5` have objective `[1,0,1,-1,-50,-3]` and `U` cycle length `[18]`.
- `[F]` For the strongest Class A representative, the minimal failure is immediate at `m=5`: the unique `U`-orbit has monodromy `0`.
- `[F]` For the strongest Class B representative, the minimal failure is also immediate at `m=5`: `U` has cycle length `11 < 25` and `R` indegree histogram `{0:5,1:115,2:5}`.

## Suggested Proof Skeleton
- `[C/H]` The strongest surviving Class A candidate suggests a proof pattern for a reduced theorem:
  1. `q` is a strict clock by design because only layer `0` uses offset `+1`.
  2. `v` is a clean fiber because layer supports depend only on `(q,w,u)`.
  3. `R_c` therefore reduces exactly to a map on `(q,w,u)` plus a cocycle in `v`.
  4. The section return `U_c` on `{q=0}` is a permutation with one `m^2`-cycle.
  5. The only missing ingredient for a full lift is a unit monodromy theorem; in the current family the cocycle sums to `0`.
- `[O]` The next family to try should preserve the same strict clock / clean fiber mechanism while forcing a nonzero `v`-cocycle on the unique `U`-orbit, ideally without breaking bijectivity of `R_c`.

## Reproduce
```bash
python scripts/torus_nd_d5_fresh_cyclic_qclock_search.py \
  --phase1-m 5 \
  --pilot-m-list 5,7,9 \
  --stability-m-list 11,13 \
  --top-k 50 \
  --sample-count 50000 \
  --mutation-seed 20260310 \
  --max-clauses 2 \
  --jobs 8 \
  --out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/search_summary.json \
  --frontier-out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/frontier_candidates.json \
  --selected-out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/selected_candidate.json \
  --no-rich

python scripts/torus_nd_d5_fresh_cyclic_qclock_validate.py \
  --candidates-json artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/handoff_candidates.json \
  --m-list 5,7,9,11,13 \
  --full-check-m-list 5,7,9,11,13 \
  --full-check-colors 0,1,2,3,4 \
  --trace-limit 3 \
  --out artifacts/d5_fresh_cyclic_qclock_vfiber_001/data/validation_summary.json \
  --trace-dir artifacts/d5_fresh_cyclic_qclock_vfiber_001/traces \
  --no-rich
```
