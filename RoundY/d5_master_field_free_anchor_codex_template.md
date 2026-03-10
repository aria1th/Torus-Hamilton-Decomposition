Task ID:
D5-MASTER-FIELD-FREE-ANCHOR-001

Question:
Search for a cyclic-equivariant permutation-valued quotient field \(\Pi_\theta\in S_5\) on the existing d=5 quotient state space, but do **not** anchor color 0 to the previous one-color witness outputs. Treat the master field itself as the primary object.

Purpose:
Move from “Can a one-color anchor be Latinized?” to “Does there exist a genuine 5-color coupled quotient field whose representative-color first return has the desired clean-frame / section / monodromy structure?”

Inputs / Search space:
- Use the existing quotient state spaces from `d5_master_field_quotient_001` as pilot phase spaces:
  - Schema A state space `Theta_A = { (L, signature) }` with layer bucket `L in {0,1,2,3,4+}` and signature bits from `q=-1`, `q+u=1`.
  - Schema B state space `Theta_B = { (L, signature) }` with signature bits from `w+u=2`, `q+u=-1`, `u=-1`.
- Keep cyclic phase action `rho` (simultaneous color/coordinate shift).
- Variables should be either:
  1. one permutation `Pi_theta in S_5` per phase orbit in `Theta`, or
  2. one anchor value `a(theta)=Pi_theta(0)` per phase orbit, using the reconstruction formula
     \[
     Pi_theta(c)=a(rho^{-c}theta)+c \pmod 5.
     \]
- Allow the color-0 output to depend on the **full phase state/orbit**, not only on the representative local signature bit-pattern.

Allowed methods:
- CP-SAT / SAT / exact backtracking
- Outgoing-Latin can be enforced orbitwise via the anchor criterion
- Incoming-Latin must be enforced on predecessor phase patterns for pilot `m=5,7,9`
- Reduced first-return computation for representative color 0 on `m=5,7,9`
- Symmetry reduction by rotation or phase-orbit representatives

Hard constraints:
1. Cyclic equivariance:
   \[
   Pi_{rho theta}=rho Pi_theta rho^{-1}.
   \]
2. Outgoing-Latin:
   each `Pi_theta` is a permutation.
3. Incoming-Latin on pilot moduli `m=5,7,9`.
4. Layer defaults:
   - layer `0`: prefer `Pi_theta` close to the `+1` shift, but do not force the previous anchor table.
   - layer `4+`: prefer canonical / identity-like behavior, but allow explicit deviations if needed for global consistency.
5. Avoid `v`-dependence by construction if possible.

Soft / target constraints (in this order):
1. Representative color 0 has a clean frame on `m=5,7,9`.
2. The induced section return `U_0` is a single cycle on `m=5,7,9`.
3. Orbitwise monodromy is a unit on `m=5,7,9`.
4. If those succeed, test all colors for full first-return cycle structure.

Success criteria:
1. Produce at least one feasible cyclic-equivariant Latin field on `Theta_A` or `Theta_B`.
2. For the best field, report:
   - clean frame existence,
   - `U_0` cycle decomposition,
   - orbitwise monodromy,
   - full color validation on `m=5,7,9`.
3. If no feasible field exists, identify whether failure occurs at:
   - outgoing-Latin orbit criterion,
   - incoming predecessor patterns,
   - clean frame,
   - section fracture,
   - monodromy.

Failure criteria:
- No feasible cyclic-equivariant Latin field exists on `Theta_A` and `Theta_B`.
- Feasible Latin fields exist but none admit representative-color clean frame on `m=5,7,9`.
- Clean frame exists but every feasible field has fractured `U_0` or nonunit monodromy.

Artifacts to save:
- code
- raw logs
- summary report
- discovered feasible / infeasible orbit-anchor tables
- predecessor-pattern obstruction tables
- reduced first-return statistics
- best candidate permutation tables

Return format:
1. One-page executive summary
2. Exact phase-space definition
3. Search variable definition (`Pi_theta` or anchor `a(theta)`)
4. Feasible field count / infeasibility certificate status
5. Best candidates with `U_0` and monodromy diagnostics
6. Explicit local obstructions if infeasible
7. Suggested proof / no-go skeleton

Reproducibility requirements:
- Fixed random seeds
- Save every feasible field found on pilot moduli
- Save a machine-readable permutation/anchor table for every top candidate
- Record exact predecessor patterns used for incoming-Latin checks
- Save pilot/stability validation separately
