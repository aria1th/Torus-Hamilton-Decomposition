Problem:
Build a fresh odd-m cyclic family for d=5 in which every color admits a clean triangular first-return frame by construction, rather than by later surgery.

Current target:
Design a new low-layer template with the following hard constraints for every color c:
1. clean fiber exists,
2. strict clock exists,
3. section return U_c is a single cycle,
4. orbitwise monodromy is a unit.

Known assumptions:
- The absolute clock must be S(x)=x_0+...+x_4 mod m.
- The natural relative coordinates are
    (q_c,w_c,v_c,u_c)=(x_{c+1},x_{c+2},x_{c+3},x_{c+4}).
- A reusable theorem now exists for color 3:
    first-return reduction + clean-frame lemma + triangular skew-product Hamiltonicity criterion.
- The old 26-move witness is now a discovery artifact, not the main uniform odd-m route.
- The G3 color-0 pilot showed that post hoc repair is the wrong abstraction level.

Attempt A:
  Idea:
  Reuse the old style:
    layer 0 = sigma,
    layers >=4 = id,
    low layers 1,2,3 corrected by a few affine-pinned orbit-gates,
  but now impose a common clean frame at the design stage.
  What works:
  - The color-3 theorem shows that a triangular skew-product is enough.
  - The natural global scaffold remains relative coordinates plus the S mod m clock.
  Where it fails:
  - If the low-layer rule is allowed to depend on the candidate fiber coordinate, clean frames disappear for other colors.
  - Boolean-only state models are already UNSAT.

Attempt B:
  Idea:
  Move to a stricter fresh family with a built-in frame:
    choose one common clean fiber axis and one common strict clock axis in the relative frame,
    then only search rules compatible with that frame.
  What works:
  - The most promising choice is
      clean fiber = v_c,
      strict clock = q_c.
  - q_c already has the correct pure-bulk drift under
      layer 0 = sigma,
      layers >=1 default = id,
    because the pure first return gives Delta q_c = +1.
  - If low-layer rules on layers 1,2,3 never output direction c+1 for color c,
    then q_c stays a strict clock by construction.
  - If low-layer support depends only on (q_c,w_c,u_c) and never on v_c,
    then v_c is a clean fiber by construction.
  Where it fails:
  - No explicit all-color witness is known yet.
  - The correct affine-pinned support family still has to be selected.

Candidate lemmas:
- [H] Frame-first principle:
  For a viable odd-m family, clean fiber and strict clock should be hard constraints, not emergent properties.

- [H] q-clock / v-fiber principle:
  A natural fresh ansatz is to force, for every color c,
    R_c(q,w,v,u) = (q+1, B_c(q,w,u), v + beta_c(q,w,u)),
  or equivalently
    R_c(q,w,v,u) = (q+1, w', u', v+beta)
  after reordering the base coordinates.
  Then the section return U_c is obtained from R_c^m on the q=0 slice.

- [H] Search should forbid low-layer uses of relative direction 1:
  that preserves q_c as strict clock.

- [H] Search should forbid any support condition involving relative coordinate v_c:
  that preserves v_c as a clean cocycle coordinate.

- [H] The right low-layer support atoms are affine-pinned, not purely Boolean:
    q=a,
    w=a,
    u=a,
    q+w=a,
    q+u=a,
    w+u=a,
    q+w+u=a,
  with small residues a in {0,1,-1,2,-2}.

Needed computations/search:
1. State compiler.
   Build the finite relative-state alphabet Sigma from the chosen affine atoms on (q,w,u), layer by layer.
   Reduce it by cyclic symmetry and by obvious equivalences.

2. Permutation-feasibility sieve.
   For each low-layer state s in Sigma_L and each layer L in {1,2,3}, choose a color-0 output
      f_L(s) in {0,2,3,4}.
   Then define all colors by cyclic covariance and require vertexwise AllDifferent.
   This is the first hard filter.

3. Pilot first-return evaluator.
   For m in {5,7,9} and every surviving candidate, compute for each color c only:
   - clean frame existence (should be automatic if the template is correctly encoded),
   - q_c strict-clock verification,
   - cycle decomposition of U_c,
   - orbitwise monodromy on U_c-orbits,
   - optional indegree histogram only after the previous three succeed.

4. Search engine.
   Use CP-SAT if available; otherwise exact backtracking / beam search over the finite table f_L.
   The score order should be:
   (i) all 5 colors have the built-in frame,
   (ii) all 5 section maps U_c are single cycles,
   (iii) all 5 monodromies are units,
   (iv) only then inspect bijectivity / indegree defects.

5. Symbolic extraction.
   Once a candidate works for m=5,7,9, extract piecewise formulas for R_c and U_c with SymPy,
   then look for a common normal form and modulus-independent pattern.

Next branching options:
1. Fresh q-clock / v-fiber family (main branch).
2. If no candidate appears, relax the choice of strict clock but keep the clean-fiber hard constraint.
3. If that still fails, move from the affine-atom table to a fully symbolic CP/SAT model in the relative frame.

Claim status labels:
  [P] proved
  [C] computationally checked
  [H] heuristic/design principle
  [F] failed
  [O] open

Concrete proposed fresh family:
- Layer 0: sigma(c)=c+1.
- Layers 4,...,m-1: canonical.
- Layers 1,2,3: rules determined by a finite state table on affine states in (q_c,w_c,u_c).
- Allowed color-c outputs on layers 1,2,3: only {c, c+2, c+3, c+4}; never c+1.
- Supports may depend on q_c,w_c,u_c through affine atoms, but never on v_c.

Why this is the right next experiment:
- It hard-wires the two properties that were missing in the failed branches:
  simultaneous clean-frame existence and an absolute strict clock.
- It aligns with the successful color-3 mechanism while removing the need to recover the frame later by surgery.
- It converts the search from “repair arbitrary witnesses” into “search finite state tables under exact structural constraints”.
