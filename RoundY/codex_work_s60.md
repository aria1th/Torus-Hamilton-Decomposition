Task ID:
`D5-DEEP-TRANSITION-CARRY-SHEET-046`

Result:
- extracted the exact future grouped-transition sheet for the carry bit on the
  checked best-seed active branch
- minimal exact future `dn` horizons:
  `2,4,6,8` on `m=5,7,9,11`, matching `m-3`
- minimal exact future grouped-state horizons:
  `3,5,7,9` on `m=5,7,9,11`, matching `m-2`
- exact compressed signature:
  current `B` plus
  `initial flat-run length where dn=(0,0,0,1)` plus
  `first nonflat dn`
- flat-run length alone is not exact

Sharpest interpretation:
- after `045`, the next carry object is no longer a vague deeper sheet
- the carry bit is already the first exact future grouped-transition event
- the `H-1` ambiguity is confined to regular carry `B`-states

Conclusion:
- the next local branch should search for an admissible surrogate for
  `B + flat-run length + first nonflat dn`
- parallel proof branch:
  package `044`, `045`, and `046` into a theorem chain
