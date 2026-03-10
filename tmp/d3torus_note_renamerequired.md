Problem:
After `Theta_AB + phase_align`, determine the next refinement object for the residual hidden tail phase.
The immediate question is no longer "which affine predicate looks good?" but:
can the residual one-bit problem be written exactly as a finite combinatorial optimization object, and if so, what does that object say?

Current target:
Write the residual nonzero-phase problem as a weighted hypergraph max-cut on the hidden phase residues
\[
\Delta_m:=\{1,2,\dots,m-1\}.
\]
Then compute the exact optimal 2-coloring for the actual saved strict-collapse field on
`Theta_AB + phase_align` for
\[
m=5,7,9,11,13.
\]

Known assumptions:
- On the saved strict-collapse field of `Theta_AB + phase_align`, the representative-color return law on the pilot range is
  \[
  R_0(q,w,v,u)=(q+1,w,v+1,u),
  \]
  so the hidden phase
  \[
  \delta:=v-q \pmod m
  \]
  is preserved during the frozen tail.
- The phase-align refinement already split the aligned branch `delta=0` from the nonzero branch.
- What remains is a family of quotient states whose nonzero hidden-phase supports are subsets
  \[
  S_s \subseteq \Delta_m,\qquad |S_s|\ge 2.
  \]

Attempt A:
  Idea:
  Formalize the residual one-bit refinement problem exactly.
  For each residual phase-align state `s`, define a hyperedge
  \[
  S_s\subseteq \Delta_m
  \]
  equal to its nonzero hidden-phase support.
  For a proposed bit `\chi:\Delta_m\to\{0,1\}`, the state `s` is split iff `\chi` is nonconstant on `S_s`.

  What works:
  - This gives an exact identity:
    if the unsplit excess contributed by `s` is `|S_s|-1`, then after a one-bit split it becomes
    \[
    |S_s|-\#\{\chi(S_s)\},
    \]
    so the excess drops by exactly `1` iff `S_s` is cut by the 2-coloring.
  - Therefore minimizing total residual excess is **exactly equivalent** to maximizing the number of cut hyperedges in this weighted hypergraph.
  - So the next-bit problem is no longer heuristic: it is an exact finite optimization object.

  Where it fails:
  - The optimizer need not come from any simple arithmetic predicate in `delta`.
  - The hyperedges have sizes larger than `2`, so pairwise graph heuristics can lose information.

Attempt B:
  Idea:
  Compute the exact hypergraph-optimal 2-coloring for the actual saved strict-collapse field on
  `Theta_AB + phase_align`, and compare it with the pair-cooccurrence graph max-cut.

  What works:
  - Exact hypergraph-optimal partitions are **unique** for
    \[
    m=5,7,9,11,13.
    \]
  - The unique best subsets are:
    - `m=5`: `{1,2}`
    - `m=7`: `{1,3,5}`
    - `m=9`: `{1,2,5,6}`
    - `m=11`: `{1,2,6,7,8}`
    - `m=13`: `{1,4,5,7,8,10}`
  - The optimality gaps in total excess are:
    - `m=5`: `12`
    - `m=7`: `14`
    - `m=9`: `28`
    - `m=11`: `13`
    - `m=13`: `1`
  - For `m=5,7,9,11`, the simpler weighted **pair graph** already has the same unique max-cut.
  - At `m=13`, the graph max-cut changes:
    - graph best: `{1,2,5,6,9,10}`
    - true hypergraph best: `{1,4,5,7,8,10}`
    and the graph-best partition is worse by `1` in total excess.
  - So higher-order tail hyperedges become genuinely visible by `m=13`.

  Where it fails:
  - The optimal subsets drift strongly with `m`.
  - There is still no theorem-level uniform arithmetic description of the best `delta`-bit.
  - Hence the exact finite object is now clear, but the right *uniform* quotient refinement has not yet been extracted.


