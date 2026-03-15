# D5 089 odd-m search screen example

This note records a small example script for using the current D5 odd-`m`
methodology as a compressed search/screening tool.

## Goal

The point is **not** to reopen a huge brute-force witness search.

The point is to take a candidate support family and ask:

1. does its first return already look theorem-friendly on odd `m`?
2. do clean frames survive?
3. which colors fail immediately?
4. which candidates deserve deeper symbolic work?

That is exactly the right use of the current D5 proof compression.

## Script

The example script is:

- `scripts/torus_nd_d5_odd_m_candidate_screen.py`

It accepts one or more support-based witness JSON files and screens them across
odd moduli.

## What it checks

For each witness, odd modulus `m`, and color `c`, the script computes:

1. the first-return permutation `R_c` on `P0={S=0}`;
2. cycle counts of `R_c`;
3. whether a clean frame exists via the translation criterion
   `R_c(x+k)=R_c(x)+k`;
4. a filtered count of candidate clean-frame directions.

This is a theorem-guided screen, not a final proof engine.

## Why this is a real compression

There are two different compressions here.

### 1. Candidate-space compression

Naively, a D5 rule on `m^5` vertices lives in a space of size roughly

- `(5!)^(m^5)`.

The screen never enters that space. It works on a support-family description,
so the search object is the finite rule family, not arbitrary vertexwise
direction tuples.

### 2. Verification compression

For a fixed candidate family of support length `L`, the main screening cost is

- `O(L * 5 * m^5)`

rule applications to build all five first-return maps.

The symmetry check is also compressed:

- naive clean-frame detection would scan all `(k,x)` pairs, which is
  `O(m^8)`;
- the script first filters candidate `k` using only `x=0`, then verifies only
  the survivors, giving
  `O(m^4 + r*m^4)`,
  where `r` is the number of filtered candidates, usually small.

So the screen does not solve D5 by itself, but it makes “odd-`m` family
diagnosis” dramatically cheaper than broad brute-force search.

## Example run

The saved example output is:

- `checks/d5_089_26_move_odd_m_screen.json`

produced by screening the fixed `26`-move witness on

- `m = 5,7,9,11`.

## How to use it

Example:

```bash
python scripts/torus_nd_d5_odd_m_candidate_screen.py \
  --witness-json RoundY/d5_m5_kempe_witness_26.json \
  --m-values 5 7 9 11 \
  --summary-out RoundY/checks/d5_089_26_move_odd_m_screen.json
```

## Intended use

This script is best used as a front-end filter:

1. propose a support family;
2. screen it on small odd moduli;
3. keep only candidates that preserve clean frames and strong cycle behavior;
4. do symbolic extraction only on survivors.

That is the correct “inverse use” of the current D5 odd-`m` proof method as a
search-space compressor.
