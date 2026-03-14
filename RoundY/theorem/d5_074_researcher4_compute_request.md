# D5 Researcher 4 Request 074

This note is the current handoff for the **compute-support** part of D5 after
the `073` refinement.

## Context

The compute role is no longer broad search.

What is now accepted:

- per-chain marked-chain rule is settled enough
- coarse bridge is settled enough
- bare `m`-state `beta` bridge is too coarse for current `epsilon4`
- static decorated `(beta,a,b)` is exact on each chain but not deterministic
  globally across splices

So the live compute target is:

> identify and stress-test the smallest **splice-compatible decorated bridge**
> on the accessible union of regular chains.

## What to aim for

The best next compute outputs would be one or more of:

1. explicit splice transition graph for the decoration state
2. smallest candidate dynamic decorated quotient that is deterministic and
   exact for current `epsilon4`
3. exactness test for the short-corner detector on that quotient
4. extension of the decorated-bridge support beyond the frozen `m=5,7,9,11`
   range when feasible and safe
5. evidence that some smaller decorated quotient fails

The compute should support the theorem questions, not replace them.

## What to avoid

- no generic search
- no reopening old small-family controller scans
- no full-state brute force beyond safe memory/time limits
- no effort on bare `beta` except as a baseline obstruction

## Likely productive probes

- treat the splice step as the real source of missing state
- search over small dynamic decoration states attached to `beta`
- examine right-congruence / future-word equivalence classes of decorated chain
  prefixes
- test whether the next-decoration state is a function of a short boundary
  window rather than a full chain-static type

## Useful starting points

- `artifacts/d5_bridge_compute_support_072/README.md`
- `artifacts/d5_bridge_compute_support_072/data/state_chain_union_quotients.json`
- `artifacts/d5_bridge_compute_support_072/data/offset_normalization_checks.json`
- `artifacts/d5_bridge_compute_support_072/data/chain_type_formula_validation.json`
- `RoundY/theorem/d5_073_r1.md`
- `RoundY/checks/d5_073_r1_support.json`
- `artifacts/d5_exact_reduction_support_068b/`

## Deliverable

Please return:

- one markdown note named `d5_074_r4.md`

Optional:

- a tar file if you generate saved data, scripts, logs, or a packaged artifact

The note should clearly include:

- scope of the compute
- exact candidate quotient(s) tested
- determinism status
- exactness status for current `epsilon4`
- exactness status for the short-corner detector
- first counterexamples if a candidate fails
