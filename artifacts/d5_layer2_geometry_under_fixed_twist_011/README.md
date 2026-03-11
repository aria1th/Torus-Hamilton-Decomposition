# D5 Layer-2 Geometry Under Fixed Twist 011

This artifact evaluates the exact Session 29 family `D5-LAYER2-GEOMETRY-UNDER-FIXED-TWIST-011`.

Question:
- With twist frozen to one exact mixed representative, can a better-signed layer-2 local switch improve the mixed baseline on `m=5,7,9`?

Canonical Stage 1 twist:
- layer-3 predecessor flag: `pred_sig1_wu2`
- layer-3 old bit: `q+u=-1`
- canonical ordered slice pair:
  - `p3=0 -> 0/3`
  - `p3=1 -> 3/0`

Auxiliary control twist:
- same layer-3 predecessor flag and old bit
- sign-reversed ordered slice pair:
  - `p3=0 -> 3/0`
  - `p3=1 -> 0/3`

Layer-2 search family:
- layer-2 local flag:
  - `pred_sig1_wu2`
  - `pred_sig4_wu2`
- ordered layer-2 slice pair from
  - `q=-1:2/4`
  - `q=-1:4/2`
  - `w+u=2:2/4`
  - `w+u=2:4/2`
  - `q=-1:0/2`
  - `q=-1:2/0`
  - `q=-1:2/3`
  - `q=-1:3/2`

Exact search sizes:
- Stage 1 canonical twist: `2 x 8 x 8 = 128` rules
- control twist comparison: `128` rules
- Stage 2 widening of layer 3: not triggered

Main outcome:
- No layer-2 rule improves the mixed baseline.
- Stage 1 clean strict survivors: `48`
- among them:
  - `46` mixed
  - `2` monodromy-only
  - `0` cycle-only
  - `0` improved mixed
- the control twist has exactly the same clean counts and exactly the same cycle signatures on all `128` layer-2 rules
- therefore, in this fixed-twist family, geometry is fully insensitive to twist sign

Exact clean strict regime distribution:
- `34` mixed rules with total pilot `U_0` cycle count `21`
  - the old baseline `5 + 7 + 9`
- `10` mixed rules with total pilot `U_0` cycle count `39`
  - counts `9,13,17`
- `2` mixed rules with total pilot `U_0` cycle count `137`
- `2` monodromy-only rules with total pilot `U_0` cycle count `155`

Control comparison:
- same cycle signature count: `128 / 128`
- same total pilot cycle count count: `128 / 128`
- same profile-kind count: `128 / 128`
- no differing examples

This is the sharpest supported conclusion from Session 29:
- freezing twist does not recover any positive-sign geometry rule on layer 2
- all geometry variation already comes from layer-2 local data
- changing twist sign does not change the geometry at all in this family
- so the next live branch should widen layer-2 local state, not layer-3 twist

Representative rules:
- Best mixed rule:
  - layer-2 flag: `pred_sig1_wu2`
  - layer 2:
    - `p2=0 -> q=-1:0/2`
    - `p2=1 -> q=-1:0/2`
  - pilot return:
    - `m=5`: `5` cycles of length `5`, monodromy `3`
    - `m=7`: `7` cycles of length `7`, monodromy `5`
    - `m=9`: `9` cycles of length `9`, monodromy `7`
  - this exactly matches the old mixed baseline and does not improve it
- Representative anti-compressive mixed rule:
  - layer-2 flag: `pred_sig1_wu2`
  - layer 2:
    - `p2=0 -> q=-1:2/4`
    - `p2=1 -> q=-1:4/2`
  - pilot `U_0` cycle counts:
    - `m=5`: `9`
    - `m=7`: `13`
    - `m=9`: `17`
- Representative monodromy-only rule:
  - layer-2 flag: `pred_sig1_wu2`
  - layer 2:
    - `p2=0 -> w+u=2:2/4`
    - `p2=1 -> w+u=2:4/2`
  - pilot return:
    - `m=5`: `25` fixed points
    - `m=7`: `49` fixed points
    - `m=9`: `81` fixed points

Per-flag summary:
- `pred_sig1_wu2`:
  - `24` clean strict survivors
  - `22` mixed
  - `2` monodromy-only
- `pred_sig4_wu2`:
  - `24` clean strict survivors
  - `24` mixed
  - `0` monodromy-only

Stability:
- top `20` validated survivors were spot-checked on `m=11,13`
- the top mixed survivors remain on the baseline profile with `11` and `13` cycles respectively

Verification:
- `python -m py_compile scripts/torus_nd_d5_layer2_geometry_under_fixed_twist_common.py scripts/torus_nd_d5_layer2_geometry_under_fixed_twist_search.py scripts/torus_nd_d5_layer2_geometry_under_fixed_twist_validate.py`
- `python scripts/torus_nd_d5_layer2_geometry_under_fixed_twist_search.py --pilot-m-list 5,7,9 --out artifacts/d5_layer2_geometry_under_fixed_twist_011/data/search_summary.json --candidates-out artifacts/d5_layer2_geometry_under_fixed_twist_011/data/validation_candidates.json --no-rich`
- `python scripts/torus_nd_d5_layer2_geometry_under_fixed_twist_validate.py --candidates-json artifacts/d5_layer2_geometry_under_fixed_twist_011/data/validation_candidates.json --pilot-m-list 5,7,9 --stability-m-list 11,13 --stability-limit 20 --out artifacts/d5_layer2_geometry_under_fixed_twist_011/data/validation_summary.json --no-rich`

Runtimes:
- search: about `11.11s`
- validation: about `27.57s`
