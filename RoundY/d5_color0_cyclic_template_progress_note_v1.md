Problem:
Promote the next d=5 odd branch from “generic cyclic-family search” to a sharper color-0 diagnosis:
  find a cyclic low-layer template where color 0 admits
  clean frame -> strict clock -> U_0 -> monodromy,
then decide whether the remaining obstruction is base fracture, bad monodromy, or something else.

Current target:
1. Build a genuinely cyclic low-layer family around the corrected clock:
     layer 0 = sigma = (1,2,3,4,0),
     layers >= 4 = canonical.
2. For color 0, extract only:
   - clean-frame existence,
   - U_0 cycle-core structure,
   - cycle-orbit monodromy,
   and choose the next branch.
3. If possible, find a candidate where base fracture disappears.

Known assumptions:
- [P] The earlier color-3 result is now fixed as
    first-return reduction + clean-frame lemma + triangular skew-product criterion + color-3 instantiation.
- [P] The integer-sum low-layer plan is dead; the absolute modular clock S mod m is mandatory.
- [P] The natural relative coordinates for color c are
    (q_c,w_c,v_c,u_c) = (x_{c+1},x_{c+2},x_{c+3},x_{c+4}).
- [P] For a general color map f_c, the first return R_c on P_0 is a functional graph, not automatically a permutation.
  So from here on, “cycle decomposition” means true directed cycle-core lengths unless explicitly stated otherwise.
- [P] The old three-way branch criterion must be refined slightly:
    clean frame / base cycle-core / monodromy are still the main filters,
  but once those are good, indegree defects (= tree mass) become the next obstruction.

Attempt A:
  Idea:
  Search very small rotational orbit-gate templates:
    one orbit-gate on layers 1,2,3 over the base
      layer 0 = sigma, layers >=4 = id,
  and diagnose color 0 with true cycle-core data.
  What works:
  - [C] A one-gate seed already gives a clean frame and a strict clock for color 0.
  - [C] Representative seed:
      G1 = [{layer:3, pair:(0,3), type:line1, axis:1, residue:0}]
    gives for color 0:
      clean fiber axis = 1,
      strict clock axis = 0,
      U_0 has m fixed points,
      cycle monodromies all 0.
  - [C] So this seed reaches the triangular stage, but fails by massive base fracture before monodromy can help.
  Where it fails:
  - [F] U_0 fractures into m components immediately, so this is not a local monodromy problem.

Attempt B:
  Idea:
  Add one more aligned orbit-gate to repair the base dynamics while preserving the clean frame:
      G2 = G1 + [{layer:1, pair:(0,3), type:line1, axis:1, residue:2}]
  What works:
  - [C] For color 0 and odd m in {5,7,9,11}:
      clean fiber axis = 1,
      strict clock axis = 0,
      U_0 has exactly m cycle-core components, each of length (m+1)/2,
      cycle monodromies are all 1 (a unit).
  - [C] Hence monodromy is no longer the issue; the only visible failure is base fracture.
  Where it fails:
  - [F] U_0 still has m cycle-core components, so G2 is not yet in the local-surgery regime.

Attempt C:
  Idea:
  Add a third aligned orbit-gate aimed at collapsing the U_0 fracture:
      G3 = G2 + [{layer:2, pair:(2,4), type:line1, axis:3, residue:4}]
  What works:
  - [C] For color 0 and odd m in {5,7,9,11,13}:
      clean fiber axis = 1,
      strict clock axis = 0,
      U_0 has a single true cycle core,
      B_0 has a single true cycle core,
      R_0 has a single true cycle core,
      cycle monodromy is (m+1)/2, hence a unit.
  - [C] Observed exact pattern on the tested odd moduli:
      U_0 cycle-core length = (m^2 + 1)/2,
      B_0 cycle-core length = m (m^2 + 1) / 2,
      R_0 cycle-core length = m^2 (m^2 + 1) / 2,
      cycle monodromy = (m+1)/2.
  - [C] This is the first color-0 candidate where the whole
      clean frame -> U_0 -> monodromy
    pipeline succeeds all the way to a single cycle core.
  Where it fails:
  - [F/C] R_0 is still not a permutation:
      there remains a large indegree-0/2 defect set, so the unique cycle core has trees attached.
  - [C] For G3 on the tested odd moduli:
      R_0 indegree histograms are
        m=5:  indeg 0:50, 1:525, 2:50
        m=7:  indeg 0:98, 1:2205, 2:98
        m=9:  indeg 0:162,1:6237, 2:162
        m=11: indeg 0:242,1:14157,2:242
        m=13: indeg 0:338,1:27885,2:338
    i.e. the remaining obstruction is concentrated tree mass, not base fracture and not monodromy.
  - [C] The same 3-gate template does not repair the other colors at m=7:
      color 1: cycle-core lengths 141,13,13
      color 2: cycle-core lengths 209,6,6,6,6,6,6
      color 3: cycle-core lengths 343,343,343,343,294,294,34,34
      color 4: cycle-core lengths 343 five times
    and no clean frame appears for colors 1/2/3/4 in this candidate.

Candidate lemmas:
- [H] In the orbit-gate cyclic family, color-0 progress seems to come in three phases:
    Phase I: clean frame + strict clock appear,
    Phase II: monodromy becomes a unit but U_0 still fractures,
    Phase III: U_0 and B_0 collapse to a single cycle core, and only indegree defects remain.
- [C] The 3-gate candidate G3 is plausibly the correct “pre-Hamilton skeleton” for color 0:
    all global dynamical obstructions except bijectivity have disappeared.
- [H] The remaining repair should target the indegree-0/2 defect loci directly, not the base dynamics.
- [H] So for color 0, the main branch has changed:
    from witness redesign to local indegree surgery.

Needed computations/search:
- [C] Extract explicit first-return formulas for G3 on color 0,
  ideally in a frame where the indegree-defect locus is described by a few affine hyperplanes.
- [C] Locate the exact indegree-0 and indegree-2 sets of R_0 for G3 and test whether they come in matched affine packets of size 2m^2.
- [C] Search local surgeries around G3 that preserve:
    clean frame,
    single U_0 cycle core,
    unit monodromy,
  while reducing the indegree defect count.
- [C] The first sampled local-surgery pass (1000 random extra gates at m=7) found:
    1 sampled extra gate preserving the same single-core + unit-monodromy regime,
    0 sampled extra gates that strictly improved the R_0 bad-indegree count.
  So naive one-gate local surgery is not enough, but the branch itself still looks correct.

Next branching options:
1. color-0 local indegree surgery (current main branch):
   keep the 3-gate skeleton G3 fixed and solve only the 0/2 indegree defects.

2. color-0 formula extraction:
   derive explicit formulas for R_0, B_0, and U_0 of G3, then prove the observed lengths and monodromy before surgery.

3. color-1/4 branch later:
   keep them parked for now.
   G3 is a color-0 pilot skeleton, not a full 5-color witness.

Claim status labels:
  [P] proved
  [C] checked computationally
  [H] heuristic
  [F] failed in the current family/model
  [O] open

Branch decision:
- [C/H] For color 0, the correct next branch is now local surgery, but not on monodromy and not on the base cycle-core.
- [C/H] The remaining problem is tree mass / indegree non-bijectivity on top of an otherwise successful skew-product skeleton.
- [O] The full d=5 odd theorem remains open.
