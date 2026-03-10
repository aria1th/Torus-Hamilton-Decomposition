Quick scan on the strict-collapse representative from `Theta_AB + phase_align`:

Goal:
Test whether the next refinement bit could simply be a *one-step-lagged copy* of an already existing atom (for example, predecessor `phase_align`, predecessor `w+u=2`, etc.).

Method:
For the representative strict-collapse field, split each visited return state by one Boolean feature of the immediate predecessor state, and measure residual hidden-phase collision size.

Baseline (no extra predecessor bit):
- `m=5`: multi-delta states `58`, total excess `70`
- `m=7`: multi-delta states `1829`, total excess `2673`, full nonzero-support states `28`
- `m=9`: multi-delta states `5509`, total excess `12707`, full nonzero-support states `228`

Best simple predecessor bits tested:
- `pred_any_phase_align`
  - `m=7`: total excess `2346`, full nonzero-support `23`
  - `m=9`: total excess `12863`, full nonzero-support `177`
- `pred_sig0_phase_align`
  - `m=7`: total excess `2459`, full nonzero-support `23`
  - `m=9`: total excess `12134`, full nonzero-support `180`
- `pred_sig1_wu2`
  - `m=7`: total excess `2435`, full nonzero-support `20`
  - `m=9`: total excess `12813`, full nonzero-support `217`
- `pred_sig4_wu2`
  - `m=7`: total excess `2530`, full nonzero-support `27`
  - `m=9`: total excess `12454`, full nonzero-support `202`

Conclusion:
- Reusing an *existing* atom one step earlier does help a little.
- But none of these simple predecessor bits removes the residual collision structure.
- So the next refinement bit should encode a genuinely new `tail-entry` / `predecessor-tail` class, not merely a delayed copy of the current atom vocabulary.
