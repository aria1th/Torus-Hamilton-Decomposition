The summary is enough; I did not reopen the tar.

The level I want next is now very concrete:

**one best seed pair, one exact defect graph, one bounded-state transducer search.**

Not a bigger word catalog. Not another selector sweep.
`032` says the problem is no longer “find a separator bit.” It is:

**route a balanced Latin defect by a small moving repair state.**

One extra observation sharpens this. For the best seed,
[
250=10\cdot 5^2,\qquad 490=10\cdot 7^2,\qquad 810=10\cdot 9^2.
]
So the hole/collision count is not just “large”; it looks like an exact
[
10m^2
]
law. That strongly suggests the defect pattern may quotient to a bounded set of template classes, which is exactly the situation where a finite-state transducer / defect-splice mechanism becomes the right next object.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Stop all static local-family widening. The next honest branch is:

**extract the Latin defect graph for one best endpoint seed pair, quotient it to its bounded template classes, and test the smallest finite-state defect-splice transducer that can route those defects.**

Known assumptions:

* I am taking your summary of `032` as sufficient for this turn.
* `025` remains the correct reduced target:

  * omit-base plus edge-tied point cocycle defect,
  * grouped base orbit size `m^2`,
  * full grouped orbit size `m^3`.
* `026/027` ruled out the current-state `B/P/M` stationary realization on both natural branches.
* `028` showed endpoint orientation is necessary.
* `029` ruled out the smallest static two-layer endpoint-word realization.
* `030` showed the path-level branch is not empty:
  there are endpoint-separated seed words.
* `031` ruled out the smallest static three-layer promotion.
* `032` sharpened the obstruction:

  * only `11` seed pairs are distinct at both layer `2` and layer `3`;
  * the best seed is

    * left `[2,2,1]`,
    * right `[1,4,4]`;
  * its Latin obstruction is exactly balanced:
    [
    \text{overfull}=\text{holes}=250,490,810
    ]
    for `m=5,7,9`, i.e.
    [
    10m^2;
    ]
  * one-gate repair on top 3 seeds: `208` candidates, `0` Latin survivors;
  * one-bit repair on top 3 seeds: `4160` candidates, `0` Latin survivors;
  * smallest two-class static repair on best seed: `384` candidates, `0` Latin survivors.
* Most importantly, the colliders are **already separable** by:

  * current label,
  * label plus every tested bit,
  * exact predecessor/current label pairs,
  * exact current/successor label pairs.
* Therefore the obstruction is no longer “missing one extra separator bit.”

Attempt A:
Idea:
Read `032` as a no-go for the whole one-bit / one-class / smallest static repair paradigm.

What works:

* This is stronger than “those bits failed.”
* The colliding incoming sources are already separated by the obvious local contexts.
* So adding one more separator cannot be the real issue.
* The failure is not lack of distinguishability; it is lack of a **coordinated reassignment mechanism**.
* The exact scaling
  [
  10m^2
  ]
  suggests the defect is structured, not random.

Where it fails:

* It does not yet identify the minimal dynamic controller that works.
* It only rules out all the smallest static repairs.

Attempt B:
Idea:
Recast the next branch as a defect-flow / defect-splice problem.

What works:

* The best seed pair should now be treated as a base rule plus a balanced defect.
* The next object to extract is not another word family, but the exact **defect graph**:

  * which source classes overfill which targets,
  * which targets are holes,
  * and which candidate local changes move mass from a given overfull target to a given hole.
* If this graph quotients to a bounded number of template defect classes, then a bounded-state transducer becomes the right next model.
* This is also the natural analogue of the d3/d4 lesson:
  once the reduced target is known, the next step is a small splice/repair normal form, not more catalog growth.

Where it fails:

* We do not yet know whether the minimal controller is:

  * a 2-state transducer,
  * a 3-state transducer,
  * or something slightly larger.
* We also do not yet know whether one alternate repair word suffices, or whether two are needed.

Candidate lemmas:

* [C] The `025` reduced target remains the correct target.
* [C] `029/031/032` together rule out static endpoint-word realization and the smallest one-bit / one-class / two-class repairs.
* [C] In the best seed, the Latin defect is balanced with exact size
  [
  10m^2
  ]
  on `m=5,7,9`.
* [C] The colliders are already separated by the obvious local contexts, so the missing ingredient is not another separator bit.
* [H] The next smallest live branch is a finite-state defect-splice transducer around one seed pair.
* [H] The first task is to extract the bounded defect graph and compute the minimal repair state count.
* [F] Another broader static search or one-bit refinement is the right next move.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* Do not widen the word catalog first.
* The next exact work should be:

1. **Best-seed defect graph extraction**
   Use only the best seed pair
   [
   L=[2,2,1],\qquad R=[1,4,4].
   ]
   Extract:

   * all overfull targets,
   * all holes,
   * the exact incoming source classes creating each overfull,
   * the exact outgoing candidate image changes available from nearby catalog words or the smallest repair palette.

