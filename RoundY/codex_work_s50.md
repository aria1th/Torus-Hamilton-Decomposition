Task ID:
D5-LIFTED-CORRIDOR-CARRIER-TARGET-037

Question:
After `036`, is the lifted corridor state still hidden, or is it already
visible on raw current coordinates?

If it is already visible, what is the correct reduced target for the next local
branch?

Purpose:
`036` changed the branch from a projected `(s,layer)` phase picture to a lifted
`(q,a,layer)` corridor model. The next honest check is whether that lift still
needs phase extraction, or whether the real missing ingredient is only
corridor-localized triggering.

Inputs / Search space:
- best seed from `032`
- defect/corridor context from `033`
- projected-phase no-go from `035`
- lifted corridor traces from `036`
- moduli `m = 5,7,9`
- control `m = 11`

Allowed methods:
- exact verification along every traced corridor state up to first exit
- raw-coordinate formula extraction
- raw odometer coordinate extraction
- reduced carrier-target extraction
- no broad new local-rule search yet

Success criteria:
1. determine whether the lifted state is already visible on raw coordinates
2. extract an exact raw odometer if it exists
3. identify the uniform first-exit targets
4. state the correct reduced target for the next local branch

Failure criteria:
- no exact raw-coordinate relation emerges
- or the raw odometer coordinate does not increment exactly by one

Artifacts to save:
- `artifacts/d5_lifted_corridor_carrier_target_037/`
- `RoundY/autonomous/d5_autonomous_perturbation_note_v12.md`
- decision log update `D28`

Return format:
- raw visibility verdict
- raw odometer rule
- regular / exceptional target phases
- next reduced target recommendation

Reproducibility requirements:
- fixed best seed `[2,2,1] / [1,4,4]`
- fixed moduli `5,7,9,11`
- full traced corridors up to first exit
- saved JSON summaries for raw visibility, odometer, and carrier targets
