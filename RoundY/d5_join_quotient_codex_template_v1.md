Task ID:
D5-MASTER-FIELD-JOIN-QUOTIENT-001

Question:
Search cyclic-equivariant master fields for d=5 on the joined quotient \(\Theta_{AB}\), obtained by combining the informative atoms from the previous Schema A and Schema B runs.

Purpose:
Determine whether quotient enlargement alone is enough to escape the old degeneracy (Latin + clean frame but trivial section return), before adding any extra flux bit.

Inputs / Search space:
- Dimension d = 5.
- Pilot moduli: m in {5,7,9}. Stability check: m in {11,13}.
- Vertex set: (Z_m)^5.
- Quotient state:
  \[
  \theta(x)=(L(x), (s_0,\dots,s_4)),
  \]
  where L is bucketed layer {0,1,2,3,4+}, and for each color c,
  \[
  q_c=x_{c+1},\quad w_c=x_{c+2},\quad u_c=x_{c+4}
  \]
  and the per-color signature bits are:
  1. q_c = -1,
  2. q_c + u_c = 1,
  3. w_c + u_c = 2,
  4. q_c + u_c = -1,
  5. u_c = -1.
- Use cyclic equivariance under simultaneous color/coordinate rotation.
- Search variables: one anchor value a(theta) in {0,1,2,3,4} per quotient state orbit (equivalently, one cyclic-equivariant permutation field Pi_theta).

Allowed methods:
- CP-SAT / SAT / exact combinatorial search.
- Outgoing Latin constraints on every quotient state.
- Incoming Latin constraints on predecessor-pattern classes for m=5,7,9.
- Optional weak preferences toward layer-0 sigma and layer-4+ identity, but do not hardwire them.

Success criteria:
1. Find at least one Latin cyclic-equivariant field on Theta_AB.
2. Validate for m=5,7,9,11,13.
3. For the representative color 0, compute first-return diagnostics in the q-clock / v-fiber frame:
   - clean_frame,
   - strict_clock,
   - U_0 cycle count and lengths,
   - orbitwise monodromies.
4. Prefer candidates with:
   - clean_frame = True,
   - strict_clock = True,
   - U_0 single cycle,
   - all monodromies units.
5. Report full color cycle counts for each validated candidate.

Failure criteria:
- No Latin cyclic-equivariant field exists on Theta_AB.
- Latin fields exist, but every strict-clock clean-frame field still has U_0 completely fractured and zero monodromy.
- Fields with nontrivial U_0 necessarily lose Latin or clean frame.

Artifacts to save:
  - code
  - raw logs
  - summary report
  - saved feasible fields
  - validation JSON
  - phase/orbit tables for Theta_AB

Return format:
1. Executive summary
2. Exact quotient definition and size statistics
3. Search constraints and solver status
4. Saved feasible fields
5. Validation table for m=5,7,9,11,13
6. Branch decision: sufficient / insufficient / needs one extra flux bit

Reproducibility requirements:
- fixed random seed
- exact solver version
- explicit orbit count and predecessor-pattern count
- deterministic validator for Latin and color-0 return diagnostics
