# d=4 line-union proof: v3 patch notes

## What changed from the earlier draft

### 1) Witness definition completed
The rule now explicitly says that the canonical tuple `(0,1,2,3)` is used **otherwise**. This fills the missing case `S(x)=2, q(x) != 0`.

### 2) Residue convention made explicit
The note now states that residues are read via their standard representatives in `{0,1,...,m-1}`. This removes any ambiguity in phrases such as `S(x) >= 3` and `q(x)=m-1`.

### 3) Simultaneous swaps clarified
The note now says that when both `x_0=0` and `x_3=0` hold on `H={S=2,q=0}`, both swaps are applied and they commute because they are disjoint.

### 4) Gate conditions written at the landing points
In the first-return proof, the layer-2 gate conditions are now expressed as `y^+_0=0`, `y^+_3=0`, `y^-_0=0`, `y^-_3=0`, avoiding reuse of the start-point variable.

### 5) Proposition 5 repaired
The old counting argument implicitly assumed injectivity/surjectivity. The new proof instead uses exact orbit-period lifting:
- if `R_c^t(x_0)=x_0` with `x_0 in Q`, then returning to `Q` forces `t` to be a multiple of `m`,
- dividing by `m` reduces the return problem to `T_c`,
- since `T_c` has exact period `m^2`, the `R_c`-period is exactly `m^3`.
This yields a single orbit of size `|P_0|=m^3`.

### 6) Proposition 6 repaired
Likewise, the lift from `P_0` to the full torus now uses exact orbit periods rather than a uniqueness-of-representation claim:
- if `f_c^t(y_0)=y_0` with `y_0 in P_0`, then returning to `P_0` forces `t` to be a multiple of `m`,
- dividing by `m` reduces the return problem to `R_c`,
- since `R_c` has exact period `m^3`, the `f_c`-period is exactly `m^4`.
This yields a single orbit of size `m^4`.

## Files
- `d4_line_union_general_theorem_proof_v3.md`
- `d4_line_union_general_theorem_proof_v3.tex`
- `d4_line_union_general_theorem_proof_v3.pdf`
