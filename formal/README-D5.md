# TorusD5 Lean Frontier Note

This note records the recommended role of Lean for the current `d=5`
frontier after artifacts `017`, `018`, and `019`.

Current implementation status for the Lean preparation branch is tracked in:

- `D5_LEAN_PROGRESS.md`

## Current frontier

The latest `d=5` return-map artifacts are:

- `artifacts/d5_return_map_model_017/README.md`
- `artifacts/d5_mixed_skew_odometer_normal_form_018/README.md`
- `artifacts/d5_mixed_normal_form_and_u_obstruction_019/README.md`

Taken together, they say that for the canonical mixed witness `mixed_008`,
the old grouped-base signal from `017` has now been upgraded to an explicit
reduced return-map model.

On reduced first-return coordinates `(q,s,u,v)` with

\[
s = w + u,
\]

the exact model is:

\[
R(q,s,u,v)=\bigl(q+1,\ s+1+1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
\]

with

\[
dv(q,s)=1 \iff \bigl(q\neq m-2 \land s=1\bigr)\ \text{or}\ \bigl(q=m-2 \land s\neq 0\bigr).
\]

On grouped-return coordinates `(s,u,v)`, the exact model is:

\[
U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
\]

with grouped cocycle

\[
\phi(s)=2+1_{s=1}-2\,1_{s=2}-1_{s=3},
\]

cohomologous to the one-defect form

\[
-2\,1_{s=2}.
\]

The most important new exact conclusion from `019` is the obstruction
statement:

- grouped return is already canonical on `(s,v)`,
- each fixed-`u` grouped fiber is a single orbit on `(s,v)` for odd `m`,
- the only passive grouped coordinate is `u`,
- and the immediate reason is that every first return contains exactly one
  direction-4 move, so `du = 1` identically.

So the active bottleneck is no longer:

- find a mixed witness,
- find the grouped-return base geometry,
- or even guess the right cocycle.

The active bottleneck is now sharper:

- prove the explicit reduced model from the witness rule cleanly,
- prove the grouped-fiber orbit statement,
- and identify the smallest mechanism that breaks grouped `u`-invariance
  without destroying the reduced carry / skew-odometer structure.

## Recommended role for Lean

Lean should be used here as a proof/specification tool, not as the main search
engine.

Lean is a good fit for:

- fixing the exact section and coordinate definitions,
- proving the first-return and grouped-return formulas from the witness rule,
- packaging the semiconjugacy / quotient statement cleanly,
- proving the explicit cocycle formula and its gauge normalization,
- proving the grouped fixed-`u` fiber orbit theorem,
- isolating the exact grouped `u`-invariance obstruction,
- checking that manuscript-level statements really follow from the extracted
  and rule-derived formulas.

Lean is not the right primary tool for:

- broad witness search,
- exploratory grouped-return experimentation across many alternative
  observables,
- raw-data mining where Python already works well,
- initial perturbation search for grouped `u`-carry mechanisms.

So the right workflow is hybrid:

1. discover candidate formulas computationally,
2. prove the stable return-map statements in Lean,
3. prove the obstruction theorem in Lean,
4. feed only theorem-shaped perturbation candidates back into Lean.

## Scope for the first D5 Lean step

Do not start by formalizing all of `d=5`.

Do not start with a full Hamilton decomposition proof.

Start with the fixed witness `mixed_008` only, and only the explicit reduced
model extracted and explained in `017`/`018`/`019`.

That is the smallest formal target that is both:

- mathematically meaningful now,
- and directly reusable if a grouped `u`-carry mechanism is later found.

## Proposed first module targets

Suggested eventual module sketch:

- `formal/TorusD5/Basic.lean`
  - torus point model for `Fin 5 -> ZMod m`
  - fixed `mixed_008` witness rule
  - the section / return coordinates used in `019`
- `formal/TorusD5/FirstReturn.lean`
  - exact first-return map on `(q,s,u,v)`
  - proof of the carry law and `dv(q,s)`
- `formal/TorusD5/GroupedReturn.lean`
  - grouped return `U = R^m |_{q=0}`
  - proof that `U(s,u,v) = (s+1,u,v+\phi(s))`
  - grouped fixed-`u` fiber orbit theorem
- `formal/TorusD5/Cocycle.lean`
  - explicit cocycle `phi`
  - proof of the skew-product normal form
  - closed-form / cohomology lemmas for `phi`
- `formal/TorusD5/Obstruction.lean`
  - statement that grouped `u` is invariant
  - theorem that the exact remaining obstruction is absence of grouped
    `u`-carry

This mirrors the successful `d=4` pattern:

- explicit first return,
- grouped / second return,
- quotient/base model,
- then the obstruction theorem before any future lift theorem.

## Concrete proof targets

The first formal targets should be theorem-sized statements of the form:

1. first-return theorem on the chosen section:
   - `R(q,s,u,v) = (q+1, s+1+1_{q=m-2}, u+1, v+dv(q,s))`
2. grouped-return theorem:
   - `U(s,u,v) = (s+1, u, v+\phi(s))`
3. cocycle theorem:
   - `\phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3}`
   - and `\phi` is cohomologous to `-2*1_{s=2}`
4. grouped-return structural corollaries:
   - `u` is invariant,
   - each fixed-`u` fiber is a single grouped orbit on `(s,v)` for odd `m`
5. obstruction theorem:
   - the reduced model is already correct on `(s,v)`,
   - the exact remaining obstruction is absence of grouped `u`-carry

The right stopping point for the first serious pass is item 4.
That would already formalize the main positive result and the main obstruction
identified by `019`.

## What should stay computational for now

Keep these outside Lean until a clear theorem candidate emerges:

- exact table extraction from witness bundles,
- perturbation search for grouped `u`-carry,
- exploratory comparisons across control witnesses,
- experiments with smaller grouped returns,
- any broader local-family sweep.

In particular, the cycle-only, monodromy-only, and anti-compressive controls
should stay as computational comparison objects until there is a precise theorem
worth importing.

## Immediate next action

If Lean work starts now, the best first deliverable is:

- a minimal `TorusD5` scaffold,
- enough definitions to state the `mixed_008` reduced section coordinates,
- a theorem file whose target is exactly the first-return formula on
  `(q,s,u,v)`,
- followed by the grouped-return formula on `(s,u,v)`.

That formal target is still small, aligns with the present frontier, and will
force the right exact definitions before any attempt to formalize the
obstruction or search for grouped `u`-carry mechanisms.
