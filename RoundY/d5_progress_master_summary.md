# d=5 Hamilton decomposition — consolidated progress summary

## Scope

This note consolidates the project status through exact pilot artifact `015`.
It is the current working summary of:

- the master-field formulation,
- the pre-pilot foundations,
- the exact D5 artifact chain `001`–`015`,
- the current mechanism picture,
- the live bottleneck and next honest branch.

The intended range for all exact pilot claims below is:

- exact exhaustive search or exact validation on `m=5,7,9`,
- with repeated stability spot-checks on `m=11,13` for frontier rules.

## Problem statement

Construct a 5-color Hamilton decomposition of

\[
D_5(m)=\mathrm{Cay}((\mathbb Z_m)^5,\{e_0,e_1,e_2,e_3,e_4\})
\]

for all `m >= 3`, using a cyclic-equivariant master permutation field

\[
\Pi_\theta \in S_5,
\qquad
f_c(x)=x+e_{\Pi_{\theta(x)}(c)}.
\]

The working program is:

- build a quotient-state system `theta`,
- encode the field by an anchor rule,
- enforce outgoing Latin, incoming Latin, and triangular admissibility,
- study first-return and second-return dynamics on the pilot sections.

The key structural reduction already established earlier is the orbit-anchor formula

\[
\Pi_\theta(c)=a(\rho^{-c}\theta)+c.
\]

So the search problem is fundamentally a search over anchor tables on quotient states.

## High-level status

### What is already solved structurally

1. Clean frame is no longer the main obstacle.
2. Latin feasibility is no longer the main obstacle.
3. Dynamic collapse is understood sharply enough that we can now target specific return mechanisms rather than broad global search.
4. The project has crossed both earlier barriers:
   - nontrivial `U_0` exists,
   - clean strict mixed cycle+monodromy witnesses also exist.

### What the exact D5 pilot line has achieved

- `005` produced the first nontrivial `U_0`.
- `008` produced the first clean strict mixed regime:
  - `U_0` has `m` cycles of length `m`,
  - every cycle has uniform nonzero monodromy.
- `009`–`015` then tested whether that mixed regime can be improved by small exact local refinements.

### What is still missing

The active frontier is no longer “find any mixed witness.”
The current exact frontier is:

> find a clean strict mixed witness whose geometry is better than the Session 26 baseline.

Concretely, the current baseline mixed profile is:

- on `m=5,7,9`, total pilot cycle count `21 = 5+7+9`,
- equivalently, `U_0` has exactly `m` cycles of length `m` on each pilot modulus,
- with uniform nonzero monodromy on those cycles.

Every exact D5 refinement after `008` has either:

- reproduced this same mixed geometry,
- destroyed twist,
- or worsened the geometry by adding fixed points / extra cycles.

## Compressed prehistory: Sessions 1–20

### Phase A. Discovery and color-by-color analysis

- Session 1 found an `m=5` Hamilton decomposition by Kempe swaps.
- Sessions 2–10 showed the original witness line was not the final route:
  affine pinning was necessary, clean-frame criteria were clarified, and the unsolved colors could not be repaired by the early cyclic-template surgery program.

Outcome:

- the original witness became a discovery tool, not the final construction.

### Phase B. Master permutation field and joined quotient

- the fresh cyclic family put clean frame into the construction,
- the conditional master-field theorem and orbit-anchor reconstruction were established,
- free-anchor search on the joined quotient made Latin feasible,
- but pilot-feasible fields collapsed dynamically.

The sharp collapse law was:

\[
R_0(q,w,v,u)=(q+1,w,v+1,u),
\qquad
U_0=\mathrm{id},
\qquad
\text{monodromy}=0.
\]

Outcome:

- the bottleneck moved inward from Latin / clean frame to return dynamics.

### Phase C. Tail-phase diagnostics

