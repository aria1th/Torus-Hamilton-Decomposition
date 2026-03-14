# TorusD5 Lean Frontier Note

This note records the recommended role of Lean for the current `d=5`
frontier.

Current implementation status for the Lean support branch is tracked in:

- `D5_LEAN_PROGRESS.md`

For the current research-facing D5 frontier, read these first:

- `../RoundY/README.md`
- `../RoundY/current-frontier-and-approach.md`
- `../RoundY/theorem/d5_076_unified_handoff.md`
- `../RoundY/theorem/d5_077_globalization_handoff.md`
- `../RoundY/theorem/d5_077_live_questions_and_tracks.md`

## Current D5 frontier

The live D5 question is no longer the old `017/018/019` base-model problem.

The current accepted theorem-level picture is:

- the structural theorem package through the phase-corner machine is close to
  stable;
- the safest bridge object is the abstract right-congruence state `(beta,rho)`;
- the strongest checked concrete model is the dynamic boundary odometer
  `(beta,q,sigma)`, equivalently `(beta,delta)` with `delta = q + m sigma`;
- the remaining gap is globalization:
  does raw global `(beta,delta)` work on the full accessible union, or only
  componentwise?

So the D5 Lean branch should currently be treated as theorem/support
infrastructure, not as the main place where the globalization question is going
to be discovered.

## Current Lean status

The existing `TorusD5/` library is intentionally conservative.

It currently contains:

- `TorusD5/Basic.lean`
  extracted base coordinates and maps
- `TorusD5/FullCoordinates.lean`
  slice/full-coordinate interface
- `TorusD5/FirstReturn.lean`
  shifted first-return presentation support
- `TorusD5/GroupedReturn.lean`
  grouped-base iterate and period package
- `TorusD5/Cocycle.lean`
  symbolic cocycle accumulation layer
- `TorusD5/Specs.lean`
  theorem/specification interfaces for the extracted model

This branch does **not** yet formalize:

- the full witness rule,
- the full bridge theorem,
- the componentwise concrete `(beta,delta)` identification theorem,
- or the globalization question.

The current safe build target remains:

```bash
cd formal
source "$HOME/.elan/env"
lake build TorusD5
```

## Recommended role for Lean

Lean is a good fit for:

- fixing exact section, quotient, and bridge-interface definitions;
- keeping the extracted-model statements theorem-shaped and stable;
- packaging abstract deterministic-quotient hypotheses cleanly;
- checking that manuscript-level bridge and realization claims really match the
  accepted formal hypotheses once the theorem object is fixed;
- proving componentwise coordinate statements only after their mathematical
  formulation is stable.

Lean is not the right primary tool for:

- broad witness or controller search;
- discovering the globalization mechanism;
- prematurely hard-coding raw global `(beta,delta)` as theorem data before the
  component-tag question is settled;
- promoting unreviewed closed forms or ad hoc coordinates ahead of the current
  RoundY theorem language.

## Safe next Lean targets

The next safe D5 Lean work should stay one layer behind the research frontier:

1. keep the extracted-model and spec layer clean and buildable;
2. formalize abstract bridge / realization interfaces against a deterministic
   quotient `Q` and current-event exactness hypotheses;
3. if the concrete bridge stabilizes mathematically, add componentwise
   `(beta,q,sigma)` / `(beta,delta)` theorem interfaces;
4. only formalize a raw global `(beta,delta)` theorem after the globalization
   criterion is actually settled.

## What not to do

Do not start by formalizing all of `d=5`.

Do not start with a full Hamilton decomposition proof.

Do not turn the current Lean branch into a speculative search engine for new
coordinates or new controller families.

In particular, unless the theorem branch changes materially, there is no reason
to reopen the old plan of proving the full witness rule before the bridge
language itself is settled.
