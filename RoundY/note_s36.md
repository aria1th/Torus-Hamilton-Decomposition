I do want to read the bundle. This is the first point where the project seems to have crossed from “quotient discovery” into “return-map extraction,” so the raw grouped-return tables matter more than another survivor count.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Extract the D5 return-map model from the mixed witness, rather than extending local-family search.

Known assumptions:

* I am taking your new summary as correct for this turn; I have not yet inspected the new bundle itself.
* For the canonical mixed witness from `008`, the grouped return
  [
  U=R^m!\mid_{q=0}
  ]
  is an exact stable `skew_odometer_candidate` on
  [
  m=5,7,9,11,13.
  ]
* Its grouped-return base map is exactly
  [
  (w,u)\mapsto (w+1,u).
  ]
* On the raw first return, the base carry already appears as
  [
  dq=1,\qquad du=1,\qquad dw=\mathbf 1_{q=m-2},
  ]
  and you spot-checked the same carry slice for `m=11,13`.
* The mixed witness therefore has a real grouped-return base model; the unresolved part is the cocycle.
* Comparison controls:

  * `monodromy_008` is the degenerate affine grouped-return case
    [
    U(w,u)=(w,u)
    ]
    with constant cocycle.
  * `cycle_007` and `anti_mixed_010` remain `non_affine_grouped_return`.
* So the mixed witness is not just “cycle-only plus decoration”; it is the cleanest grouped-return object currently known in D5.

Attempt A:
Idea:
Read the mixed witness as already giving the correct D5 **base** return model.

What works:

* The raw first return law
  [
  dq=1,\quad du=1,\quad dw=\mathbf 1_{q=m-2}
  ]
  is almost a carry system in canonical form already.
* After the harmless shift
  [
  \hat q := q+1,
  ]
  this becomes
  [
  \hat q'=\hat q+1,\qquad
  w'=w+\mathbf 1_{\hat q=m-1},\qquad
  u'=u+1.
  ]
* So the raw return base is a two-digit odometer on ((\hat q,w)), together with an advancing coordinate (u).
* Grouping over one full (\hat q)-cycle kills the advancing (u)-motion mod (m) and produces
  [
  U(w,u)=(w+1,u).
  ]
* That is the first genuinely canonical base model we have seen in D5.
* This matches the correct d3/d4 lesson: first get the right return quotient, then conjugate it to a simple carry system.

Where it fails:

* This only identifies the base map.
* It does not yet identify the grouped cocycle
  [
  \phi(w,u)
  ]
  or show what gauge makes it simple.

Attempt B:
Idea:
Treat the unresolved part as a cocycle-normalization problem over the affine base
[
U(w,u)=(w+1,u).
]

What works:

* Each fixed (u) is an (m)-cycle in (w).
* The reported cycle monodromy on every such cycle is
  [
  m-2 \equiv -2 \pmod m.
  ]
* Therefore, for each fixed (u), the grouped cocycle (\phi(\cdot,u)) has orbit sum (-2).
* Over a cyclic base, any cocycle with fixed orbit sum is cohomologous to a single-defect cocycle. Concretely, for each (u) there exists a gauge (g_u(w)) such that
  [
  \phi(w,u)=g_u(w+1)-g_u(w)-2,\mathbf 1_{w=0}.
  ]
* So the real next question is not “does a return model exist?” It does.
* The real next question is:
  can the gauge be chosen uniformly in (u), or does (u) still carry genuine D5 state in the cocycle?
* If the gauge can be made (u)-independent, then the D5 mixed witness is already extremely close to a canonical skew-odometer:
  [
  (w,u,t)\mapsto (w+1,u,\ t-2,\mathbf 1_{w=0}).
  ]
* If not, then (u) is the first remaining reduced state variable of the cocycle.

Where it fails:

* I need the actual grouped cocycle table (U_{dv}(w,u)), not just the orbit sums, to decide whether the cocycle is:

  * already (u)-independent,
  * (u)-dependent but cohomologous uniformly,
  * or genuinely requiring a richer reduced state.

Candidate lemmas:

* [P] For the canonical mixed witness, the grouped-return base is exactly affine:
  [
  U(w,u)=(w+1,u)
  ]
  on `m=5,7,9,11,13`.
* [C] The raw first return already exhibits the carry law
  [
  dq=1,\quad du=1,\quad dw=\mathbf 1_{q=m-2}.
  ]
