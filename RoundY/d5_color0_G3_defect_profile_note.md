Problem:
Analyze the color-0 pilot cyclic candidate G3 for d=5 and decide whether the remaining obstruction is base fracture, monodromy, or pure local indegree defect.

Current target:
Extract an exact first-return formula for color 0 under G3, identify the clean frame and the defect packets, and record one-gate surgery evidence.

Known assumptions:
- Candidate G3 uses orbit-gates:
  layer 1: swap (0,3) on x1=2
  layer 2: swap (2,4) on x3=4
  layer 3: swap (0,3) on x1=0
- Color 0 relative coordinates are (q,w,v,u)=(x1,x2,x3,x4).

Attempt A:
  Idea:
  Derive d1,d2,d3 exactly and compare to brute-force first return.
  What works:
  For every tested odd m in {5,7,9,11,13}, the exact formula matches the computed first return on all m^4 states.
  Where it fails:
  The map is not injective; it has explicit indegree-0 and indegree-2 packets.

Attempt B:
  Idea:
  Classify the defect slice-by-slice in q and test whether a single extra orbit-gate can remove it while preserving clean frame + single U-cycle + unit monodromy.
  What works:
  The obstruction is fully localized in two source slices q=1 and q=m-1.
  Where it fails:
  Exhaustive single line1-gate search at m=7 gives no improvement, and a targeted single line2 search on the natural (x1,x3) surgery coordinates also gives no improvement.

Candidate lemmas:
- [P] Exact first-return formula for color 0 under G3:
    d1 = 2 if v=2; else 3 if q=1; else 0.
    d2 = 4 if (q,v)=(3,4); else 2 if q=3; else 3 if u=4; else 0.
    x3^(2) = v + 1_(d1=3) + 1_(d2=3).
    d3 = 2 if x3^(2)=0; else 3 if q=m-1; else 0.
  Therefore
    R0(q,w,v,u)=(
      q+1,
      w + 1_(d1=2)+1_(d2=2)+1_(d3=2),
      v + 1_(d1=3)+1_(d2=3)+1_(d3=3),
      u + 1_(d2=4)
    ).
- [P] Clean frame:
    w is a clean fiber coordinate; after quotienting by w, q is a strict clock.
- [P] Exact defect packets:
    Z0 = {(0,w,1,u)} ∪ {(2,w,3,u): u≠4} ∪ {(2,w,4,4)}
    D0 = {(0,w,0,u)} ∪ {(2,w,2,u): u≠4} ∪ {(2,w,3,4)}
  where Z0 is the indegree-0 set and D0 is the indegree-2 target set.
  Hence |Z0|=|D0|=2m^2 and the total bad indegree mass is 4m^2.
- [P] Slice maps:
    For q not in {1,m-1}, the induced map on (v,u) is bijective.
    For q=m-1, the defect is the universal packet v'=1 missing, v'=0 doubled.
    For q=1, the defect is the packet v'=3+1_(u=4) missing, v'=2+1_(u=4) doubled.
- [C] At m=7, exhaustive one-gate search over all 1047 extra orbit-line1 gates yields:
    same single-core/unit-monodromy candidates = 0,
    strict bad-indegree improvements = 0.
- [C] At m=7, targeted one-gate search over all 140 natural orbit-line2 gates on (x1,x3) yields:
    same single-core/unit-monodromy candidates = 0,
    strict bad-indegree improvements = 0.

Needed computations/search:
- Search for two-gate affine-pinned surgery, probably with one gate aimed at q=1 and one at q=m-1.
- Prefer line2 conditions on (x1,x3) or equivalent relative tests, since the packets are v-line collisions inside two q-slices.
- If that fails, move to a fresh cyclic family rather than keep patching G3.

Next branching options:
1. Two-gate surgery on G3, explicitly targeting the q=1 and q=m-1 defect slices.
2. Derive a reduced 2D normal form for the quotient U and classify which local modifications preserve the single core and unit monodromy.
3. Abandon G3 if two-gate surgeries still fail, and impose clean-frame existence as a hard constraint in a new cyclic ansatz.

Claim status labels:
  [P] proved
  [C] computationally verified
  [H] heuristic
  [F] failed
  [O] open