- rigid pilot grammars on `Theta_AB + phase_align` were extracted,
- predecessor copies of old atoms were weak,
- pure hidden-phase cuts beat ad hoc arithmetic predicates,
- but the best cut drifted with `m`, so no single arithmetic bit emerged.

Outcome:

- the next useful refinement had to come from the residual hidden-phase automaton, not guessed formulas.

## Exact D5 artifact chain

### `001` — exact tail cut and quotient rerun

Artifact: `D5-TAIL-CUT-QUOTIENT-RERUN-001`

Main outcome:

- the nonzero hidden-phase incidence-signature quotient is already discrete on `m=5,7,9`,
- exact pilot `tail_cut` bits were extracted,
- but rerunning the free-anchor search with that bit returned the lifted strict-collapse field exactly.

Interpretation:

- the one-bit tail cut was combinatorially real but dynamically inert in the then-current passive branch.

### `002` — passive divergence and recursive second bit

Artifact: `D5-ACTIVE-TAIL-GRAMMAR-002`

Main outcome:

- the passive refined quotient is not exhausted by the lifted collapse field,
- a same-preference nonlifted witness exists,
- an exact recursive second bit `b2` can be extracted.

Interpretation:

- the passive branch was richer than `001` first suggested, but still not enough to break `U_0` triviality.

### `003` — smallest active `(b1,b2)` neighborhood around the strict seed

Artifact: `D5-ACTIVE-U0-MERGE-003`

Main outcome:

- exact family size `256`,
- only one strict clean survivor,
- it is exactly the old strict seed,
- `U_0` remains trivial.

Interpretation:

- the smallest active two-bit neighborhood around the seed is exhausted.

### `004` — strict-friendly context-only two-anchor family

Artifact: `D5-STRICT-PALETTE-CONTEXT-004`

Main outcome:

- all clean strict survivors collapse to constant anchor pairs,
- there are no context-dependent clean survivors,
- there are no nontrivial-`U_0` survivors.

Interpretation:

- dependence on tail-context bits alone does not survive clean-frame + strict-clock in this family.

### `005` — one old bit clean-survival breakthrough

Artifact: `D5-ONE-OLD-BIT-CLEAN-SURVIVAL-005`

This is the first real D5 breakthrough.

Main outcome:

- `328` clean strict survivors,
- `240` strict survivors with nontrivial `U_0`,
- all context-dependent clean survivors are actually one-old-bit-only,
- the pilot line splits cleanly into two separated mechanisms:
  - cycle-only,
  - monodromy-only.

Interpretation:

- one old bit is enough to break `U_0` triviality,
- but not enough to combine geometry and twist in the same witness.

### `006` — decoupled two-old-bit family with layer-3 alternate `0`

Artifact: `D5-TWO-OLD-BIT-CYCLE-MONODROMY-006`

Main outcome:

- `200` clean strict survivors,
- every one is cycle-only,
- layer 3 is dynamically invisible at pilot-return level in this branch.

Interpretation:

- decoupling with layer-3 alt `0` collapses back to the pure layer-2 geometry mechanism.

### `007` — decoupled two-old-bit family with layer-3 palette `{0,2}`

Artifact: `D5-LAYER3-ALT2-DECOUPLED-007`

Main outcome:

- `360` clean strict survivors,
- exact trichotomy:
  - `296` cycle-only,
  - `32` monodromy-only,
  - `32` trivial,
- still `0` combined cycle+monodromy witnesses.

Interpretation:

- the right layer-3 palette already exists,
- but one old bit on layer 3 is still too coarse.

### `008` — predecessor mode switch: first mixed regime

Artifact: `D5-LAYER3-MODE-SWITCH-008`

This is the second decisive D5 breakthrough.

Main outcome:

- `64` clean strict survivors,
- `24` combined cycle+monodromy survivors,
- `32` cycle-only,
- `8` monodromy-only,
- `0` trivial.

Representative mixed witness:

- layer 2 fixed to a simple old-bit split,
- layer 3 controlled by `pred_sig1_wu2` or `pred_sig4_wu2`,
- slice pair `0/3` versus `3/0`.

