Problem:
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\operatorname{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
for all \(m\ge 3\), and do so in a form that is theorem-driven rather than witness-driven.

Current target:
Replace color-by-color rule search by a 5-color coupled object:
\[
\pi_x\in S_5,
\qquad f_c(x)=x+e_{\pi_x(c)}.
\]
The immediate goal is a conditional “cyclic-equivariant master template theorem” whose hypotheses are local and quotient-level, and whose conclusion is a full 5-color Hamilton decomposition.

Known assumptions:
- [P] Color 3 already yields a representative-color theorem: after first-return reduction to \(P_0=\{S=0\}\), a clean frame and triangular skew-product with single section cycle and unit monodromy imply Hamiltonicity.
- [P] The triangular skew-product criterion itself is reusable: if
  \[
  R(a,s,z)=(B(a,s),\ s+1,\ z+\beta(a,s))
  \]
  with section return \(U=B^m|_{s=0}\) a single cycle and orbitwise monodromy a unit mod \(m\), then \(R\) is a single cycle.
- [H] The right next abstraction is not “another good color”, but a permutation-valued local field \(\pi_x\in S_5\) with cyclic equivariance and Latin compatibility.
- [C] The uploaded Codex run `d5_fresh_cyclic_qclock_vfiber_001` searched a reduced family with built-in representative-color q-clock and v-fiber shielding. In that family, the frontier splits stably into:
  - Class A: `U` single cycle, `R` permutation, monodromy 0;
  - Class B: unit monodromy, but `U` fractured and `R` indegree-defective.
- [C] That Codex family did **not** enforce the 5-color outgoing/incoming Latin constraints. It is therefore a representative-color probe, not yet a decomposition family.
- [C] For the strongest Class A candidate
  `L1:d3 | L2:d2[q=-1->4; q+u=1->0] | L3:d4`,
  every color map is individually a permutation, but the coupled 5-color field is not Latin:
  - at `m=5`, 500 of 3125 vertices fail outgoing-Latin, 495 fail incoming-Latin;
  - at `m=7`, 1740 of 16807 vertices fail both outgoing/incoming Latin.
  So the fresh family, as searched, does not yet live in the correct 5-color state space.

Attempt A:
  Idea:
  Search representative-color cyclic families with built-in strict q-clock and clean v-fiber, then hope to lift to all colors by rotation.

  What works:
  - clean frame is built in by design;
  - first return reduces exactly to a map on `(q,w,u)` plus a `v`-cocycle;
  - large stable frontier found across `m=5,7,9,11,13`;
  - the search is good at isolating *structural* failure modes.

  Where it fails:
  - the search space does not encode `\pi_x\in S_5`;
  - hence arc-disjointness and incoming-Latin are not controlled;
  - even the best candidates are only single-color probes;
  - the frontier exhibits a rigid A/B dichotomy: either single-base with monodromy 0, or unit monodromy with fractured base / indegree defects.

Attempt B:
  Idea:
  Promote the whole problem to a cyclic-equivariant permutation field on a finite phase quotient:
  \[
  \theta(x)\in \Theta,\qquad \pi_{\theta(x)}\in S_5,
  \qquad \pi_{\rho\theta}=\rho\pi_\theta\rho^{-1}.
  \]
  Require outgoing-Latin automatically via `\pi_\theta\in S_5`, and incoming-Latin as a local compatibility condition between neighboring phase states.

  What works:
  - outgoing arc-disjointness becomes structural rather than post-checked;
  - incoming bijectivity becomes a local finite constraint;
  - cyclic equivariance should make all 5 colors conjugate, so only one representative-color proof is needed;
  - the color 3 theorem drops in as the representative-color Hamiltonicity criterion.

  Where it fails:
  - no explicit finite quotient `\Theta` with all three ingredients (Latin + cyclic + triangular representative color) has been found yet;
  - the current fresh family only models the representative-color quotient, not the full master field;
  - it is still open whether strict triangularity is enough once Latin coupling is enforced.

Candidate lemmas:
- [P] **Master-template implication.**
  Let `\rho` be simultaneous color/coordinate rotation. Suppose:
  1. `\theta:V\to\Theta` is a finite phase map with `\theta(\rho x)=\rho\theta(x)`.
  2. `\pi:\Theta\to S_5` satisfies `\pi_{\rho\theta}=\rho\pi_\theta\rho^{-1}`.
  3. The incoming-Latin map
     \[
     i\mapsto \pi_{\theta(x-e_i)}^{-1}(i)
     \]
     is a permutation of `{0,1,2,3,4}` for every vertex `x`.
  4. For color 0, the first return on `P_0` has a clean frame and satisfies the triangular skew-product Hamiltonicity criterion.

  Then all five color maps `f_c(x)=x+e_{\pi_{\theta(x)}(c)}` are Hamilton cycles, pairwise arc-disjoint, and together form a Hamilton decomposition.

- [H] **Fresh-family dichotomy may reflect a flux law.**
  In the current representative-color q-clock / v-fiber family, the stable split between
  `(single U, monodromy 0)` and `(unit monodromy, fractured U)` suggests a hidden conservation principle for `v`-flux under the current atom set.

- [H] **The next quotient likely needs one more local state bit.**
  The present quotient remembers only affine atoms in `(q,w,u)`. To escape the A/B dichotomy while preserving clean frame, one likely needs either
  - a local flux/parity bit,
  - or a slightly richer finite transducer state,
  before imposing `\pi_\theta\in S_5`.

Needed computations/search:
- [C] Search directly over a finite phase set `\Theta` with variables `\Pi_\theta\in S_5`, not over per-color offsets.
- [C] Hard constraints:
  - cyclic equivariance,
  - outgoing-Latin built in (`\Pi_\theta\in S_5`),
  - incoming-Latin on neighboring phase transitions,
  - representative-color clean frame,
  - representative-color strict clock / triangular normal form.
- [C] First pilot quotient should include:
  - layer `L\in\{0,1,2,3,\ge 4\}`,
  - a small affine atom signature in representative coordinates,
  - possibly one extra flux/parity bit.
- [C] Diagnostic outputs to save for every candidate family:
  - existence of clean frame,
  - section return `U` cycle decomposition,
  - orbitwise monodromy,
  - outgoing/incoming Latin defect counts,
  - indegree histograms.

Next branching options:
1. **Master-field search (preferred).**
   Build a quotient-state SAT/CP-SAT search with phase variables `\Pi_\theta\in S_5` and local Latin constraints.
2. **No-go theorem inside the current probe family.**
   Try to prove that in the q-clock / v-fiber affine-atom family, `U`-single-cycle plus `R`-permutation forces monodromy 0.
3. **Enriched strict-triangular family.**
   Keep the representative-color triangular target, but add one extra phase bit to encode the missing flux information before imposing Latin coupling.
4. **Weak-clean-frame side branch.**
   If strict triangular master fields fail repeatedly, open a controlled semitriangular branch rather than overfitting to color 3.

Claim status labels:
  [P] rigorously proved or immediate conditional theorem
  [C] computationally verified / extracted from artifacts
  [H] heuristic design principle / conjectural structural reading
  [F] ruled out within a defined family
  [O] open

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
