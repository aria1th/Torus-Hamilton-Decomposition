Task ID:
D5-TAIL-CUT-QUOTIENT-RERUN-001

Question:
Using the exact residual hidden-phase hypergraph already extracted from the strict-collapse representative on `Theta_AB + phase_align`, what is the coarsest exact hidden-phase quotient on the pilot moduli `m in {5,7,9}`, and does adding the resulting exact pilot `tail_cut` bit to the quotient search produce any structural gain beyond the current phase-align schema?

Purpose:
Close the loop from the Session 19 partition scan to an actual quotient refinement. The hypergraph object is now known exactly, so the next task is not to rediscover it, but to:

1. compute the exact hidden-phase equivalence classes from incidence signatures,
2. export the exact pilot max-cut colorings as a concrete tail bit,
3. rerun the refined quotient search / validation, and
4. decide whether one pilot bit buys anything, or whether the branch should move directly to a two-bit tail grammar.

Inputs / Search space:
- exact hypergraph extraction artifact:
  - `artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_extract.json`
  - `artifacts/d5_tail_automaton_bit_extraction_001/data/hypergraph_optimize.json`
  - `artifacts/d5_tail_automaton_bit_extraction_001/data/factor_search_summary.json`
- saved strict-collapse representative:
  - `artifacts/d5_theta_ab_phase_align_001/data/best_strict_collapse_field.json`
- existing phase-align search/validation code:
  - `scripts/torus_nd_d5_master_field_quotient_family.py`
  - `scripts/torus_nd_d5_theta_ab_phase_align_search.py`
  - `scripts/torus_nd_d5_theta_ab_phase_align_validate.py`
- pilot moduli `m in {5,7,9}`
- optional stability moduli `m in {11,13}` for post hoc checks only

Known facts to treat as established:
- The exact residual support hypergraph has already been extracted.
- The unique optimal one-bit cuts modulo complement are:
  - `m=5`: `{1,2}`
  - `m=7`: `{1,3,5}`
  - `m=9`: `{1,2,5,6}`
  - `m=11`: `{1,2,6,7,8}`
  - `m=13`: `{1,4,5,7,8,10}`
- Pair-graph and antisymmetric surrogates agree through `m=11` and fail first at `m=13`.
- No tested common one-bit automaton factor on current / predecessor / successor / entry windows reproduces the exact optimal partitions globally on `m=5,7,9,11,13`.
- Therefore a uniform theorem-level arithmetic `tail_cut(delta)` is not currently supported. The realistic next test is an exact pilot lookup bit.

Allowed methods:
- direct use of the saved support table `tau -> D_tau`
- computation of incidence signatures `I_m(delta) = (1_{delta in D_tau})_tau`
- quotient by identical incidence signatures
- exact pilot lookup tables `tail_cut_m(delta)` from the saved hypergraph optima
- exact rerun of the quotient search / validation with the lookup bit wired into the schema
- deterministic branch-and-bound / ILP / brute force on pilot moduli
- exact post-split excess and support-histogram recomputation

Success criteria:
1. Compute the exact hidden-phase equivalence classes from identical incidence signatures on `m=5,7,9`.
2. State explicitly whether those classes are all singletons on the pilot range.
3. Export the exact pilot one-bit lookup tables `tail_cut_5`, `tail_cut_7`, `tail_cut_9`.
4. Add the lookup bit to the quotient schema in an explicit, reproducible way.
5. Re-run the refined quotient search and validation on the pilot range.
6. Report whether the refined quotient still freezes layers `2+`, or whether the return/support statistics improve in a structurally meaningful way.
7. If it still collapses, give the sharpest data-backed no-go statement and the smallest credible two-bit continuation.

Failure criteria:
- cannot recover the incidence-signature classes from the saved exact hypergraph data
- pilot signature classes are incompatible with any explicit exact lookup-bit implementation
- the exact pilot lookup bit yields no structural gain over the current phase-align schema
- the rerun still exhibits complete layer-`2+` freeze with no sharper diagnosis than before

Artifacts to save:
- code
- raw logs
- summary report
- incidence-signature tables
- hidden-phase equivalence classes
- exact pilot lookup tables `tail_cut_m`
- refined quotient search outputs
- validation outputs
- explicit negative results if the lookup bit fails

Return format:
1. Exact definition of residual states `tau`
2. Incidence-signature quotient on `m=5,7,9`
3. Exact pilot lookup tables `tail_cut_m`
4. Refined quotient/search implementation details
5. Refined search outcome
6. Validation outcome
7. Sharpest no-go statement, or concrete structural gain
8. Recommended next branch

Reproducibility requirements:
- deterministic signature extraction from the saved hypergraph JSON
- fixed solver seeds
- saved incidence-signature class tables in JSON/CSV
- saved exact pilot lookup tables and objective values
- explicit scripts that recompute all reported excess / histogram / validation statistics
- a tar bundle containing code plus artifact outputs
