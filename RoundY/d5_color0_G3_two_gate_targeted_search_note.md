Problem:
Assess whether the color-0 pilot template G3 can be repaired by the most natural affine-pinned two-gate surgeries suggested by the exact defect packets.

Current target:
Search two targeted local-surgery families at m=7 and decide whether G3 should be kept or abandoned for general odd-m work.

Known assumptions:
- G3 already has clean frame, single U-core, and unit monodromy for color 0; only indegree defect remains.
- The exact defect packets suggest two ideal packetwise repairs:
  - at q=1, v=2: change the effective layer-1 action from 2 to 3;
  - at q=m-1, x3^(2)=0: change the effective layer-3 action from 2 to 3.

Attempt A:
  Idea:
  Search the exact-support family with two added orbit-line2 gates on the two ideal packets:
    layer 1: condition (x1,x3)=(1,2),
    layer 3: condition (x1,x3)=(-1,0),
  while varying the transposition pairs independently.
  What works:
  Exhaustive search over 100 pair choices was completed at m=7.
  Where it fails:
  No candidate has a good frame; no candidate preserves the single-core/unit-monodromy structure and improves bad indegree.
  Best bad indegree count is 195 (base is 196), but this candidate has R_num_cycles=12 with top cycle lengths [7, 7, 7, 7, 7, 7, 7, 7, 7, 7].

Attempt B:
  Idea:
  Keep the transposition pair fixed at (2,3), but broaden the supports to a natural affine-pinned family around the packet coordinates:
    layer 1 supports built from q=1 together with v or u tests,
    layer 3 supports built from q=-1 together with v=0 or u=4 tests.
  What works:
  Exhaustive search over 126 support pairs was completed at m=7.
  Where it fails:
  No candidate has a good frame, and no candidate even matches the base bad-indegree count 196.
  Best bad indegree count is 248 with R_num_cycles=4 and top cycle lengths [6, 6, 6, 6].

Candidate lemmas:
- [C] The natural two-gate affine-pinned surgery family suggested by the exact packets does not repair G3 at m=7.
- [H] This strongly suggests that G3 patching is not the right uniform odd-m template.
- [H] The next viable branch is a new cyclic family with clean-frame existence imposed from the outset, rather than post hoc surgery.

Needed computations/search:
- Check whether any of the best exact-support failures extend coherently to m=5,9 (for negative evidence only).
- Start a fresh cyclic-family search with hard clean-frame constraints for all colors, not just color 0.

Next branching options:
1. Abandon G3 patching and design a new cyclic family guided by the color-3 triangular criterion.
2. As a last diagnostic only, test the handful of best exact-support failures at m=5 and m=9 to see whether the failure profile is stable.

Claim status labels:
  [P] [C] [H] [F] [O]
Cross-check on small odd m:
- The best exact-support failures remain bad at m=5 and m=9 as well: they have no clean axes and no good frame in all tested cases.
- Candidate ((0,2),(0,2)) has (bad,R_num_cycles) = (99,7) at m=5, (195,12) at m=7, (322,16) at m=9.
- Candidate ((2,4),(0,2)) has (bad,R_num_cycles) = (111,4) at m=5, (214,1) at m=7, (352,2) at m=9.
- Candidate ((0,2),(2,4)) has (bad,R_num_cycles) = (110,2) at m=5, (215,2) at m=7, (350,2) at m=9.

Branch decision:
- [C] The natural affine-pinned two-gate repair program for G3 does not produce a clean-frame uniform odd-m template.
- [H] This is strong evidence to abandon post hoc G3 surgery and move to a fresh cyclic family with clean-frame constraints built in from the start.
