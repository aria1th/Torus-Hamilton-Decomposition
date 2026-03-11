Understood. I’ll format the next handoff as `.md` documents.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field, and break the current strict-collapse tail behavior in the `Theta_AB` program.

Current target:
Interpret what the Codex rerun actually proves, identify the exact remaining gap, and choose the next branch.

Known assumptions:

* The exact residual support hypergraph was extracted on the pilot range `m=5,7,9`.
* The incidence-signature quotient on nonzero hidden phase `δ` is already discrete on the pilot range:
  every `δ≠0` is its own class.
* The exact pilot tail-cut lookup is:

  * `m=5`: `{1,2}`
  * `m=7`: `{1,3,5}`
  * `m=9`: `{1,2,5,6}`
* Exact post-cut residual excess is:

  * `m=5`: `14`
  * `m=7`: `1282`
  * `m=9`: `8150`
* The refined quotient rerun on
  `Theta_AB + phase_align + tail_cut`
  has `54,982` pilot states and returns `OPTIMAL` with
  `changed_state_count_vs_lifted = 0`.
* The resulting searched field is exactly the lifted old strict-collapse field on the pilot range.
* Layers `2,3,4+` remain constant with permutation `01234`.
* Important code-level fact: the added `tail_cut` bit changes the quotient state identity, but the helper `required_output_for_signature(...)` still branches only on the old low bits `1,2,4`; it does **not** use the new `tail_cut` bit in the layer-2/3 output logic.

Attempt A:
Idea:
Treat the Codex artifact as a one-bit exact tail-cut no-go result.

What works:

* This is now much stronger than Session 19’s heuristic scan.
* It proves the next useful phase quotient is not hiding in a coarser equivalence relation: on the pilot range, the hidden-phase quotient is already discrete.
* It proves the hypergraph-optimal one-bit cut is real, exact, and correctly integrated into the quotient.
* It proves that, inside the **current free-anchor search model**, this exact one-bit refinement is dynamically inert:
  the solver’s optimal solution is literally the old lifted collapse field.

Where it fails:

* This does **not** yet prove that every solution on the refined quotient must collapse.
* The rerun objective maximizes only the existing preference score, which rewards layer `0` and `4+` behavior and is indifferent to layers `1,2,3`.
* More importantly, the new bit is still **passive** in the grammar:
  it splits states, but it does not participate in the layer-2/3 output rule.
* So the artifact kills “passive one-bit tail refinement,” not yet “all one-bit tail information whatsoever.”

Attempt B:
Idea:
Reinterpret the result as evidence that the next step must be an **active tail grammar**, not another passive state split.

What works:

* The code-level structure explains why the rerun stayed frozen.
* `tail_cut` enters the quotient signature, but the layer-2/3 helper still reads only the old atom bits.
* So the searched family was essentially:
  “same old local grammar, but with cloned tail states.”
* In that family, getting the same collapse field is not surprising.
* This sharply suggests the next branch:
  let tail information affect the **output grammar** on layers `2` and `3`, rather than only the anchor lookup.
* The natural candidate is a **two-bit tail grammar**:

  * `b1 = tail_cut(δ)` from the exact hypergraph-optimal split;
  * `b2` extracted from the residual fragments that remain after conditioning on `b1`.

Where it fails:

* We do not yet know the right `b2`.
* We also do not yet know whether a passive equal-preference noncollapsed witness exists on the current refined quotient.
* So there are two logically clean next sub-branches:
  one “strengthen the no-go,” one “activate the grammar.”

Candidate lemmas:

* [C] On the pilot range `m=5,7,9`, the exact incidence-signature quotient on nonzero hidden phases is discrete.
* [C] The exact hypergraph-optimal one-bit tail cut, when added only as a passive state bit, leaves the old strict-collapse field optimal in the current free-anchor model.
* [H] Passive quotient refinement is insufficient because the layer-2/3 output grammar still ignores the new bit.
* [H] Any successful next refinement must let new tail information participate in the layer-2/3 local rule, not merely split quotient states.
* [H] The correct second bit should be extracted from the residual post-`tail_cut` fragments, not from a fresh ad-hoc arithmetic ansatz.
* [F] “There is a useful coarser hidden-phase equivalence class still waiting to be found” is now ruled out on the pilot range.
* [F] “Another single passive phase bit should rescue the search” is no longer a credible primary branch.

Needed computations/search:

* First, close the logical gap in the passive model:
  search for a field on the current refined quotient with either

  1. the same preference score but some changed tail anchors, or
  2. any feasible noncollapsed pilot witness even at lower preference.
* Separately, build the active branch:

  * condition the residual support table on `b1=tail_cut`;
  * extract a second bit `b2` from the remaining residual fragments;
  * allow the layer-2/3 output helper to depend on `(old atoms, phase_align, b1, b2)`;
  * search over a very small admissible palette table rather than only over anchors.

Next branching options:

1. **Best immediate cleanup**:
   strengthen the passive no-go by asking whether the current refined quotient admits any nonlifted pilot witness at all.
2. **Main constructive branch**:
   move to an active two-bit tail grammar where the new bits affect layer-2/3 outputs.
3. If the active two-bit grammar still collapses:
   the next serious target becomes a structural no-go theorem for all “tail-bit refinements without grammar surgery.”

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-ACTIVE-TAIL-GRAMMAR-002

```
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
```

My view:
The Codex artifact is genuinely valuable, and it narrows the program a lot. The strongest lesson is not merely “one more bit failed.” It is:

**passive tail bits are now basically exhausted.
The next honest branch is grammar surgery on layers 2–3.**
