Task ID:
D5-MIXED-NORMAL-FORM-AND-U-OBSTRUCTION-019

Question:
Can the canonical mixed witness `mixed_008` be upgraded from an exact computational normal form to the explicit D5 return-map model

\[
R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
\]
\[
U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
\]

with

\[
\phi(s)\sim -2\,\mathbf 1_{s=2},
\]

and can the remaining obstruction be identified precisely as grouped `u`-invariance?

Purpose:
`018` extracted the reduced model computationally. The next step is to derive the same formulas directly from the raw `mixed_008` witness rule, identify the exact grouped-return factorization, and isolate the remaining obstruction in theorem-ready language.

Inputs / Search space:
- primary witness:
  - `mixed_008`
- controls:
  - `monodromy_008`
  - `cycle_007`
  - `anti_mixed_010`
- prior bundles:
  - `017`
  - `018`
- fixed moduli:
  - `5,7,9,11,13,15,17,19`

Allowed methods:
- symbolic derivation from the `mixed_008` rule
- exact replay verification against saved reduced tables
- grouped cocycle summation and gauge normalization
- grouped orbit analysis on fixed `u` fibers
- comparison with controls in the same reduced language
- modest proof-supporting computation only
- no broad new search

Success criteria:
1. Derive directly from the witness rule that first return depends on `(q,s,u,v)` with `s=w+u`.
2. Derive the exact first-return formulas
   `q' = q+1`,
   `s' = s+1+1_{q=m-2}`,
   `u' = u+1`,
   `v' = v+dv(q,s)`.
3. Derive the exact grouped return
   `U(s,u,v)=(s+1,u,v+phi(s))`.
4. Derive the explicit cocycle formula
   `phi(s)=2+1_{s=1}-2*1_{s=2}-1_{s=3}` and its gauge reduction to `-2*1_{s=2}`.
5. Prove or verify that each fixed-`u` fiber is a single grouped orbit on `(s,v)` for odd `m`.
6. State the exact obstruction as grouped `u`-invariance.
7. Explain why the controls do not realize the same normal form.

Failure criteria:
- the symbolic derivation does not reproduce the extracted reduced formulas,
- or the cocycle / grouped orbit conclusions fail on the checked moduli,
- or the control comparison undermines the claimed obstruction.

Artifacts to save:
- code
- raw logs
- summary report
- symbolic derivation note
- grouped orbit calculations
- control-comparison interpretation
- proof-supporting computations

Return format:
- exact reduced coordinates used
- exact first-return formulas
- exact grouped-return formulas
- exact cocycle formula and gauge reduction
- fixed-`u` grouped orbit statement
- exact obstruction statement
- control comparison
- smallest plausible next perturbation target

Reproducibility requirements:
- fixed witness definitions
- fixed moduli `5,7,9,11,13,15,17,19`
- deterministic extraction order
- explicit separation of:
  - rule-derived facts
  - replay-verified facts
- saved JSON for reduced maps, cocycles, grouped orbits, and controls
