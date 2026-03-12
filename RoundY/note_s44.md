The summary is enough, so I did not reopen the tar.

My main reaction is:

**`026/027` do not just kill one tuning. They identify the missing kind of local state.**
The `025` reduced target is still the right one, but it cannot be realized by a **vertex-conditioned** current-state layer-2 rule. The collision says the next honest branch must be an **edge-conditioned / one-step-memory transducer**.

That is the cleanest way to read the two negatives.

Return the research note:

Problem:
Construct a 5-color Hamilton decomposition of
[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,{e_0,e_1,e_2,e_3,e_4})
]
via a cyclic-equivariant master permutation field.

Current target:
Keep the `025` reduced target, but abandon the current-state `B/P/M` ansatz completely.

The next smallest live branch is:

**a directed-edge transducer on the carry slice**
that distinguishes the two endpoints of the active adjacent pair and places the omitted-edge cocycle defect on a chosen directed endpoint.

Known assumptions:

* From `019`, the canonical mixed witness already has explicit reduced first return
  [
  R(q,s,u,v)=\bigl(q+1,\ s+1+\mathbf 1_{q=m-2},\ u+1,\ v+dv(q,s)\bigr),
  ]
  and grouped return
  [
  U(s,u,v)=\bigl(s+1,\ u,\ v+\phi(s)\bigr),
  \qquad
  \phi(s)\sim -2,\mathbf 1_{s=2}.
  ]
* From `025`, the reduced normal-form target is explicit:

  * omit one row of the diagonal/anti-diagonal moving adjacent transposition,
  * then add a one-point or two-point omitted-edge cocycle defect,
  * and this yields a **single grouped orbit of size `m^3`** on all checked odd moduli.
* From `026`, in the diagonal fixed-`w` stationary rewrite:

  * the tiny current-state `B/P/M` family has `0` all-color Latin candidates on `m=5,7,9`.
* From `027`, in the anti-diagonal fixed-`t` stationary rewrite:

  * again `0` all-color Latin candidates on `m=5,7,9`.
* In both branches, the sharp obstruction is the same:

  * the intended `P` target and the adjacent `M` target land on the **same layer-2 current state**,
  * so a deterministic current-state layer-2 rule cannot separate them.
* Baseline `mixed_008` still validates on the same evaluator, so the obstruction is in the family, not in the checker.

Attempt A:
Idea:
Promote `026/027` to a structural no-go: the `025` reduced target cannot be realized by any stationary rewrite whose layer-2 perturbation is a deterministic function of the current layer-2 state alone.

What works:

* This is stronger than “the tiny family failed.”
* The saved collision witnesses show the real issue: the two required roles

  * `P` = one endpoint of the active adjacent pair,
  * `M` = the other endpoint,
    are not vertex-separable in the current stationary coordinates.
* So the problem is not parameter choice, and not lack of a good selector.
* It is the wrong type of controller.
* In graph language: `025` is an **edge** perturbation, while `026/027` attempted to encode it by a **vertex** coloring.

Where it fails:

* It does not yet tell us the smallest realizable edge controller.
* It only tells us current-state vertex control is impossible.

Attempt B:
Idea:
Recast the next branch as a directed-edge / one-step-memory transducer.

What works:

* The `025` reduced target is naturally edge-based:

  * transposition on one active adjacent pair,
  * omission on one row,
  * cocycle defect at an omitted-edge endpoint.
* The `026/027` collision tells us exactly what extra state is missing:
  **endpoint orientation**.
* So the smallest live controller is not a new one-bit selector on vertices. It is a 3-state edge controller:
  [
  \epsilon \in {\text{off-edge},\ \text{left-end},\ \text{right-end}}.
  ]
* In the diagonal stationary rewrite, this means:

  * `P` on one endpoint of the fixed adjacent `w`-pair,
  * `M` on the other,
  * `B` off the pair,
  * and on the omitted row, `B` on both.
* The cocycle defect should be driven by the **same directed-edge controller**, because `025`’s successful defect is endpoint-tied, not row-sized or graph-sized.
* This is the first local family truly matched to the reduced model.

Where it fails:

* We do not yet know whether a one-step predecessor/current (or current/successor) controller is enough, or whether two-step memory is needed.
* We also do not yet know which local observable best realizes the endpoint orientation bit.

Candidate lemmas:

* [C] `026` and `027` together rule out the stationary `B/P/M` realization strategy on both natural branches.
* [C] More sharply: no deterministic current-state layer-2 rule can realize the `025` edge target, because the `P` and `M` roles collide on the same layer-2 current state.
* [H] Therefore the next honest local branch must be edge-conditioned or one-step-memory, not vertex-conditioned.
* [H] The omitted-edge cocycle defect should be controlled by the same directed-edge state as the base transposition, since the successful reduced defect in `025` is endpoint-tied.
* [H] The next smallest live family is a directed-edge transducer on the carry slice.
* [F] Another selector expansion around the current-state `B/P/M` ansatz can succeed.
* [O] Full Hamilton decomposition remains open.

Needed computations/search:

* No broad search is justified.
* The next step should be tightly staged.

1. **Edge-signature extraction**

   * Use the collision witnesses from `026/027` to extract the smallest local data that separates:

     * left endpoint of the active pair,
     * right endpoint of the active pair,
     * off-edge states.
   * Most likely sources:

     * predecessor/current local signature on the carry slice,
     * or current/successor local signature.
   * The point is not “find a new selector”; it is “find the smallest edge-orientation controller.”

