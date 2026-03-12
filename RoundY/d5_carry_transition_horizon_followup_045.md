# D5 carry follow-up after 045
This note records direct follow-up checks on the frozen active dataset from `045`.
## Main extra finding
The negative from `045` does **not** point only to an amorphous “broader gauge”. On the checked active union, a finite future grouped-transition window already realizes the carry bit exactly.
For the grouped-delta stream `dn`, the minimal exact future window lengths are:
- m=5: exact window length 2
- m=7: exact window length 4
- m=9: exact window length 6
- m=11: exact window length 8

This matches `m-3` on all checked moduli.
For the future grouped-state window `B, B_next, ...`, the minimal exact lengths are one larger:
- m=5: exact window length 3
- m=7: exact window length 5
- m=9: exact window length 7
- m=11: exact window length 9

This matches `m-2` on all checked moduli.
## More compressed signature
A more theorem-friendly exact signature is:
- the length of the initial flat run where `dn=(0,0,0,1)`, and
- the first nonflat `dn` after that run.
Combined with current `B`, this signature is exact on `m=5,7,9,11`. The flat-run length by itself is **not** exact.
## Interpretation
So the next local branch can be sharpened from
> “broader lifted gauge or deeper-than-2-step transition sheet”
to
> “carry realization by the first exact future grouped-transition sheet, with minimal horizon `m-3` in the checked data.”
This suggests two concrete sub-branches:
1. Exact computation branch: prove or test that the minimal future `dn` horizon is `m-3` in general odd `m`.
2. Admissibility branch: search for an admissible surrogate of that horizon / first-nonflat signature, instead of continuing with more short-horizon current features.
## Caution
This does **not** yet solve admissibility. The exact future window is a structural clue, not an admissible observable.
