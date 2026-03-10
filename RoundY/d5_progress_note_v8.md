# d=5 progress note v8 — color 0 analysis

Problem:
Prove the `d=5` case: for every `m >= 3`, the directed torus
`D_5(m)=Cay((Z_m)^5,{e_0,e_1,e_2,e_3,e_4})` admits a decomposition into five arc-disjoint directed Hamilton cycles.

Current target:
Classify the fixed 26-move witness for **color 0** on `P0={S=0}`, and isolate:
- exact obstruction mechanisms,
- exact low-layer formulas,
- and any uniform non-Hamilton branches.

Known assumptions:
- [P] For the fixed witness, color 3 is Hamilton for every odd `m >= 5`.
- [P] For the fixed witness, color 2 is Hamilton iff `gcd(m,3)=1`.
- [P] For the fixed witness, color 1 has an explicit fixed-set obstruction for every `m >= 6`.
- [P] Therefore the remaining unresolved colors of the fixed witness are `0` and `4`.

Attempt A:
  Idea:
  Work directly on `P0` in color-0 relative coordinates
  `(q,w,v,u)=(x_1,x_2,x_3,x_4)`, so `x_0=-(q+w+v+u)`.
  Because the witness is supported only on layers `0,1,2,3`, the entire first return is determined by the four-step prefix `(d0,d1,d2,d3)`.

  What works:
  - [P] For every `m >= 6`, the color-0 prefix has the exact form
    `d0=0` and

    `d1 = 3` if `q=2, w=0, q+v+u ≡ 0`,
    `d1 = 4` if `q=2` and not the previous case,
    `d1 = 2` if `q != 2, u=1`,
    `d1 = 0` otherwise.

    `d2 = 2` if `q=0, u=4, w+v ≡ m-4`,
    `d2 = 3` if `q=0, u=4, w+v \not\equiv m-4`,
    `d2 = 1` on the three carry branches
      - `q != 2, u=2`,
      - `q != 2, u=0, v=4`,
      - `q=2` with either `u=1`, or `u=m-1, v=4`, or the special line `w=0, v+u ≡ m-2, u=2`,
    and `d2 = 0` otherwise.

    `d3` is determined from the layer-3 prestate:
      let
      `x0^(3) = -(q+w+v+u) + 1 + 1_(d1=0) + 1_(d2=0)`,
      `x2^(3) = w + 1_(d1=2) + 1_(d2=2)`.
      Then
      `d3 = 2` if `x0^(3)=4`,
      `d3 = 1` if `x0^(3) != 4` and `x2^(3)=2`,
      `d3 = 3` otherwise.

  - [P] Hence for every `m >= 6`,
    `R_0(q,w,v,u) = (q+α, w+β, v+γ, u+δ)` with
      `α = 1_(d2=1) + 1_(d3=1)`,
      `β = 1_(d1=2) + 1_(d2=2) + 1_(d3=2)`,
      `γ = 1_(d1=3) + 1_(d2=3) + 1_(d3=3)`,
      `δ = 1_(d1=4)`.

  - [P] These formulas were matched against the actual witness by direct simulation for every `m = 6,7,...,16`.

  Where it fails:
  - [O] The odd-`m` global orbit structure of this exact map is still not classified.
  - [O] No uniform 1D or 2D odometer reduction for all odd `m` has been extracted yet.

Attempt B:
  Idea:
  Use the exact formulas to isolate a clean invariant family for even `m`, and a “background odometer skeleton” on the generic region for odd `m`.

  What works:
  - [P] For every even `m >= 6` and every `w != 2`,
    the set
    `L_w = {(0,w,v,4): v ≡ w+1 (mod 2)}`
    is invariant under `R_0`, and on this set
    `R_0(0,w,v,4) = (0,w,v+2,4)`.

    Reason:
    on `L_w`, one has `d1=0`, `d2=3`, and because `w+v` is odd while `m-4` and `m-6` are even,
    the exceptional `d2=2` and `d3=2` branches never fire; also `w != 2` kills the `d3=1` branch.

  - [P] Therefore each `L_w` is a directed cycle of length `m/2`, so color 0 is **not Hamilton for every even `m >= 6`**.

  - [P] On the generic region
    `q not in {0,2}` and `u not in {0,1,2,4,m-1}`,
    one has `d1=d2=0`, and therefore
      - `d3=2` exactly when `q+w+v+u ≡ m-1`,
      - `d3=1` exactly when `w=2` and `q+w+v+u \not\equiv m-1`,
      - `d3=3` otherwise.
    So away from the defect hyperplanes the map is the clean carry skeleton
      - carry `w` when the affine sum hits `m-1`,
      - carry `q` when `w=2`,
      - otherwise advance `v`.

  Where it fails:
  - [O] For odd `m`, the exceptional branches at
    `q in {0,2}` and `u in {0,1,2,4,m-1}`
    still reconnect the generic skeleton in a nontrivial way.
  - [C] Computation shows non-Hamiltonicity for many odd `m`, but the exact obstruction theorem is still missing.

Candidate lemmas:
- [P] Exact color-0 first-return formula above for every `m >= 6`.
- [P] Even-`m` invariant family:
  for every even `m >= 6`, each `L_w` (`w != 2`) is an `m/2`-cycle.
- [P] Consequently color 0 is non-Hamilton for every even `m >= 6`.
- [P] Generic-region lemma:
  outside `q in {0,2}` and `u in {0,1,2,4,m-1}`, the map reduces to the three-branch carry skeleton described above.
- [H] The odd-`m` obstruction should come from the way the exceptional `q/u` branches splice several large generic carry blocks together.

Needed computations/search:
- [C] Build a compressed automaton on the exceptional set
  `E = {q in {0,2} or u in {0,1,2,4,m-1}}`
  together with the generic carry skeleton, and compute its induced return on one generic section.
- [C] Search for an explicit proper invariant subset for odd `m` using the exact `R_0` formula, not the full witness simulation.
- [C] Check whether color 4 is affine-conjugate or semi-conjugate to color 0 under a coordinate reversal; if yes, solve both at once.
- [C] Classify the odd-`m` cycle counts for more `m` using the exact formula, then look for arithmetic signatures.

Next branching options:
1. **Odd color-0 obstruction branch**:
   compress the exact `R_0` map to a return on the exceptional set and try to prove non-transitivity.
2. **Color-4 comparison branch**:
   derive the exact color-4 formula and test whether it is conjugate to color 0.
3. **Repair branch**:
   treat the exact color-0 obstruction as a design spec for how a new affine-pinned repair must alter the bad `q/u` branches without breaking colors 2 and 3.

Claim status labels:
  [P] rigorously closed
  [C] computation only
  [H] heuristic / design principle
  [F] disproved or structurally blocked
  [O] open

Current color-0 status:
- [P] exact first-return formula for all `m >= 6`,
- [P] explicit non-Hamilton obstruction for every even `m >= 6`,
- [C] odd-`m` non-Hamilton cycle counts verified for
  `m = 7,9,11,13,15,17,19,21,23`,
- [O] uniform odd-`m` theorem still open.
