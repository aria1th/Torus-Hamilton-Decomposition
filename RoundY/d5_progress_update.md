# d=5 progress update

## Hard conclusions
- The warning against using the absolute low layer `S_Z <= 3` is correct: if the defect support is cut out by the ordinary integer sum instead of the residue clock `S mod m`, then most bulk orbits never hit the defect region once `m >= 5`.
- The earlier `q`-section diagnostics based on a color-0-fixed coordinate frame should not be trusted for colors 1,2,3,4. A color-covariant relative coordinate system is needed. The clean base choice is
  - `q_c = x_{c+1}`,
  - `w_c = x_{c+2}`,
  - `v_c = x_{c+3}`,
  - `u_c = x_{c+4}`.
  Under the layer clock `S mod m` with layer-0 default `+e_{c+1}` and higher-layer default `+e_c`, the pure bulk first return is exactly `e_{c+1}-e_c`, so `q_c` increases by `1` while `w_c,v_c,u_c` are frozen.

## New computation
I switched from the earlier invalid direct tuple-family search to a search over **actual Kempe-valid swaps** from the canonical coloring. This guarantees that every intermediate coloring is valid (every color map remains a permutation).

### m = 5
I found an explicit low-layer witness:
- all supports are on layers `S mod 5 in {0,1,2,3}`,
- all moves are Kempe-valid,
- final cycle counts are `[1,1,1,1,1]`.

A 27-move witness was found first; one move is redundant. The 26-move pruned witness is saved in `d5_m5_kempe_witness_26.json`.

### m = 7
The same 26-move template remains Kempe-valid but is not yet Hamiltonian:
- cycle counts `[5, 433, 1, 1, 3]`,
- max cycle lengths `[5103, 12271, 16807, 16807, 10899]`.

This is strong evidence that the `S mod m` low-layer clock is the right topology, but the carry logic still needs an `m`-uniform symbolic description.

## Interpretation
The constants that appear in the explicit `m=5` witness (`0,1,2,3,4` on pinned coordinates) are consistent with the relative-coordinate viewpoint: after unfolding one full return, simple zero-tests in the color-covariant frame become affine one-coordinate pinning conditions in the absolute frame. So the witness supports the “nested carry cascade” picture, but not yet in a clean closed form.

## SymPy vs CP-SAT
- **CP-SAT / SAT** is the right primary tool for the collision-resolution stage, because the hard part is the discrete `AllDifferent` / permutation constraint.
- **SymPy** is useful *after* a candidate is found: extract and simplify the first-return formulas in the relative coordinates, detect affine cases, and prove odometer conjugacy.
- In this environment `sympy` is available, but `ortools` is not installed.

## Immediate next target
Use the color-covariant frame `(q_c,w_c,v_c,u_c)` plus the residue clock `S mod m` to compress the `m=5` witness into a small symbolic rule, then either:
1. generalize that rule to odd `m`, or
2. feed the reduced Boolean state model into a SAT/CP-SAT solver outside this container.