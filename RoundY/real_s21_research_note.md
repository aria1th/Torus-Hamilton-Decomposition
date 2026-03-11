# Session 21 continuation — active tail grammar reading

Return the research note:

## Problem
Construct a 5-color Hamilton decomposition of
\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]
via a cyclic-equivariant master permutation field, and break the remaining dynamical degeneracy after the `Theta_AB + phase_align + tail_cut` refinement.

## Current target
Use the positive Codex result to update the bottleneck and choose the next constructive branch.

## Known assumptions
- The passive refined quotient already contains nonlifted same-preference witnesses on the pilot range `m=5,7,9`.
- Exact divergence result:
  - preference score remains `32176`
  - changed pilot states vs lifted field: `22806`
  - status: `OPTIMAL`
- Two pilot witnesses were found:
  - `same_preference_divergence`
    - layer `2`: `12340`
    - layer `3`: `12340`
    - layer `4+`: `01234`
    - clean frame holds on `m=5,7,9`
    - strict clock fails on `m=5,7,9`
  - `best_divergent_field`
    - layer `2`: `23401`
    - layer `3`: `34012`
    - layer `4+`: `01234`
    - clean frame holds on `m=5,7,9`
    - strict clock holds on `m=5,7,9`
    - `U_0` splits into `m^2` fixed points with all monodromies `0`
- Exact recursive second bit `b2` was extracted from post-`b1` residual fragments:
  - `m=5`: `b1={1,2}`, `b2={1,3}`, residual excess after `b2`: `0`
  - `m=7`: `b1={1,3,5}`, `b2={1,2,4}`, residual excess after `b2`: `420`
  - `m=9`: `b1={1,2,5,6}`, `b2={1,3,5,7}`, residual excess after `b2`: `3354`
- Scope note:
  - these claims come from the uploaded bundle’s `README.md`, `passive_divergence_summary.json`, `b2_summary.json`, and `discovered_grammar_tables.json`
  - I did not rerun the searches from scratch in this turn.

## Attempt A
### Idea
Treat the passive-divergence witness as the decisive rebuttal to the earlier “passive tail bit is inert” reading, and update the frontier accordingly.

### What works
- The earlier strong no-go was false.
- The passive refined quotient is already rich enough to contain large nonlifted witnesses.
- So the hidden-phase information is genuinely entering the search space in a nontrivial way.
- The best divergent witness is especially important because it preserves `clean_frame=True` and `strict_clock=True` on `m=5,7,9` while breaking the old collapse law.
- This means the project has advanced from “escape strict collapse” to a subtler stage.

### Where it fails
- The witness still has trivial section dynamics:
  - `U_0` decomposes into `m^2` fixed points
  - all monodromies remain `0`
- So the project has not yet produced the nontrivial return structure needed for a Hamiltonian picture.
- In other words, the obstruction has moved from the coarse return law to the internal dynamics of the first-return section.

## Attempt B
### Idea
Use the best divergent witness as the new grammar seed, and let the exact tail bits `(b1,b2)` actively perturb layers `2` and `3` with the explicit goal of merging the fixed points of `U_0`.

### What works
- The `best_divergent_field` gives a clean starting seed:
  - layer `2` base permutation `23401`
  - layer `3` base permutation `34012`
  - layer `4+` fixed as `01234`
- This seed already preserves the two structural properties that were hardest to keep simultaneously:
  - clean frame
  - strict clock
- The exact bit `b2` is no longer speculative; it is extracted from the residual hypergraph after conditioning on `b1`.
- Since `b2` completely resolves the residual fragment excess at `m=5` and still cuts it sharply at `m=7,9`, it is the strongest exact tail refinement currently available.

### Where it fails
- We do not yet know which local grammar perturbations preserve Latin + triangular admissibility while producing nontrivial `U_0` cycles.
- The current evidence only says that `(b1,b2)` are the right discrete tail observables, not that the correct active use of them has already been identified.

## Candidate lemmas
- [C] The passive refined quotient `Theta_AB + phase_align + tail_cut` contains nonlifted same-preference pilot witnesses.
- [C] The best currently known passive witness preserves clean frame and strict clock on `m=5,7,9` but still has `U_0` equal to a disjoint union of `m^2` fixed points with monodromy `0`.
- [C] The exact recursive bit `b2` is data-derived from the residual fragment hypergraph, not an arithmetic guess.
- [H] The principal remaining bottleneck is no longer strict collapse; it is the absence of nontrivial section dynamics.
- [H] The next constructive step should use `(b1,b2)` to alter the layer-2/3 grammar in a way targeted at merging `U_0` fixed points.
- [F] “Passive tail refinement is inert” is no longer tenable.
- [F] “The old collapse law is the core obstruction” is no longer the right frontier.

