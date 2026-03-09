# 4D Generalization Scouting Note

## Purpose

This note is a standalone summary of the first computational scouting pass for a
possible 4-dimensional analogue of the directed-torus Hamilton-decomposition
pattern.

The goal was not to prove a theorem directly. The goal was to answer a more
basic research question:

- is there an immediate small counterexample signal in dimension `4`?
- if not, does there exist a low-complexity pattern that looks theorem-shaped?

What follows is a compact account of what was tried, what was found, and where
the mathematical bottleneck now lies.

## Research strategy

The search was organized in increasing structural complexity.

1. `Exact small-case search`

For very small `m`, use a CP-SAT model that searches over all local direction
assignments subject to:

- each color chooses one direction at every vertex,
- the chosen directions form a permutation of the coordinate directions,
- each color map has indegree `1` everywhere,
- subtour cuts are added iteratively until either a Hamilton decomposition is
  found, the instance is proved impossible, or the time budget ends.

2. `Uniform low-layer families`

Test the simplest possible "Claude-style" generalization:

- the bulk is canonical,
- only a few low residue layers are modified,
- each active layer uses one fixed permutation everywhere.

3. `Affine low-layer families`

If the uniform family fails, allow the active low layer to carry a small amount
of coordinate-dependent structure:

- one default permutation on the active layer,
- one special permutation on one affine slice inside that layer.

4. `Affine stripe refinement`

If a one-slice affine family is promising, allow the chosen affine form to have
a separate permutation on each residue class, while keeping the bulk and active
layer geometry fixed.

The principle behind this progression is simple: do not search for existence in
an unconstrained way unless there is already some evidence of a compressible
pattern. A theorem will not come from a bag of unrelated witnesses.

## What was computed

### A. Exact search at `d=4, m=3`

An exact CP-SAT run was carried out with a `120s` budget.

Observed outcome:

- status: `timeout`
- iterations: `475`
- subtour cuts added: `5277`
- best incumbent cycle counts: `[4, 1, 4, 4]`

Interpretation:

- no theorem-level counterexample was found in this budget;
- no Hamilton decomposition was found either;
- the best incumbent is already highly nontrivial:
  - one color is Hamiltonian,
  - the other three still split into `4` cycles each.

Structural summary of the incumbent:

- `24` distinct local direction tuples appear,
- only `2` of the `81` vertices remain canonical,
- so the unrestricted search is already using substantial
  coordinate-dependent structure.

This matters because it immediately rules out the hope that a very crude
one-rule-per-layer pattern is enough.

### B. Uniform low-layer family

The first structured family tested was:

- canonical tuple `(0,1,2,3)` in the bulk,
- on one active residue layer `S = 0`, use the permutation `(1,0,3,2)`,
- all other layers remain canonical.

This turned out to be the best member of the entire uniform layer family tested
for `m = 3,4,5,6`.

Its behavior is rigid:

- for `m=3`, all four colors have `9` cycles;
- for `m=4`, all four colors have `16` cycles;
- for `m=5`, all four colors have `25` cycles;
- for `m=6`, all four colors have `36` cycles.

In other words, this family bottoms out at exactly `m^2` cycles per color, and
the induced `P0` return maps have the same cycle counts.

Conclusion:

- the naive low-layer uniform generalization fails,
- and it fails in a stable, non-noisy way.

### C. One-slice affine low-layer family

The next family allowed one affine slice inside the active layer to behave
differently.

The repeated best candidate was:

- outside `S = 0`: use the canonical tuple `(0,1,2,3)`;
- on `S = 0`: use the default tuple `(1,0,3,2)`;
- on the affine slice `x_0 + x_2 \equiv 0 \pmod m` inside `S = 0`, use the
  special tuple `(3,2,1,0)`.

This candidate was not guessed from theory first. It emerged as the repeated
best solution of the affine-family search.

What is striking is the stability of its cycle law.

For `m = 3,4,5,6`, the best affine search found:

- full color-map cycle counts: `[m, m, m, m]`,
- induced `P0` cycle counts: `[m, m, m, m]`.

This is a decisive improvement over the uniform family:

- uniform family: `m^2` cycles per color,
- affine-split family: `m` cycles per color.

