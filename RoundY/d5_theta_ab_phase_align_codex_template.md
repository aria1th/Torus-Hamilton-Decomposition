Task ID:
D5-THETA-AB-PHASE-ALIGN-001

Question:
Search for a cyclic-equivariant master field on the refined quotient
Theta_AB_plus_phase_align,
where
phase_align_c(x)=1_{(x_{c+3}-x_{c+1}) mod m = 0},
and determine whether this refinement breaks the dynamic-collapse law
R_0(q,w,v,u)=(q+1,w,v+1,u).

Purpose:
Test the minimal grammar refinement suggested by the dynamic-collapse analysis.
The goal is not just Latin feasibility, but representative-color dynamics with:
1. clean frame,
2. strict q-clock,
3. nontrivial U_0,
4. nonzero/unit orbitwise monodromy.

Inputs / Search space:
- Dimension d=5.
- Quotient state:
  theta_plus(x)=(L(x), (s_c(x), phase_align_c(x))_{c in Z/5Z}),
  where s_c are the five existing joined-quotient atoms.
- Use free cyclic-equivariant field variables Pi_theta in S_5 (or anchor a(theta) with reconstruction).
- Pilot m-values: 5,7,9.
- Validate on 11,13 for survivors.

Allowed methods:
- CP-SAT / SAT / backtracking over quotient states or orbit representatives.
- Hard constraints:
  - cyclic equivariance,
  - outgoing Latin on all quotient states,
  - incoming Latin on predecessor-pattern classes for m=5,7,9.
- Soft/derived targets:
  - representative-color clean frame,
  - strict q-clock,
  - U_0 single cycle,
  - unit orbitwise monodromy,
  - low bad indegree.

Success criteria:
1. Find at least one Latin-feasible field on Theta_AB_plus_phase_align.
2. For the representative color, show the stable collapse law no longer holds.
3. Preferably obtain:
   - clean frame,
   - strict q-clock,
   - U_0 not equal to identity,
   - monodromy nonzero (ideally a unit),
   - improved full-color cycle profile.
4. If no survivor exists, extract a minimal residual conflict proving that phase_align alone is insufficient.

Failure criteria:
- No Latin-feasible field exists on the refined quotient.
- Every Latin-feasible field still collapses to trivial U_0 / zero monodromy.
- The only survivors merely reproduce the old kick-kick-freeze automaton modulo the new bit.

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- tables / plots / proof-supporting computations

Return format:
1. Executive summary.
2. Quotient size / orbit count after phase_align refinement.
3. Best Latin-feasible fields found.
4. Representative-color diagnostics:
   - clean frame,
   - strict clock,
   - U_0 cycle decomposition,
   - orbitwise monodromy,
   - indegree defect.
5. If failure: minimal residual conflict / forbidden motif on the refined quotient.
6. Recommendation: stop at one bit or add one predecessor-tail bit.

Reproducibility requirements:
- Fixed random seeds.
- Save exact quotient-state definition.
- Save every best-so-far field.
- Record solver versions.
- Deterministic validation scripts for m=5,7,9,11,13.
