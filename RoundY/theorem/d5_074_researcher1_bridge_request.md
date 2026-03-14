# D5 Researcher 1 Request 074

This note is the current handoff for the **bridge-dynamics** part of D5 after
the `073` refinement.

## Context

The current D5 picture should now be read as follows.

- The theorem package is close to stable in shape.
- The coarse bridge is no longer the main mystery:
  the per-chain marked-chain quotients already glue at the carry /
  distance-to-endpoint level.
- The bare `m`-state `beta` bridge is too coarse for current `epsilon4`.
- The static chain-decoration model `(beta,a,b)` is exact on each chain but
  `073` shows it is **not** a deterministic global quotient across splices.

So the live bridge question is no longer “does any bridge exist?” It is:

> what is the smallest **splice-compatible decorated bridge** on the accessible
> union of regular chains?

## What is accepted

Treat the following as current working facts.

- Per-chain exact marked-chain rule is understood.
- Coarse global bridge exists at carry / endpoint-distance level.
- Bare `beta` is not exact enough for current `epsilon4`.
- Static `(beta,a,b)` is not splice-compatible as a deterministic global
  quotient.

## Your target

Find the correct **dynamic / splice-compatible** decorated bridge.

That may mean one of the following.

- derive a deterministic update law for a refined decoration state across the
  wrap/splice;
- replace `(a,b)` by a smaller or more canonical right-congruence state;
- prove that any exact global bridge must remember a particular finite boundary
  state at splice.

The best outcome is a theorem-shape statement of the form:

> the smallest exact bridge is a quotient with state `(beta,delta)` where
> `delta` evolves by an explicit deterministic splice law and current
> `epsilon4` factors exactly through `(beta,delta)`.

## What to avoid

- do not reopen generic controller search
- do not treat the static `(a,b)` chain label as if it were already the final
  global object
- do not re-argue the theorem package unless the bridge proof genuinely needs a
  structural lemma

## Useful starting points

- `RoundY/theorem/d5_071_unified_bridge_handoff.md`
- `RoundY/theorem/d5_072_context_sync_paragraph.md`
- `RoundY/theorem/d5_073_r1.md`
- `RoundY/theorem/d5_073_decorated_exact_bridge_handoff.md`
- `artifacts/d5_bridge_compute_support_072/data/state_chain_union_quotients.json`
- `RoundY/checks/d5_073_r1_support.json`

## Deliverable

Please return:

- one markdown note named `d5_074_r1.md`

Optional:

- a tar file if you produce additional derived tables, scripts, or packaged
  transition summaries

The note should clearly separate:

- what is proved / argued
- what is only checked on saved data
- what exact bridge state you propose
- what remains open after your proposal
