I reviewed the uploaded bundle’s `README.md`, `passive_divergence_summary.json`, `b2_summary.json`, and `discovered_grammar_tables.json`, and I wrote the continuation note as markdown here:

[session20_active_research_note.md](sandbox:/mnt/data/session20_active_research_note.md)

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the remaining dynamical degeneracy after the `Theta_AB + phase_align + tail_cut` refinement.

Current target:
Use the positive active-tail result to update the bottleneck. The frontier is no longer “escape strict collapse,” but “create nontrivial section dynamics.”

Known assumptions:

* The passive refined quotient already contains nonlifted same-preference witnesses on `m=5,7,9`.
* Exact divergence result from the bundle:

  * preference score `32176`
  * changed pilot states vs lifted field `22806`
  * status `OPTIMAL`
* Two witnesses matter:

  * `same_preference_divergence`

    * layer 2 = `12340`
    * layer 3 = `12340`
    * layer 4+ = `01234`
    * clean frame holds on `m=5,7,9`
    * strict clock fails
  * `best_divergent_field`

    * layer 2 = `23401`
    * layer 3 = `34012`
    * layer 4+ = `01234`
    * clean frame holds on `m=5,7,9`
    * strict clock holds on `m=5,7,9`
    * `U_0` splits into `m^2` fixed points, all monodromies `0`
* Exact recursive `b2` is now available:

  * `m=5`: `b1={1,2}`, `b2={1,3}`, residual excess `0`
  * `m=7`: `b1={1,3,5}`, `b2={1,2,4}`, residual excess `420`
  * `m=9`: `b1={1,2,5,6}`, `b2={1,3,5,7}`, residual excess `3354`
* Scope:

  * these are bundle-backed claims
  * I did not rerun the searches in this turn
  * the detailed JSON exposes the strict-clock / `U_0` evidence directly; the “old collapse law broken” claim appears in the README and derived grammar summary rather than as a dedicated boolean in the detailed validation block

Attempt A:
Idea:
Treat the passive-divergence witness as the decisive rebuttal to the earlier “passive tail bit is inert” interpretation.

What works:

* That earlier reading is no longer sustainable.
* The refined quotient is genuinely richer than the lifted collapse field.
* The `best_divergent_field` is especially important because it preserves both clean frame and strict clock on the pilot range.

Where it fails:

* The section dynamics are still trivial.
* `U_0` remains a union of fixed points with monodromy `0`.
* So the obstruction has moved inward: from the coarse collapse law to the internal first-return dynamics.

Attempt B:
Idea:
Use the strict-clock divergent witness as the new seed, and let the exact tail bits `(b1,b2)` actively perturb layers 2 and 3 to merge the fixed points of `U_0`.

What works:

* There is now a natural seed:

  * layer 2 anchor `2` (`23401`)
  * layer 3 anchor `3` (`34012`)
  * layer 4+ anchor `0` (`01234`)
* This seed already preserves the two hardest structural properties together: clean frame and strict clock.
* `b2` is exact and data-derived, not guessed.

Where it fails:

* We do not yet know which active local perturbations preserve Latin + triangular admissibility while creating nontrivial `U_0` cycles.
* So the next step is still a search problem, not yet a theorem.

Candidate lemmas:

* [C] The passive refined quotient contains same-preference nonlifted pilot witnesses.
* [C] The best currently known passive witness preserves clean frame and strict clock on `m=5,7,9` but still has trivial `U_0`.
* [C] The recursive second tail bit `b2` is exact and hypergraph-derived.
* [H] The main bottleneck is now the absence of nontrivial section dynamics, not the old strict-collapse law.
* [H] The next constructive branch should let `(b1,b2)` affect the layer-2/3 grammar with the explicit goal of merging `U_0` fixed points.
* [F] “Passive tail refinement is inert” is false.
* [F] “The old collapse law is still the core obstruction” is no longer the right frontier.

Needed computations/search:

* Build an active two-bit grammar around the strict-clock seed:

  * layer 2 base anchor `2`
  * layer 3 base anchor `3`
* Let layer-2/3 outputs depend on `(old atoms, phase_align, b1, b2)`.
* Optimize directly for nontrivial `U_0` behavior:

  * reduce `U_0` cycle count
  * create cycle lengths `>1`
  * or produce nonzero monodromy
* Keep clean frame, and preferably strict clock, on `m=5,7,9`.

Next branching options:

* Main branch: active `(b1,b2)`-driven layer-2/3 grammar targeted at `U_0` merging.
* Side branch: if that fails, prove a no-go theorem for a small active palette neighborhood around the `23401/34012` seed.
* Recursive branch: only after exhausting the active two-bit family, consider a third residual bit.

Claim status labels:
[P] passive refined quotient contains same-preference nonlifted witnesses
[C] best divergent witness preserves clean frame + strict clock but has trivial `U_0`
[C] exact recursive `b2` extracted
[H] next frontier is active two-bit grammar for `U_0` merging
[F] passive-inert reading is false
[O] full Hamilton decomposition remains open

Work Template:
Task ID:
D5-ACTIVE-U0-MERGE-003

```
Question:
Can an active layer-2/3 grammar depending on the exact tail bits `(b1,b2)` produce nontrivial section dynamics — merging the `m^2` fixed points of `U_0` into larger cycles or inducing nonzero monodromy — while preserving clean frame and ideally strict clock on `m=5,7,9`?

Purpose:
Advance from the current strict-clock divergent witness to the first genuinely nontrivial return automaton on the pilot range.

Inputs / Search space:
- base seed field = `best_divergent_field`
- layer 2 base anchor `2`
- layer 3 base anchor `3`
- layer 4+ anchor `0`
- quotient features:
  - old atom bits
  - `phase_align`
  - exact `b1`
  - exact `b2`
- pilot moduli `5,7,9`
- optional spot-checks `11,13`

Allowed methods:
- exact CP-SAT / finite pilot search
- small active grammar-table search for layers 2 and 3
- lexicographic optimization aimed at `U_0` complexity
- direct validation of Latin / clean frame / strict clock / `U_0` cycle structure / monodromy

Success criteria:
- find a pilot witness with `clean_frame=True` on `m=5,7,9`
- preferably keep `strict_clock=True`
- achieve genuinely nontrivial `U_0` dynamics:
  - fewer than `m^2` cycles, or
  - some cycle length `>1`, or
  - some nonzero monodromy
- save the explicit active grammar table and validation summary

Failure criteria:
- every searched active two-bit grammar still yields only `m^2` fixed points with monodromy `0`
- or any nontrivial `U_0` witness necessarily destroys clean frame or Latin feasibility

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- tables / plots / proof-supporting computations

Return format:
- active grammar definition
- best witness found
- validation table for `m=5,7,9`
- `U_0` cycle statistics and monodromy summary
- strongest conclusion supported

Reproducibility requirements:
- fixed pilot moduli `5,7,9`
- fixed solver seed
- saved grammar-table JSON and markdown summary
- deterministic validation scripts
```

The most important update is simple: the project has crossed the “collapse escape” boundary. The next honest target is to make `U_0` genuinely move.
