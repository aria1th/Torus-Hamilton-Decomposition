Codex template (next run if more compute is needed):
Task ID:
D5-MASTER-FIELD-QUOTIENT-001

Question:
Find a cyclic-equivariant permutation-valued local field `\Pi_\theta\in S_5` on a finite quotient state space `\Theta` for `d=5`, such that the induced representative-color first return has a clean frame and satisfies a triangular skew-product Hamiltonicity criterion.

Purpose:
Move from representative-color probes to an actual 5-color coupled decomposition template where outgoing/incoming Latin compatibility is enforced by construction.

Inputs / Search space:
- dimension `d=5`
- odd pilot moduli `m in {5,7,9}`, then `11,13`
- quotient states `\Theta` built from:
  - layer `L in {0,1,2,3,4+}`
  - a small affine atom signature in representative coordinates `(q,w,u)`
  - optional one-bit flux/parity tag
- variables: one permutation `\Pi_\theta in S_5` for each quotient state
- cyclic equivariance under simultaneous rotation of coordinates/colors

Allowed methods:
- SAT / CP-SAT / MILP over finite quotient states
- exact exhaustive search for very small quotients
- branch-and-bound / beam search with exact validation
- symbolic extraction of representative-color first-return formulas

Success criteria:
1. Every quotient state carries a valid permutation `\Pi_\theta in S_5`.
2. Outgoing-Latin and incoming-Latin both hold on every tested vertex.
3. Representative color 0 has clean frame and strict clock.
4. Section return `U_0` is a single cycle on `m=5,7,9`.
5. Orbitwise monodromy is a unit on `m=5,7,9`.
6. Full five-color validation passes on `m=5,7,9`, with stability checks on `11,13`.

Failure criteria:
- no candidate satisfies Latin constraints together with clean frame;
- all Latin-compatible candidates fall into base-fracture or monodromy-zero classes;
- the quotient must grow beyond the chosen state budget.

Artifacts to save:
  - code
  - raw logs
  - summary report
  - candidate phase tables
  - Latin defect tables
  - section-return / monodromy traces
  - proof-supporting formulas

Return format:
1. Executive summary
2. Exact quotient state definition
3. Permutation table `\Pi_\theta`
4. Representative-color `R_0` / `U_0` formulas
5. Latin validation summary
6. Cross-modulus cycle summary
7. If unsuccessful, the sharpest no-go theorem suggested by the data

Reproducibility requirements:
- fixed seeds
- exact solver versions
- saved candidate tables in JSON/CSV
- deterministic validation scripts
- explicit quotient-state schema
