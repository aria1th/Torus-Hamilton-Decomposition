I read the bundle.

My main thought is: this is stronger than “the grouped base is affine.”
For the canonical mixed witness, the **full grouped output signature already collapses to one reduced coordinate**
[
s:=w+u \pmod m,
]
not just the base motion on ((w,u)).

That is the first place in the D5 project where I think we can honestly say: **a candidate reduced return-map state has appeared.**

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Stop treating local-family search as the main program. Use the new grouped-return extraction to formulate the D5 return-map normal form.

Known assumptions:

* I read the new `017` bundle, including:

  * `README.md`
  * `data/analysis_summary.json`
  * the raw mixed-witness tables

    * `mixed_008_m*_first_return.json`
    * `mixed_008_m*_grouped_return.json`
    * `mixed_008_m*_quotient_R.json`
    * `mixed_008_m*_quotient_U.json`
* I also checked the control classifications from `analysis_summary.json`.
* For the canonical mixed witness `mixed_008`, the grouped return
  [
  U = R^m!\mid_{q=0}
  ]
  is stable on
  [
  m=5,7,9,11,13.
  ]
* Bundle-backed base law:
  [
  U_{\text{base}}(w,u)=(w+1,u).
  ]
* Bundle-backed grouped monodromy on every grouped-return cycle:
  [
  m-2 \equiv -2 \pmod m.
  ]
* From my direct inspection of the quotient tables:

  * the first-return quotient for output signature `dv + low_layer_word` is exactly the partition by
    [
    (q,s),\qquad s:=w+u \pmod m;
    ]
  * the grouped-return quotient for output signature `phi + grouped_low_layer_trace` is exactly the partition by
    [
    s=w+u \pmod m.
    ]
* So the mixed witness already has an exact reduced grouped state of size `m`, not `m^2`.

Attempt A:
Idea:
Extract the exact reduced first-return model before grouped return.

What works:

* The quotient tables show that the raw first return is already deterministic on
  [
  (q,s),\qquad s=w+u.
  ]
* On the inspected moduli `m=5,7,9,11,13`, the reduced first-return map is exactly
  [
  R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr).
  ]
* The reduced output is also exact:
  [
  dv(q,s)=
  \begin{cases}
  1,& q\neq m-2,\ s=1,\
  1,& q=m-2,\ s\neq 0,\
  0,& \text{otherwise,}
  \end{cases}
  ]
  and the representative low-layer word is
  [
  (1,4,\ 2,\mathbf 1_{q=m-2},\ 3,dv(q,s)).
  ]
* This is already a finite-state carry system, not just an empirical summary.

Where it fails:

* This is an exact extraction from the saved tables, not yet a proof from the witness definition.
* I have not yet derived why the local rule collapses to ((q,s)) directly from the `008` witness formula.

Attempt B:
Idea:
Push from the reduced first return to a grouped cocycle normal form.

What works:

* Since grouped return starts on `q=0`, the grouped quotient coordinate is
  [
  s=w+u.
  ]
* The grouped quotient transitions are exactly
  [
  s\mapsto s+1.
  ]
* The grouped cocycle depends only on `s`, with an exact stable formula on all inspected moduli:
  [
  \phi(s)=2+\mathbf 1_{s=1}-2,\mathbf 1_{s=2}-\mathbf 1_{s=3}
  \qquad (\bmod m).
  ]
* Equivalently, the raw grouped cocycle is:

  * `3` at `s=1`,
  * `0` at `s=2`,
  * `1` at `s=3`,
  * `2` everywhere else.
* This already explains the orbit sums:
  [
  \sum_{j=0}^{m-1}\phi(s+j)=m-2.
  ]
* Better still, this cocycle is cohomologically simple.
  With the local gauge
  [
  g(s)=\mathbf 1_{s\in{2,3}},
  ]
  the transformed cocycle
  [
  \phi'(s)=\phi(s)+g(s)-g(s+1)
  ]
  becomes
  [
  \phi'(s)=2-2,\mathbf 1_{s=2}.
  ]
* Then with the linear gauge
  [
  h(s)=2s,
  ]
  since
  [
  h(s)-h(s+1)=-2,
  ]
  one gets the pure one-defect form
  [
  \phi''(s)=-2,\mathbf 1_{s=2}.
  ]
* So the mixed witness is not merely a “skew_odometer_candidate.”
  On the inspected moduli, it is already cohomologous to a **one-dimensional odometer with a single defect cocycle**.

Where it fails:

* I have not yet turned this into a theorem-level derivation from the raw `R_red` dynamics.
* I also have not yet proved that the same formulas persist for all odd `m≥5`; at the moment they are exact on `5,7,9,11,13`.

Candidate lemmas:

* [P] For `mixed_008`, the grouped-return quotient on output signature `phi + grouped_low_layer_trace` is exactly the `m`-state quotient by
  [
  s=w+u \pmod m
  ]
  on `m=5,7,9,11,13`.
* [P] For `mixed_008`, the first-return quotient on output signature `dv + low_layer_word` is exactly the `m^2`-state quotient by
  [
  (q,s),\qquad s=w+u \pmod m,
  ]
  on `m=5,7,9,11,13`.
* [P] The reduced first return is exactly
  [
  R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr).
  ]
* [P] The reduced grouped return is exactly
  [
  U_{\mathrm{red}}(s)=s+1.
  ]
* [P] The grouped cocycle is exactly
  [
  \phi(s)=2+\mathbf 1_{s=1}-2,\mathbf 1_{s=2}-\mathbf 1_{s=3}
  \qquad (\bmod m)
  ]
  on `m=5,7,9,11,13`.
