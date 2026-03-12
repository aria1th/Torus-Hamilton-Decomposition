I read the bundle.

My main take is that `018` upgrades the project from “we found a live mixed witness” to “we have an explicit reduced return model, and we can now name the exact remaining obstruction.”

The strongest new point is not just that the grouped cocycle normalizes nicely. It is that, combining `017` and `018`, the canonical mixed witness now looks like

[
R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
]
with
[
dv(q,s)=1 \iff \bigl(q\neq m-2 \land s=1\bigr)\ \text{or}\ \bigl(q=m-2 \land s\neq 0\bigr),
]
and grouped return
[
U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
\qquad
\phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}.
]

So the mixed witness is already:

* a fast carry digit `q`,
* a true active odometer coordinate `s=w+u`,
* a cocycle coordinate `v`,
* and one passive grouped invariant `u`.

That is the D5 return-map model, at least computationally.

The remaining obstruction is no longer vague. It is:

**the grouped dynamics factor as identity on `u` times a one-defect skew-odometer on `(s,v)`.**

Because
[
\sum_{s\in \mathbb Z_m}\phi(s)=m-2\equiv -2 \pmod m,
]
and `m` is odd, each fixed-`u` grouped fiber is already a single orbit on `(s,v)`. The current mixed witness therefore explains its own baseline: it is “perfect” on each `u`-fiber, but it does not couple the `u`-fibers together.

That is exactly the kind of obstruction statement one wants before an odometer-style proof.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Promote the mixed witness from a computational normal form to the D5 return-map model, and isolate the exact remaining obstruction.

Known assumptions:

* I read the `018` bundle, including:

  * `README.md`
  * `data/analysis_summary.json`
  * `data/saved_vs_direct_comparison.json`
  * `data/control_comparison.json`
  * the reduced tables in

    * `data/saved_table_reductions/`
    * `data/direct_replay_reductions/`
* From the earlier `017` result already accepted in the project:

  * for `mixed_008`, grouped return on the base is exactly
    [
    (w,u)\mapsto (w+1,u)
    ]
    on `m=5,7,9,11,13`.
* From `018`:

  * first-return quotient is exactly by
    [
    (q,s),\qquad s=w+u \pmod m
    ]
    on saved-table moduli `5,7,9,11,13`;
  * grouped-return quotient is exactly by
    [
    s=w+u \pmod m
    ]
    on saved-table moduli `5,7,9,11,13`;
  * direct replay reproduces the same reduced formulas on
    [
    m=5,7,9,11,13,15,17,19.
    ]
* Exact reduced first-return formulas:
  [
  R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr),
  ]
  [
  dv(q,s)=1 \iff \bigl(q\neq m-2 \land s=1\bigr)\ \text{or}\ \bigl(q=m-2 \land s\neq 0\bigr),
  ]
  with representative low-layer word
  [
  (1,4,\ 2\mathbf 1_{q=m-2},\ 3,dv(q,s)).
  ]
* Exact grouped cocycle:
  [
  \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}\pmod m.
  ]
* Exact gauge reductions:
  [
  \phi \sim 2-2\mathbf 1_{s=2}
  \sim -2\mathbf 1_{s=2}.
  ]
* Controls:

  * `monodromy_008` is the degenerate affine/translation case.
  * `cycle_007` and `anti_mixed_010` remain non-affine at grouped return.

Attempt A:
Idea:
Combine the `017` grouped-base law with the `018` cocycle collapse to write the full reduced grouped dynamics of the mixed witness.

What works:

* Since grouped base is
  [
  (w,u)\mapsto (w+1,u)
  ]
  and grouped cocycle depends only on
  [
  s=w+u,
  ]
  the full grouped return on active coordinates can be written as
  [
  U(w,u,v)=\bigl(w+1,\ u,\ v+\phi(w+u)\bigr).
  ]
* In coordinates
  [
  s=w+u,
  ]
  this becomes
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr).
  ]