Exact pilot mixed profile:

- `m=5`: `5` cycles of length `5`, monodromy `3`,
- `m=7`: `7` cycles of length `7`, monodromy `5`,
- `m=9`: `9` cycles of length `9`, monodromy `7`.

Interpretation:

- one extra predecessor-local layer-3 flag is enough to mix geometry and twist,
- the live mechanism is concentrated in the `wu2` predecessor tests.

### `009` — strong cycle-mix graft

Artifact: `D5-STRONG-CYCLE-MIX-009`

Main outcome:

- the `008` twist gadget survives on a very large fraction of widened rules,
- Stage 1: `240` clean strict, `192` mixed,
- Stage 2: `960` clean strict, `912` mixed,
- but `0` mixed survivor improves the `008` mixed baseline.

Interpretation:

- the twist gadget is robust,
- but in this family it controls holonomy without improving geometry.

### `010` — shared predecessor interaction

Artifact: `D5-SHARED-PRED-INTERACTION-010`

Main outcome:

- the shared switch is genuinely interactive,
- it breaks the universal `m`-cycle profile from `009`,
- but only in the wrong direction.

Exact regimes include:

- baseline mixed total `21`,
- anti-compressive mixed total `39`,
- mixed total `137`,
- monodromy-only total `155`.

No improved mixed survivor exists.

Interpretation:

- genuine layer-2/layer-3 interaction appears here,
- but the sign is wrong: interaction adds fixed points rather than compressing cycles.

### `011` — layer-2 geometry under fixed twist

Artifact: `D5-LAYER2-GEOMETRY-UNDER-FIXED-TWIST-011`

Main outcome:

- under a canonical fixed mixed twist, no layer-2 rule improves the baseline,
- `48` clean strict survivors,
- `46` mixed,
- `2` monodromy-only,
- control twist with reversed sign gives exactly the same cycle signatures on all `128` tested layer-2 rules.

Interpretation:

- in this family, geometry is entirely insensitive to twist sign,
- changing twist is not the right knob.

### `012` — alt-4 two-flag geometry

Artifact: `D5-ALT4-TWO-FLAG-GEOMETRY-012`

Main outcome:

- the two-flag layer-2 refinement is genuinely live,
- Stage 1: `256` clean strict survivors,
- Stage 2: `640` clean strict survivors,
- new mixed geometry classes appear, including totals `35`, `57`, `119`, `137`,
- still `0` improved mixed survivors.

Interpretation:

- the family is not collapsing to coarse state,
- but every new geometry class is anti-compressive.

### `013` — alt-4 three-flag geometry

Artifact: `D5-ALT4-THREE-FLAG-GEOMETRY-013`

Main outcome:

- both named extra flags give the same exact result,
- `1024` clean strict survivors per family,
- regime histogram identical to `012`,
- `0` improved mixed survivors.

Important exact point:

- most clean survivors genuinely use the full eight-state partition,
- so this is not a “state collapse” failure.

Interpretation:

- the added named predecessor-phase flags are dynamically sterile for the sign problem.

### `014` — exact signature diagnostic and coupled mode-switch

Artifact: `D5-SIGNATURE-DIAG-AND-COUPLED-MODESWITCH-014`

Main outcome:

- the exact predecessor-tail signature is much smaller than feared:
  - exact classes `12`,
  - generated by the old named partition plus one real new bit,
  - the new bit is `pred_sig1_phase_align`.

Stage A:

- the new bit is locally real,
- but the layer-2-only search is pilot-return sterile:
  - `16` rules total,
  - only the old constant pure-alt-4 tables survive cleanly.

Stage B:

- as a standalone coupled layer-3 controller, the exact bit also fails:
  - Stage B1: `6` clean survivors, all cycle-only,
  - Stage B2: `12` clean survivors, all cycle-only,
  - Stage B3: `0` clean survivors.