The fixed candidate was then scanned directly on the wider set
`m = 3,4,5,6,7,8,10,12`, and the same exact law persisted:

- each color has exactly `m` cycles,
- each induced `P0` map has exactly `m` cycles,
- sign product stays `+1`.

This is the first truly theorem-shaped signal in dimension `4`.

### D. Affine stripe refinement

To test whether the one-slice affine rule was merely a rough approximation, a
more flexible family was searched:

- keep the same active layer `S = 0`,
- keep the same affine form `x_0 + x_2`,
- but allow each residue class of `x_0 + x_2 \pmod m` to have its own
  permutation.

This did not improve the best cycle counts for the smallest exact cases tested:

- for `m=3`, the best cycle counts remain `[3,3,3,3]`,
- for `m=4`, the best cycle counts remain `[4,4,4,4]`.

So, at least in the first exact cases, the one-slice affine family already
captures the best visible behavior of that broader stripe-based refinement.

## What the computations now say

At this point the computations support the following statements.

1. `No small exact counterexample has been found.`

The theorem is not disproved by the current scouting pass.

2. `The naive 4D generalization is wrong.`

The simplest low-layer uniform model fails, and it fails in a rigid way.

3. `There is a specific affine low-layer pattern worth taking seriously.`

The rule

- bulk canonical,
- layer `S=0` default `(1,0,3,2)`,
- affine slice `x_0+x_2 \equiv 0` carrying `(3,2,1,0)`

produces exactly `m` cycles per color across every tested `m`.

4. `The next difficulty is no longer computational enumeration.`

The present bottleneck is mathematical interpretation.

## Bottleneck for a mathematician

This is the point where the research stops being "find a candidate" and starts
being "explain the candidate."

The main bottleneck is:

### Why does the affine-split rule produce exactly `m` cycles?

That is the first theorem-level question now forced by the data.

It is no longer enough to say that the candidate performs well computationally.
One needs a conceptual explanation of the exact `m`-cycle law.

A mathematician would likely need to do at least the following.

1. Identify the correct transversal and return map.

The computations suggest that the induced `P0` maps mirror the full cycle
counts, so there should be a natural return-map description in which the affine
split becomes transparent.

2. Explain the `m`-cycle decomposition structurally.

The data strongly suggests that the affine split does not yet splice the system
into one cycle, but instead organizes the dynamics into an `m`-family of
parallel strands.

So the right question is:

- what invariant labels those `m` strands?
- why is it preserved by the affine-split rule?

3. Decide whether a bounded splice can merge those `m` strands.

This is the real next theorem problem.

The computations no longer suggest searching for a completely different family.
They suggest starting from the affine-split rule and asking whether there is a
finite or low-complexity repair that merges the `m` cycles into one.

4. Determine whether the `m`-cycle law is a feature or an obstruction.

There are two possibilities.

- `Constructive reading`: the affine-split family has isolated the correct
  bulk geometry, and only a finite splice remains.
- `Obstruction reading`: the affine-split family reveals a genuine invariant,
  so no bounded repair of this type can succeed.

This is not something the current automatic search can settle cleanly. It now
requires an actual mathematical invariant or splice analysis.

## Why this is the correct stopping point

There is a clear reason to stop here rather than continue blind search.

Before the affine-split discovery, computation was still answering a yes/no
engineering question: "is there any compressible pattern at all?"

After the affine-split discovery, the question has changed. The best structured
family is now stable across odd and even `m`, and its failure mode is exact:

- not random,
- not chaotic,
- not varying by residue class in the tested range,
- but precisely `m` cycles.

That is already strong enough to demand a mathematical explanation.

So the next step should not be another round of brute-force family design. The
next step should be proof-oriented analysis of the affine-split candidate.

## Practical next questions

If one wants to continue from here in a theorem-oriented way, the most useful
questions are:

1. Can the `m` cycles be written explicitly in terms of a conserved or
   approximately conserved quantity?
2. Is there a clean return-map formula on `P0` or another transversal that
   makes the `m`-cycle law obvious?
3. Does a finite splice mechanism exist that breaks the `m`-strand invariant?
4. If not, can one prove that every bounded perturbation of this affine type
   still leaves at least `m` cycles?

Those are now the mathematically relevant questions.