* So the mixed witness is the product of:

  * identity on `u`,
  * a one-dimensional skew-odometer on `(s,v)`.
* This is the first explicit D5 reduced return-map model that really looks like the d4-style endpoint.

Where it fails:

* This is still theorem extraction from exact computations, not yet a symbolic proof from the witness rule.
* The formula for the full grouped map is a synthesis of the exact `017` and `018` extractions, not a separately proved statement in the bundle.

Attempt B:
Idea:
Use the reduced formulas to identify the exact remaining obstruction.

What works:

* Over each fixed `u`, the grouped return is
  [
  (s,v)\mapsto (s+1,\ v+\phi(s)).
  ]
* Since
  [
  \sum_s \phi(s)=m-2\equiv -2 \pmod m
  ]
  and `m` is odd, the total cocycle over one `s`-cycle is invertible mod `m`.
* Therefore, for each fixed `u`, the grouped return has one orbit of length `m^2` on `(s,v)`.
* This explains the whole baseline geometry:
  the mixed witness is already fully transitive on each `u`-fiber, but `u` itself stays invariant under grouped return.
* So the remaining obstruction is not “missing cocycle structure.” The cocycle is already clean.
* The remaining obstruction is:
  **no grouped `u`-carry.**

Where it fails:

* We do not yet know the minimal perturbation that breaks `u`-invariance without destroying the skew-odometer on `(s,v)`.
* That is now the real next question, and it should be asked in the reduced return-map language, not in the old local-family language.

Candidate lemmas:

* [P] For `mixed_008`, the first-return quotient is exactly by `(q,s)` with `s=w+u`, and the grouped-return quotient is exactly by `s=w+u`, on saved-table moduli `5,7,9,11,13`, with direct replay extending the same formulas to `15,17,19`.
* [P] The reduced first return is exactly
  [
  R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr),
  ]
  with
  [
  dv(q,s)=1 \iff \bigl(q\neq m-2 \land s=1\bigr)\ \text{or}\ \bigl(q=m-2 \land s\neq 0\bigr).
  ]
* [P] The grouped cocycle is exactly
  [
  \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3}\pmod m,
  ]
  cohomologous to
  [
  -2,\mathbf 1_{s=2}.
  ]
* [C] Combining `017` and `018`, the grouped return of `mixed_008` is
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr)
  ]
  on the checked moduli.
* [C] Hence the mixed witness is identity on `u` times a one-defect skew-odometer on `(s,v)`.
* [C] Because the cycle sum is `m-2`, each fixed-`u` grouped fiber is a single orbit on `(s,v)` for odd `m`.
* [C] `monodromy_008` is the degenerate constant-cocycle affine case, while `cycle_007` and `anti_mixed_010` fail to collapse to this reduced model.
* [H] The main remaining obstruction is the passive grouped invariant `u`.
* [H] The next progress should be framed as:
  identify the minimal mechanism that introduces grouped `u`-carry while preserving the skew-odometer on `(s,v)`.
* [F] The right next main branch is another broad local-family sweep.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No big exhaustive search is needed for the next main step.
* The right next work is structural:

  1. derive the reduced first-return formulas directly from the `mixed_008` witness rule;
  2. derive the grouped cocycle formula symbolically from the reduced first return;
  3. formalize the gauge reduction to the one-defect cocycle;
  4. prove that grouped return on each fixed `u`-fiber is a single orbit because the cycle sum is `-2`;
  5. package the exact obstruction as:
     [
     U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
     ]
     with `u` the only passive grouped coordinate.
* Only after that, use the controls to diagnose what kind of local event could change `u` under grouped return without destroying the `(s,v)` model.

Next branching options:

1. Main branch:
   theorem extraction for the mixed witness normal form and the invariant-`u` obstruction.
2. Secondary branch:
   compare the controls in the same reduced language to isolate which local mechanism is capable of generating grouped `u`-carry.