* [C] Hence `mixed_008` is already cohomologous to the one-defect skew-odometer
  [
  (s,t)\mapsto (s+1,\ t-2,\mathbf 1_{s=2}).
  ]
* [C] `monodromy_008` is the degenerate affine case: identity base with constant cocycle.
* [C] `cycle_007` and `anti_mixed_010` do not affine-collapse at grouped return.
* [H] The D5 mixed witness is not “cycle-only plus decoration”; it is the first branch that has reached a real reduced return-map model.
* [H] The next job is proof extraction and canonicalization, not another wide local search.
* [F] The next main branch should still be another local-family sweep near the `wu2` gadget.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No broad search is needed now.
* The right next computation is structural:

  1. derive the exact formulas for `R_red`, `dv`, and `low_layer_word` directly from the `008` witness rule, not just from tables;
  2. derive the grouped cocycle formula
     [
     \phi(s)=2+\mathbf 1_{s=1}-2,\mathbf 1_{s=2}-\mathbf 1_{s=3};
     ]
  3. formalize the gauge reduction to
     [
     \phi''(s)=-2,\mathbf 1_{s=2};
     ]
  4. extend exact spot-checks modestly to a few larger odd moduli, e.g.
     [
     m=15,17,19,
     ]
     only as stability evidence, not as a new search program.
* Then compare the controls in the same reduced-language:

  * why `monodromy_008` collapses to trivial base + constant cocycle;
  * why `cycle_007` and `anti_mixed_010` fail to collapse to the same reduced odometer state.

Next branching options:

1. Main branch:
   theorem-level extraction of the reduced mixed return map.
2. Secondary branch:
   modest stability spot-checks on a few larger odd moduli.
3. Only if the proof extraction stalls:
   identify the smallest missing coordinate in the control branches, not in the mixed witness.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-MIXED-SKEW-ODOMETER-NORMAL-FORM-018

```
Question:
Can the canonical mixed witness `mixed_008` be promoted from an empirical grouped-return signal to an explicit D5 normal form?

More concretely:
prove or rigorously extract that its reduced return map is the one-dimensional skew-odometer
\[
s \mapsto s+1,\qquad
t \mapsto t+\phi(s),
\]
with cocycle cohomologous to
\[
-2\,\mathbf 1_{s=2}.
\]

Purpose:
The recent search chain identified the live mixed mechanism and ruled out many fake state variables. The new grouped-return bundle shows that the mixed witness has already reached a canonical reduced state. The next step is to turn that into the D5 return-map model, not to widen local search families.

Inputs / Search space:
- Primary witness:
  - `mixed_008`
- Control witnesses:
  - `monodromy_008`
  - `cycle_007`
  - `anti_mixed_010`
- Existing exact tables from `017`:
  - first-return tables
  - grouped-return tables
  - quotient_R tables
  - quotient_U tables
- Tested moduli already available:
  - `m in {5,7,9,11,13}`
- Optional modest extensions:
  - `m in {15,17,19}`

Allowed methods:
- exact extraction from saved tables
- direct derivation from the witness rule used in `mixed_008`
- partition refinement / quotient verification
- cohomological normalization of the grouped cocycle
- modest stability spot-checks on a few larger odd moduli
- comparison with control witnesses
- no broad new local-family search

Success criteria:
1. Verify exactly that the first-return quotient is
   \[
   (q,s),\qquad s=w+u.
   \]
2. Verify exactly that the grouped-return quotient is
   \[
   s=w+u.
   \]
3. Derive the reduced first-return map
   \[
   R_{\mathrm{red}}(q,s)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2}\bigr).
   \]
4. Derive the reduced grouped-return map
   \[
   U_{\mathrm{red}}(s)=s+1.
   \]
5. Derive the grouped cocycle formula
   \[
   \phi(s)=2+\mathbf 1_{s=1}-2\,\mathbf 1_{s=2}-\mathbf 1_{s=3}.
   \]
6. Produce an explicit gauge reducing this to
   \[
   2-2\,\mathbf 1_{s=2},
   \]
   and then to the pure one-defect form
   \[
   -2\,\mathbf 1_{s=2}.
   \]
7. Explain, in the same language, why the three control witnesses do not realize the same normal form.

Failure criteria:
- the reduced-state formulas do not survive direct derivation from the witness rule,
- or the cocycle formula fails outside the currently tested moduli,
- or the control comparison shows that the apparent normal form is an artifact of the present quotient extraction.
- If failure occurs, identify the precise missing coordinate or grouped-return refinement.

Artifacts to save:
- code
- raw logs
- summary report
- reduced first-return tables
- reduced grouped-return tables
- cocycle tables
- gauge / normalization tables
- control-comparison tables
- proof-supporting computations

Return format:
- exact reduced coordinates used
- exact first-return formulas
- exact grouped-return formulas
- exact cocycle formula
- explicit gauge reduction
- comparison with controls
- strongest D5 normal-form statement supported
- exact remaining gap to a theorem, if any

Reproducibility requirements:
- fixed witness definitions
- fixed inspected moduli `5,7,9,11,13`
- deterministic extraction order
- saved JSON/CSV for reduced maps and cocycles
- exact scripts for quotient verification and cocycle normalization
- explicit separation of table-derived facts from proof-derived facts
```

My bottom-line view:

**This is the first point where D5 looks like it has a real odometer-style model in hand.**
Not just an affine base, but a reduced grouped state
[
s=w+u
]
and a cocycle that already appears to be cohomologous to a single defect.

That is exactly the kind of object the earlier search phase was trying to uncover.
