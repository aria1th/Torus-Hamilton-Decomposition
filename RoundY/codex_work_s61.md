Task:
`D5-FUTURE-TRANSITION-CARRY-CODING-047`

Question:
After `046`, can the exact future-transition carry target be pruned further on
the checked active branch, and what is the first exact transition-sheet coding
of
`c = 1_{q=m-1}`?

Result:
- On `m=5,7,9,11`, `B + tau + epsilon4` is exact, and the boundary event class
  at `tau=0` is genuinely `3`-class minimal:
  `wrap`, `carry_jump`, `other`.
- No smaller tau truncation or threshold-bit quotient survives on the checked
  range before horizon `8`.
- The unique minimal exact contiguous interval quotient on `tau in {0,...,9}`
  is:
  `{0,1} | {2} | {3} | {4} | {5} | {6} | {7} | {8,9}`.
- The first exact checked-range transition-sheet coding found here is:
  current `B` plus
  current `epsilon4` plus
  the next `7` future flat/nonflat indicators after the current step.
- Full future `4`-class event windows become exact at horizon `8`.
- Pure future binary flat/nonflat windows become exact only at horizon `10`.

Meaning:
- The live hidden datum is still the flat-run counter `tau`, not a vague
  larger future sheet.
- `epsilon` is a secondary boundary correction, not the main missing state.
- The next honest local branch is admissible coding of `tau` itself, or a
  proof-style no-go for the first natural coding families.

Artifacts:
- script:
  `scripts/torus_nd_d5_future_transition_carry_coding.py`
- data:
  `artifacts/d5_future_transition_carry_coding_047/data/`