3. Only after that:
   run a tiny targeted search whose objective is explicitly “break grouped `u`-invariance while preserving the skew-odometer on `(s,v)`.”

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-MIXED-NORMAL-FORM-AND-U-OBSTRUCTION-019

```
Question:
Can the canonical mixed witness `mixed_008` be upgraded from an exact computational normal form to the explicit D5 return-map model
\[
R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
\]
\[
U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
\]
with
\[
\phi(s)\sim -2\,\mathbf 1_{s=2},
\]
and can the remaining obstruction be identified precisely as grouped `u`-invariance?

Purpose:
`018` indicates that the project has reached the return-map extraction stage. The mixed witness already appears to factor as identity on `u` times a one-defect skew-odometer on `(s,v)`. The next goal is to prove that model and isolate the exact missing carry needed to go beyond the baseline geometry.

Inputs / Search space:
- Primary witness:
  - `mixed_008`
- Controls:
  - `monodromy_008`
  - `cycle_007`
  - `anti_mixed_010`
- Bundles already available:
  - `017`
  - `018`
- Exact tables already extracted:
  - reduced first-return tables
  - reduced grouped-return tables
  - quotient tables
  - control-comparison tables
- Checked moduli:
  - saved-table range `m in {5,7,9,11,13}`
  - direct-replay range `m in {15,17,19}`

Allowed methods:
- symbolic derivation from the `mixed_008` witness rule
- exact replay verification against saved reduced tables
- cocycle summation and cohomological normalization
- grouped-orbit analysis on fixed `u`-fibers
- comparison with controls in the same reduced coordinates
- very small diagnostic computations only if needed
- no broad new local-family sweep

Success criteria:
1. Derive directly from the witness rule that first return depends only on `(q,s,u,v)` with `s=w+u`.
2. Derive the exact first-return formulas:
   \[
   q' = q+1,\qquad
   s' = s+1+\mathbf 1_{q=m-2},\qquad
   u' = u+1,\qquad
   v' = v+dv(q,s).
   \]
3. Derive the exact grouped return:
   \[
   U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr).
   \]
4. Derive the explicit cocycle formula
   \[
   \phi(s)=2+\mathbf 1_{s=1}-2\mathbf 1_{s=2}-\mathbf 1_{s=3},
   \]
   and its gauge reduction to
   \[
   -2\,\mathbf 1_{s=2}.
   \]
5. Prove that each fixed-`u` fiber is a single grouped-return orbit on `(s,v)` for odd `m`.
6. State the exact obstruction:
   grouped return is already canonical on `(s,v)`, and the only passive grouped coordinate is `u`.
7. Explain, in the same language, why the three control witnesses do not realize this normal form.

Failure criteria:
- the symbolic derivation from the witness rule does not reproduce the extracted reduced formulas,
- or the grouped cocycle fails to normalize as claimed,
- or the control comparison shows that the apparent normal form is not genuinely distinguishing.
- If failure occurs, identify the exact missing coordinate or grouped-return refinement.

Artifacts to save:
- code
- raw logs
- summary report
- symbolic derivation note
- reduced return formulas
- cocycle / gauge tables
- grouped orbit calculations
- control-comparison tables
- proof-supporting computations

Return format:
- exact reduced coordinates used
- exact first-return formulas
- exact grouped-return formulas
- exact cocycle formula and gauge reduction
- proof that each fixed-`u` fiber is a single grouped orbit
- exact obstruction statement
- comparison with controls
- smallest plausible next perturbation target if the obstruction is confirmed

Reproducibility requirements:
- fixed witness definitions
- fixed moduli `5,7,9,11,13,15,17,19`
- deterministic extraction order
- saved JSON/CSV for reduced maps, cocycles, and grouped orbits
- exact scripts for replay verification and cocycle normalization
- explicit separation of:
  - table-derived facts
  - proof-derived facts
```

No big compute is needed for this next main step. The current `017` and `018` artifacts are enough. The next job is mostly proof extraction and obstruction isolation, with only modest verification if we want a little more stability evidence.
