# D5 Researcher 2 Request 074

This note is the current handoff for the **symmetry / asymmetry** part of D5
after the `073` refinement.

## Context

The pre-`072` question “is the chain offset removable?” is no longer the right
top-level fork by itself.

What is now accepted:

- the coarse chain offset is removable at the bridge level
- the bare `m`-state `beta` bridge is too coarse for exact current `epsilon4`
- the surviving issue is not coarse offset, but the finite decoration needed
  near the splice / early post-carry region

`073` then sharpened this again:

- the static decorated bridge `(beta,a,b)` is exact on each chain
- but it is not splice-compatible as a deterministic global quotient

So the real symmetry question is now:

> is the remaining asymmetry merely a finite dynamic decoration on top of a
> symmetric global clock, or is there a deeper non-removable asymmetry in the
> splice dynamics?

## What is accepted

- Coarse bridge exists.
- Carry is rotatable at the coarse theorem-side level.
- Bare `beta` is not enough for exact `epsilon4`.
- Static chain decoration is not enough globally.

## Your target

Clarify the nature of the remaining asymmetry.

The strongest useful outcome would be one of:

1. a theorem-style statement that the only surviving asymmetry is a finite
   dynamic decoration attached to a global clock; or
2. a proof that even after allowing finite decoration, some deeper asymmetry
   remains and obstructs a canonical symmetric bridge.

In practice, likely subquestions are:

- can the splice dynamics be written in a more invariant gauge than the raw
  `(a,b)` chain labels?
- is there a canonical orbit / right-congruence interpretation of the
  decoration?
- is the decoration best read as future-word state, boundary memory, or some
  invariant parity/class?

## What to avoid

- do not spend time re-proving the coarse offset obstruction from `071`
- do not assume the static chain type is already the final symmetry object
- do not broaden this into a generic local-rule impossibility program

## Useful starting points

- `RoundY/theorem/d5_071_unified_bridge_handoff.md`
- `RoundY/theorem/d5_072_context_sync_paragraph.md`
- `RoundY/theorem/d5_072_r2.md`
- `RoundY/theorem/d5_073.md`
- `RoundY/theorem/d5_073_r1.md`
- `RoundY/checks/d5_researcher2_decorated_symmetry_support_073.json`

## Deliverable

Please return:

- one markdown note named `d5_074_r2.md`

Optional:

- a tar file if you produce additional symmetry tables, normalized transition
  diagrams, or packaged derivations

The note should clearly state:

- what is symmetric
- what is not
- whether the remaining asymmetry is dynamic decoration or something deeper
- what theorem statement you think is the right final symmetry claim
