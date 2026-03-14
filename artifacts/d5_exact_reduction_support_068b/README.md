# D5 Exact Reduction Support 068B

This artifact packages the `068` compute-support extension for the current D5
clock-route / rigidity-route split.

The goal was not to reopen generic search. The goal was to validate the exact
reduction object and the canonical `beta` clock on regenerated active rows, as
far as practical without reckless OOM/time escalation.

## Result

The main result is:

- on the **full regenerated active-row range**
  `m = 13, 15, 17, 19, 21`,
  the safer first exact reduction object is a **marked length-`m` chain**
  extracted from regular carry-jump slices;
- on that same full-row range, the canonical clock
  `beta = -(q+s+v+layer) mod m`
  has exact unit drift and `(B,beta)` is exact for
  `q`, `c`, `epsilon4`, `tau`, `next_tau`, and `next_B`;
- on the same marked chains, small quotients such as `next_dn` and
  `dn + next_dn` still read the carry mark exactly, but deterministic quotients
  already force the full `m`-scale state;
- on the **branch-local extension range**
  `m = 31, 33, 35, 37, 39, 41`,
  the raw phase scheduler, universal targets, and beta drift remain exact.

So this materially strengthens the current `067/068` picture:

- theorem side:
  the marked-chain exact object is now supported beyond the tiny frozen range;
- clock route:
  the canonical beta clock is supported on regenerated full rows through
  `m = 21`;
- rigidity side:
  the first quotient diagnostics now stably separate
  "small exact carry readout" from
  "deterministic transport forces full `m`-scale state".

## Practical scope

The original `068` request asked for exhaustive larger-modulus support
potentially up to `m = 41`. In this environment, the full regenerated active
rows were pushed through `m = 21`, and the exact branch-local support was then
extended through `m = 41`.

That cap was deliberate:

- the full-row builder remains safe at this range;
- the runtime curve steepens sharply after `m = 21`;
- the theorem value is already strong once full rows reach `m = 21` and the
  branch-local exact support reaches `m = 41`.

So this artifact should be read as:

> exhaustive full-row support through `21`, plus exact branch-local extension
> through `41`.

## Files

- `data/analysis_summary.json`
  top-level result summary
- `data/marked_chain_validation.json`
  per-modulus chain validation on the regenerated full-row range
- `data/beta_exactness_extension.json`
  per-modulus exactness of beta drift and `(B,beta)` readouts
- `data/accessible_quotient_on_chain.json`
  first quotient diagnostics on the marked chains
- `data/branch_support_extension.json`
  branch-local exact support through `m = 41`
- `logs/summary.json`
  saved machine summary

## Main quantitative facts

On the full-row range:

- `m = 13`
  `20,436` active rows
- `m = 15`
  `38,010` active rows
- `m = 17`
  `65,008` active rows
- `m = 19`
  `104,310` active rows
- `m = 21`
  `159,180` active rows

Across all of those moduli:

- all regular carry-jump slices satisfy the marked length-`m` chain law;
- all chain endpoints splice correctly to the next `w`-slice;
- beta drift is exact on every nonterminal row;
- `(B,beta)` is exact for
  `q`, `c`, `epsilon4`, `tau`, `next_tau`, `next_B`;
- `next_dn` and `dn + next_dn` have quotient size `2`, read carry exactly, and
  are not deterministic;
- `B`, `B -> B_next`, and `B -> B_next -> B_next2` have quotient size `m`,
  read carry exactly, and are deterministic.

This is exactly the quotient split the current rigidity route wanted to see.

## Reproduction

Run:

```bash
PYTHONPATH=scripts python scripts/torus_nd_d5_exact_reduction_support_068.py \
  --out-dir artifacts/d5_exact_reduction_support_068b/data \
  --summary-out artifacts/d5_exact_reduction_support_068b/logs/summary.json \
  --jobs 1 \
  --full-m-values 13 15 17 19 21 \
  --branch-m-values 31 33 35 37 39 41
```

## Interpretation

The main mathematical takeaway is:

1. the safer first exact reduction object is a marked chain before a cycle;
2. the canonical beta clock is already exact on that object;
3. exact carry readout alone is cheap, but exact deterministic transport is
   not;
4. so the current D5 rigidity route is now better supported as a transport /
   injectivity story, not just a lower-bound story.