Attempt C:
  Idea:
  Test whether the learned one-bit partition is still compatible with the natural negation symmetry
  \[
  \delta \leftrightarrow -\delta.
  \]
  Concretely, restrict to antisymmetric subsets `A` satisfying
  \[
  A \cap (-A)=\varnothing,\qquad A\cup(-A)=\Delta_m.
  \]

  What works:
  - For
    \[
    m=5,7,9,11,
    \]
    the unrestricted hypergraph optimum is already antisymmetric:
    - `m=5`: `{1,2}`
    - `m=7`: `{1,3,5}`
    - `m=9`: `{1,2,5,6}`
    - `m=11`: `{1,2,6,7,8}`
  - At
    \[
    m=13,
    \]
    this breaks for the first time.
    The unrestricted optimum is
    `{1,4,5,7,8,10}`,
    while the best antisymmetric partition is
    `{1,3,5,6,9,11}`,
    worse by `27` in total excess.
  - So `m=13` is the first tested modulus where the best one-bit split must distinguish more than a pure `delta` vs `-delta` orientation class.

  Where it fails:
  - This still does not produce a theorem-level uniform formula for the next bit.
  - But it does rule out a large and natural class of candidate tail bits.


Candidate lemmas:
- [P] On a fixed residual-support family `{S_s}`, the one-bit refinement problem is equivalent to weighted hypergraph max-cut on `\Delta_m`.
- [C] For the actual saved strict-collapse field on `Theta_AB + phase_align`, the hypergraph-optimal partition is unique for `m=5,7,9,11,13`.
- [C] The pair-cooccurrence graph suffices up to `m=11` but fails first at `m=13`; therefore higher-order hyperedges matter.
- [C] The hypergraph optimum is antisymmetric under `\delta\leftrightarrow -\delta` for `m=5,7,9,11`, but this symmetry breaks first at `m=13`.
- [H] The next refinement should be learned from the residual **tail hypergraph / automaton**, not from ad hoc affine predicates in `(q,w,u,delta)` and not from pairwise data alone.
- [H] Since the `m=13` optimum is no longer antisymmetric, the next useful tail bit likely has to encode an *oriented* tail-entry class, not merely an unsigned phase class.

Needed computations/search:
- Build the residual tail automaton / hypergraph at the quotient level, not only as a `delta`-support summary.
- Identify whether the unique hypergraph-optimal pilot partitions come from a smaller predecessor-tail automaton state.
- Test whether a learned automaton bit reproduces these partitions on `m=5,7,9,11,13`.
- If no one-bit automaton factor does so stably, move to a two-bit tail grammar.

Next branching options:
1. `automaton-bit extraction` branch:
   derive the best one-bit quotient refinement from the residual tail automaton, using the hypergraph optimum as the target signal.
2. `one-bit no-go` branch:
   prove that no uniform pure-`delta` bit can explain the unique optimal pilot partitions.
3. `two-bit tail grammar` branch:
   if the automaton-derived one-bit factor is still unstable (especially given the `m=13` near-tie), move directly to a two-bit tail-state quotient.

Claim status labels:
  [P] exact finite reformulation / proof from the support-family definition
  [C] computation-backed claim for the actual saved strict-collapse field on `Theta_AB + phase_align`
  [H] structural diagnosis / next-branch heuristic
  [F] refuted direction
  [O] open

Bottom line:
- [P] The residual one-bit problem after `Theta_AB + phase_align` is now pinned down exactly as a weighted hypergraph max-cut on the nonzero hidden phases.
- [C] The optimal 2-coloring is unique for `m=5,7,9,11,13`, but it drifts with `m`, stops being visible from the pair graph at `m=13`, and also ceases to be negation-antisymmetric there.
- [H] So the next useful quotient refinement should be learned from the full residual tail hypergraph / automaton, not from a guessed arithmetic `delta`-predicate and not from pairwise compatibility alone.