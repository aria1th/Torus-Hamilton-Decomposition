# D5 Shared Predecessor Interaction 010

This artifact evaluates the exact Session 28 family `D5-SHARED-PRED-INTERACTION-010`.

Question:
- Can a shared predecessor-based mode switch on both layers `2` and `3` break the universal `m`-cycle collapse from `009` while keeping nonzero monodromy and improving the mixed cycle baseline on `m=5,7,9`?

Inputs:
- fixed anchors: layer `0 -> 1`, layer `1 -> 4`, layer `4+ -> 0`
- shared predecessor flag:
  - `pred_sig1_wu2`
  - `pred_sig4_wu2`
- Stage 1 layer-2 mode pool:
  - `q=-1:2/4`
  - `q=-1:4/2`
  - `w+u=2:2/4`
  - `w+u=2:4/2`
- Stage 2 widening, only because Stage 1 failed to beat the mixed baseline:
  - `q=-1:0/2`
  - `q=-1:2/0`
  - `q=-1:2/3`
  - `q=-1:3/2`
- layer-3 old bits:
  - `q+u=1`
  - `q+u=-1`
  - `u=-1`
- layer-3 ordered slice pairs:
  - all ordered distinct pairs from `{0/3, 3/0, 3/3}`
- pilot moduli:
  - `m=5,7,9`
- stability spot-checks:
  - `m=11,13` on the top `20` validated survivors

Exact search sizes:
- Stage 1: `4 x 4 x 2 x 3 x 6 = 576` rules
- Stage 2: `8 x 8 x 2 x 3 x 6 = 2304` rules

Main outcome:
- The shared-switch branch is genuinely live, but it still fails the compression target.
- Stage 1 does break the full `009` universal-collapse law: not every clean survivor has `U_0 = m` cycles of length `m`.
- But every non-universal clean survivor is worse than the mixed baseline, not better.
- Stage 2 confirms that the minimal representative widening does not help. It only adds more baseline-shape mixed survivors and a small cycle-only cancellation regime.

Exact pilot totals:
- Stage 1:
  - clean survivors: `576`
  - strict survivors: `576`
  - mixed survivors: `540`
  - cycle-only survivors: `0`
  - monodromy-only survivors: `36`
  - trivial survivors: `0`
  - improved mixed survivors: `0`
  - universal-`m`-cycle clean survivors: `324`
- Stage 2:
  - clean survivors: `864`
  - strict survivors: `864`
  - mixed survivors: `780`
  - cycle-only survivors: `48`
  - monodromy-only survivors: `36`
  - trivial survivors: `0`
  - improved mixed survivors: `0`
  - universal-`m`-cycle clean survivors: `612`

Exact regime distributions among clean strict survivors:
- Stage 1:
  - `324` mixed rules with total pilot `U_0` cycle count `21`:
    the old baseline `5 + 7 + 9`
  - `180` mixed rules with total pilot `U_0` cycle count `39`:
    counts `9,13,17`
  - `36` mixed rules with total pilot `U_0` cycle count `137`
  - `36` monodromy-only rules with total pilot `U_0` cycle count `155`
- Stage 2:
  - `564` mixed rules with total pilot `U_0` cycle count `21`
  - `180` mixed rules with total pilot `U_0` cycle count `39`
  - `36` mixed rules with total pilot `U_0` cycle count `137`
  - `48` cycle-only rules with total pilot `U_0` cycle count `21`
  - `36` monodromy-only rules with total pilot `U_0` cycle count `155`

Representative rules:
- Best mixed rule, Stage 1:
  - shared flag: `pred_sig1_wu2`
  - layer 2:
    - `p=0 -> q=-1:2/4`
    - `p=1 -> q=-1:2/4`
  - layer 3:
    - old bit `q+u=-1`
    - `p=0 -> 0/3`
    - `p=1 -> 3/0`
  - pilot return:
    - `m=5`: `5` cycles of length `5`, monodromy `3`
    - `m=7`: `7` cycles of length `7`, monodromy `5`
    - `m=9`: `9` cycles of length `9`, monodromy `7`
  - this exactly matches the old mixed baseline and does not improve it
- Representative non-universal mixed rule:
  - shared flag: `pred_sig1_wu2`
  - layer 2:
    - `p=0 -> q=-1:2/4`
    - `p=1 -> q=-1:4/2`
  - layer 3:
    - old bit `q+u=1`
    - `p=0 -> 0/3`
    - `p=1 -> 3/0`
  - pilot `U_0` cycle counts:
    - `m=5`: `9`
    - `m=7`: `13`
    - `m=9`: `17`
  - this is the clearest proof that the shared switch creates real interaction, but the interaction is anti-compressive
- Representative monodromy-only rule:
  - shared flag: `pred_sig1_wu2`
  - layer 2:
    - `p=0 -> w+u=2:2/4`
    - `p=1 -> w+u=2:4/2`
  - layer 3:
    - any off-diagonal ordered pair in the validated summary
  - pilot return:
    - `m=5`: `25` fixed points
    - `m=7`: `49` fixed points
    - `m=9`: `81` fixed points
  - nonzero monodromy survives, but all `U_0` cycles collapse to length `1`
- Representative Stage 2 cycle-only rule:
  - layer 2:
    - `p=0 -> q=-1:0/2`
    - `p=1 -> q=-1:3/2`
  - layer 3:
    - same mixed layer-3 gadget class as above
  - result:
    - pilot `U_0` cycle count stays `21`
    - monodromy cancels to `0`

Structural conclusion:
- Session 28 is not another separability no-go like `009`.
- The shared predecessor switch does produce genuine layer-2/layer-3 interaction.
- But inside this exact family the interaction only moves the system away from the baseline by adding fixed points or by killing twist, never by compressing `U_0` below the old mixed baseline.
- So the strongest supported handoff is:
  - shared switching is a live ingredient
  - this exact shared-switch family is still wrong-signed for cycle compression
  - the next branch should keep genuine interaction but change the layer-2 local palette or the shared local state, rather than merely widening within the present mode pool

Verification:
- `python -m py_compile scripts/torus_nd_d5_shared_pred_interaction_common.py scripts/torus_nd_d5_shared_pred_interaction_search.py scripts/torus_nd_d5_shared_pred_interaction_validate.py`
- `python scripts/torus_nd_d5_shared_pred_interaction_search.py --pilot-m-list 5,7,9 --out artifacts/d5_shared_pred_interaction_010/data/search_summary.json --candidates-out artifacts/d5_shared_pred_interaction_010/data/validation_candidates.json --no-rich`
- `python scripts/torus_nd_d5_shared_pred_interaction_validate.py --candidates-json artifacts/d5_shared_pred_interaction_010/data/validation_candidates.json --pilot-m-list 5,7,9 --stability-m-list 11,13 --stability-limit 20 --out artifacts/d5_shared_pred_interaction_010/data/validation_summary.json --no-rich`

Runtimes:
- search: about `138.06s`
- validation: about `118.80s`
