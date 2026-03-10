Task ID:
D5-TAIL-AUTOMATON-BIT-EXTRACTION-001

Question:
On the residual tail family of `Theta_AB + phase_align`, extract a quotient-level one-bit refinement from the full residual automaton/hypergraph, rather than from an ad hoc arithmetic predicate in `delta`.

Purpose:
Use the exact hypergraph-optimal one-bit partitions for `m=5,7,9,11,13` as supervision signals, and determine whether they come from a smaller predecessor-tail automaton state. If yes, propose the corresponding cyclic-equivariant quotient bit. If not, produce evidence that one bit is insufficient and recommend the smallest two-bit tail grammar.

Inputs / Search space:
- Bundle: `/mnt/data/d5_theta_ab_phase_align_001.tar.gz`
- Saved strict-collapse field on `Theta_AB + phase_align`
- Residual hidden phase supports on nonzero `delta`
- Pilot/extended moduli: `m in {5,7,9,11,13}`
- Candidate refinement objects:
  - predecessor-tail automaton states
  - local tail-entry classes
  - oriented tail-phase classes
  - one-bit quotient factors derived from the residual automaton
- Do not restrict to affine predicates in `(q,w,u,delta)` unless they emerge from the automaton analysis.

Allowed methods:
- Build the residual tail automaton / compatibility hypergraph
- Exact hypergraph max-cut on the nonzero `delta` classes
- State-merging / partition-refinement / DFA-minimization style analysis
- Search for quotient-level one-bit factors whose induced colorings match the optimal cuts
- If needed, search for two-bit factors after proving or strongly evidencing one-bit insufficiency

Success criteria:
1. Construct the residual tail automaton/hypergraph explicitly.
2. Recover the exact unique optimal one-bit partitions for `m=5,7,9,11,13`.
3. Determine whether these partitions are induced by a common quotient-level one-bit factor.
4. If yes, state the factor precisely and explain how to add it to the quotient.
5. If no, give a minimal obstruction and propose the smallest credible two-bit tail grammar.

Failure criteria:
- Only rediscovers ad hoc `delta in A` predicates with no automaton interpretation.
- Uses only pairwise compatibility data and misses higher-order hyperedge effects.
- Produces a candidate bit that fails to reproduce the exact optimal partitions on the tested moduli.
- Leaves the one-bit vs two-bit decision unresolved.

Artifacts to save:
  - code
  - raw logs
  - summary report
  - residual automaton / compatibility hypergraph data
  - exact optimal partitions for each tested modulus
  - candidate one-bit / two-bit quotient factors
  - tables / plots / proof-supporting computations

Return format:
1. Executive summary
2. Exact residual automaton/hypergraph definition
3. Optimal partition data for `m=5,7,9,11,13`
4. Learned quotient factor(s), or one-bit obstruction
5. Suggested next quotient schema
6. Negative results for ruled-out factor families
7. Reproducibility notes

Reproducibility requirements:
- Fixed deterministic computations
- Save the exact residual hypergraphs / automata in machine-readable JSON
- Record all candidate quotient factors tested
- Include scripts that recompute the optimal partitions and verify induced colorings
- Log package versions / solver versions