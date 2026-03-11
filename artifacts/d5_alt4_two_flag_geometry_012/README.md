# D5 Alt-4 Two-Flag Geometry 012

This artifact evaluates the exact Session 30 family `D5-ALT4-TWO-FLAG-GEOMETRY-012`.

Question:
- With twist frozen to the canonical exact mixed representative, can a four-state layer-2 predecessor state
  `c2 = (pred_sig1_wu2, pred_sig4_wu2)`
  repair the sign of the alt-`4` geometry mechanism?

Fixed twist:
- layer-3 flag: `pred_sig1_wu2`
- layer-3 old bit: `q+u=-1`
- canonical slice pair:
  - `p3=0 -> 0/3`
  - `p3=1 -> 3/0`

Control twist:
- sign-reversed pair, checked only on the top validated survivors:
  - `p3=0 -> 3/0`
  - `p3=1 -> 0/3`

Layer-2 state and pools:
- four-state layer-2 local state:
  - `00, 01, 10, 11` from `(pred_sig1_wu2, pred_sig4_wu2)`
- Stage 1 pure alt-`4` pool:
  - `q=-1:2/4`
  - `q=-1:4/2`
  - `w+u=2:2/4`
  - `w+u=2:4/2`
- Stage 2 widening, because Stage 1 found no improvement:
  - add
    - `q=-1:0/2`
    - `q=-1:2/0`
    - `q=-1:2/3`
    - `q=-1:3/2`

Exact search sizes:
- Stage 1: `4^4 = 256` rules
- Stage 2: `8^4 = 4096` rules

Main outcome:
- The two-flag refinement is genuinely live, but it still fails.
- Stage 1 clean strict survivors: `256`
- Stage 1 profile split:
  - `248` mixed
  - `8` monodromy-only
  - `0` cycle-only
  - `0` improved mixed
- Stage 2 clean strict survivors: `640`
- Stage 2 profile split:
  - `608` mixed
  - `16` cycle-only
  - `16` monodromy-only
  - `0` improved mixed

The key structural point is:
- Session 30 does create new geometry classes that were not present in `011`
- but every new class is still anti-compressive
- so the sign problem survives the two-flag refinement

Exact clean strict regime distributions:
- Stage 1:
  - `104` mixed with total pilot `U_0` cycle count `21`
  - `32` mixed with total pilot `U_0` cycle count `35`
  - `80` mixed with total pilot `U_0` cycle count `39`
  - `8` mixed with total pilot `U_0` cycle count `57`
  - `8` mixed with total pilot `U_0` cycle count `119`
  - `16` mixed with total pilot `U_0` cycle count `137`
  - `8` monodromy-only with total pilot `U_0` cycle count `155`
- Stage 2:
  - `320` mixed with total pilot `U_0` cycle count `21`
  - `64` mixed with total pilot `U_0` cycle count `35`
  - `160` mixed with total pilot `U_0` cycle count `39`
  - `16` mixed with total pilot `U_0` cycle count `57`
  - `16` mixed with total pilot `U_0` cycle count `119`
  - `32` mixed with total pilot `U_0` cycle count `137`
  - `16` cycle-only with total pilot `U_0` cycle count `21`
  - `16` monodromy-only with total pilot `U_0` cycle count `155`

Representative rules:
- Best mixed rule:
  - all four layer-2 states use `q=-1:2/4`
  - pilot `U_0` cycle counts: `5,7,9`
  - this is exactly the old mixed baseline
- New `35` regime:
  - `00 -> q=-1:2/4`
  - `01 -> q=-1:4/2`
  - `10 -> q=-1:4/2`
  - `11 -> q=-1:2/4`
  - pilot `U_0` cycle counts: `5,7,23`
- New `57` regime:
  - `00 -> q=-1:2/4`
  - `01 -> w+u=2:2/4`
  - `10 -> w+u=2:4/2`
  - `11 -> q=-1:2/4`
  - pilot `U_0` cycle counts: `13,19,25`
- New `119` regime:
  - `00 -> w+u=2:2/4`
  - `01 -> q=-1:2/4`
  - `10 -> q=-1:2/4`
  - `11 -> q=-1:2/4`
  - pilot `U_0` cycle counts: `17,37,65`
- Persistent destructive `137` regime:
  - `00 -> w+u=2:2/4`
  - `01 -> q=-1:2/4`
  - `10 -> w+u=2:4/2`
  - `11 -> q=-1:2/4`
  - pilot `U_0` cycle counts: `21,43,73`
- Monodromy-only `155` regime:
  - `00 -> w+u=2:2/4`
  - `01 -> w+u=2:2/4`
  - `10 -> w+u=2:4/2`
  - `11 -> q=-1:2/4`
  - pilot `U_0` cycle counts: `25,49,81`

What Stage 2 adds:
- no improved mixed witness
- no new positive geometry class
- more copies of the same anti-compressive mixed regimes
- a small cycle-only cancellation regime at total pilot cycle count `21`

Validation:
- every one of the `640` clean survivors was revalidated on `m=5,7,9`
- all `640` match the search summary exactly
- all validated clean survivors are full-color Latin and strict
- top `20` survivors were spot-checked on `m=11,13`
- the best mixed survivors stay on the baseline `11,13` cycle profile
- top `20` survivors were also checked under the sign-reversed control twist
- all `20 / 20` had the same cycle signature under control twist

Strongest supported conclusion:
- fixed twist is still not the right knob
- the two-flag layer-2 refinement is live enough to generate new geometry classes
- but every new class is worse than the mixed baseline
- so the next branch should widen layer-2 local state again, not return to layer-3 widening

Verification:
- `python -m py_compile scripts/torus_nd_d5_alt4_two_flag_geometry_common.py scripts/torus_nd_d5_alt4_two_flag_geometry_search.py scripts/torus_nd_d5_alt4_two_flag_geometry_validate.py`
- `python scripts/torus_nd_d5_alt4_two_flag_geometry_search.py --pilot-m-list 5,7,9 --out artifacts/d5_alt4_two_flag_geometry_012/data/search_summary.json --candidates-out artifacts/d5_alt4_two_flag_geometry_012/data/validation_candidates.json --no-rich`
- `python scripts/torus_nd_d5_alt4_two_flag_geometry_validate.py --candidates-json artifacts/d5_alt4_two_flag_geometry_012/data/validation_candidates.json --pilot-m-list 5,7,9 --stability-m-list 11,13 --stability-limit 20 --control-limit 20 --out artifacts/d5_alt4_two_flag_geometry_012/data/validation_summary.json --no-rich`

Runtimes:
- search: about `80.09s`
- validation: about `80.42s`
