Task ID:
D5-ENDPOINT-LATIN-REPAIR-032

Question:
Can one of the `030` endpoint-separated seed pairs be repaired into a
Latin/clean/strict realization of the `025` reduced target by the smallest
possible local fix:
- one repair class,
- one extra bit of context,
- or the smallest best-seed two-class static repair?

Purpose:
`028–031` already showed that the reduced target is still right, endpoint
orientation is necessary, but static endpoint-word families fail at the Latin
stage. The next honest step is to extract exact collision certificates and test
whether the first nontrivial repair layer is enough.

Inputs / Search space:
- reduced target: `025`
- endpoint signature: `028`
- static negative boundaries: `029`, `031`
- seed pool: `030`
- primary moduli: `5,7,9`
- first control: `11`

Allowed methods:
- exact collision certificate extraction
- exact seed ranking
- one-gate repair search on top seeds
- one-bit repair search on top seeds
- smallest two-class static probe on the best seed

Success criteria:
- identify a seed with compact collision support
- find a one-gate or one-bit repair that is Latin/clean/strict on `5,7,9`
- ideally preserve the `025` grouped target

Failure criteria:
- one-gate search has `0` Latin survivors
- one-bit search has `0` Latin survivors
- best-seed two-class static probe also has `0` Latin survivors

Artifacts to save:
- `artifacts/d5_endpoint_latin_repair_032/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v7.md`
- decision log update `D23`

Return format:
- best-ranked seed
- exact collision profile
- one-gate result
- one-bit result
- strongest obstruction

Reproducibility requirements:
- deterministic seed list from `030`
- deterministic top-seed selection
- fixed moduli `5,7,9,11`
