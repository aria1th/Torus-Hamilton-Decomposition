# D5 Compute Validation Request 075

This request is for the active **compute validation** branch.

## Current context

The compute role is now narrowly focused.

What is accepted:

- coarse bridge exists
- bare `beta` fails for current `epsilon4`
- static `(beta,a,b)` fails determinism globally
- dynamic `(beta,q,sigma)` is supported on the checked frozen range

The compute job is therefore not search. It is validation and falsification of
the dynamic bridge model.

## Your target

Validate or break the dynamic bridge

`(beta,q,sigma)` / `(beta,delta)`

with attention to:

- splice law
- current `epsilon4` exactness
- short-corner exactness
- accessible subset `A`
- possible smaller exact factors

The most useful outcomes are:

1. extension of support beyond the frozen checked range
2. clarification of the accessible subset
3. first real counterexample if the model fails
4. evidence that no smaller deterministic exact quotient survives

## What to avoid

- no broad controller search
- no reopening old small-family scans
- no dangerous full-state jobs without a clear reduction target

## Deliverable

Please return:

- `d5_075_compute.md`

Optional:

- `.tar` if you generate packaged data, scripts, logs, or an artifact

Your note should clearly include:

- scope
- data source
- candidate quotient(s) tested
- determinism result
- exactness result for `epsilon4`
- exactness result for short-corner
- first failure witness if something breaks
