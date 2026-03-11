Return the research note:

Problem:
After `Theta_AB + phase_align`, determine whether the residual tail obstruction is governed by a nontrivial equivalence relation on hidden phases `δ∈Z_m^*`, or whether the next bit is already a genuine 2-coloring problem on essentially discrete `δ`-states.

Current target:
Use the Session 19 `δ`-partition scan to extract the correct abstract object behind the scan, compare it with the pilot-optimal subsets for `m=5,7,9`, and turn that into the next quotient-search template.

Known assumptions:

* Session 17 gives two rigid pilot grammars on `Theta_AB + phase_align`; both freeze layers `2+` to identity, so the missing information lives in the tail grammar.
* Session 18 shows delayed copies of existing atoms help only marginally.
* Session 19 shows pure `δ`-partitions outperform affine-mixed predicates, but the best subset drifts with `m`.
* In the attached summary data, the pilot-optimal one-bit `δ`-cuts are:

  * `m=5`: `{1,2}`
  * `m=7`: `{1,3,5}`
  * `m=9`: `{1,2,5,6}`
* My new computations in this session used the attached summary JSON only, not raw state-support tables.

Attempt A:
Idea:
Reinterpret the Session 19 scan as an exact hidden-phase hypergraph cut problem.

What works:

* Let `T_m` be the residual multi-`δ` tail states of the strict-collapse representative, and for each such state `τ` let
  `D_τ ⊂ Z_m^*`
  be the set of hidden phases realizing that same visited quotient state.
* Then the baseline excess is exactly
  `E_0 = Σ_τ (|D_τ|-1)`.
* After adding a bit `b_A(δ)=1_{δ∈A}`, the excess becomes
  `E_A = Σ_τ [ (|D_τ∩A|-1)_+ + (|D_τ\A|-1)_+ ]`.
* Hence
  `E_A = E_0 - cut_H(A)`,
  where `cut_H(A)` is the number of residual supports `D_τ` that meet both colors. So the arbitrary `δ`-partition scan in Session 19 is already computing max-cuts of a hidden-phase compatibility hypergraph `H_m`.
* This gives a precise theorem-level meaning to “compatibility hypergraph / return automaton”:
  each residual tail support is a hyperedge.
* Immediate numerical consequence from the saved summaries:

  * `m=5`: best cut reduces excess `70→14`, so it cuts `56` residual supports.
  * `m=7`: best cut reduces excess `2673→1282`, so it cuts `1391` residual supports.
  * `m=9`: best cut reduces excess `12707→8150`, so it cuts `4557` residual supports.
* So the next bit should be chosen by hypergraph cut, not by an ad-hoc arithmetic ansatz.

Where it fails:

* The current bundle does not contain the raw state-level support table `τ ↦ D_τ`, only aggregated partition scores.
* So I can define the exact hypergraph and prove what objective it must satisfy, but I cannot materialize its full edge list from the attached files alone.

Attempt B:
Idea:
Use the recorded partition-score function itself to test whether any two nonzero phases are still indistinguishable, and to see whether a coarser phase quotient exists before coloring.

What works:

* Define the recorded cut-score
  `F_m(A) := E_0 - E_A`
  on the subsets present in the saved Session 19 summary.
* I checked the symmetry group of this recorded score function on the available subsets.
  Result:
  for `m=5,7,9`, the only observed symmetries are `id` and reversal `δ ↦ -δ`.
* Stronger: for every pair `δ≠δ'` in `Z_m^*`, the transposition `δ↔δ'` changes at least one recorded score.
  So no two nonzero phases are interchangeable modulo the pilot compatibility data already visible in the scan.
* Therefore the pilot data do **not** support a nontrivial coarse equivalence relation on hidden phase.
  The coarsest pilot hidden-phase quotient is effectively discrete: each nonzero `δ` already matters.
* This explains the Session 19 drift:
  there is no reason to expect one uniform arithmetic class such as “odd”, “quadratic residue”, or “first half” to win across all `m`.
  The scan is not revealing a simple arithmetic partition; it is revealing max-cuts on a nearly discrete hidden-phase hypergraph.
