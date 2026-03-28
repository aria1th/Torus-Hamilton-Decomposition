# d5_249 master status after closing G1

## Closed theorem objects in the present slice

The following theorem objects are now closed in the current working slice:

- `T0` actual-needed core
- `T1`
- `T2`
- `T3`
- `T4`
- `G1`
- `G2`

## What was actually added at G1

`G1` closes by an explicit two-defect-set splice of the valid baseline package:

- `D1 = {sum = 2, x0 = m-1}`
- `D2 = color-4 classes L3s30p1 ∪ L3s31p0`  
  equivalently for `m >= 5`,
  `{sum = 3 and ((x0 != m-1 and x1+x3 = 2) or (x0 = m-1 and x1+x3 != 2))}`

The package is:

- `g0 = B0`
- `g3 = B3`
- swap colors `1` and `4` on `D1`
- swap colors `2` and `4` on `D2`

This gives:
- pointwise outgoing exhaustiveness
- colorwise incoming Latin / permutation
- exact agreement of `g4` with the surfaced `mixed_008` color-4 branch

## Remaining non-frontier inputs

What is still treated as prior / stable input is not a live frontier theorem object but the stable graph-side package already flagged in the manuscript, especially:

- corrected selector baseline as prior graph-side input
- closed color-4 branch package
- globalization input

So the honest status is:

- **no live frontier theorem object remains inside the present `T0--T4,G1,G2` slice**
- what remains is packaging / internalization of already-stable graph-side inputs if desired
