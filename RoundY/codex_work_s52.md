Task ID:
D5-RAW-BIRTH-MARKER-TRANSPORT-039

Question:
For the unresolved best-seed channel `R1 -> H_L1`, are the source and entry
birth slices already exact on raw current coordinates, and if so does the next
reduced problem become tagged carrier transport rather than birth discovery?

Purpose:
`038` only ruled out small simple birth-local bit projections. The next honest
check is whether birth was already explicit on raw current coordinates all
along, in which case the remaining reduced obstruction is transport.

Inputs / Search space:
- best seed from `032`
- unresolved corridor branch from `033–038`
- moduli `m = 5,7,9`
- control `m = 11`
- source slice `R1`
- entry slice `alt-2(R1)`
- representative regular and exceptional corridor traces

Allowed methods:
- exact extraction from the existing best-seed pipeline
- exact formula matching on raw `(layer,q,w,u)`
- exact representative drift checks
- reduced carrier-state packaging
- no reopened broad local-rule search

Success criteria:
1. verify the exact raw source formula
2. verify the exact raw entry formula
3. verify the exceptional birth tag at source and entry
4. verify that current raw `u` drifts through all residues later
5. package the smallest tagged transport target

Failure criteria:
- the raw birth formulas are not exact on `m = 5,7,9,11`
- or the family bit remains statically readable later from current raw `u`

Artifacts to save:
- `artifacts/d5_raw_birth_marker_transport_039/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v14.md`
- decision log update `D30`

Return format:
- exact source formula
- exact entry formula
- family-bit drift verdict
- reduced tagged-transport recommendation