* [C] After shifting (q\mapsto \hat q=q+1), the raw return base is conjugate to a standard carry system on ((\hat q,w)) with a passive advancing coordinate (u).
* [C] The mixed witness is structurally cleaner than the comparison controls: `monodromy_008` is degenerate affine, while `cycle_007` and `anti_mixed_010` remain non-affine at grouped return.
* [H] The D5 base return model is essentially found; the unresolved piece is the cocycle normal form.
* [H] The next correct branch is cocycle extraction and cohomological normalization, not another family search.
* [H] The likely D5 analogue of the d4 story is now a skew-odometer / carry system with one defect cocycle, not a larger local palette.
* [F] The next main task should still be “search for another surviving family.”
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Read the new bundle and extract, for the mixed witness and the three control witnesses:

  * raw first-return map on ((q,w,u)),
  * grouped-return map (U(w,u)),
  * grouped cocycle table (U_{dv}(w,u)),
  * cycle sums / monodromy by (u)-fiber.
* Then do three exact analyses:

  1. verify the affine base law uniformly on `m=5,7,9,11,13`;
  2. solve the cohomological normalization problem for (U_{dv}(w,u));
  3. test whether the normalized cocycle is (u)-independent or whether (u) remains a genuine reduced state variable.
* If the cocycle normalizes to one defect slice uniformly in (u), we should stop local search entirely and start writing the D5 canonical model.
* If the cocycle still depends genuinely on (u), then the next grouped-return refinement should target that (u)-dependence, not new local flags.

Next branching options:

1. Main branch:
   grouped cocycle extraction and normalization for the `008` mixed witness.
2. Secondary branch:
   compare the normalized cocycle against `cycle_007`, `monodromy_008`, and `anti_mixed_010` to isolate what makes the mixed witness canonical.
3. Only if the cocycle refuses a clean grouped normal form:
   try a second/grouped return refinement, not a broader local-family sweep.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-GROUPED-COCYCLE-NORMAL-FORM-018

```
Question:
For the canonical mixed witness, what is the exact grouped cocycle over the affine base
\[
U(w,u)=(w+1,u),
\]
and can it be conjugated to a simple canonical defect cocycle?

Purpose:
The new result appears to identify the D5 grouped-return base model. The main unresolved step is now cocycle extraction and normalization, which is the natural D5 analogue of the d4 odometer reduction.

Inputs / Search space:
- Witnesses:
  - canonical mixed witness from `008`
  - monodromy-only control
  - strongest cycle-only control
  - representative anti-compressive mixed control
- Moduli:
  - pilot `m in {5,7,9}`
  - stability `m in {11,13}`
- Required data per witness:
  - raw first-return map \((q,w,u)\mapsto(q',w',u')\)
  - grouped-return map \(U(w,u)\)
  - grouped cocycle \(U_{dv}(w,u)\)
  - monodromy by grouped-return cycles

Allowed methods:
- exact extraction of return tables
- exact verification of affine base law
- cohomological normalization of cocycles over cyclic \(w\)-orbits
- comparison across \(u\)-fibers and across moduli
- grouped / second-return refinement only if needed
- no broad local-family sweep

Success criteria:
1. Confirm the grouped-return base law
   \[
   U(w,u)=(w+1,u)
   \]
   uniformly on `m=5,7,9,11,13` for the mixed witness.
2. Compute the grouped cocycle \(U_{dv}(w,u)\).
3. Determine whether \(U_{dv}\) is cohomologous to a canonical one-defect cocycle.
4. Determine whether the normalization can be chosen uniformly in \(u\).
5. Produce the sharpest reduced D5 return-map model supported by the data.

Failure criteria:
- the grouped base law breaks outside the currently checked moduli, or
- the grouped cocycle has no stable normal form across moduli, or
- the remaining \(u\)-dependence is too irregular to admit a small reduced-state model.
- If failure occurs, state exactly which extra grouped state variable is still missing.

Artifacts to save:
- code
- raw logs
- summary report
- grouped-return tables
- grouped cocycle tables
- gauge / normalization tables
- comparison tables across witnesses
- proof-supporting computations

Return format:
- exact witnesses used
- grouped-return base tables
- grouped cocycle tables
- normalized cocycle model
- verdict on \(u\)-dependence
- comparison with controls
- strongest reduced D5 return-map model supported

Reproducibility requirements:
- fixed witness definitions
- fixed moduli `5,7,9,11,13`
- deterministic extraction order
- saved JSON/CSV for grouped maps and cocycles
- exact scripts for the normalization step
```

The specific files I want from the new bundle are:

* `analysis_summary.json`
* any raw grouped-return table for (U(w,u))
* any raw cocycle table (U_{dv}(w,u))
* the witness payloads for the mixed and control cases
* any first-return trace tables showing the `dq, dw, du` law

This is not a big search. It is a moderate structural computation, and it is exactly the right next one.
