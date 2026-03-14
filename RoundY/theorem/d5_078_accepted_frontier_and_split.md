# D5 Accepted Frontier And Split 078

This note records the accepted post-`077` frontier for odd `m` in `d=5`.

It is the current compact statement of:

- what is now accepted,
- what is still open,
- what the next jobs are,
- what each active researcher should focus on,
- and what each one should hand back.

## 1. What is now accepted

The following should now be treated as accepted working context.

### 1.1 Structural theorem package

The theorem package through the phase-corner machine is no longer the main live
frontier.

Accepted shape:

- the active regular dynamics are organized by the phase clock `beta`;
- countdown/reset behavior is controlled by the phase-corner scheduler;
- per-chain dynamics are exact marked length-`m` chains.

### 1.2 Safe global theorem object

The accepted safe theorem object is the abstract exact bridge

`(beta,rho)`,

where `rho` is the boundary right-congruence class of the padded future current
event word.

This is the bridge that is currently safe to state globally.

### 1.3 Abstract realization theorem

The accepted realization picture is:

- on `(beta,rho)`, the clock already descends as the first coordinate;
- the short-corner detector descends automatically;
- recurrence is needed only for the corner-time characterization.

### 1.4 Concrete componentwise bridge

The accepted strongest concrete model is

`(beta,q,sigma)`,

equivalently

`(beta,delta)` with `delta = q + m sigma`.

Accepted componentwise package:

- uniform splice law,
- uniform current-event readout,
- orbit-segment description of the component boundary image.

### 1.5 What `077` adds

The accepted `077` reduction is:

- componentwise bridge identification is no longer the issue;
- repeated fixed-`delta` ambiguity is no longer a local event-law issue;
- the only remaining possible ambiguity at fixed `delta` is **tail length** /
  terminal distance;
- on the actual frozen regular union for `m=7,9,11`, the observed data glue to
  one odometer successor with no conflicting observed future-prefixes.

So the old “find the bridge” frontier is over.

## 2. Current live question

The current D5 question is now:

> does raw global `(beta,delta)` work without a component tag?

Equivalent form:

> can the same realized `delta` occur in different accessible components with
> different padded future current-event words?

By the accepted `077` Track B reduction, this is now equivalent to:

> at fixed realized `delta`, can the remaining full-chain tail length vary
> across accessible components?

So the globalization problem is now a **component-geometry / tail-length**
problem, not a local bridge-readout problem.

## 3. What is still open

Three specific things remain open.

### 3.1 True global component structure

We still do not have the actual splice-connected decomposition of the accessible
regular union in theorem form.

### 3.2 Globalization criterion

We still do not know whether

`rho = rho(delta)`

on the full accessible union.

### 3.3 Larger actual-union evidence

We still do not have the decisive larger-modulus actual-union object:

- raw row-level successor tables, or
- a chain-level splice graph, or
- explicit component IDs

for the regenerated regular union on `m=13,15,17,19,21`.

## 4. Next jobs

There are now exactly three active jobs.

### Job A: Global component structure

Main question:

- what are the true splice-connected accessible regular components?

Best route:

- identify the actual exit-to-entry splice map through the patched region;
- determine whether the source-family windows are genuine components or
  overlapping charts on one larger component;
- pay special attention to the exceptional sector and the `u -> u-3` arithmetic
  suggested by the accepted `077` Track A note.

Success criterion:

- a theorem or explicit structural argument describing the actual components.

### Job B: Globalization criterion / tail-length theorem

Main question:

- does fixed `delta` determine the padded future word globally?

Best route:

- use the accepted Track B reduction:
  fixed-`delta` ambiguity is equivalent to tail-length ambiguity;
- therefore do not re-open local event-law analysis;
- instead connect the tail-length criterion directly to the component structure
  from Job A.

Success criterion:

- either a proof that tail length is constant at fixed realized `delta`,
  implying raw global `(beta,delta)`;
- or a proof / counterexample showing two realizations of the same `delta` with
  different tail lengths, forcing the final global theorem to remain abstract as
  `(beta,rho)`.

### Job C: Compute support for actual unions

Main question:

- what do the true regenerated regular unions do beyond the frozen `m <= 11`
  range?

Best route:

- no broad search;
- extract the smallest concrete objects that decide the globalization question:
  row-level successor tables, chain-level splice graphs, or explicit component
  IDs on `m=13,15,17,19,21`;
- if those are too large, produce compact exports:
  per regular source, the realized `delta` interval, endpoint successor target,
  and overlap / component information.

Success criterion:

- a direct actual-union test of whether repeated realized `delta` values carry
  the same future words or only tail-length differences.

## 5. Researcher focus

### Researcher A

Focus:

- global component structure
- patched exit-to-entry splice map
- exceptional-sector continuation

Do not spend time on:

- local bridge readout
- abstract realization theorem
- new controller families

Hand over:

- a markdown note with theorem-style component conclusions,
- and, if helpful, a compact diagram/table of the splice map.

Suggested filename:

- `d5_078_rA.md`

### Researcher B

Focus:

- globalization criterion
- tail-length reduction
- proof that `rho = rho(delta)` or proof that it fails

Do not spend time on:

- rediscovering `(beta,delta)` locally
- proxy-only ambiguity unless it informs the true criterion

Hand over:

- a markdown note with the theorem/counterexample structure,
- and a clean final statement of the strongest safe global bridge theorem.

Suggested filename:

- `d5_078_rB.md`

### Researcher C

Focus:

- actual-union compute on `m=13,15,17,19,21`
- chain-level splice graph / component IDs / successor tables
- compact exports useful to A and B

Do not spend time on:

- broad search
- speculative new bridge families

Hand over:

- a markdown summary,
- JSON/CSV/tar only if needed,
- and at least one compact reusable export, not only prose.

Suggested filenames:

- `d5_078_rC.md`
- optional `d5_078_rC_artifacts.tar.gz`

## 6. What to hand over to new collaborators

The shortest current handoff set is:

1. `RoundY/theorem/d5_078_accepted_frontier_and_split.md`
2. `RoundY/theorem/d5_077_globalization_handoff.md`
3. `RoundY/theorem/d5_077_live_questions_and_tracks.md`
4. `tmp/d5_076_bridge_main.md`
5. `tmp/d5_076_realization_trackB.md`
6. `tmp/d5_076_concrete_bridge_proof.md`
7. `tmp/077_d5_trackB_tail_length_reduction.md`
8. `tmp/d5_077_trackC_actual_union_check_20260314.md`

Then add only the smallest needed support files:

- `RoundY/checks/d5_077_compact_interval_summary.json`
- `artifacts/d5_exact_reduction_support_068b/data/marked_chain_validation.json`
- `artifacts/d5_exact_reduction_support_068b/data/accessible_quotient_on_chain.json`
- `artifacts/d5_exact_reduction_support_068b/data/branch_support_extension.json`
- `artifacts/d5_phase_scheduler_branch_support_059b/data/large_range_branch_validation.json`
- `artifacts/d5_phase_scheduler_branch_support_059b/data/representative_branch_tables.json`

## 7. Bottom line

The current D5 frontier is no longer bridge discovery.

It is:

- understand the true accessible components,
- decide whether fixed `delta` has one tail length or several,
- and therefore decide whether the final global theorem is raw
  `(beta,delta)` or only abstract `(beta,rho)`.

That is the accepted post-`077` split.
