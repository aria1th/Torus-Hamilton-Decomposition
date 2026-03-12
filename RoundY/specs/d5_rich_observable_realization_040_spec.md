# D5-RICH-OBSERVABLE-RAW-CARRIER-REALIZATION-040

## Question

For the unresolved best-seed channel

- `R1 -> H_L1`

and the fixed best seed pair

- `left = [2,2,1]`
- `right = [1,4,4]`

can the exact raw tagged-carrier model already extracted in `037` and `039`
be realized in the smallest admissible local observable family, or does the
remaining gap provably require a richer source-edge / temporal observable than
the simple `038` neighborhood alphabet?

## Purpose

`037` and `039` together give an exact reduced control model on raw current
coordinates:

- source birth is exact on raw current coordinates,
- the family split is exact at birth,
- the corridor raw odometer is explicit,
- the regular and exceptional first-exit targets are explicit,
- the family tag must be initialized at birth and transported.

So the control logic is no longer the unclear part.

The next honest problem is:

- **realize the fixed raw 3-state carrier in an admissible local observable family**

rather than search again for a generic carrier or generic transducer.

A new prep check sharpens this further:

- the simple `038` birth-local bit family remains insufficient even if one uses
  the **entire** current+pred+succ 24-bit row,
- so there is no reason to continue larger combo search in that same simple
  alphabet.

## Raw carrier already fixed

Use the exact raw carrier states

- `off`
- `active_reg`
- `active_exc`

with the following intended semantics.

### Birth rules

At a source state:

- `layer = 1`
- `q = m-1`
- `w = 0`
- `u != 0`

initialize by taking the alt-2 entry.

Split the family tag at birth by:

- `u = 3  -> active_exc`
- `u != 3 -> active_reg`

So the birth rules are:

- if `layer=1, q=m-1, w=0, u=3`, take alt-2 and enter `active_exc`
- if `layer=1, q=m-1, w=0, u!=0,3`, take alt-2 and enter `active_reg`

### Transport rules

While active, follow the already extracted raw corridor dynamics.

No new routing search is needed at this level.

### Fire rules

- `active_reg` fires exactly at raw phase `(q,w,layer) = (m-1, m-2, 1)` and exits by direction `2`
- `active_exc` fires exactly at raw phase `(q,w,layer) = (m-2, m-1, 1)` and exits by direction `1`

Then return to `off`.

## Inputs / fixed scope

- reduced target from `025`: omit-base + edge-tied point cocycle defect
- unresolved best-seed channel from `033`: `R1 -> H_L1`
- static phase-gate no-go from `035`
- lifted corridor from `036`
- raw odometer and family-specific targets from `037`
- simple birth-local no-go / cheap source exceptional bit from `038`
- exact raw birth formulas and drift from `039`
- checked moduli: `m in {5,7,9,11}`

## New prep facts to treat as fixed for 040

The following should be treated as already established before any larger 040
search.

### A. Full simple birth-local row still does not isolate source or entry

In the simple `038` alphabet built from:

- current `layer, q=-1, phase_align, wu2`
- one-step predecessor `phase_align, wu2` in directions `0..4`
- one-step successor `phase_align, wu2` in directions `0..4`

using the **entire** 24-bit row still fails to isolate:

- source marker,
- entry marker,
- exceptional entry slice.

So `038` is not merely a size-`<=5` combo no-go.

It is evidence that the whole simple point-neighborhood bit family is the
wrong realization alphabet for the marker.

### B. Full simple row also does not stably identify the target phase

On representative regular and exceptional corridor traces, the final target row
in that same simple alphabet is not stably unique:

- regular target is unique in the full row only for `m=5,7`, but already fails
  for `m=9,11`,
- exceptional target is not unique even within the representative active trace
  for every checked modulus.

So the same simple alphabet should **not** be the default transport/trigger
search family either.

### C. Family bit remains cheap only at birth

Inside the source class, the exceptional slice is already cheap via the `038`
source bits

- `pred2_wu2`
- `pred4_wu2`

but `039` shows current raw `u` drifts through all residues later, so the
family tag must still be initialized at birth and transported.

## Main 040 target

Do **not** reopen broad carrier search.

Do **not** reopen bigger combo search in the same simple `038` alphabet.

Instead:

1. **freeze the raw 3-state carrier logic**, and
2. search only for the **smallest admissible realization family** that can
   implement the needed birth and target predicates.

## Allowed methods

- exact search over richer observable families than the `038` simple bit row
- source-edge or source->entry coupled observables
- temporal two-step or bounded-lag observables
- radius-2 local contexts if needed
- active-conditioned target tests
- exact reuse of the cheap birth-time exceptional split from `038`
- exact validation on `m=5,7,9` with control `m=11`

### Explicitly discouraged for 040

- no more larger projection search inside the same 24-bit simple alphabet
- no generic bounded-state transducer search with unconstrained control logic
- no reopening of phase-exposure work already settled by `037`
- no treating “family bit” as the main obstruction

## Success criteria

1. State the exact raw carrier as the fixed reduced control model.
2. Identify a richer admissible observable family that realizes the birth event:
   - either the raw source class directly,
   - or a source-edge / source->entry coupled birth event equivalent to it.
3. Identify a realization of the target tests for `active_reg` and `active_exc`:
   - either exact local target observables,
   - or an equivalent deterministic active transport law that makes the fire
     event locally decidable.
4. Validate any surviving realization on `m=5,7,9` and control `m=11`.
5. If no realization exists in the first richer family, report the exact next
   missing ingredient.

## Failure criteria

Failure occurs if the first richer realization family cannot:

- create the active marker at birth, or
- distinguish the active regular / exceptional trigger event,
- without ambient collisions.

If failure occurs, report whether the next missing state is best read as:

- an edge-centered observable,
- a two-step temporal observable,
- a radius-2 context,
- or a genuinely coordinate-level quantity not yet locally exposed.

## Candidate lemmas

- [C] `037` + `039` give an exact raw 3-state carrier model for the unresolved channel.
- [C] The simple `038` birth-local alphabet does not isolate source or entry even at full 24-bit resolution.
- [C] The same simple alphabet does not stably isolate the active target phase, especially on the exceptional branch.
- [H] The next honest branch is realization/compression of the fixed raw carrier, not generic carrier discovery.
- [F] Larger projection search in the same simple birth-local alphabet is the right next move.
- [O] Full D5 decomposition remains open.

## Needed computations / search

1. Save the exact raw carrier transducer in machine-readable form.
2. Save the full simple-alphabet no-go summary so it is not retried.
3. Build the first richer observable catalog, prioritizing:
   - source-edge observables,
   - source->entry pair signatures,
   - temporal lag-1 / lag-2 signatures,
   - active-conditioned target observables.
4. Search that richer family for an admissible realization of:
   - birth,
   - regular target,
   - exceptional target.
5. Only after that, if something survives, do mechanism validation.

## Return format

- exact raw 3-state carrier model
- explicit statement of what the simple `038` alphabet still cannot do, even at full-row resolution
- first richer observable family tested
- exact success or no-go result in that richer family
- smallest surviving realization, if any
- strongest obstruction if no realization exists
- recommendation for the next branch after 040

## Artifacts to save

- code
- raw_carrier_transducer_spec.json
- simple_alphabet_full_row_nogo_040.json
- active_target_visibility_simple_alphabet_040.json
- richer_observable_catalog_040.json
- realization_search_summary.json
- proof-supporting computations

## Reproducibility requirements

- fixed best seed pair `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- deterministic observable extraction order
- explicit separation of:
  - `037-039` raw carrier facts,
  - new `040` realization/no-go facts
