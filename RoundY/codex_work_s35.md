Task ID:
D5-RETURN-MAP-MODEL-017

Question:
What is the correct reduced return-map model behind the current D5 mixed witness family?

More concretely:
can one identify a section `Sigma`, a first return or grouped return `R`, and a reduced state variable `xi` such that the mixed witness factors through a simple canonical system, ideally an odometer, skew-odometer, or finite-state carry system with twist?

Purpose:
The exact search chain through `016` should now be treated as quotient discovery. The next main goal is no longer another broad local-family sweep. It is to extract the D5 return-map normal form.

Inputs / Witness set:
- canonical mixed witness from `008`
- strongest validated cycle-only witness
- representative monodromy-only witness
- representative anti-compressive mixed witness from `010`–`013`

Section / return objects:
- use the clean section already underlying the color-0 `U_0` return
- analyze:
  - raw first return on `(q,w,u)`
  - grouped return `U = R^m` on `q=0`

Pilot moduli:
- `m in {5,7,9}`

Stability moduli:
- `m in {11,13}`

Return observables to save:
- first-return word
- low-layer word / trace
- return increment on section coordinates
- monodromy increment
- grouped-return map
- cycle signature

Model-extraction methods:
- exact witness replay
- exact state-table extraction
- partition refinement / deterministic quotient minimization
- affine-fit checks for return maps and cocycles
- search for invariant and advancing linear forms
- comparison across witnesses and moduli

Success criteria:
1. Define the section explicitly.
2. Produce exact first-return data for the fixed witness set.
3. Produce exact grouped-return data for the same witness set.
4. Identify a reduced-state candidate that is stable across `m=5,7,9`.
5. Find an explicit canonical model if one exists:
   - odometer
   - skew-odometer
   - finite-state carry automaton with cocycle
6. Compare the mixed witness against cycle-only, monodromy-only, and anti-compressive controls.
7. If no satisfactory model appears, state the sharpest obstruction and the next missing coordinate or grouped-return refinement.

Failure criteria:
- no stable reduced quotient across the pilot moduli,
- or the grouped return is still too irregular to support a small exact model,
- or the extracted model depends too strongly on witness choice to be a credible D5 normal form candidate.

Artifacts to save:
- code
- raw logs
- summary report
- witness registry
- exact first-return state tables
- exact grouped-return state tables
- partition-refinement outputs
- affine-fit and linear-form checks
- representative trace tables
- obstruction tables if no canonical model is found

Return format:
- exact witnesses used
- section definition
- first-return summary
- grouped-return summary
- reduced-state candidates
- best canonical model found
- comparison across witnesses
- strongest obstruction if unresolved
- recommendation for the next missing coordinate / grouped-return refinement

Reproducibility requirements:
- fixed witness definitions
- fixed pilot moduli `5,7,9`
- deterministic enumeration order
- saved JSON for state tables, grouped-return tables, minimized quotients, and model checks
