Task ID:
D5-CORRIDOR-PHASE-EXTRACTION-034

Question:
For the best endpoint seed pair
- left = [2,2,1]
- right = [1,4,4]

does the unresolved channel
- R1 -> H_L1

already factor through a reduced orbit-phase coordinate, so that the missing
repair state is phase on a known orbit rather than a generic bounded-state
transducer state?

Purpose:
`033` already killed the natural `2`-state and `3`-state transducer branch on
the current local alphabet. The next honest step is to extract the unresolved
channel itself as a reduced phase model and decide whether the short/long delay
split is just one extra orbit lap.

Inputs / Search space:
- best seed from `032`
- defect/corridor data from `033`
- reduced mixed/grouped context from `019` and `023`
- moduli `m = 5,7,9`
- control `m = 11`

Allowed methods:
- exact extraction of the unresolved `R1` alt-2 corridor
- reduced-coordinate embedding into `(s, layer)` and related coordinates
- exact phase-map extraction
- exact orbit-size verification
- exact delay/residue formula fitting and control check
- no new broad local search
- no bounded-state synthesis unless the phase model fails

Success criteria:
1. identify an explicit reduced phase rule for the corridor
2. verify a large/small orbit split
3. determine whether the short/long delay families differ by one full orbit lap
4. produce a clear verdict for the next branch

Failure criteria:
- no stable reduced phase model emerges
- or the delay split does not align with a clean orbit period

Artifacts to save:
- `artifacts/d5_corridor_phase_extraction_034/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v9.md`
- decision log update `D25`

Return format:
- explicit corridor phase model
- orbit-size verdict
- short/long delay law
- whether the missing state is orbit phase
- next recommended branch

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- deterministic representative source extraction by `u_source`
- saved JSON summaries for the phase model and delay laws
