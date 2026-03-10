Task ID:
D5-FRESH-CYCLIC-QCLOCK-VFIBER-001

Question:
Search for a fresh odd-m cyclic low-layer family for d=5 such that every color c has a built-in triangular first-return frame in the relative coordinates
(q_c,w_c,v_c,u_c)=(x_{c+1},x_{c+2},x_{c+3},x_{c+4}),
with clean fiber v_c and strict clock q_c.

Purpose:
Replace post hoc witness repair by a family designed from the start to satisfy:
1. clean frame for all colors,
2. single-cycle section return U_c for all colors,
3. unit orbitwise monodromy for all colors,
4. only then address bijectivity / indegree defects.

Inputs / Search space:
- Dimension d=5.
- Odd moduli m in {5,7,9} for pilot search; then test {11,13}.
- Absolute clock S(x)=x_0+...+x_4 mod m.
- Relative coordinates for color c:
    (q_c,w_c,v_c,u_c)=(x_{c+1},x_{c+2},x_{c+3},x_{c+4}).
- Layer 0 fixed to sigma(c)=c+1.
- Layers 4,...,m-1 fixed to canonical c.
- Layers 1,2,3 defined by finite state tables on affine-pinned states of (q_c,w_c,u_c).
- Allowed affine atoms:
    q=a,
    w=a,
    u=a,
    q+w=a,
    q+u=a,
    w+u=a,
    q+w+u=a,
  with residues a in {0,1,-1,2,-2} mod m.
- Allowed color-c outputs on layers 1,2,3:
    only {c, c+2, c+3, c+4}; never c+1.
- Supports must never depend on v_c.
- Full rule must be rotationally covariant under simultaneous index shift.

Allowed methods:
- CP-SAT / SAT / exact backtracking / beam search.
- Explicit first-return computation on P_0.
- Cycle-core and indegree analysis of functional graphs.
- Symbolic extraction of R_c and U_c after candidates are found.
- Symmetry reduction and caching across cyclic states.

Success criteria:
1. For m=5,7,9, every color c admits the built-in frame:
   - v_c is a clean fiber,
   - q_c is a strict clock.
2. For m=5,7,9, every section return U_c is a single cycle.
3. For m=5,7,9, every unique U_c-orbit has monodromy a unit mod m.
4. Preferably, at least one candidate also has no indegree defect for all colors at m=5 and m=7.
5. If no perfect candidate is found, return the Pareto frontier ranked by
   (all colors framed, all U_c single-cycle, all monodromies unit, smallest indegree defect).

Failure criteria:
- No candidate in the chosen affine-atom family gives all 5 colors a clean frame at m=5 and m=7.
- Or, all such framed candidates still fail because some U_c fractures for every tested m.
- Or, all such candidates have nonunit monodromy in some color for every tested m.

Artifacts to save:
  - code
  - raw logs
  - summary report
  - discovered examples / counterexamples
  - tables / plots / proof-supporting computations
  - the finite state tables f_L for each surviving candidate
  - extracted formulas for R_c and U_c where available

Return format:
1. Executive summary.
2. Exact state-table rules for the best candidates.
3. For each candidate and each color c:
   - clean frame yes/no,
   - clock axis,
   - U_c cycle decomposition,
   - orbitwise monodromy,
   - indegree histogram of R_c.
4. Cross-modulus stability table for m=5,7,9,11,13.
5. Minimal counterexamples for failed subfamilies.
6. Suggested proof skeleton for the strongest surviving candidate.

Reproducibility requirements:
- Fixed random seeds if any heuristic search is used.
- Deterministic verification scripts for R_c, U_c, monodromy, and indegree histograms.
- Full record of the affine atom set and every symmetry reduction used.
- Save every frontier-improving candidate.
- Save machine-readable candidate tables (JSON/CSV).
- Record Python and solver versions.
