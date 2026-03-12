Task ID:
D5-RICH-OBSERVABLE-RAW-CARRIER-REALIZATION-040

Question:
Can the fixed raw carrier model from `037` and `039` already be realized in
the first richer observable families beyond the simple `038` point alphabet, or
do those families still fail so that the remaining gap is only coordinate
exposure / admissibility?

Purpose:
Freeze the control logic first. Then test only the smallest richer realization
families:
- full simple row
- source-edge full-row pair
- lag-1 / lag-2 full-row temporal pairs
- coordinate-level raw current family

Inputs / Search space:
- best seed `[2,2,1] / [1,4,4]`
- unresolved channel `R1 -> H_L1`
- fixed raw carrier from `037` and `039`
- moduli `m = 5,7,9`
- control `m = 11`

Allowed methods:
- exact extraction from the current best-seed pipeline
- exact isolation checks
- exact active-trace uniqueness / prehit checks
- no broad transducer search

Success criteria:
1. save the fixed raw carrier in machine-readable form
2. confirm the full simple row still fails
3. test the first richer simple-row-derived families
4. identify the first surviving realization family, if any
5. state the exact next gap

Failure criteria:
- no clear boundary emerges between failing simple families and surviving richer
  coordinate-level families

Artifacts to save:
- `artifacts/d5_rich_observable_realization_040/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v15.md`
- decision log update `D31`

Return format:
- fixed raw carrier spec
- simple-family no-go
- richer-family result
- surviving realization family, if any
- next-gap recommendation
