Task ID:
D5-BIRTH-LOCAL-SIGNATURE-038

Question:
After `037`, can the unresolved best-seed corridor marker already be born
locally in a small raw neighborhood alphabet, and can the exceptional
`u_source = 3` family bit also be generated locally there?

Purpose:
`037` reduced the live problem to a localized carrier plus one family bit.
The next honest check is whether those are coupled or not: maybe the family
bit is already easy at birth while the marker itself is the real obstruction.

Inputs / Search space:
- best seed from `032`
- unresolved channel / corridor framing from `033–037`
- moduli `m = 5,7,9`
- control `m = 11`
- target sets:
  - source slice `R1`
  - entry slice `alt-2(R1)`
  - exceptional subsets coming from `u_source = 3`
- simple local alphabet:
  - current bits `layer, q=-1, phase_align, wu2`
  - one-step predecessor bits `phase_align, wu2` in relative directions `0..4`
  - one-step successor bits `phase_align, wu2` in relative directions `0..4`
- projection sizes `1..5`

Allowed methods:
- exact search over local-bit projections only
- no broad new witness search
- no new transducer family yet

Success criteria:
1. decide whether the source marker is already locally isolatable
2. decide whether the entry marker is already locally isolatable
3. decide whether the exceptional family bit is already locally visible
4. sharpen the next reduced target accordingly

Failure criteria:
- the simple neighborhood search gives no stable conclusion

Artifacts to save:
- `artifacts/d5_birth_local_signature_search_038/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v13.md`
- decision log update `D29`

Return format:
- source-marker verdict
- entry-marker verdict
- exceptional-family-bit verdict
- next reduced target recommendation

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- exact projection counts for sizes `1..5`