Strongest exact fact:

- every clean Stage B survivor has `mode_p0 = mode_p1`,
- so the exact bit is ignored on layer 3 whenever clean-frame + strict-clock survives.

Interpretation:

- the new exact bit exists and matters locally,
- but it is globally sterile in the obvious one-bit roles.

### `015` — `wu2` secondary exact twist

Artifact: `D5-WU2-SECONDARY-EXACT-TWIST-015`

Main outcome:

- the live `wu2` mixed gadget from `008` survives,
- but the exact bit still cannot survive as a genuine secondary controller.

Counts:

- Stage 1: `36` clean strict, `24` mixed, `12` cycle-only,
- Stage 2: `108` clean strict, `72` mixed, `36` cycle-only,
- every clean survivor stays on the old mixed baseline total `21`,
- `0` improved mixed survivors.

Strongest exact fact:

- every clean survivor is `p`-trivial inside each active `wu2` slice,
- there are `0` clean survivors with genuine dependence on the new exact bit inside that live gadget.

Interpretation:

- the exact bit is neither a viable standalone controller (`014`)
- nor a viable one-bit secondary refinement of the existing `wu2` mixed mechanism (`015`).

## Bottleneck evolution

The D5 bottleneck has moved through the following exact stages:

1. clean frame absent,
2. Latin infeasibility,
3. dynamic collapse,
4. missing hidden-phase information,
5. `U_0` triviality,
6. separation of cycle-only and monodromy-only mechanisms,
7. existence of a mixed regime,
8. failure to improve mixed geometry,
9. exhaustion of obvious one-bit exact refinements inside the live mixed branch.

So the current obstruction is not “mixed dynamics do not exist.”
It is:

> the project has a stable mixed mechanism, but every exact local refinement tested so far either preserves the same mixed geometry or worsens it.

## What is now established

### Proved or theorem-level within the project

- orbit-anchor reconstruction,
- master-field conditional theorem,
- strict-collapse law on the joined-quotient pilot branch,
- earlier color-by-color structural results from the pre-master-field phase.

### Exact computationally established on the pilot range

- discrete hidden-phase incidence-signature quotient on nonzero tail phase,
- exact pilot bits `b1` and `b2`,
- passive divergence beyond the lifted collapse field,
- existence of many clean strict witnesses with nontrivial `U_0`,
- existence of a clean strict mixed regime (`008`),
- robustness of the `wu2` mixed gadget under substantial widening (`009`),
- genuine layer-2/layer-3 interaction that is anti-compressive rather than positive (`010`),
- twist-sign irrelevance for geometry in the fixed-twist family (`011`),
- new geometry classes from larger layer-2 state, all anti-compressive (`012`, `013`),
- exact new bit `pred_sig1_phase_align`, locally real but globally sterile in one-bit roles (`014`, `015`).

### Exact failures now known

- tail-only context dependence does not survive the clean-frame stage in the strict-friendly two-anchor family,
- the smallest active `(b1,b2)` neighborhood around the strict seed,
- decoupled two-old-bit families as a route to mixed dynamics,
- named predecessor-phase widenings as a route to improved mixed geometry,
- the one-bit exact signature as a standalone controller,
- the one-bit exact signature as a secondary controller inside the live `wu2` mixed gadget.

## Current mechanism picture

The cleanest way to summarize the current D5 picture is:

### 1. Layer 2 controls geometry

Layer-2 old-bit structure determines the base `U_0` cycle geometry.
It can produce:

- trivial geometry,
- cycle-only geometry,
- the baseline mixed geometry,
- or anti-compressive geometry classes.

### 2. The live layer-3 gadget controls holonomy

The first genuinely successful mixed gadget is the predecessor-based `wu2` switch from `008`.
It injects uniform nonzero monodromy while preserving a good geometry class.

### 3. The current failure is not lack of interaction, but wrong-signed interaction

