Task ID:
D5-MIXED-SKEW-ODOMETER-NORMAL-FORM-018

Question:
Can the canonical mixed witness `mixed_008` be promoted from an empirical grouped-return signal to an explicit D5 normal form?

More concretely:
verify or rigorously extract that its reduced return map is a one-dimensional skew-odometer

\[
s \mapsto s+1,\qquad
t \mapsto t+\phi(s),
\]

with cocycle cohomologous to a single defect.

Purpose:
The `017` bundle identified a stable grouped-return base for the mixed witness.
The next job is not another local-family sweep. It is to verify whether the
mixed witness already collapses to a reduced state `s = w+u` and whether the
grouped cocycle admits a canonical normal form.

Inputs:
- saved `017` bundle:
  - `artifacts/d5_return_map_model_017/data/analysis_summary.json`
  - raw mixed-witness tables
  - raw control tables
- direct witness replay for `mixed_008` via the existing `008` common code

Primary moduli:
- `m in {5,7,9,11,13}`

Optional stability moduli:
- `m in {15,17,19}`

Required checks:
1. Verify the first-return quotient is exactly by `(q,s)` with `s = w+u`.
2. Verify the grouped-return quotient is exactly by `s = w+u`.
3. Verify the reduced first-return formula
   `R_red(q,s) = (q+1, s+1+1_{q=m-2})`.
4. Verify the reduced grouped-return formula
   `U_red(s) = s+1`.
5. Verify the grouped cocycle formula
   `phi(s) = 2 + 1_{s=1} - 2*1_{s=2} - 1_{s=3}` mod `m`.
6. Verify an explicit gauge reduction to:
   - `2 - 2*1_{s=2}`
   - then `-2*1_{s=2}`
7. Compare the mixed witness against:
   - `monodromy_008`
   - `cycle_007`
   - `anti_mixed_010`

Allowed methods:
- exact extraction from saved tables
- direct witness replay from the `008` rule
- reduced-table construction
- quotient verification
- cocycle normalization
- modest stability checks on a few larger odd moduli
- no broad local-family search

Success criteria:
1. Produce exact reduced first-return tables for `mixed_008`.
2. Produce exact reduced grouped-return / cocycle tables for `mixed_008`.
3. Show that the saved `017` quotient tables are exactly the `(q,s)` and `s`
   quotients.
4. Show that direct replay reproduces the same formulas on `5,7,9,11,13`.
5. If feasible, extend the same formulas to `15,17,19` as stability evidence.
6. Package the control comparison in the same reduced-language.
7. Return the sharpest supported D5 normal-form statement and the remaining gap
   to a theorem.

Failure criteria:
- the reduced-state formulas fail on the saved tables,
- or direct witness replay fails to reproduce them,
- or the cocycle formula/gauge reduction fails,
- or the controls show that the apparent normal form is an artifact of the
  chosen quotient.

Artifacts to save:
- code
- raw logs
- summary report
- reduced first-return tables
- reduced grouped-return tables
- cocycle / gauge tables
- control-comparison summary
- witness registry

Return format:
- exact reduced coordinates used
- exact reduced first-return formulas
- exact grouped-return / cocycle formulas
- exact gauge reduction
- comparison with controls
- strongest supported normal-form statement
- exact remaining theorem gap

Reproducibility requirements:
- fixed witness definitions
- fixed inspected moduli `5,7,9,11,13`
- deterministic extraction order
- explicit separation of:
  - saved-table facts
  - direct-replay facts
- saved JSON for reduced maps and cocycle tables
