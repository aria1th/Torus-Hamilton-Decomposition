# D5 Researcher 3 Request 074

This note is the current handoff for the **realization / clock descent** part
of D5 after the `073` refinement.

## Context

The realization route is conceptually much cleaner than before.

What is now accepted:

- the canonical clock is not the mystery object
- if a deterministic global quotient is exact for current `epsilon4`, then the
  short-corner detector and the canonical clock descend automatically by
  corner-time
- the bare `m`-state bridge is too coarse
- the likely correct bridge is a decorated bridge, but `073` shows the naive
  static `(beta,a,b)` version is not yet a deterministic global quotient across
  splices

So your job is no longer to invent a clock. It is:

> formulate the realization theorem against the **correct splice-compatible
> decorated bridge** and identify precisely what exactness and uniqueness
> hypotheses are still needed.

## What is accepted

- `070` conditional corner-time descent theorem is the right template.
- `073` already explains that the theorem should be read against a decorated
  bridge, not the bare bridge.
- Once the correct exact global quotient is fixed, the realization burden
  should be small.

## Your target

Produce the sharpest realization theorem you can for the post-`073` bridge.

The ideal outcome is a theorem of the form:

> let `Q` be a deterministic splice-compatible decorated bridge exact for
> current `epsilon4`; then the short corner is visible on `Q`, and the
> canonical clock descends uniquely by corner-time.

Important subquestions:

- what is the minimal exactness hypothesis?
- what componentwise / periodicity hypothesis is needed?
- is short-corner uniqueness automatic once the bridge is exact?
- how should the theorem be normalized if the final bridge is longer than one
  bare `m`-cycle?

## What to avoid

- do not assume the static chain-type `(a,b)` is already the final bridge
- do not spend time rediscovering the bridge state; treat that as Researcher 1
  and 4’s live target
- do not broaden this into a controller-design problem

## Useful starting points

- `RoundY/theorem/d5_corner_time_descent_theorem_20260314_070.md`
- `RoundY/theorem/d5_072_r3.md`
- `RoundY/theorem/d5_073_decorated_bridge_realization.md`
- `RoundY/theorem/d5_073_decorated_exact_bridge_handoff.md`
- `RoundY/theorem/d5_071_unified_bridge_handoff.md`

## Deliverable

Please return:

- one markdown note named `d5_074_r3.md`

Optional:

- a tar file if you produce packaged theorem snippets, diagrams, or companion
  examples

The note should clearly separate:

- the theorem statement you believe is correct now
- what is assumed
- what is automatic
- what still depends on the unresolved decorated bridge construction