2. **Template quotient**
   Quotient the defect data by the obvious translational symmetries.
   Test whether the `10m^2` defect count really comes from a bounded number of template classes, plausibly `10` template defects.

3. **Minimal state lower bound**
   Solve the finite repair problem at the quotient level:

   * can a 2-state transducer route the defect?
   * if not, can a 3-state transducer?
   * what is the smallest number of repair classes needed?

4. **Micro-family synthesis**
   Only after the quotient is understood:
   test one very small dynamic family around the best seed:

   * one best seed pair,
   * at most one or two alternate repair words,
   * 2-state or 3-state transducer only.

Next branching options:

1. Main branch:
   best-seed defect graph + minimal transducer state count.
2. Secondary branch:
   if 2-state fails at the quotient level, try 3-state before any new seed pair.
3. Only after that:
   go to a second seed or a larger splice family.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:

```
Work Template:
    Task ID:
    D5-DEFECT-SPLICE-TRANSDUCER-033

    Question:
    For the best endpoint seed pair
        left = [2,2,1], right = [1,4,4],
    can the balanced Latin defect be quotiented to a bounded template defect graph and repaired by the smallest finite-state transducer, while preserving the 025 reduced target as closely as possible?

    Purpose:
    032 shows that the obstruction is no longer “missing a separator bit.”
    The colliders are already separated by obvious contexts, yet all one-gate, one-bit, and smallest two-class static repairs fail.
    The next honest step is therefore to treat the best seed as a base rule plus a balanced defect-flow problem, and compute the minimal dynamic repair mechanism.

    Inputs / Search space:
    - reduced target:
      - 025 omit-base + edge-tied point cocycle defect
    - local pruning chain:
      - 026, 027, 029, 031, 032
    - primary seed pair only:
      - left = [2,2,1]
      - right = [1,4,4]
    - primary moduli:
      - m in {5,7,9}
    - first control:
      - m = 11 only if something survives pilot stage
    - candidate repair palette:
      - best seed pair words
      - optionally one or two nearest alternate words from 030, but keep this minimal
    - candidate dynamic controllers:
      - 2-state transducer first
      - 3-state transducer only if 2-state is impossible at quotient level

    Allowed methods:
    - exact extraction of:
      - overfull targets
      - hole targets
      - incoming source classes
      - candidate reassignment moves
    - quotient the defect graph by translational symmetries
    - compute whether the defect count 10*m^2 comes from a bounded number of template classes
    - exact lower-bound / feasibility analysis for:
      - 2-state repair
      - 3-state repair
    - only after quotient-level feasibility:
      tiny exact synthesis search on the best seed pair
    - direct all-color Latin / clean / strict validation for any synthesized candidate
    - no broad seed expansion
    - no generic selector sweep

    Success criteria:
    1. Produce the exact defect graph for the best seed pair.
    2. Produce a bounded template quotient of that defect graph.
    3. Determine the minimal state count required for repair:
       - 2-state sufficient or not,
       - 3-state sufficient or not.
    4. If feasible, synthesize a nonbaseline Latin/clean/strict repair on m=5,7,9.
    5. Check whether the repaired candidate still matches the 025 reduced target to first order.

    Failure criteria:
    - the defect graph does not quotient to a bounded template family,
    - or 2-state and 3-state repair are both impossible at the quotient level,
    - or every synthesized bounded-state repair destroys the reduced 025 target immediately.
    - If failure occurs, the report must state clearly whether the next honest branch is:
      - a larger transducer state space, or
      - a different local splice mechanism not centered on a single seed pair.

    Artifacts to save:
    - code
    - raw logs
    - summary report
    - best_seed_defect_graph.json
    - best_seed_defect_templates.json
    - state_lower_bound_report.json
    - transducer_synthesis_summary.json
    - validation outputs
    - proof-supporting computations

    Return format:
    - exact best seed defect graph
    - quotient template classes
    - defect count formula and template explanation
    - 2-state feasibility verdict
    - 3-state feasibility verdict
    - best synthesized repair, if any
    - strongest obstruction if none survives
    - explicit recommendation for the next branch

    Reproducibility requirements:
    - fixed best seed pair [2,2,1] / [1,4,4]
    - fixed moduli 5,7,9
    - deterministic extraction and quotienting order
    - saved JSON summaries for defect graph, template quotient, and transducer feasibility
    - exact scripts for all-color Latin / clean / strict validation
    - explicit separation of:
      - defect-graph facts
      - synthesis facts
```

The brief level I want is:

**one seed, one defect graph, one minimal-state verdict.**

If 2-state or 3-state already fails at that level, then we will know the project has crossed from “small transducer repair” into a genuinely larger splice mechanism.