* It also explains why the pilot-optimal subsets differ:
  they are the max-cut colorings of `H_m`, not evaluations of one fixed arithmetic formula.
* A useful shadow computation:
  a nonnegative pairwise graph fit to the recorded cut scores is exact for `m=5`, very accurate on the recorded subsets for `m=7`, and still accurate on-record for `m=9`; its max-cut reproduces the pilot optimum for `m=5` and `m=7`, but not stably for `m=9`.
  So `m=9` is where genuine higher-order hyperedges or unrecorded subset data begin to matter.

Where it fails:

* “Discrete on pilot data” is not yet the same as “proved discrete from raw predecessor-tail local data”.
* For `m=9`, only part of the full subset score table is present in the summary, so the symmetry diagnosis is still evidence from recorded cuts rather than a full inversion of the hypergraph.

Candidate lemmas:

* [P] Hypergraph-cut identity:
  for any one-bit split `A⊂Z_m^*`,
  `E_A = E_0 - #{τ : 0<|D_τ∩A|<|D_τ|}`.
  So minimizing post-split excess is exactly hypergraph max-cut on the residual supports.
* [C] On the pilot scan data, the recorded score function has only reversal symmetry `δ↦-δ`; no nontrivial transposition of hidden phases preserves the recorded scores for `m=5,7,9`.
* [C] Consequently, no nontrivial merger of distinct nonzero phases is compatible with the pilot partition data already saved; the hidden-phase quotient is effectively discrete on the pilot moduli.
* [C] The pilot-optimal one-bit cuts are unique up to complement/reversal:
  `m=5:{1,2}`, `m=7:{1,3,5}`, `m=9:{1,2,5,6}`.
* [H] Therefore the next quotient bit should be learned as a max-cut coloring of the discrete hidden-phase support hypergraph, not by first searching for a small arithmetic phase-class quotient.
* [H] If one learned bit still leaves many residual supports, the natural continuation is recursive hypergraph bisection, i.e. a two-bit tail automaton, not another hand-designed arithmetic predicate.
* [F] “One fixed arithmetic family explains the next bit uniformly” is not supported by the pilot data.
* [F] “A delayed copy of current atoms is the missing information” is already ruled out by Session 18.

Needed computations/search:

* Extract the raw support table `τ ↦ D_τ` from the saved strict-collapse representative on `Theta_AB + phase_align` for `m=5,7,9`.
* Compute the incidence signature
  `I_m(δ) = (1_{δ∈D_τ})_{τ∈T_m}`.
* Quotient by identical signatures. My current diagnosis predicts singleton classes on pilot moduli, but this must be checked from raw data.
* Build the weighted hypergraph on these classes, with one hyperedge per residual tail support.
* Solve:
  primary objective = minimize exact post-split excess;
  secondary objective = lexicographically minimize residual support histogram from largest supports downward.
* Add the resulting color `tail_cut(δ)` as the next quotient bit.
* Re-run master-field search.
* If the refined quotient still freezes layers `2+`, recursively split the monochromatic residual hyperedges to obtain a two-bit tail automaton.

Next branching options:

1. Preferred:
   exact hypergraph extraction and max-cut bit on the residual tail supports.
2. If the one-bit rerun still collapses:
   recursive two-bit tail automaton obtained by a second max-cut on the remaining monochromatic supports.
3. No-go side branch:
   prove that any refinement constrained to existing atom vocabulary plus one affine equality in `(q,w,u,δ)` cannot realize the discrete pilot hidden-phase structure.

Claim status labels:
[P] [C] [H] [F] [O]

Bottom line:

* The Session 19 scan already has the right abstract object hidden inside it: a residual hidden-phase hypergraph.
* The pilot data do **not** suggest a nontrivial coarse phase equivalence; they suggest that nonzero `δ`’s are already individually distinguishable.
* So the next quotient bit should not be “find a nice arithmetic subset”.
  It should be:
  “extract the residual support hypergraph, solve its max-cut, and encode that coloring as `tail_cut`.”
* The drift of the optimal subsets with `m` is then not a bug; it is what one should expect when the hidden-phase quotient is essentially discrete and only reversal symmetry survives.