`010` shows genuine shared interaction exists.
`012` and `013` show richer local state creates many new geometries.
But the interaction is currently wrong-signed:

- it preserves the old baseline mixed geometry,
- or pushes the system into more cycles / more fixed points,
- rather than compressing cycles below the baseline.

### 4. The new exact bit is real, but not yet structurally useful

`pred_sig1_phase_align` is a true local refinement of the predecessor-tail signature.
But on the current exact searches:

- as a layer-2 refinement it is pilot-return sterile,
- as a standalone layer-3 controller it is ignored,
- as a secondary refinement inside the `wu2` gadget it collapses to `p`-trivial behavior.

## Current best baseline

The exact D5 pilot baseline to beat is now the Session 26 mixed regime:

- clean,
- strict-clock,
- full-color Latin,
- on `m=5,7,9`:
  - `U_0` has exactly `m` cycles of length `m`,
  - every cycle has uniform monodromy `m-2`.

Equivalently:

- total pilot cycle count `21`,
- no exact refinement after `008` has improved on that total.

## Recommended next branch

The smallest honest next branch is no longer another one-bit refinement.

The strongest evidence from `014` and `015` is:

- the live mixed mechanism is real,
- the obvious one-bit exact refinement is exhausted,
- the next credible gain requires either:
  - a second exact local bit,
  - or a minimally synchronized two-layer local controller where two small states act together.

So the next branch should look like:

- keep the live `wu2` mixed gadget as the reference mechanism,
- introduce one additional exact local state beyond `pred_sig1_phase_align`,
- or search a genuinely synchronized two-layer controller rather than a separable layer-2 refinement or one-bit layer-3 patch.

What should *not* be reopened first:

- more one-bit variants of `pred_sig1_phase_align`,
- more twist-sign flips,
- more pure named predecessor-phase widenings without new exact state.

## Compact milestone table

| Artifact | Exact result | Takeaway |
|---|---|---|
| `001` | exact `tail_cut`, but lifted collapse field remains optimal | one-bit tail cut alone is inert |
| `002` | passive divergence plus exact `b2` | passive branch richer than first thought |
| `003` | smallest active `(b1,b2)` family collapses back to seed | minimal two-bit seed neighborhood exhausted |
| `004` | context-only strict family collapses to constants | tail-context alone does not survive clean stage |
| `005` | first nontrivial `U_0` | cycle-only and monodromy-only mechanisms exist |
| `006` | decoupled alt-`0` family is all cycle-only | layer 3 can be dynamically invisible |
| `007` | cycle-only / monodromy-only / trivial trichotomy | right palette exists, but still no mixing |
| `008` | first clean strict mixed regime | predecessor `wu2` switch is the first live mixed gadget |
| `009` | mixed gadget is very robust, but never improves geometry | holonomy survives without geometric gain |
| `010` | shared switch creates real interaction, but anti-compressively | interaction exists but is wrong-signed |
| `011` | fixed-twist geometry is insensitive to twist sign | twist is not the geometry knob |
| `012` | two-flag layer-2 state creates new regimes `35/57/119/...` | richer state, still all anti-compressive |
| `013` | three-flag widenings add no new positive regime | named extra flags are dynamically sterile |
| `014` | exact new bit `pred_sig1_phase_align` found, but one-bit roles fail | exact refinement exists, but is globally sterile alone |
| `015` | exact bit fails even inside the live `wu2` mixed gadget | one-bit exact refinement path is exhausted |

## Bottom line

The D5 program has passed the old “dynamic collapse” stage.
It now has an exact, validated, clean strict mixed mechanism.

The current exact statement is:

> on the pilot range `m=5,7,9`, the project already has stable mixed witnesses, but every local refinement tested after that breakthrough either reproduces the same mixed geometry or worsens it.

So the next honest move is not a fresh global redesign.
It is a small but real jump in local state complexity: a two-bit exact refinement or a minimally synchronized two-layer controller built around the already-live `wu2` mixed gadget.