## Needed computations/search
1. Build an active two-bit grammar family around the strict-clock seed:
   - base layer-2 anchor `2` (`23401`)
   - base layer-3 anchor `3` (`34012`)
2. Allow the layer-2 and layer-3 outputs to depend on `(old atoms, phase_align, b1, b2)`.
3. Keep the search family small:
   - first try cyclic-neighbor perturbations around anchors `2` and `3`
   - then enlarge only if needed.
4. Optimize directly for nontrivial section dynamics, not just preference:
   - primary: maximize number of non-fixed `U_0` states or reduce `U_0` cycle count
   - secondary: preserve clean frame / strict clock / preference.
5. Check whether any candidate creates genuine `U_0` cycles or nonzero monodromy on `m=5,7,9`.

## Next branching options
1. **Main constructive branch**
   Search an active `(b1,b2)`-driven layer-2/3 grammar around the `23401/34012` seed, targeted at merging `U_0` fixed points.
2. **Structural side branch**
   If this fails, prove a no-go theorem for all two-bit active grammars in a prescribed small palette neighborhood.
3. **Recursive refinement branch**
   If `U_0` still remains too split, extract a third residual bit from the post-`b2` fragments, but only after the active two-bit grammar has been exhausted.

## Claim status labels
- [P] passive refined quotient contains same-preference nonlifted witnesses
- [C] best divergent witness preserves clean frame + strict clock but has trivial `U_0`
- [C] exact recursive `b2` extracted
- [H] next frontier is merging `U_0` fixed points via active two-bit grammar
- [F] passive-inert reading is false
- [O] full Hamilton decomposition remains open

---

## Work Template

### Task ID
D5-ACTIVE-U0-MERGE-003

### Question
Can an active layer-2/3 grammar depending on the exact tail bits `(b1,b2)` produce nontrivial section dynamics — i.e. merge the `m^2` fixed points of `U_0` into larger cycles or induce nonzero monodromy — while preserving clean frame and, ideally, strict clock on `m=5,7,9`?

### Purpose
Advance from the currently best strict-clock passive witness to the first genuinely nontrivial return automaton on the pilot range.

### Inputs / Search space
- base seed field: the discovered `best_divergent_field`
  - layer `2` base anchor `2` (`23401`)
  - layer `3` base anchor `3` (`34012`)
  - layer `4+` anchor `0` (`01234`)
- quotient features:
  - old atom bits
  - `phase_align`
  - exact `b1`
  - exact `b2`
- pilot moduli: `m=5,7,9`
- optional stability spot-checks: `m=11,13`

### Allowed methods
- exact CP-SAT / finite pilot search
- small grammar-table search for active layer-2/3 outputs
- lexicographic optimization aimed at `U_0` complexity
- residual-fragment diagnostics
- direct validation of Latin / clean frame / strict clock / `U_0` cycle structure / monodromy

### Success criteria
1. Find a pilot witness with `clean_frame=True` on `m=5,7,9`.
2. Preferably keep `strict_clock=True` on `m=5,7,9`.
3. Achieve genuinely nontrivial `U_0` dynamics:
   - fewer than `m^2` cycles, or
   - at least one cycle length `>1`, or
   - at least one nonzero monodromy.
4. Save the explicit active grammar table and validation summary.

### Failure criteria
- every searched active two-bit grammar still yields only `m^2` fixed points with monodromy `0`
- or any nontrivial `U_0` witness necessarily destroys clean frame or Latin feasibility on the pilot range

### Artifacts to save
- code
- raw logs
- summary report
- discovered examples / counterexamples
- tables / plots / proof-supporting computations

### Return format
- active grammar definition
- best witness found
- validation table for `m=5,7,9`
- `U_0` cycle statistics and monodromy summary
- strongest conclusion supported

### Reproducibility requirements
- fixed pilot moduli `5,7,9`
- fixed solver seed
- saved grammar-table JSON and markdown summary
- deterministic validation scripts