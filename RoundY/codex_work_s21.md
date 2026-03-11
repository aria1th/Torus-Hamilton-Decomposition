Task ID:
D5-ACTIVE-U0-MERGE-003

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
