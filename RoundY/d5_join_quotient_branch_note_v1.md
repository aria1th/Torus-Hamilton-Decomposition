Problem:
Construct a cyclic-equivariant permutation-valued local field for d=5 that can support a full 5-color Hamilton decomposition.

Current target:
Move from the failed fixed-quotient free-anchor searches to the next quotient enlargement step.
The immediate goal is not a full witness, but a sharper master-field specification on an enlarged quotient where both base dynamics and monodromy can coexist.

Known assumptions:
- [P] Under cyclic equivariance, a local field \(\Pi_\theta\in S_5\) is completely determined by its anchor values \(a(\theta)=\Pi_\theta(0)\), via
  \[
  \Pi_\theta(c)=a(\rho^{-c}\theta)+c \pmod 5.
  \]
  So “free anchor” is already as general as “free \(\Pi\)” on a fixed quotient.
- [C] On the current quotient spaces (Schema A and Schema B), free-anchor search found Latin fields but the best strict-clock representatives collapse to the trivial regime:
  layer 0 uses \(\sigma\), all other saved strict-clock states use identity, hence
  \[
  R_0(q,w,v,u)=(q+1,w,v,u),
  \]
  so \(U_0\) is the identity on the section and all monodromies are zero.
- [C] The non-clock saved representatives still remain Latin and clean-frame, but fail strict clock; they do not recover useful base dynamics either.
- [H] Therefore the obstruction is not additional freedom in anchor values, but missing state information in the quotient itself.

Attempt A:
  Idea:
  Keep the old quotient and relax anchored color-0 outputs to free anchor values.

  What works:
  - [C] Outgoing/incoming Latin constraints become satisfiable.
  - [C] Clean frame can still survive.

  Where it fails:
  - [C] The best strict-clock fields on both Schema A and Schema B use only two local permutations: identity and \(\sigma\).
  - [C] Their representative-color first return is the pure q-clock
    \(R_0(q,w,v,u)=(q+1,w,v,u)\), so \(U_0\) fractures into \(m^2\) fixed points and monodromy is zero.
  - [P] Since free-anchor already parameterizes every cyclic-equivariant field on a fixed quotient, no further “anchor relaxation” can help without changing the quotient.

Attempt B:
  Idea:
  Enlarge the quotient state by taking the join of the two previously informative quotient schemas.
  Schema A captured the “single-cycle / zero-monodromy” side; Schema B captured the “unit-monodromy / fractured-U” side.
  The natural next quotient is their join.

  What works:
  - [H] This is the smallest evidence-based enlargement that simultaneously remembers the atom sets responsible for the two half-successes.
  - [C] The joined quotient remains finite and computationally manageable on the pilot moduli.

  Where it fails:
  - [O] No search has yet been run on the joined quotient.
  - [O] It is unknown whether the join already suffices, or whether one extra flux bit / predecessor-phase bit is still needed.

Candidate lemmas:
- [P] On any fixed cyclic-equivariant quotient, free anchor = free local field.
- [H] If a quotient collapses all strict-clock Latin solutions to the identity-outside-layer-0 regime, then that quotient cannot support a triangular Hamiltonicity proof.
- [H] The next quotient should at least separate the atoms that individually controlled base connectivity and monodromy in the previous two searches.

Needed computations/search:
- [C] Build the joined quotient \(\Theta_{AB}\) with per-color atoms
  1. \(q_c=-1\),
  2. \(q_c+u_c=1\),
  3. \(w_c+u_c=2\),
  4. \(q_c+u_c=-1\),
  5. \(u_c=-1\).
- [C] Enumerate its state count and rotation-orbit count on pilot/stability moduli.
- [C] Run free-anchor / cyclic-equivariant Latin search on \(\Theta_{AB}\).
- [C] Diagnose saved fields by
  1. clean frame,
  2. strict q-clock,
  3. \(U_0\) cycle decomposition,
  4. orbitwise monodromy,
  5. full color cycle counts.
- [H] If \(\Theta_{AB}\) still produces the same degeneracy, add one more quotient bit that records a predecessor-phase / flux class.

Next branching options:
1. Joined quotient first: test whether A∪B atoms already unblock simultaneous base + monodromy.
2. If joined quotient still degenerates, add a single flux bit and rerun.
3. Only after quotient enlargement fails twice should we consider leaving the current q-clock / v-fiber normal-form class.

Claim status labels:
  [P] Proven / logically closed
  [C] Computationally observed
  [H] Heuristic but strongly motivated
  [F] Failed / structurally ruled out in the tested family
  [O] Open

Concrete joined quotient data:
- [C] Schema A union state count over \(m=5,7,9,11,13\): 1005 states, 209 rotation orbits.
- [C] Schema B union state count over \(m=5,7,9,11,13\): 3805 states, 773 rotation orbits.
- [C] Joined quotient \(\Theta_{AB}\) over the same moduli: 9427 states, 1899 rotation orbits.
- [C] Pilot predecessor-pattern counts for \(\Theta_{AB}\):
  - \(m=5\): 3125,
  - \(m=7\): 15774,
  - \(m=9\): 34631.
These sizes are still CPU-search territory.

Branch decision:
The next step should enlarge the quotient state itself. The evidence-based first enlargement is the joined quotient \(\Theta_{AB}\), not more anchor freedom on Schema A/B.
