Problem:
After the G3 color-0 surgery branch, decide what fresh cyclic odd-m template should replace post hoc local patching.

Current target:
Record the branch decision forced by the color-3 clean triangular criterion and the color-0 targeted-surgery failures.

Known assumptions:
- Color 3 admits a clean triangular skew-product frame with strict clock and unit orbitwise monodromy for all odd m>=5.
- The G3 color-0 pilot has clean frame + single base core + unit monodromy, but only an indegree defect packet.
- The most natural affine-pinned two-gate surgeries around the exact defect packets fail computationally at m=7, and the best failures remain bad at m=5 and m=9.

Attempt A:
  Idea:
  Keep G3 and repair the remaining indegree defect by natural affine-pinned two-gate surgeries.
  What works:
  The packetwise repair instructions are explicit: the q=1 packet wants an effective 2->3 change at layer 1, and the q=-1 packet wants an effective 2->3 change at layer 3.
  Where it fails:
  Natural exact-support and broadened pair-(2,3) two-gate families do not yield a good clean frame at m=7, and their best failures stay nonuniform across m=5,7,9.

Attempt B:
  Idea:
  Replace post hoc surgery by a fresh cyclic family in which clean-frame existence is built in as a hard design constraint for every color from the start.
  What works:
  The color-3 theorem supplies the target normal form: first return should be triangular with
    - one clean fiber coordinate z,
    - one strict clock s,
    - a section return U on two remaining coordinates,
    - unit orbitwise monodromy.
  The absolute clock S mod m and the relative coordinates (q_c,w_c,v_c,u_c) remain the right global scaffolding.
  Where it fails:
  No explicit all-color witness has been found yet in this new branch.

Candidate lemmas:
- [H] A viable odd-m family should impose clean-frame existence simultaneously for all colors, not recover it by later surgery.
- [H] The low-layer rules should be triangular in the relative frame: the chosen clean fiber must never feed back into the lower coordinates.
- [H] The next search space should exclude any gate family that destroys clean axes even when it mildly improves indegree.
- [H] The color-3 pattern suggests using cyclic low-layer rules with a built-in strict clock and delayed carry, rather than independent packet repairs.

Needed computations/search:
- Search fresh cyclic orbit-gate families with hard clean-frame constraints for all colors.
- For each color c, record only:
  1. clean frame existence,
  2. U_c cycle decomposition,
  3. orbitwise monodromy.
- Discard any candidate before full formula extraction if any color lacks a clean frame.

Next branching options:
1. Fresh cyclic family with layer-1/2/3 gates chosen to force a common clean fiber across all colors.
2. More restrictive search where the section return U_c is required to be a single cycle before looking at monodromy.
3. If no such family appears quickly, move to a still more symbolic CP/SAT formulation in the relative frame.

Claim status labels:
  [P] proved
  [C] computationally checked
  [H] heuristic/design principle
  [F] failed
  [O] open