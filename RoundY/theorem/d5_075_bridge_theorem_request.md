# D5 Bridge Theorem Request 075

This request is for the active **bridge theorem** branch.

## Current context

The live bridge candidate is no longer:

- bare `beta`
- static `(beta,a,b)`

The best current candidate is the dynamic boundary-odometer bridge

`(beta,q,sigma)` or `(beta,delta)` with `delta = q + m sigma`.

This is supported on the checked frozen range and gives the first
splice-compatible exact quotient currently visible.

## Your target

Prove the bridge theorem uniformly from the D5 structure.

The best outcome would be a theorem package of the form:

1. the accessible regular union admits a boundary state
   `delta = q + m sigma`
2. successor is
   - inside a chain: `beta -> beta-1`, `delta` fixed
   - at splice: `beta=0 -> m-1`, `delta -> delta+1`
3. current `epsilon4` factors exactly through `(beta,delta)`
4. identify the accessible splice-invariant subset `A` of boundary states

## What is accepted

- coarse bridge exists
- bare `beta` is too coarse for `epsilon4`
- static decorated bridge is not deterministic globally
- checked data support the dynamic bridge

## What to avoid

- no controller-search framing
- no return to the old “does any bridge exist?” fork
- no treating checked support as if it were already uniform proof

## Deliverable

Please return:

- `d5_075_bridge.md`

Optional:

- `.tar` if you create extra proofs, diagrams, or packaged tables

Your note should separate:

- what is proved
- what still depends on checked support
- how the accessible subset `A` enters
