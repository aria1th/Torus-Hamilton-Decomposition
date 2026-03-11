Task ID:
D5-ACTIVE-TAIL-GRAMMAR-002

Question:
Does there exist a noncollapsed pilot master field on `m=5,7,9` once tail information is allowed to affect the layer-2/3 output grammar, rather than only splitting quotient states?

Purpose:
Distinguish “passive tail bits are inert” from “tail information is fundamentally useless,” and search the smallest credible active grammar beyond the current collapse model.

Inputs / Search space:
- current exact `tail_cut` bit `b1`
- exact residual support table after conditioning on `b1`
- candidate second bit `b2` derived from the remaining residual fragments
- layer buckets `2` and `3`
- old atom bits, `phase_align`, `b1`, `b2`
- admissible color-0 outputs / local palettes compatible with Latin + triangular constraints

Allowed methods:
- witness search on the current passive refined quotient:
  - same-preference divergence search
  - lower-preference noncollapse witness search
- residual-fragment analysis conditioned on `b1`
- exact extraction of `b2`
- small grammar-table search for layer-2/3 outputs
- CP-SAT / exact pilot search on `m=5,7,9`
- direct validation of `clean_frame`, `strict_clock`, `U_0`, monodromy, and return law

Success criteria:
1. Either prove the passive refined quotient admits no nonlifted pilot witness, or exhibit one.
2. Construct a concrete second tail bit `b2` from residual fragment data.
3. Search an active layer-2/3 grammar depending on `(old atoms, phase_align, b1, b2)`.
4. Either find a pilot field that breaks the old collapse law, or prove this whole active family still fails.
5. Save the exact grammar table and validation outputs.

Failure criteria:
- passive divergence search is inconclusive
- no stable `b2` can be extracted from residual fragments
- active grammar search produces only the old collapse field
- no sharper no-go statement emerges

Artifacts to save:
- code
- raw logs
- summary report
- discovered examples / counterexamples
- tables / plots / proof-supporting computations

Return format:
- passive-model witness / no-go result
- definition of `b2`
- active grammar table
- pilot search outcome
- validation summaries
- strongest conclusion supported

Reproducibility requirements:
- fixed pilot moduli `m=5,7,9`
- saved residual-fragment tables
- saved grammar table JSON/MD
- fixed solver seed
- exact validation script for the reported field
