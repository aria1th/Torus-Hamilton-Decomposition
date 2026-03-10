Task ID:
D5-DYNAMIC-COLLAPSE-CORE-001

Question:
On the joined quotient `Theta_AB` for the d=5 master-field problem, identify a minimal local motif (state / predecessor pattern / orbit motif) that forces dynamically trivial representative-color return, despite Latin feasibility.

Purpose:
Replace the vague instruction “add one more bit” with a precise statement of what information is missing from `Theta_AB`. The goal is to extract a minimal dynamic-collapse core and derive one explicit one-bit quotient refinement.

Inputs / Search space:
- Joined quotient `Theta_AB` from `d5_join_quotient_001`
- Saved Latin-feasible fields, especially `best_stable_field.json`
- State table, rotation orbit table, predecessor patterns for `m=5,7,9`
- Representative color `0`
- Relative coordinates `(q,w,v,u) = (x_1,x_2,x_3,x_4)`

Allowed methods:
- Exact analysis of saved fields
- Hypergraph / automaton representation of local compatibility
- Exhaustive motif enumeration on quotient states / predecessor patterns
- Minimal unsat core extraction for candidate return-splitting constraints
- SAT / CP-SAT only if it helps isolate a minimal core
- Symbolic return-law compression

Success criteria:
1. Exhibit a small finite motif family on `Theta_AB` that forces the stable field return law
   `R_0(q,w,v,u) = (q+1,w,v+1,u)`
   or otherwise forces `U_0 = id` / monodromy `0`.
2. Show that the motif cannot be removed without changing the quotient grammar.
3. Propose one concrete additional bit whose value distinguishes the conflicting cases.
4. State the refined quotient rule in a form ready for the next search.

Failure criteria:
- No identifiable small motif family; collapse appears globally diffuse.
- Proposed extra bit does not correspond to an observable conflict class on `Theta_AB`.
- The analysis only restates that the current field is degenerate without explaining why.

Artifacts to save:
- code
- raw logs
- summary report
- minimal motif tables
- candidate one-bit refinement definition
- compatibility hypergraph / automaton data

Return format:
1. Executive summary
2. Exact stable-field return law and its forced consequences
3. Minimal dynamic-collapse motifs
4. Proposed one-bit refinement and why it is the right one
5. Suggested next search configuration

Reproducibility requirements:
- Fixed random seeds where search is used
- Save exact motif enumeration tables
- Save any extracted unsat / conflict cores in machine-readable form
- Include deterministic verification for every stated motif