2. **Directed-edge transducer family**

   * In the diagonal fixed-`w` branch first, define a tiny controller
     [
     \epsilon\in{\text{off},\text{L},\text{R}}.
     ]
   * Map it to the 3-word palette:

     * `off -> B`,
     * `L -> P`,
     * `R -> M`,
       with the omitted row forcing both endpoints back to `B`.
   * Tie the layer-3 cocycle defect to one chosen directed omitted-edge endpoint (or both endpoints as control).

3. **Validation target**

   * Check only whether the local family realizes the exact `025` reduced signature:

     * grouped base orbit size `m^2`,
     * full grouped orbit size `m^3`,
     * clean/strict on `m=5,7,9`,
     * `m=11` as first control.
   * No generic selector widening.

Next branching options:

1. Main branch:
   directed-edge / one-step-memory transducer in the diagonal fixed-`w` stationary branch.
2. Secondary branch:
   if one-step memory is still insufficient, widen only to the smallest two-step edge controller.
3. Only then:
   revisit the anti-diagonal branch or predecessor/non-affine micro-families around the same edge target.

Claim status labels:
[P] [C] [H] [F] [O]

Work Template:
Task ID:
D5-EDGE-TRANSDUCER-028

```
Question:
Can the `025` reduced normal form be realized locally by a **directed-edge transducer** on the carry slice, rather than by a current-state layer-2 selector?

More concretely:
can one build a tiny local family in the diagonal stationary branch in which the controller distinguishes

\[
\epsilon \in \{\text{off-edge},\text{left endpoint},\text{right endpoint}\},
\]

and uses

- `B` off the active pair,
- `P` on one endpoint,
- `M` on the other,
- with omission on one row `s=s_0`,
- and a point/two-point cocycle defect on a chosen omitted-edge endpoint,

so as to emulate the full `025` reduced signature?

Purpose:
`025` already identified the correct reduced target. `026/027` prove that the obstacle is not parameter tuning but controller type: the target is edge-based, while the failed `B/P/M` ansatz was vertex-based. The next honest local step is therefore an edge-conditioned transducer.

Inputs / Search space:
- Base witness:
  - `mixed_008`
- Reduced target:
  - `025` omit-base + edge-tied cocycle defect
- Negative local boundary:
  - `026/027` stationary current-state `B/P/M` no-go
- Preferred branch:
  - diagonal fixed-`w` stationary rewrite
- Active adjacent pair:
  \[
  \{w_0-1,\ w_0\}
  \]
- Omitted row:
  \[
  s=s_0
  \]
- Carry-slice palette:
  - `B`: baseline mixed carry word
  - `P`: plus-shift word
  - `M`: minus-shift word
- Edge controller:
  - Stage 1:
    extract a one-step local signature
    \[
    \epsilon\in\{\text{off},\text{L},\text{R}\}
    \]
    from predecessor/current or current/successor data
  - Stage 2 only if needed:
    smallest two-step edge signature
- Cocycle defect:
  - point defect at one omitted-edge endpoint
  - point defect at the other endpoint
  - two-point omitted-edge defect as control
- Primary moduli:
  - `m in {5,7,9}`
- First control:
  - `m=11`

Allowed methods:
- exact extraction of endpoint-separating local signatures from the saved collision witnesses
- exact exhaustive enumeration over the tiny transducer tables consistent with
  \[
  \epsilon \mapsto \{B,P,M\}
  \]
- direct full-color Latin testing
- clean-frame filtering
- strict-clock validation
- grouped orbit extraction in reduced coordinates
- exact comparison against the `025` reduced target
- no broad selector sweep
- no generic affine-family expansion

Success criteria:
1. Find a one-step edge controller that separates left/right endpoints of the active adjacent pair.
2. Find a clean strict local realization on `m=5,7,9`.
3. Recover grouped base orbit size `m^2`.
4. Recover full grouped orbit size `m^3`.
5. Match the `025` reduced signature up to relabeling/gauge.
6. Preferably persist at `m=11`.

Failure criteria:
- no one-step edge controller separates the endpoints,
- or every such controller destroys all-color Latin / clean-frame,
- or grouped orbit sizes fail to match the `025` reduced target.
- If failure occurs, identify whether the next widening should be:
  - two-step edge memory,
  - or a different non-affine/predecessor micro-family tied to the same edge target.

Artifacts to save:
- code
- raw logs
- summary report
- extracted collision-signature tables
- transducer tables
- grouped orbit tables
- reduced-signature comparison tables
- validation outputs
- discovered realizations / counterexamples

Return format:
- exact collision-signature used
- exact edge-controller states and transducer tables
- clean/strict survivor counts
- grouped base orbit sizes
- full grouped orbit sizes
- best realization of the `025` reduced target, if any
- strongest obstruction if none survives
- recommended minimal widening

Reproducibility requirements:
- fixed base witness `mixed_008`
- fixed reduced target from `025`
- fixed moduli `5,7,9,11`
- deterministic enumeration order
- saved JSON summaries for:
  - endpoint-separating signatures
  - all tested transducer tables
  - grouped orbit comparisons
- exact scripts for grouped reduction and validation
```

Optional additional material that would be useful, but not required:

* the machine-readable collision witness files from `026` and `027`,
* one explicit omitted-edge endpoint sample from `025`,
* and the baseline mixed carry-slice trace on those same states.

The short strategic conclusion is:

**`025` remains the right reduced target.
`026/027` show the failed ansatz was wrong because it tried to realize an edge perturbation with a vertex controller.
So the next honest move is a tiny edge-conditioned transducer search, not another selector expansion.**
