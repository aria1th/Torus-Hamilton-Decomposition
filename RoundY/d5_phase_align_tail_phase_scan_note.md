Problem:
After `Theta_AB + phase_align`, identify what kind of one-bit refinement should come next.
The question is no longer whether more anchor freedom helps; it is whether the residual collapse is best attacked by
(1) another delayed copy of existing atoms, or
(2) a new bit that cuts the hidden tail phase itself.

Current target:
Use the strict-collapse representative on `Theta_AB + phase_align` as a diagnostic object and scan one-bit refinements that depend on the hidden tail phase
\[
\delta := v-q \pmod m.
\]
The immediate goal is *not* to produce the final quotient, but to decide whether the next bit should be:
- a predecessor/current-atom hybrid, or
- a genuine tail-phase class bit.

Known assumptions:
- On the pilot range `m=5,7,9`, the saved strict-collapse grammar has exact return law
  \[
  R_0(q,w,v,u)=(q+1,w,v+1,u),
  \]
  so `delta=v-q` is preserved during the frozen tail.
- The simple predecessor-bit scan already showed that one-step-lagged copies of current atoms help only slightly and do not remove the residual multi-delta structure.
- The saved strict-collapse field is only a pilot diagnostic object, not a theorem for all feasible fields on the quotient.

Attempt A:
  Idea:
  Scan *all one-bit partitions of the hidden nonzero phase set* `delta in Z_m^*` for `m=5,7,9` and measure how much residual multi-delta collision remains after splitting each visited quotient state by that bit.

  What works:
  - The optimal pure-delta partitions are substantially stronger than the previously scanned predecessor-atom bits.
  - Best arbitrary delta partitions found:
    - `m=5`: `{1,2}` gives total excess `14` (baseline `70`).
    - `m=7`: `{1,3,5}` gives total excess `1282` (baseline `2673`).
    - `m=9`: `{1,2,5,6}` gives total excess `8150` (baseline `12707`).
  - In all three pilot moduli, these best delta-partitions remove the "full nonzero support" residual states entirely.

  Where it fails:
  - The pilot-optimal subset drifts with `m`; there is no single obvious arithmetic subset `A subset Z_m^*` that wins uniformly on `m=5,7,9`.
  - So the data do *not* support a theorem of the form "the next bit is simply delta in A" for one fixed closed-form family `A`.

Attempt B:
  Idea:
  Test whether mixing `delta` with current coordinates `(q,w,u)` helps. Concretely, scan affine equality bits
  \[
  a q + b w + c u + \delta \equiv t \pmod m,
  \qquad a,b,c\in\{-1,0,1\},\ t\in\{-2,-1,0,1,2\}.
  \]

  What works:
  - Among these affine mixed predicates, the best performers are actually the *pure delta* ones:
    - `delta = ±2` performs best in this family,
    - then `delta = ±1`,
    - then other mixed predicates.
  - This is direct evidence that the missing information lives in the tail phase itself rather than in a new low-weight affine combination with `(q,w,u)`.

  Where it fails:
  - Even the best affine equality predicates remain weaker than the best arbitrary delta partitions.
  - So a single affine equality of the form `aq+bw+cu+delta=t` is not enough to explain the pilot-optimal split.

Candidate lemmas:
- [C] On the strict-collapse representative, pure delta-partitions outperform the previously scanned simple predecessor bits.
- [C] In the affine family `aq+bw+cu+delta=t`, the best candidates are pure-delta equalities; adding `q,w,u` does not improve the scan.
- [C] No single obvious uniform arithmetic delta-bit emerges from `m=5,7,9`.
- [H] Therefore the next useful refinement should be a *tail-phase class bit* learned from the return automaton / compatibility hypergraph, not a delayed copy of current atoms and not an ad hoc affine mix with `(q,w,u)`.

Needed computations/search:
- Build the compatibility hypergraph / return automaton on the residual tail family and ask for the coarsest 2-coloring of hidden phase classes that separates the collapse motifs.
- In particular, extract the equivalence relation on nonzero `delta` induced by identical predecessor-tail local data.
- Compare that automaton-derived partition against the pilot-optimal arbitrary delta partitions for `m=5,7,9`.

Next branching options:
1. `automaton-derived tail bit` branch:
   compute the minimal hidden-phase 2-coloring forced by the residual compatibility data, then use that as the next quotient bit.
2. `tail no-go` branch:
   prove that any quotient refinement built only from existing atoms plus one affine equality in `(q,w,u,delta)` still leaves the residual collapse.
3. `two-bit tail grammar` branch:
   if the automaton-derived partition is not consistent across pilot moduli, move directly to a two-bit tail-state quotient.

Claim status labels:
  [P] exact derivation from a fixed return law / finite scan definition
  [C] computation-backed claim on the strict-collapse representative
  [H] structural diagnosis / next-branch heuristic
  [F] refuted direction on the scanned family
  [O] open

Bottom line:
- [C] The next missing information is genuinely a hidden tail-phase class, not another copy of the existing atom vocabulary.
- [C] But the pilot data do not point to one obvious closed-form arithmetic bit such as `delta=1`, `delta=±1`, or `delta` odd that works uniformly best.
- [H] So the next refinement should come from the residual compatibility automaton itself: learn the tail-phase partition first, then encode it as the next quotient bit.
