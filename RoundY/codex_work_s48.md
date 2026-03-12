Task ID:
D5-STATIC-PHASE-GATE-NOGO-035

Question:
After `034`, is the first static phase-exposure layer already enough on the
best endpoint seed
- left = `[2,2,1]`
- right = `[1,4,4]`

If we isolate the first `H_L1` exit along the unresolved corridor by a raw
current-coordinate projection of `(q,w,v,u,s,layer)`, can the resulting static
`B`-state phase gates survive Latin / clean / strict / grouped-orbit checks?

Purpose:
`034` changed the branch from “generic transducer state” to “explicit corridor
phase.” The first honest no-go after that is to test whether a raw static
coordinate gate already exposes enough phase to matter, or whether even that
layer is dead.

Inputs / Search space:
- best seed from `032`
- defect/corridor context from `033`
- reduced phase model from `034`
- fields: `q, w, v, u, s, layer`
- projection sizes: `1, 2, 3`
- primary moduli: `5,7,9`
- first control: `11`
- gate modes:
  - `reg_only`
  - `exc_only`
  - `both`
- cocycle defects:
  - `none`
  - `left`
  - `right`
  - `both`

Allowed methods:
- exact extraction of first `H_L1` exit rows on the best seed
- exact projection screening for first-exit separation
- exact static `B`-state gate synthesis only on separating projections
- no broad seed widening
- no generic bounded-state transducer search

Success criteria:
1. find the smallest separating projection size
2. if static gates survive, identify a live phase-exposing family
3. otherwise return a sharp no-go that prunes the first static phase layer

Failure criteria:
- no `1`- or `2`-coordinate projection separates the first exit
- and every static gate built from the separating `3`-coordinate projections
  fails Latin on the pilot range

Artifacts to save:
- `artifacts/d5_static_phase_gate_nogo_035/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v10.md`
- decision log update `D26`

Return format:
- smallest separating projection size
- exact list of separating projections
- exact static gate family counts
- strongest supported conclusion for the next branch

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- deterministic first-exit extraction by source `u`
- saved JSON summaries for projection screening and static-gate outcomes
